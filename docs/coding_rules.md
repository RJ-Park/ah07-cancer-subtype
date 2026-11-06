# 팀 코딩 규칙

코드를 어떻게 짜든(직접 작성, AI 도구 활용 등) **결과 코드가 아래 규칙을 지키면 돼요.**
확인은 PR 리뷰에서 PR 양식의 체크리스트로 해요. 하나라도 어기면 수상에서 제외되니, 애매하면 혼자 판단하지 말고 팀장에게 물어봐 주세요.

## 1. 데이터 누수 금지 (가장 중요)

| 하면 안 되는 것 | 이렇게 해요 |
|---|---|
| train과 test를 합쳐서(`concat`) 전처리 | train으로만 기준을 만들고 test에는 적용만 |
| 전체 X에 인코더·스케일러·결측 대체·피처 선택을 fit 한 뒤 fold 나누기 | 이런 변환은 **sklearn Pipeline 안에** 넣어서 `run_cv()`가 fold마다 다시 fit 하게 |
| test에 `pd.get_dummies()` 따로 쓰기, `align()`으로 test에 맞춰 컬럼 정하기 | train으로 fit 한 변환기로 test를 transform |
| test의 통계(평균·최빈값·분포·결측 개수), index, 행 개수 사용 | test는 **형식 확인과 최종 추론에만** |
| test를 EDA 해서 얻은 정보로 전처리 정하기 | EDA는 train으로만 |
| test에 가짜 라벨을 붙여 재학습 (pseudo-labeling) | 사용하지 않음 |

**괜찮은 것:** 한 행 안에서만 하는 계산(WT=0·변이=1, 환자별 변이 개수, 변이 표기에서 유형 뽑기), train 통계로 test를 처리하는 것.

## 2. 재현성

- 모든 난수 고정: `set_seed(SEED)`, 모델에 `random_state=SEED` (CatBoost는 `random_seed=SEED`, LightGBM은 `deterministic=True, force_row_wise=True`도 같이)
- 하이퍼파라미터는 코드에 숫자로 (dict로 정의해서 `log_result()`에 넘기기)
- 최종 제출에 쓸 모델은 CPU로 학습

## 3. 코드 출처

- 외부 데이터 사용 금지
- 이전 데이콘 대회(특히 2024년 같은 주제 대회)·다른 대회의 공개 코드나 수상 코드를 가져오거나 따라 하지 않기
- 사전학습 모델은 논문으로 공개된 것만, 논문 링크를 주석으로

## 4. 공통 코드 사용 (새로 만들지 말고 이걸 써요)

| 파일 | 함수 | 담당 |
|---|---|---|
| `src/config.py` | `SEED`(42), `N_SPLITS`(5), `DATA_DIR`, `set_seed()` | ④ |
| `src/data_loader.py` | `load_data()`, `split_xy()`, `encode_target()` | ④ |
| `src/preprocessing.py` | `binarize_mutations()`, `basic_transformer()` | ② |
| `src/features.py` | 검증된 공통 피처 (`mutation_count()` 등) | ② |
| `src/validation.py` | `get_folds()`, `run_cv()`, `balanced_weights()` | ③ |
| `src/evaluation.py` | `macro_f1()`, `per_class_f1()`, `log_result()`, `save_predictions()`, `load_predictions()` | ③ |
| `src/prediction.py` | `make_submission()` | ④ |

노트북 첫 셀(환경 설정)은 고치지 않아요.

## 5. 실험 작성 순서

1. `pipe = Pipeline([("features", 전처리·피처), ("model", 모델(**PARAMS))])`
2. `cv = run_cv(pipe, X, y, folds=folds)`: 빠른 확인은 `folds=folds[:1]`, **기록은 5-fold로만**
3. `per_class_f1(y, cv["oof"], le.classes_)`: 약한 클래스 확인
4. `log_result(owner="내 owner", ...)`: 자기 기록표에 기록 (owner: `J_leader` / `H_data` / `A_model` / `P_light`)
5. 앙상블 후보면: 전체 train으로 fit → `test_proba` → `save_predictions(...)`

## 6. 협업

- 자기 브랜치(`feature/이니셜_역할`)에서 **자기 폴더만** 수정해요. 담당이 아닌 `src/` 파일은 담당자에게 요청해요.
- develop에는 PR로만 합쳐요. 팀원 1명이 승인한 뒤에 Merge해요. main은 팀장만 합쳐요.
- csv, 모델 파일(.pkl 등), API 키는 커밋하지 않아요.
- 코드는 **직접 설명할 수 있어야** 해요. 코드 검증과 발표 질의응답에서 물어볼 수 있어요.

---

## (선택) AI 도구를 쓸 때

AI 도구로 코드를 짠다면, 아래 요약을 첫 메시지로 주면 위 규칙에 맞는 코드를 받기 쉬워요. 쓰지 않아도 돼요. 결과 코드가 규칙만 지키면 돼요.

```text
데이콘 해커톤 팀 작업이야. 아래 규칙을 지켜서 코드를 짜줘.
[나] 역할: (예: ② 데이터·피처) / 폴더: (예: notebooks/H_data/) / 담당 src: (예: src/preprocessing.py, src/features.py)
[과제] 유전자 변이(4,384개 컬럼, 값은 "WT" 또는 "R132H" 같은 변이 표기)로 암 아형 SUBCLASS 26개를 분류. 평가 Macro F1.
[누수 금지] 학습하는 변환(인코더·스케일러·결측 대체·피처 선택)은 sklearn Pipeline 안에 넣어 fold 학습 부분에만 fit.
  train+test concat 금지, test에 get_dummies 금지, test 통계·EDA·행 개수 사용 금지, pseudo-labeling 금지. 한 행 안의 계산은 허용.
[재현] set_seed(SEED), random_state=SEED, 하이퍼파라미터는 숫자로. 외부 데이터·공개 대회 코드 금지.
[공통 함수 사용] load_data, split_xy, encode_target / basic_transformer / get_folds, run_cv / per_class_f1, log_result, save_predictions / make_submission
  점수는 run_cv(pipe, X, y, folds=folds)로, 기록은 log_result()로. 노트북 첫 셀은 고치지 마.
[협업] 내 폴더 파일만 수정. 한국어 주석으로 설명하고, 누수 가능성이 있으면 먼저 경고해줘.
```
