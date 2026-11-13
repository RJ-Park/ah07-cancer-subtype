# 서비스 기획  ·  담당: ① 장성은

> 발표 1번(문제 정의)·7번(서비스 시나리오)·8번(한계와 결론)의 근거 자료이다.
> 범위: 본 모델은 의료진의 추가 검사 및 치료 검토를 **보조하는 도구**이며, 진단을 확정하거나 치료법을 추천하지 않는다.

## 1. 문제 정의

**요약:** 본 프로젝트는 표적치료 목적으로 시행되는 유전자 패널 검사 결과를 재활용하여, 암의 원발 장기 추정에 필요한 단서를 의료진에게 제공하는 것을 목표로 한다.

- **대상 문제**
  - **원발부위 불명암(Cancer of Unknown Primary, CUP)**: 전이 병변은 확인되었으나 원발 장기를 특정하지 못한 암이다. 포괄적 유전체 분석과 PET-CT가 도입된 현재, 신규 암 진단의 1% 미만이 CUP로 분류되며, 1년 생존율은 약 30%이다 [1].
  - 원발 장기에 따라 표준 항암요법과 표적치료제가 달라지므로, 원발 장기 미상은 치료 선택을 제한한다.
- **현행 진단 과정**
  - 영상 검사(CT, PET)와 조직검사 후 면역조직화학 염색(Immunohistochemistry, IHC; 단백질 표지자 염색 검사)으로 원발 장기를 추정하며, 유전자 발현 분석과 차세대 염기서열 분석(Next-Generation Sequencing, NGS)도 원발 부위 추정에 활용될 수 있다 [1].
  - 원발 장기가 특정되지 않으면 경험적 복합 항암요법을 시행한다.
- **현행 과정의 한계**
  - **조직 부족**: 생검 조직이 소량인 경우 추가 검사가 제한된다.
  - **정보 미활용**: NGS 결과는 주로 표적치료제 적용 여부 판단에 사용되며, 원발 장기 추정 정보로는 충분히 활용되지 않는다.
  - **신뢰도 불명확**: AI 예측의 적용 범위와 신뢰도가 제시되지 않으면 임상 적용 시 오판 위험이 있다.
- **치료 근거의 현황**
  - 유전자 발현 분석으로 원발 부위를 예측하여 치료한 무작위 연구에서는 생존 이득이 확인되지 않았다 [4][5].
  - 반면 포괄적 유전체 검사 후 표적 변이에 맞춘 치료는 무진행 생존을 연장하였으며(6.1개월 vs 4.4개월), 저자들은 진단 시 유전체 검사를 권고하였다 [6]. 이는 원발 부위 예측이 아닌 표적 변이 기반 치료라는 점에 유의한다.
  - 따라서 유전체 검사는 CUP 진료에서 점차 시행될 가능성이 크며, 그 결과를 원발 장기 단서로 재활용하는 것은 추가 조직과 비용 없이 가능하다.
- **선행 연구와 차별점**
  - Penson 외는 임상 NGS 패널 데이터로 22개 암 종류를 예측하여 독립 코호트 정확도 74.1%를 보고하였다. 확률 95% 초과 예측(전체의 43.5%)에 한정하면 정확도는 96.6%였다 [2].
  - Jiao 외는 전장 유전체(Whole-Genome Sequencing, WGS)의 패신저 변이 패턴으로 24개 암 종류를 정확도 91%(전이암 83%)로 분류하였으며, 드라이버 변이 정보를 추가하면 정확도가 오히려 낮아짐을 보고하였다 [3]. 이는 정보량이 적은 데이터에서는 성능이 제한될 수 있음을 시사한다.
  - 본 프로젝트는 성능 수치에 그치지 않고, **점 변이(point mutation) 정보만으로 구분 가능한 범위와 불가능한 범위를 데이터로 제시**하며, 예측 신뢰도가 낮은 경우 판단을 보류하는 구조를 제안한다.

## 2. 사용자와 사용 장면

| 사용자 | 사용 시점 | 제공 정보 | 기대 효과 |
|---|---|---|---|
| 종양내과 전문의 | CUP 환자의 NGS 결과 확인 시 | 상위 3개 후보 암 종류와 각 확률 | 추가 검사 및 치료 방향 선정의 근거 |
| 병리과 전문의 | IHC 결과가 결정적이지 않을 때 | 예측 근거 유전자 (예: 대장암 후보의 APC 변이) | IHC 소견과 대조 가능한 보조 정보 |
| 분자종양위원회(Molecular Tumor Board, MTB) | 다학제 치료 방침 결정 시 | 후보 목록, 근거 유전자, 판단 보류 여부 | 근거 기반 논의 자료 |
| 환자 및 보호자 (간접) | 치료 방침 설명 시 | 의료진의 설명 | 치료 선택 근거에 대한 이해 증진 |

## 3. 서비스 흐름

```
① NGS 패널 결과 입력 (기존 검사 활용, 추가 조직·비용 불필요)
      ↓
② 모델 예측: 상위 3개 후보 암 종류 및 확률 산출
      ↓
③ 예측 근거 유전자 변이 제시
      ↓
④ 신뢰도 판정
   ├─ 신뢰도 높음 → 후보 제시
   └─ 신뢰도 낮음 (예: 변이 수가 매우 적은 경우) → 판단 보류 및 추가 검사 권고
      ↓
⑤ 의료진 최종 판단 (모델은 의사결정을 대체하지 않고 보조 정보만 제공함)
```

- **상위 3개 후보 제시 근거**: 기본 모델의 교차검증 결과, 1순위 정답률은 34.2%, 상위 3개 후보 내 정답 포함률은 62.7%였다 [③ 최종 모델 수치로 교체]. 후보 범위를 좁히는 것만으로도 후속 검사 선택에 기여할 수 있다.
- **판단 보류 근거**: 선행 연구에서도 고확신 예측에 한정하면 정확도가 크게 높아졌다 [2]. 확신도 기준은 교차검증으로 정한다 [③].
- **확률 보정(calibration)**: 제시 확률이 실제 정답 빈도와 일치하는지 검증한다. 예를 들어 "60%"로 제시된 예측은 실제로 약 60% 수준의 정답률을 보여야 한다 [③].

## 4. 왜 경량 모델인가

- **운영 환경**: 환자 유전체 정보는 외부 반출이 제한되므로, 병원 내부 서버 또는 일반 PC에서 동작해야 한다.
- **설명 가능성**: 구조가 단순한 모델일수록 예측 근거 제시가 용이하다.
- **채택 기준**: 두 모델의 성능 차이가 0.02 이하인 경우 경량 모델을 서비스 모델로 채택한다.
- **비교 결과**: 최종 평가 후 발표 자료와 README에 기재한다.

## 5. 시장성·확장

- **기존 검사 재활용**: 국내에서는 2017년 3월부터 NGS 패널 검사가 건강보험 선별급여로 시행되고 있으며(고형암 10종 등) [7], 본 서비스는 신규 검사 없이 기존 결과의 활용도를 높이는 방식이다.
- **유전자 패널 최적화**: 분류 기여도가 높은 유전자를 선별하면 소규모 패널로도 유사한 성능을 낼 가능성이 있다 [② 축소 유전자 결과].
- **다중 정보 결합**: 유전자 발현 [1][4], 패신저 변이 패턴 [3], 복제수 변이(copy number alteration), 메틸화(methylation), 병리 영상 등을 결합하면 성능 향상이 기대되며, 본 분석 결과는 추가 정보 선택의 근거로 활용할 수 있다.
- **연구 기여**: 점 변이만으로 구분되지 않는 암 종류와 그 원인을 정리한 결과는 독립적인 연구 가치를 가진다.

## 6. 한계

**데이터 한계 (train 데이터 분석 결과)**

| 항목 | 수치 | 해석 |
|---|---|---|
| 변이가 없는 환자 | 94명 | 모델이 활용할 정보가 없음 |
| 변이 5개 이하 환자 | 약 20% | 정보량이 매우 적음 |
| 다중 암 공통 변이 | BRAF V600E 321명: 갑상선암 184, 흑색종 106, 대장암 20 | 단일 변이로 암 종류를 확정할 수 없음 |
| 1회만 출현한 변이 | 서로 다른 변이 115,200개 중 65,531개 | 대부분 우연히 발생한 변이로 학습에 기여하기 어려움 |
| 저변이 암의 오분류 | 흉선암, 갈색세포종, 전립선암, 갑상선암이 유방암으로 편향 | 점 변이만으로 구분이 어려운 암 그룹임 |
| 대표 유전자 변이 부재 | 투명세포 신장암(KIRC) 중 VHL 변이 보유 약 45% | 결실·메틸화에 의한 불활성화는 데이터에 반영되지 않음 |
| 주요 유전자 부재 | KRAS, PBRM1, SETD2 등 | 실제 임상 패널 대비 정보량이 적음 |
| 동일 변이·상이 라벨 쌍 | KIPAN–KIRC 270쌍, GBMLGG–LGG 173쌍 | 통합 코호트 코드와 개별 코드의 중복으로 추정되며, 운영진 문의 예정 |

**방법론적 한계**
- 임상 검증을 수행하지 않았다.
- 학습 데이터(The Cancer Genome Atlas, TCGA)는 원발 암과 정상 조직 시료로 구성되나 [8], 실제 CUP는 전이 병변이므로 분포 차이가 존재할 수 있다.
- 원발 부위 예측에 기반한 치료의 생존 이득은 무작위 연구에서 확인되지 않았다 [4][5].

**연구 윤리 및 접근 원칙**
- 데이터 오류를 성능 향상에 이용하지 않았으며, 해당 오류는 데이터 품질 문제로 보고하였다.
- 예측 신뢰도가 낮은 경우 판단을 보류하는 구조를 채택하였다.
- 구분이 불가능한 영역은 근거와 함께 한계로 제시하였다.

## 참고문헌

1. National Cancer Institute. Cancer of Unknown Primary (CUP) Treatment (PDQ®)–Health Professional Version. Updated 2025-05-07. https://www.cancer.gov/types/unknown-primary/hp/unknown-primary-treatment-pdq
2. Penson A, Camacho N, Zheng Y, et al. Development of genome-derived tumor type prediction to inform clinical cancer care. *JAMA Oncol*. 2020;6(1):84-91. doi:10.1001/jamaoncol.2019.3985
3. Jiao W, Atwal G, Polak P, et al. A deep learning system accurately classifies primary and metastatic cancers using passenger mutation patterns. *Nat Commun*. 2020;11:728. doi:10.1038/s41467-019-13825-8
4. Hayashi H, Kurata T, Takiguchi Y, et al. Randomized phase II trial comparing site-specific treatment based on gene expression profiling with carboplatin and paclitaxel for patients with cancer of unknown primary site. *J Clin Oncol*. 2019;37(7):570-579. doi:10.1200/JCO.18.00771
5. Fizazi K, et al. GEFCAPI 04: a phase III trial of empiric chemotherapy versus systemic treatment tailored by molecular gene expression analysis in patients with carcinoma of unknown primary site. ESMO Congress 2019 (학회 발표, 원문 확인 필요).
6. Krämer A, Bochtler T, Pauli C, et al. Molecularly guided therapy versus chemotherapy after disease control in unfavourable cancer of unknown primary (CUPISCO): an open-label, randomised, phase 2 study. *Lancet*. 2024;404(10452):527-539. doi:10.1016/S0140-6736(24)00814-6
7. 데일리팜. [기자의 눈] NGS 패널검사, 유전자 구성 확대 필요. 2020-10-12. https://www.dailypharm.com/user/news/58398
8. National Cancer Institute. The Cancer Genome Atlas Program (TCGA). https://www.cancer.gov/ccg/research/genome-sequencing/tcga