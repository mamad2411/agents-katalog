<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: qa
description: >
  Systematically QA test code and fix bugs found. Run tests, find failures,
  fix them with atomic commits, re-verify. Triggers on "qa", "QA", "테스트",
  "find bugs", "test and fix", "버그 찾아서 고쳐", "품질 검사".
  Three tiers: Quick (critical/high), Standard (+ medium), Exhaustive (+ cosmetic).
  Produces before/after health scores, fix evidence, and ship-readiness summary.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# /qa — Test → Fix → Verify

You are a QA engineer AND a bug-fix engineer. Run tests, find failures, fix them
in source code with atomic commits, then re-verify. Produce a structured report
with before/after evidence.

## Preamble

Before executing this skill:

1. **Load context from memory**:
   ```
   memory_search(query: "{skill-relevant-query}", associative: true, limit: 5)
   memory_search(tag: "{skill-name}", limit: 3)
   ```
   Review returned memories for relevant past context, decisions, and patterns.

2. **Check OMC state for active work**:
   ```
   state_get_status()
   ```
   If conflicting active tasks exist, warn the user before proceeding.

3. **Detect current branch** (for git-related skills):
   ```bash
   git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "not-a-git-repo"
   ```

4. **Check proactive mode**:
   ```
   state_read("occ-proactive")
   ```
   If `"false"`: do NOT proactively suggest other OpenClaw-CC skills during this session.
   Only run skills the user explicitly invokes.

5. **Log skill activation**:
   ```
   memory_daily_log(type: "note", entry: "Skill activated: /{skill-name}")
   ```

## Memory Context Loading

Before starting work, load relevant context from the 3-layer memory system:

```
# Search for related past work
memory_search(query: "{task description}", associative: true, limit: 5)

# Search by relevant tags
memory_search(tag: "{relevant-tag}", limit: 3)

# Check for recent related daily logs
memory_search_date(start: "{7 days ago}", end: "{today}", category: "daily-logs", limit: 5)
```

**Use retrieved context to**:
- Avoid repeating past mistakes
- Build on previous decisions
- Maintain consistency with established patterns
- Reference related knowledge graph nodes

If critical related memories exist, summarize them before proceeding:
```
Found {N} related memories:
- {memory_1 title}: {brief relevance}
- {memory_2 title}: {brief relevance}
```

## Setup

**Parse the user's request for parameters:**

| Parameter | Default | Override example |
|-----------|---------|-----------------|
| Tier | Standard | `--quick`, `--exhaustive` |
| Scope | Full project (or diff-scoped) | `Focus on the auth module` |

**Tiers determine which issues get fixed:**
- **Quick:** Fix critical + high severity only
- **Standard:** + medium severity (default)
- **Exhaustive:** + low/cosmetic severity

**If on a feature branch with no specific scope:** Automatically enter **diff-aware mode** —
focus testing on changed files via `git diff origin/$BASE --name-only`.

**Check for clean working tree:**
```bash
git status --porcelain
```

If dirty, AskUserQuestion:
"Your working tree has uncommitted changes. /qa needs a clean tree so each bug fix gets its own atomic commit."
- A) Commit my changes — commit all current changes with a descriptive message, then start QA
- B) Stash my changes — stash, run QA, pop the stash after
- C) Abort — I'll clean up manually

RECOMMENDATION: A — uncommitted work should be preserved as a commit before QA adds its own fix commits.

## Base Branch Detection

Detect the correct base branch for diff and PR operations:

```bash
# Method 1: Check if there's an existing PR for this branch
BASE=$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null)

# Method 2: Check repo default branch
if [ -z "$BASE" ]; then
  BASE=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null)
fi

# Method 3: Fallback to common defaults
if [ -z "$BASE" ]; then
  if git show-ref --verify --quiet refs/heads/main 2>/dev/null; then
    BASE="main"
  elif git show-ref --verify --quiet refs/heads/master 2>/dev/null; then
    BASE="master"
  else
    BASE="main"
  fi
fi

echo "Base branch: $BASE"
```

Use `$BASE` for all subsequent operations:
- `git diff origin/$BASE...HEAD` — Changes on this branch
- `git log origin/$BASE..HEAD` — Commits on this branch
- `gh pr create --base $BASE` — PR targeting correct branch

---

## Phase 1 — Test Framework Detection

## Test Framework Detection & Bootstrap

Detect the project's test framework automatically:

```bash
# Check package.json for test command
TEST_CMD=""
if [ -f "package.json" ]; then
  TEST_CMD=$(node -e "try{const p=require('./package.json');console.log(p.scripts&&p.scripts.test||'')}catch(e){}" 2>/dev/null)
fi

# Check for common test runners
if [ -z "$TEST_CMD" ]; then
  if [ -f "jest.config.js" ] || [ -f "jest.config.ts" ]; then
    TEST_CMD="npx jest"
  elif [ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ]; then
    TEST_CMD="npx vitest run"
  elif [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
    TEST_CMD="python -m pytest"
  elif [ -f "Cargo.toml" ]; then
    TEST_CMD="cargo test"
  elif [ -f "go.mod" ]; then
    TEST_CMD="go test ./..."
  fi
fi

if [ -n "$TEST_CMD" ]; then
  echo "Test command detected: $TEST_CMD"
else
  echo "No test framework detected"
fi
```

**If no test framework detected**:
- Check CLAUDE.md for test commands
- Ask the user if they have a preferred test command
- If none available, skip test-dependent steps and note in output

**Usage**: Run detected command with `$TEST_CMD`

If no test framework detected: ask the user for test command or abort.

---

## Phase 2 — Baseline Test Run

```bash
$TEST_CMD 2>&1 | tee /tmp/qa_baseline.txt
```

Record:
- Total tests, passed, failed, skipped
- Error messages and stack traces
- Baseline health score: `passed / total * 100`

---

## Phase 3 — Failure Triage

For each failure, classify severity:

| Severity | Criteria | Example |
|----------|----------|---------|
| Critical | Crash, data loss, security | Uncaught exception, SQL injection |
| High | Feature broken, incorrect output | Wrong calculation, missing validation |
| Medium | Edge case failure, degraded UX | Timeout on large input, wrong error message |
| Low | Cosmetic, minor inconsistency | Formatting, log noise, deprecation warning |

Sort by severity descending.

---

## Phase 4-6 — Root Cause Analysis

For each failure (in severity order):
1. Read the failing test and its target code
2. Trace the code path from test assertion to failure point
3. Identify the root cause (use Grep/Glob to find related code)
4. Classify: Is this a source bug or a test bug?

---

## Phase 7 — Triage Decision

Apply tier filter:
- **Quick:** Fix critical + high only. Mark medium/low as "deferred"
- **Standard:** Fix critical + high + medium. Mark low as "deferred"
- **Exhaustive:** Fix all

Issues that cannot be fixed from source (external dependency, infra) → always "deferred".

---

## Phase 8 — Fix Loop

For each fixable issue, in severity order:

### 8a. Locate source
```bash
# Grep for error messages, function names, route definitions
```

### 8b. Fix
- Read source code, understand context
- Make **minimal fix** — smallest change that resolves the issue
- Do NOT refactor surrounding code or add features

### 8c. Commit
```bash
git add <only-changed-files>
git commit -m "fix(qa): ISSUE-NNN — short description"
```
One commit per fix. Never bundle.

### 8d. Re-test
```bash
$TEST_CMD 2>&1 | tee /tmp/qa_retest.txt
```
Verify fix works AND no regressions.

### 8e. Classify
- **verified**: re-test confirms fix, no new errors
- **best-effort**: fix applied but couldn't fully verify
- **reverted**: regression detected → `git revert HEAD` → mark "deferred"

### 8e.5. Regression Test Generation

If classification is "verified" and test framework detected:

Delegate to OMC test-engineer:
```
Agent(subagent_type: "oh-my-claudecode:test-engineer", prompt: "
  Write a regression test for ISSUE-NNN:
  - Bug: {what was broken}
  - Root cause: {why it broke}
  - Fix: {what was changed}
  Match existing test conventions exactly.
  Test MUST fail without fix, pass with fix.
")
```

If test passes → commit: `test(qa): regression test for ISSUE-NNN`
If fails → delete, defer.

### 8f. WTF-Likelihood Self-Regulation

Every 5 fixes (or after any revert), compute:

```
WTF-LIKELIHOOD:
  Start at 0%
  Each revert:                +15%
  Each fix touching >3 files: +5%
  After fix 15:               +1% per additional fix
  All remaining Low severity: +10%
  Touching unrelated files:   +20%
```

**If WTF > 20%:** STOP immediately. Show progress. Ask whether to continue.
**Hard cap: 50 fixes.** Stop regardless.

---

## Phase 9 — Final QA

After all fixes:
1. Re-run full test suite
2. Compute final health score
3. **If final score WORSE than baseline:** WARN prominently

---

## Phase 10 — Report

```
═══════════════════════════════════════
QA REPORT
═══════════════════════════════════════
Tier:           {Quick / Standard / Exhaustive}
Baseline:       {passed}/{total} ({X}%)
Final:          {passed}/{total} ({Y}%)
Delta:          {+/-Z}%

Issues Found:   {N}
  Fixed:        {M} (verified: {a}, best-effort: {b})
  Reverted:     {c}
  Deferred:     {d}

Regression Tests: {generated}/{committed}
WTF-Likelihood:   {percentage}%
Ship-Ready:       {Yes / No — reason}
═══════════════════════════════════════
```

## Memory Persistence

After completing the workflow, persist results to the 3-layer memory system:

### Required Actions

1. **Log completion to daily log**:
   ```
   memory_daily_log(type: "done", entry: "{skill-name}: {brief result summary}")
   ```

2. **Store significant findings** (importance ≥ 6):
   ```
   memory_store(
     category: "{appropriate category}",
     title: "{descriptive title}",
     content: "{structured result content}",
     tags: ["{skill-name}", "{project}", "{relevant-tags}"],
     importance: {6-10 based on significance}
   )
   ```

3. **Link to related memories** (if applicable):
   ```
   memory_link(source: "{new_memory_id}", target: "{related_id}", relation: "{related|derived|refines}")
   ```

### Category Routing

| Content Type | Category | Subcategory |
|-------------|----------|-------------|
| Bug fix / debugging | knowledge | debugging |
| Code review results | projects | {project-name} |
| Design decisions | projects | {project-name} |
| Research findings | knowledge | {topic} |
| Release / deploy | projects | {project-name} |
| Person-related info | people | — |
| Task / action item | tasks | — |

```
memory_store(category: "projects", title: "QA Report: {scope}",
  tags: ["qa", "{project}"], importance: 7)
```

## Messenger Notification

Send notifications for significant events via messenger:

### When to Notify

| Event | Platform | Priority |
|-------|----------|----------|
| Task/pipeline completed | telegram | Normal |
| Verification failed | telegram | High |
| Long-running task done (10+ min) | telegram | Normal |
| Critical error or blocker | telegram | High |
| PR created / release shipped | all | Normal |
| Importance ≥ 8 memory created | telegram | Normal |

### Notification Format

```
messenger_send(
  platform: "telegram",
  message: "[{skill-name}] {status_emoji} {brief description}\n\n{details if relevant}"
)
```

**Status Emojis**:
- Completed successfully: ✅
- Completed with warnings: ⚠️
- Failed / blocked: ❌
- Needs attention: 🔔

### Do NOT Notify

- Routine memory operations
- Intermediate progress steps
- Read-only operations (search, list, status)

## Completion Status Protocol

Every skill must end with one of these status codes:

| Code | Meaning | When to Use |
|------|---------|-------------|
| **DONE** | All steps completed, evidence provided | Root cause found + fix verified, PR created, review finished |
| **DONE_WITH_CONCERNS** | Completed with warnings or caveats | Tests pass but coverage dropped, fix applied but can't fully verify |
| **BLOCKED** | Cannot proceed, requires user intervention | 3 failed attempts, missing permissions, external dependency down |
| **NEEDS_CONTEXT** | Missing information to continue | Unclear requirements, need user clarification |

### Escalation Rules

1. **3-strike rule**: After 3 failed attempts at any step, **STOP** and escalate to user.
   Do not continue guessing. Present what was tried and ask for direction.

2. **Scope escalation**: If fix/change touches 5+ files unexpectedly, pause and confirm
   with the user before proceeding.

3. **Security uncertainty**: If you are unsure about a security implication, **STOP** and
   escalate. Never guess on security.

4. **Verification requirement**: Never claim DONE without evidence.
   - "Should work" → RUN IT. Confidence is not evidence.
   - "Already tested earlier" → Code changed since. Test again.
   - "Trivial change" → Trivial changes break production.

### Output Format

```
═══════════════════════════════════════
Status: {DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT}
Summary: {one-line description of outcome}
Evidence: {test output, verification results, or blocking reason}
═══════════════════════════════════════
```
