# NGS·유전체 조사 정리  ·  담당: ② 홍시윤

> 발표 2번 파트("데이터와 NGS 이해")의 근거 자료예요. 인용하는 논문은 **링크를 직접 열어 확인한 것만** 적어요.

## 1. NGS에서 변이 테이블까지
<!-- NGS → 변이 검출(variant calling) → 유전자별 변이 표기 → 이 대회 데이터. 3~5줄 -->

## 2. 주요 유전체 변이 유형
| 변이 유형 | 표기 예시 | 의미 |
| :--- | :--- | :--- |
| 미스센스 (Missense) | `R132H`, `V600E` | 아미노산이 다른 아미노산으로 바뀜 |
| 동의 변이 (Synonymous) | `D623D`, `L42L` | DNA가 변했지만 아미노산은 동일 |
| 넌센스 (Nonsense) | `R213*`, `E237*` | 종결 코돈이 생겨 단백질 합성이 조기에 종료될 수 있음 |
| 프레임시프트 (Frameshift) | `K16fs`, `L1854fs` | 삽입·결실로 단백질 번역의 읽기 틀이 바뀜 |
| 인프레임 결실 (In-frame deletion) | `E746_A750del` | 읽기 틀을 유지하면서 아미노산이 삭제됨 |
| 인프레임 삽입 (In-frame insertion) | `A767_V769dup` | 읽기 틀을 유지하면서 아미노산이 추가됨 |
| 중복 (Duplication) | `A767_V769dup` | 특정 서열이 반복됨 |
| 스플라이스 변이 (Splice-site) | `c.1903+1G>A` | RNA 스플라이싱에 영향을 줄 수 있음 |
| 시작 코돈 변이 (Start-loss) | `M1?` | 단백질 번역 시작에 영향을 줄 수 있음 |
| 종결 코돈 소실 (Stop-loss) | `*110Qext*17` | 기존 종결 코돈이 사라져 단백질이 연장될 수 있음 |
| 유전자 융합 (Gene fusion) | `BCR::ABL1` | 서로 다른 유전자가 연결됨 |
| 복제수 변이 (CNV) | `ERBB2 amplification` | 유전자 복제수가 증가하거나 감소함 |
| 기타/미분류 | 위 규칙에 해당하지 않는 경우 | 별도 확인 필요 |


- 변이 하지 않은 경우 WT(Wild Type)로 표기함.
- 한 유전자에 여러 변이가 기록된 경우 공백으로 구분함.  ex) `R273C R248Q`

## 3. TCGA 33개 암종별 주요 관련 유전자 및 유전체 특징
<!-- 예) GBMLGG·LGG ↔ IDH1 R132H, SKCM·THCA ↔ BRAF V600E … train에서 확인한 것 + 근거 -->
> **출처:** 미국 국립암연구소(NCI), [TCGA Cancers Selected for Study](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/studied-cancers). 이 목록은 NCI 페이지의 연구 결과를 암종별로 간추린 **자료조사 요약**이며, 암종마다 반드시 나타나는 유전자나 암종 특이적 진단 마커 목록이 아니다.
>
> **주의:** `변이`, `발현`, `증폭/복제수`, `융합`, `경로`는 서로 다른 정보다. 해커톤 데이터가 단백질 변이 표기(`R895R` 등)만 포함한다면 발현·융합·복제수 변화는 직접 관측할 수 없다. NCI 페이지에 특정 유전자가 명시되지 않은 암종은 임의로 추가하지 않았다.

### 3-1. 암종별 요약

| 코드 | 암종 (한글명) | NCI 페이지에서 언급한 주요 유전자/표지 | 주요 유전체 특징 및 해석 |
|---|---|---|---|
| ACC | 부신피질암 | **IGF2, TP53, PRKAR1A** | IGF2 과발현, TP53·PRKAR1A 변이, 염색체 복제수 변화 |
| BLCA | 방광 요로상피암 | **ERCC2** | 흡연과 ERCC2 변이/변이 시그니처 연관; p53·세포주기, DNA 복구, PI3K/AKT 경로 이상 |
| BRCA | 침윤성 유방암 | **ERBB2 (HER2), CDH1 (E-cadherin)** | HER2-enriched 등 분자 아형; 소엽암에서 E-cadherin 소실. ERBB2는 HER2 아형 표지이며 이 페이지의 해당 항목이 단순한 ERBB2 점돌연변이 빈도를 제시하는 것은 아님 |
| CESC | 자궁경부 편평세포암 및 선암 | **MED1, ERBB3, CASP8, HLA-A, TGFBR2, BCAR4** | 새로운 변이 유전자와 BCAR4 융합; HPV 및 PI3K/MAPK·TGF-β 경로 관련 |
| CHOL | 담관암 | **CDKN2 계열, BAP1, ARID1 계열, FGFR2, IDH1, IDH2** | 종양억제유전자 기능 저하, FGFR2 활성화/재배열, IDH 변이 관련 아형. NCI 페이지의 일부 유전자명은 계열 수준으로 표기됨 |
| COAD | 결장선암 | **ARID1A, SOX9, AMER1 (FAM123B/WTX), ERBB2, IGF2** | 변이 및 WNT 경로 이상; ERBB2·IGF2 과발현도 보고. NCI는 COAD와 READ를 통합해 설명 |
| DLBC | 미만성 거대 B세포 림프종 | **페이지에 구체적 유전자 명시 없음** | ⭐️(수정-)이 NCI 요약 페이지에 별도 DLBC 항목이 없어 추가 논문 검토 필요 |
| ESCA | 식도암 | **ERBB2 (HER2)** | 일부 식도선암에서 ERBB2 변화; 선암과 편평세포암의 분자적 차이가 큼 |
| GBM | 교모세포종 | **EGFR, MDM2, CDK4, NF1, ERBB2, TP53, PIK3R1, TERT** | EGFR 및 MDM2/CDK4 영역 변화, 여러 변이 유전자와 분자 아형 |
| HNSC | 두경부 편평세포암 | **TRAF3, E2F1, PIK3CA, BIRC2, FADD, TP53, CDKN2A** | HPV 양성/음성에 따라 분자 특징이 다름; 증폭, 불활성화, 변이가 혼재 |
| KICH | 신장 혐색소성 암 | **TP53, PTEN, TERT** | 상대적으로 낮은 체세포 변이 부담; TERT 프로모터 구조 변화 |
| KIRC | 신장 투명세포암 | **VHL, SETD2** | 산소 감지 및 PI3K/AKT/mTOR 경로 이상, SETD2 변이 |
| KIRP | 신장 유두상 세포암 | **MET, CDKN2A** | 제1형에서 MET 변화, 제2형 일부에서 CDKN2A 발현 소실 및 메틸화 아형 |
| LAML | 급성 골수성 백혈병 | **NPM1** | NPM1 변이와 전사인자·코헤신·신호전달 관련 유전자군의 반복 변이 |
| LGG | 저등급 신경교종 | **IDH1, IDH2** | IDH 변이 및 1p/19q 공동결실이 중요한 분류 기준 |
| LIHC | 간세포암 | **TERT, TP53, CTNNB1, MDM4** | TERT 프로모터·TP53·CTNNB1 변이; MDM4 발현에 의한 TP53 억제 가능성 |
| LUAD | 폐선암 | **KRAS, EGFR, BRAF, NF1** | 수용체 티로신 키나아제 관련 신호 경로 활성화 및 드라이버 변이 |
| LUSC | 폐편평세포암 | **TP53, CDKN2A, HLA-A** | TP53 변화 및 CDKN2A 불활성화; ERBB/FGFR/JAK 유전자군도 경로 수준에서 언급 |
| MESO | 중피종 | **BAP1, TP53, SETDB1, VSIR (VISTA)** | BAP1 변화, 일부 TP53/SETDB1 변이; VISTA 높은 발현은 단백질/면역 관련 특징 |
| OV | 난소 장액성 암 | **TP53, BRCA1, BRCA2** | TP53 변이가 매우 빈번하며 BRCA1/2 변이도 일부에서 관찰 |
| PAAD | 췌장선암 | **KRAS, RREB1** | KRAS 및 RAS–MAPK 경로의 중요성; RREB1 관련 가능성 |
| PCPG | 갈색세포종 및 부신경절종 | **CSDE1, MAML3** | CSDE1 변이 및 MAML3 융합; WNT 관련 아형 |
| PRAD | 전립선선암 | **SPOP, FOXA1** | 변이 기반 아형과 유전자 융합 기반 아형이 공존 |
| READ | 직장선암 | **ARID1A, SOX9, AMER1 (FAM123B/WTX), ERBB2, IGF2** | NCI 페이지에서 COAD와 함께 대장·직장암으로 통합 분석 |
| SARC | 육종 | **TP53, ATRX, RB1, SSX1, SSX2, TERT, JUN** | 변이·유전자 융합·증폭이 육종 세부 유형별로 다름 |
| SKCM | 피부 흑색종 | **BRAF, RAS 계열, NF1, AKT3** | BRAF/RAS/NF1 변이 및 triple-WT 아형; AKT3는 발현 변화로 언급 |
| STAD | 위선암 | **PIK3CA** | EBV 양성 아형에서 PIK3CA 변화; MSI, GS, CIN 등 분자 아형 |
| TGCT | 고환 생식세포종양 | **KIT, KRAS** | 일부 정상피종에서 KIT 변이, KRAS 복제수 변화; 전반적으로 낮은 변이 빈도 |
| THCA | 갑상선암 | **BRAF, RAS 계열, EIF1AX** | BRAF V600E 또는 RAS 관련 아형; EIF1AX도 드라이버로 언급 |
| THYM | 흉선종 | **GTF2I, HRAS, NRAS, TP53** | 전반적으로 낮은 변이 부담, GTF2I 반복 변이 |
| UCEC | 자궁내막암 | **POLE, TP53, PTEN, KRAS** | POLE 초고변이, MSI, 복제수 고/저 아형; 아형별 변이 양상 차이 |
| UCS | 자궁암육종 | **TP53** | TP53 변이가 빈번하고 PI3K 경로 이상도 관찰 |
| UVM | 포도막 흑색종 | **BAP1** | BAP1 변화와 3번 염색체 단일염색체성(M3) 및 전이 위험 관련 |

### 3-2. 주의할 점
1. **유전자 이름과 실제 변이 유형 구분:** `TP53` 컬럼에 `R175H`가 있으면 단백질 수준 변이로 해석할 수 있지만, `TP53`의 발현 증가나 유전자 결실 여부를 알 수 있는 것은 아니다.
2. **암종별 유전자 목록을 정답 규칙으로 사용하지 않기:** `TP53`처럼 여러 암종에 공통으로 나타나는 유전자가 많다. 대표 유전자에 변이가 있다고 해당 암종이라고 단정할 수 없다.
3. **표본에서 학습한 암종별 변이 빈도는 교차검증 폴드 안에서 계산:** 전체 학습 데이터의 `SUBCLASS`를 이용해 유전자별 암종 특이성을 산출한 뒤 검증 폴드에 그대로 적용하면 데이터 누수가 발생할 수 있다.
4. **외부 문헌 기반 후보 유전자 집합은 사전 정의 가능:** 단, 외부 연구와 해커톤 데이터의 환자·검체 중복 여부, 데이터 출처, 유전자 측정 범위가 다를 수 있다는 점을 확인한다.
5. **동의 변이와 기능 변화 변이를 구분해 실험:** `R895R`처럼 아미노산이 바뀌지 않는 변이를 단순 변이 존재와 구분한 파생변수는 실험해 볼 수 있다. 단백질 표기만으로 실제 기능적 영향이 확정되는 것은 아니다.
6. **원본 데이터에 없는 변이 종류는 만들지 않기:** 복제수 변화(CNV), 발현량, 유전자 융합, 프로모터 변이는 해당 측정값이 없으면 직접적인 피처로 사용할 수 없다.
7. 위 표는 NCI 요약에 언급된 유전자 중심의 선별된 예시이며 각 암종의 전체 드라이버 유전자 목록이나 임상 진단 기준이 아니다. 일부 유전자명은 현행 기호로 보완 표기했다(AMER1/WTX, VSIR/VISTA).

### 3-3. 출처
- **1차 출처:** [NCI — TCGA Cancers Selected for Study](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/studied-cancers)
- **암종 약어:** [GDC — TCGA Study Abbreviations](https://gdc.cancer.gov/resources-tcga-users/tcga-code-tables/tcga-study-abbreviations)

## 4. 관련 논문 (확인한 것만)
| 논문 | 링크 | 데이터·방법 | 우리 작업과의 연결 |
|---|---|---|---|
|  |  |  |  |

## 5. 모델 담당에게 넘긴 관찰
1.
2.
3.


@@@ 빈 칸은 차차 해갈게요 @@@