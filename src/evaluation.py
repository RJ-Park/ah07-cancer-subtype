"""
평가 지표, 실험 기록, 예측 저장  ·  담당: ③ 안주형 (수정하면 디스코드에 공유)
"""
import csv
import json
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, f1_score

from .config import EXPERIMENT_DIR

PRED_DIR = EXPERIMENT_DIR / "preds"


def macro_f1(y_true, y_pred) -> float:
    """대회 평가 지표: Macro F1 (26개 클래스를 같은 비중으로 평균)."""
    return f1_score(y_true, y_pred, average="macro")


def per_class_f1(y, oof, class_names) -> pd.DataFrame:
    """클래스별 F1 (낮은 순). Macro F1을 끌어내리는 클래스를 찾을 때 써요."""
    report = classification_report(y, oof, labels=range(len(class_names)), target_names=class_names,
                                   output_dict=True, zero_division=0)
    return (pd.DataFrame(report).T.loc[list(class_names), ["f1-score", "support"]]
            .sort_values("f1-score"))


LOG_COLUMNS = ["date", "owner", "notebook", "experiment", "features", "model", "params",
               "cv_mean", "cv_std", "lb_score", "notes"]


def log_result(owner: str, notebook: str, experiment: str, features: str, model: str,
               params, cv: dict, notes: str = "") -> None:
    """
    실험 결과를 experiments/log_{owner}.csv 에 한 줄 추가해요.
    owner: J_leader / H_data / A_model / P_light 중 자기 것 (각자 자기 파일에만 써서 충돌 없음)
    lb_score(리더보드 점수)는 제출한 뒤 팀장이 채워요.
    """
    EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
    path = EXPERIMENT_DIR / f"log_{owner}.csv"
    new = not path.exists() or path.stat().st_size == 0
    with open(path, "a", newline="", encoding="utf-8-sig" if new else "utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
        if new:
            w.writeheader()
        w.writerow({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "owner": owner, "notebook": notebook, "experiment": experiment,
            "features": features, "model": model, "params": str(params),
            "cv_mean": round(cv["mean"], 4), "cv_std": round(cv["std"], 4),
            "lb_score": "", "notes": notes,
        })
    print(f"기록: {path.name} ← {experiment} (CV {cv['mean']:.4f})")


# ── 앙상블용 예측 저장 규칙 ─────────────────────────────────────
# 앙상블 후보가 된 모델만 저장해요. 모두 같은 형식이어야 05_ensemble에서 섞을 수 있어요.
#   oof_proba  : run_cv()의 cv["oof_proba"]  (행 = train 순서, 열 = le.classes_ 순서)
#   test_proba : 전체 train으로 학습한 모델의 test 예측 확률 (행 = test 순서, 열 = le.classes_ 순서)
# 파일: experiments/preds/{owner}__{name}__oof.npy / __test.npy / __meta.json

def save_predictions(owner: str, name: str, oof_proba, test_proba, classes, cv: dict, notes: str = "") -> None:
    """앙상블 후보 모델의 예측 확률을 정해진 형식으로 저장해요."""
    oof_proba = np.asarray(oof_proba, dtype=np.float32)
    test_proba = np.asarray(test_proba, dtype=np.float32)
    classes = [str(c) for c in classes]
    assert oof_proba.ndim == 2 and oof_proba.shape[1] == len(classes), "oof_proba 열 수가 클래스 수와 달라요"
    assert test_proba.ndim == 2 and test_proba.shape[1] == len(classes), "test_proba 열 수가 클래스 수와 달라요"
    assert "__" not in owner and "__" not in name, "owner, name에 '__'(밑줄 두 개)는 쓰지 마세요"
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    stem = PRED_DIR / f"{owner}__{name}"
    np.save(f"{stem}__oof.npy", oof_proba)
    np.save(f"{stem}__test.npy", test_proba)
    meta = {"owner": owner, "name": name, "classes": classes,
            "cv_mean": round(cv["mean"], 4), "cv_std": round(cv["std"], 4),
            "n_train": int(oof_proba.shape[0]), "n_test": int(test_proba.shape[0]),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"), "notes": notes}
    with open(f"{stem}__meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"예측 저장: {stem.name} (CV {cv['mean']:.4f}) → experiments/preds/")


def load_predictions(classes=None) -> dict:
    """experiments/preds/ 의 모든 예측을 불러와요. classes를 주면 클래스 순서가 같은지 확인해요."""
    out = {}
    for meta_path in sorted(PRED_DIR.glob("*__meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        stem = str(meta_path)[: -len("__meta.json")]
        if classes is not None:
            assert meta["classes"] == [str(c) for c in classes], f"{meta_path.name}: 클래스 순서가 달라요"
        key = f"{meta['owner']}__{meta['name']}"
        out[key] = {"oof": np.load(f"{stem}__oof.npy"), "test": np.load(f"{stem}__test.npy"), "meta": meta}
    print(f"불러온 예측 {len(out)}개: {list(out)}")
    return out
