# ah07-cancer-subtype

AI 헬스케어 7기 해커톤 · **유전자 변이 정보 기반 암 아형(SUBCLASS) 분류**

- 과제: 환자별 유전자 변이(유전자 4,384개, `WT` 또는 변이 표기)로 26개 암 아형 예측
- 평가: Macro F1 (Public = Test 100%), 하루 제출 4회
- 일정: 11/11(수) 모든 제출 완료 → 11/12 리허설 → 11/13 발표
- 팀 기준 점수: **CV Macro F1 0.3209** (`notebooks/J_leader/00_baseline.ipynb`, XGBoost + 기본 피처)

> 처음 왔다면 **[AI_RULES.md](AI_RULES.md)** 부터 읽어 주세요. 누수 하나면 실격이에요.

## 폴더 구조

| 경로 | 내용 | 수정하는 사람 | 깃허브 |
|---|---|---|---|
| `AI_RULES.md` | AI에게 먼저 붙여넣는 규칙 | ① 장성은 | 올림 |
| `data/` | 대회 csv 3개 (각자 넣기) | - | **안 올림** |
| `src/config.py` | seed, fold 수, 경로 | ④ 박유정 | 올림 |
| `src/data_loader.py` | 데이터 불러오기 | ④ 박유정 | 올림 |
| `src/preprocessing.py` | 기본 전처리 (WT=0, 변이=1) | ② 홍시윤 | 올림 |
| `src/features.py` | **검증된** 공통 피처 | ② 홍시윤 | 올림 |
| `src/validation.py` | 공통 교차검증 (fold, run_cv) | ③ 안주형 | 올림 |
| `src/evaluation.py` | Macro F1, 클래스별 F1, 실험 기록 | ③ 안주형 | 올림 |
| `src/prediction.py` | 제출 파일 만들기 | ④ 박유정 | 올림 |
| `notebooks/J_leader/` | 00_baseline (팀 기준 점수) | ① 장성은 | 올림 |
| `notebooks/H_data/` | 01_eda, 02_features | ② 홍시윤 | 올림 |
| `notebooks/A_model/` | 03_models (+ 앙상블) | ③ 안주형 | 올림 |
| `notebooks/P_light/` | 04_lightweight | ④ 박유정 | 올림 |
| `experiments/log_*.csv` | 실험 기록 (사람별 1개) | 각자 자기 파일 | 올림 |
| `reports/figures/` | 발표용 그래프 | 전원 | 올림 |
| `submit/` | 최종 제출용 통합 파일 1개 | ④ 박유정 | 올림 |
| `docs/` | 조사 자료, 확정된 역할분담 (md) | 전원 | 올림 |
| `models/` | 학습된 모델 파일 | - | **안 올림** |
| `submissions/` | 제출 csv | - | **안 올림** |

실험 기록 파일: `log_J_leader.csv` · `log_H_data.csv` · `log_A_model.csv` · `log_P_light.csv`

## 시작하기

### 1. 데이터 넣기
데이콘에서 받은 `train.csv`, `test.csv`, `sample_submission.csv`를 `data/` 폴더에 넣어요.

### 2-A. Colab
1. 깃허브 레포 페이지 왼쪽 위 브랜치가 **develop**인지 확인하고, **Code → Download ZIP**으로 받아 압축을 풀어요.
2. 폴더 이름을 `ah07-cancer-subtype`으로 맞추고, 구글 드라이브 `내 드라이브`에 통째로 올려요. 그 안 `data/`에 csv를 넣어요.
3. 드라이브에서 자기 폴더의 노트북(예: `notebooks/A_model/03_models.ipynb`)을 Colab으로 열고 위에서부터 실행해요. 첫 셀이 드라이브를 자동으로 연결해요.
4. 작업이 끝나면 **파일 → GitHub에 사본 저장**을 눌러요. 브랜치는 **자기 브랜치**(예: `feature/A_model`), 경로는 `notebooks/자기폴더/파일이름`으로 올려요. 처음 한 번은 깃허브 권한 허용이 필요하고, "비공개 저장소 포함"에 체크해야 레포가 보여요.
5. 깃허브 레포 페이지에서 **Pull request**를 만들어요 (아래 "브랜치와 PR" 참고).
6. 다른 사람의 `src/` 변경이 develop에 합쳐졌다면, develop 브랜치 ZIP을 다시 받아 `src/` 폴더만 바꿔 넣어요.

### 2-B. VS Code / Jupyter (로컬)
```bash
git clone https://github.com/jsejj87/ah07-cancer-subtype.git
```
```bash
pip install -r requirements.txt
```
`data/`에 csv를 넣고, 커밋 템플릿을 한 번 등록해요.
```bash
git config --local commit.template .github/commit_template.txt
```
그다음 자기 브랜치로 옮겨서 작업해요 (아래 "브랜치와 PR").

## 실험하는 법

모든 노트북 첫 부분(환경 설정, 데이터 불러오기)은 이미 들어 있어요. 아래처럼 실험해요.

```python
from xgboost import XGBClassifier
PARAMS = dict(n_estimators=200, max_depth=6, random_state=SEED)

pipe = Pipeline([
    ("features", basic_transformer()),      # 전처리는 Pipeline 안에 (fold 안에서만 fit)
    ("model", XGBClassifier(**PARAMS)),
])
cv = run_cv(pipe, X, y, folds=folds)        # 모두 같은 fold, 같은 지표
per_class_f1(y, cv["oof"], le.classes_)     # 어떤 클래스가 약한지
# cv["oof_proba"]: fold 밖 예측 확률 (앙상블용, 행=train 순서, 열=le.classes_ 순서)
log_result(owner="A_model", notebook="03_models.ipynb", experiment="xgb_depth8",
           features="basic", model="XGBoost", params=PARAMS, cv=cv)   # 기록
```

## 브랜치와 PR

```
feature/이니셜_역할  ──PR(1명 승인)──▶  develop  ──(최종, 팀장)──▶  main
```

| 브랜치 | 용도 | 누가 올리나 |
|---|---|---|
| `main` | 최종 제출본만 | 팀장이 develop에서 합침 (11/11) |
| `develop` | 팀이 같이 쓰는 최신본 | PR로만 합침 (직접 push 금지) |
| `feature/J_leader` · `feature/H_data` · `feature/A_model` · `feature/P_light` | 각자 작업 | 본인 |

**PR 규칙:** develop으로 PR을 올리면 **본인 말고 팀원 아무나 1명**이 PR 템플릿의 누수 체크리스트를 보고 Approve → 병합해요. 누수가 애매하면 팀장에게 넘겨요.

**VS Code에서 매일 하는 순서**
```bash
git checkout feature/A_model
```
```bash
git pull origin develop
```
작업 → 자기 파일만 add → commit → push
```bash
git push origin feature/A_model
```
그다음 깃허브에서 **Compare & pull request** → base를 **develop**으로 → PR 생성.

## 협업 규칙

1. **자기 폴더만 수정해요.** `.ipynb`는 같은 파일을 둘이 고치면 합칠 수 없어요. 새 실험 노트북은 자기 폴더 안에 자유롭게 만들어요.
2. **`src/`는 담당자만 수정해요.** 바꾸면 디스코드에 알려 주세요. 다른 사람은 develop에 합쳐진 뒤 `git pull origin develop`으로 받아요.
3. **피처는 검증된 것만 `src/features.py`로.** 노트북에서 `run_cv()` 점수가 오르는 게 확인된 것만 옮겨요.
4. **리더보드 제출은 팀장을 통해서만** (하루 4회). 제출하고 싶은 후보는 기록표의 CV 점수와 함께 알려 주세요.
5. **원본 데이터, 모델 파일, 제출 csv, 가상환경, API 키는 올리지 않아요.** `.gitignore`가 대부분 막아 줘요.
6. **이전 대회나 공개 코드는 복사하지 않아요.** 외부 데이터는 쓰지 않아요.
