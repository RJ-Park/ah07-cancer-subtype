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
