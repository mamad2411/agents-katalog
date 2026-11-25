---
name: dod-validator
description: "Validates Definition of Done before sprint can close. Checks mandatory criteria (steps marked, goal addressed, increment exists, HANDOFF updated, test compliance, internal review) and conditional criteria. HARD GATE - blocks /sprint:complete if criteria fail."
---

# DoD Validator

Definition of Done гейт перед закрытием sprint - HARD BLOCK если что-то не сделано.

## Verification artifact contract

Before re-running any tests/app exercises, look for
`docs/verification/<task_ref>/latest.json` produced by `solo-sdlc:verify`
(schema `schemas/verification-report.schema.json`).
- If absent OR `mtime < task.started_at` → DoD FAIL with
  message "verification report missing — run /solo-sdlc:verify-app".
- If `verdict != pass` → DoD FAIL with `verdict_reason`.
- If `verdict == pass` → mark verification criterion satisfied; do NOT re-run tests.

This avoids duplicate work between solo-sdlc:verify and ai-scrum:dod.


## Когда применять

- При вызове `/sprint:complete`
- Phase 5.4 sprint cycle
- Этот skill - **последняя линия защиты** перед closing sprint

## Mandatory criteria (cannot skip)

### 1. All steps marked

Все sprint backlog steps должны иметь status:
- `done`
- `skipped` (с justification)
- `failed` (с reason)

NO unmarked steps.

**Verification**:
- Read `.sprints/active/sprint-{N}.md`
- Parse checkin log
- Compare with original backlog
- All steps accounted for? PASS / FAIL

### 2. Sprint goal addressed

Final checkin must explicitly state:
- "Sprint goal achieved: ..." OR
- "Sprint goal partial: ..." OR
- "Sprint goal NOT achieved: ..."

**Verification**:
- Search checkin log для goal-related statement
- Match against required pattern
- PASS / FAIL

### 3. Increment artifacts exist

All declared increment artifacts должны:
- Physically exist as files
- Be non-empty (>0 bytes, не just whitespace)
- Match expected type (md is markdown, json valid, etc.)

**Verification**:
```bash
for artifact in declared_artifacts:
  test -f "$artifact" || FAIL "Missing: $artifact"
  test -s "$artifact" || FAIL "Empty: $artifact"
  validate_format "$artifact"  # if applicable (JSON schema, etc.)
```

### 4. HANDOFF.md updated

HANDOFF.md must:
- Be modified within sprint window (timestamp check)
- Have new sprint cycle section appended
- Required sections present (Recent activity, Open questions, Important decisions, Next priorities)

**Verification**:
- Run handoff-keeper subagent в validation mode
- Returns PASS / FAIL with details

### 5. Test-first compliance

For all production code changes in sprint:
- Test file changes preceded production changes within same task
- OR `/sprint:test-exempt` invoked with logged reason

**Verification**:
- Parse `tool-history.log` for write/edit operations
- Group by task
- For each production change: was there test change earlier in same task?
- Auto-exempt files (configs, migrations, generated) skipped
- Explicit exempts logged in `.sprints/active/test-exemptions.log`

If non-exempt production change without preceding test → FAIL.

### 6. Test increment

If sprint had production code changes:
- At least 1 test file added or modified

If sprint was audit/research/docs only:
- N/A applies, must be documented in DoD justification field

**Verification**:
- Parse tool-history for production code edits → has them?
- If yes: parse for test file edits → has them?
- N/A claim must have justification text

### 7. Internal SE review passed

senior-engineer subagent must complete review, returning:
- `PASS` (no blocking issues), OR
- `WAIVE` (explicit waiver with documented reason)

`FAIL` blocks sprint closure.

**Verification**:
- Read `.sprints/active/reviews/se-review-sprint-{N}.md`
- Check verdict field
- If FAIL → BLOCK
- If WAIVE → require justification in waive_reason field

## Conditional criteria

### 8. External Codex review

**Condition**: codex-plugin-cc installed

**Requirement**: Codex review verdict is PASS or AGREE_WITH_CLAUDE

**Verification**:
- Check codex-plugin-cc availability
- If installed - read `.sprints/active/reviews/codex-review-sprint-{N}.md`
- Verdict check

In strict: REQUIRED if Codex available
In lenient: OPTIONAL

### 9. ADR for architectural decisions

**Condition**: Sprint introduces architectural changes

**Detection** (heuristic):
- New framework dependency added (changes in package.json/requirements.txt)
- Database schema migration с структурными изменениями (not just data fixes)
- Auth flow modification (changes in auth/ paths)
- API contract changes (changes in API/route definitions)
- New service/module introduction

**Requirement**: ADR file created or updated

**Verification**:
- Parse git diff for sprint changes
- Apply detection heuristics
- If detected - check `docs/architecture/adr/` (or similar) для new file or modification within sprint window

### 10. Rollback plan

**Condition**: Sprint includes risky changes (migrations, destructive ops)

**Requirement**: Rollback plan documented in task or ADR

**Verification**:
- Detect migration files в diff (`migrations/`, `*migrate*`)
- Detect destructive SQL/operations
- If detected - check task description или referenced ADR for rollback section

### 11. No regressions

**Condition**: Sprint had code changes

**Requirement**: All previously passing tests still pass + verification methodology applied

**Verification**:

#### Path A: Kit's `verify` skill available (preferred)

Если `.claude/skills/verify/SKILL.md` exists в проекте - **invoke kit's verify skill**:

1. Apply 10-step verification methodology:
   - Run full test suite (with project-specific commands)
   - Lint (golangci-lint, ruff, mypy, eslint, tsc)
   - Run the app
   - Exercise each acceptance criterion (with curl/playwright/etc.)
   - Check observability (structured logs, metrics)
   - Performance smoke test (если NFRs)
   - Edge case verification
   - Visual verification (для UI work)
   - Generate verification report
   - Block proceeding если anything failed

2. Read verification report - if all PASS → DoD criterion 11 PASSES.

3. Verification report saved to `.sprints/active/verification-sprint-{N}.md` (Boris Cherny принцип).

**Why preferred**: kit's verify - deep methodology. "It compiles ≠ it works". Real verification not just test exit codes.

#### Path B: Fallback inline check (если kit absent)

Если kit's verify не available:

```bash
# Quick fallback verification
case "$LANGUAGE" in
    python) pytest --no-cov -q ;;
    typescript) npm test ;;
    go) go test ./... ;;
esac
```

Compare exit code и failed tests count vs baseline.
If new failures - FAIL.

**Limitation**: structural check only. Not real verification (just "tests pass"). 

In quick mode (no test framework setup) - skip with WARN.

**Recommendation в DoD report**: если using Path B - note "verification was structural only; recommend installing kit's verify skill for deep methodology".

### 12. LSP no errors in changed files

**Condition**: LSP integration available (через lsp-bridge skill)

**Requirement**: LSP shows no type errors or unresolved references in changed files

**Verification**:
- Get list of files changed in sprint
- Run lsp-bridge для каждого:
  - Type errors
  - Unresolved references
- If errors found - FAIL с details

### 13. Mutation score threshold

**Condition**: `mutation_testing.enabled = true` in config AND sprint added/modified tests

**Requirement**: Mutation score for changed tests >= threshold (default 60%)

**Verification**:
- Detect mutation tool availability (mutmut, stryker, go-mutesting)
- Run on changed test files only
- Score >= threshold → PASS
- Below threshold → FAIL

This is slow (часы возможны) - only if explicitly enabled.

## Workflow

### 1. Load DoD criteria

From config:
- Default mandatory (always 1-7)
- Applicable conditional (8-13 based on detection)
- Custom additions (from /sprint:dod-customize)

### 2. Run all checks

Sequential, capture each result:

```python
for criterion in dod_criteria:
    result = check_criterion(criterion, sprint_state)
    results[criterion.id] = result
```

### 3. Apply strictness rules

**strict**: Any FAIL → BLOCK
**lenient**: Mandatory FAIL → BLOCK; Conditional FAIL → WARN
**permissive**: Critical mandatory FAIL → BLOCK; rest → WARN

### 4. Generate report

Save `.sprints/active/dod-validation-sprint-{N}.md`:

```markdown
# DoD Validation: Sprint {N}

**Validated at**: {timestamp}
**Result**: {PASS | FAIL | PASS_WITH_WARNINGS}

## Mandatory criteria

| ID | Criterion | Status | Details |
|----|-----------|--------|---------|
| 1 | All steps marked | PASS | 8 done, 1 skipped (justified), 0 failed |
| 2 | Sprint goal addressed | PASS | "achieved" stated in checkin |
| 3 | Increment artifacts | PASS | All 3 files exist, valid format |
| 4 | HANDOFF.md updated | PASS | New section added, all required sections present |
| 5 | Test-first compliance | PASS | All 4 prod changes preceded by tests |
| 6 | Test increment | PASS | 5 test files modified |
| 7 | Internal SE review | PASS | Verdict: PASS, 2 minor findings logged |

## Conditional criteria

| ID | Criterion | Applicable | Status |
|----|-----------|------------|--------|
| 8 | External Codex review | YES (codex-plugin-cc installed) | PASS |
| 9 | ADR for arch decisions | NO (no arch changes detected) | N/A |
| 10 | Rollback plan | NO | N/A |
| 11 | No regressions | YES (code changes) | PASS |
| 12 | LSP no errors | YES | PASS |
| 13 | Mutation score | NO (mutation_testing disabled) | N/A |

## Verdict

**PASS** - All mandatory and applicable conditional criteria met.
Sprint can close.
```

### 5. Return verdict

To sprint-orchestrator:
- PASS → proceed to internal SE review (if not yet) или close sprint
- FAIL → BLOCK `/sprint:complete`, return errors to executor

If FAIL - executor must address blocking criteria и retry `/sprint:complete`.

## Auto-detection logic

Some criteria require detection:

### Production code change detection

```python
production_paths = config.discipline.test_first.production_paths
auto_exempt_paths = config.discipline.test_first.auto_exempt_paths

def is_production_change(file_path):
    if matches_any(file_path, auto_exempt_paths):
        return False
    if matches_any(file_path, production_paths):
        return True
    # Default: source files in src/, app/, lib/ are production
    return False
```

### Architectural change detection

```python
def has_architectural_changes(diff):
    indicators = [
        'package.json' in diff and 'dependencies' in diff,
        'requirements.txt' in diff or 'pyproject.toml' in diff,
        bool(re.search(r'/auth/', diff)),
        bool(re.search(r'/api/.*\.(py|ts|go)$', diff)),
        'migration' in diff.lower() and 'CREATE TABLE' in diff,
    ]
    return any(indicators)
```

### Risky change detection

```python
def has_risky_changes(diff):
    return any([
        'DROP TABLE' in diff,
        'DROP COLUMN' in diff,
        bool(re.search(r'migrations/.*\.py', diff)),
        'data deletion' in commit_message.lower(),
    ])
```

## Override mechanism

If executor genuinely cannot satisfy criterion - escalation:

```
/sprint:complete --force "Reason for waiving DoD criteria"
```

`--force`:
- Logged extensively
- Triggers extra audit step (force-justification report)
- In strict mode: still blocks if mandatory criteria fail
- Use ONLY when criterion is genuinely impossible (rare)

## Output

`.sprints/active/dod-validation-sprint-{N}.md` with full report.
Updated `_state.json` with validation result.

If PASS: sprint can proceed to closure.
If FAIL: sprint cannot close, executor must address.
