---
name: tdd-task
description: >
  Use this skill when the user says "tdd task", "next tdd task", "run tdd",
  "TDD 태스크", "다음 태스크", or wants to run a TDD RED-GREEN-REFACTOR cycle.
  Reads the active .tdd-sessions/ file, finds the current pending task,
  and runs the full ping-pong TDD cycle with the developer.
---

# TDD Task

## Invocation

```
/tdd-task [story-id]
```

- **인수 없음** — `.tdd-sessions/`에서 활성 세션 파일을 자동 감지
- **스토리 ID 제공** — `.tdd-sessions/{story-id}.md`를 직접 사용

---

## 시작 시: 세션 파일 찾기

### 인수 없이

1. `.tdd-sessions/`의 파일 목록 나열
2. **디렉토리가 존재하지 않거나 비어 있는 경우:**
   ```
   "No active TDD session found. Run /tdd-plan first to create a session."
   ```
   중지.
3. **파일이 정확히 하나만 있는 경우:** 해당 파일 사용
4. **여러 파일이 있는 경우:**
   ```
   "Multiple sessions found. Which story are you working on?
   [1] 12345678.md — User Profile Update
   [2] user-profile-update-2026-03-31.md — (no ID)
   Type the number or story ID."
   ```
   일시 정지하고 선택을 기다립니다.

### 파일을 찾은 후

세션 파일을 읽습니다. **모든 태스크가 이미 ✅ 완료된 경우:**
```
"All tasks in this session are complete. Run /tdd-commit to review and commit."
```
중지.

상태가 `⏳ pending`인 첫 번째 태스크를 찾아 파일에서 `🔄 active`로 표시합니다.

---

## 세션 상태 블록

모든 AI 작업 전에 렌더링합니다. `.tdd-session.md`에서 모든 값을 읽습니다.

```markdown
---
## 🏓 Session State
| Field        | Value |
|--------------|-------|
| Story        | [ID]: [title] |
| Stack        | [stack] |
| Test FW      | [framework] |
| E2E FW       | [framework] |
| Conventions  | [conventions summary] |
| Phase        | RED / GREEN / REFACTOR |
| Current Task | [N] of [total]: [task title] |
| Turn         | DEV / AI |
| Next Action  | [one-line description] |
---

### Task Progress
| # | Title | Type | Status |
|---|-------|------|--------|
| 1 | [title] | unit | ✅ done / 🔄 active / ⏳ pending |
...
```

---

## 턴 설정

현재 태스크 세부 사항을 표시한 후 질문합니다:

```
Task [N]: [title]
Type: [unit/integration/e2e]
The first test will assert: [assertion description]

Who writes the first failing test?
→ **"me"** — I'll write it
→ **"you"** — AI writes it
```

일시 정지하고 기다립니다.

---

## 탈출 옵션 (항상 사용 가능)

| 개발자 입력 | 효과 |
|----------------|--------|
| `skip` | AI가 현재 턴을 대신 진행 |
| `next task` | 현재 태스크를 완료로 표시하고 다음으로 이동 |
| `abort` | 세션 중지, 완료된 내용을 커밋하려면 /tdd-commit 실행 |
| `restart task` | 현재 태스크 초기화, RED부터 다시 시작 |

---

## RED 단계

### AI의 턴인 경우

1. 세션 상태 블록 렌더링 (Phase: RED, Turn: AI)
2. **작성 전, 세션 파일에서 감지된 컨벤션을 확인합니다:**
   - 테스트 파일 위치 (동일 위치 vs `test/` 디렉토리)
   - 파일 명명 접미사
   - describe/test/it 구조 및 중첩 깊이
   - 어서션 라이브러리 및 스타일
   - 목 패턴 (vi.mock, vi.fn injection, mockk, MagicMock, 등)
   - 테스트 메서드 명명 컨벤션
3. 다음 조건을 충족하는 실패하는 테스트를 **직접 파일로 작성합니다**:
   - 프로젝트에서 감지된 컨벤션을 따릅니다 (일반적인 기본값이 아님)
   - 명확하고 동작을 설명하는 이름을 가집니다
   - 아직 존재하지 않거나 올바르지 않게 동작하는 함수/클래스/엔드포인트를 참조합니다
   - **올바른 이유**로 실패합니다: 어서션 실패 또는 심볼 누락 — 문법/import 오류가 아님
4. 파일 생성/수정 도구로 테스트를 **실제 파일에 작성합니다** (코드 블록만 표시하고 끝내지 않습니다)
5. 작성한 파일 경로와 예상 실패 출력을 표시합니다:
   ```
   ✏️ 테스트 파일 작성 완료: [정확한 파일 경로]

   예상 실패:
   [실패 메시지 예시]

   테스트를 실행하고 RED 상태(올바른 이유로 실패)를 확인해주세요.
   Type **"red confirmed"** or **"failing"** to continue.
   (Or type "skip" to have AI write the implementation instead)
   ```
6. 일시 정지하고 기다립니다

### 개발자의 턴인 경우

1. 세션 상태 블록 렌더링 (Phase: RED, Turn: DEV)
2. 표시:
   ```
   ## 🔴 RED — Your Turn

   Task [N]: [task title]
   Write a failing test that asserts: [assertion description]

   Paste your test code here.
   (Or type "skip" to have AI write it instead)
   ```
3. 일시 정지하고 기다립니다
4. 개발자가 코드를 붙여넣으면: 확인하고, 파일 경로를 기록하고, GREEN으로 진행합니다

### "올바른 이유"의 의미

```
✅ Correct RED                              ❌ Wrong RED (fix first)
─────────────────────────────────────────────────────────────────
TypeError: method is not a function         SyntaxError: Cannot find module
AssertionError: expected null to equal {...} ImportError: cannot import name
MockKException: no answer found             ClassNotFoundException
```

실패 이유가 잘못된 경우: 컴파일/import 오류를 해결하기 위해 빈 스텁(동작 없음)을 생성하고, 다시 실행한 후 RED를 확인합니다.

---

## GREEN 단계

### AI의 턴인 경우

1. 세션 상태 블록 렌더링 (Phase: GREEN, Turn: AI)
2. **작성 전, 세션 파일에서 감지된 컨벤션을 확인합니다:**
   - 디렉토리 구조 (기능 기반 vs 레이어 기반)
   - 클래스/함수 명명 컨벤션
   - 의존성 주입 패턴
   - 어노테이션/데코레이터 스타일
   - 오류 처리 방식
3. 실패한 테스트를 통과시키기 위한 **최소한의 코드**를 파일로 직접 작성합니다 — 그 이상은 작성하지 않습니다
4. 파일 생성/수정 도구로 구현 코드를 **실제 파일에 작성합니다** (코드 블록만 표시하고 끝내지 않습니다)
5. 작성한 파일 경로를 표시한 후:
   ```
   ✏️ 구현 파일 작성 완료: [정확한 파일 경로]

   전체 테스트를 실행해주세요.
   Type **"green confirmed"** or **"passing"** when all tests pass.
   (Paste error output if tests still fail)
   ```
6. 일시 정지하고 기다립니다
7. 개발자가 오류를 붙여넣으면: 근본 원인을 진단하고, 파일을 직접 수정하고, 다시 일시 정지합니다

### 개발자의 턴인 경우

1. 세션 상태 블록 렌더링 (Phase: GREEN, Turn: DEV)
2. 표시:
   ```
   ## 🟢 GREEN — Your Turn

   Write the minimum code to make the failing test pass.
   No extra features — pass the test only.

   Type **"done"** or **"green confirmed"** when all tests pass.
   (Or type "skip" to have AI implement it instead)
   ```
3. 일시 정지하고 기다립니다

### 최소 구현 원칙

```
// ✅ Minimum — only what the current test needs
async getUser(id: string) {
  return this.repository.findById(id)
}

// ❌ Over-engineering during GREEN
async getUser(id: string) {
  const cached = this.cache.get(id)   // no test for this yet
  if (!cached) throw new Error(...)    // no test for this yet
  return cached
}
```

캐싱, 오류 처리 등은 테스트에서 요구할 때만 추가합니다.

---

## REFACTOR 단계

1. 세션 상태 블록 렌더링 (Phase: REFACTOR)
2. 테스트와 구현을 다음 사항에 대해 검토합니다:
   - **중복** — 테스트와 구현에 동일한 로직이 있나요?
   - **명명** — 이름이 주석 없이도 의도를 드러내나요?
   - **매직 값** — 명명된 상수로 추출할 수 있나요?
   - **메서드 길이** — 10줄 이상인가요? 추출을 고려하세요.
   - **프레임워크 관용구** — Spring beans, React hooks, pytest fixtures
   - **컨벤션 일관성** — 세션 파일에서 감지된 패턴과 일치하나요?
3. 각 제안에 대해 표시하고 일시 정지합니다:
   ```
   **Refactoring suggestion [N]:** [one-line title]

   Reason: [why this matters]

   Before:
   [code block]

   After:
   [code block]

   Apply this refactor? (yes / no / modify)
   ```
4. 개발자가 **yes**를 입력하면: 파일 수정 도구로 **직접 변경 사항을 적용합니다**
5. 개발자가 **modify**를 입력하면: 수정 방향을 받아 반영한 후 직접 적용합니다
6. 리팩토링할 것이 없는 경우: "코드가 깔끔합니다. 이번 사이클에는 리팩토링이 필요하지 않습니다."
7. 모든 제안이 해결된 후:
   ```
   REFACTOR complete. Are all tests still GREEN?
   Type **"green"** to continue to the next test.
   ```
8. 일시 정지하고 기다립니다

---

## 사이클 완료 → 역할 교체

REFACTOR 후:
- 동일한 태스크의 다음 테스트를 위해 역할을 교체합니다 (AI ↔ DEV)
- 교체된 역할로 RED로 돌아갑니다

---

## 태스크 완료

개발자가 태스크의 테스트가 완료되었음을 알리거나 (더 이상 이 태스크에 대한 테스트가 없는 경우), 또는 양측이 태스크가 완료되었다고 동의하는 경우:

1. `.tdd-sessions/{story-id}.md`를 업데이트합니다:
   - 현재 태스크를 `✅ done`으로 표시합니다
   - 다음 태스크가 있는 경우, 다음 `/tdd-task` 호출 시 자동으로 감지됩니다

2. 표시:
   ```
   ✅ Task [N] complete: [task title]

   Tasks remaining: [list of pending tasks]

   → Run **/tdd-task** to continue with Task [N+1]: [title]
   → Run **/tdd-commit** if you want to commit what's done so far
   ```

---

## 참조 파일

| 파일 | 읽는 시점 |
|------|-------------|
| `.agents/skills/tdd-task/references/tdd-test-writing-guide.md` | 스택별 전체 테스트 패턴 |
| `.agents/skills/tdd-task/references/convention-detection.md` | 스택별 컨벤션 추출 |
| `.agents/skills/tdd-task/references/red-green-refactor-guide.md` | 상세 단계 완료 기준 |
