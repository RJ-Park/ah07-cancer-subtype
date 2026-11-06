"""
데이터 불러오기  ·  담당: ④ 박유정 (수정하면 디스코드에 공유)

test는 형식 확인과 최종 추론에만 써요. test의 통계나 분포는 보지 않아요.
"""
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from .config import DATA_DIR, ID_COL, TARGET


def load_data(data_dir=DATA_DIR):
    """train, test를 읽고, test 컬럼이 train과 같은지(형식)만 확인해요."""
    data_dir = Path(data_dir)
    train = pd.read_csv(data_dir / "train.csv")
    test = pd.read_csv(data_dir / "test.csv")
    feature_cols = [c for c in train.columns if c not in (ID_COL, TARGET)]
    assert list(test.columns) == [ID_COL] + feature_cols, "test 컬럼이 train과 달라요"
    return train, test


def split_xy(train: pd.DataFrame):
    """train을 입력(X)과 정답(y)으로 나눠요."""
    X = train.drop(columns=[ID_COL, TARGET])
    y = train[TARGET]
    return X, y


def encode_target(y):
    """정답 라벨(문자) → 숫자. train 정답에만 fit 해요. le.inverse_transform()으로 되돌려요."""
    le = LabelEncoder().fit(y)
    return le.transform(y), le
