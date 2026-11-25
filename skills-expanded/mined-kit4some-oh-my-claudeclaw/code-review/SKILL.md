<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: code-review
description: >
  Multi-pass code review with scope drift detection and Fix-First heuristic.
  Triggers on "코드 리뷰", "리뷰해줘", "PR 확인", "code review", "review this",
  "check my code", "review PR", "코드 검토". Pass 1 auto-fixes mechanical issues;
  Pass 2 security audit; Pass 3 flags judgment-required items. WTF-likelihood safety gate.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---

# Code Review — Multi-Pass Review with Scope Drift Detection

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

## Step 1 — Branch & Diff Setup

```bash
git branch --show-current
```

If on base branch: "Nothing to review — you're on the base branch." Stop.

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

```bash
git fetch origin $BASE --quiet
git diff origin/$BASE --stat
```

If no diff: stop.

---

## Step 1.5 — Scope Drift Detection

Before reviewing code quality, check: **did they build what was requested?**

1. Read `TODOS.md` (if exists). Read PR description (`gh pr view --json body -q .body 2>/dev/null`).
   Read commit messages (`git log origin/$BASE..HEAD --oneline`).
2. Identify the **stated intent** — what was this branch supposed to accomplish?
3. Compare files changed against stated intent.
4. Evaluate:

   **SCOPE CREEP**: Files changed unrelated to intent. "While I was in there..." changes.
   **MISSING REQUIREMENTS**: Requirements not addressed in the diff. Partial implementations.

5. Output:
   ```
   Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
   Intent: <1-line summary>
   Delivered: <1-line summary of what diff actually does>
   ```

This is **INFORMATIONAL** — does not block the review.

---

## Step 2 — Pass 1: Mechanical Review via OMC `code-reviewer` (opus)

**Pre-review diagnostics via OMC tools:**
```bash
# Run LSP diagnostics on all changed directories
lsp_diagnostics_directory("<changed-directory>")

# Search for known anti-patterns via AST
ast_grep_search(pattern: "$FUNC($$$ARGS)", lang: "typescript")
```

Use LSP/AST findings to inform the code-reviewer agent delegation.

```
Agent(subagent_type: "oh-my-claudecode:code-reviewer", prompt: "
  Review diff: git diff origin/$BASE
  Check: SQL injection, XSS, CSRF, secrets, race conditions, magic numbers,
  dead code, stale comments, N+1 queries, style violations.

  Classify each finding:
  - AUTO-FIX: Safe to fix automatically (dead code, style, stale comments)
  - ASK: Requires judgment (architecture, security tradeoffs, API design)

  Auto-fix all AUTO-FIX items. Report: [AUTO-FIXED] [file:line] Problem → Fix
")
```

---

## Step 2.5 — Pass 2: Security Review via OMC `security-reviewer` (parallel)

Run **in parallel** with Pass 1:

```
Agent(subagent_type: "oh-my-claudecode:security-reviewer", prompt: "
  Security audit: git diff origin/$BASE
  Check OWASP Top 10, secrets exposure, unsafe deserialization,
  dependency vulnerabilities, auth/authz gaps.
  Report severity-rated findings. Do NOT auto-fix.
")
```

---

## Step 3 — Pass 3: Deep Analysis (Judgment Required)

Merge results from both agents. For each ASK item, present via AskUserQuestion:

```
Auto-fixed {N} issues. {K} need your input:

1. [CRITICAL] file:line — Problem description
   Fix: Recommendation
   → A) Fix  B) Skip

2. [INFORMATIONAL] file:line — Problem description
   Fix: Recommendation
   → A) Fix  B) Skip

RECOMMENDATION: {overall recommendation}
```

---

## Step 3.5 — Documentation Staleness Check

Cross-reference diff against .md files in repo root:
- If code changed but related docs NOT updated → INFORMATIONAL finding
- "Documentation may be stale: [file] describes [feature] but code changed."

---

## Step 4 — Verification of Claims

Before producing final output:
- If you claim "this pattern is safe" → cite the specific line
- If you claim "handled elsewhere" → read and cite the handling code
- If you claim "tests cover this" → name the test file and method
- **Never say "likely handled" or "probably tested"** — verify or flag as unknown

---

## WTF-Likelihood Safety Gate

| Action | Risk Delta |
|--------|-----------|
| Revert a file | +15% |
| Modify 3+ files | +5% per file beyond 3 |
| Change public API | +10% |
| Modify test fixtures | +5% |
| Touch configuration | +8% |

- **> 20%**: Pause, ask user
- **> 40%**: Full risk breakdown, recommend incremental approach
- **Hard cap**: 50 changes max

---

## Review Report

```
═══════════════════════════════════════
Code Review Report
═══════════════════════════════════════
Scope Check: {CLEAN/DRIFT/MISSING}
Pass 1 — Auto-Fixed: {N} issues across {M} files
Pass 2 — Security: {K} findings ({severity breakdown})
Pass 3 — Flagged: {J} items requiring decision
Doc Staleness: {any stale docs}
WTF-Likelihood: {percentage}%
Overall Health: {Good / Needs Attention / Significant Issues}
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
