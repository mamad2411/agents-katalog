---
name: pwrl-work-execute
description: Execute tasks with quality gates (inline, serial, or parallel modes)
argument-hint: "[Task list context from pwrl-work-prepare, execution mode]"
---

# pwrl-work-execute — Task Execution Engine

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What tasks should be executed? Confirm the execution parameters and verify the environment is ready."
- Provide clear recovery suggestions when errors occur

**Purpose:** Core execution engine that coordinates task implementation across three modes (inline, serial, parallel), enforces quality gates, manages task status progression, and integrates GitHub status syncing.

## Input

Accepts prepared context from `pwrl-work-prepare`:

```yaml
taskList:
  source: plan | task | prompt
  taskCount: 5
  tasks:
    - unit-id: S1
      file: docs/tasks/in-progress/2026-06-05-s1-task.md
      dependencies: []
      status: in-progress
executionMode: inline | serial | parallel
executionModeReasoning: "..."
githubIntegration:
  enabled: true | false
  tasksLinked: 3
  readyForSync: true | false
```

## Output: Execution Results

```yaml
mode: serial
taskCount: 5
tasksCompleted: 5
tasksFailed: 0
testsPassed: true
commitHash: abc1234
results:
  - unit-id: S1
    taskFile: docs/tasks/for-review/2026-06-05-s1-task.md
    status: for-review
    testsPassed: true
    summary: "Implemented feature X"
```

---

## Execution Modes

### Inline Mode (1-2 Tasks)

Direct execution without subagents, suitable for small work.

**When used:** 1-2 tasks, user interaction expected, small scope.

**Per-task flow:**

1. **Read context:**
   - Load task file and extract goal, implementation steps, test scenarios, acceptance criteria
   - Read files listed in task's `files` field
   - Check existing tests related to task scope
   - Identify codebase patterns and conventions

2. **Mark in-progress:**
   - Update task frontmatter: `status: in-progress`
   - If using directory org: move `to-do/` → `in-progress/`
   - Call S4 (pwrl-work-sync-status) if GitHub enabled

3. **Implement test-first (TDD):**
   - Write failing test for new behavior
   - Confirm test fails (red)
   - Implement minimal code to pass test (green)
   - Run test to confirm it passes
   - Refactor for clarity (refactor)
   - Repeat for each behavior slice

4. **Run quality gates:**
   - Run affected tests (not full suite)
   - Verify code follows project patterns
   - Run system checks (callbacks, events, failure paths, alternate entry points)

5. **Mark for-review on success:**
   - Update frontmatter: `status: for-review`
   - **CRITICAL: Move file** `docs/tasks/in-progress/` → `docs/tasks/for-review/`
     - Read the task file from `in-progress/` folder
     - Update frontmatter status: `status: in-progress` → `status: for-review`
     - Write the updated file to `docs/tasks/for-review/` with same filename
     - Delete original from `in-progress/`
     - Log: `Task ready for review: docs/tasks/in-progress/[file] → docs/tasks/for-review/[file]`
   - Update `docs/tasks/INDEX.md`
   - Call S4 for GitHub sync if enabled

**Status Transition:**

```
in-progress/ (status: in-progress) → for-review/ (status: for-review)
```

6. **Return result:**

```yaml
mode: inline
taskCount: 1
tasksCompleted: 1
tasksFailed: 0
testsPassed: true
results:
  - unit-id: U1
    status: for-review
    testsPassed: true
    summary: "Implemented email validation"
```

---

### Serial Mode (3+ Dependent Tasks)

Sequential execution for tasks with dependencies.

**When used:** 3+ tasks, dependencies exist between tasks, or file conflicts detected.

**Flow:**

1. **Determine execution order:**
   - Parse dependency graph from task list
   - Topological sort: tasks with no dependencies first, then their dependents
   - Build ordered execution queue

2. **For each task (sequentially):**

   **a) Execute task:**
   - Load task file and extract goal, implementation steps, test scenarios, acceptance criteria
   - Implement following test-first discipline
   - Run affected tests and quality gates
   - Update task status to `for-review`

   **b) Collect results:**
   - Capture test status, verification summaries, implementation summary
   - Verify task status is `for-review` or `blocked`

   **c) Check progress:**
   - Log: `[N/M] Task [unitId] completed: [status] ✓`
   - If blocked: pause, ask user to resolve, retry or skip

3. **After all tasks complete:**

   **a) Run full targeted test suite:**
   - Run test suite covering all files modified by all tasks
   - Verify no integration issues between sequentially executed tasks
   - If tests fail: investigate, mark affected tasks as blocked

   **b) Stage and commit:**
   - Stage all changes
   - Create commit message with unit IDs and summary
   - Push to branch
   - Log commit hash

4. **Return aggregated result:**

```yaml
mode: serial
taskCount: 5
tasksCompleted: 5
tasksFailed: 0
testsPassed: true
commitHash: abc1234
results:
  - unit-id: S1, status: for-review, testsPassed: true
  - unit-id: S2, status: for-review, testsPassed: true
  - ...
```

---

### Parallel Mode (3+ Independent Tasks)

Concurrent execution for independent tasks.

**When used:** 3+ tasks, no dependencies, no file conflicts (verified by prepare phase).

**Safety constraints (MUST verify before proceeding):**

- No task depends on another task's output
- No file appears in more than one task's `files` list
- If conflicts found at runtime → downgrade to serial mode

**Flow:**

1. **Verify safety (pre-execution):**
   - Re-check file-to-task map for conflicts
   - If any overlap found: log warning, fall back to serial mode
   - If safe: proceed to parallel execution

2. **Execute all tasks in parallel:**
   - For each task: execute implementation independently
   - Each task runs: load → implement → verify → status update
   - Run targeted tests for each task (not full suite)
   - Track execution progress and results

3. **Runtime conflict detection (during execution):**
   - Monitor file access for conflicts
   - If conflicts detected:
     - **Pause new task starts** — Do not begin new parallel tasks
     - **Wait for in-flight tasks** — Allow running tasks to complete
     - **Log conflict details** — Which tasks share which files
     - **Ask user:** "File conflicts detected during parallel execution. Retry in serial mode or abort?"
     - **If user chooses serial:** Re-queue all tasks for serial re-execution
     - **If user chooses abort:** Mark all tasks as blocked, return partial results

4. **Collect results:**
   - Aggregate all task results as execution completes
   - Track completion time per task

```yaml
parallelTasksStarted: 4
parallelTasksCompleted: 4
parallelTasksFailed: 0
tasks:
  - unit-id: U1, status: for-review, testsPassed: true, duration: "5m"
  - unit-id: U2, status: for-review, testsPassed: true, duration: "3m"
  - ...
```

5. **Run full targeted test suite:**
   - All modified files collected from all tasks
   - Run test suite covering all affected areas
   - Verify no integration issues between parallel work
   - If integration tests fail: identify which task(s) caused the issue

6. **Stage and commit:**
   - Stage all changes from all completed tasks
   - Create commit message with all unit IDs
   - Push to branch
   - Log commit hash

7. **Return result:**
   - Same structure as serial mode result

---

### NEW: Cross-Plan Parallel Execution (with Sync Points)

**When used:** Multiple plans with cross-plan dependencies; parallelization groups generated by pwrl-work-prepare.

**Coordination Protocol:**

**Per Group Cycle (repeat for each parallelization group):**

1. **Pre-execution validation:**
   - Verify all tasks in group have no file conflicts (double-check)
   - Verify all dependency constraints from previous groups are met
   - If any task status invalid (per state machine) → abort group, rollback

2. **Execute all tasks in group in parallel:**
   - For each task in parallelGroup[N]: execute implementation
   - Each task works independently within the group
   - Track group ID and sync point ID for each task
   - Run targeted tests for each task

3. **Wait for group completion:**
   - Wait for all tasks in group to complete
   - Collect individual task results

4. **Sync point validation:**
   - **File conflict check**: Scan all changed files across all tasks in group
     - If any file modified by 2+ tasks in same group → abort, rollback, error
   - **Git state check**: Verify working directory is clean (no uncommitted changes outside of this group)
   - **Status validation**: Check all task frontmatter for state machine violations

5. **Atomic commit (sync point):**
   - Stage all changes from all tasks in group
   - Create single commit message: `[GROUP-N] U1, U2, U3: <summary>`
   - Commit atomically (all-or-nothing)
   - Push to branch
   - Log sync point completion: `✓ Sync point N completed: 3 tasks, 12 files changed`

6. **Signal dependent tasks:**
   - For any tasks in subsequent groups that depend on current group:
     - Update their `blockedBy` status (dependencies now met)
     - Flag as ready to execute in next group cycle

7. **If group fails:**
   - Mark all tasks in group as blocked
   - Rollback working directory to pre-group state
   - Ask user: "Retry group, skip group, or abort workflow?"

**Cross-group atomicity guarantee:**

- Each sync point produces exactly one commit
- Commits are sequential (group 0 → sync 0 → commit, group 1 → sync 1 → commit, etc.)
- If sync point N fails, sync points N+1 onwards are not executed

**Output per cross-plan execution:**

```yaml
executionMode: parallel-cross-plan
parallelGroups: 3
groupResults:
  - groupId: 0
    tasksCompleted: 3
    tasksFailed: 0
    syncPointId: 0
    commitHash: abc1234
    filesChanged: 12
    testsPassed: true
  - groupId: 1
    tasksCompleted: 2
    tasksFailed: 0
    syncPointId: 1
    commitHash: def5678
    filesChanged: 8
    testsPassed: true
  - groupId: 2
    tasksCompleted: 1
    tasksFailed: 0
    syncPointId: 2
    commitHash: ghi9012
    filesChanged: 3
    testsPassed: true

totalTasksCompleted: 6
totalCommits: 3
finalCommitHash: ghi9012
```

---

## Quality Gates

### Test Verification

- ✅ Tests pass for all affected test files
- ✅ New tests cover the new behavior
- ✅ Existing tests still pass (no regressions)
- ❌ **Fail if:** Tests don't pass after implementation

### Code Pattern Verification

- No magic numbers or strings (use constants)
- No unused imports or dead code
- Functions are small and focused
- Names are meaningful (no `$data`, `$result`)
- Follows language-specific style guides
- ❌ **Fail if:** Significant pattern deviations found

### System Check

For each task, verify:

1. **Callbacks/middleware/observers/events:**
   - Are all expected callbacks triggered?
   - Are middleware chains complete?

2. **Test coverage depth:**
   - Do tests cover real interactions (not only mocks)?
   - Are edge cases covered (empty, null, error)?

3. **Failure paths:**
   - Are failure paths idempotent (can retry safely)?
   - Are cleanup handlers in place (finally blocks, teardown)?

4. **Consistency:**
   - Is behavior consistent across alternate entry points?
   - Are error messages consistent with project conventions?

### Failure Handling

| Gate Failure                            | Action                                                  |
| --------------------------------------- | ------------------------------------------------------- |
| Test fails                              | Mark task `blocked`, show test output, offer retry/skip |
| Pattern deviation                       | Warn, ask user: accept or revise                        |
| System check fails                      | Mark task `blocked`, log details, offer retry           |
| Subagent timeout (parallel)             | Kill subagent, mark task failed, other tasks unaffected |
| Integration test fails (post-execution) | Mark offending task blocked, revert if needed           |

---

## Task Status Progression

State machine for each task:

```
to-do
  ↓ (execution starts)
in-progress
  ├→ (all gates pass)
  │   ↓
  │ for-review  ← Ready for review phase (S6)
  └→ (gate failure)
      ↓
    blocked  ← User must resolve, then retry
```

**Actions at each transition:**

| Transition                        | File Ops                      | Index Update  | GitHub Sync                           |
| --------------------------------- | ----------------------------- | ------------- | ------------------------------------- |
| `to-do` → `in-progress`           | Move to `in-progress/`        | Update status | Add `in-progress` label, post comment |
| `in-progress` → `for-review`      | Move to `for-review/`         | Update status | Add `for-review` label, post comment  |
| `in-progress` → `blocked`         | Stay in `in-progress/` + note | Update status | Add `blocked` label, post reason      |
| `blocked` → `in-progress` (retry) | Keep in `in-progress/`        | Update status | Add `in-progress`, remove `blocked`   |

---

## Subagent Constraints

**Subagents MUST NOT:**

1. Run full test suite (only targeted tests for changed files)
2. Stage or commit changes (orchestrator does this)
3. Push to remote (orchestrator does this)
4. Modify branch or stash (orchestrator manages branches)
5. Update `docs/tasks/INDEX.md` directly (orchestrator aggregates)

**Subagents CAN:**

1. Read and modify source files
2. Run targeted tests for changed files
3. Update task file frontmatter (status field)
4. Move task file between directories
5. Call S4 (pwrl-work-sync-status) for GitHub sync

**Enforcement:**

- Pass constraint flags when spawning: `--no-full-suite`, `--no-commit`
- Subagent checks flags at startup and refuses violations
- Orchestrator validates after each subagent completes

---

## Error Handling & Recovery

| Scenario                    | Handling                                     | Recovery                           |
| --------------------------- | -------------------------------------------- | ---------------------------------- |
| Task execution crashes      | Catch error, mark `blocked`, log stack trace | Retry task after fix               |
| Test failure                | Mark `blocked`, show failing test output     | Fix tests or implementation, retry |
| Quality gate fails          | Mark `blocked`, show gate reason             | Address issue, retry               |
| Subagent timeout (parallel) | Kill subagent, mark failed                   | Re-run as serial or fix            |
| Git error during commit     | Log error, show git state                    | Fix git state, retry commit        |
| Parallel safety violation   | Downgrade to serial, warn                    | Continue safely in serial          |

**User prompts for blocked tasks:**

- "Task [unitId] is blocked due to [reason]. Would you like to retry, skip, or investigate?"
- Retry: Re-execute the task
- Skip: Mark as skipped (add to backlog)
- Investigate: Provide details for manual intervention

---

## Progress Reporting

**Inline:**

```
[1/2] Executing task U1: Add email validation
  → Reading target files...
  → Writing test first... ✓ FAIL (expected)
  → Implementing feature...
  → Running tests... ✓ PASS
  → Task complete: for-review
```

**Serial:**

```
[1/5] Spawning subagent for task U1...
[2/5] Subagent U1 completed: for-review ✓
[3/5] Spawning subagent for task U2 (depends on U1)...
[4/5] Subagent U2 completed: for-review ✓
[5/5] Running full test suite...
[✓] All tests pass
[✓] Creating commit: "Implement U1, U2: Add user validation"
```

**Parallel:**

```
[1/4] Spawning 4 parallel subagents...
  [U1] Starting... [U2] Starting... [U3] Starting... [U4] Starting...
[✓] All subagents complete
[✓] Aggregating results: 4 completed, 0 failed
[✓] Running full integration test suite...
[✓] All tests pass
[✓] Creating commit: "Implement U1, U2, U3, U4"
```

---

## Dependencies

- **pwrl-work-prepare** — Consumes prepared task list and execution mode
- **pwrl-work-sync-status (S4)** — Called for GitHub sync at status transitions
- **File system** — Task file management, source file reading/writing
- **Test framework** — Running targeted and integration tests
- **Git** — Staging and committing (orchestrator only)
- **Subagent infrastructure** — For serial/parallel spawning

## References

- **S1 Analysis:** `docs/analysis/2026-06-05-pwrl-work-structure-analysis.md`
- **S3 Skill:** `pwrl-work-prepare/SKILL.md`
- **S4 Skill:** `pwrl-work-sync-status/SKILL.md`
- **Source Phase 2:** Installed `pwrl-work` skill (Phase 2: Execute, lines 122-172)
- **Next Skill:** `pwrl-work-review` (S6)
