# AI 작업 규칙 (AI에게 먼저 붙여넣기)

> 바이브코딩으로 작업할 때, AI(Claude, ChatGPT, Gemini, Copilot 등)에게 **작업을 시키기 전에 아래 박스 내용을 통째로 붙여넣어 주세요.**
> AI는 대회 규정을 몰라서, 그냥 "점수 올려줘"라고 하면 실격 사유가 되는 코드를 주는 경우가 많아요.

---

```text
지금부터 데이콘 해커톤 코드를 같이 작성할 거야. 아래 규칙을 반드시 지켜. 규칙을 어기면 실격이야.

[과제]
- 환자별 유전자 변이 정보(유전자 컬럼 4,384개, 값은 "WT" 또는 변이 표기)로 암 아형 SUBCLASS(26개 클래스)를 예측하는 다중 분류.
- 평가 지표는 Macro F1.

[데이터 누수 금지 - 가장 중요]
- 인코더, 스케일러, 결측치 대체, 피처 선택, 차원 축소 등 데이터로 학습하는 모든 변환은 train(교차검증에서는 각 fold의 학습 부분)에만 fit 하고, 검증/test에는 transform만 해.
- train과 test를 합쳐서(concat) 전처리하지 마.
- test에 pd.get_dummies()를 따로 쓰지 마.
- test의 통계(평균, 최빈값, 분포, 결측 개수), index, 행 개수를 어디에도 쓰지 마.
- test를 탐색(EDA)해서 얻은 정보를 전처리나 학습에 반영하지 마. test는 컬럼 형식 확인과 최종 추론에만 써.
- test에 가짜 라벨을 붙여 다시 학습하는 pseudo-labeling 금지.
- 한 행 안에서만 하는 계산(예: WT를 0, 변이를 1로 바꾸기, 환자별 변이 개수)은 허용.
- 전처리와 모델은 sklearn Pipeline으로 묶어서 fold 안에서만 fit 되게 해.

[검증과 재현]
- 레포 구조: src/config.py(SEED, DATA_DIR), src/data_loader.py(load_data, split_xy, encode_target), src/preprocessing.py(basic_transformer, binarize_mutations), src/features.py(mutation_count 등 검증된 피처), src/validation.py(get_folds, run_cv, balanced_weights), src/evaluation.py(macro_f1, per_class_f1, log_result), src/prediction.py(make_submission). 이 함수들을 그대로 써.
- 점수는 반드시 get_folds(), run_cv()로 계산해 (5-fold Stratified K-Fold, SEED=42, Macro F1). 결과는 log_result()로 기록해.
- 모든 난수에 seed를 고정해 (set_seed(SEED), 모델 random_state=SEED).
- 하이퍼파라미터는 코드에 숫자로 직접 적어.
- 데이터 경로는 src/config.py 의 DATA_DIR 하나로만 다뤄 (최종 제출 코드에서는 "/data").
- 내 폴더(notebooks/이니셜_역할/)의 노트북만 수정하고, src/ 파일은 수정하지 마 (수정이 필요하면 나에게 먼저 말해).

[코드 출처]
- 외부 데이터 사용 금지.
- 이전 데이콘 대회(특히 2024년 같은 주제 대회)나 다른 대회의 공개 코드, 수상 코드를 가져오거나 비슷하게 따라 하지 마. 이 대회를 위해 새로 작성해.
- 사전학습 모델을 쓰려면 논문으로 공개된 것만 쓰고, 논문 링크를 주석으로 남겨.

[작성 방식]
- 코드에 한국어 주석으로 각 단계가 무엇을 하는지 설명해.
- 내가 이해하지 못한 부분은 설명해 줘. 나중에 발표와 재현 검증에서 직접 설명해야 해.
```

---

## 팀원 체크 (AI 코드를 쓰기 전에)

- [ ] `pd.concat([train, test])` 같은 코드가 없나요?
- [ ] `fit`, `fit_transform`이 test에 쓰이지 않나요?
- [ ] 점수를 `run_cv()`로 냈나요?
- [ ] 실험 기록표에 점수를 남겼나요?

애매하면 혼자 판단하지 말고 팀장에게 물어봐 주세요.
