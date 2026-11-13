"""Fixed holdout manifest: generate once, commit CSV, then only load/verify.
Run at project root: python scripts/fixed_holdout_manifest.py --create
                    python scripts/fixed_holdout_manifest.py --verify
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import LabelEncoder

SEED = 42
# 스크립트 위치를 기준으로 프로젝트 루트 자동 탐색
ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data" / "train.csv"
MANIFEST = ROOT / "data" / "splits" / "holdout_seed42.csv"
META = ROOT / "data" / "splits" / "holdout_seed42_meta.json"

def manifest_sha256(path: Path) -> str:
    """Hash CSV consistently across LF/CRLF checkouts.

    The committed legacy metadata stores the CRLF-form hash. Normalize
    line endings in memory only; never rewrite the manifest itself.
    """
    raw = path.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    return hashlib.sha256(normalized).hexdigest()


def data():
    df = pd.read_csv(DATA_PATH, low_memory=False)
    required = {'ID', 'SUBCLASS'}
    if not required.issubset(df):
        raise ValueError('Missing ID or SUBCLASS')
    if df.ID.isna().any() or df.ID.astype(str).duplicated().any():
        raise ValueError('ID must be non-null and unique')
    genes = df.drop(columns=['ID','SUBCLASS'])
    return df, genes

def signatures(df, genes):
    # Stable per-row signature independent of Python hash randomization.
    # Uses pandas hashing only for change detection; manifest is authoritative.
    return pd.util.hash_pandas_object(genes.fillna('<MISSING>').astype(str), index=False).astype('uint64').astype(str)

def create():
    if MANIFEST.exists() or META.exists():
        raise FileExistsError('Manifest already exists; refusing to overwrite')
    df, genes = data()
    y = LabelEncoder().fit_transform(df.SUBCLASS.astype(str))
    groups = pd.util.hash_pandas_object(genes.fillna('<MISSING>').astype(str), index=False).to_numpy()
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    dev, hold = next(iter(cv.split(genes, y, groups)))
    if set(groups[dev]) & set(groups[hold]):
        raise AssertionError('Group leakage')
    sig = signatures(df, genes)
    manifest = pd.DataFrame({'ID':df.ID.astype(str), 'split': 'dev', 'row_signature':sig})
    manifest.loc[hold, 'split'] = 'holdout'
    MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    manifest.to_csv(MANIFEST,index=False,encoding='utf-8')
    metadata = {'seed':SEED,'algorithm':'StratifiedGroupKFold first split; full raw row groups',
                'n_dev':len(dev),'n_holdout':len(hold),'n_total':len(df),
                'manifest_sha256':manifest_sha256(MANIFEST),
                'pandas':pd.__version__}
    import sklearn
    metadata['scikit_learn'] = sklearn.__version__
    META.write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Created:',metadata)

def verify():
    df, genes = data()
    if not MANIFEST.exists() or not META.exists():
        raise FileNotFoundError('Ask owner to commit manifest and metadata; do not regenerate')
    meta=json.loads(META.read_text(encoding='utf-8'))
    assert manifest_sha256(MANIFEST) == meta['manifest_sha256'], 'Manifest changed'
    m=pd.read_csv(MANIFEST,dtype={'ID':str,'split':str,'row_signature':str})
    assert len(m)==len(df) and m.ID.is_unique and set(m.split)=={'dev','holdout'}
    assert set(m.ID)==set(df.ID.astype(str)), 'ID sets differ'
    current=pd.DataFrame({'ID':df.ID.astype(str),'row_signature':signatures(df,genes)})
    merged=current.merge(m,on='ID',validate='one_to_one',suffixes=('_current','_saved'),sort=False)
    assert len(merged)==len(df), 'IDs missing'
    assert (merged.row_signature_current==merged.row_signature_saved).all(), 'Dataset content differs'
    dev=np.flatnonzero(merged.split.eq('dev').to_numpy())
    hold=np.flatnonzero(merged.split.eq('holdout').to_numpy())
    assert len(dev)==meta['n_dev'] and len(hold)==meta['n_holdout']
    raw_hash=pd.util.hash_pandas_object(genes.fillna('<MISSING>').astype(str),index=False).to_numpy()
    assert not(set(raw_hash[dev]) & set(raw_hash[hold])), 'Group leakage'
    print(f"VERIFIED: dev={len(dev)}, holdout={len(hold)}; same IDs and row signatures")
    return dev,hold

if __name__=='__main__':
    p=argparse.ArgumentParser()
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--create',action='store_true')
    mode.add_argument('--verify',action='store_true')
    args=p.parse_args()
    create() if args.create else verify()
