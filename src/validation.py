"""팀 공통 검증: 쌍둥이 누수 방지 StratifiedGroupKFold. 담당: A_model.

쌍둥이: 전체 유전자 행 동일, 변이 유전자 2개 이상, 라벨이
KIPAN/KIRC 또는 GBMLGG/LGG인 상충 라벨 샘플.
"""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import StratifiedGroupKFold
from .config import N_SPLITS, SEED
from .evaluation import macro_f1

TWIN_PAIRS = (("KIPAN", "KIRC"), ("GBMLGG", "LGG"))


def twin_groups(X: pd.DataFrame, y, classes=None):
    """동일 원본 행의 지정된 상충 암종 쌍을 같은 그룹으로 묶음.

    X는 반드시 이진화 전 원본 유전자 행이며 ID/TARGET은 없어야 함.
    y가 숫자라면 classes=le.classes_ 를 필수로 전달.
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X는 원본 유전자 DataFrame이어야 합니다")
    labels = np.asarray(y)
    if len(X) != len(labels):
        raise ValueError("X와 y의 행 수가 다릅니다")
    if classes is not None:
        classes = np.asarray(classes)
        if not np.issubdtype(labels.dtype, np.integer):
            raise ValueError("classes를 주면 y는 0부터 시작하는 정수 라벨이어야 합니다")
        if labels.min() < 0 or labels.max() >= len(classes):
            raise ValueError("y 인코딩 범위가 classes와 다릅니다")
        names = classes[labels].astype(str)
    else:
        if np.issubdtype(labels.dtype, np.number):
            raise ValueError("숫자 y에는 classes=le.classes_가 필요합니다")
        names = labels.astype(str)

    # 결측과 'WT'를 구별한 원본 행 전체의 해시. 인덱스는 그룹 판정에 사용하지 않음.
    raw = X.reset_index(drop=True)
    row_hash = pd.util.hash_pandas_object(raw, index=False).to_numpy()
    n_mut = (raw.notna() & raw.ne("WT") & raw.ne("")).sum(axis=1).to_numpy()
    groups = np.arange(len(raw), dtype=np.int64)
    for a, b in TWIN_PAIRS:
        eligible = np.flatnonzero((n_mut >= 2) & np.isin(names, [a, b]))
        buckets = {}
        for i in eligible:
            buckets.setdefault(int(row_hash[i]), []).append(int(i))
        for indices in buckets.values():
            if len(indices) < 2 or not ({a, b} <= set(names[indices])):
                continue
            # 해시 충돌에 대비해 실제 전체 행 일치도 검사
            for i in indices:
                if groups[i] != i:
                    continue
                same = [j for j in indices if raw.iloc[j].equals(raw.iloc[i])]
                if {a, b} <= set(names[same]):
                    groups[same] = min(same)
    return groups


def get_folds(
    y,
    X=None,
    classes=None,
    n_splits=N_SPLITS,
    seed=SEED
):
    """
    팀 공통 StratifiedGroupKFold.

    get_folds(y)
        -> train.csv를 읽어 원본 X와 클래스 순서를 가져옴

    get_folds(y, X=X, classes=le.classes_)
        -> 전달받은 X와 클래스를 사용

    두 방식은 동일한 Fold를 생성해야 함.
    """
    from .config import DATA_DIR, ID_COL, TARGET
    from .data_loader import split_xy, encode_target

    y = np.asarray(y).ravel()

    if X is None:
        # test.csv는 읽지 않고 train만 사용
        train = pd.read_csv(DATA_DIR / "train.csv")

        if len(y) != len(train):
            raise ValueError(
                f"y 길이({len(y)})와 "
                f"train 길이({len(train)})가 다릅니다."
            )

        X, y_raw = split_xy(train)
        _, le = encode_target(y_raw)

        if classes is None:
            classes = le.classes_

    else:
        if len(y) != len(X):
            raise ValueError(
                f"y 길이({len(y)})와 "
                f"X 길이({len(X)})가 다릅니다."
            )

        if classes is None:
            raise ValueError(
                "X를 직접 전달할 때는 classes=le.classes_도 지정하세요."
            )

    groups = twin_groups(X, y, classes=classes)

    sgkf = StratifiedGroupKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=seed
    )

    folds = list(sgkf.split(X, y, groups=groups))

    for train_idx, val_idx in folds:
        if set(groups[train_idx]) & set(groups[val_idx]):
            raise RuntimeError(
                "동일 그룹이 학습/검증에 동시에 포함되었습니다."
            )

    return folds


def run_cv(model, X: pd.DataFrame, y, folds=None, fit_params_fn=None, verbose=True):
    """그룹 Fold를 반드시 명시. fold별 clone, OOF 확률의 클래스 순서 검증."""
    y = np.asarray(y)
    if folds is None:
        raise ValueError("get_folds(y, X=원본X, classes=le.classes_)로 생성한 folds를 전달하세요")
    classes = np.unique(y)
    if not np.array_equal(classes, np.arange(len(classes))):
        raise ValueError("y는 LabelEncoder로 0..K-1 인코딩되어야 합니다")
    oof = np.full(len(y), -1, dtype=int)
    oof_proba = None
    scores = []
    seen = np.zeros(len(y), dtype=int)
    for k, (tr_idx, va_idx) in enumerate(folds):
        tr_idx, va_idx = np.asarray(tr_idx), np.asarray(va_idx)
        if np.intersect1d(tr_idx, va_idx).size or np.any(seen[va_idx]):
            raise ValueError("Fold 중복 또는 Train/Validation 중첩")
        seen[va_idx] += 1
        m = clone(model)
        kwargs = fit_params_fn(y[tr_idx]) if fit_params_fn else {}
        m.fit(X.iloc[tr_idx], y[tr_idx], **kwargs)
        if hasattr(m, "predict_proba"):
            proba = np.asarray(m.predict_proba(X.iloc[va_idx]), dtype=float)
            model_classes = m.classes_ if hasattr(m, "classes_") else m[-1].classes_
            if not np.array_equal(np.asarray(model_classes), classes):
                raise ValueError("Fold 모델 클래스가 전체 클래스와 달라 확률 열을 정렬할 수 없습니다")
            if oof_proba is None:
                oof_proba = np.zeros((len(y), len(classes)), dtype=float)
            if proba.shape != (len(va_idx), len(classes)) or not np.isfinite(proba).all():
                raise ValueError("확률 배열의 형태 또는 값이 잘못되었습니다")
            oof_proba[va_idx] = proba
            oof[va_idx] = classes[np.argmax(proba, axis=1)]
        else:
            oof[va_idx] = np.asarray(m.predict(X.iloc[va_idx])).ravel()
        score = macro_f1(y[va_idx], oof[va_idx])
        scores.append(float(score))
        if verbose:
            print(f"fold {k+1}: Macro F1 = {score:.4f}")
    if not np.all(seen == 1):
        raise ValueError("OOF에 누락되거나 중복된 행이 있습니다")
    result = {"scores": scores, "mean": float(np.mean(scores)),
              "std": float(np.std(scores)), "oof": oof, "oof_proba": oof_proba}
    if verbose:
        print(f"CV Macro F1 = {result['mean']:.4f} (std {result['std']:.4f})")
    return result


def balanced_weights(y_tr):
    from sklearn.utils.class_weight import compute_sample_weight
    return compute_sample_weight("balanced", y_tr)
