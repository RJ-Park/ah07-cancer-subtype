"""
공통 설정  ·  담당: ④ 박유정 (팀 전원이 같은 값을 써요. 바꿀 일이 있으면 팀에 먼저 공유)

- 경로는 이 파일 위치를 기준으로 자동 계산돼요. 로컬, Colab(드라이브) 어디서든 그대로 동작해요.
- 최종 제출 코드에서는 DATA_DIR을 "/data"로 바꿔요 (환경변수 DATA_DIR로도 지정 가능).
"""
import os
import random
from pathlib import Path

import numpy as np

# ── 재현성 ───────────────────────────────────────────
SEED = 42
N_SPLITS = 5
DEVICE = "auto" j# auto / cpu / cuda
# ── 컬럼 ────────────────────────────────────────────
TARGET = "SUBCLASS"
ID_COL = "ID"

# ── 경로 ────────────────────────────────────────────
REPO_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("DATA_DIR", REPO_DIR / "data"))
EXPERIMENT_DIR = REPO_DIR / "experiments"     # 실험 기록 (깃허브에 올라감)
FIGURE_DIR = REPO_DIR / "reports" / "figures"  # 발표용 그래프 (깃허브에 올라감)
MODEL_DIR = REPO_DIR / "models"               # 학습된 모델 (깃허브에 안 올라감)
SUBMISSION_DIR = REPO_DIR / "submissions"     # 제출 csv (깃허브에 안 올라감)


def set_seed(seed: int = SEED) -> None:
    """파이썬, numpy 난수 seed 고정. 모델의 random_state에도 SEED를 넣어 주세요."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
