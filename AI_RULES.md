# AI 작업 안내서 (AI에게 통째로 붙여넣기)

> **사용법:** AI(ChatGPT, Gemini, Claude, Copilot 등)에게 작업을 시키기 전에, 아래 `---- 여기부터 ----`부터 `---- 여기까지 ----`를 **통째로 복사해서 첫 메시지로** 붙여넣어 주세요. 맨 위 `[나]` 칸만 자기 정보로 바꿔요.
> Claude Code, Codex, Copilot은 레포의 `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`를 통해 이 파일을 자동으로 읽어요.
> 이 파일이 바뀌면 다시 붙여넣어 주세요. 기준은 항상 develop 브랜치의 최신본이에요.

---- 여기부터 ----

```text
너는 지금부터 우리 팀(4조)의 데이콘 해커톤 코드 작업을 돕는다. 아래 내용을 모두 기억하고, 규칙과 충돌하는 요청은 하지 말고 나에게 먼저 알려줘.

[나]
- 이름/역할: (예: ② 홍시윤 / 데이터·피처)
- 내 브랜치: (예: feature/H_data)
- 내 폴더: (예: notebooks/H_data/)
- 내가 담당하는 src 파일: (예: src/preprocessing.py, src/features.py / 없으면 "없음")

[과제]
- 환자별 유전자 변이로 암 아형 SUBCLASS(26개 클래스)를 예측하는 다중 분류.
- 데이터: train.csv(6,201행, ID + SUBCLASS + 유전자 4,384개), test.csv(2,546행, ID + 유전자 4,384개), sample_submission.csv.
- 유전자 값: "WT"(변이 없음, 전체의 약 99%) 또는 변이 표기("R132H", "V600E", 여러 개면 공백 구분 "R273C R248Q", "L42L" 같은 동의 변이, "R213*" 같은 넌센스 변이).
- 평가 지표: Macro F1 (26개 클래스를 같은 비중으로 평균). 하루 제출 4회, 제출은 팀장만.
- 시상: 리더보드 90% + 발표 10%. 데이터 누수, 코드 재현 불가, 외부 데이터, 기존 대회 코드 재사용 중 하나라도 걸리면 수상 제외.
- 팀 기준 점수: CV Macro F1 0.3209 (XGBoost + 기본 피처). 이것보다 오르면 개선.

[데이터 누수 금지 - 가장 중요]
- 인코더, 스케일러, 결측치 대체, 피처 선택, 차원 축소, 군집화 등 데이터로 "학습"하는 모든 변환은 train(교차검증에서는 각 fold의 학습 부분)에만 fit 하고, 검증/test에는 transform만 한다.
- 이런 변환은 sklearn Pipeline 안에 넣어서 run_cv()가 fold마다 다시 fit 하게 한다. fold를 나누기 전에 전체 X에 fit 하지 않는다.
- train과 test를 합치지(concat) 않는다. test에 pd.get_dummies()를 따로 쓰지 않는다. align()으로 test에 맞춰 컬럼을 정하지 않는다.
- test의 통계(평균, 최빈값, 분포, 결측 개수), index, 행 개수를 쓰지 않는다. test를 EDA하지 않는다. test는 컬럼 형식 확인과 최종 추론에만 쓴다.
- pseudo-labeling(test에 가짜 라벨을 붙여 재학습) 금지.
- 허용: 한 행 안에서만 하는 계산(WT를 0·변이를 1로, 환자별 변이 개수, 변이 표기에서 유형 추출 등), train 통계로 test를 처리하는 것.

[재현성]
- 모든 난수 고정: set_seed(SEED), 모델 random_state=SEED (CatBoost는 random_seed=SEED), LightGBM은 deterministic=True, force_row_wise=True도 같이.
- 하이퍼파라미터는 코드에 숫자로 직접 쓴다 (dict로 정의해서 log_result에 넘긴다).
- 최종 제출에 쓸 모델은 CPU로 학습한다.

[코드 출처]
- 외부 데이터 사용 금지. 이전 데이콘 대회(특히 2024년 같은 주제 대회)나 다른 대회의 공개 코드·수상 코드를 가져오거나 따라 하지 않는다. 이 대회를 위해 새로 작성한다.
- 사전학습 모델은 논문으로 공개된 것만, 논문 링크를 주석으로 남긴다.

[레포 구조와 공통 함수 - 새로 만들지 말고 이것을 쓴다]
- 노트북 첫 셀(환경 설정)은 고치지 않는다. REPO_DIR, DATA_DIR를 잡고 src를 import 할 수 있게 해준다.
- src/config.py      : SEED=42, N_SPLITS=5, DATA_DIR, set_seed()
- src/data_loader.py : load_data() → (train, test) / split_xy(train) → (X, y_raw) / encode_target(y_raw) → (y, le)
- src/preprocessing.py : binarize_mutations(X) (WT·결측=0, 변이=1), basic_transformer() (Pipeline용 기본 전처리)
- src/features.py    : 검증된 공통 피처 (mutation_count 등)
- src/validation.py  : get_folds(y) (팀 공통 5-fold), run_cv(model, X, y, folds=folds, fit_params_fn=None)
                       → {"scores","mean","std","oof","oof_proba"}, balanced_weights(y_tr)
- src/evaluation.py  : macro_f1, per_class_f1(y, oof, le.classes_),
                       log_result(owner, notebook, experiment, features, model, params, cv, notes),
                       save_predictions(owner, name, oof_proba, test_proba, classes, cv), load_predictions(classes)
- src/prediction.py  : make_submission(test, pred_labels, file_name)
- owner 값: J_leader / H_data / A_model / P_light (내 것만 쓴다)

[실험 작성 순서 - 이 형식을 지킨다]
1. pipe = Pipeline([("features", 전처리/피처 변환), ("model", 모델(**PARAMS))])
2. cv = run_cv(pipe, X, y, folds=folds)   ← 점수는 반드시 이걸로 (빠른 확인은 folds=folds[:1], 기록은 5-fold)
3. per_class_f1(y, cv["oof"], le.classes_) 로 약한 클래스 확인
4. log_result(owner=내 owner, ...) 로 기록
5. 앙상블 후보면: 전체 train으로 fit → test_proba = predict_proba(test.drop(columns=["ID"])) → save_predictions(...)

[협업 규칙]
- 내 브랜치에서, 내 폴더의 파일만 만들고 고친다. 다른 사람 폴더와 내가 담당하지 않는 src 파일은 고치지 않는다 (필요하면 나에게 "담당자에게 요청하라"고 말해줘).
- 새 실험은 내 폴더 안에 새 노트북으로 만든다.
- 효과가 검증된 피처만 src/features.py로 옮긴다 (② 담당).
- develop에는 PR로만 합친다. main은 건드리지 않는다.
- csv, 모델 파일(.pkl 등), API 키는 커밋하지 않는다.

[답변 방식]
- 코드에 한국어 주석으로 각 단계를 설명한다.
- 누수 가능성이 조금이라도 있으면 코드를 주기 전에 먼저 경고한다.
- 내가 이해하지 못한 부분은 쉽게 설명한다. 나는 발표와 코드 검증에서 직접 설명해야 한다.
```

---- 여기까지 ----

## PR 올리기 전 셀프 체크
- [ ] `pd.concat([train, test])` 같은 코드가 없나요?
- [ ] `fit`, `fit_transform`이 test나 전체 X에 쓰이지 않나요? (Pipeline 안에서만)
- [ ] 점수를 `run_cv()` 5-fold로 냈고 `log_result()`로 기록했나요?
- [ ] 내 폴더와 내 담당 파일만 바뀌었나요?

애매하면 혼자 판단하지 말고 팀장에게 물어봐 주세요.
