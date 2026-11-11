
# 돌연변이 서명(Mutational Signatures) 조사

> **문서 목적**
>
> 암 유전체에서 나타나는 DNA 염기 치환 패턴과 Mutational Signature의 개념을 이해하고, 본 프로젝트에서 시도한 단백질 변이 기반 치환 패턴 추정 방식의 원리와 한계를 정리한다.
>
> **핵심 구분**
>
> - DNA 염기 치환 패턴: 실제 DNA에서 발생한 염기 변화
> - COSMIC SBS Signature: 염기 치환과 주변 염기서열 맥락을 바탕으로 추정한 돌연변이 과정의 특징
> - 프로젝트의 추정 피처: 단백질 변이 문자열로부터 가능한 염기 치환 정보를 간접적으로 추정한 값
>
> 세 가지는 서로 관련이 있지만 동일한 개념이 아니다.

## 목차

1. Mutational Signature란?
2. DNA 염기 치환의 6가지 유형
3. SBS96과 Trinucleotide Context
4. COSMIC Mutational Signatures
5. 단백질 변이에서 DNA 치환을 추정하는 원리
6. 프로젝트의 Mutation Signature 관련 피처
7. 실제 SBS Signature와 프로젝트 피처의 차이
8. 프로젝트 적용 시 주의사항
9. 참고 자료 및 출처

---

## 1. Mutational Signature란?

### 1-1. 기본 개념

Mutational Signature(돌연변이 서명)는 유전체에 축적된 돌연변이의 유형과 분포를 분석하여, 그 변이를 만들어 낸 생물학적 과정이나 외부 요인의 흔적을 파악하는 개념이다.

쉽게 말하면 다음과 같다.

```text
DNA 손상 또는 돌연변이 발생 과정
          │
          ▼
특정한 유형의 변이가 축적됨
          │
          ▼
변이 유형별 분포를 분석
          │
          ▼
Mutational Signature
```

예를 들어 서로 다른 원인으로 발생한 DNA 손상은 서로 다른 변이 패턴을 남길 수 있다.

대표적인 관련 요인은 다음과 같다.

- 자외선(UV) 노출
- 담배 연기와 관련된 돌연변이 유발 물질
- 세포 내 자연적인 DNA 화학 변화
- APOBEC 계열 효소의 작용
- DNA 복구 과정의 이상

단, 모든 Mutational Signature의 원인이 밝혀진 것은 아니다.

### 1-2. 변이 하나와 Mutational Signature의 차이

특정 변이 하나가 발견되었다고 해서 Mutational Signature를 확인한 것은 아니다.

예를 들어 다음과 같은 DNA 변이가 있다고 가정하자.

```text
변이 1: C>T
변이 2: C>A
변이 3: C>T
변이 4: T>G
```

이 변이들을 모으면 어떤 유형이 상대적으로 많이 발생했는지 확인할 수 있다.

하지만 이러한 단순 빈도만으로 특정 돌연변이 원인을 확정할 수는 없다.

실제 Mutational Signature 분석에서는 많은 변이의 유형과 주변 염기서열 정보를 종합적으로 분석한다.

### 1-3. 관련 연구의 시작

Alexandrov et al. (2013)은 7,042개 암 샘플에서 약 493만 개의 체세포 변이를 분석하여 20개 이상의 서로 다른 돌연변이 서명을 확인했다.

이 연구는 암 유전체에 축적된 변이의 패턴을 통해 돌연변이 발생 과정의 특징을 연구할 수 있음을 보여주었다.

이후 대규모 암 유전체 데이터가 축적되면서 Mutational Signature의 종류와 분석 방법도 확장되었다.

---

## 2. DNA 염기 치환의 6가지 유형

### 2-1. Single Base Substitution(SBS)

SBS는 DNA의 염기 하나가 다른 염기로 바뀌는 현상이다.

예를 들어 다음과 같다.

```text
기준 DNA: A C G
변이 DNA: A T G
            ^
```

가운데 염기가 C에서 T로 바뀌었으므로 `C>T` 치환이다.

### 2-2. 왜 6가지 유형으로 구분할까?

DNA에는 A, T, G, C 네 가지 염기가 있다.

각 염기는 자신을 제외한 세 가지 염기로 바뀔 수 있으므로 방향을 구분하면 총 12가지 치환이 가능하다.

하지만 DNA는 상보적인 두 가닥으로 이루어져 있다.

```text
A ↔ T
C ↔ G
```

따라서 상보적인 가닥에서 관찰한 치환을 동일한 유형으로 묶을 수 있다.

예를 들어 다음 두 표기는 상보적인 관계다.

```text
C>T
G>A
```

Mutational Signature 분석에서는 일반적으로 피리미딘 염기(C 또는 T)를 기준으로 표준화한다.

그 결과 6가지 SBS 유형을 사용한다.

### 2-3. SBS의 6가지 기본 유형

| 유형 | 의미 | 상보적 치환 |
|---|---|---|
| C>A | Cytosine → Adenine | G>T |
| C>G | Cytosine → Guanine | G>C |
| C>T | Cytosine → Thymine | G>A |
| T>A | Thymine → Adenine | A>T |
| T>C | Thymine → Cytosine | A>G |
| T>G | Thymine → Guanine | A>C |

예를 들어 DNA에서 `G>A`가 관찰되면, 상보적 관계를 이용해 `C>T` 유형으로 정규화할 수 있다.

**중요:** 이 표준화는 두 DNA 가닥을 중복해서 계산하지 않기 위한 표현 방식이다. 실제로 어느 가닥에서 손상이 시작되었는지를 확정한다는 의미는 아니다.

### 2-4. Transition과 Transversion

DNA 염기 치환은 염기의 화학적 계열에 따라 구분할 수도 있다.

| 구분 | 의미 | 예시 |
|---|---|---|
| Transition | 같은 계열의 염기끼리 치환 | C>T, T>C |
| Transversion | 서로 다른 계열의 염기끼리 치환 | C>A, C>G, T>A, T>G |

염기의 계열은 다음과 같다.

- Purine(퓨린): A, G
- Pyrimidine(피리미딘): C, T

이 구분은 염기 치환의 종류를 이해하는 데 유용하다.

다만 Transition/Transversion 비율만으로 특정 COSMIC Signature를 판별할 수는 없다.

---

## 3. SBS96과 Trinucleotide Context

### 3-1. SBS6만으로는 부족한 이유

SBS6는 어떤 염기가 무엇으로 바뀌었는지만 나타낸다.

하지만 동일한 `C>T` 변이라도 주변에 어떤 염기가 존재하는지에 따라 돌연변이 발생 확률이 달라질 수 있다.

예를 들어 다음 두 변이를 살펴보자.

```text
변이 A: A[C>T]G
변이 B: T[C>T]A
```

두 변이 모두 가운데 염기는 `C>T`다.

하지만 주변 염기서열은 서로 다르다.

따라서 변이가 발생한 위치의 염기서열 맥락을 함께 분석하면 더 세밀한 변이 패턴을 표현할 수 있다.

### 3-2. Trinucleotide Context란?

Trinucleotide Context는 변이가 발생한 염기와 바로 양옆에 위치한 염기를 함께 고려하는 방식이다.

```text
5' - A C G - 3'
         ^
       변이 위치
```

이 예시에서 가운데 C가 T로 바뀌었다면 다음과 같이 표현한다.

```text
A[C>T]G
```

구성은 다음과 같다.

| 구성 | 의미 |
|---|---|
| A | 변이 위치의 5' 방향 인접 염기 |
| C>T | 실제 염기 치환 |
| G | 변이 위치의 3' 방향 인접 염기 |

### 3-3. 왜 96개 유형일까?

SBS96은 다음 요소를 조합한다.

- 염기 치환 유형: 6가지
- 5' 방향 인접 염기: 4가지
- 3' 방향 인접 염기: 4가지

따라서 다음과 같이 계산된다.

```text
6 × 4 × 4 = 96
```

즉, SBS96은 DNA의 단일 염기 치환을 주변 염기서열까지 포함해 96개 범주로 구분한 방식이다.

### 3-4. SBS6와 SBS96 비교

| 구분 | SBS6 | SBS96 |
|---|---|---|
| 분류 기준 | 염기 치환 종류 | 염기 치환 + 양옆 염기 |
| 유형 수 | 6 | 96 |
| 예시 | C>T | A[C>T]G |
| 정보량 | 상대적으로 적음 | 주변 염기 맥락 포함 |
| 필요한 정보 | 정확한 DNA 염기 치환 | DNA 염기 치환 및 참조 서열의 인접 염기 |

**주의:** SBS96은 96개 변이 범주를 의미한다.

96개의 Mutational Signature가 존재한다는 뜻이 아니다.

### 3-5. SBS96을 계산하려면?

일반적으로 다음 정보가 필요하다.

1. 변이가 발생한 염색체
2. 참조 유전체상의 정확한 위치
3. 변이 전 DNA 염기
4. 변이 후 DNA 염기
5. 변이 위치 양옆의 참조 염기서열

따라서 단백질 변이 표기인 `R132H`만으로는 정확한 SBS96 범주를 결정할 수 없다.

---

## 4. COSMIC Mutational Signatures

### 4-1. COSMIC이란?

COSMIC(Catalogue Of Somatic Mutations In Cancer)은 암에서 발견되는 체세포 변이 정보를 수집하고 제공하는 데이터베이스다.

COSMIC Mutational Signatures는 암 유전체에서 관찰되는 돌연변이 패턴과 관련된 참조 서명을 제공한다.

대표적으로 다음과 같은 유형이 있다.

| 구분 | 의미 |
|---|---|
| SBS | Single Base Substitution |
| DBS | Doublet Base Substitution |
| ID | Small Insertion and Deletion |

본 문서에서는 SBS를 중심으로 설명한다.

### 4-2. SBS Signature란?

SBS Signature는 DNA의 단일 염기 치환 패턴을 기반으로 정의되는 돌연변이 서명이다.

일반적으로 SBS96 범주에 대한 상대적인 변이 비율로 표현된다.

```text
SBS96 변이 분포
       │
       ▼
여러 변이 패턴을 분석
       │
       ▼
SBS Signature 추정
       │
       ▼
돌연변이 발생 과정과의 연관성 연구
```

한 암 샘플에서 여러 돌연변이 과정이 동시에 작용할 수 있으므로 여러 Signature가 함께 나타날 수 있다.

### 4-3. 대표적인 COSMIC SBS Signature

| Signature | 주요 연관성 | 해석 |
|---|---|---|
| SBS1 | 5-methylcytosine의 탈아미노화 | 세포 내 자연적인 화학 변화와 관련 |
| SBS2 | APOBEC 계열 효소 | 특정 염기서열 맥락에서의 C>T 변이 |
| SBS13 | APOBEC 계열 효소 | 특정 염기서열 맥락에서의 C>G 변이 |
| SBS4 | 담배 연기 관련 돌연변이 유발 물질 | 일부 흡연 관련 암에서 관찰 |
| SBS7 계열 | 자외선(UV) 노출 | 피부암 등에서 관찰 |
| SBS10 계열 | DNA polymerase proofreading 이상 | 일부 POLE 관련 종양에서 관찰 |

이 표는 대표적인 연관성을 간단히 요약한 것이다.

Signature와 원인 사이의 근거 수준은 서로 다르며, 하나의 Signature가 특정 원인이나 암종을 확정하는 진단 기준은 아니다.

### 4-4. 암종과 Signature의 관계

암종마다 노출되는 환경과 DNA 복구 과정이 다를 수 있다.

따라서 Mutational Signature의 분포도 암종에 따라 달라질 수 있다.

예를 들어 다음과 같은 연관성이 연구되어 왔다.

- 피부암: 자외선 관련 변이 패턴
- 일부 폐암: 흡연 관련 변이 패턴
- 일부 종양: DNA 복구 또는 복제 오류 관련 변이 패턴

그러나 같은 Signature가 여러 암종에서 나타날 수 있다.

따라서 Signature 하나만으로 암종을 확정할 수는 없다.

### 4-5. 관련 대규모 연구

Alexandrov et al. (2020)은 23,829개 암 샘플의 대규모 변이 데이터를 분석했다.

이 연구는 SBS뿐 아니라 DBS와 작은 삽입·결실 변이까지 포함해 다양한 Mutational Signature를 체계적으로 조사했다.

연구 결과는 돌연변이 서명이 암종마다 다른 분포를 보이며, 여러 생물학적 과정과 관련될 수 있음을 보여준다.

단, 연구에서 사용한 Signature 수는 해당 시점의 결과다. 현재 COSMIC 데이터베이스의 Signature 수와 동일하다고 가정해서는 안 된다.

---

## 5. 단백질 변이에서 DNA 치환을 추정하는 원리

### 5-1. 프로젝트 데이터의 한계

본 프로젝트는 주로 다음과 같은 단백질 변이 표기를 사용한다.

```text
R132H
V600E
G12D
R213*
```

이 표기는 아미노산 변화와 단백질 위치를 나타낸다.

그러나 정확히 어떤 DNA 염기가 바뀌었는지는 직접 제공하지 않는다.

따라서 실제 DNA 변이 정보를 이용하는 SBS 분석과는 차이가 있다.

### 5-2. 코돈을 이용한 역추정

코돈은 3개의 염기로 구성되며 아미노산을 지정한다.

예를 들어 다음과 같다.

| DNA 코돈 | 아미노산 |
|---|---|
| GAA | E (Glutamate) |
| GAG | E (Glutamate) |
| GAC | D (Aspartate) |
| GAT | D (Aspartate) |

단백질에서 `E>D` 치환이 관찰되었다면 다음과 같은 코돈 변화가 가능하다.

```text
GAA → GAC
GAA → GAT
GAG → GAC
GAG → GAT
```

하지만 위 후보가 모두 단일 염기 치환인 것은 아니다.

| 코돈 변화 | 다른 염기 수 | 단일 염기 치환 여부 |
|---|---:|---|
| GAA → GAC | 1 | 가능 |
| GAA → GAT | 1 | 가능 |
| GAG → GAC | 1 | 가능 |
| GAG → GAT | 1 | 가능 |

이 예시에서는 네 후보 모두 단일 염기 치환이지만, 다른 아미노산 치환쌍에서는 두 개 이상의 염기 변화가 필요한 코돈 조합도 존재할 수 있다.

따라서 코돈을 이용한 추정에서는 후보 코돈 간 차이를 확인해야 한다.

### 5-3. 왜 정확한 DNA 치환을 알 수 없을까?

하나의 아미노산을 여러 코돈이 지정할 수 있기 때문이다.

예를 들어 Arginine(R)은 여러 코돈으로 지정된다.

```text
CGT, CGC, CGA, CGG, AGA, AGG
```

Histidine(H)은 다음 코돈으로 지정된다.

```text
CAT, CAC
```

따라서 `R>H`라는 정보만으로는 어떤 코돈이 어떤 코돈으로 바뀌었는지 확정할 수 없다.

또한 단백질 위치가 알려져 있더라도 실제 전사체의 DNA 서열을 확인하지 않으면 정확한 변이 위치와 염기를 결정할 수 없다.

### 5-4. 가능한 치환과 실제 치환의 차이

다음 두 개념은 반드시 구분해야 한다.

| 구분 | 의미 |
|---|---|
| 가능한 염기 치환 | 아미노산 변화와 유전암호를 이용해 계산한 후보 |
| 실제 염기 치환 | DNA 시퀀싱 결과에서 확인된 변화 |

예를 들어 `R>H`에서 특정 DNA 치환이 가능하다고 계산되더라도, 그것이 실제 환자에게 발생한 치환이라고 확정할 수 없다.

### 5-5. 단백질 변이에서 추정하기 어려운 정보

| 정보 | 단백질 변이 문자열만으로 확인 가능한가? |
|---|---|
| 원래 아미노산 | 가능 |
| 변경된 아미노산 | 가능 |
| 단백질 위치 | 표기에 포함된 경우 가능 |
| 가능한 코돈 조합 | 유전암호를 이용해 계산 가능 |
| 실제 DNA 코돈 | 일반적으로 불가능 |
| 실제 DNA 염기 치환 | 일반적으로 불가능 |
| SBS96 주변 염기 맥락 | 불가능 |
| 실제 COSMIC Signature 노출도 | 직접 계산 불가능 |

---

## 6. 프로젝트의 Mutation Signature 관련 피처

### 6-1. 실험 목적

본 프로젝트에서는 단백질 변이 문자열에서 DNA 수준의 치환 특성과 관련된 정보를 간접적으로 추출할 수 있는지 검토했다.

핵심 아이디어는 다음과 같다.

```text
단백질 변이 문자열
        │
        ▼
아미노산 치환쌍 추출
        │
        ▼
가능한 코돈 조합 탐색
        │
        ▼
가능한 DNA 염기 치환 유형 계산
        │
        ▼
추정 치환 패턴 피처
```

이 과정은 실제 DNA 변이 데이터를 이용한 Signature 분석이 아니다.

### 6-2. 아미노산 치환쌍 추출

예시:

| 원본 변이 | 치환쌍 |
|---|---|
| R132H | R>H |
| R175H | R>H |
| V600E | V>E |
| G12D | G>D |

이 단계에서는 유전자명과 단백질 위치를 제외하고 아미노산 변화만 표현한다.

단, 실제 프로젝트 구현에서 유전자 또는 위치 정보를 별도로 보존했는지는 코드로 확인해야 한다.

### 6-3. 가능한 코돈 변화 탐색

예를 들어 `E>D` 치환을 살펴보자.

```text
E 코돈: GAA, GAG
D 코돈: GAT, GAC
```

가능한 코돈 조합 중 단일 염기 차이가 있는 후보를 찾을 수 있다.

```text
GAA → GAT : A>T
GAA → GAC : A>C
GAG → GAT : G>T
GAG → GAC : G>C
```

이들은 DNA 암호화 가닥 기준으로 표기한 치환이다.

SBS6 표준화 방식으로 표현하면 다음과 같다.

| 코돈 변화 | DNA 치환 | SBS6 표준화 |
|---|---|---|
| GAA → GAT | A>T | T>A |
| GAA → GAC | A>C | T>G |
| GAG → GAT | G>T | C>A |
| GAG → GAC | G>C | C>G |

따라서 `E>D`라는 단백질 치환은 하나의 SBS6 유형으로만 대응되지 않는다.

**이 예시는 단백질 치환을 실제 DNA 치환으로 확정할 수 없는 이유를 보여준다.**

### 6-4. 추정 치환 패턴 피처

프로젝트에서는 가능한 DNA 치환 유형을 이용해 다음과 같은 피처를 구성하는 접근을 검토할 수 있다.

| 피처 예시 | 의미 |
|---|---|
| inferred_C_A | C>A 가능성 관련 정보 |
| inferred_C_G | C>G 가능성 관련 정보 |
| inferred_C_T | C>T 가능성 관련 정보 |
| inferred_T_A | T>A 가능성 관련 정보 |
| inferred_T_C | T>C 가능성 관련 정보 |
| inferred_T_G | T>G 가능성 관련 정보 |

다만 이 표는 **가능한 피처 설계 예시**다.

실제 `05_mutation_signature.ipynb`에서 사용한 컬럼명이나 계산 방식이 위 표와 동일하다고 가정해서는 안 된다.

특히 다음 구현 방식은 서로 다른 의미를 가진다.

- 가능한 치환 유형마다 1을 부여
- 가능한 치환 유형에 동일한 가중치를 부여
- 참조 코돈 사용 빈도 등을 이용해 가중치를 부여
- 특정 조건에서 후보 치환을 하나만 선택

어떤 방식을 사용했는지는 실제 코드로 확인해야 한다.

### 6-5. 중요한 해석상의 차이

예를 들어 `inferred_C_T = 1`이라는 값이 생성되었다고 하자.

이 값은 다음을 의미할 수 있다.

> 단백질 변이로부터 계산한 가능한 DNA 치환 후보에 C>T가 포함된다.

그러나 다음과 같이 해석하면 안 된다.

> 실제 환자의 DNA에서 C>T 변이가 확인되었다.

두 문장은 과학적으로 서로 다르다.

### 6-6. 관련 노트북

- `notebooks/H_data/05_mutation_signature.ipynb`

실제 사용한 코돈 후보 생성 규칙, SBS6 변환 방식, 가중치 및 결측치 처리 방법은 해당 노트북을 기준으로 확인해야 한다.

---

## 7. 실제 SBS Signature와 프로젝트 피처의 차이

### 7-1. 핵심 비교

| 항목 | 실제 COSMIC SBS Signature | 프로젝트의 추정 피처 |
|---|---|---|
| 입력 | DNA 변이 정보 | 단백질 변이 문자열 |
| 실제 DNA 치환 | 확인됨 | 후보만 추정 가능 |
| 주변 염기서열 | SBS96 분석에 필요 | 제공되지 않음 |
| 기본 분류 | SBS96 등 | 추정 SBS6 관련 정보 |
| 분석 대상 | 돌연변이 과정의 패턴 | 단백질 변이에서 유도한 간접 특징 |
| 특정 원인과의 연관성 | 검증된 참조 Signature와 비교 가능 | 직접적인 원인 추정 불가 |
| 결과 해석 | Mutational Signature 또는 Signature exposure | 추정 염기 치환 패턴 피처 |

### 7-2. Signature Exposure란?

Signature Exposure는 하나의 샘플에서 특정 Mutational Signature가 얼마나 기여했는지를 나타내는 값이다.

예를 들어 한 종양의 실제 SBS96 분포를 여러 참조 Signature의 조합으로 설명할 수 있다.

```text
관측된 SBS96 분포
       │
       ▼
참조 Signature들과 비교
       │
       ▼
각 Signature의 기여도 추정
```

이러한 과정은 단순히 C>T 변이가 몇 개 있는지 세는 것과 다르다.

따라서 프로젝트에서 추정한 SBS6 관련 피처를 `SBS1 exposure`, `SBS4 exposure` 등으로 명명해서는 안 된다.

### 7-3. 왜 SBS6만으로 COSMIC Signature를 구분하기 어려울까?

서로 다른 Signature가 동일한 염기 치환 유형을 많이 포함할 수 있기 때문이다.

예를 들어 SBS1과 SBS2는 모두 C>T 치환과 관련될 수 있지만, 주변 염기서열 맥락과 변이 분포에서 차이가 있다.

SBS6는 이러한 주변 염기 정보를 제거하므로 서로 다른 돌연변이 과정을 구분하는 능력이 제한된다.

더욱이 본 프로젝트에서는 실제 SBS6도 관측한 것이 아니라 단백질 치환으로부터 후보를 추정한다.

따라서 실제 SBS Signature 분석과는 정보 수준의 차이가 더 크다.

### 7-4. 논문과 프로젝트의 관계

Alexandrov et al. (2013, 2020)은 실제 암 유전체의 체세포 변이 데이터를 바탕으로 돌연변이 서명을 연구했다.

반면 본 프로젝트는 단백질 변이 문자열에서 간접적으로 염기 치환 특성을 추정한다.

따라서 이 논문들은 **돌연변이 패턴이 암 연구에서 중요한 이유**를 설명하는 근거가 된다.

하지만 본 프로젝트의 코돈 역추정 피처가 실제 COSMIC Signature를 복원할 수 있다는 근거는 아니다.

---

## 8. 프로젝트 적용 시 주의사항

### 8-1. 실제 관측값과 추정값을 구분한다

가장 중요한 원칙이다.

```text
R132H
  │
  ├── 실제 관측: 단백질 변이 표기
  │
  └── 추정 가능: 일부 DNA 코돈·치환 후보
```

단백질 변이로부터 생성한 값은 원본 DNA 시퀀싱 결과가 아니다.

### 8-2. 단일 염기 치환 여부를 확인한다

일부 아미노산 치환은 하나의 DNA 염기 변화만으로 설명되지 않을 수 있다.

따라서 코돈 후보를 탐색할 때 다음을 확인해야 한다.

1. 원래 아미노산의 가능한 코돈
2. 변경된 아미노산의 가능한 코돈
3. 각 코돈 조합 사이의 염기 차이 수
4. 단일 염기 치환에 해당하는 후보인지

단일 염기 치환으로 설명할 수 없는 경우에는 SBS6 피처로 단순 변환하지 않는 것이 적절하다.

### 8-3. Synonymous 변이 처리

`R895R`과 같은 Synonymous 변이는 아미노산이 바뀌지 않았다는 정보를 나타낸다.

그러나 실제 DNA에서는 염기 변화가 발생했을 수 있다.

따라서 Synonymous 변이를 단순히 DNA 변이가 없는 상태로 처리해서는 안 된다.

또한 아미노산이 동일하다는 사실만으로 정확한 DNA 치환을 복원할 수 없다.

### 8-4. Nonsense 및 Frameshift 변이 처리

`R213*`와 같은 Nonsense 변이는 특정 아미노산 코돈이 종결 코돈으로 바뀌었다는 의미다.

코돈 정보를 이용해 가능한 DNA 변화 후보를 계산할 수 있지만, 실제 치환을 확정할 수는 없다.

반면 Frameshift 변이는 삽입·결실 등에 의해 읽기 틀이 바뀌는 변이이므로 단순한 SBS6 치환으로 처리하는 것은 부적절하다.

### 8-5. 데이터의 관측 범위

본 프로젝트는 유전자별 단백질 변이 정보를 활용한다.

따라서 전체 유전체의 모든 체세포 변이를 관측했다고 가정해서는 안 된다.

실제 Mutational Signature 분석에서는 충분한 변이 수와 적절한 시퀀싱 범위가 중요하다.

관측 범위가 제한되면 변이 패턴을 안정적으로 추정하기 어려울 수 있다.

### 8-6. 피처 명명 권장사항

프로젝트의 추정 피처는 다음과 같이 명명하는 것이 정확하다.

**권장**

- `inferred_sbs6`
- `codon_inferred_substitution`
- `aa_derived_nucleotide_pattern`
- `possible_base_substitution`

**주의가 필요한 명칭**

- `COSMIC_SBS_signature`
- `SBS1_exposure`
- `SBS4_exposure`
- `true_mutational_signature`

실제 DNA 기반 Signature 분석을 수행하지 않았다면 후자의 명칭은 부정확하다.

### 8-7. 프로젝트 관점의 최종 정리

본 프로젝트의 Mutation Signature 관련 접근은 다음과 같이 정리할 수 있다.

> 단백질 변이 문자열에서 아미노산 치환 정보를 추출하고, 유전암호를 이용해 가능한 DNA 염기 치환 유형을 추정하여 추가적인 피처로 활용하는 접근이다.

이 방식은 생물학적 개념을 참고한 피처 엔지니어링이지만, 실제 DNA 기반 COSMIC Mutational Signature 분석과는 구분해야 한다.

---

## 9. 참고 자료 및 출처

### 9-1. 공식 데이터베이스 및 기술 자료

| 번호 | 출처 | 참고한 부분 | 문서 내 활용 위치 |
|---|---|---|---|
| [1] | [COSMIC — Mutational Signatures](https://cancer.sanger.ac.uk/signatures/) | Mutational Signature 개요, SBS·DBS·ID 구분 | 1, 4 |
| [2] | [COSMIC — SBS Signatures](https://cancer.sanger.ac.uk/signatures/sbs/) | SBS 6개 기본 유형 및 SBS96 설명 | 2, 3, 4 |
| [3] | [COSMIC — SBS96](https://cancer.sanger.ac.uk/signatures/sbs/sbs96/) | 96개 변이 범주와 주변 염기서열 맥락 | 3, 7 |
| [4] | [COSMIC — SBS1](https://cancer.sanger.ac.uk/signatures/sbs/sbs1/) | SBS1의 변이 패턴과 제안된 발생 원인 | 4-3 |
| [5] | [COSMIC — SBS2](https://cancer.sanger.ac.uk/signatures/sbs/sbs2/) | APOBEC 관련 변이 패턴 | 4-3 |
| [6] | [NHGRI — Genetic Code](https://www.genome.gov/genetics-glossary/Genetic-Code) | 코돈과 아미노산의 대응 관계 | 5, 6 |
| [7] | [HGVS — Sequence Variant Nomenclature](https://hgvs-nomenclature.org/stable/) | 단백질 변이 표기와 DNA 변이 표기의 구분 | 5, 8 |

### 9-2. 학술 논문

**[8] Alexandrov et al. (2013)**

*Signatures of mutational processes in human cancer*

- 학술지: Nature
- DOI: https://doi.org/10.1038/nature12477
- 참고 내용:
  - 대규모 암 유전체에서 돌연변이 서명 추출
  - 서로 다른 돌연변이 과정의 변이 패턴
  - 암종별 Signature 분포
- 참고 부분:
  - Abstract
  - 본문 Mutational Signatures 분석 결과
- 문서 내 활용: 1-1, 1-3, 4-4, 7-4

**[9] Alexandrov et al. (2020)**

*The repertoire of mutational signatures in human cancer*

- 학술지: Nature
- DOI: https://doi.org/10.1038/s41586-020-1943-3
- 참고 내용:
  - SBS96 기반 Mutational Signature 분석
  - 대규모 암 유전체의 SBS·DBS·ID Signature
  - 암종별 돌연변이 과정과 Signature 분포
- 참고 부분:
  - Mutational signature analysis
  - Single-base substitution signatures
  - Methods
- 문서 내 활용: 3, 4-5, 7-2, 7-4, 8-5

**[10] Bergstrom et al. (2019)**

*SigProfilerMatrixGenerator: a tool for visualizing and exploring patterns of small mutational events*

- 학술지: BMC Genomics
- DOI: https://doi.org/10.1186/s12864-019-6041-2
- 참고 내용:
  - 체세포 변이 유형별 행렬 생성
  - SBS와 주변 염기서열 맥락의 표현
  - 변이 패턴 시각화 및 분석
- 참고 부분:
  - Background
  - Implementation
- 문서 내 활용: 3-2, 3-3, 7-2

### 9-3. 프로젝트 내부 자료

| 자료 | 참고 내용 | 문서 내 활용 위치 |
|---|---|---|
| `notebooks/H_data/05_mutation_signature.ipynb` | 단백질 변이 기반 치환 패턴 추정 실험 | 6, 8 |
| `notebooks/H_data/02_features.ipynb` | 아미노산 치환쌍 관련 피처 | 5, 6 |
| `docs/genomics_research.md` | DNA, 코돈, 아미노산 기초 개념 | 2, 5 |
| `docs/mutation_features.md` | 아미노산 치환쌍 및 변이 기반 피처 | 6, 7 |

---

## 문서 범위 및 해석상 주의

1. 본 문서는 DNA 염기 치환과 Mutational Signature의 기본 개념을 설명한다.
2. COSMIC SBS Signature는 실제 DNA 변이 정보를 바탕으로 연구되는 돌연변이 서명이다.
3. 단백질 변이 문자열만으로 정확한 DNA 치환이나 SBS96을 복원할 수 없다.
4. 프로젝트의 코돈 기반 추정 피처는 실제 COSMIC Signature와 동일하지 않다.
5. 가능한 염기 치환 후보를 실제 관측된 DNA 변이로 해석하지 않는다.
6. 특정 Signature와 암종·환경 노출의 연관성을 확정적인 인과관계로 해석하지 않는다.
7. 프로젝트의 실제 피처 계산 규칙과 성능은 관련 노트북의 실행 결과를 기준으로 확인한다.
