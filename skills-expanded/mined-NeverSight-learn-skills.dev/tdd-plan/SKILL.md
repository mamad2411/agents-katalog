---
name: tdd-plan
description: >
  Use this skill when the user says "tdd plan", "plan tdd", "start tdd session",
  "TDD 플랜", "TDD 세션 시작", or wants to plan a TDD session for a story.
  Fetches a story from TrackerBoot MCP or accepts pasted content, detects the tech stack
  and conventions, plans task decomposition, and writes the .tdd-sessions/ file.
---

# TDD Plan

## Invocation

```
/tdd-plan <project-id> <story-id>
/tdd-plan <project-id> "full story content"
```

- **`project-id`** — TrackerBoot 프로젝트 ID **(필수)**
- **`story-id`** — TrackerBoot 스토리 ID (숫자형, 예: `12345678` 또는 `#12345678`) → MCP를 통해 가져오기
- **`"full story content"`** — 스토리 텍스트를 직접 붙여넣기 → 직접 사용
- **project-id 없음** → 오류를 표시하고 중지: "프로젝트 ID가 필요합니다. TrackerBoot 프로젝트 ID를 첫 번째 인수로 제공하세요."
- **story-id/content 없음** → 오류를 표시하고 중지: "스토리가 필요합니다. TrackerBoot 스토리 ID를 제공하거나 스토리 내용을 붙여넣으세요."

---

## Step 1: 스토리 불러오기

### 인수 검증

호출 시 `project-id`와 `story-id` (또는 스토리 텍스트)가 모두 제공되었는지 확인한다.

**`project-id`가 없으면 즉시 중단:**

```
❌ TrackerBoot 프로젝트 ID가 필요합니다.

프로젝트 ID 없이 실행하면 권한이 있는 임의의 프로젝트에서 스토리를 조회할 수 있습니다.

사용법: /tdd-plan <project-id> <story-id>
        /tdd-plan <project-id> "스토리 내용"
예시:   /tdd-plan 99887766 12345678
```

STOP.

**`story-id` 또는 스토리 텍스트가 없으면 즉시 중단:**

```
❌ 스토리가 필요합니다.

TrackerBoot 스토리 ID를 제공하거나 스토리 내용을 붙여넣으세요.

사용법: /tdd-plan <project-id> <story-id>
        /tdd-plan <project-id> "스토리 내용"
```

STOP.

**모두 제공되었으면:** `project-id`를 세션 전체에서 사용할 값으로 저장한다.

### 스토리 ID가 제공된 경우

`tracker-boot-mcp-tb_get_story` 도구를 사용하여 스토리를 페치합니다:

```json
{
  "storyId": 12345678
}
```

호출 전 앞에 있는 `#`을 제거합니다 (`#12345678` → `12345678`).

응답에서 추출:
- **제목:** `name` 필드
- **설명:** `description` 필드
- **인수 기준:** `tasks[]` 배열 (권장) 또는 설명의 "Acceptance Criteria:" 섹션 파싱
- **상태:** `current_state` 필드

**MCP 도구를 찾을 수 없거나 호출이 실패한 경우:**
```
"Could not fetch story [ID] from TrackerBoot.
Please check that the TrackerBoot MCP server is configured, then try again,
or paste the story content directly."
```
**중지 — 진행하지 마십시오.**

### 스토리 내용을 붙여넣은 경우

직접 파싱 — 텍스트에서 제목, 설명, 인수 기준을 추출합니다.

### 개발자에게 확인

스토리를 표시하고 일시 정지:

```markdown
## Story

**ID:** [id or "—"]
**Title:** [title]

**Description:**
[description]

**Acceptance Criteria:**
- [ ] [AC 1]
- [ ] [AC 2]
...

---
Does this look correct? Type "ok" to continue, or let me know what to fix.
```

"ok" / "yes" / "looks good"를 기다립니다. 수정 사항이 있으면 적용하고 다시 표시합니다.

---

## Step 2: 기술 스택 감지

프로젝트 루트 파일을 읽고 다음 규칙을 순서대로 적용합니다:

| 파일 존재 | 스택 |
|-------------|-------|
| 의존성에 `"react"`가 있는 `package.json` | TypeScript + React |
| kotlin 플러그인이 있는 `build.gradle.kts` | Kotlin + Spring |
| `build.gradle` (.kts 아님) + `src/main/java/` | Java + Spring |
| `pom.xml` + `src/main/java/` | Java + Spring (Maven) |
| `fastapi`가 있는 `pyproject.toml` 또는 `requirements.txt` | Python + FastAPI |

TypeScript의 경우, devDependencies도 확인:
- `"vitest"` → 단위 테스트 FW: Vitest
- `"jest"` → 단위 테스트 FW: Jest
- `"@playwright/test"` 또는 `playwright.config.*` → E2E: Playwright
- `"cypress"` → E2E: Cypress

모호한 경우: "감지된 후보: [목록]. 어떤 스택으로 작업하고 있나요?"
감지되지 않은 경우: "스택을 감지할 수 없습니다. 다음 중 하나를 지정하세요: typescript-react / kotlin-spring / java-spring / python-fastapi"

전체 감지 규칙은 `.agents/skills/tdd-plan/references/tech-stack-detection.md`를 참조하세요.

---

## Step 3: 프로젝트 컨벤션 감지

**기존 테스트 또는 소스 파일이 없는 경우(새 프로젝트) 이 단계를 건너뜁니다.**

스토리와 같은 영역에서 테스트 파일 2~3개와 소스 파일 1~2개를 읽습니다. 최근 수정된 파일을 선호합니다.

추출:
- 테스트 파일 위치 (동일 위치 vs `test/` 디렉토리)
- 테스트 파일 명명 접미사 (`*.test.ts`, `*Test.kt`, `test_*.py`)
- 테스트 구조 (describe/it 중첩, `@Nested`, 클래스 기반)
- 어서션 라이브러리 및 스타일
- 목 패턴 (vi.mock, vi.fn injection, mockk, @MockBean, MagicMock)
- 소스 파일의 의존성 주입 패턴
- 명명 컨벤션 (접미사, 대소문자)

간략한 요약을 표시합니다 (일시 정지 없음 — 정보 제공 목적):

```markdown
## Project Conventions Detected

Files read: [file list]

- **Test location:** [co-located / test/ directory]
- **Test naming:** [pattern]
- **Test structure:** [describe/it / @Nested / class-based]
- **Assertions:** [expect().toEqual / assertThat / assert ==]
- **Mocks:** [vi.mock / vi.fn injection / mockk / MagicMock]
- **Source structure:** [feature-based / layer-based]

All new code will follow these patterns.
```

전체 컨벤션 규칙은 `.agents/skills/tdd-plan/references/convention-detection.md`를 참조하세요.

---

## Step 4: 태스크 분해 제안

세션 상태를 표시한 후 태스크를 제안합니다:

```markdown
---
## 🏓 Session State
| Field | Value |
|-------|-------|
| Story | [ID]: [title] |
| Stack | [stack] |
| Test FW | [test framework] |
| E2E FW | [e2e framework] |
| Conventions | [new project / existing — key patterns] |
| Phase | PLANNING |
---

## Task Plan (Draft)

### Task List

#### Task 1: [title]
- **Type:** unit | integration | e2e
- **The test will assert:** [one sentence]
- **Implementation scope:** [what code will be written]
- **Acceptance criteria link:** [which ACs]
- **Dependencies:** none

#### Task 2: [title]
...

#### Task [N] (E2E): [title]
- **Type:** e2e
- **The test will assert:** [full user flow]
- **Implementation scope:** E2E test only
- **Acceptance criteria link:** Full AC coverage check
- **Dependencies:** Task [N-1]

---
**Questions for clarification:**
1. [ambiguity or scope question]

---
Please review. You can add, remove, reorder, or adjust tasks.
Type **"ready"**, **"go"**, or **"approved"** when satisfied.
```

### 태스크 순서 결정 기준
1. 도메인/서비스 레이어 우선 (순수 로직, 단위 테스트하기 가장 쉬움)
2. 레포지토리/데이터 레이어 두 번째 (영속성)
3. API/컨트롤러 레이어 세 번째 (HTTP 인터페이스)
4. E2E 마지막 (전체 흐름 검증)

### 피드백 후

태스크 목록을 업데이트하고 다시 표시합니다. 트리거 문구를 받을 때까지 반복합니다:
`ready` / `go` / `approved` / `looks good`

---

## Step 5: 세션 파일 작성

### 세션 파일 경로 결정

세션 파일은 프로젝트 루트의 `.tdd-sessions/`에 저장됩니다. 파일 이름은 스토리 ID를 기반으로 합니다:

| 상황 | 파일 이름 |
|-----------|----------|
| 스토리 ID 사용 가능 (예: `12345678`) | `.tdd-sessions/12345678.md` |
| 스토리 ID 없음 (붙여넣은 내용) | `.tdd-sessions/{title-slug}-{YYYY-MM-DD}.md` |

**제목 슬러그:** 소문자, 공백 및 특수 문자는 하이픈으로 대체, 최대 40자.
예: "User Profile Update" → `user-profile-update` → `.tdd-sessions/user-profile-update-2026-03-31.md`

### `.tdd-sessions/`를 `.gitignore`에 추가

세션 파일을 작성하기 전에:

1. 프로젝트 루트에 `.gitignore`가 존재하는지 확인
2. `.tdd-sessions/` (또는 `.tdd-sessions`)가 이미 목록에 있는지 확인
3. 목록에 없는 경우:
   - `.gitignore`가 존재하는 경우: 파일에 `.tdd-sessions/` 줄을 추가
   - `.gitignore`가 존재하지 않는 경우: `.tdd-sessions/`를 단일 항목으로 포함하여 생성
4. 표시: "`.tdd-sessions/`를 `.gitignore`에 추가했습니다" (또는 "`.tdd-sessions/`가 이미 `.gitignore`에 있습니다")

### 세션 파일 작성

`.tdd-sessions/` 디렉토리가 없으면 생성한 후 파일을 작성합니다:

```markdown
# TDD Session

## Meta
- **Story ID:** [id or "—"]
- **Story Title:** [title]
- **Stack:** [stack]
- **Test FW:** [framework]
- **E2E FW:** [framework]
- **Conventions:** [summary line]

## Tasks
| # | Title | Type | Status |
|---|-------|------|--------|
| 1 | [title] | unit | ⏳ pending |
| 2 | [title] | integration | ⏳ pending |
| 3 | [title] | e2e | ⏳ pending |

## Task Details

### Task 1: [title]
- **Type:** unit
- **The test will assert:** [assertion description]
- **Implementation scope:** [scope]
- **Acceptance criteria link:** [AC reference]
- **Dependencies:** none
- **Status:** ⏳ pending

### Task 2: [title]
...
```

그런 다음 표시:

```markdown
## ✅ Session Ready

`.tdd-sessions/[filename]` created with [N] tasks.

Run **/tdd-task** to start Task 1.
```
