"""
예측과 제출 파일  ·  담당: ④ 박유정 (수정하면 디스코드에 공유)

리더보드 제출은 팀장을 통해서만 해요 (하루 4회).
"""
from pathlib import Path

import pandas as pd

from .config import DATA_DIR, ID_COL, SUBMISSION_DIR, TARGET


def make_submission(test: pd.DataFrame, pred_labels, file_name: str, data_dir=DATA_DIR) -> pd.DataFrame:
    """sample_submission 형식에 맞춰 submissions/{file_name} 으로 저장하고 형식을 검증해요."""
    sub = pd.read_csv(Path(data_dir) / "sample_submission.csv")
    assert len(sub) == len(pred_labels), "예측 개수가 제출 양식과 달라요"
    assert (sub[ID_COL].values == test[ID_COL].values).all(), "ID 순서가 제출 양식과 달라요"
    sub[TARGET] = pred_labels
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    out = SUBMISSION_DIR / file_name
    sub.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"저장: {out} ({len(sub)}행)")
    return sub
