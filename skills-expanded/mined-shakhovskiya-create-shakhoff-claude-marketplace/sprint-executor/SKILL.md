---
name: sprint-executor
description: "Core sprint execution loop. Manages task-by-task execution within a sprint with discipline gates: DoR check before task, AC verification after task, hooks active during execution. Used by sprint-orchestrator during sprint execution phase."
---

# Sprint Executor

Исполняет sprint task-by-task с жёсткой дисциплиной.

## Когда применять

- Phase 5.x of sprint cycle
- После DoR validation passed for all sprint tasks
- Hooks active: pre-tool-use-checkin, pre-tool-use-test-first, post-tool-use-tracker

## Execution loop per task

Для каждой task в active sprint:

### 1. Task start

```
[ai-scrum] Starting task T-{N}: {title}
[ai-scrum] AC count: {N}
[ai-scrum] Test approach: {brief}
[ai-scrum] Effort estimate: {XS|S|M|L}
```

Update `.sprints/active/_state.json`:
- `active_task: T-{N}`
- `task_started_at: timestamp`

### 2. Strict checkin discipline

executor работает над task. На каждый logical step делает checkin:

```
/sprint:checkin "Read existing implementation"
/sprint:checkin "Wrote failing test for X scenario"
/sprint:checkin "Implemented function X to pass test"
/sprint:checkin "Verified existing tests still pass"
```

**Hooks enforce**:
- pre-tool-use-checkin warns/blocks if no checkin in 5 min
- pre-tool-use-test-first blocks production code without preceding test changes
- post-tool-use-tracker silently logs все tool calls

### 3. Failures and fallbacks

Если что-то не работает:

**Tool failure**:
```
/sprint:fail "pydeps Python 3.13 incompatible" --error-log=/tmp/pydeps-error.log
/sprint:fallback "Use madge for JS deps, manual import analysis for Python"
```

**Step impossible to complete**:
```
/sprint:skip "Mutation testing" "depth=quick mode, not applicable per skill methodology"
```

### 4. AC verification (mandatory)

After task work appears complete - verify each AC:

```
[executor] Verifying AC for T-{N}:
  AC 1: User can register with email
    Verified by: test_user_registration_email
    Status: PASS (test exists, runs, passes)
  
  AC 2: System validates email format
    Verified by: test_email_format_validation
    Status: PASS
  
  AC 3: Password hashed with bcrypt
    Verified by: test_password_hashing
    Status: PASS
```

If any AC unverified - **task NOT done**, must continue work or escalate.

### 5. Task close

```
/sprint:checkin "Task T-{N} complete - all AC verified"
```

Update `.sprints/active/tasks/T-{N}.md`:
- Status: done
- Completed: timestamp
- AC verification results

Update `.sprints/active/sprint-{N}.md`:
- Move T-{N} to completed list
- Update sprint progress

## Sprint completion

После all tasks в sprint completed:

### 1. Sprint goal verification

Explicitly state in checkin:
```
/sprint:checkin "Sprint goal achieved: {goal text}"
```

OR partial:
```
/sprint:checkin "Sprint goal partial: {what was done, what deferred and why}"
```

OR not achieved:
```
/sprint:checkin "Sprint goal NOT achieved: {explanation}"
```

### 2. Increment verification

For each declared increment artifact:
```
[executor] Verifying increment artifacts:
  ✓ docs/audit/<TS>/architecture/findings.json (1.2 KB, valid JSON)
  ✓ docs/audit/<TS>/architecture/c4-inferred.md (3.4 KB, valid markdown)
  ✓ HANDOFF.md updated (last modified within sprint window)
```

If any increment missing - cannot close sprint.

### 3. Trigger sprint complete

```
/sprint:complete
```

This triggers:
- DoD validation gate
- If passes: internal SE review
- If passes: external Codex review (if available)
- If passes: retrospective
- HANDOFF.md update validation
- Move to next sprint or finalize task cycle

## Принципы execution

### Honest progress

- Don't `/sprint:checkin "step done"` если не сделано
- Don't `/sprint:complete` если AC unverified
- Don't claim test pass без actual test run

### Test-first discipline

Hard rule:
- Production code change → test must exist or be modified first in same task
- Hook blocks otherwise
- Override через `/sprint:test-exempt` только с явной justification (logged)

### Fail-secure

If unsure if step complete:
- Don't checkin "done"
- Either: continue work, ask user, or `/sprint:skip` с explanation

### Continuous tool tracking

Каждый tool call автоматически logged в `.sprints/active/tool-history.log`. Это для:
- checkin-validator honesty checks
- Retrospective accurate timing
- Audit trail

## Integration с claude-solo-factory kit (если установлен)

Если в проекте есть kit - executor должен **delegate methodology к kit skills** где applicable.

**Detection** (в начале sprint execution):
```bash
KIT_AVAILABLE=false
test -d .claude/skills && KIT_AVAILABLE=true
```

### Kit skills для использования

#### `tdd` skill (для code tasks)

Если task involves writing/modifying code AND `.claude/skills/tdd/SKILL.md` exists:

1. **Read kit's tdd skill** для full methodology
2. **Apply Red-Green-Refactor cycle** per kit's instructions:
   - Write failing test first
   - **WATCH IT FAIL** (run test runner, confirm failure for right reason)
   - Write minimum code to pass
   - **WATCH IT PASS** (confirm tests pass)
   - Refactor если needed
3. ai-scrum's test-first hook **enforces** structurally - kit's tdd skill **teaches** правильно
4. Combined: hook physically blocks bad practice, skill teaches good practice

#### `code-discipline` skill (для всех code edits)

Если `.claude/skills/code-discipline/SKILL.md` exists - apply Karpathy rules для каждого edit:

1. **Minimum code that solves the problem** - no speculative features, no premature abstraction
2. **Surgical changes** - touch only what необходимо
3. **Surface assumptions** - ask when unclear, don't invent
4. **Goal-driven execution** - define verification before starting

These rules apply во время каждой task, не только final review.

#### `verify` skill (часть DoD validation)

См. dod-validator skill - "no regressions" criterion может invoke kit's `verify` skill.

#### Other kit skills (контекстуально)

- `mock-fidelity` - если task includes UI from mockup
- `data-source-research` - если task touches new database/API
- `lsp-setup` - если LSP not configured
- `design-md` - если working with design system

Apply contextually based on task type.

### Если kit absent

Sprint-executor follows **inline instructions** из этого skill без external dependencies:
- Test-first via hook enforcement (не TDD methodology)
- Generic code discipline (не Karpathy rules)
- Direct AC verification (без deep verify methodology)

**Functional но less rich**. Plugin recommends копирование kit для richer experience.

## Edge cases

### Task taking longer than estimated

If task estimated XS but reaching M effort:
- Continue but log warning
- In retrospective: review estimation accuracy
- Don't artificially split mid-task

### Task discovers blocking dependency

```
/sprint:fail "T-3 blocked by missing T-X (not in plan)"
```

Then:
- Either /sprint:cancel and /sprint:replan
- Or document, defer T-3 to next sprint cycle
- Or address dependency inline (if minor)

### User interrupts mid-sprint

User says "stop":
- Save current state in `_state.json`
- Don't auto-cancel
- User has options: /sprint:status, /sprint:cancel, или resume in next session

### Hook BLOCK during execution

User sees BLOCK message с resolution options. Examples:

**Test-first BLOCK**:
```
BLOCKED: Cannot edit src/auth.py
Test-first violation. Current task T-2 has no test file changes yet.

Resolution:
  1. Write/modify test file first
  2. /sprint:test-exempt "reason" if this change shouldn't have test
```

**No-checkin BLOCK** (in strict mode):
```
BLOCKED: No checkin in last 5 minutes.
Last action: Edit src/billing.py (10 min ago)
Current task: T-3

Resolution:
  /sprint:checkin "describe what you've been doing"
```

## Output

Sprint execution doesn't produce its own files - just orchestrates updates to:
- Task files (status, AC verification)
- Sprint file (progress, log)
- Increment artifacts (whatever task produces)
- Tool history (silently)

Output to user during execution:
- Periodic progress updates
- Failures requiring attention
- Hook BLOCKs (require resolution)
- Task completions
