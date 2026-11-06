"""
기본 전처리  ·  담당: ② 홍시윤 (수정하면 디스코드에 공유)

팀 기본 피처: WT 또는 결측 = 0, 변이 = 1 (11/06 킥오프에서 합의할 초안)

값의 형태 (train 기준)
- "WT" : 변이 없음 (Wild Type). 전체 값의 약 99%
- 그 외 : 변이 표기. 예) "R132H", "V600E". 여러 개면 공백으로 구분 "R273C R248Q"
- 결측 : 변이 정보 없음 → WT와 같게 처리 (고정 규칙, 통계 사용 아님)

이 파일의 변환은 "한 행 안에서만" 계산해서 누수가 없어요.
데이터로 학습하는 변환(인코더, 스케일러 등)을 추가할 때는 sklearn Transformer로 만들어
Pipeline 안에 넣어요 (fold 안에서만 fit 되도록).
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import FunctionTransformer

WT = "WT"


def binarize_mutations(X: pd.DataFrame) -> pd.DataFrame:
    """[팀 기본 피처] WT 또는 결측 = 0, 변이 = 1."""
    return (X.notna() & (X != WT)).astype(np.int8)


def basic_transformer() -> FunctionTransformer:
    """Pipeline에 넣어 쓰는 기본 전처리 (상태가 없어 fit해도 아무것도 배우지 않음)."""
    return FunctionTransformer(binarize_mutations)
