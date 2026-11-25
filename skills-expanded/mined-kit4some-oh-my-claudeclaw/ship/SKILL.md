<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: ship
description: >
  Automated release workflow with comprehensive quality gates. Triggers on "배포",
  "릴리스", "ship it", "PR 만들어", "release", "deploy", "create PR", "push this",
  "ship". Non-interactive: user says /ship, next thing they see is the PR URL.
  Delegates commit organization to OMC git-master, review to code-reviewer,
  verification to verifier. Sends PR notification via messenger.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---

# Ship — Fully Automated Release Workflow

You are running the `/ship` workflow. This is **non-interactive, fully automated**.
Do NOT ask for confirmation at any step. The user said `/ship` which means DO IT.
Run straight through and output the PR URL at the end.

**Only stop for:**
- On the base branch (abort)
- Merge conflicts that can't be auto-resolved
- Test failures
- Pre-landing review finds ASK items needing user judgment
- MINOR or MAJOR version bump needed

**Never stop for:**
- Uncommitted changes (always include them)
- PATCH/MICRO version bump (auto-pick)
- CHANGELOG content (auto-generate from diff)
- Commit message approval (auto-commit)

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

---

## Step 0 — Base Branch Detection

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

## Step 1 — Pre-flight Checks

1. Check current branch. If on base branch, **abort**: "You're on the base branch. Run /ship from a feature branch."
2. Run `git status` (never use `-uall`). Uncommitted changes are always included.
3. Run `git diff $BASE...HEAD --stat` and `git log $BASE..HEAD --oneline` to understand what's being shipped.

---

## Step 2 — Merge Base Branch (BEFORE tests)

Fetch and merge the base branch so tests run against the merged state:

```bash
git fetch origin $BASE && git merge origin/$BASE --no-edit
```

If merge conflicts: try auto-resolve simple ones. If complex, **STOP** and show them.
If already up to date: continue silently.

---

## Step 2.5 — Test Framework Bootstrap

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

---

## Step 3 — Run Tests (on merged code)

Run detected test command:
```bash
$TEST_CMD 2>&1 | tee /tmp/ship_tests.txt
```

**If any test fails:** Show failures and **STOP**. Do not proceed.
**If all pass:** Continue — note counts briefly.

**Post-test LSP diagnostics:**

If OMC LSP tools are available, run diagnostics on changed files:
```
lsp_diagnostics_directory("<changed-directory>")
```
Flag any type errors, unused imports, or lint issues that tests might not catch.

---

## Step 3.4 — Test Coverage Audit

Delegate to OMC test-engineer for coverage analysis:

```
Agent(subagent_type: "oh-my-claudecode:test-engineer", prompt: "
  Analyze test coverage for the diff: git diff origin/$BASE...HEAD
  1. Trace every changed codepath
  2. Map each branch against existing tests
  3. Output ASCII coverage diagram with [TESTED] and [GAP] markers
  4. Generate tests for uncovered paths (max 20 tests)
  5. Run generated tests, commit passing ones
")
```

**Fast path:** All paths covered → "Step 3.4: All new code paths have test coverage ✓"

---

## Step 3.5 — Pre-Landing Review

Delegate to OMC code-reviewer for structural review:

```
Agent(subagent_type: "oh-my-claudecode:code-reviewer", prompt: "
  Review diff: git diff origin/$BASE
  Two-pass review:
  Pass 1 (CRITICAL): SQL safety, race conditions, secrets exposure, auth gaps
  Pass 2 (INFORMATIONAL): Dead code, magic numbers, style, N+1 queries

  Classify each finding as AUTO-FIX or ASK.
  AUTO-FIX: apply directly, report one line per fix.
  ASK: collect for user decision.
")
```

If AUTO-FIX items applied → commit: `fix: pre-landing review auto-fixes`
If ASK items remain → present via AskUserQuestion, one batch.

---

## Step 4 — Version Bump (auto-decide)

If VERSION file exists:
1. Count lines changed: `git diff origin/$BASE...HEAD --stat | tail -1`
2. Auto-decide: <50 lines → MICRO/PATCH, 50+ → PATCH, major feature → ask MINOR
3. Write new version, reset lower digits to 0

If no VERSION file: skip this step.

---

## Step 5 — CHANGELOG (auto-generate)

If CHANGELOG.md exists:
1. Read header for format
2. Generate from ALL commits: `git log $BASE..HEAD --oneline`
3. Categorize: Added / Changed / Fixed / Removed
4. Insert after header, dated today
5. Do NOT ask the user — infer from diff

---

## Step 5.5 — TODOS.md Auto-Update

If TODOS.md exists:
1. Cross-reference diff against open TODOs
2. Mark completed items (conservative — only clear evidence)
3. Move to Completed section with version and date

---

## Step 6 — Bisectable Commits

Organize changes into logical, independently valid commits:

| Order | Category |
|-------|----------|
| 1 | Infrastructure (deps, config, CI) |
| 2 | Data/Schema (migrations, types) |
| 3 | Core logic (services, controllers) |
| 4 | Tests |
| 5 | VERSION + CHANGELOG + TODOS.md |

Each commit: conventional message, independently valid, no broken imports.
Final commit gets co-author trailer:
```
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

---

## Step 6.5 — Verification Gate (Iron Law)

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

Before pushing, if ANY code changed after Step 3's test run:
1. Re-run test suite. Paste fresh output.
2. Run build if applicable.

Rationalization prevention:
- "Should work now" → RUN IT.
- "Confident" → Confidence is not evidence.
- "Already tested" → Code changed. Test again.

If tests fail: **STOP**. Fix and return to Step 3.

---

## Step 7 — Push

```bash
git push -u origin $(git rev-parse --abbrev-ref HEAD)
```

---

## Step 8 — Create PR

```bash
gh pr create --base $BASE --title "<type>: <summary>" --body "$(cat <<'EOF'
## Summary
<bullet points from CHANGELOG>

## Test Coverage
<coverage diagram from Step 3.4>

## Pre-Landing Review
<findings from Step 3.5>

## Test Plan
- [x] All tests pass
- [x] Pre-landing review complete
- [x] Verification gate passed

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Output the PR URL.

---

## Step 9 — Record & Notify

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

```
memory_daily_log(entry: "Shipped: {PR title} #{PR number}", type: "done")
messenger_send(platform: "all", message: "✅ [ship] PR created: {PR URL}\n{summary}")
```

---

## Safety Rules

1. Never push to main/master directly
2. Never force push without explicit user request
3. Always run tests before creating PR
4. Never skip hooks (--no-verify)
5. Verify branch is not main before any push

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
