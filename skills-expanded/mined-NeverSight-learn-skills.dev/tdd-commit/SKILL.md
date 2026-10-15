---
name: tdd-commit
description: >
  Use this skill when the user says "tdd commit", "commit tdd", "finish tdd session",
  "TDD 커밋", "세션 커밋", or wants to commit after a TDD session.
  Reads the active .tdd-sessions/ file, summarizes completed tasks,
  proposes a Conventional Commits message, executes the commit, and cleans up the session file.
---

# TDD Commit

## 호출 방법

```
/tdd-commit [story-id]
```

- **인수 없음** — `.tdd-sessions/`에서 활성 세션 파일을 자동 감지
- **스토리 ID 제공** — `.tdd-sessions/{story-id}.md`를 직접 사용

---

## 1단계: 세션 파일 찾기

1. `.tdd-sessions/` 내 파일 목록 조회
2. **디렉토리가 존재하지 않거나 비어 있는 경우:**
   ```
   "No active TDD session found. Run /tdd-plan to start a new session."
   ```
   중단.
3. **파일이 정확히 하나인 경우:** 해당 파일 사용
4. **파일이 여러 개인 경우:**
   ```
   "Multiple sessions found. Which story are you committing?
   [1] 12345678.md — User Profile Update
   [2] payment-intent-2026-03-31.md — (no ID)
   Type the number or story ID."
   ```
   일시 중지하고 선택을 기다림.

---

## 2단계: 변경 사항 요약 출력

```markdown
## Changes Summary

**Story:** [ID]: [title]
**Stack:** [stack]

### Completed Tasks
- ✅ Task 1: [title] — [type]
- ✅ Task 2: [title] — [type]
- ⏳ Task 3: [title] — [type] ← skipped / not started

### Pending Tasks (not committed)
- [list any ⏳ pending tasks, or "none — all tasks complete"]
```

미완료 태스크가 있는 경우 다음을 표시: "이 태스크들은 완료되지 않았으며 이번 커밋에 포함되지 않습니다."

---

## 3단계: 커밋 메시지 제안

Conventional Commits 형식 사용:

```
[#STORY-ID] feat(<scope>): <short description under 72 chars>

Implements [STORY-ID]: [story title]

Tasks completed:
- [task 1 title]: [one-line description of what was implemented]
- [task 2 title]: [one-line description]
- [task N title]: [one-line description]

TDD: ping-pong pair programming session
```

### 스코프 선택

기술 레이어가 아닌 기능/도메인 이름을 사용:

| 컨텍스트 | 스코프 예시 |
|---------|-------------|
| TypeScript React | `user-profile`, `cart`, `checkout`, `auth` |
| Kotlin/Java Spring | `payment`, `order`, `user-service`, `notification` |
| Python FastAPI | `users`, `products`, `orders`, `auth` |

### 타입 선택

| 상황 | 타입 |
|-----------|------|
| 새 기능 (가장 일반적) | `feat` |
| 버그 수정 | `fix` |
| 리팩토링만, 새로운 동작 없음 | `refactor` |

---

## 4단계: 커밋 미리보기 출력 후 일시 중지

```markdown
## Commit Preview

**Message:**
```
[full commit message]
```

**Files to stage:**
[list source + test files created or modified during the session]
(Build artifacts, .env files, and IDE folders will NOT be staged)

Ready to commit?
→ Type **"commit"** or **"ship it"** to execute
→ Type your preferred message to override it
→ Type **"cancel"** to exit without committing
```

일시 중지하고 기다림.

---

## 5단계: 커밋 실행

개발자가 확인하면:

1. 세션의 모든 소스 및 테스트 파일을 스테이징 (스테이징 금지: `.env`, `.env.*`, `target/`, `build/`, `dist/`, `__pycache__/`, `.gradle/` 등 빌드 아티팩트)
2. `git add [files]` 후 `git commit -m "[message]"` 실행
3. 결과 커밋 해시 출력:
   ```
   ✅ Committed: abc1234 feat(payment): add payment intent creation endpoint
   ```

---

## 6단계: 세션 파일 정리

```
Delete `.tdd-sessions/[filename]`? (yes / no)
→ "yes" — delete the file
→ "no" — keep it (useful if the story spans multiple sessions)
```

일시 중지하고 기다림. 응답에 따라 실행.

삭제 후 `.tdd-sessions/`가 비어 있어도 그대로 두면 됩니다 — 이미 gitignore에 등록되어 있습니다.

---

## 레퍼런스 파일

| 파일 | 읽는 시점 |
|------|-------------|
| `.agents/skills/tdd-commit/references/commit-conventions.md` | 전체 커밋 형식 규칙 및 멀티 세션 전략 |
