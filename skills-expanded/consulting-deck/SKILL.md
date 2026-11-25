---
name: consulting-deck
description: "Use when the user wants a consulting-style presentation deck as single-file HTML — 컨설팅 덱, 전략 보고 자료, 경영진 보고, 이사회 자료, 제안서, 입찰 제안서, 피치덱, IR 덱, 사업 계획 발표자료, 전략 수립 보고, 진단 보고서, IT 전략/비용 최적화 보고 (예: \"IT 비용 최적화 전략 12장짜리 경영진 보고 덱으로 만들어줘\", \"AI 전환 전략 제안서\", \"이사회 보고 자료 만들어\"). 듣는 사람이 배우는 교육 자료는 이 스킬이 아니라 edu-deck 스킬로 간다. 산출물은 1920×1080 단계 공개 HTML 한 파일(PPTX 생성·변환은 하지 않는다)."
---

# consulting-deck: 주제 → 근거 → 주장 → 권고 (컨설팅 덱 전용)

의사결정자를 설득해 결정과 실행을 이끄는 단일 HTML 덱을 만든다. 교육 덱(edu-deck)이 학습을 지원한다면 이 덱은 **의사결정과 실행**을 지원한다 — 결론이 앞서고, 모든 수치에 근거가 따르고, 권고로 닫는다.

결과물은 파일 하나다. 발표 셸·모션 엔진·빌드·검사는 edu-deck과 같은 것을 쓴다(`<base>` = 이 스킬과 같이 설치된 `edu-deck` 스킬의 `shared/` 폴더). 외부 글꼴·이미지·스크립트 없이 어디서나 열린다. 키보드로 넘기고(→ 한 단계씩), N 발표자 노트, F 전체 화면, P 인쇄 자료. 확인 문제·자습 모드 같은 학습 장치는 교육 전용이라 기본적으로 쓰지 않는다.

## 진입 판별 (edu-deck과의 경계)

- **이 스킬**: 듣는 사람이 무언가를 **결정하거나 승인하도록** 만드는 덱 — 전략·진단·제안·심사·권고·보고. "제안서, 전략 수립, 경영진 보고, 이사회 자료, 피치/IR" 신호.
- **edu-deck**: 듣는 사람이 무언가를 **배우도록** 만드는 덱 — 교육·훈련·매뉴얼·워크숍. edu-deck 스킬의 "대상 밖" 안내를 받으면 이 스킬로 온다.
- 둘 다 섞였거나 애매하면 한 번만 묻는다: "이 자료는 결정을 받는 용도인가요, 배우는 용도인가요?" 답이 없으면 요청 문구의 목적 동사(보고·제안·승인 vs 교육·연수)로 정하고 보고에 근거를 남긴다.
- 한 장짜리 설명 페이지·보도자료·포스터는 이 스킬이 아니다. PPTX 파일 요청은 거절하고 단일 HTML 대안을 제안한다.

## 저작 형태 — 요청 정리 때 한 번 정한다

| 형태 | 언제 | 스토리라인 |
|---|---|---|
| **문제해결형** | 결정이 걸린 과제 — 진입 여부, 투자 심사, 전환 승인 | 문제 정의 → 이슈 트리 → 가설 → 근거 → 권고. `references/storyline.md` 전체 절차 |
| **자료종합형** | 자료를 충실하게 종합해 보여주는 과제 — 시장 동향 브리핑, 연간 리뷰 | 요약 중심 서사(What–So what–Now what). **가설 트리를 강요하지 않는다** |

형태는 brief에 한 줄로 남긴다(`형태: 문제해결형 (근거: …)`). 혼합이면 장 그룹마다 어느 형태인지 표시한다.

## 기본값 (사용자가 따로 말하지 않으면)

| 항목 | 기본값 |
|---|---|
| 청중 | 의사결정자(경영진·이사회·사업부장) |
| 분량 | 요청에 따름. 없으면 10~15장(과제 §8 데모 참고) |
| 밀도 | 발표 겸 읽기(Reading-first 기본, 발표자가 있으면 Speaker-led — `references/consulting-design.md`) |
| 작업 폴더 | `${EDU_DECK_OUTPUT_DIR:-./outputs}/consulting-deck/<YYYYMMDD>-<영문-slug>/` |
| 결과 파일 | `<작업 폴더>/<주제>-컨설팅덱.html` |
| 중간 확인 | 없음(구성안 승인을 원하면 사용자가 말한다) |

## 작업 순서

### 1. 요청 정리 → brief.md
- **의사결정 질문 1개**를 문장으로 못 박는다("시장을 분석해라" → "X 세그먼트 진입 여부와 조건은"). 결정 주체·기한·범위 내외·성공 기준·제약을 적는다.
- 저작 형태(위 표)를 정한다. 청중·발표 상황(회의실 발표인지 혼자 읽는 보고인지)을 적는다.
- 조직 고유 정보가 꼭 필요하면 한 번에 묶어 한 번만 묻고, 답이 없으면 가정을 brief에 남긴다.

### 2. 근거 조사 → research.md + evidence.json
- 근거 원장 `evidence.json`을 작업 폴더에 만들고 조사와 함께 채운다 — 출처(source)와 주장(claim)을 ID로 연결하고, 원본 값·계산 방법·가정/사실 구분을 남긴다. 형식과 규칙: `references/evidence.md`.
- 공개 자료를 쓸 때의 인용·복제 경계: `references/reference-sources.md`.
- 확인 안 된 수치는 화면에 못 쓴다. 대안은 두 가지다 — 검증된 공개 자료를 찾거나, **가상 데이터로 만들고 표기한다**.

### 3. 스토리라인 → storyline.md
- 통치 사상(전체 주장 한 문장) → 서사 뼈대 → 장별 주장형 제목 표를 짠다. 절차·테스트: `references/storyline.md`.
- 통과 조건: **제목만 순서대로 읽으면 짧은 경영 메모처럼 읽힌다.** Exec Summary는 본문이 다 정해진 뒤 마지막에 쓴다(본문과 불일치 금지).

### 4. 차트 모델 → charts/*.json → src 조각 생성
- 화면에 들어가는 **모든 분석 차트는 chart_gen.mjs로 만든다** — 수치를 조각 HTML에 직접 타이핑하지 않는다. 질문→차트 선택과 5층 구조: `references/analytical-charts.md`, 문법 원본: `charts/schema.md`.
```bash
node <이 스킬>/charts/chart_gen.mjs --in <작업 폴더>/charts/NN-이름.json -o <작업 폴더>/src/NN-이름.html
```
- 데이터 계산·합계·출처·가상 표기는 모델이 검증한다(expectTotal·source·synthetic). 재생성 검사: `python3 <이 스킬>/charts/regen.py --check <작업 폴더>`.

### 5. 슬라이드 저작 → src/
- 장마다 역할(정의/주장/증명/비교/결정/동원)에 맞는 배치를 고른다 — 카탈로그: `references/consulting-layouts.md`(고정 템플릿이 아니라 목적별 후보다).
- 재료 사용 4방식(그대로·변형·조합·새로 설계)과 저작 권한은 `<base>/references/authoring.md`가 그대로 적용된다. 조각·아키타입·도식 문법은 `<base>/references/`를, 컨설팅 특화 배치·톤은 `references/consulting-design.md`를 따른다.
- 컨설팅 덱은 **팩 경로를 쓰지 않는다**. `deck.json`에 `title`·`output`만 쓰고 `src/`를 직접 저작한다. 테마는 덱 로컬 `src/*.css`(consult.css 계열 — `consulting-deck/assets/consult.css`를 복사해 쓴다)로 준다. IT 아키텍처·전환 장은 Architecture Kit(`<base>/references/architecture.md`)을 그대로 결합할 수 있다.
- 노트는 장마다 실제 발표 근거로 쓴다(자동 진행 금지). 계약(`data-step/add/only/lit/until`·`.chk`·`aside.notes`)은 교육 덱과 동일하게 보호한다.

### 6. 조립·검사·심미 리뷰
```bash
python3 <base>/scripts/build_deck.py <작업 폴더>
python3 <base>/scripts/check_deck.py <작업 폴더>/<결과 파일> --sheets <작업 폴더>/qa --json <작업 폴더>/qa/check.json
python3 <이 스킬>/checks/check_consulting.py <작업 폴더>     # 컨설팅 게이트(논리·데이터·근거 대조)
python3 <base>/scripts/capture_deck.py <작업 폴더>/<결과 파일> <작업 폴더>/qa/shots   # 전 장 최종 상태 캡처(공용 도구)
```
- 게이트의 기준·자동 검사와 사람 승인의 구분: `references/quality-gates.md`.
- 1920×1080 캡처를 직접 본다(표지·핵심 장·차트 장). 모션은 단계·재방문·인쇄·reduced-motion을 확인한다.
- **심미 리뷰(의무)**: 자동 검사 통과는 심미 품질의 증거가 아니다. 완성 덱은 반드시
  공통 크리틱 계약 `<base>/references/design-critique.md`(6단계 절차·9항목·Blocker/Major/Minor)로
  독립 검수를 통과한다 — 저작 에이전트가 아니라 **시각 판단 기능이 있는 에이전트**(이 환경:
  agy/gemini-4-argon)가 캡처를 보고 진단한다. 컨설팅 특화(펌 대비·방향 시안 3안)는
  `references/design-review.md`. Blocker→Major 순으로 반영하고 재평가 받는다.
  자기 결과물 자체 평가로 갈음하지 않는다.

### 7. 보고
- 결과 경로·장 수·형태·청중·서사 뼈대 한 줄. 사용한 출처 수와 가상 데이터 항목.
- 검사 결과(check_deck·check_consulting·regen --check RESULT 줄). 못 한 검사는 이유와 함께.
- **자동 검사 통과와 컨설팅 품질 승인은 별개로 보고한다.** 품질 게이트(논리·데이터·시각·실행)의 사람 판단 항목은 직접 보고한다.
- 확인 필요 목록: 가정한 조직 정보·기준일이 지난 수치·가상 데이터 위치.

## 빌드 경로 (파일 구조)

```
<작업 폴더>/
  deck.json            # title·output (+ theme 있으면 legacy 테마와 병합)
  brief.md  research.md  storyline.md  evidence.json
  charts/NN-*.json     # 차트 선언 모델(원본 데이터·계산·출처)
  src/NN-이름.html      # 장 조각(차트 장은 chart_gen이 굽는다)
  src/consult.css      # 덱 로컬 테마(assets/consult.css 계열 복사·변형)
  qa/                  # 검사 결과·캡처
```

## 반드시 지킬 것

- 근거 없는 수치·인용을 화면에 쓰지 않는다. 근거를 못 찾으면 가상 데이터로 만들고 표기한다(evidence.md).
- 장 제목은 주장이다. 토픽 명사형 제목으로 끝내지 않는다.
- 차트 수치는 charts 모델에만 산다 — 슬라이드 조각·제목·Exec Summary의 수치가 모델과 일치해야 한다(check_consulting이 대조한다).
- 가정·추정·전망을 실적·사실처럼 쓰지 않는다. 화면에 구분 표기를 남긴다.
- 펌 보고서의 문장·레이아웃·로고·차트를 복제하지 않는다(reference-sources.md). 배운 패턴은 우리 문법으로 재작성한다.
- 검사를 통과시키려고 검사 스크립트·기준을 고치지 않는다. 고칠 것은 슬라이드와 모델이다.
- 공유 자산(`edu-deck/shared/`)은 수정하지 않는다. 컨설팅 전용 도구는 이 스킬 폴더 안에 둔다.

## 파일 안내

| 파일 | 언제 읽나 |
|---|---|
| `references/storyline.md` | 3단계: 저작 형태 분기·문제 정의·이슈 트리·통치 사상·서사 뼈대·주장형 제목·Exec Summary |
| `<base>/references/design-critique.md` | 6단계: 공통 심미 크리틱 — 6단계 절차·9항목·Blocker/Major/Minor·캡처 도구·크리틱 에이전트 호출 |
| `references/design-review.md` | 6단계: 컨설팅 특화 심미 리뷰 — 펌 대비 언어화·방향 시안 3안 비교·재평가 |
| `references/evidence.md` | 2·4단계: evidence.json 원장·증거 유형·가정/사실 구분·가상 데이터 표기·계산 검증 |
| `references/consulting-layouts.md` | 5단계: 19 유형 배치 카탈로그(목적·수용량·만드는 법)와 선택 규칙 |
| `references/analytical-charts.md` | 4단계: 질문 기반 차트 선택·5층 구조·주석·색·출처 블록·모션 |
| `references/consulting-design.md` | 5단계: 4가지 시각 방향·타이포·밀도(Speaker-led/Reading-first)·펌 패턴의 번역·consult.css |
| `references/quality-gates.md` | 6·7단계: 논리·데이터·시각·실행 게이트 — 자동 검사와 품질 승인의 구분 |
| `references/reference-sources.md` | 2단계 및 인용 시: 오픈소스 이식 내역·펌 분석 근거·차단 기록·복제 경계 |
| `charts/schema.md` | 4단계: 차트 모델 문법의 원본(타입별 데이터 계약·검증 규칙) |
| `<base>/references/authoring.md` | 저작 권한·재료 4방식·검사와 품질의 구분 — 교육 덱과 동일 적용 |
| `<base>/references/design.md`·`DESIGN_TOKENS.md`·`MOTION_LIBRARY.md` | 5단계: 공통 판단 기준·토큰·모션(컨설팅 문서는 이 위에 특화만 얹는다) |
| `<base>/references/architecture.md` | 기술 아키텍처·전환 장 결합 시(Architecture Kit) |

개념 출처: 이 스킬의 서사·차트·게이트 체계는 zairuilab/consulting-deck(Apache-2.0, d25dd54)과 McKinsey Vizro(Apache-2.0, 146b932)의 개념을 한국어로 재작성한 것이다. 내역: `references/reference-sources.md`.
