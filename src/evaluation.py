"""
평가 지표와 실험 기록  ·  담당: ③ 안주형 (수정하면 디스코드에 공유)
"""
import csv
from datetime import datetime

import pandas as pd
from sklearn.metrics import classification_report, f1_score

from .config import EXPERIMENT_DIR


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
