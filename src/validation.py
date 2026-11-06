"""
공통 검증 코드  ·  담당: ③ 안주형 (초안, 킥오프에서 함께 확정. 수정하면 디스코드에 공유)

팀 전원이 이 함수로 점수를 내야 서로 비교할 수 있어요.
- 같은 fold 분할 (Stratified K-Fold, N_SPLITS=5, SEED=42)
- 같은 지표 (Macro F1, evaluation.py)

누수 방지: run_cv()는 모델(또는 Pipeline)을 fold마다 새로 복사(clone)해서
그 fold의 학습 부분에만 fit 해요. 전처리를 Pipeline 안에 넣으면 자동으로 지켜져요.

앙상블 준비: 모델에 predict_proba가 있으면 fold 밖 예측 확률(oof_proba)도 저장해요.
행 순서는 train 순서, 열 순서는 encode_target()의 클래스 순서(le.classes_)로 모두 같아요.
"""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold

from .config import N_SPLITS, SEED
from .evaluation import macro_f1


def get_folds(y, n_splits: int = N_SPLITS, seed: int = SEED):
    """팀 공통 fold 분할. 모두 이 함수를 써야 점수를 비교할 수 있어요."""
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    return list(skf.split(np.zeros(len(y)), y))


def run_cv(model, X: pd.DataFrame, y, folds=None, fit_params_fn=None, verbose: bool = True):
    """
    공통 교차검증.

    model         : sklearn 모델 또는 Pipeline (fold마다 clone → 학습 부분에만 fit)
    X, y          : split_xy(), encode_target()로 만든 train 데이터
    folds         : 생략하면 get_folds(y)
    fit_params_fn : fold의 학습 정답(y_tr)을 받아 fit()에 넘길 dict를 돌려주는 함수 (선택)
                    예) lambda y_tr: {"model__sample_weight": balanced_weights(y_tr)}

    반환: {"scores", "mean", "std", "oof"(fold 밖 예측 라벨), "oof_proba"(확률, 없으면 None)}
    """
    y = np.asarray(y)
    n_classes = len(np.unique(y))
    folds = folds if folds is not None else get_folds(y)
    oof = np.full(len(y), -1)
    oof_proba = None
    scores = []
    for k, (tr_idx, va_idx) in enumerate(folds):
        m = clone(model)
        fit_params = fit_params_fn(y[tr_idx]) if fit_params_fn else {}
        m.fit(X.iloc[tr_idx], y[tr_idx], **fit_params)
        X_va = X.iloc[va_idx]
        if hasattr(m, "predict_proba"):
            proba = m.predict_proba(X_va)
            if oof_proba is None:
                oof_proba = np.zeros((len(y), n_classes))
            oof_proba[va_idx] = proba
            oof[va_idx] = proba.argmax(axis=1)
        else:
            oof[va_idx] = np.asarray(m.predict(X_va)).ravel()
        score = macro_f1(y[va_idx], oof[va_idx])
        scores.append(score)
        if verbose:
            print(f"fold {k}: Macro F1 = {score:.4f}")
    result = {"scores": scores, "mean": float(np.mean(scores)), "std": float(np.std(scores)),
              "oof": oof, "oof_proba": oof_proba}
    if verbose:
        print(f"CV Macro F1 = {result['mean']:.4f} (std {result['std']:.4f})")
    return result


def balanced_weights(y_tr):
    """클래스 불균형 보정용 sample weight. fold의 학습 정답으로만 계산해요."""
    from sklearn.utils.class_weight import compute_sample_weight

    return compute_sample_weight("balanced", y_tr)
