---
name: auto-project-builder
description: 인터랙티브 설정(플랫폼·기술스택·서비스 유형·개수)을 거쳐 트렌드 조사·경쟁 분석·아이디어 평가를 자율 수행하고, 자동 QA 루프로 실제 동작하는 프로젝트를 완성까지 구현하는 완전 자동화 스킬. 체크포인트 재개, 완료 알림, 날짜별 리포트, overview.html 포함.
triggers:
  - auto-project-builder
  - 자율 프로젝트
  - 아이디어 자동 구현
  - autonomous build
  - 서비스 자동 생성
---

## 핵심 원칙

> **사람의 개입 없이 실제로 동작하는 프로젝트를 완성한다.**
> 빌드 오류, 타입 오류, 린트 오류가 남은 프로젝트는 "완성"이 아니다.
> 사람은 완성된 결과물만 받는다.

> **⚠️ 모든 프로젝트는 반드시 `projects/` 디렉토리 안에서 구현한다. (절대 예외 없음)**
> PRD, ROADMAP, 소스 코드, README 등 프로젝트 관련 모든 파일은 `projects/{slug}/` 경로에 위치해야 한다.
> `projects/` 바깥에 소스 코드를 생성하거나 수정하는 것은 금지된다.

---

## 컨텍스트 관리 원칙 (Context Budget)

> **메인 컨텍스트는 오케스트레이션 정보만 보유한다.**
> 소스 코드, QA 로그, 에이전트 전체 응답은 메인 컨텍스트에 축적하지 않는다.

### 4대 규칙

**규칙 1 — 프로젝트별 Agent 격리 (가장 중요)**
Phase 2의 각 프로젝트는 **독립 Agent 호출** 안에서 실행한다.
프로젝트 코드, QA 오류, 에이전트 상세 응답이 메인 컨텍스트에 쌓이지 않는다.
Agent는 완료 후 **JSON 요약만** 메인 컨텍스트에 반환한다:

```json
{
  "slug": "프로젝트-슬러그",
  "status": "done | skip",
  "qa_attempts": 1,
  "github_url": "https://github.com/...",
  "errors_fixed": ["오류 1줄 요약"],
  "skipped_reason": null
}
```

**규칙 2 — 소스 코드를 메인 컨텍스트에 읽지 않는다**
코드 파일은 에이전트가 직접 접근한다. 메인 루프에서 `Read(src/...)` 금지.

**규칙 3 — 파일 기반 상태 저장**
아이디어 목록, PRD, QA 결과 등 모든 중간 상태를 즉시 파일로 저장한다.
메인 루프는 **파일 경로와 JSON 요약**만 추적한다.

**규칙 4 — 컴팩션 체크포인트**
프로젝트 3개 완료마다, 또는 메인 컨텍스트가 길어졌다고 판단되면:
1. 체크포인트 파일 저장 (`2-8` 형식)
2. `/compact` 실행
3. 체크포인트에서 상태 복원 후 이어서 진행

---

## 한국어 UI 원칙 (모든 플랫폼 공통 — 절대 예외 없음)

> **모든 사용자 대면 텍스트는 한국어로 작성한다.**
> 영어로 작성된 UI는 완성으로 인정하지 않는다.

적용 범위:
- 버튼 레이블 ("저장", "삭제", "확인", "취소")
- 네비게이션 메뉴 ("대시보드", "설정", "내 정보")
- 폼 레이블 및 플레이스홀더 ("이메일을 입력하세요")
- 에러/성공 메시지 ("저장되었습니다", "필수 항목입니다")
- 빈 상태 메시지 ("데이터가 없습니다", "아직 항목이 없어요")
- 페이지 제목, 섹션 헤딩, 카드 타이틀
- 툴팁, 모달 내용, 알림 메시지
- CLI: 커맨드 설명(`description`), 에러 메시지, 도움말 텍스트

---

## 기능 풍부성 기준 (Feature Richness — 플랫폼별 최소 기준)

> **기능이 빈약한 프로젝트는 완성으로 인정하지 않는다.**
> 아래 기준을 충족하지 못하면 Phase 2-3 구현을 재실행한다.

### 웹 앱 최소 기준
- **화면/페이지 수**: 최소 6개 (로그인 포함 시 7개 이상)
- **Must-have 기능**: 최소 8개 (CRUD 외 실질적 기능 포함)
- **필수 포함 요소**:
  - 검색 또는 필터 기능
  - 목록 + 상세 보기 (2단계 이상 UX)
  - 빈 상태(empty state) 처리
  - 로딩 상태 처리
  - 에러 상태 처리
  - 반응형 레이아웃 (모바일 대응)
  - 대시보드 또는 요약 통계 화면

### 모바일 앱 최소 기준
- **스크린 수**: 최소 6개
- **Must-have 기능**: 최소 7개
- **필수 포함 요소**:
  - 탭 또는 드로어 네비게이션
  - 목록 + 상세 화면
  - 로컬 데이터 영속성 (SQLite)
  - 빈 상태/에러 상태 처리
  - 입력 폼 + 유효성 검사

### CLI 최소 기준
- **커맨드 수**: 최소 5개 (서브커맨드 포함)
- **Must-have 기능**: 최소 6개
- **필수 포함 요소**:
  - 컬러 출력 (chalk 또는 동급)
  - 테이블 형식 출력
  - 로컬 DB 영속성
  - `--help` 전체 문서화
  - 에러 시 친절한 한국어 메시지
  - 설정 저장/불러오기

---

## Phase -0.5: OMC/ECC 환경 감지

이 단계는 **모든 Phase보다 먼저** 자동으로 실행된다. 사용자에게는 별도로 고지하지 않는다.

### 감지 로직

현재 세션에서 사용 가능한 스킬 목록을 확인한다:

```
if "oh-my-claudecode:" in available_skills:
  OMC_MODE = "omc"
elif "everything-claude-code:" in available_skills:
  OMC_MODE = "ecc"
else:
  OMC_MODE = "none"
```

`OMC_MODE` 값에 따라 이후 모든 Phase에서 **Agent 위임 전략**이 달라진다.
`OMC_MODE = "omc"` 일 때 가장 풍부한 스킬 조합을 활용한다.

---

## Phase -1: 체크포인트 확인 + 인터랙티브 설정

### ⚠️ 최우선: RUN_DATE 즉시 캡처

**스킬이 시작되는 즉시, 다른 어떤 작업보다 먼저** RUN_DATE를 캡처한다:

```bash
RUN_DATE=$(date +%Y%m%d%H%M)   # 예: 202605242157
```

이 값은 이후 절대 변경하지 않는다. Phase 3에서 `{RUN_DATE}_report.html` 파일명으로 사용된다.

---

### 0단계 — 이전 실행 체크포인트 확인

스킬 시작 직후 체크포인트 파일을 탐색한다:

```bash
ls .auto-project-builder-checkpoint.json 2>/dev/null
```

파일이 존재하면 내용을 읽어 아래 정보를 추출한다:
- 실행 날짜, 플랫폼, 스택, 총 프로젝트 수
- 완료된 프로젝트 목록
- 남은 프로젝트 목록

그 후 AskUserQuestion 도구로 확인:

```
이전 실행에서 중단된 작업이 있습니다.

실행일: {날짜}  /  플랫폼: {PLATFORM}  /  스택: {TECH_STACK}
완료: {완료 목록}  /  남은 것: {미완료 목록}

이어서 진행할까요, 아니면 새로 시작할까요?

1. 이어서 진행  — 완료된 프로젝트는 건너뛰고 남은 것부터 시작
2. 새로 시작    — 이전 체크포인트 삭제 후 처음부터
```

- **이어서 진행** 선택: 저장된 변수를 복원하고 Phase 2 루프로 바로 진입
- **새로 시작** 선택: 체크포인트 삭제 후 아래 질문 1로 진행

체크포인트 파일이 없으면 질문 1로 바로 진행.

---

### 질문 1 — 플랫폼

```
어떤 플랫폼의 프로젝트를 만들고 싶으신가요?

1. 웹 (Web)          — 브라우저에서 동작하는 웹 앱
2. 앱 (Mobile App)   — iOS / Android 모바일 앱
3. CLI               — 터미널에서 동작하는 커맨드라인 도구
4. 알아서            — 트렌드·서비스 유형 기반으로 자율 선택
5. 자유롭게          — 직접 설명해 주세요
```

**"알아서" 선택 시**: Phase 0-B 트렌드 조사 결과와 SERVICE_CATEGORIES를 바탕으로
가장 적합한 플랫폼을 자율 결정하고 이유와 함께 고지한 뒤 진행한다.
예: `알아서 선택: 웹 — 생산성 SaaS는 브라우저 접근성이 전환율에 직결되므로`

→ 선택 결과를 `PLATFORM`에 저장.

---

### 질문 1.5 — 아이디어 유무

```
생각하고 계신 아이디어가 있으신가요?

1. 알아서   — 트렌드·카테고리 기반으로 아이디어를 자율 기획합니다
2. 직접 입력 — 만들고 싶은 서비스를 설명해 주세요
```

**"직접 입력" 선택 시**:
- 사용자로부터 아이디어 설명을 자유 텍스트로 입력받는다
- 입력 내용을 `USER_IDEA`에 저장
- 사용자가 원하는 서비스가 명확하므로 PROJECT_COUNT = 1로 자동 설정
- 서비스 유형(Q3)과 프로젝트 개수(Q4)는 물어보지 않는다 → **질문 2로 바로 진행**
- 기술 스택(Q2)은 선호 여부만 확인 (없어도 Phase 1에서 아이디어에 맞게 자율 결정)

**"알아서" 선택 시**:
- `USER_IDEA = null`로 저장
- 기존 흐름대로 Q2 → Q3 → Q4 순서로 진행

→ 선택 결과를 `USER_IDEA`에 저장 (직접 입력 텍스트 또는 null).

---

### 질문 2 — 선호하는 기술 스택 (PLATFORM 및 USER_IDEA 기반 추천)

> **이 질문은 항상 표시된다.** 단, USER_IDEA가 있을 경우 추천 스택이 아이디어 내용을 반영한다.

**PLATFORM = 웹 (또는 USER_IDEA가 웹 서비스인 경우):**
```
선호하는 기술 스택이 있으신가요?

1. Next.js 14+ · shadcn/ui · Drizzle + SQLite   (추천)
2. Nuxt 3 · Tailwind CSS · PGlite
3. SvelteKit · shadcn-svelte · Drizzle + SQLite
4. Remix · shadcn/ui · Drizzle + SQLite
5. 없음    — 아이디어가 정해지면 각 프로젝트에 맞는 스택을 자율 선택
6. 직접 입력 — 원하는 스택을 설명해 주세요
```

**PLATFORM = 앱 (또는 USER_IDEA가 모바일 앱인 경우):**
```
선호하는 기술 스택이 있으신가요?

1. React Native + Expo · SQLite (expo-sqlite)   (추천)
2. Flutter · Dart · sqflite
3. 없음    — 아이디어가 정해지면 각 프로젝트에 맞는 스택을 자율 선택
4. 직접 입력 — 원하는 스택을 설명해 주세요
```

**PLATFORM = CLI (또는 USER_IDEA가 CLI 도구인 경우):**
```
선호하는 기술 스택이 있으신가요?

1. Node.js · TypeScript · Commander.js · SQLite   (추천)
2. Python · Typer · Click · SQLite
3. Go · Cobra · SQLite
4. Rust · Clap · SQLite
5. 없음    — 아이디어가 정해지면 각 프로젝트에 맞는 스택을 자율 선택
6. 직접 입력 — 원하는 스택을 설명해 주세요
```

**PLATFORM = 알아서 / 자유롭게:**
```
선호하는 기술 스택이 있으신가요?
(예: "Electron + React + SQLite", "FastAPI + HTMX + PostgreSQL" 등)

1. 없음    — 아이디어가 정해지면 각 프로젝트에 맞는 스택을 자율 선택
2. 직접 입력 — 원하는 스택을 설명해 주세요
```

**"없음" 선택 시**: `TECH_STACK = "auto-per-idea"`로 저장.
Phase 1에서 각 아이디어의 특성(플랫폼, 규모, 복잡도)을 고려해 프로젝트별로
최적 스택을 독립적으로 결정하고, PRD 작성 전 선택 이유와 함께 고지한다.
예: `스택 선택: Flutter — 크로스플랫폼 네이티브 UI가 이 앱의 핵심 경험에 적합하므로`

복수 프로젝트일 경우 아이디어마다 다른 스택이 선택될 수 있다.
예: 아이디어 1 → Next.js, 아이디어 2 → SvelteKit, 아이디어 3 → Remix

→ 선택/입력 결과를 `TECH_STACK`에 저장.

---

### 질문 3 — 서비스 유형

> **이 질문은 `USER_IDEA = null` (알아서 경로)일 때만 표시된다.**
> USER_IDEA가 있으면 서비스 유형은 Phase 1에서 아이디어 내용을 기반으로 자율 결정한다.

```
어떤 유형의 서비스를 만들고 싶으신가요?
(복수 선택 가능)

1.  생산성        — 할 일 관리, 시간 추적, 노트, 자동화
2.  콘텐츠        — 블로그, 미디어, 뉴스레터, 크리에이터 도구
3.  팀·협업       — 팀 관리, 소통, 프로젝트 추적
4.  커머스        — 쇼핑, 마켓플레이스, 구독
5.  교육          — 학습, 퀴즈, 튜터링, 플래시카드
6.  헬스·라이프   — 건강 추적, 피트니스, 웰빙, 식단
7.  파이낸스      — 예산 관리, 투자, 가계부
8.  개발자 도구   — 유틸리티, API 도구, 코드 분석
9.  커뮤니티      — 소셜, 포럼, 네트워킹
10. 알아서        — 트렌드 조사 기반으로 유망 카테고리 자율 선택
11. 자유롭게      — 직접 설명해 주세요
```

**"알아서" 선택 시**: Phase 0-B 트렌드 조사 결과(`TREND_DATA.market_gaps`, `TREND_DATA.trending_categories`)를
기반으로 현재 가장 유망한 카테고리를 자율 선택하고 이유와 함께 고지한 뒤 진행한다.
예: `알아서 선택: 개발자 도구 — GitHub Trending에서 AI 코드 도구 수요가 급증 중이므로`

→ 선택 결과(복수 가능)를 `SERVICE_CATEGORIES[]`에 저장.

---

### 질문 4 — 프로젝트 개수

> **이 질문은 `USER_IDEA = null` (알아서 경로)일 때만 표시된다.**
> USER_IDEA가 있으면 PROJECT_COUNT = 1로 자동 설정하고 이 질문은 건너뛴다.

```
총 몇 개의 서비스를 만들까요? (기본값: 5, 최대: 10)

숫자 입력, 또는:
- 알아서 — 선택한 카테고리 수와 트렌드 밀도를 기반으로 자율 결정
```

**"알아서" 선택 시**: `SERVICE_CATEGORIES` 수와 `TREND_DATA.competitive_density`를 기반으로
적정 개수를 결정한다. 카테고리 1개당 2–3개, 최대 10개를 초과하지 않는다.
예: `알아서 선택: 6개 — 카테고리 2개 × 3개씩`

→ 입력값을 `PROJECT_COUNT`에 저장. 빈 입력이면 5. "알아서"이면 위 공식으로 계산.

---

### 설정 요약 출력

**USER_IDEA가 있는 경우 (직접 입력 경로):**

```
━━━ 설정 요약 ━━━
플랫폼:      {PLATFORM}
아이디어:    {USER_IDEA}
선호 스택:   {TECH_STACK | "아이디어 기반 자율 선택"}
서비스 유형: 아이디어 기반 자율 결정
프로젝트 수: 1개
━━━━━━━━━━━━━━━━━
진행할까요? (yes / 취소)
```

**USER_IDEA가 없는 경우 (알아서 경로):**

```
━━━ 설정 요약 ━━━
플랫폼:      {PLATFORM}
선호 스택:   {TECH_STACK | "아이디어별 자율 선택"}
서비스 유형: {SERVICE_CATEGORIES}
프로젝트 수: {PROJECT_COUNT}개
━━━━━━━━━━━━━━━━━
진행할까요? (yes / 취소)
```

사용자가 yes가 아닌 경우 Phase -1 처음으로 돌아간다.

---

## Phase 0: 환경 조사

Context7 조사와 트렌드 조사를 **병렬로** 실행한다.

### 0-A. Context7 스택 조사 (병렬 레인 1)

`TECH_STACK`에 포함된 라이브러리/프레임워크의 최신 버전과 권장 사용 패턴 조사.

```
# 공통
mcp__context7__resolve-library-id("drizzle-orm")

# 웹 — Next.js 선택 시
mcp__context7__resolve-library-id("next.js")
mcp__context7__resolve-library-id("shadcn/ui")
mcp__context7__resolve-library-id("better-sqlite3")
mcp__context7__resolve-library-id("next-auth")

# 앱 — React Native 선택 시
mcp__context7__resolve-library-id("react-native")
mcp__context7__resolve-library-id("expo")

# CLI — Node.js 선택 시
mcp__context7__resolve-library-id("commander")
mcp__context7__resolve-library-id("inquirer")

# ... 선택 스택에 맞게 동적으로 조사
```

조사 결과를 `STACK_VERSIONS`에 저장.

### 0-B. 트렌드 조사 (병렬 레인 2)

**OMC_MODE == "omc"** 일 때도 WebSearch 또는 Exa로 직접 조사 (autoresearch는 웹 조사 도구가 아닌 반복 개선 루프이므로 사용하지 않는다):

그 외 모드에서도 동일하게 WebSearch 또는 Exa로 직접 조사:

```
# Product Hunt 최근 인기 서비스
WebSearch("site:producthunt.com {SERVICE_CATEGORIES} {PLATFORM} app 2025 2026")

# GitHub Trending 조사
WebSearch("github trending {TECH_STACK_KEYWORD} repositories 2025")

# 해당 카테고리 인기 앱/서비스 현황
WebSearch("{SERVICE_CATEGORIES} best apps 2025 market trends")
```

조사 결과를 `TREND_DATA`에 저장:
```json
{
  "trending_categories": ["현재 뜨는 세부 카테고리"],
  "popular_features": ["사용자들이 원하는 기능"],
  "market_gaps": ["아직 해결 안 된 문제"],
  "competitive_density": "high | medium | low"
}
```

두 레인 완료 후 Phase 1로 진행.

---

## 변수 추적 (Variable Flow)

| 변수명 | 초기화 위치 | 타입/범위 |
|--------|------------|-----------|
| `OMC_MODE` | Phase -0.5 | string: "omc" / "ecc" / "none" |
| `PLATFORM` | Phase -1 Q1 | string: 웹/앱/CLI/auto/자유 |
| `USER_IDEA` | Phase -1 Q1.5 | string(사용자 입력 텍스트) 또는 null; null이면 알아서 경로 |
| `TECH_STACK` | Phase -1 Q2 | string: 선택 스택 명칭 또는 "auto-per-idea" (아이디어별 자율 결정) |
| `SERVICE_CATEGORIES[]` | Phase -1 Q3 (USER_IDEA=null 시만) | string[]; "auto" 이면 트렌드 기반 자율 결정; USER_IDEA 있으면 Phase 1에서 자율 결정 |
| `PROJECT_COUNT` | Phase -1 Q4 (USER_IDEA=null 시만) | 정수 1–10, 기본 5; USER_IDEA 있으면 1로 고정; "알아서" 이면 공식 계산 |
| `STACK_VERSIONS` | Phase 0-A | 라이브러리 버전 맵 |
| `TREND_DATA` | Phase 0-B | 트렌드 조사 결과 객체 |
| `IDEAS[]` | Phase 1 | PROJECT_COUNT개 객체 배열 |
| `IDEA_SCORES[]` | Phase 1.3 | idea-generator 출력: {idea, pain, market, originality, feasibility, flaw_penalty, total/15, verdict}[] |
| `GITHUB_REPOS[]` | Phase 1.5 | {name, description, url}[] |
| `REJECTED_IDEAS[]` | Phase 1.3 + 1.5 | 탈락 아이디어 + 사유 |
| `APPROVED_IDEAS[]` | Phase 1.5 | 최종 승인 아이디어 |
| `REPLACEMENT_ATTEMPTS` | Phase 1.3 + 1.5 | 정수, 최대 PROJECT_COUNT×3 |
| `PROJECT_LOG[]` | Phase 2 | 완료 프로젝트 로그 |
| `QA_ATTEMPTS` | Phase 2-4 | 프로젝트별 QA 재시도 횟수 |
| `DESIGNER_OUTPUT_PATH` | Phase 2-3 (웹/앱만) | string: `projects/{slug}/UI_GUIDE.md`; 웹/앱 아닌 경우 null |
| `GITHUB_URLS[]` | Phase 2-6 | string[]: push 완료된 저장소 URL 목록 |
| `SKIPPED_PROJECTS[]` | Phase 2 | string[]: status="skip"인 프로젝트 slug 목록 |
| `RUN_DATE` | Phase -1 시작 즉시 | YYYYMMDDHHmm 형식 (년월일시분, 예: `202605242157`) — 이후 절대 변경하지 않음 |
| `CHECKPOINT_FILE` | Phase -1 | `.auto-project-builder-checkpoint.json` |
| `USE_AUTOPILOT` | Phase 2 시작 직전 | bool; `(OMC_MODE == "omc") AND (user_requested_autopilot OR PROJECT_COUNT >= 5)` — True이면 루프 건너뛰고 autopilot Skill 호출 |

---

## Phase 1: 아이디어 생성 (`idea-generator` 스킬 활용)

> **아이디어 품질이 최종 프로젝트 품질을 결정한다.**
> 이 단계는 전용 `idea-generator` 스킬에 위임하여 멀티소스 페인 마이닝과 YC 스타일 적대적 평가를 수행한다.
> 트렌딩 기술이 아니라 **실제 사용자 고통의 증거**에서 아이디어를 뽑아낸다.

### USER_IDEA 분기

```
if USER_IDEA != null:
  # 사용자가 직접 아이디어를 입력한 경우 — 바로 빌드 준비
  IDEAS = [{
    "slug": slugify(USER_IDEA),
    "name_ko": USER_IDEA,
    "pain_statement": "사용자가 직접 제시한 아이디어",
    "pain_evidence": ["사용자 직접 입력"],
    "target_user": "아이디어 내용에서 자율 추론",
    "core_features": [],   # Phase 2-1 PRD 작성 시 확정
    "tech_stack": TECH_STACK,
    "verdict": "GO"
  }]
  SERVICE_CATEGORIES = infer_category(USER_IDEA)
  APPROVED_IDEAS = IDEAS
  → Phase 1.5(GitHub 중복 검토)로 바로 진행
else:
  → idea-generator 스킬 호출 (아래)
```

### idea-generator 스킬 호출

`USER_IDEA == null`인 경우, `idea-generator` 스킬을 아래 컨텍스트와 함께 실행한다:

```
Skill("idea-generator", context={
  "PLATFORM": PLATFORM,
  "SERVICE_CATEGORIES": SERVICE_CATEGORIES,
  "TREND_DATA": TREND_DATA,
  "PROJECT_COUNT": PROJECT_COUNT,
  "TECH_STACK": TECH_STACK,
  "OMC_MODE": OMC_MODE
})
```

idea-generator 스킬이 수행하는 작업:

1. **Phase A — 멀티소스 페인 마이닝** (4레인 병렬)
   - Reddit: "I wish there was" / "why is there no" 불만 수집
   - Hacker News: "Ask HN: Is there a tool for..." 미충족 수요 스레드
   - 앱스토어 1점 리뷰: 경쟁 제품의 반복되는 불만 패턴
   - GitHub Issues: 인기 저장소의 미해결 feature request

2. **Phase B — 페인 클러스터 → 아이디어 변환**
   - 수집된 고통 증거를 클러스터링
   - PROJECT_COUNT × 2개 후보 아이디어 생성 (필터링 여유분)
   - 모든 아이디어는 실제 인용문에 근거

3. **Phase C — 병렬 3역할 적대적 평가**
   - planner: 제품 기획자 시각 (가치 제안, 타겟 페르소나, 킬러 기능)
   - architect: 기술 아키텍트 시각 (구현 가능성, 리스크, MVP sprint 수)
   - critic: YC 심사위원 시각 (실패 이유 먼저, 경쟁자 검토, 수익화 경로)

4. **Phase D — 15점 YC 스코어카드 + go/no-go 판정**
   - 페인 강도(1-3) + 시장 규모(1-3) + 독창성(1-3) + 구현 가능성(1-3) + 치명적 결함 감점(-3~0)
   - GO(≥11) / CONDITIONAL(8–10) / NO-GO(≤7)

스킬 종료 후 `IDEAS[]`가 컨텍스트에 설정된다. 각 아이디어 객체는 다음을 포함한다:
`slug`, `name_ko`, `pain_evidence[]`, `target_user`, `core_features[]`,
`competitors[]`, `differentiator`, `tech_stack`, `score{total/15}`,
`fatal_flaws[]`, `flaw_mitigations[]`, `verdict`

### TECH_STACK = "auto-per-idea" 처리

`TECH_STACK = "auto-per-idea"`이면 idea-generator가 각 아이디어별로 최적 스택을 독립 결정하여
아이디어 객체의 `tech_stack` 필드에 저장한다. 이후 Phase 2에서는 아이디어별 `tech_stack`을 사용한다.

---

## Phase 1.3: 아이디어 평가 결과 확인

> **평가는 idea-generator 내부에서 완료된다.** (15점 YC 스타일 스코어카드)
> 이 단계는 결과를 확인하고 APPROVED_IDEAS를 확정하는 역할만 한다.

```
APPROVED_IDEAS = [idea for idea in IDEAS if idea.verdict in ["GO", "CONDITIONAL"]]
REJECTED_IDEAS = [idea for idea in IDEAS if idea.verdict == "NO-GO"]
# NO-GO 아이디어의 대체는 idea-generator 내부에서 이미 처리됨
```

판정 기준:
- **GO** (11점 이상): 즉시 빌드 추천
- **CONDITIONAL** (8–10점): 지적된 결함 수정 사항을 Phase 2-1 PRD에 반영 후 진행
- **NO-GO** (7점 이하): 폐기 — idea-generator가 자동으로 대체 아이디어 생성

평가 결과 출력:
```
━━━ 아이디어 평가 결과 ━━━
통과: {A}개 ✅  |  탈락: {R}개 ❌  |  (idea-generator 내부에서 대체 생성 완료)
─────────────────────────
{서비스명}  페인 {P}/3 · 시장 {M}/3 · 독창성 {O}/3 · 구현 {F}/3 · 결함 {X}  = {T}/15  ✅/⚠️/❌
...
━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 1.5: GitHub 중복 검토

```bash
gh repo list --limit 200 --json name,description,url
```

유사도 판정 후 탈락/승인 분류. 대체 아이디어 생성 루프 실행 (최대 PROJECT_COUNT×3회).

결과 출력:
```
━━━ GitHub 중복 검토 결과 ━━━
총 검토: {N}개 | 승인: {A}개 ✅ | 탈락: {R}개 ❌ | 대체 시도: {T}회
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 2: 각 프로젝트 실행 루프

`APPROVED_IDEAS[]`를 순회하며 각 프로젝트를 `TECH_STACK` 기준으로 구현.

### ⚠️ 프로젝트별 실행 전략 (OMC_MODE에 따라 분기)

**메인 루프는 OMC_MODE와 USE_AUTOPILOT에 따라 다른 전략으로 각 프로젝트를 처리한다.**
- **전략 A (기본)**: OMC 에이전트를 단계별 순차 호출 (`_run_omc_pipeline`)
- **전략 B**: autopilot에 Phase 2 전체 위임 (루프를 건너뜀)
- **기본 모드**: 단일 Agent가 전체 단계를 처리

모든 결과물(PRD, ROADMAP, 코드)은 **디스크에 저장**되며, 메인 컨텍스트에는 단계별 한 줄 요약과 최종 JSON만 수집된다.

```
# 메인 루프
PROJECT_LOG = []

# ──────────────────────────────────────────────────────────────────
# 전략 선택: OMC 모드에서 autopilot 전략 B를 선택하면 루프를 건너뜀
# USE_AUTOPILOT = True 조건:
#   - 사용자가 명시적으로 autopilot 사용을 요청한 경우, 또는
#   - PROJECT_COUNT >= 5 이고 모니터링 없이 완전 자율 실행을 원하는 경우
# ──────────────────────────────────────────────────────────────────
USE_AUTOPILOT = (OMC_MODE == "omc") AND (user_requested_autopilot OR PROJECT_COUNT >= 5)

if USE_AUTOPILOT:
  # 전략 B: autopilot에 Phase 2 전체 위임 (아래 "OMC 모드 실행 전략 선택" 섹션 참조)
  Skill("oh-my-claudecode:autopilot",
    prompt="{PROJECT_COUNT}개 프로젝트를 아래 사양으로 처음부터 끝까지 완성하라.
            프로젝트 목록: {APPROVED_IDEAS}
            공통: PLATFORM={PLATFORM}, TECH_STACK={TECH_STACK}, 작업 경로=projects/{slug}/
            단계 순서: PRD → ROADMAP → 구현 → QA(최대 3회) → README → push
            QA 3회 실패 시 MoSCoW SHOULD/COULD 기능 제거 후 재시도, 그래도 실패 시 SKIP.")
  # autopilot 완료 후 Phase 3(리포트)로 바로 이동
else:
  # 전략 A (기본): 프로젝트별 루프
  for idea in APPROVED_IDEAS:
    if idea.slug in CHECKPOINT.completed_projects:
      continue  # 이미 완료된 프로젝트는 건너뜀

    idea_summary = {
      "slug": idea.slug,
      "name_ko": idea.name_ko,
      "tech_stack": idea.tech_stack,
      "core_features": idea.core_features,
      "platform": PLATFORM
    }

    if OMC_MODE == "omc":
      result = _run_omc_pipeline(idea, idea_summary)   # 전문 OMC 에이전트 파이프라인
    else:
      result = _run_default_pipeline(idea, idea_summary)  # 단일 에이전트 처리

    PROJECT_LOG.append(result)
    checkpoint_update(idea.slug, result)

    completed_count = len([r for r in PROJECT_LOG if r.status == "done"])
    if completed_count % 3 == 0 and completed_count > 0:
      print(f"💾 {completed_count}개 완료 — 컨텍스트 절약을 위해 /compact 를 실행하거나 계속 진행할 수 있습니다.")
```

---

#### _run_default_pipeline (OMC_MODE != "omc")

단일 Agent가 PRD → ROADMAP → 구현 → QA → README → push를 모두 처리한다.

```
def _run_default_pipeline(idea, idea_summary):
  result = Agent(
    prompt=f"""
아래 프로젝트를 처음부터 끝까지 완성하라.

아이디어: {idea_summary}
플랫폼: {PLATFORM}
스택: {idea.tech_stack}
작업 경로: projects/{idea.slug}/

★ 필수 실행 순서 (절대 예외 없음):
1. PRD 작성 → projects/{idea.slug}/PRD.md 파일로 저장
2. ROADMAP 작성 → projects/{idea.slug}/ROADMAP.md 파일로 저장
   ★★★ ROADMAP.md가 존재하지 않으면 구현(3단계)으로 절대 진행하지 않는다 ★★★
3. 구현 → ROADMAP.md를 읽고 Sprint 번호 순서대로 (임의 변경 금지)
4. QA 루프 (최대 3회)
5. README.md 생성
6. GitHub push

완료 기준:
- tsc/lint/build 오류 0개
- 한국어 UI (모든 버튼·레이블·메시지)
- 웹/앱: 최소 6개 화면, 대시보드, 검색/필터 포함
- CLI: 최소 5개 커맨드, 테이블 출력, 컬러 포함
- README.md 생성
- GitHub push 완료

반환 형식 (JSON만, 다른 텍스트 없음):
{{
  "slug": "{idea.slug}",
  "status": "done | skip",
  "qa_attempts": <숫자>,
  "github_url": "<URL 또는 null>",
  "errors_fixed": ["<오류 1줄 요약>"],
  "skipped_reason": null
}}
""",
    run_in_background=False
  )
  return result
```

---

#### _run_omc_pipeline (OMC_MODE == "omc")

전문 OMC 에이전트를 단계별로 순차 호출한다. 각 에이전트는 결과물을 **디스크에 저장**하고
**한 줄 요약만** 메인 컨텍스트로 반환한다 — 컨텍스트 오염 없음.

**★ PRD → ROADMAP 순서는 절대 예외가 없다. ROADMAP.md 없이 구현을 시작하면 절대 안 된다.**

```
def _run_omc_pipeline(idea, idea_summary):
  slug = idea.slug
  errors_fixed = []
  qa_attempts = 0
  github_url = None
  high_issues_count = 0

  # ── Phase 2-1: PRD 작성 (oh-my-claudecode:planner) ───────────────
  Agent(oh-my-claudecode:planner,
    prompt="다음 아이디어의 PRD를 작성하라: {idea_summary}.
            플랫폼: {PLATFORM}, 스택: {idea.tech_stack}.
            Must-have 기능 웹/앱 8개 이상, CLI 6개 이상 정의.
            각 기능에 서브기능 2개 이상 포함 (단순 CRUD만 금지).
            검색/필터, 통계/대시보드, 빈 상태 처리를 Must-have에 반드시 포함.
            한국어 UI 텍스트 가이드(주요 버튼·레이블·메시지) 포함.
            출력 경로: projects/{slug}/PRD.md
            완료 후 한 줄 상태만 반환: 'PRD 완료 | Must-have N개'")

  # ── PRD.md 존재 검증 (필수 게이트) ─────────────────────────────────
  if not file_exists(f"projects/{slug}/PRD.md"):
    # planner 실패 폴백: 직접 최소 PRD 작성
    # idea_summary.core_features 기반으로 Must-have 8개+ 직접 생성
    # 형식: MoSCoW 테이블(Must/Should/Could), 타겟 페르소나, 화면 목록, 한국어 UI 가이드
    # 스택별 비기능 요구사항(성능·보안·접근성) 포함
    Write(f"projects/{slug}/PRD.md", content=generate_minimal_prd(idea_summary))
    if not file_exists(f"projects/{slug}/PRD.md"):
      return {"slug": slug, "status": "skip", "qa_attempts": 0,
              "github_url": null, "errors_fixed": [], "skipped_reason": "PRD 생성 실패"}

  # ── Phase 2-2: ROADMAP 작성 (oh-my-claudecode:architect) ─────────
  Agent(oh-my-claudecode:architect,
    prompt="PRD(projects/{slug}/PRD.md) 기반 기술 아키텍처 설계.
            스택: {idea.tech_stack}.
            Sprint 계획(번호·목표·완료 기준 명시), DB 스키마, 컴포넌트 구조도, 기술 결정 근거 포함.
            각 Sprint는 독립 완료 가능 단위로 작성하여 executor가 Sprint 번호 순서대로 구현할 수 있게 하라.
            출력 경로: projects/{slug}/ROADMAP.md
            완료 후 한 줄 상태만 반환: 'ROADMAP 완료 | Sprint N개'")

  # ── ROADMAP.md 존재 검증 ★★★ 구현 전 절대 필수 게이트 ★★★ ────────
  if not file_exists(f"projects/{slug}/ROADMAP.md"):
    # architect 실패 폴백: 스택별 기본 Sprint 구조로 직접 ROADMAP 작성
    # 웹→Sprint 0~6, 앱→Sprint 0~5, CLI→Sprint 0~5 (Phase 2-2 참고)
    # PRD Must-have 기능을 Sprint에 균등 분배, 각 Sprint에 완료 기준 명시
    # DB 스키마·컴포넌트 구조도는 기본 형식으로 포함
    Write(f"projects/{slug}/ROADMAP.md", content=generate_minimal_roadmap(idea_summary, PLATFORM))
    if not file_exists(f"projects/{slug}/ROADMAP.md"):
      return {"slug": slug, "status": "skip", "qa_attempts": 0,
              "github_url": null, "errors_fixed": [], "skipped_reason": "ROADMAP 생성 실패"}
  # ROADMAP.md 없이는 절대로 구현(Phase 2-3)으로 진행하지 않는다

  # ── Phase 2-3: 구현 ──────────────────────────────────────────────

  # 웹/앱: designer가 먼저 UI 가이드 작성 (oh-my-claudecode:designer)
  if PLATFORM in ["웹", "앱"]:
    Agent(oh-my-claudecode:designer,
      prompt="PRD(projects/{slug}/PRD.md) + ROADMAP(projects/{slug}/ROADMAP.md) 기반 UI/UX 설계.
              컴포넌트 목록, 색상 팔레트, 레이아웃 초안 제공. 스택: {idea.tech_stack}.
              ★ 출력 경로: projects/{slug}/UI_GUIDE.md (반드시 이 경로에 마크다운으로 저장)
              완료 후 한 줄 상태만 반환: 'UI가이드 완료 | 컴포넌트 N개'")

  # executor: ROADMAP Sprint 순서대로 구현 (oh-my-claudecode:executor)
  Agent(oh-my-claudecode:executor,
    prompt="구현 시작 전 projects/{slug}/ROADMAP.md를 반드시 읽고
            Sprint 번호 순서대로 완료 기준 확인 후 구현하라. 스택: {idea.tech_stack}.
            ★ 파일 위치: 모든 파일은 projects/{slug}/ 안에만 생성·수정 (바깥 경로 절대 금지)
            ★ ROADMAP Sprint 순서 준수 — 임의 변경 금지, 완료 기준 충족 후 다음 Sprint 진행
            ★ 웹/앱: projects/{slug}/UI_GUIDE.md 가 존재하면 반드시 읽고 UI 설계를 따르라
            ★ 한국어 UI 필수 — 모든 버튼·레이블·메뉴·메시지·빈 상태 메시지
            ★ 웹/앱: 최소 6개 화면, 대시보드/통계, 검색/필터, 빈 상태·로딩·에러 상태 포함
            ★ CLI: 최소 5개 커맨드, 테이블 출력, 컬러, 진행 상태 표시 포함
            ★ 코드 품질: immutable 패턴, Repository 패턴, 명시적 에러 처리
            완료 후 한 줄 상태만 반환: '구현 완료 | 파일 N개 | Sprint N개 완료'")

  # 코드 리뷰 (oh-my-claudecode:code-reviewer)
  review_result = Agent(oh-my-claudecode:code-reviewer,
    prompt="projects/{slug}/ 코드 리뷰. CRITICAL/HIGH 이슈 직접 수정.
            완료 후 한 줄 상태만 반환: '리뷰 완료 | CRITICAL N개, HIGH N개 수정'")
  high_issues_count = parse_high_count(review_result)

  # 보안 검토 — 인증/외부 API/사용자 입력 처리가 있는 경우 (oh-my-claudecode:security-reviewer)
  if PRD includes "auth" OR "user input" OR "external API":
    Agent(oh-my-claudecode:security-reviewer,
      prompt="projects/{slug}/ OWASP Top 10 기준 보안 취약점 검토. CRITICAL 즉시 수정.
              완료 후 한 줄 상태만 반환: '보안검토 완료 | CRITICAL N개 수정'")

  # ── Phase 2-4: QA 루프 ──────────────────────────────────────────
  while qa_attempts < 3:
    qa_result = run_qa_commands(slug)
    if qa_result.success: break

    qa_attempts += 1
    errors_fixed.extend(qa_result.errors)

    # debugger: 근본 원인 분석 + 수정 (oh-my-claudecode:debugger)
    Agent(oh-my-claudecode:debugger,
      prompt="다음 빌드 오류를 근본 원인부터 분석하고 수정하라: {qa_result.errors}
              프로젝트: projects/{slug}/ 스택: {idea.tech_stack}
              완료 후 한 줄 상태만 반환: '디버그 완료 | 수정 N건'")

  if qa_attempts == 3 and not qa_result.success:
    # 스코프 축소: PRD MoSCoW 테이블의 SHOULD-have / COULD-have 항목 전부 제거
    # Must-have 기능의 관련 소스 파일·라우트·컴포넌트만 남기고 나머지 삭제 또는 stub 처리
    # ROADMAP의 관련 Sprint 태스크도 동일하게 제거
    Agent(oh-my-claudecode:executor,
      prompt="projects/{slug}/PRD.md의 MoSCoW 테이블에서 SHOULD-have / COULD-have 항목을 전부 제거하라.
              Must-have 항목만 남기고, 해당하지 않는 소스 파일·라우트·컴포넌트를 삭제 또는 stub 처리.
              projects/{slug}/ROADMAP.md의 관련 Sprint 태스크도 동일하게 제거.
              이후 Must-have 기능만으로 재구현하라.")
    qa_result = run_qa_commands(slug)
    if not qa_result.success:
      return {"slug": slug, "status": "skip", "qa_attempts": qa_attempts,
              "github_url": null, "errors_fixed": errors_fixed,
              "skipped_reason": "QA 3회 실패 + 스코프 축소 후에도 빌드 불통"}

  # QA 통과 후 기능 검증 (oh-my-claudecode:verifier)
  Agent(oh-my-claudecode:verifier,
    prompt="projects/{slug}/ PRD Must-have 기능이 실제 동작하는지 검증.
            실패 항목은 구체적 재현 방법과 함께 보고.
            완료 후 한 줄 상태만 반환: '검증 완료 | 통과 N/M개'")

  # ── ralph 품질 개선 루프 (자동 조건 충족 시) ──────────────────────
  # 아래 조건 중 하나 이상 충족 시 ralph 자동 실행:
  if qa_attempts >= 2 OR idea.score.total <= 6 OR high_issues_count >= 3:
    Skill("oh-my-claudecode:ralph",
      prompt="projects/{slug}/ 의 품질을 아래 기준으로 완성하라.
              Acceptance Criteria:
              1. 테스트 커버리지 80% 이상
              2. tsc/lint/build 오류 0개
              3. 모든 에러 경계에서 명시적 에러 처리
              4. 함수/컴포넌트 200줄 이하
              5. PRD Must-have 기능 전부 동작
              제약: 기존 기능 동작 유지, 스코프 확장 금지.")

  # ── Phase 2-5: README 작성 (oh-my-claudecode:writer) ─────────────
  Agent(oh-my-claudecode:writer,
    prompt="projects/{slug}/ README.md 작성. PRD + 실제 구현 기반.
            포함: 서비스 소개, 기능 목록, 기술 스택 표, 설치/실행 방법.
            언어: 영문, 톤: 간결하고 기술적.
            완료 후 한 줄 상태만 반환: 'README 완료'")

  # ── Phase 2-6: GitHub Push (oh-my-claudecode:git-master) ─────────
  git_result = Agent(oh-my-claudecode:git-master,
    prompt="projects/{slug}/ 를 새 GitHub 저장소 {slug}에 push.
            커밋 메시지: 'feat: initial implementation of {idea.name_ko}'.
            저장소 설명: '{idea 한 줄 설명}'.
            완료 후 한 줄 상태만 반환: 'push 완료 | URL: <URL>'")
  github_url = parse_url(git_result)

  return {
    "slug": slug,
    "status": "done",
    "qa_attempts": qa_attempts,
    "github_url": github_url,
    "errors_fixed": errors_fixed,
    "skipped_reason": null
  }
```

> OMC 파이프라인에서도 각 에이전트는 결과물을 디스크에 저장하고 **한 줄 요약만** 반환한다.
> 10개 프로젝트를 실행해도 메인 컨텍스트에는 단계별 한 줄 로그와 JSON 10줄만 쌓인다.

---

### OMC 모드 실행 전략 선택 (OMC_MODE = "omc")

OMC 모드에서는 **두 가지 실행 전략 중 하나를 선택한다.** 혼용하지 않는다.

| 전략 | 언제 사용 | 제어 수준 |
|------|-----------|-----------|
| **A. `_run_omc_pipeline` (기본값)** | 단계별 진행 상황을 확인하며 제어하고 싶을 때 | 높음 — 각 에이전트 결과를 확인 후 다음 단계 진행 |
| **B. autopilot (완전 자율)** | 사람 개입 없이 처음부터 끝까지 자동 완성할 때 | 낮음 — autopilot이 모든 판단을 자율 처리 |

**전략 A (기본값)**: 위의 `_run_omc_pipeline` 함수가 호출된다. planner → architect → designer → executor → code-reviewer → debugger → verifier → writer → git-master 순서로 각 OMC 전문 에이전트를 단계별 호출.

**전략 B (autopilot)**: 사용자가 명시적으로 autopilot 사용을 요청하거나 PROJECT_COUNT ≥ 5이고 모니터링 없이 완전 자율 실행을 원하는 경우.

```
# 전략 B: autopilot에 Phase 2 전체 위임
Skill("oh-my-claudecode:autopilot",
  prompt="아래 조건으로 {PROJECT_COUNT}개 프로젝트를 처음부터 끝까지 완성하라.

  완료 기준:
  - tsc/lint/build 오류 없음
  - 80%+ 테스트 커버리지
  - README.md 생성
  - GitHub push 완료

  프로젝트 목록: {APPROVED_IDEAS}
  플랫폼: {PLATFORM}  스택: {TECH_STACK}
  작업 디렉토리: projects/  (모든 파일은 projects/{slug}/ 안에만 생성)

  각 프로젝트 완료 시 체크포인트 저장:
  .auto-project-builder-checkpoint.json

  단계 순서: PRD → ROADMAP → 구현 → QA 루프(최대 3회) → README → GitHub push
  QA 실패 3회 시 MoSCoW SHOULD/COULD 기능 제거 후 재시도, 그래도 실패 시 SKIP 마킹.")
```

> **주의**: 전략 A와 B를 동시에 실행하지 않는다. 전략 B를 선택하면 `_run_omc_pipeline` 루프를 건너뛴다.

---

루프 시작 시 체크포인트에서 이미 완료된 프로젝트는 건너뛴다:
```
if slug in CHECKPOINT.completed_projects: SKIP → 다음 아이디어
```

---

---

> **📌 참조 문서 (Phase 2-1 ~ 2-6)**
> 아래 섹션은 각 단계의 요구 사항 명세이다.
> **실제 실행 코드는 `_run_omc_pipeline` 함수 (위)가 권위 있는 원본이다.**
> 두 섹션이 상충하면 `_run_omc_pipeline`의 코드를 따른다.

---

### 2-1. PRD 작성 (`projects/{slug}/PRD.md`)

**OMC_MODE == "omc"** 일 때:
```
Agent(oh-my-claudecode:planner,
  prompt="다음 아이디어의 PRD를 작성하라: {IDEA}.
          플랫폼: {PLATFORM}, 스택: {TECH_STACK}.

          ★ 기능 풍부성 요구사항 (필수):
          - Must-have 기능을 웹/앱이면 8개 이상, CLI이면 6개 이상 정의
          - 각 기능은 서브기능 2개 이상 포함 (단순 CRUD만은 금지)
          - 검색/필터, 통계/대시보드, 빈 상태 처리를 반드시 기능 목록에 포함
          - 사용자가 매일 쓸 이유가 있는 핵심 기능 1개를 'killer feature'로 명시

          ★ 한국어 UI 요구사항 (필수):
          - 모든 화면명, 기능명, 버튼명을 한국어로 명시
          - 예: '대시보드', '내 활동', '설정', '저장하기', '삭제', '검색'

          포함: 타겟 사용자 페르소나, MoSCoW 기능 목록(Must 8개+),
          경쟁 서비스 분석 + 차별점, 데이터 모델 초안, 비기능 요구사항,
          화면 목록(웹/앱 6개+, CLI 커맨드 5개+).
          출력 경로: projects/{slug}/PRD.md")
```

그 외 모드에서는 직접 작성. 포함 내용:
- 서비스 개요 및 목적
- 타겟 사용자 페르소나
- 핵심 기능 (MoSCoW 우선순위, Must-have 최소 8개)
- 화면/커맨드 목록 (웹/앱 6개+, CLI 5개+)
- 경쟁 서비스 분석 및 차별점
- 선택된 기술 스택 명세 (`TECH_STACK` 기반)
- 데이터 모델 초안
- 비기능 요구사항
- 한국어 UI 텍스트 가이드 (주요 레이블/버튼명)

---

### 2-2. ROADMAP 작성 (`projects/{slug}/ROADMAP.md`)

> PRD.md 완성 후 즉시 실행. 구현은 반드시 ROADMAP Sprint 순서를 따른다.

**OMC_MODE == "omc"** 일 때:
```
Agent(oh-my-claudecode:architect,
  prompt="PRD(projects/{slug}/PRD.md) 기반 기술 아키텍처 설계.
          스택: {TECH_STACK}.
          포함: Sprint 계획(번호·목표·완료 기준 명시), DB 스키마, 컴포넌트 구조도, 기술 결정 근거.
          각 Sprint는 독립적으로 완료 가능한 단위로 쪼개어, 이후 executor가
          Sprint 번호 순서대로 구현할 수 있도록 상세히 작성하라.
          출력 경로: projects/{slug}/ROADMAP.md")
```

그 외 모드에서는 직접 작성. `TECH_STACK`에 맞는 Sprint 계획:

**웹 (Next.js):**
- Sprint 0: 프로젝트 셋업 (Next.js 초기화, 의존성 설치)
- Sprint 1: DB 스키마 (Drizzle + SQLite)
- Sprint 2: 핵심 기능 구현
- Sprint 3: UI/UX (shadcn/ui)
- Sprint 4: 인증 (NextAuth — 필요 시)
- Sprint 5: 테스트 + 마무리
- Sprint 6: GitHub push

**앱 (React Native/Expo):**
- Sprint 0: Expo 초기화, 의존성
- Sprint 1: 네비게이션 구조 + SQLite 스키마
- Sprint 2: 핵심 기능 구현
- Sprint 3: UI 컴포넌트
- Sprint 4: 테스트 + 마무리
- Sprint 5: GitHub push

**CLI (Node.js):**
- Sprint 0: 프로젝트 셋업, Commander.js
- Sprint 1: SQLite 스키마 + DB 초기화
- Sprint 2: 핵심 커맨드 구현
- Sprint 3: 출력 포맷·UX
- Sprint 4: 테스트 + 마무리
- Sprint 5: GitHub push + npm publish 준비

**자유 스택:** 위를 참고해 적합한 Sprint 계획 자율 수립.

---

### 2-3. 구현

**OMC_MODE == "omc"** 일 때 — 아래 순서로 에이전트 위임:

```
# 1. UI 있는 플랫폼(웹/앱): designer가 먼저 UI 가이드 작성
if PLATFORM in ["웹", "앱"]:
  Agent(oh-my-claudecode:designer,
    prompt="PRD + ROADMAP 기반 UI/UX 설계.
            컴포넌트 목록, 색상 팔레트, 레이아웃 초안 제공.
            스택: {TECH_STACK}")

# 2. executor가 ROADMAP Sprint 순서대로 구현
Agent(oh-my-claudecode:executor,
  prompt="구현 시작 전 projects/{slug}/ROADMAP.md를 반드시 읽고
          Sprint 번호 순서대로 완료 기준을 확인한 뒤 구현하라.
          스택: {TECH_STACK}.

          ★ ROADMAP 준수 (절대 예외 없음):
          - ROADMAP.md의 Sprint 순서를 지킨다 (임의 순서 변경 금지)
          - 각 Sprint의 완료 기준을 충족한 뒤 다음 Sprint로 넘어간다
          - PRD Must-have 기능 중 ROADMAP에 없는 항목 발견 시 Sprint에 추가 후 구현

          ★ 한국어 UI 필수 (예외 없음):
          모든 버튼·레이블·메뉴·플레이스홀더·에러메시지·빈 상태 메시지를
          한국어로 작성하라. 영어 UI 텍스트는 빌드 실패와 동일하게 처리.

          ★ 기능 풍부성 필수:
          - 웹/앱: 최소 6개 화면, 검색·필터·빈 상태·로딩·에러 상태 반드시 구현
          - CLI: 최소 5개 커맨드, 테이블 출력·컬러·진행 상태 표시 포함
          - 대시보드/통계 화면 반드시 포함 (웹/앱)
          - 목록 화면에 정렬·필터 기능 1개 이상 포함

          ★ 코드 품질:
          immutable 패턴, Repository 패턴, 명시적 에러 처리 준수.
          완료 기준: 컴파일·린트·빌드 오류 없음, 80%+ 테스트 커버리지.")

# 3. 코드 리뷰 (구현 직후)
Agent(oh-my-claudecode:code-reviewer,
  prompt="projects/{slug}/ 코드 리뷰.
          CRITICAL/HIGH 이슈 발견 시 직접 수정. 수정 파일 목록 보고.")

# 4. 보안 검토 — 인증/외부 API/사용자 입력 처리가 있는 경우
if PRD includes "auth" OR "user input" OR "external API":
  Agent(oh-my-claudecode:security-reviewer,
    prompt="projects/{slug}/ OWASP Top 10 기준 보안 취약점 검토.
            CRITICAL 이슈 즉시 수정.")
```

**OMC_MODE != "omc"** 일 때 — 직접 구현:

Sprint 완료 체크리스트:
```
[ ] 컴파일/타입 오류 없음
[ ] 린트 오류 없음
[ ] 핵심 기능 동작 확인
[ ] 테스트 존재 (80%+ 커버리지 목표)
```

**구현 원칙**:
- **한국어 UI 필수**: 모든 사용자 대면 텍스트(버튼, 레이블, 메시지, 메뉴)를 한국어로 작성
- **기능 풍부성 필수**: 웹/앱 6개+ 화면, CLI 5개+ 커맨드. 검색·필터·빈 상태·에러 상태 포함
- Immutable 패턴
- Repository 패턴 (DB 접근 추상화)
- 명시적 에러 처리
- 컴포넌트/함수 200줄 이하

---

### 2-4. 자동 QA 루프 (핵심)

> 이 단계를 통과하지 못하면 프로젝트는 완성 처리하지 않는다.

**스택별 QA 명령:**

```bash
# 웹 / CLI (TypeScript)
npx tsc --noEmit && npm run lint && npm run build

# 앱 (Expo)
npx expo-doctor && npx tsc --noEmit

# CLI (Python)
python -m mypy . && python -m pytest

# CLI (Go)
go vet ./... && go build ./... && go test ./...

# CLI (Rust)
cargo check && cargo clippy && cargo test
```

**QA 루프 알고리즘:**

```
QA_ATTEMPTS = 0
MAX_QA_ATTEMPTS = 3

while QA_ATTEMPTS < MAX_QA_ATTEMPTS:
  result = run_qa_commands()

  if result.success:
    → QA 통과, Phase 2-5로 진행
    break

  QA_ATTEMPTS += 1
  errors = parse_errors(result.stderr)

  if QA_ATTEMPTS <= 2:
    # OMC_MODE에 따라 오류 수정 에이전트 선택
    if OMC_MODE == "omc":
      → Agent(oh-my-claudecode:debugger,
           prompt="다음 빌드 오류를 근본 원인부터 분석하고 수정하라:
                   {errors}
                   프로젝트: projects/{slug}/  스택: {TECH_STACK}")
    elif OMC_MODE == "ecc":
      → Agent(everything-claude-code:build-error-resolver, errors, context=프로젝트_소스코드)
    else:
      → Task(build-error-resolver, errors, context=프로젝트_소스코드)
    → 수정 후 재시도

  if QA_ATTEMPTS == 3 and not result.success:
    → 스코프 축소:
       PRD MoSCoW 테이블에서 SHOULD-have / COULD-have 항목을 전부 제거.
       Must-have 항목만 남기고 해당 기능의 소스 파일·라우트·컴포넌트를 삭제 또는 stub 처리.
       ROADMAP의 관련 Sprint 태스크도 동일하게 제거.
       (Must-have 정의: PRD MoSCoW 테이블의 'Must' 행에 명시된 항목만 해당)
    → 스코프 축소 후 executor에게 Must-have 기준 재구현 지시
    → 재구현 완료 후 최종 QA 1회 더 실행
    → 그래도 실패 시 SKIP 마킹 + report_data에 오류 기록

# QA 통과 후 — OMC_MODE == "omc" 이면 verifier로 기능 동작 최종 확인
if QA passed and OMC_MODE == "omc":
  Agent(oh-my-claudecode:verifier,
    prompt="projects/{slug}/ 핵심 기능이 실제로 동작하는지 검증.
            PRD Must-have 기능 체크리스트 기준. 실패 항목은 재현 방법과 함께 보고.")
```

**기능 풍부성 게이트 (빌드 통과 후 추가 검증):**

```
# QA 통과 후 기능 풍부성 체크 (자동)
FEATURE_GATE_PASS = true

if PLATFORM in ["웹", "앱"]:
  page_count = count_pages_or_screens(projects/{slug}/)
  has_search_or_filter = grep("검색|filter|search|필터", src/)
  has_empty_state = grep("빈 상태|empty|데이터가 없|아직", src/)
  has_dashboard = grep("대시보드|dashboard|통계|stats", src/)
  has_korean_ui = check_korean_ui_text(src/)

  if page_count < 6: FEATURE_GATE_PASS = false; reason = f"화면 {page_count}개 (최소 6개)"
  if not has_search_or_filter: FEATURE_GATE_PASS = false; reason += " | 검색/필터 없음"
  if not has_dashboard: FEATURE_GATE_PASS = false; reason += " | 대시보드 없음"
  if not has_korean_ui: FEATURE_GATE_PASS = false; reason += " | 영어 UI 텍스트 발견"

if PLATFORM == "CLI":
  cmd_count = count_commands(projects/{slug}/)
  has_table = grep("테이블|table|chalk|color", src/)
  has_korean_help = grep("한국어|description.*[가-힣]", src/)

  if cmd_count < 5: FEATURE_GATE_PASS = false; reason = f"커맨드 {cmd_count}개 (최소 5개)"
  if not has_table: FEATURE_GATE_PASS = false; reason += " | 테이블 출력 없음"

if not FEATURE_GATE_PASS:
  → executor에게 재작업 지시:
    "기능 풍부성 기준 미달: {reason}
     누락된 기능을 추가 구현하라. 기존 기능은 그대로 유지."
  → QA_ATTEMPTS 카운트에 포함하지 않고 재시도
```

QA 결과 출력:
```
━━━ QA 결과: {서비스명} ━━━
시도: {QA_ATTEMPTS}회  |  결과: ✅ 통과 / ❌ SKIP
기능 게이트: ✅ 통과 / ⚠️ 재작업 ({reason})
오류 타입: {오류 분류}
수정 내역: {수정된 파일 목록}
━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 2-5. README 자동 생성 (`projects/{slug}/README.md`)

QA 통과 후 즉시 생성.

**OMC_MODE == "omc"** 일 때:
```
Agent(oh-my-claudecode:writer,
  prompt="projects/{slug}/ README.md 작성.
          PRD + 실제 구현 내용 기반. 한국어 우선, 간결하고 기술적인 톤.
          포함: 서비스 소개(한국어), 주요 기능 목록(한국어 기능명),
          기술 스택 표, 설치/실행 방법, 스크린샷 섹션 자리.")
```

그 외 모드에서는 아래 템플릿을 직접 생성.

포함 내용:

```markdown
# {서비스명}

> {한 줄 설명 (한국어)}

## 주요 기능
- {핵심 기능 1 (한국어)}
- {핵심 기능 2 (한국어)}
- {핵심 기능 3 (한국어)}

## 기술 스택
| 레이어 | 기술 |
|--------|------|
| {레이어} | {기술} |

## 시작하기

### 필수 환경
{스택별 필수 환경 — Node 버전, Python 버전 등}

### 설치
```bash
{설치 명령}
```

### 실행
```bash
{실행 명령}
```

## 스크린샷
> _스크린샷 추가 예정_

## 라이선스
MIT
```

스택과 실제 구현된 기능 목록을 기반으로 내용을 동적으로 생성.

---

### 2-6. GitHub 저장소 생성 및 Push

**OMC_MODE == "omc"** 일 때:
```
Agent(oh-my-claudecode:git-master,
  prompt="projects/{slug}/ 을 새 GitHub 저장소 {slug}에 push.
          커밋 메시지: 'feat: initial implementation of {서비스명}'.
          저장소 설명: '{서비스 한 줄 설명}'.
          public 저장소. push 성공 후 URL 반환.")
```

그 외 모드에서는 아래 명령을 직접 실행:

```bash
gh repo create {slug} --public --description "{서비스 설명}"
git init && git add . && git commit -m "feat: initial implementation of {서비스명}"
git remote add origin https://github.com/{owner}/{slug}.git
git push -u origin main
```

Push 실패 시 최대 3회 재시도 (지수 백오프: 5s → 10s → 20s).

---

### 2-7. 완료 알림

프로젝트 1개 완료 시 macOS 알림 발송:

```bash
osascript -e 'display notification "{서비스명} 빌드 완료 ({현재번호}/{PROJECT_COUNT})" with title "auto-project-builder" sound name "Glass"'
```

Linux/WSL 환경이면 알림을 생략하고 터미널에만 출력.

```
✅ [{현재번호}/{PROJECT_COUNT}] {서비스명} 완료 — {GitHub URL}
```

---

### 2-8. 체크포인트 저장 + 컴팩션 트리거

매 프로젝트 완료 후 즉시 체크포인트 업데이트:

```json
{
  "run_date": "YYYYMMDDHHmm",
  "platform": "PLATFORM",
  "tech_stack": "TECH_STACK",
  "service_categories": [],
  "project_count": 5,
  "approved_ideas": [...],
  "completed_projects": ["slug-1", "slug-2"],
  "remaining_projects": ["slug-3", "slug-4", "slug-5"],
  "last_updated": "ISO 날짜"
}
```

```bash
# 저장
echo '{...}' > .auto-project-builder-checkpoint.json
```

**컴팩션 트리거 (3개 완료마다)**:

```
completed_count = len(CHECKPOINT.completed_projects)
if completed_count % 3 == 0 and completed_count > 0:
  → 체크포인트 파일이 최신 상태임을 확인
  → 사용자에게 출력:
    "━━━ 컨텍스트 절약 포인트 ━━━
     ✅ {completed_count}개 완료 / {PROJECT_COUNT - completed_count}개 남음
     체크포인트: .auto-project-builder-checkpoint.json
     지금 /compact 를 실행하면 컨텍스트를 압축하고 이어서 진행할 수 있습니다.
     (엔터 또는 아무 입력으로 계속 진행)"
  → 사용자 응답 대기 없이 자동으로 다음 프로젝트 진행
     (사용자가 /compact 를 실행하면 체크포인트에서 자동 재개됨)
```

> **재개 방법**: `/compact` 실행 후 `/auto-project-builder` 를 다시 실행하면
> 체크포인트를 감지하여 "이어서 진행" 선택 → 완료된 프로젝트 건너뜀.

전체 완료 시 체크포인트 파일 삭제:
```bash
rm .auto-project-builder-checkpoint.json
```

---

### 2-9. 진행 로그 기록 (`report_data/{slug}_log.json`)

```json
{
  "project": "slug",
  "platform": "PLATFORM",
  "tech_stack": "TECH_STACK",
  "category": "SERVICE_CATEGORY",
  "idea_score": { "market": 3, "originality": 2, "feasibility": 3, "total": 8 },
  "competitors": ["경쟁 서비스 1", "경쟁 서비스 2"],
  "differentiator": "차별점 설명",
  "idea_rationale": "선택 이유",
  "tech_decisions": ["결정사항과 이유"],
  "qa_attempts": 1,
  "qa_errors_fixed": ["수정된 오류 목록"],
  "challenges": ["겪은 문제들"],
  "solutions": ["해결 방법"],
  "github_url": "https://github.com/...",
  "completed_at": "ISO 날짜"
}
```

---

### 2-10. 프로젝트별 고도화 제안 수집

프로젝트 완료 직후 해당 프로젝트의 후속 작업과 고도화 전략을 생성하여 `projects/{slug}/user-suggest.html`에 저장한다.
각 프로젝트마다 독립된 파일로 생성되며, 5개 프로젝트이면 5개의 개별 파일이 만들어진다.

**생성 항목:**

```
per_project_suggestion = {
  "slug": slug,
  "name": 서비스명,
  "tech_stack": TECH_STACK,
  "platform": PLATFORM,
  "github_url": GitHub URL,
  "completed_at": ISO 날짜,

  # 즉시 할 수 있는 후속 작업 (단기 — 1~2주)
  "quick_wins": [
    "사용자 피드백 수집을 위한 간단한 설문 폼 추가",
    "랜딩 페이지 / 소개 페이지 작성 및 Product Hunt 등록",
    "기본 분석 (GA4 or Plausible) 연동",
    "실제 사용자 3명에게 베타 테스트 요청",
    ...  # PRD Must-have 기능 기반으로 구체화
  ],

  # 기능 고도화 전략 (중기 — 1~3개월)
  "feature_enhancements": [
    {
      "title": "기능명",
      "description": "구체적 구현 방향",
      "priority": "high | medium | low",
      "effort": "small | medium | large"
    },
    ...  # PRD Nice-to-have + 경쟁 서비스 분석에서 도출
  ],

  # 기술 부채 / 리팩토링 (중기)
  "tech_improvements": [
    "테스트 커버리지 80% → 95% 향상",
    "SQLite → PostgreSQL 마이그레이션 가이드",
    "CI/CD 파이프라인 구축 (GitHub Actions)",
    ...  # QA 과정에서 발견한 이슈 기반으로 구체화
  ],

  # 성장 전략 (장기 — 3~6개월)
  "growth_strategies": [
    {
      "title": "전략명",
      "description": "구체적 실행 방법",
      "expected_impact": "예상 효과"
    },
    ...  # 경쟁 분석 + 시장 트렌드 기반으로 도출
  ],

  # 수익화 아이디어
  "monetization_ideas": [
    "프리미엄 플랜 (기능 제한 / 용량 제한)",
    "팀 플랜 (협업 기능 추가)",
    ...  # 서비스 유형·타겟 사용자 기반으로 현실적인 아이디어
  ]
}
```

**OMC_MODE = "omc"** 일 때:
```
Agent(oh-my-claudecode:planner,
  prompt="projects/{slug}/ 의 PRD, 구현 내용, QA 결과, 경쟁 분석을 기반으로
          단기 후속 작업(quick_wins), 기능 고도화(feature_enhancements),
          기술 개선(tech_improvements), 성장 전략(growth_strategies),
          수익화 아이디어(monetization_ideas)를 각 항목별로 3~5개씩 구체적으로 작성하라.
          현실적이고 실행 가능한 내용만 포함. 추상적 문구 금지.")
```

그 외 모드에서는 PRD + 구현 내용 + 경쟁 분석을 직접 분석하여 생성.

생성된 데이터를 `report_data/{slug}_suggestions.json`에 저장하고, `projects/{slug}/user-suggest.html`을 생성/갱신한다.

---

## Phase 3: 보고서 생성

모든 프로젝트 완료 후 세 파일을 생성/업데이트.

### 3-1. 날짜별 리포트: `{RUN_DATE}_report.html`

`RUN_DATE` = 실행 시작 날짜+시간 (YYYYMMDDHHmm, 예: `202605242157_report.html`)

> **같은 날 여러 번 실행해도 파일이 덮어쓰이지 않는다.** 분 단위까지 포함하므로 실행마다 고유한 파일명이 생성된다.

**보고서 구성** (한국어):

#### 섹션 1: 실행 요약 대시보드
- 실행 날짜, 플랫폼, 기술 스택, 서비스 유형, 총 프로젝트 수
- 완료/스킵/QA 재시도 현황
- 트렌드 조사 요약 (`TREND_DATA`)

#### 섹션 2: 아이디어 선정 배경
- 트렌드 조사 결과 요약 (시장 갭, 인기 기능)
- 평가 점수별 아이디어 분포 (통과/탈락 사유 포함)
- GitHub 중복 검토 결과
- 최종 선정 순위 (점수 기준)

#### 섹션 3: 프로젝트별 상세 보고 (PROJECT_COUNT개)

각 프로젝트 카드:
```
┌─ 프로젝트 N: {서비스명}  [{PLATFORM} / {TECH_STACK}]
│
│  [아이디어 배경]
│  ├─ 해결하는 고통: {pain_statement}
│  ├─ 실제 증거: "{pain_evidence[0]}" / "{pain_evidence[1]}"
│  ├─ 타겟 사용자: {target_user}
│  └─ 지금 만들어야 하는 이유: {why_now}
│
│  [서비스 내용]
│  ├─ 핵심 솔루션: {solution}
│  ├─ 경쟁 서비스: {competitors}
│  └─ 차별점: {differentiator}
│
│  [주요 기능]
│  ├─ 킬러 기능: {core_features[0]}
│  ├─ {core_features[1]}
│  ├─ {core_features[2]}
│  └─ {core_features[3]} (있는 경우)
│
│  [구현 결과]
│  ├─ 아이디어 평가: 페인 {P}/3 · 시장 {M}/3 · 독창성 {O}/3 · 구현 {F}/3 · 결함 {X} = {T}/15  {verdict}
│  ├─ 기술적 결정사항: {tech_stack 선택 근거}
│  ├─ QA 결과: {시도 횟수}회, 수정된 오류 목록
│  └─ GitHub: {URL}  |  빌드: ✅ 성공
└─
```

#### 섹션 4: 전체 회고
- QA 공통 오류 패턴 (어떤 오류가 자주 발생했는지)
- 잘 된 점 / 아쉬운 점
- 다음 실행 개선점

---

**⚠️ 필수 실행: 보고서 파일 생성 알고리즘 (절대 생략 불가)**

> `{RUN_DATE}_report.html` 파일을 디스크에 실제로 저장하는 것은 Phase 3의 **가장 첫 번째 의무**다.
> overview.html 업데이트 전에 반드시 먼저 완료해야 한다.
> 이 단계를 건너뛰면 Phase 3 전체가 실패로 간주된다.

```
1. RUN_DATE 확인
   → Phase -1에서 이미 캡처됨. 없으면 즉시 캡처: RUN_DATE=$(date +%Y%m%d%H%M)

2. report_data/ 디렉토리의 모든 {slug}_log.json 읽기
   → PROJECT_LOG[] 재구성 (없으면 이번 세션의 PROJECT_LOG[] 사용)

3. 위 섹션 1~4 구조로 완전한 HTML 작성
   스타일: Tailwind CDN + 현대적 카드 레이아웃 (기존 overview.html / *_report.html 스타일 참고)
   언어: 한국어
   내용: 실행된 모든 프로젝트 데이터를 실제 값으로 채움 (플레이스홀더 금지)

4. 파일 저장 (Write 도구 또는 bash heredoc 사용):
   경로: ./{RUN_DATE}_report.html  (작업 디렉토리 루트)

5. 저장 확인:
   ls -la {RUN_DATE}_report.html
   → 파일이 없거나 크기가 1KB 미만이면 즉시 재생성
```

---

### 3-2. overview.html 갱신

> **⚠️ overview.html은 절대 덮어쓰지 않는다.**
> 파일이 없으면 새로 생성하고, 있으면 **기존 내용을 보존하면서 이번 실행 결과만 추가**한다.
> 이전 실행의 프로젝트 카드, 실행 이력, 통계는 절대 삭제하거나 초기화하지 않는다.

**목적**: 모든 실행 이력과 전체 프로젝트 현황을 한 파일에 누적하여 언제든 전체 진행 상황을 한눈에 파악할 수 있게 한다.

**구조**:

```html
<!-- overview.html 레이아웃 -->
헤더: "Project Overview — 전체 프로젝트 현황"

[실행 이력 타임라인]  ← 새 실행 항목이 맨 위에 추가됨 (기존 항목 유지)
  ├─ 2026-05-24 21:57  |  웹 / Next.js  |  10개  |  QA 통과율 100%  →  링크
  ├─ 2026-05-23 15:30  |  웹 / Next.js  |  5개   |  QA 통과율 100%  →  링크
  └─ ...

[전체 프로젝트 카탈로그]  ← 새 프로젝트 카드가 기존 카드 앞에 추가됨 (기존 카드 유지)
  플랫폼별 / 유형별 / 점수별 필터 UI
  각 프로젝트 카드:
    - 서비스명, 플랫폼, 스택, 카테고리, 아이디어 평가 점수
    - GitHub URL 링크
    - 실행 날짜, QA 시도 횟수

[통계 대시보드]  ← 전체 누적 데이터 기반으로 재계산
  - 총 프로젝트 수 (누적)
  - 플랫폼 분포 차트
  - 카테고리 분포 차트
  - 기술 스택 사용 빈도
  - 평균 QA 재시도 횟수
  - 평균 아이디어 점수
```

**업데이트 알고리즘 (추가 전용 — append-only)**:

```
1. overview.html 파일 존재 여부 확인
   - 없으면: 빈 템플릿으로 신규 생성 후 3단계로 진행
   - 있으면: 파일 전체 읽기 (기존 내용 메모리에 보존)

2. 기존 프로젝트 카드 목록 추출 (<!-- PROJECT_CARDS_START --> ~ <!-- PROJECT_CARDS_END --> 사이)
   → 이 내용은 절대 수정하지 않음

3. 이번 실행의 PROJECT_LOG[] 기반으로 새 프로젝트 카드 HTML 생성
   → 기존 카드 목록 맨 앞에 새 카드들을 삽입 (기존 카드는 뒤에 그대로 유지)

4. 기존 실행 이력 타임라인 추출 (<!-- TIMELINE_START --> ~ <!-- TIMELINE_END --> 사이)
   → 새 실행 항목을 맨 위에 추가 (기존 항목은 아래에 그대로 유지)
   → 항목 형식: {RUN_DATE} | {PLATFORM} / {TECH_STACK} | {PROJECT_COUNT}개 | QA {통과율}% → {RUN_DATE}_report.html 링크

5. 전체 통계 재계산 (기존 + 신규 데이터 합산)
   → 총 프로젝트 수 = 기존 수 + 이번 실행 수
   → 평균 점수 = 전체 프로젝트 점수의 평균
   → 카테고리/플랫폼 분포 = 전체 기준으로 재산출

6. 업데이트된 전체 HTML 저장
```

> **마커 규칙**: 신규 생성 시 반드시 아래 마커를 포함시켜 후속 업데이트가 정확한 위치를 찾을 수 있게 한다:
> - `<!-- PROJECT_CARDS_START -->` / `<!-- PROJECT_CARDS_END -->`
> - `<!-- TIMELINE_START -->` / `<!-- TIMELINE_END -->`
> - `<!-- STATS_TOTAL -->`, `<!-- STATS_AVG_SCORE -->` (숫자 인라인 마커)

**스타일**: 현대적 HTML+CSS (Tailwind CDN), 다크/라이트 모드 지원, 카드형 레이아웃, 인쇄 가능.

---

### 3-3. user-suggest.html 생성 (프로젝트별 독립 파일)

`projects/{slug}/user-suggest.html`은 **해당 프로젝트 전용 실행 가이드**다.
Phase 2-10에서 프로젝트 완료 직후 즉시 생성되며, 프로젝트마다 별도의 파일로 만들어진다.
5개 프로젝트 → 5개의 독립된 `user-suggest.html` 파일.

**구조**:

```html
<!-- projects/{slug}/user-suggest.html 레이아웃 -->
헤더: "{서비스명} — 다음 단계 가이드"
부헤더: "[{PLATFORM} / {TECH_STACK}]  GitHub 링크 ↗  완료일: {completed_at}"

  ⚡ Quick Wins — 지금 바로 할 수 있는 것 (1~2주)
    □ {quick_win_1}
    □ {quick_win_2}
    □ ...

  🚀 기능 고도화 (1~3개월)
    ┌ [우선순위: high] {기능명} — {설명} / 난이도: {effort}
    ├ [우선순위: medium] ...
    └ ...

  🔧 기술 개선 사항
    • {tech_improvement_1}
    • {tech_improvement_2}
    • ...

  📈 성장 전략 (3~6개월)
    ┌ {전략명}: {설명}
    │  → 예상 효과: {expected_impact}
    └ ...

  💰 수익화 아이디어
    • {monetization_idea_1}
    • ...
```

**생성 방법**:
1. `report_data/{slug}_suggestions.json` 읽기
2. 위 구조의 HTML을 새로 생성하여 `projects/{slug}/user-suggest.html`로 저장
3. 기존 파일이 있으면 덮어쓴다

**스타일**: 현대적 HTML+CSS (Tailwind CDN), 다크/라이트 모드 지원, 체크박스 인터랙션(JS), 인쇄 가능.

---

## Agent 위임 전략

`OMC_MODE` 값에 따라 아래 전략 중 하나를 선택한다.

---

### OMC_MODE = "none" (기본 내장 에이전트)

```
# PRD 작성 + 프로젝트 초기화 병렬
Task(planner/sonnet,  "PRD 작성 → projects/{slug}/PRD.md
                       포함: 페르소나, MoSCoW 기능 목록, 데이터 모델, 한국어 UI 가이드") ||
Task(executor/haiku,  "프로젝트 디렉토리 초기화")

# PRD 완료 후 ROADMAP 작성
Task(architect/sonnet, "ROADMAP 작성 (PRD 기반) → projects/{slug}/ROADMAP.md
                        Sprint 번호·목표·완료 기준 명시, DB 스키마, 컴포넌트 구조도 포함")

# ROADMAP 기반 구현 → 코드 리뷰
Task(executor/sonnet,  "projects/{slug}/ROADMAP.md 읽고 Sprint 순서대로 구현") →
Task(code-reviewer/sonnet, "코드 리뷰")

# QA 루프 — 오류 수정
Task(build-error-resolver/sonnet, "빌드 오류 수정", errors=QA_ERRORS)

# 복잡한 아키텍처 검토
Task(architect/opus, "DB 스키마 설계 검토")
```

---

### OMC_MODE = "omc" (oh-my-claudecode 최적화)

OMC가 감지되면 아래 스킬 조합을 사용한다. 각 스킬은 `Skill` 도구로 호출하거나 서브에이전트로 위임한다.

#### Phase 0-B: 트렌드 조사

```
# WebSearch / Exa로 직접 조사 (autoresearch는 반복 개선 루프이므로 웹 리서치에 사용하지 않음)
WebSearch("site:producthunt.com {SERVICE_CATEGORIES} {PLATFORM} app 2025 2026")
WebSearch("github trending {TECH_STACK_KEYWORD} repositories 2025")
WebSearch("{SERVICE_CATEGORIES} best apps 2025 market trends")
```

#### Phase 1: 아이디어 기획 — `idea-generator` 스킬 위임

Phase 1 전체를 `idea-generator` 스킬에 위임한다.
내부적으로 **멀티소스 페인 마이닝 + planner · architect · critic 3역할 병렬 평가 + YC 스코어카드**를 수행하며,
단순 트렌드 조사 기반 아이디어 생성보다 훨씬 높은 품질의 결과를 낸다.

```
Skill("idea-generator", context={
  "PLATFORM": PLATFORM,
  "SERVICE_CATEGORIES": SERVICE_CATEGORIES,
  "TREND_DATA": TREND_DATA,        # Phase 0-B 결과 전달
  "PROJECT_COUNT": PROJECT_COUNT,
  "TECH_STACK": TECH_STACK,
  "OMC_MODE": OMC_MODE
})
# 결과: IDEAS[] — 각 아이디어에 pain_evidence[], score{total/15}, verdict, fatal_flaws[] 포함
→ Phase 1.3 아이디어 평가 결과 확인으로 진행
```

#### Phase 2 전체: autopilot 자율 오케스트레이션 (선택 옵션)

기획 결과를 바탕으로 **Phase 2 전체를 사람 개입 없이 완전 자율 실행**하고 싶을 때 사용한다.
autopilot은 아이디어부터 동작하는 코드까지 전체 파이프라인을 조율한다.
(ultrawork는 병렬 실행 컴포넌트이며 완전 파이프라인이 아니다 — 풀 파이프라인에는 autopilot을 사용한다)

```
Skill("oh-my-claudecode:autopilot",
  prompt="{PROJECT_COUNT}개 프로젝트를 아래 사양으로 처음부터 끝까지 완성하라.

  프로젝트 목록 (각 항목: slug | 서비스명 | 한 줄 설명):
  {APPROVED_IDEAS}

  공통 사양:
  - PLATFORM: {PLATFORM}
  - TECH_STACK: {TECH_STACK}
  - PRD 출력 경로: projects/{slug}/PRD.md
  - ROADMAP 출력 경로: projects/{slug}/ROADMAP.md

  완료 기준 (모든 항목 충족 필수):
  1. tsc --noEmit / lint / build 오류 0개
  2. 테스트 커버리지 80% 이상
  3. README.md 생성 완료
  4. GitHub 저장소 push 완료 (URL 반환)
  5. PRD Must-have 기능 전부 동작 확인

  단계 순서: PRD → ROADMAP → 구현 → QA → README → Push
  각 프로젝트는 독립적으로 병렬 실행 가능하면 병렬로 처리하라.")
```

autopilot을 사용하지 않는 경우(기본값)에는 `_run_omc_pipeline` 함수(Phase 2 루프 섹션)가 실행된다.

> **Phase 2-1 ~ 2-6 상세 에이전트 프롬프트 및 요구 사항 명세는**
> **Phase 2 루프 내 `_run_omc_pipeline` 코드 블록을 참조한다.**
> 본 "Agent 위임 전략" 섹션과 `_run_omc_pipeline`이 상충하면 **`_run_omc_pipeline`이 우선한다.**

#### 품질 반복 개선 — ralph 루프

ralph는 PRD 기반의 검증 루프를 돌려 **모든 acceptance criteria가 통과할 때까지** 자동으로 반복한다.

**자동 적용 조건** (아래 중 하나 이상):
- `QA_ATTEMPTS >= 2` (빌드 오류가 많았던 프로젝트)
- `IDEA_SCORE.total <= 6` (저점 아이디어)
- 코드 리뷰에서 HIGH 이상 이슈가 3개 이상 발견된 경우

**선택적 적용**: 모든 완료 프로젝트에 ralph를 돌려 전체 품질을 균일하게 높일 수 있다.

```
Skill("oh-my-claudecode:ralph",
  prompt="projects/{slug}/ 의 품질을 아래 acceptance criteria 기준으로 완성하라.

  Acceptance Criteria:
  1. 테스트 커버리지 80% 이상 (jest/pytest/go test 기준)
  2. tsc --noEmit / lint / build 오류 0개
  3. 모든 에러 경계에서 명시적 에러 처리 존재
  4. 함수/컴포넌트 200줄 이하 준수
  5. PRD Must-have 기능 전부 동작 확인

  작업 우선순위:
  1. 누락된 테스트 추가 (커버리지 목표 달성)
  2. 에러 처리 보완 (silent failure 제거)
  3. 코드 가독성 개선 (함수 분리, 네이밍)
  4. 빌드/타입 오류 수정

  제약: 기존 기능 동작 유지. 스코프 확장 금지.")
```

ralph는 위 criteria가 모두 통과할 때까지 자동으로 반복 실행한다. 통과 후 자동 종료.

---

### OMC_MODE = "ecc" (everything-claude-code 최적화)

`oh-my-claudecode`는 없고 `everything-claude-code` 스킬만 있을 때 사용.

```
# 트렌드 조사
Agent(everything-claude-code:market-research, "SERVICE_CATEGORIES 시장 조사")

# PRD 작성 — prp-prd 스킬 사용 (ECC 전용 PRD 작성기)
Agent(everything-claude-code:prp-prd,
  prompt="아이디어: {IDEA}. 플랫폼: {PLATFORM}, 스택: {TECH_STACK}.
          Must-have 기능 웹/앱 8개+, CLI 6개+. 한국어 UI 텍스트 가이드 포함.
          출력 경로: projects/{slug}/PRD.md")

# ROADMAP 작성 — PRD 기반 아키텍처 설계
Agent(everything-claude-code:architect,
  prompt="PRD(projects/{slug}/PRD.md) 기반 기술 아키텍처 설계.
          스택: {TECH_STACK}.
          Sprint 번호·목표·완료 기준 명시, DB 스키마, 컴포넌트 구조도 포함.
          출력 경로: projects/{slug}/ROADMAP.md")

# 구현 — ROADMAP Sprint 순서 준수
Agent(everything-claude-code:feature-dev,
  prompt="projects/{slug}/ROADMAP.md를 읽고 Sprint 번호 순서대로 구현 (TDD 포함).
          한국어 UI 필수. ROADMAP Sprint 완료 기준 충족 후 다음 Sprint 진행.")

# 리뷰 (병렬)
Agent(everything-claude-code:code-review, "코드 품질 검토") ||
Agent(everything-claude-code:security-review, "보안 취약점 검토")

# 기능 검증 — PRD Must-have 기준
Agent(everything-claude-code:verify,
  prompt="projects/{slug}/PRD.md의 Must-have 기능이 모두 동작하는지 검증.")

# 문서
Agent(everything-claude-code:docs, "README + 기술 문서 생성")

# 스택별 빌드 오류
Agent(everything-claude-code:build-error-resolver, errors=QA_ERRORS)
```

---

## 폴백 전략

```
오류 발생
  ├─ 1차: build-error-resolver 에이전트 위임 (최대 5분)
  ├─ 2차: build-error-resolver 재시도 (스코프 축소 힌트 포함)
  ├─ 3차: 스코프 축소 (Nice-to-have 제거 후 재구현 + QA 1회)
  └─ 4차: SKIP 마킹 + report_data에 오류 상세 기록 후 다음으로 진행
```

GitHub push 실패 시 최대 3회 재시도 (지수 백오프 5s→10s→20s).

---

## 파일 구조

```
{작업 디렉토리}/
├── projects/
│   └── {slug}/
│       ├── PRD.md                   ← Phase 2-1: 기획 문서 (먼저 작성)
│       ├── ROADMAP.md               ← Phase 2-2: 기술 로드맵 (PRD 기반, 구현 전 작성)
│       ├── README.md                ← Phase 2-5: 자동 생성
│       ├── user-suggest.html        ← Phase 2-10: 프로젝트 전용 후속 작업 & 고도화 전략 가이드
│       └── ... (소스 코드)          ← Phase 2-3: ROADMAP Sprint 순서대로 구현
├── report_data/
│   ├── {slug}_log.json              ← 프로젝트별 빌드 로그
│   └── {slug}_suggestions.json     ← 프로젝트별 고도화 제안 원본
├── .auto-project-builder-checkpoint.json  ← 실행 중 존재, 완료 시 삭제
├── {YYYYMMDDHHmm}_report.html       ← 이번 실행 보고서 (시분 포함으로 같은 날 여러 번 실행해도 덮어쓰지 않음)
└── overview.html                    ← 전체 누적 현황
```

---

## 실행 예시

```
# 기본 실행 (인터랙티브 설정 시작)
/auto-project-builder

# 인터랙티브 대화 예시:
> 이전 체크포인트 발견 → "새로 시작" 선택
> 어떤 플랫폼? → 웹
> 기술 스택?   → Next.js 14+ · shadcn/ui · SQLite
> 서비스 유형? → 생산성, 교육
> 몇 개?       → 3
→ Phase 0: Context7 + 트렌드 조사 병렬 실행
→ Phase 1: 아이디어 3개 생성 + 경쟁 분석
→ Phase 1.3: 점수화 (탈락 시 재생성)
→ Phase 1.5: GitHub 중복 검토
→ Phase 2×3: 빌드 → QA 루프 → README → Push → 알림 → 체크포인트

# 자연어로도 가능 (인터랙티브 질문 건너뛰고 파싱)
"CLI 프로젝트 2개 개발자 도구로 만들어줘"
"웹앱 5개 커머스 관련으로 자율 빌드"
```

## 주의사항

- SQLite DB 파일 `.gitignore` 추가 (`*.db`, `*.sqlite`)
- `.env.local` `.gitignore` 추가, `.env.example` 커밋
- `overview.html`은 누적 파일 — 절대 삭제하거나 전체를 교체하지 않음. 항상 기존 내용 보존 + 새 내용 추가만 허용
- `{RUN_DATE}_report.html` 파일명에 시분(HHmm)이 포함되므로, 같은 날 여러 번 실행해도 파일이 덮어쓰이지 않음 (예: `202605242157_report.html`)
- `RUN_DATE`는 **Phase -1 시작 즉시** `date +%Y%m%d%H%M` 형식으로 캡처 — 이후 절대 변경하지 않음 (예: `202605242157`)
- `.auto-project-builder-checkpoint.json`은 실행 중에만 존재 — 완료 시 자동 삭제
