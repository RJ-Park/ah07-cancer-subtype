
# NGS 및 유전체 변이 조사 정리

> **문서 목적**
>
> NGS를 통해 유전체 변이가 검출되는 과정과 변이 표기법을 이해하고, 암종별 주요 유전자 및 유전체 특징을 정리한다.
>
> 기존 팀 발표 자료인 「데이터와 NGS 이해」를 기반으로 작성했으며, 생물학 비전공자도 이해할 수 있도록 핵심 개념을 설명한다.
>
> **주의:** 문헌에 보고된 유전체 특징과 본 프로젝트 데이터에서 직접 관측할 수 있는 정보는 구분한다.

## 목차

1. NGS에서 변이 테이블까지
2. 주요 유전체 변이 유형
3. 변이 표기법과 실제 데이터 해석
4. TCGA 암종별 주요 관련 유전자 및 유전체 특징
5. 프로젝트 데이터와의 연결
6. 기존 팀 공유 분석 기록
7. 참고 자료 및 출처

---

## 1. NGS에서 변이 테이블까지

### 1-1. NGS란?

NGS(Next-Generation Sequencing, 차세대 염기서열 분석)는 DNA 또는 RNA의 염기서열을 대량으로 읽어 분석하는 기술이다.

기존의 Sanger sequencing과 비교했을 때, 많은 DNA 조각을 병렬로 분석할 수 있다는 특징이 있다.

NGS는 암 연구에서 다음과 같은 목적으로 활용된다.

- 암세포에서 발생한 DNA 변이 확인
- 암 관련 유전자 및 변이 패턴 연구
- 암종 간 유전체 특징 비교
- 암의 발생 및 진행에 관여하는 분자적 기전 연구

다만 **NGS는 분석 기술의 범주를 의미하며, 모든 NGS 검사가 동일한 정보를 제공하는 것은 아니다.**

### 1-2. 주요 시퀀싱 방법

| 방법 | 분석 대상 | 특징 |
|---|---|---|
| WGS (Whole Genome Sequencing) | 전체 유전체 | 단백질 암호화 영역과 비암호화 영역을 폭넓게 분석 |
| WES (Whole Exome Sequencing) | 주로 단백질 암호화 영역(엑솜) | 단백질 서열에 영향을 주는 변이 연구에 활용 |
| Targeted Sequencing | 선택한 유전자 또는 특정 영역 | 관심 유전자에 집중해 분석 |
| RNA-seq | RNA | 유전자 발현, 전사체 및 일부 RNA 수준 변화를 분석 |

**예시**

`BRAF V600E` 같은 단백질 변이를 확인하려면 해당 변이를 포함하는 DNA 영역이 분석 대상에 포함되어 있어야 한다.

반면 유전자 발현량은 DNA 변이 정보만으로 직접 측정할 수 없다. 일반적으로 RNA-seq 등의 별도 분석이 필요하다.

### 1-3. NGS 분석 과정

NGS에서 변이 정보가 만들어지는 일반적인 흐름은 다음과 같다.

```text
환자 검체
   │
   ▼
DNA 추출
   │
   ▼
라이브러리 제작
   │
   ▼
NGS 시퀀싱
   │
   ▼
Raw Reads (FASTQ)
   │
   ▼
참조 유전체에 정렬 (Alignment)
   │
   ▼
정렬 결과 (BAM / CRAM)
   │
   ▼
변이 검출 (Variant Calling)
   │
   ▼
변이 정보 (VCF)
   │
   ▼
변이 주석화 (Annotation)
   │
   ▼
유전자별 변이 테이블
```

위 과정은 DNA 변이 분석의 대표적인 예시다.

실제 분석 과정은 시퀀싱 플랫폼, 검체 종류, 분석 목적에 따라 달라질 수 있다.

### 1-4. 주요 파일 형식

| 형식 | 의미 | 담고 있는 정보 |
|---|---|---|
| FASTQ | 시퀀싱 원본 데이터 | 읽어낸 염기서열과 품질 점수 |
| BAM / CRAM | 정렬된 시퀀싱 데이터 | 각 Read가 참조 유전체의 어디에 정렬되는지 |
| VCF | Variant Call Format | 검출된 유전체 변이와 관련 정보 |
| MAF | Mutation Annotation Format | 암 연구에서 활용되는 변이 주석 정보 |

**핵심 구분**

- FASTQ: 실제로 읽어낸 염기서열
- BAM/CRAM: 참조 유전체와 비교한 정렬 결과
- VCF: 검출된 변이 기록
- 유전자별 변이 테이블: 변이 정보를 분석 목적에 맞게 재구성한 데이터

본 프로젝트에서 사용하는 `R132H`, `V600E` 등의 값은 원시 염기서열이 아니라 **단백질 수준의 변이 표기**에 해당한다.

따라서 프로젝트 데이터만으로 원본 FASTQ나 DNA 염기서열을 복원할 수는 없다.

### 1-5. Variant Calling이란?

Variant Calling(변이 검출)은 시퀀싱 결과를 참조 유전체와 비교해 DNA 서열의 차이를 찾아내는 과정이다.

예를 들어 다음과 같은 차이가 검출될 수 있다.

```text
참조 DNA: A T G G A A C
샘플 DNA: A T G G A C C
                    ^
```

위 예시는 한 위치의 염기가 `A → C`로 달라진 경우다.

그러나 실제 분석에서는 단순히 한 Read가 다르다고 해서 변이로 확정하지 않는다.

일반적으로 다음 요소를 함께 고려한다.

- 해당 위치를 읽은 Read 수(Depth)
- 변이를 지지하는 Read의 비율
- 염기 품질 및 정렬 품질
- 시퀀싱 또는 정렬 과정의 오류 가능성
- 정상 조직과 종양 조직의 비교 여부

암 유전체 분석에서는 특히 다음을 구분하는 것이 중요하다.

| 구분 | 의미 |
|---|---|
| Germline variant | 생식세포 계열에서 유래해 개인의 세포에 광범위하게 존재하는 변이 |
| Somatic variant | 출생 이후 특정 세포 계통에서 발생한 변이 |

암 연구에서는 종양에서 획득된 Somatic variant를 중요한 분석 대상으로 삼는다.

다만 종양 데이터에 존재하는 변이가 모두 Somatic variant인 것은 아니다. 정상 검체와의 비교, 분석 절차 등을 통해 구분해야 한다.

---

## 2. 주요 유전체 변이 유형

### 2-1. 변이 유형이란?

DNA 서열의 변화는 단백질에 서로 다른 영향을 줄 수 있다.

예를 들어 DNA의 염기 하나가 바뀌더라도 다음과 같은 결과가 발생할 수 있다.

- 아미노산이 다른 아미노산으로 변경
- 아미노산은 그대로 유지
- 단백질 합성이 조기에 종료
- 단백질의 읽기 틀이 변경

이러한 차이를 구분하기 위해 변이 유형을 사용한다.

### 2-2. 주요 변이 유형

| 변이 유형 | 표기 예시 | 의미 |
|---|---|---|
| 미스센스 (Missense) | `R132H`, `V600E` | 아미노산이 다른 아미노산으로 바뀜 |
| 동의 변이 (Synonymous) | `D623D`, `L42L` | DNA 서열이 변했지만 아미노산은 동일 |
| 넌센스 (Nonsense) | `R213*`, `E237*` | 종결 코돈이 생겨 단백질 합성이 조기에 종료될 수 있음 |
| 프레임시프트 (Frameshift) | `K16fs`, `L1854fs` | 삽입·결실 등으로 단백질 번역의 읽기 틀이 바뀜 |
| 인프레임 결실 (In-frame deletion) | `E746_A750del` | 읽기 틀을 유지하면서 아미노산이 삭제됨 |
| 인프레임 삽입 (In-frame insertion) | `A767_V769ins...` | 읽기 틀을 유지하면서 아미노산이 삽입됨 |
| 중복 (Duplication) | `A767_V769dup` | 특정 서열이 반복됨 |
| 스플라이스 변이 (Splice-site) | `c.1903+1G>A` | RNA 스플라이싱에 영향을 줄 수 있음 |
| 시작 코돈 변이 (Start-loss) | `M1?` | 단백질 번역 시작에 영향을 줄 수 있음 |
| 종결 코돈 소실 (Stop-loss) | `*110Qext*17` | 기존 종결 코돈이 사라져 단백질이 연장될 수 있음 |
| 유전자 융합 (Gene fusion) | `BCR::ABL1` | 서로 다른 유전자 영역이 연결됨 |
| 복제수 변이 (CNV) | `ERBB2 amplification` | 유전자 또는 DNA 구간의 복제수가 증가하거나 감소함 |
| 기타/미분류 | 별도 확인 필요 | 위 규칙으로 분류하기 어려운 경우 |

> **표기 주의**
>
> 위 표의 일부 예시는 데이터에서 자주 보이는 축약 표기다. HGVS의 완전한 표준 표기와는 차이가 있을 수 있다.
>
> 예를 들어 `K16fs`는 프레임시프트를 간략하게 표현한 형태이며, 정확한 단백질 변화와 새로운 종결 위치를 기술하려면 추가 정보가 필요할 수 있다.
>
> 또한 `A767_V769dup`은 삽입과 관련된 변화이지만 표기법상으로는 중복(Duplication)에 해당하므로 일반적인 삽입(Insertion)과 구분한다.

### 2-3. Missense와 Synonymous의 차이

**Missense**

```text
DNA 코돈: GAA → GAC
아미노산:  E  →  D
```

DNA 변화로 아미노산이 바뀌는 경우다.

**Synonymous**

```text
DNA 코돈: GAA → GAG
아미노산:  E  →  E
```

DNA는 변했지만 동일한 아미노산을 지정하는 경우다.

따라서 `R895R`처럼 앞뒤 아미노산이 동일한 표기는 Synonymous 변이를 나타낼 수 있다.

다만 **단백질 표기만으로 실제 DNA의 어떤 염기가 바뀌었는지 확정할 수는 없다.**

또한 Synonymous 변이라고 해서 반드시 생물학적 영향이 없는 것은 아니다. 일부 변이는 RNA 스플라이싱이나 유전자 발현 등에 영향을 줄 수 있다.

### 2-4. Truncating mutation이란?

Truncating mutation은 단백질이 정상적인 길이보다 짧아지도록 만드는 변이를 통칭하는 표현이다.

대표적으로 다음과 같은 변이가 포함될 수 있다.

- Nonsense mutation
- Frameshift mutation 중 조기 종결을 유발하는 경우
- 일부 스플라이싱 관련 변이

**주의:** Truncating은 단일한 변이 표기 유형이라기보다 단백질에 미치는 결과를 기준으로 묶는 개념이다.

모든 Frameshift나 Splice-site 변이를 실제 기능 검증 없이 동일한 Truncating 변이로 확정해서는 안 된다.

---

## 3. 변이 표기법과 실제 데이터 해석

### 3-1. 단백질 변이 표기 읽는 방법

다음 변이를 살펴보자.

```text
R132H
```

| 구성 | 의미 |
|---|---|
| R | 기존 아미노산: Arginine |
| 132 | 단백질 내 아미노산 위치 |
| H | 변경된 아미노산: Histidine |

즉, **단백질의 132번 위치에서 Arginine이 Histidine으로 바뀌었다**는 의미다.

다른 예시:

| 표기 | 해석 |
|---|---|
| `V600E` | 600번 위치의 Valine → Glutamate |
| `R175H` | 175번 위치의 Arginine → Histidine |
| `R895R` | 895번 위치의 Arginine이 유지됨 |
| `R213*` | 213번 위치가 종결 신호로 바뀜 |

### 3-2. 주요 아미노산 한 글자 코드

| 코드 | 아미노산 | 코드 | 아미노산 |
|---|---|---|---|
| A | Alanine | R | Arginine |
| N | Asparagine | D | Aspartate |
| C | Cysteine | Q | Glutamine |
| E | Glutamate | G | Glycine |
| H | Histidine | I | Isoleucine |
| L | Leucine | K | Lysine |
| M | Methionine | F | Phenylalanine |
| P | Proline | S | Serine |
| T | Threonine | W | Tryptophan |
| Y | Tyrosine | V | Valine |

`*`는 일반적으로 단백질 변이 표기에서 번역 종료 신호를 나타낸다.

### 3-3. HGVS 표기법

HGVS(Human Genome Variation Society)는 유전체 변이를 일관되게 기술하기 위한 표기 규칙을 제공한다.

변이 표기에는 분석 수준을 나타내는 접두어가 사용된다.

| 접두어 | 의미 | 예시 |
|---|---|---|
| `g.` | Genomic DNA 수준 | `g.123A>G` |
| `c.` | Coding DNA 수준 | `c.215C>G` |
| `n.` | 비암호화 RNA 전사체의 DNA 기준 서열 수준 | `n.76A>G` |
| `r.` | RNA 수준 | `r.76a>g` |
| `p.` | Protein 수준 | `p.Val600Glu` |

위 예시는 표기 형식을 설명하기 위한 것이며, 완전한 HGVS 기술에는 적절한 참조 서열 식별자가 필요하다.

예를 들어 `V600E`는 단백질 수준의 축약 표기이고, `p.Val600Glu`는 HGVS의 단백질 치환 표기 형식이다.

실제로 어떤 유전자와 전사체의 변이인지 정확히 지정하려면 참조 서열 정보가 필요하다.

### 3-4. WT(Wild Type)

WT는 Wild Type의 약어로, 일반적으로 기준형 또는 참조형을 의미한다.

프로젝트 데이터에서는 변이가 기록되지 않은 상태를 나타내는 값으로 사용된다.

다만 `WT`의 정확한 의미는 데이터 생성 방식에 따라 달라질 수 있다.

예를 들어 특정 유전자에서 WT라고 표시되었다고 해서 그 유전자의 모든 가능한 위치에서 변이가 존재하지 않는다는 사실이 보장되는 것은 아니다.

### 3-5. WT와 결측치의 차이

| 값 | 의미 |
|---|---|
| `WT` | 데이터에서 기준형으로 표시된 상태 |
| `NaN` | 값이 기록되지 않았거나 제공되지 않은 상태 |
| `R132H` | 특정 단백질 변이가 기록된 상태 |

**중요한 점**

`WT`와 결측치는 원칙적으로 서로 다른 개념이다.

따라서 결측치를 WT와 동일하게 처리하더라도, 이는 데이터 분석을 위한 가정이지 두 값이 생물학적으로 동일하다는 의미는 아니다.

### 3-6. 하나의 유전자에 여러 변이가 기록된 경우

프로젝트 데이터에는 한 유전자에 여러 변이가 기록된 경우가 있다.

예시:

```text
R273C R248Q
```

이 값은 하나의 유전자 컬럼에 두 개의 단백질 변이 표기가 기록된 형태다.

따라서 다음을 구분해야 한다.

| 개념 | 의미 |
|---|---|
| 변이가 기록된 유전자 수 | 변이 정보가 있는 유전자 컬럼의 개수 |
| 개별 변이 개수 | 각 유전자 컬럼 안에 기록된 변이 토큰의 총개수 |

예를 들어 한 유전자에 두 개의 변이가 있다면 변이가 기록된 유전자 수는 1개지만, 개별 변이 토큰은 2개다.

단, 두 변이가 같은 DNA 분자에 존재하는지, 서로 다른 대립유전자에 존재하는지는 단순 문자열만으로 판단할 수 없다.

---

## 4. TCGA 암종별 주요 관련 유전자 및 유전체 특징

### 4-1. 표를 해석하는 기준

다음 표는 NCI의 TCGA 암종별 연구 요약을 바탕으로 정리한 것이다.

**중요한 구분**

- 변이(Mutation): DNA 서열의 변화
- 발현(Expression): RNA 또는 단백질 생성 수준
- 증폭(Amplification): 특정 DNA 영역의 복제수 증가
- 결실(Deletion): DNA 영역의 일부 또는 전체 손실
- 융합(Fusion): 서로 다른 유전자 영역의 연결
- 경로(Pathway): 여러 분자가 함께 작동하는 생물학적 기능 체계

이들은 서로 다른 정보다.

특정 암종에서 `ERBB2` 증폭이 중요하다고 알려져 있어도, 본 프로젝트의 단백질 변이 표기만으로 `ERBB2` 증폭 여부를 알 수 있는 것은 아니다.

또한 아래 유전자들은 **암종을 확정하는 규칙이나 전체 Driver 유전자 목록이 아니다.**

### 4-2. 암종별 요약

| 코드 | 암종 | 주요 유전자·표지 | 주요 유전체 특징 및 해석 |
|---|---|---|---|
| ACC | 부신피질암 | IGF2, TP53, PRKAR1A | IGF2 과발현, TP53·PRKAR1A 변이, 염색체 복제수 변화 |
| BLCA | 방광 요로상피암 | ERCC2 | 흡연과 ERCC2 변이 및 변이 서명의 연관성, DNA 복구와 세포주기 관련 이상 |
| BRCA | 침윤성 유방암 | ERBB2, CDH1 | HER2 관련 분자 아형, 소엽암에서 E-cadherin 소실 등 |
| CESC | 자궁경부 편평세포암 및 선암 | MED1, ERBB3, CASP8, HLA-A, TGFBR2, BCAR4 | HPV 관련 특성, PI3K/MAPK·TGF-β 경로 변화 및 일부 유전자 융합 |
| CHOL | 담관암 | CDKN2 계열, BAP1, ARID1 계열, FGFR2, IDH1, IDH2 | 종양억제유전자 기능 저하, FGFR2 관련 변화, IDH 변이 아형 |
| COAD | 결장선암 | ARID1A, SOX9, AMER1, ERBB2, IGF2 | WNT 경로 이상, 일부 유전자 변이 및 과발현. NCI에서 READ와 함께 분석 |
| DLBC | 미만성 거대 B세포 림프종 | 별도 검토 필요 | 기존 NCI 암종별 요약 페이지에 구체적인 유전자 설명이 없어 추가 논문 확인 필요 |
| ESCA | 식도암 | ERBB2 | 선암과 편평세포암 사이에 분자적 차이가 있으며 일부 선암에서 ERBB2 변화 |
| GBM | 교모세포종 | EGFR, MDM2, CDK4, NF1, ERBB2, TP53, PIK3R1, TERT | EGFR 및 세포주기 관련 변화, 다양한 분자 아형 |
| HNSC | 두경부 편평세포암 | TRAF3, E2F1, PIK3CA, BIRC2, FADD, TP53, CDKN2A | HPV 양성·음성에 따른 분자적 차이, 변이·증폭·불활성화가 혼재 |
| KICH | 신장 혐색소성 암 | TP53, PTEN, TERT | 상대적으로 낮은 체세포 변이 부담, TERT 프로모터 구조 변화 |
| KIRC | 신장 투명세포암 | VHL, SETD2 | 산소 감지 및 PI3K/AKT/mTOR 경로 이상, SETD2 변이 |
| KIRP | 신장 유두상 세포암 | MET, CDKN2A | 제1형에서 MET 관련 변화, 제2형의 일부에서 CDKN2A 발현 소실 |
| LAML | 급성 골수성 백혈병 | NPM1 | NPM1 및 전사인자·코헤신·신호전달 관련 유전자군의 반복 변이 |
| LGG | 저등급 신경교종 | IDH1, IDH2 | IDH 변이 및 1p/19q 공동결실이 중요한 분자적 특징 |
| LIHC | 간세포암 | TERT, TP53, CTNNB1, MDM4 | TERT 프로모터 및 TP53·CTNNB1 변이, MDM4 관련 변화 |
| LUAD | 폐선암 | KRAS, EGFR, BRAF, NF1 | 성장 신호 전달 경로의 활성화와 관련된 변이 |
| LUSC | 폐편평세포암 | TP53, CDKN2A, HLA-A | TP53 변화 및 CDKN2A 불활성화, 여러 신호전달 경로 이상 |
| MESO | 중피종 | BAP1, TP53, SETDB1, VSIR | BAP1 관련 변화, 일부 TP53·SETDB1 변이, VISTA 발현 특징 |
| OV | 난소 장액성 암 | TP53, BRCA1, BRCA2 | TP53 변이가 매우 빈번하며 일부에서 BRCA1/2 변이 관찰 |
| PAAD | 췌장선암 | KRAS, RREB1 | KRAS 및 RAS–MAPK 경로가 중요한 역할 |
| PCPG | 갈색세포종 및 부신경절종 | CSDE1, MAML3 | CSDE1 변이, MAML3 융합 및 WNT 관련 아형 |
| PRAD | 전립선선암 | SPOP, FOXA1 | 변이 기반 아형과 유전자 융합 기반 아형이 공존 |
| READ | 직장선암 | ARID1A, SOX9, AMER1, ERBB2, IGF2 | NCI에서 COAD와 함께 대장·직장암으로 통합 분석 |
| SARC | 육종 | TP53, ATRX, RB1, SSX1, SSX2, TERT, JUN | 육종 세부 유형에 따라 변이·융합·증폭이 다르게 나타남 |
| SKCM | 피부 흑색종 | BRAF, RAS 계열, NF1, AKT3 | BRAF/RAS/NF1 관련 분자 아형, AKT3 발현 변화 |
| STAD | 위암 | PIK3CA | EBV 양성, MSI, GS, CIN 등 분자 아형 |
| TGCT | 고환 생식세포종양 | KIT, KRAS | 일부 정상피종에서 KIT 변이, KRAS 복제수 변화 및 낮은 변이 빈도 |
| THCA | 갑상선암 | BRAF, RAS 계열, EIF1AX | BRAF V600E 또는 RAS 관련 아형 |
| THYM | 흉선종 | GTF2I, HRAS, NRAS, TP53 | 낮은 변이 부담과 GTF2I 반복 변이 |
| UCEC | 자궁내막암 | POLE, TP53, PTEN, KRAS | POLE 초고변이, MSI, 복제수 고·저 아형 |
| UCS | 자궁암육종 | TP53 | TP53 변이가 빈번하며 PI3K 경로 이상도 관찰 |
| UVM | 포도막 흑색종 | BAP1 | BAP1 변화와 3번 염색체 단일염색체성 및 전이 위험의 연관성 |

※ `AMER1`은 과거 `FAM123B/WTX`, `VSIR`은 `VISTA`로도 알려져 있다.

### 4-3. 실제 프로젝트에서 주의할 점

**① 유전자 이름과 변이 유형을 구분한다.**

예를 들어 `TP53` 컬럼에 `R175H`가 기록되어 있다면 TP53 단백질 수준의 변이 표기로 해석할 수 있다.

그러나 이것만으로 TP53의 발현 증가, 단백질 양 또는 유전자 복제수 변화 여부를 알 수는 없다.

**② 대표 유전자를 암종의 확정 기준으로 사용하지 않는다.**

`TP53`, `KRAS` 등은 여러 암종에서 변이가 발견될 수 있다.

따라서 대표 유전자 하나에 변이가 있다는 이유만으로 특정 암종이라고 단정할 수 없다.

**③ 문헌에서 언급된 모든 유전체 특징을 프로젝트 데이터에 적용할 수 있는 것은 아니다.**

예를 들어 다음 정보는 해당 데이터가 별도로 제공되지 않는 한 직접 관측할 수 없다.

- 유전자 발현량
- 유전자 증폭 및 복제수 변화
- 유전자 융합
- DNA 메틸화
- 염색체 수준의 구조 변화

**④ 동의 변이와 단백질 변화 변이를 구분한다.**

`R895R`과 `R895H`는 서로 다른 유형의 변이 표기다.

두 변이를 모두 단순히 변이 존재로만 처리하면 아미노산 변화 여부에 대한 정보가 사라질 수 있다.

다만 아미노산 변화 여부가 실제 기능적 영향의 크기를 그대로 나타내는 것은 아니다.

---

## 5. 프로젝트 데이터와의 연결

### 5-1. 데이터 구성

기존 프로젝트 분석 기록에 따르면 데이터는 다음과 같이 구성된다.

| 항목 | 내용 |
|---|---|
| Train 샘플 | 6,201개 |
| 유전자 관련 컬럼 | 4,384개 |
| 예측 대상 | 26개 암종(SUBCLASS) |
| 유전자별 값 | WT, 결측치, 단백질 변이 문자열 |

이 수치는 프로젝트의 기존 분석 기록을 기준으로 하며, TCGA 연구 전체의 데이터 규모와는 다르다.

### 5-2. 변이 문자열을 해석할 때 중요한 점

프로젝트의 각 유전자 컬럼은 단백질 변이 표기 또는 WT·결측치 등을 포함한다.

따라서 원본 데이터에서 직접 확인할 수 있는 정보는 주로 다음과 같다.

- 특정 유전자에 변이 표기가 존재하는지
- 어떤 단백질 위치에 변이가 기록되어 있는지
- 어떤 아미노산이 다른 아미노산으로 바뀌었는지
- 단백질 변이 문자열이 어떤 유형에 해당하는지
- 하나의 유전자에 여러 변이 토큰이 기록되었는지

반면 단백질 변이 문자열만으로 다음을 확정할 수는 없다.

- 정확한 DNA 염기 치환
- 원본 시퀀싱 품질
- 변이 대립유전자 비율(VAF)
- 유전자 발현량
- 실제 단백질 기능 변화
- 모든 변이의 Driver/Passenger 여부

### 5-3. 관련 노트북

| 노트북 | 관련 내용 |
|---|---|
| [01_eda.ipynb](../notebooks/H_data/01_eda.ipynb) | 데이터 구조 및 변이 문자열 분석 |
| [02_features.ipynb](../notebooks/H_data/02_features.ipynb) | 변이 유형과 아미노산 치환 정보 활용 |
| [03_hotspot_bins.ipynb](../notebooks/H_data/03_hotspot_bins.ipynb) | 변이 위치와 Hotspot 관련 실험 |
| [04_position_bin_tuning.ipynb](../notebooks/H_data/04_position_bin_tuning.ipynb) | 단백질 위치 구간 관련 실험 |
| [05_mutation_signature.ipynb](../notebooks/H_data/05_mutation_signature.ipynb) | 아미노산 치환 기반 염기 변화 유형 추정 |

Hotspot과 Position-bin은 [mutation_features.md](./mutation_features.md)에서, 변이 서명은 [mutation_signatures.md](./mutation_signatures.md)에서 자세히 설명한다.

---

## 6. 기존 팀 공유 분석 기록

> **보존 목적**
>
> 이 섹션은 기존 `ngs_research.md`의 팀 공유 기록을 요약한 것이다.
>
> 위의 생물학 개념 설명과 달리 프로젝트 내부 분석·실험 기록에 해당한다.
>
> 기존 원본의 상세 실험 결과는 별도로 보존하고, 최신 결과는 해당 노트북과 실험 로그를 기준으로 확인한다.

### 6-1. EDA에서 확인한 내용

- 학습 데이터는 6,201개 샘플, 4,384개 유전자 관련 컬럼, 26개 암종으로 구성된다.
- 유전자별 값은 `WT`, 결측치, `R132H`와 같은 변이 문자열로 구성된다.
- 하나의 셀에 여러 변이가 공백으로 구분되어 기록된 경우가 있다.
- Missense, Synonymous, Nonsense, Frameshift 등 변이 유형에 해당하는 문자열 패턴을 확인했다.
- 동일한 아미노산 치환쌍이 여러 유전자에서 반복적으로 나타날 수 있음을 확인했다.

### 6-2. 피처 구성 관련 관찰

기존 실험에서는 다음과 같은 정보를 활용했다.

| 구분 | 활용 정보 |
|---|---|
| 기본 변이 정보 | 유전자별 변이 존재 여부 |
| 변이 유전자 수 | 변이가 기록된 유전자 컬럼 개수 |
| 변이 유형 | Missense, Synonymous, Nonsense, Frameshift 등의 개수 |
| 개별 변이 정보 | 유전자명과 변이 문자열의 조합 |
| 아미노산 치환쌍 | `R132H → R>H`와 같은 치환 관계 |

이 중 아미노산 치환쌍은 단백질 수준의 변화 정보다.

따라서 DNA 염기서열에서 직접 계산하는 Mutational Signature와 동일한 개념이 아니다.

### 6-3. 기존 실험 결과 보존

기존 문서에는 8개 피처 구성에 대한 XGBoost 교차검증 결과가 기록되어 있다.

| 피처 구성 | 기존 기록의 Macro F1 평균 |
|---|---:|
| A Multi-Hot (빈도 ≥5) | 0.1590 |
| A Multi-Hot (빈도 ≥3) | 0.1630 |
| B 이진 인코딩 | 0.3200 |
| C 변이 유전자 수 추가 | 0.3663 |
| D 변이 유형별 개수 추가 | 0.3836 |
| D + Multi-Hot (빈도 ≥5) | 0.3867 |
| D + Multi-Hot (빈도 ≥3) | 0.3851 |
| D + 아미노산 치환쌍 (빈도 ≥16) | 0.4271 |

이 표는 **기존 팀 공유 기록을 보존하기 위한 자료**이며, 생물학 개념에 대한 문헌적 근거는 아니다.

후속 실험에 따라 최종 피처 구성이나 성능은 달라질 수 있다.

관련 파일:

- `notebooks/H_data/02_features.ipynb`
- `experiments/log_H_data.csv`
- `src/features.py`

---

## 7. 참고 자료 및 출처

### 7-1. 공식 기관 및 기술 문서

| 번호 | 출처 | 참고한 부분 | 문서 내 활용 위치 |
|---|---|---|---|
| [1] | [NHGRI — DNA Sequencing](https://www.genome.gov/genetics-glossary/DNA-Sequencing) | DNA 시퀀싱의 기본 개념 | 1-1 |
| [2] | [NHGRI — Whole Genome Sequencing](https://www.genome.gov/genetics-glossary/Whole-Genome-Sequencing) | 전체 유전체 분석의 범위 | 1-2 |
| [3] | [GATK — Best Practices Workflows](https://gatk.broadinstitute.org/hc/en-us/sections/360007226651-Best-Practices-Workflows) | 정렬, 전처리 및 변이 검출 워크플로 | 1-3, 1-5 |
| [4] | [SAMtools / HTSlib](https://www.htslib.org/) | SAM/BAM/CRAM 및 VCF/BCF 파일 형식 | 1-4 |
| [5] | [HGVS — Sequence Variant Nomenclature](https://hgvs-nomenclature.org/stable/) | 변이 표기 규칙 및 참조 서열 | 2-2, 3-1, 3-3 |
| [6] | [HGVS — Protein Substitution](https://hgvs-nomenclature.org/stable/recommendations/protein/substitution/) | 단백질 치환 표기 | 2-2, 3-1 |
| [7] | [HGVS — Frameshift](https://hgvs-nomenclature.org/stable/recommendations/protein/frameshift/) | 프레임시프트 표기 | 2-2 |
| [8] | [NCI — TCGA Cancers Selected for Study](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/studied-cancers) | TCGA 암종별 연구 개요 및 관련 논문 | 4-1, 4-2 |
| [9] | [NCI — TCGA Cancers Selected for Study, 연구 결과 요약](https://www.cancer.gov/about-nci/organization/dcb/research-programs/past-programs/tcga-cancers-selected-for-study) | 암종별 주요 유전자 및 분자적 특징 | 4-2, 4-3 |
| [10] | [NCI GDC — TCGA Study Abbreviations](https://gdc.cancer.gov/resources-tcga-users/tcga-code-tables/tcga-study-abbreviations) | 암종 약어 및 공식 명칭 | 4-2 |

### 7-2. 관련 학술 논문

**[11] Koboldt et al. (2013)**

*The Next-Generation Sequencing Revolution and Its Impact on Genomics*

- 학술지: Cell
- DOI: https://doi.org/10.1016/j.cell.2013.09.006
- 참고 내용: 차세대 염기서열 분석 기술과 유전체 연구에서의 활용
- 문서 내 활용: 1-1, 1-2

**[12] McKenna et al. (2010)**

*The Genome Analysis Toolkit: A MapReduce Framework for Analyzing Next-Generation DNA Sequencing Data*

- 학술지: Genome Research
- DOI: https://doi.org/10.1101/gr.107524.110
- 참고 내용: NGS 데이터 분석 및 변이 검출을 위한 계산적 분석 체계
- 문서 내 활용: 1-3, 1-5

**[13] Vogelstein et al. (2013)**

*Cancer Genome Landscapes*

- 학술지: Science
- DOI: https://doi.org/10.1126/science.1235122
- 참고 내용: 암 유전체의 변이, Driver/Passenger 변이, 암 관련 유전자
- 문서 내 활용: 4-1, 4-3

**[14] The Cancer Genome Atlas Research Network (2014)**

*Comprehensive Molecular Profiling of Lung Adenocarcinoma*

- 학술지: Nature
- DOI: https://doi.org/10.1038/nature13385
- 참고 내용: 폐선암의 유전체 변이와 주요 신호전달 경로
- 문서 내 활용: 4-2, LUAD 항목

**[15] The Cancer Genome Atlas Research Network (2015)**

*Genomic Classification of Cutaneous Melanoma*

- 학술지: Cell
- DOI: https://doi.org/10.1016/j.cell.2015.05.044
- 참고 내용: BRAF, RAS, NF1 및 Triple-WT 기반 피부 흑색종 분류
- 문서 내 활용: 4-2, SKCM 항목

**[16] The Cancer Genome Atlas Research Network (2014)**

*Integrated Genomic Characterization of Papillary Thyroid Carcinoma*

- 학술지: Cell
- DOI: https://doi.org/10.1016/j.cell.2014.09.050
- 참고 내용: BRAF V600E와 RAS 관련 갑상선암 분자적 특성
- 문서 내 활용: 4-2, THCA 항목

### 7-3. 프로젝트 내부 자료

| 자료 | 참고 내용 | 문서 내 활용 위치 |
|---|---|---|
| `notebooks/H_data/01_eda.ipynb` | 데이터 구조 및 변이 문자열 관찰 | 3-5, 3-6, 5, 6-1 |
| `notebooks/H_data/02_features.ipynb` | 변이 유형과 아미노산 치환쌍 활용 | 5, 6-2, 6-3 |
| `src/features.py` | 변이 유형 관련 함수 구현 | 6-3 |
| `experiments/log_H_data.csv` | 기존 피처 실험 기록 | 6-3 |

---

## 문서 범위 및 해석상 주의

1. 본 문서는 NGS와 유전체 변이에 대한 기초 개념을 설명한다.
2. 변이 표기는 HGVS 표준과 데이터셋의 축약 표현을 구분한다.
3. 단백질 변이 정보만으로 DNA의 정확한 염기 치환을 확정하지 않는다.
4. TCGA 문헌의 발현·복제수·융합 정보는 해당 측정값이 없는 프로젝트 데이터에서 직접 관측할 수 없다.
5. 암종별 관련 유전자 목록은 연구 결과를 요약한 것으로, 특정 암종을 확정하는 진단 규칙이 아니다.
6. 기존 프로젝트의 분석 결과는 학술 논문에서 검증된 일반적인 생물학적 사실과 구분한다.
7. Hotspot, Position-bin 및 변이 서명에 관한 상세 설명은 각각 별도 문서에서 다룬다.