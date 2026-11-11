
# 유전체 기초 및 암종 분류 개념 정리

> **문서 목적**
>
> 유전체 변이 기반 암종 분류 프로젝트를 이해하기 위한 기초 생물학 개념과 TCGA 암종 분류 체계를 정리한다.
>
> 생물학 비전공자를 대상으로 하며, 과학적 사실과 프로젝트에서 사용하는 데이터 표현을 구분한다.

## 목차

1. DNA부터 단백질까지
2. 유전체 변이와 암의 관계
3. 암종과 분자적 특성
4. TCGA 암종 코드
5. 프로젝트 데이터와의 연결
6. 참고 자료 및 출처

---

## 1. DNA부터 단백질까지

### 1-1. 핵심 용어

| 용어 | 쉬운 설명 |
|---|---|
| DNA | 생명체의 유전정보를 저장하는 분자 |
| 염기(Base) | DNA나 RNA의 유전정보를 구성하는 기본 문자 |
| 염기서열(Sequence) | 염기들이 나열된 순서 |
| 유전자(Gene) | 특정 기능을 수행하는 RNA나 단백질 생성에 필요한 정보를 담은 DNA 구간 |
| 유전체(Genome) | 생명체가 가진 전체 유전정보 |
| RNA | 유전정보 전달과 단백질 합성 등 다양한 역할을 하는 분자 |
| mRNA | DNA의 유전정보를 리보솜에 전달하는 전령 RNA |
| 코돈(Codon) | 아미노산 또는 번역 종료 신호를 지정하는 3개 염기 조합 |
| 아미노산(Amino acid) | 단백질을 구성하는 기본 단위 |
| 단백질(Protein) | 아미노산 사슬이 접혀 만들어지며 세포의 구조와 기능에 관여하는 분자 |

### 1-2. DNA와 염기서열

DNA(Deoxyribonucleic Acid)는 유전정보를 저장하는 분자다.

DNA에는 네 가지 염기가 존재한다.

| 기호 | 이름 |
|---|---|
| A | Adenine, 아데닌 |
| T | Thymine, 티민 |
| G | Guanine, 구아닌 |
| C | Cytosine, 시토신 |

예를 들어 다음은 DNA 염기서열이다.

```text
ATG GAA TTT
```

염기의 종류뿐 아니라 **어떤 순서로 배열되는지**가 중요하다.

단백질을 암호화하는 DNA 구간에서는 염기서열의 변화가 단백질의 아미노산 서열에 영향을 줄 수 있다.

### 1-3. mRNA와 단백질 합성

mRNA(Messenger RNA)는 DNA에 저장된 유전정보를 리보솜에 전달하는 역할을 한다.

단백질 합성은 크게 두 과정으로 구분된다.

| 과정 | 의미 |
|---|---|
| 전사(Transcription) | DNA의 정보를 이용해 RNA를 생성하는 과정 |
| 번역(Translation) | 리보솜이 mRNA의 코돈을 읽고 아미노산을 연결하는 과정 |

**전체 흐름**

```text
DNA (유전정보 저장)
  │
  │ 전사 (Transcription)
  ▼
mRNA (유전정보 전달)
  │
  │ 번역 (Translation)
  ▼
아미노산 사슬
  │
  │ 접힘 및 가공
  ▼
단백질
```

DNA와 RNA는 사용하는 염기에 차이가 있다.

| DNA | RNA |
|---|---|
| A | A |
| T (Thymine) | U (Uracil) |
| G | G |
| C | C |

RNA에서는 DNA의 T 대신 U를 사용한다.

**주의:** 위 과정은 단백질을 암호화하는 유전자를 기준으로 단순화한 것이다. 모든 RNA가 단백질로 번역되는 것은 아니다.

### 1-4. 코돈과 아미노산

코돈(Codon)은 mRNA의 연속된 3개 염기로 이루어진 정보 단위다.

예를 들어 DNA의 단백질 암호화 가닥을 기준으로 다음과 같이 대응한다.

| DNA 코돈 | mRNA 코돈 | 아미노산 |
|---|---|---|
| ATG | AUG | Methionine (M) |
| GAA | GAA | Glutamate (E) |
| TTT | UUU | Phenylalanine (F) |

```text
DNA:       ATG | GAA | TTT
mRNA:      AUG | GAA | UUU
아미노산:    M  |  E  |  F
```

표준 유전암호에는 총 64개의 코돈이 있다.

- 61개: 아미노산 지정
- 3개: 번역 종료 신호

여러 코돈이 동일한 아미노산을 지정할 수 있다.

따라서 DNA 염기가 변하더라도 아미노산이 바뀌지 않을 수 있다.

---

## 2. 유전체 변이와 암의 관계

### 2-1. 유전체 변이(Genomic Variant)

유전체 변이는 기준 서열과 비교했을 때 DNA 서열에 차이가 있는 것을 의미한다.

예시:

```text
기준 DNA: ATG GAA TTT
변이 DNA: ATG GAC TTT
                 ^
```

위 예시는 DNA 코돈 `GAA`가 `GAC`로 바뀐 경우다.

- GAA → Glutamate (E)
- GAC → Aspartate (D)

따라서 단백질 수준에서는 E가 D로 바뀔 수 있다.

다만 모든 DNA 변이가 단백질 기능을 변화시키는 것은 아니며, 모든 변이가 질병을 유발하는 것도 아니다.

### 2-2. 암과 유전자 변이

암은 세포의 성장과 분열을 조절하는 체계에 이상이 축적되면서 발생할 수 있다.

암 발생에 관여하는 유전자는 다음과 같이 구분할 수 있다.

| 구분 | 역할 | 쉬운 비유 |
|---|---|---|
| Proto-oncogene | 정상적인 세포 성장·분열 조절 | 자동차 가속페달 |
| Oncogene | 비정상적으로 활성화되면 세포 증식을 촉진 | 가속페달이 계속 눌린 상태 |
| Tumor suppressor gene | 세포 증식 억제 및 손상 대응 등에 관여 | 자동차 브레이크 |
| DNA repair gene | 손상된 DNA를 복구하는 데 관여 | 고장 수리 장치 |

**대표 유전자 예시**

- `KRAS`: 세포 성장 신호 전달에 관여
- `TP53`: 세포주기 조절과 DNA 손상 대응에 관여
- `BRCA1`, `BRCA2`: DNA 손상 복구에 관여

유전자 이름만으로 특정 변이가 암을 유발했다고 판단할 수는 없다.

변이의 위치, 유형, 기능적 영향과 생물학적 맥락을 함께 고려해야 한다.

### 2-3. Driver와 Passenger 변이

암세포에서 발견되는 모든 변이가 암 발생에 직접 기여하는 것은 아니다.

| 구분 | 의미 |
|---|---|
| Driver mutation | 암세포의 성장이나 생존에 선택적 이점을 제공하는 변이 |
| Passenger mutation | 암 발생 과정에서 함께 축적되었지만 직접적인 선택적 이점을 제공하지 않는 변이 |

특정 암종에서 반복적으로 발견되는 변이는 중요한 연구 대상이 될 수 있다.

그러나 **자주 나타난다는 사실만으로 Driver 변이라고 확정할 수는 없다.**

---

## 3. 암종과 분자적 특성

### 3-1. 암종(Cancer Type)이란?

암종은 암이 발생한 조직, 세포의 특성, 조직학적 형태 등을 기준으로 구분하는 분류 단위다.

예를 들어 폐암도 다음과 같이 나뉜다.

- LUAD: 폐선암
- LUSC: 폐편평세포암

두 암종은 모두 폐에서 발생하지만 조직학적 특성과 분자적 특징이 다르다.

따라서 암이 발생한 장기만으로 암종을 완전히 구분할 수는 없다.

### 3-2. 암종마다 변이 패턴이 다른 이유

암종마다 다음과 같은 차이가 존재할 수 있다.

1. 암이 발생한 조직 및 세포의 특성
2. 암 발생에 관여하는 유전자와 신호전달 경로
3. 환경적 노출 및 돌연변이 유발 과정
4. 암세포가 성장하면서 축적한 유전체 변화

이 때문에 암종별로 특정 유전자나 변이 패턴의 출현 빈도가 달라질 수 있다.

하지만 하나의 변이가 여러 암종에서 발견될 수도 있으므로 특정 변이 하나만으로 암종을 확정하는 것은 부적절하다.

### 3-3. 관련 연구

**Hoadley et al. (2018)**

*Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer*

- 학술지: Cell
- DOI: https://doi.org/10.1016/j.cell.2018.03.022

TCGA의 약 10,000개 종양, 33개 암종을 대상으로 다양한 분자 데이터를 통합 분석한 연구다.

연구에서는 암종의 분자적 분류에 암이 유래한 조직과 세포의 특성이 중요한 역할을 한다는 점을 보여준다.

**프로젝트와의 연결**

유전체 변이 패턴을 활용해 암종을 구분하려는 접근의 생물학적 배경을 이해하는 데 도움이 된다.

단, 해당 연구는 DNA 변이뿐 아니라 유전자 발현, DNA 메틸화 등 다양한 데이터를 통합했다.

따라서 해당 연구 결과가 우리 프로젝트의 단백질 변이 데이터만으로 동일한 분류 성능을 달성할 수 있다는 의미는 아니다.

---

## 4. TCGA 암종 코드

### 4-1. TCGA란?

TCGA(The Cancer Genome Atlas)는 암의 분자적 특성을 체계적으로 분석하기 위해 수행된 대규모 암 유전체 연구 프로젝트다.

TCGA는 33개 암종에 걸쳐 대규모 종양 및 정상 조직 검체의 분자 데이터를 분석했다.

암종을 구분할 때 `BRCA`, `LUAD`, `SKCM`과 같은 약어를 사용한다.

### 4-2. TCGA 암종 코드

기존 문서의 암종 목록과 순서를 유지했다.

`GBMLGG`와 `KIPAN`은 여러 암종을 묶어 나타내는 상위 그룹으로, 구성 암종을 들여쓰기로 표시했다.

| 코드 | 영문명 | 한글명 |
|---|---|---|
| ACC | Adrenocortical carcinoma | 부신피질암 |
| BLCA | Bladder Urothelial Carcinoma | 방광 요로상피암 |
| BRCA | Breast invasive carcinoma | 침윤성 유방암 |
| CESC | Cervical squamous cell carcinoma and endocervical adenocarcinoma | 자궁경부 편평세포암 및 선암 |
| CHOL | Cholangiocarcinoma | 담관암 |
| COAD | Colon adenocarcinoma | 결장선암 |
| DLBC | Diffuse Large B-cell Lymphoma | 미만성 거대 B세포 림프종 |
| ESCA | Esophageal carcinoma | 식도암 |
| **GBMLGG** | **GBM + LGG** | **신경교종 통합 그룹** |
| ↳ GBM | Glioblastoma multiforme | 교모세포종 |
| ↳ LGG | Brain Lower Grade Glioma | 저등급 신경교종 |
| HNSC | Head and Neck squamous cell carcinoma | 두경부 편평세포암 |
| **KIPAN** | **Pan-kidney cohort** | **신장암 통합 그룹** |
| ↳ KICH | Kidney Chromophobe | 신장 혐색소성 암 |
| ↳ KIRC | Kidney renal clear cell carcinoma | 신장 투명세포암 |
| ↳ KIRP | Kidney renal papillary cell carcinoma | 신장 유두상 세포암 |
| LAML | Acute Myeloid Leukemia | 급성 골수성 백혈병 |
| LIHC | Liver hepatocellular carcinoma | 간세포암 |
| LUAD | Lung adenocarcinoma | 폐선암 |
| LUSC | Lung squamous cell carcinoma | 폐편평세포암 |
| MESO | Mesothelioma | 중피종 |
| OV | Ovarian serous cystadenocarcinoma | 난소 장액성 암 |
| PAAD | Pancreatic adenocarcinoma | 췌장선암 |
| PCPG | Pheochromocytoma and Paraganglioma | 갈색세포종 및 부신경절종 |
| PRAD | Prostate adenocarcinoma | 전립선선암 |
| READ | Rectum adenocarcinoma | 직장선암 |
| SARC | Sarcoma | 육종 |
| SKCM | Skin Cutaneous Melanoma | 피부 흑색종 |
| STAD | Stomach adenocarcinoma | 위선암 |
| TGCT | Testicular Germ Cell Tumors | 고환 생식세포종양 |
| THCA | Thyroid carcinoma | 갑상선암 |
| THYM | Thymoma | 흉선종 |
| UCEC | Uterine Corpus Endometrial Carcinoma | 자궁내막암 |
| UCS | Uterine Carcinosarcoma | 자궁암육종 |
| UVM | Uveal Melanoma | 포도막 흑색종 |

> **참고:** GBMLGG와 KIPAN은 각각 하위 암종을 묶은 분석 그룹이다. TCGA의 33개 개별 암종을 셀 때는 별도로 추가하지 않는다.

### 4-3. 기타 TCGA 코드 (표준 33개 암종 제외)

| 코드 | 영문명 | 의미 |
|---|---|---|
| CNTL | Controls | 대조군 |
| FPPP | FFPE Pilot Phase II | 포르말린 고정 파라핀 포매(FFPE) 검체 관련 파일럿 연구 |
| LCML | Chronic Myelogenous Leukemia | 만성 골수성 백혈병 |
| MISC | Miscellaneous | 기타 항목 |

---

## 5. 프로젝트 데이터와의 연결

### 5-1. 프로젝트 개요

본 프로젝트는 유전체 변이 정보를 이용하여 암종을 분류하는 것을 목표로 한다.

기존 EDA 기록 기준 데이터 구성은 다음과 같다.

| 항목 | 내용 |
|---|---|
| Train 데이터 | 6,201개 샘플 |
| 유전자 관련 컬럼 | 4,384개 |
| 분류 대상 | 26개 SUBCLASS |
| 입력 정보 | 유전자별 변이 표기 |
| 예측 대상 | 암종 클래스(SUBCLASS) |

※ 위 수치는 프로젝트의 기존 분석 기록에 따른 것이며, 외부 논문의 수치가 아니다.

### 5-2. 원본 데이터 표현

유전자별 데이터는 다음과 같은 형태로 기록될 수 있다.

| 유전자 | 예시 값 | 의미 |
|---|---|---|
| BRAF | `V600E` | 단백질 600번 위치의 V가 E로 치환 |
| IDH1 | `R132H` | 단백질 132번 위치의 R이 H로 치환 |
| TP53 | `R175H` | 단백질 175번 위치의 R이 H로 치환 |
| KRAS | `WT` | 데이터에서 기준형으로 표기 |
| 기타 | 결측치 | 해당 값이 기록되지 않음 |

위 표는 데이터 형식을 설명하기 위한 예시이며, 실제 특정 환자의 기록을 의미하지 않는다.

특히 다음 두 가지를 구분해야 한다.

- `WT`: 데이터에서 기준형으로 표시된 값
- 결측치: 값이 제공되지 않았거나 기록되지 않은 상태

결측치를 무조건 WT로 해석해서는 안 된다.

또한 단백질 변이 표기만으로 DNA의 정확한 염기 치환을 확정할 수는 없다.

변이 유형과 표기법은 [ngs_research.md](./ngs_research.md)에서 자세히 다룬다.

### 5-3. 암종 분류에서 중요한 점

1. 하나의 유전자 변이가 여러 암종에서 발견될 수 있다.
2. 같은 암종이라도 환자별 변이 패턴이 다를 수 있다.
3. 유전자 변이가 존재한다는 사실만으로 암종을 확정할 수 없다.
4. 데이터에 기록되지 않은 유전자 발현량, 복제수 변화, 유전자 융합 등을 관측한 것으로 해석해서는 안 된다.
5. TCGA의 33개 암종과 프로젝트의 26개 SUBCLASS가 동일한 분류 체계라고 가정해서는 안 된다.

### 5-4. 관련 프로젝트 노트북

- [01_eda.ipynb](../notebooks/H_data/01_eda.ipynb)
  - 유전자별 데이터 구조 및 변이 표기 확인
- [02_features.ipynb](../notebooks/H_data/02_features.ipynb)
  - 변이 정보를 활용한 피처 생성

---

## 6. 참고 자료 및 출처

### 6-1. 공식 기관 자료

| 번호 | 출처 | 참고한 부분 | 문서 내 활용 위치 |
|---|---|---|---|
| [1] | [NHGRI — Talking Glossary of Genetic Terms](https://www.genome.gov/genetics-glossary) | DNA, Gene, Genome, RNA, Protein의 정의 | 1-1, 1-2 |
| [2] | [NHGRI — Messenger RNA](https://www.genome.gov/genetics-glossary/Messenger-RNA) | mRNA의 역할과 유전정보 전달 | 1-1, 1-3 |
| [3] | [NHGRI — Transcription](https://www.genome.gov/genetics-glossary/Transcription) | DNA에서 RNA가 생성되는 과정 | 1-3 |
| [4] | [NHGRI — Translation](https://www.genome.gov/genetics-glossary/Translation) | mRNA를 이용한 단백질 합성 | 1-3 |
| [5] | [NHGRI — Genetic Code](https://www.genome.gov/genetics-glossary/Genetic-Code) | 코돈과 아미노산의 대응 관계 | 1-4 |
| [6] | [NHGRI — Codon](https://www.genome.gov/genetics-glossary/Codon) | 64개 코돈과 번역 종료 신호 | 1-4 |
| [7] | [NCI — What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer) | How Does Cancer Develop? | 2-2 |
| [8] | [NHGRI — Oncogene](https://www.genome.gov/genetics-glossary/Oncogene) | Oncogene의 정의와 역할 | 2-2 |
| [9] | [NCI GDC — TCGA Resources](https://gdc.cancer.gov/about-data/gdc-data-processing/resources-tcga-users) | TCGA 프로젝트 및 데이터 개요 | 4-1 |
| [10] | [NCI GDC — TCGA Study Abbreviations](https://gdc.cancer.gov/resources-tcga-users/tcga-code-tables/tcga-study-abbreviations) | 암종 코드 및 공식 영문명 | 4-2, 4-3 |

### 6-2. 학술 논문

**[11] Vogelstein et al. (2013)**

*Cancer Genome Landscapes*

- 학술지: Science
- DOI: https://doi.org/10.1126/science.1235122
- 참고 내용: 암 유전체, 암 관련 유전자, Driver 및 Passenger 변이
- 문서 내 활용: 2-2, 2-3

**[12] Hoadley et al. (2018)**

*Cell-of-Origin Patterns Dominate the Molecular Classification of 10,000 Tumors from 33 Types of Cancer*

- 학술지: Cell
- DOI: https://doi.org/10.1016/j.cell.2018.03.022
- 원문: https://pmc.ncbi.nlm.nih.gov/articles/PMC5957518/
- 참고 내용: TCGA 33개 암종의 통합 분자 분석 및 세포 기원에 따른 분류
- 참고 부분: Summary, Results
- 문서 내 활용: 3-2, 3-3

### 6-3. 프로젝트 내부 자료

| 자료 | 활용 내용 | 문서 내 활용 위치 |
|---|---|---|
| `notebooks/H_data/01_eda.ipynb` | 데이터 구조 및 변이 표기 | 5-1, 5-2 |
| `notebooks/H_data/02_features.ipynb` | 변이 기반 피처 생성 | 5-4 |

---

## 문서 범위 및 해석상 주의

- 본 문서는 유전체·암종 분류에 필요한 기초 생물학 개념을 설명한다.
- 실제 변이 표기법은 `ngs_research.md`에서 다룬다.
- Hotspot, Position-bin 등 프로젝트의 변이 기반 피처는 `mutation_features.md`에서 다룬다.
- 변이 서명과 염기 치환 패턴은 `mutation_signatures.md`에서 다룬다.
- 논문의 생물학적 연구 결과와 본 프로젝트의 실험 결과는 구분한다.
- 본 문서는 임상 진단 기준이나 특정 암종의 확정 진단 방법을 제시하는 자료가 아니다.