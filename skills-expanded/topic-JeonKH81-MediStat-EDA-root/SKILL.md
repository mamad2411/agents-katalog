---
name: clinical-eda-report
description: 의학연구 tabular 데이터(.xlsx/.csv)에 대해 한국어 단일 HTML EDA 리포트를 자동 생성하는 스킬. 행이 관찰 단위(환자·내원·병변·검체 등), 열이 변수인 모든 의학연구 데이터셋이 대상이며 연구 디자인(후향/전향 코호트, RCT·임상시험, case-control, cross-sectional, registry, survey 등)을 가리지 않는다. n·변수 타입별 요약, 결측 패턴, 분포 플롯, 이상치(implausible value) 감지, 선택적 소그룹별 Table 1, 상관관계 heatmap, VIF를 모두 한 파일에 임베딩한다. 사용자가 임상연구·관찰연구·임상시험·환자 데이터·registry·연구 데이터셋·엑셀/CSV 파일을 업로드하면서 "EDA", "데이터 탐색", "탐색적 분석", "기초통계", "Table 1", "결측 보고", "분포 확인", "데이터 살펴봐", "데이터 점검" 같은 표현을 사용하면 적극적으로 트리거하라. 단순 통계 분석(t-test, Cox regression 등)이나 가설 검정 요청, 시각화 1개만 요청한 경우는 대상이 아니다. raw 영상(DICOM/JPEG)·ECG waveform·자연어 free text·omics 매트릭스 같은 비-tabular 데이터는 대상이 아니다. clinical-research-harness:data-inspect와 달리 사전등록·검정력 평가 없이 독립적으로 동작한다.
---

# Clinical EDA Report

의학연구 tabular 데이터(행 = 관찰 단위, 열 = 변수)를 받아, **단일 한국어 HTML 대시보드 리포트**를 생성한다. 연구 디자인(후향/전향 코호트, RCT·임상시험, case-control, cross-sectional, registry 등)이나 관찰 단위(환자·내원·병변·검체 등)에 구애받지 않으며, 행 단위가 무엇인지는 리포트 상단에 함께 명시한다. 결과 리포트는 다음 기능을 갖춘 단일 HTML 파일이다:

- **상단 KPI 카드 6장** — 관찰 수, 변수 수, 전체 결측률, 고결측 변수 수, 이상치 후보 수, VIF≥10 변수 수. 각 카드를 클릭하면 해당 섹션으로 부드럽게 스크롤된다
- **좌측 sticky 사이드바** + **scrollspy** — 현재 보이는 섹션이 자동으로 highlight
- **인터랙티브 SVG 분포 플롯** — 막대 위에 마우스를 올리면 구간/빈도/% 툴팁 표시. Vector 출력이라 확대·인쇄·다크모드 모두 깔끔
- **다크모드 토글** — 헤더 우상단 버튼. `prefers-color-scheme` 자동 감지 + `localStorage` 영속화 (실패 시 graceful fallback)
- **인쇄·PDF 버튼** — 사이드바/컨트롤 자동 숨김, 강제 라이트 모드, 패널 단위 page-break 컨트롤
- **입력 파일의 SHA-256 short hash(12자)** 푸터에 표시 — 같은 파일로 만든 두 리포트의 동일성 검증용

모든 그래프, 폰트, 차트, JS는 base64/인라인으로 임베딩되므로 받는 사람은 파일 하나만 열면 된다 (외부 의존 0).

## 언제 이 스킬을 쓰는가

- 새로 받은 연구 데이터셋(.xlsx/.csv)의 전반적 상태를 빠르게 파악하고 싶을 때 — 후향/전향 코호트, RCT·임상시험, case-control, cross-sectional, registry, survey 등 디자인 무관
- IRB 제출 전·연구계획서 작성 전에 baseline characteristics와 결측 현황을 점검할 때
- 협력기관에서 받은 데이터셋의 품질(이상치, 결측, 코딩 오류)을 검수할 때
- 임상시험 database lock 후·sub-study 시작 전 데이터셋 sanity check

가설검정·생존분석 같은 inferential analysis는 이 스킬의 대상이 아니다. 그쪽은 `survival-analysis` 또는 `clinical-research-harness:stat-analysis`를 안내하라.

**대상이 아닌 데이터**: raw 영상(DICOM, JPEG/PNG 등 이미지 자체), ECG/PPG waveform 시그널, 자연어 임상 기록 free text, 고차원 omics(genome/transcriptome) 매트릭스는 별도 도구가 필요하다. Long-format longitudinal 데이터(환자당 여러 행)는 동작은 하지만 분포·요약통계가 "환자"가 아닌 "관찰 단위(행)" 기준임을 사용자가 인지해야 한다 — 리포트 상단에 행 단위를 명시하므로 해석 시 반드시 확인할 것.

## 핵심 원칙

1. **PHI는 출력에 넣지 않는다.** 환자 ID·이름·주민번호·생년월일 같은 식별자가 열에 있으면 리포트에서는 열 이름만 표시하고 값은 마스킹한다 (요약통계의 unique count만 표기). 환자 단위 raw row는 절대 HTML에 박지 않는다.
2. **근거를 명시한다.** 모든 수치는 어떤 데이터에서 어떤 방법으로 계산했는지 (n, 분모, 통계량 정의) 함께 적는다.
3. **이상치는 자동 탐지하되 자동 수정하지 않는다.** "임상적으로 말이 안 되는 값" 후보만 표 형태로 보고하고, 어떻게 처리할지는 사용자가 결정한다.

## 실행 흐름

다음 순서로 진행한다. 디자인 확인(단계 0) 이후로는 사용자 확인을 받지 말고 한 번에 끝내라 — 사용자는 최종 HTML만 받아보고 싶다.

### 0. 연구 디자인 확인

스킬이 트리거되면 가장 먼저 **연구 디자인**을 확인한다. 디자인은 (1) 리포트 메타데이터로 명시되어 받는 사람의 잘못된 해석을 방지하고, (2) §6 Table 1 해석 가이드(특히 baseline p-value 보고 관례)를 분기시킨다. 이 단계만이 사용자에게 묻는 유일한 단계다.

- 사용자 메시지에 디자인이 명확히 명시되어 있으면(예: "retrospective cohort 데이터입니다", "RCT 결과", "case-control 자료") **그대로 사용**하고 추가 질문 없이 다음 단계로 진행한다.
- 명시가 없으면 `ask_user_input_v0`로 **딱 한 번** 묻는다. 단일 선택 옵션:
  - `RCT` (randomized clinical trial / 임상시험)
  - `Prospective cohort` (전향적 코호트)
  - `Retrospective cohort` (후향적 코호트)
  - `Case-control` (환자-대조군)
  - `Cross-sectional` (단면 연구)
  - `Registry` (등록·관찰 데이터베이스)
  - `Single-arm prospective` (단일군)
  - `Other / Unsure` (기타·확실치 않음)

답을 받으면 그 값을 `--study-design` 인자로 다음 단계 스크립트에 전달한다. "Other / Unsure"가 선택되면 빈 문자열 또는 사용자 자유 입력을 그대로 전달한다 (스크립트가 "(unspecified)"로 처리).

### 1. 입력 파악

사용자가 업로드한 파일 경로를 확인한다. .xlsx면 시트가 여러 개일 수 있으므로 첫 시트(또는 명시된 시트)를 기본으로 쓰되, 시트 목록은 리포트 상단에 함께 보고한다. .csv는 인코딩 감지(utf-8 → cp949 → euc-kr 순으로 시도)를 한다.

선택적 입력으로 **grouping_var**(소그룹별 Table 1을 만들 변수명, 예: `treatment_arm`, `MACE_30day`)이 명시되었는지 확인한다. 없으면 Table 1 섹션은 생략하고 그 사실을 리포트에 명시한다.

### 2. 스크립트 호출

`scripts/run_eda.py`를 실행한다. 이 스크립트가 데이터 로딩 → 분석 → 그래프 → HTML 조립까지 모두 처리한다. Claude가 직접 pandas 코드를 새로 짜지 마라. 이미 잘 다듬어 둔 스크립트가 있고 매번 새로 만들면 일관성이 깨진다.

```bash
python3 scripts/run_eda.py \
  --input <입력 파일 절대경로> \
  --output <출력 .html 절대경로> \
  [--study-design "<RCT|Prospective cohort|Retrospective cohort|Case-control|Cross-sectional|Registry|Single-arm prospective|기타 자유텍스트>"] \
  [--sheet <시트명>] \
  [--grouping-var <열 이름>] \
  [--id-cols <쉼표 구분, 예: patient_id,name,RRN>] \
  [--force-categorical <쉼표 구분, 분류 오류 보정용>] \
  [--force-numeric <쉼표 구분, 분류 오류 보정용>]
```

필요한 패키지(pandas, numpy, matplotlib, scipy)는 표준 설치되어 있다. 한글 폰트는 스크립트가 자동 fallback 처리한다.

## 변수 타입 자동 분류 (v0.2.0+)

`is_numeric_dtype()`만 보고 무조건 numeric으로 분류하면 0/1로 코딩된 binary 변수(HTN, DM, MACE 등)나 1-12로 코딩된 site 번호가 연속형으로 잡혀 분포 플롯·이상치·상관관계가 무의미해진다. 다음 순서의 휴리스틱을 적용한다:

1. **All missing** → `allmissing` 그룹
2. **Object dtype + 70% 이상 datetime 파싱 가능** → `datetime` (자동 변환)
3. **Numeric dtype + nunique ≤ 2** → `categorical` (binary; HTN/DM/MACE 0/1 등)
4. **Numeric dtype + 모든 값이 정수 + nunique ≤ 15** → `categorical` (NYHA 1-4, Killip 1-4, site 1-12 등)
5. **Numeric dtype + 변수명이 의료 categorical 패턴 매칭** → `categorical` (안전망)
   - 매칭 정규식 (대소문자 무관): `htn`, `hypertens`, `dm`, `diabet`, `dyslip`, `ckd`, `chf`, `hf`, `cad`, `ihd`, `mi`, `stemi`, `nstemi`, `stroke`, `tia`, `cva`, `af`, `afib`, `pad`, `pvd`, `copd`, `asthma`, `cancer`, `malign`, `hcv`, `hbv`, `hiv`, `tb`, `smok`, `male`, `female`, `sex`, `alive`, `dead`, `death`, `mortality`, `event`, `outcome`, `yes`, `no`, `yn`, `present`, `absent`, `site`, `center`, `centre`, `hospital`, `institution`, `clinic`, `nyha`, `killip`, `ccs`, `ecog`, `kps`, `asa`, `child`, `childpugh`, `grade`, `stage`, `class`, `severity`, `type`, `category`, `group`, `arm`, `treatment`, `cohort`
6. **그 외 numeric** → `numeric` (연속형)
7. **Object dtype + low cardinality** → `categorical` (자연어 라벨)
8. **Object dtype + high cardinality** → `text`

**사용자 강제 override**: `--force-categorical var1,var2` / `--force-numeric var3,var4` 로 휴리스틱을 무시하고 강제 분류 가능. 예: `lab_count`처럼 정수값이지만 진짜 count 데이터인 경우 `--force-numeric lab_count`.

### 3. 결과 확인

스크립트가 종료되면 stdout 마지막 줄에 `OK <html_path>` 또는 `FAIL <reason>`을 출력한다. 실패하면 reason을 사용자에게 그대로 전달하고 어떤 정보가 부족한지(예: 헤더가 2행 구조, 시트가 비어있음) 짚어준다.

성공하면 사용자에게 `computer://` 링크 한 줄과 간단한 요약(n, 변수 수, 결측 심한 변수 top 3, 이상치 후보 개수)만 전달하라. 리포트 본문을 채팅에 다시 풀어 쓰지 마라 — 사용자는 HTML을 보기 위해 이 스킬을 쓴 것이다.

## 리포트 구조 (스크립트가 자동 생성)

리포트는 다음 구성을 갖춘 단일 HTML 대시보드다 — 헤더 + KPI strip + 좌측 사이드바 + 메인 패널 + 푸터. 각 패널은 카드 형태로, 좌측 네비게이션은 sticky이며 scrollspy로 현재 보이는 섹션이 자동 highlight된다.

**상단 KPI strip (6장)** — 데이터 품질 한눈 보기:
1. 관찰 단위(n) — neutral
2. 변수 수 + 타입별 breakdown — neutral
3. 전체 결측률 — ≥10%면 warning, ≥30%면 danger
4. 고결측 변수 수(≥30%) — >0이면 warning
5. 이상치 후보 변수 수 — >0이면 warning
6. VIF≥10 변수 수 — >0이면 danger

**좌측 사이드바** — 7개 섹션 네비게이션. **메인 영역** — 다음 7개 섹션이 같은 순서로 카드(패널) 형태로 만들어진다. 일관성이 신뢰를 만든다.

1. **데이터셋 개요** — 파일명, 시트, n_rows, n_cols, 변수 타입별 개수 (numeric/categorical/datetime/text), **연구 디자인**(단계 0에서 확인), 분석 일시
2. **변수별 요약통계** — numeric: n, missing(%), mean±SD, median[IQR], min, max | categorical: n, missing(%), unique, top 3 levels with frequency
3. **결측 패턴** — 변수별 결측률 막대그래프 + missingness heatmap(행 50개 이상이면 무작위 50행 샘플) + 결측 ≥30% 변수 경고 박스
4. **분포 플롯** — numeric: 히스토그램 + KDE | categorical: 빈도 bar chart (level이 20개 이상이면 top 20만 + "기타" 막대)
5. **이상치 / Implausible value 후보** — 자동 규칙(IQR×3 바깥, 음수가 말이 안 되는 변수의 음수, 0이 말이 안 되는 lab value의 0, age>120, 날짜 미래)에 걸린 행 개수와 예시 값(마스킹된)
6. **소그룹별 Table 1** — grouping_var이 있을 때만. 그룹별 n, baseline characteristic mean±SD/median[IQR]/n(%) + t-test/Mann-Whitney/chi-sq p-value (군 수가 3 이상이면 ANOVA/Kruskal-Wallis). **해석 가이드는 연구 디자인에 따라 분기**한다:
   - **RCT**의 경우, CONSORT 2010 권고에 따라 baseline p-value 보고는 일반적으로 권장되지 않음을 명시한다 (Moher D, et al. *BMJ* 2010;340:c869; Senn S, *Stat Med* 1994;13:1715–26).
   - **관찰연구**(cohort, case-control, cross-sectional, registry)의 경우, baseline 비교는 confounding 검토에 유용하나 unadjusted p-value의 한계와 함께 SMD(<0.1 권장) 같은 보조 지표 사용을 안내한다 (Austin PC, *Stat Med* 2009;28:3083–3107).
   - 디자인이 "기타/확실치 않음"이면 일반 unadjusted 경고만 표시한다.
7. **상관관계 및 다중공선성** — numeric 변수 간 Spearman correlation heatmap + VIF 테이블(변수가 2개 이상 numeric일 때). VIF≥10 변수는 경고 색으로 표시.

각 섹션 끝에는 **해석 가이드** 박스(1-2문장)를 넣어 "이 결과를 어떻게 읽어야 하는지" 알려준다.

## 출력 위치

기본 출력 경로는 `<input과 같은 폴더>/<입력파일명>_EDA_report.html`이다. 사용자가 다른 경로를 지정하면 그대로 따른다. Cowork mode에서는 outputs 폴더에 저장하고 `computer://` 링크로 제공한다.

## 자주 발생하는 함정과 대응

**폰트 (한글 + 영문 일관 가독성)**: 스킬은 `assets/fonts/`에 **Pretendard**(SIL OFL 1.1) 9개 weight를 번들로 포함한다. 스크립트는 (1) matplotlib에 Pretendard를 등록해 그래프 라벨에 사용하고, (2) Regular(400)/Bold(700) 두 weight를 base64로 `@font-face`에 임베딩해 HTML 본문에 사용한다. 따라서 받는 사람이 폰트를 설치하지 않아도 보는 화면이 같다 (HTML 용량은 ~6.5MB 증가). 폰트 폴더가 없거나 손상되었으면 기존 시스템 한글 폰트(AppleGothic/NanumGothic/Malgun Gothic 등) → 영문 fallback 순으로 동작한다. 라이선스 고지는 `assets/fonts/LICENSE_PRETENDARD.md`에 있다.

**거대 데이터**: row가 100만 이상이면 결측 heatmap·분포 플롯은 무작위 100k 샘플로 그린다 (요약통계는 전체 사용). 이 사실을 리포트 상단 메모로 표기한다.

**모든 값이 결측인 열**: 그래프에서 제외하고 "전열 결측" 표에 따로 모은다.

**날짜형 변수**: ISO 포맷 추정 + pd.to_datetime errors='coerce'. 변환 실패율이 30%↑이면 텍스트로 취급한다.

**식별자 자동 감지**: 열 이름이 정규식 `(?i)(id|name|rrn|registration|patient|chart|mrn|phone|address|birth)`에 매칭되면 ID 후보로 자동 분류하고 값 마스킹. 사용자가 `--id-cols`로 명시하면 그것을 우선 사용.

## 한계 — 사용자에게 명시할 것

- 이 리포트는 **descriptive only**다. 인과 추론·가설 검정 결과가 아니다.
- Table 1의 p-value는 unadjusted이며 multiple comparison correction 없음 — 그대로 논문 Table 1에 옮기지 말고 분석 단계에서 재계산할 것.
- 이상치 후보는 자동 규칙 기반이므로 false positive가 있을 수 있다. 임상적 판단으로 최종 결정해야 한다.
- 결측 패턴 해석(MCAR/MAR/MNAR)은 본 리포트에서 다루지 않는다.

위 한계는 스크립트가 리포트 맨 아래 **Limitations** 박스에 자동 포함한다.
