"""
공통 피처  ·  담당: ② 홍시윤 (수정하면 디스코드에 공유)

여기에는 "효과가 검증된" 피처만 올려요. 실험 중인 피처는 각자 노트북에서 만들어 보고,
run_cv() 점수가 기본 피처보다 오르는 게 확인되면 이 파일로 옮겨요. (화요일 12시 확정)

규칙
- 한 행 안에서만 계산하는 피처는 여기 함수로 (train/test 통계를 쓰지 않으니 누수 없음)
- 피처 선택처럼 데이터로 학습하는 것은 sklearn Transformer로 만들어 Pipeline 안에 넣기
"""
import pandas as pd

from .preprocessing import binarize_mutations


def mutation_count(X: pd.DataFrame) -> pd.Series:
    """환자별 변이가 있는 유전자 개수."""
    return binarize_mutations(X).sum(axis=1).rename("n_mutated_genes")


# =====================공통 코드 끝=====================

# 변이 유형별 개수 피처 생성
# 원본 변이 문자열을 기준으로 환자별 변이 유형 개수를 계산

def mutation_type_counts(X):
    """
    환자별 변이 유형 개수 계산

    반환 피처:
    - n_missense
    - n_synonymous
    - n_nonsense
    - n_frameshift
    - n_other

    주의: 변이 표기 문자열을 기준으로 분류한 값이며,
    실제 생물학적 기능을 완전히 판정한 결과는 아님.
    """
    import re
    import pandas as pd

    feature_names = [
        "n_missense",
        "n_synonymous",
        "n_nonsense",
        "n_frameshift",
        "n_other",
    ]

    # 결측치와 WT를 제외한 실제 변이만 추출
    mutations = X.stack().dropna()
    mutations = mutations[mutations != "WT"]

    # 한 셀에 여러 변이가 있는 경우 각각 분리
    tokens = mutations.astype(str).str.split().explode().dropna()

    # 변이 표기 패턴에 따라 유형 분류
    def classify(token):
        if "fs" in token.lower():
            return "n_frameshift"

        if re.fullmatch(r"[A-Z]\d+\*", token):
            return "n_nonsense"

        if re.fullmatch(r"[A-Z]\d+[A-Z]", token):
            if token[0] == token[-1]:
                return "n_synonymous"
            return "n_missense"

        return "n_other"

    types = tokens.map(classify)

    # 환자별 변이 유형 개수 집계
    counts = pd.crosstab(
        tokens.index.get_level_values(0),
        types
    )

    result = counts.reindex(
        index=X.index,
        columns=feature_names,
        fill_value=0
    ).astype("int32")

    return result


def amino_acid_pair_counts(X: pd.DataFrame) -> pd.DataFrame:
    """
    환자별 아미노산 치환 쌍 개수 계산.

    예:
        V600E -> aa_V_E
        R132H -> aa_R_H

    - Missense와 synonymous 형태의 치환 표기만 집계
    - WT, 결측치 제외
    - 한 셀에 여러 변이가 있으면 각각 집계
    - 전체 아미노산 치환 쌍을 고정된 컬럼으로 반환
    - log1p는 모델 입력 단계에서 적용
    """
    import re

    amino_acids = "ACDEFGHIKLMNPQRSTVWY"
    pairs = [
        f"aa_{a}_{b}"
        for a in amino_acids
        for b in amino_acids
    ]

    # WT와 결측치 제외
    mutations = X.stack().dropna()
    mutations = mutations[mutations != "WT"]

    # 한 셀에 여러 변이가 있으면 분리
    tokens = mutations.astype(str).str.split().explode().dropna()

    # 아미노산 치환 표기 추출
    matches = tokens.str.extract(r"^([A-Z])\d+([A-Z])$")

    valid = (
        matches[0].isin(list(amino_acids))
        & matches[1].isin(list(amino_acids))
        & (matches[0] != matches[1])
    )
    matches = matches.loc[valid]

    # 치환 쌍 이름 생성
    pair_names = "aa_" + matches[0] + "_" + matches[1]

    # 환자별 치환 쌍 개수
    counts = pd.crosstab(
        pair_names.index.get_level_values(0),
        pair_names
    )

    return counts.reindex(
        index=X.index,
        columns=pairs,
        fill_value=0
    ).astype("int32")


def gene_truncation_flags(X: pd.DataFrame) -> pd.DataFrame:
    """
    유전자별 단백질 절단형 변이 여부.

    - Nonsense: R213*, E237* 등
    - Frameshift: fs가 포함된 변이 표기
    - 해당 유전자에 하나라도 존재하면 1, 없으면 0
    - 원본 유전자 컬럼별로 피처 생성
    """
    import re

    def has_truncation(value):
        if pd.isna(value):
            return 0

        tokens = str(value).split()

        return int(any(
            "fs" in token.lower()
            or re.fullmatch(r"[A-Z]\d+\*", token)
            for token in tokens
        ))

    result = X.apply(lambda col: col.map(has_truncation))

    result.columns = [
        f"trunc_{col}" for col in X.columns
    ]

    return result.astype("int8")