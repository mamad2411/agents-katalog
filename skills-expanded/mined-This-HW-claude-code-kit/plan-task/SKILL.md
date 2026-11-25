---
name: plan-task
description: Structured task planning using Work files. Use for any new feature, bug fix, or project that needs a task breakdown before implementation.
model: opus
effort: max
---

# Plan-Task 스킬

## 사용법

```
/plan-task W-001                    # 기존 Work ID로 재개
/plan-task 로그인 기능 추가          # 새 요청 (Work 자동 생성)
/plan-task fix the auth bug         # 새 요청 (description 형식)
```

## Phase Gate

이 스킬은 **brainstorming** 이후에 실행되어야 합니다.

`docs/specs/`에 관련 스펙 파일이 없으면:
- 새 기능이라면 → 먼저 `brainstorming` 스킬을 invoke하세요
- 버그 수정/소규모 작업이라면 → 계속 진행 가능 (단, 이 사실을 명시)

---

Work 파일과 Task 시스템을 통합하여 구조화된 Planning을 진행합니다.

---

## Step 0: Work ID 확보 [건너뛰기 금지]

### 체크리스트 초기화 [최우선]

Step 0 진입 즉시, Work ID 확보 전에 스킬 자체 진행을 추적할 Tasks를 생성합니다:

1. `ToolSearch("select:TaskCreate,TaskUpdate,TaskList")` 실행

> **Task 도구가 없으면 멈추지 말고 대체 경로로 간다** — `ToolSearch`가 Task 계열을
> 반환하지 않는 호스트/세션이 있다(F-038). 그때는 `./scripts/checklist.sh` 기반
> durable checklist로 추적한다. 규율 SSOT: `skills/plan-task/references/task-tools-fallback.md`.
2. 다음 Tasks 생성 (이미 `[Planning]` Task 있으면 스킵):

```
TaskCreate: [Planning] Work ID 확보 및 초기화
TaskCreate: [Planning] 요구사항 명확화
TaskCreate: [Planning] 구현 계획 수립
TaskCreate: [Planning] Planning 완료 처리
```

의존성 설정: 각 Task는 이전 Task가 완료되어야 시작 가능 (addBlockedBy).

### Work ID가 제공된 경우 (예: `/plan-task W-043`)

1. `docs/works/idea/` 디렉토리에서 해당 Work 폴더 탐색
2. `W-XXX-{slug}/W-XXX-{slug}.md` 파일 읽기
3. `progress.md`로 현재 진행 상황 확인 — 중단된 지점부터 재개
4. frontmatter `status`, `current_phase` 확인

### Work ID가 없는 경우 (새 요청)

`docs/works/` 폴더가 존재하면:

1. `work.sh new`로 Work 파일 생성:
   ```bash
   ./scripts/work.sh new "<요청 제목>"
   ```
   → `docs/works/idea/W-XXX-{slug}/` 폴더와 파일 자동 생성
   → 출력된 Work ID(예: W-001)를 이후 단계에서 사용

`docs/works/` 폴더 자체가 없으면 → Fallback으로 이동

Work ID 확보 완료 후에만 Step 1로 진행.

---

## Step 1: Task 시스템 초기화 [건너뛰기 금지]

1. `ToolSearch("select:TaskCreate,TaskUpdate,TaskList")` — 스키마 fetch (deferred tool이므로 필수)
2. `TaskList` 실행 → 이미 생성된 동일 Work Task 있으면 이 Step 스킵 (중복 방지)
3. Task 없으면 아래 두 Tasks 생성:

   ```
   T1: [W-XXX][Planning] 요구사항 명확화
   T2: [W-XXX][Planning] 구현 계획 수립   ← blockedBy T1
   ```

   TaskCreate 시 모든 Task에 metadata 포함:

   ```json
   { "work_id": "W-XXX", "phase": "planning" }
   ```

   T2 생성 직후 `TaskUpdate(T2, addBlockedBy=[T1])` 설정.

4. `progress.md` Task Map 섹션 초기화 (description 컬럼 포함):

   ```markdown
   ## Task Map

   ### Planning

   | Task ID | 제목            | 설명                          | 상태 | blockedBy |
   | ------- | --------------- | ----------------------------- | ---- | --------- |
   | T-1     | 요구사항 명확화 | clarify-requirements 에이전트 | ⏳   | -         |
   | T-2     | 구현 계획 수립  | plan-implementation 에이전트  | ⬜   | T-1       |

   ## Task 업데이트 로그

   - {ISO timestamp}: W-XXX Planning 시작
   ```

---

## Step 2: T1 실행 — 요구사항 명확화

`clarify-requirements` 에이전트에 위임하거나 직접 진행:

1. **규모 판단** (planning-protocol.md 기준):
   - Small: 1개 모듈, 1-3파일, ~10h
   - Medium: 2-3개 모듈, 4-10파일, 20-50h
   - Large: 4개+ 모듈, 10파일+, 50h+
   - 판단 후 Work frontmatter `size` 업데이트

2. **P0 모호함 해결**: P0 발견 시 즉시 중단 → 사용자에게 질문

   ```
   맥락: [상황]   질문: [구체적 질문]
   옵션: 1. [A]   2. [B]
   ```

3. **요구사항 정리**: 핵심 요구사항, 영향 범위, 리스크

4. **완료 후 의무 업데이트**:
   - `planning-results.md` → `## 요구사항 명확화` 섹션에 결과 기록
   - `decisions.md` → P0 결정 사항 DEC-XXX로 추가
   - `progress.md` Task Map: T-1 행 상태 ✅로 수정
   - `progress.md` Task 업데이트 로그에 완료 시각 기록
   - Work frontmatter `updated_at` 갱신

5. `TaskUpdate(T1, status="completed")` 마킹

---

## Step 3: T2 실행 — 구현 계획 수립

`plan-implementation` 에이전트에 위임하거나 직접 진행:

1. T1 결과(`planning-results.md`) 기반으로 구현 계획 작성
2. 규모별 추가 단계 (planning-protocol.md 참고):
   - Medium+: 사용자 여정 설계 포함
   - Large+: 비즈니스 로직 정의 포함
3. 구현 순서, 의존성, 예상 범위 명시

4. **완료 후 의무 업데이트**:
   - `planning-results.md` → `## 구현 계획` 섹션에 결과 기록
   - `progress.md` Task Map: T-2 행 상태 ✅로 수정
   - `progress.md` Task 업데이트 로그에 완료 시각 기록
   - Work frontmatter `phases_completed: [planning]`, `updated_at` 갱신

5. `TaskUpdate(T2, status="completed")` 마킹

---

## Step 4: Planning 완료 처리

0. **[건너뛰기 금지]** auto-dev invoke(핸드오프) **전에** `TaskList`로 이 Work의
   `[Planning]`/`[Brainstorm]` 중 "끝났는데 마킹 안 된" 태스크를 completed로 정리한다
   (규율 SSOT: `rules/definition-of-done.md#task-마감-규율`).
1. Work 파일 최종 업데이트 확인 (frontmatter, progress.md, planning-results.md)
2. 다음 단계 안내:

Planning이 완료되었습니다. 바로 개발을 시작하겠습니다.

`auto-dev` 스킬을 즉시 invoke합니다. (사용자가 "나중에" 또는 "직접 실행"을 원하면 아래 명령을 안내하고 invoke를 건너뜁니다)

```bash
/auto-dev W-XXX        # 개발 파이프라인 시작
./scripts/work.sh next-phase W-XXX  # Phase만 전환
```

---

## Fallback: Work 시스템 없는 경우

`docs/works/` 폴더가 없으면 Work 파일 없이 Planning만 진행:

1. 요구사항 명확화 (P0 질문 포함)
2. 규모 판단
3. 구현 계획 수립
4. 결과를 대화창에 출력

---

## 참고 문서

| 문서              | 경로                                              |
| ----------------- | ------------------------------------------------- |
| Work 시스템 상세  | `plugins/common/skills/plan-task/references/work-system.md` |
| Planning 프로토콜 | `plugins/common/rules/planning-protocol.md`       |
