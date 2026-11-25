---
name: clinical-table1
description: 의학연구 tabular 데이터(.xlsx/.csv)에서 baseline characteristics을 비교하는 Table 1을 자동 생성하는 스킬. RCT, prospective/retrospective cohort, case-control, cross-sectional, registry, single-arm 등 연구 디자인을 모두 지원하며 디자인에 따라 p-value 보고 정책(RCT는 CONSORT 2010에 따라 baseline p 숨김)이 자동 분기된다. 연속형은 정규성에 따라 mean±SD(Welch t/ANOVA)와 median[IQR](Mann-Whitney/Kruskal-Wallis)로, 범주형은 n(%)와 chi-square/Fisher's exact/Monte Carlo chi-square로 처리한다. 모든 변수에 대해 SMD(2군은 표준, ≥3군은 max pairwise)를 색 코딩(<0.1 ok / 0.1-0.2 small / ≥0.2 meaningful)으로 표시한다. 출력은 HTML(단일 자기완결, Pretendard 임베딩, 다크모드/인쇄)과 Word(.docx)와 LaTeX(booktabs)을 한 번에 생성한다. 사용자가 "Table 1", "baseline characteristics", "기초통계 표", "환자군 특성 비교", "demographic comparison" 같은 표현을 임상 데이터(.xlsx/.csv)와 함께 언급하면 적극적으로 트리거하라. clinical-eda-report의 Table 1 섹션과 달리 grouping이 필수이며, 출판 가능한 표 형식(Word/LaTeX)을 함께 제공하는 것이 차별점이다. Survival analysis, regression, propensity score matching은 대상이 아니다.
---

# Clinical Table 1 — Baseline Characteristics

의학연구 tabular 데이터(.xlsx/.csv)에서 **publishable Table 1** 한 세트 (HTML + Word + LaTeX)를 한 번에 생성한다. 행은 관찰 단위(환자·내원·병변 등), 열은 변수, 그리고 사용자는 비교 대상이 될 **grouping variable**(예: 배정군, 노출군, case/control)을 지정한다.

## 핵심 차별점

- **연구 디자인별 p-value 정책 자동 분기** — RCT는 CONSORT 2010 (Moher BMJ 2010;340:c869) 및 Senn (Stat Med 1994;13:1715-26) 권고에 따라 baseline p-value 기본 숨김. 관찰연구는 표시하되 multiple testing 경고와 함께.
- **모든 변수에 SMD 표시** (Austin Stat Med 2009;28:3083). 색 코딩: |SMD| < 0.1 (ok), 0.1–0.2 (small), ≥ 0.2 (meaningful) — propensity adjustment 검토 트리거.
- **출판 가능한 3가지 포맷 동시 생성** — HTML (검토용/공유용), Word .docx (논문 본문 복붙), LaTeX (NEJM/JAMA 등 LaTeX 저널 직행).
- **자동 정규성 판정** — |skewness| > 1 또는 사전등록된 known-skewed lab 변수(TG, CRP, BNP, troponin, creatinine, hsCRP, LOS, ferritin 등)는 자동 median[IQR].
- **자동 expected count 체크** — chi-square / Fisher's exact / Monte Carlo chi-square 자동 선택.

## 언제 이 스킬을 쓰는가

- 임상연구 분석의 첫 단계 — 군 간 baseline 비교표 제작
- 논문 Methods/Results의 Table 1 직접 사용
- IRB/PI 보고용 baseline summary
- Multi-center / multi-arm 연구의 군별 특성 점검

가설검정 본분석, 생존분석, Cox/로지스틱 회귀, propensity score matching은 본 스킬의 대상이 아니다. 그쪽은 `survival-analysis`나 다른 분석 도구를 안내하라.

## 핵심 원칙

1. **연구 디자인에 따라 통계 정책이 분기된다** — 사용자가 디자인을 명시하지 않으면 단계 0에서 묻는다.
2. **p-value보다 SMD를 우선** — p-value는 표본크기에 좌우되어 임상 의미를 왜곡할 수 있다. SMD가 진짜 균형의 척도다.
3. **PHI는 출력에 넣지 않는다** — 식별자 컬럼(`patient_id`, `name`, `RRN` 등)은 자동 감지 또는 `--id-cols`로 명시하여 표에서 제외.
4. **이상치는 알아서 처리하지 않는다** — 입력 데이터의 통계를 그대로 보고한다. 이상치 처리는 사전에 `clinical-eda-report`로 점검해야 한다.

## 실행 흐름

### 0. 입력 확인

다음 항목을 사용자 메시지에서 추출하거나, 없으면 한 번에 묻는다.

- **연구 디자인** (필수): `RCT` / `Prospective cohort` / `Retrospective cohort` / `Case-control` / `Cross-sectional` / `Registry` / `Single-arm prospective` / `Other`
- **Grouping variable** (필수): Table 1의 컬럼이 될 군 분류 변수명. 예: `treatment_arm`, `case_control`, `responder`
- 선택사항: `stratified-vars` (RCT의 stratified randomization 변수), `exclude-vars` (outcome 변수 등 분석에서 제외), `non-normal-vars` (강제 median[IQR]), `normal-vars` (강제 mean±SD)

사용자가 명시했으면 그대로 사용. 명시 안 했고 디자인이 명백히 추론 가능하면 (예: "ㅇㅇ RCT 데이터") 그렇게 가정하고 진행. 둘 다 불명이면 `ask_user_input_v0`로 한 번 묻고 끝낸다.

### 1. 스크립트 호출

`scripts/run_table1.py`를 실행한다. 직접 pandas 코드를 새로 짜지 마라.

```bash
python3 scripts/run_table1.py \
  --input <입력 파일 절대경로> \
  --output-dir <출력 폴더 절대경로> \
  --group-var <grouping 변수명> \
  --study-design "<RCT|Prospective cohort|...|Other 자유텍스트>" \
  [--sheet <xlsx 시트명>] \
  [--id-cols patient_id,name,RRN] \
  [--exclude-vars mace,time_to_mace_months,cv_death,recurrent_mi,stroke,hf_hospitalization,all_cause_death] \
  [--stratified-vars site,age_group] \
  [--non-normal-vars TG,CRP] \
  [--normal-vars age] \
  [--group-order GLP-1,Placebo] \
  [--p-value-policy auto|always|never] \
  [--formats html,docx,latex]
```

**기본 정책**:
- `--p-value-policy auto`: RCT면 p-value 숨김, 나머지는 표시
- `--formats`: 기본 모두 (html, docx, latex)
- `--id-cols` 미지정 시 정규식 `(?i)(id|name|rrn|registration|patient|chart|mrn|phone|address|birth)` 매칭 컬럼은 자동 제외

**Outcome 변수 처리** — Table 1은 baseline만 다뤄야 하므로 outcome 변수는 명시적으로 `--exclude-vars`에 넣어야 한다. 사용자가 outcome 컬럼을 잘 모르겠다고 하면, 컬럼명에서 `outcome`, `mace`, `death`, `event`, `time_to_`, `follow`, `_3yr`, `_3y`, `_fu` 같은 키워드를 가진 것들을 추론해 안내하라.

### 2. 결과 확인

스크립트가 정상 종료하면 stdout 마지막 줄에 `OK <html_path> <docx_path> <tex_path>` 형태로 출력한다.

성공 시 사용자에게:
1. HTML 경로 (브라우저로 미리보기)
2. Word 경로 (논문 본문에 직접 붙여넣기)
3. LaTeX 경로 (저널 양식에 import)
4. 간단 요약: N per group, SMD ≥ 0.2 변수 개수, p < 0.05 변수 개수(관찰연구일 때만)

리포트 본문을 채팅에 다시 풀어 쓰지 말 것.

## 통계 정책 (스크립트가 자동 적용)

### 연속형 변수
- **정규성 판정**: `|skewness| > 1` (Bulmer's rule) 또는 known-skewed lab 변수명 매칭 → 비정규로 분류
- **요약 통계**: 정규 → `mean ± SD`, 비정규 → `median [Q1, Q3]`
- **검정**:
  - 2군 정규 → Welch t-test (Student t 대신 — 등분산 가정 회피)
  - 2군 비정규 → Mann-Whitney U
  - ≥3군 정규 → one-way ANOVA
  - ≥3군 비정규 → Kruskal-Wallis
  - v0.1.0은 **post-hoc pairwise comparison 미포함** (Tukey HSD, Dunn 등) — 필요하면 footnote 안내
- **SMD**: 2군에서는 표준 (`(m₁−m₂)/√((s₁²+s₂²)/2)`); ≥3군에서는 max pairwise SMD를 표시

### 범주형 변수
- **요약**: `n (%)`, 분모는 비결측 n
- **검정**: 모든 expected cell ≥ 5 → χ²; 2×2 with small cells → Fisher's exact; r×c with small cells → Monte Carlo χ² (10,000 simulations)
- **SMD**:
  - Binary → `(p₁−p₂)/√((p₁q₁+p₂q₂)/2)`
  - Multi-level → Yang & Dalton (2012) generalized SMD (K-1 dimensional Mahalanobis-like)
- ≥3군 → max pairwise SMD

### 결측 처리
- 변수마다 available-case 분모 사용. "Missing" 컬럼에 결측 n (%) 표시.
- MCAR/MAR/MNAR 진단은 본 스킬의 대상이 아님 (clinical-eda-report 또는 별도 분석 필요).

### Stratified randomization 변수
- `--stratified-vars`로 지정하면 그 변수는 분포만 표시하고 비교 통계 없이 "by design" 표기. 행이 background-highlighted.

## 출력 포맷

### HTML (default)
- Pretendard 폰트 base64 임베딩 (외부 의존 0)
- 다크모드 토글 + localStorage 영속화
- 인쇄/PDF 버튼 (강제 라이트 모드 후 print dialog)
- 색 코딩된 SMD
- 입력 파일 SHA-256 short hash 푸터

### Word (.docx)
- python-docx 사용
- Light Grid 테이블 스타일 (위 굵은 줄 + 아래 일반 줄)
- 색 코딩된 SMD (green/yellow/red)
- 논문 본문 복사 시 그대로 사용 가능한 폰트 크기 (9pt)

### LaTeX
- `booktabs` (toprule, midrule, bottomrule)
- `longtable` (페이지 넘김 자동)
- `xcolor` 로 SMD 색 코딩
- standalone 컴파일 가능 (`pdflatex file.tex`)
- 사용자가 `\begin{longtable}...\end{longtable}` 블록만 자기 논문에 import 가능

## 의존성

- Python 3.9+
- `pandas`, `numpy`, `scipy` (표준)
- `python-docx` (Word 출력용; `pip install python-docx`)
- LaTeX 컴파일은 사용자 측 (`pdflatex` 또는 Overleaf 업로드)

## 자주 발생하는 함정과 대응

**Outcome 변수가 baseline 표에 들어감**: 사용자가 outcome 변수를 `--exclude-vars`에 안 넣었을 때 흔히 발생. 메타데이터 박스에서 "분석 대상 변수 N개" 옆에 의심 변수 (`_3yr`, `time_to_`, `event`, `death`, `mace` 등 매칭)가 보이면 사용자에게 확인 요청.

**ID 컬럼이 표에 unique 개수만 표시되는 변수로 잘못 들어감**: 정규식 자동 감지가 작동하지만, 한국어 컬럼명 (예: "환자번호")은 못 잡으니 `--id-cols`로 명시.

**큰 표본 (n > 10,000)에서 모든 p-value < 0.001**: 정상. p-value의 한계 — SMD를 우선 보라고 footnote에 명시되어 있음. 사용자에게 해석 시 강조.

**Stratified randomization 변수에 p-value가 잡혀서 0.05 미만이 나옴**: `--stratified-vars`로 지정하지 않으면 발생. RCT 사용자에게 stratification 변수가 있었는지 확인할 것.

**범주형에 결측을 별도 level로 보이고 싶다**: 현재 v0.1.0은 available-case (결측은 분모에서 제외). 별도 옵션은 v0.2.0+ 로 계획.

## 한계 — 사용자에게 명시할 것

- **Descriptive only**: 이 표는 가설검정이나 인과추론 결과가 아님.
- **Multiple testing 보정 없음**: 20개 변수면 5% 알파에 1개가 chance로 유의. RCT는 처음부터 p 숨김, 관찰연구는 SMD를 우선시.
- **Post-hoc pairwise 미포함**: ≥3군에서 omnibus 검정이 유의해도 어느 군 쌍이 다른지는 추가 분석 필요.
- **Propensity matching 전후 표 동시 출력은 v0.1.0 미지원** — v0.2.0+ 계획.
- **Time-varying baseline은 지원하지 않음** — baseline = enrollment 시점이라 가정.

위 한계는 HTML 푸터 / Word 푸터 / LaTeX footnote에 자동 포함된다.

## 참고문헌

- Moher D, Hopewell S, Schulz KF, et al. CONSORT 2010 Explanation and Elaboration. *BMJ* 2010;340:c869.
- Senn S. Testing for baseline balance in clinical trials. *Stat Med* 1994;13:1715–1726.
- Austin PC. Using the standardized difference to compare the prevalence of a binary variable. *Stat Med* 2009;28:3083–3107.
- Yang D, Dalton JE. A unified approach to measuring the effect size between two groups using SAS. SAS Global Forum 2012, Paper 335-2012.
