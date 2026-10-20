# Comprehensive Code Review

Run a multi-lens review of the current branch's changes. Groups changed files into logical chunks, spawns specialized review agents for each chunk × review type in parallel, writes per-chunk reports, then consolidates everything into a single verdict.

**Arguments:** $ARGUMENTS

## Usage

```
/comp-review [--security] [--performance] [--reliability] [--general] [--all] [--base <branch>]
```

**Review types** (combine freely; omitting all type flags defaults to `--all`):
- `--security` — bearer auth, token storage, MSAL invariants, secrets, input validation
- `--performance` — async correctness, Graph API efficiency, pagination, token refresh overhead
- `--reliability` — concurrent safety, error recovery, resource lifecycle, startup/shutdown
- `--general` — architecture alignment, coding standards, correctness, testing completeness

**Options:**
- `--base <branch>` — diff against this branch (default: `main`)

**Examples:**
```
/comp-review --security
/comp-review --security --reliability
/comp-review --all
/comp-review --general --base develop
/comp-review                              # same as --all
```

---

## Step 1: Parse Arguments

Parse `$ARGUMENTS` to determine what to run.

**Review type flags** — scan for each and set a boolean:
- `--security` → `RUN_SECURITY=true`
- `--performance` → `RUN_PERFORMANCE=true`
- `--reliability` → `RUN_RELIABILITY=true`
- `--general` → `RUN_GENERAL=true`
- `--all` → all four true

If **no type flag is present at all**, treat as `--all` (all four enabled).

**Base branch** — look for `--base <value>`. If absent, `BASE_BRANCH=main`.

---

## Step 2: Collect Branch Context

Run these in parallel:

```bash
git branch --show-current
```

```bash
git diff $BASE_BRANCH...HEAD --stat --no-color
```

```bash
git log HEAD --not $(git rev-parse $BASE_BRANCH) --oneline 2>/dev/null | head -15
```

**If the diff stat returns nothing** (no changes vs base), report:
> "No changes vs `$BASE_BRANCH` — nothing to review."
and stop.

Get the full list of changed files:

```bash
git diff $BASE_BRANCH...HEAD --name-only --no-color
```

---

## Step 3: Group Files into Logical Chunks

Analyze the file list and produce named chunks. A chunk is a set of closely related files that should be reviewed together.

**Chunking rules:**

1. **Module boundary**: Separate files by top-level module:
   - `auth/` → Auth chunk
   - `graph/` → Graph API chunk
   - `tests/` → Tests chunk
   - `deploy/` → Deploy/Config chunk
   - Root files (`server.py`, `config.py`, `run_auth.py`) → Server Core chunk
   - `.github/`, `.claude/`, `Makefile`, `pyproject.toml`, `*.yml` → CI/Config chunk

2. **Co-location rule**: Always keep a source file and its test file in the same chunk. Never split `graph/mail.py` from `tests/test_mail.py`.

3. **Size limit**: If a chunk has more than 15 files, split by sub-module.

**Naming**: Give each chunk a short kebab-case slug:
`auth`, `graph-mail`, `graph-calendar`, `graph-contacts`, `graph-tasks`, `graph-client`, `server-core`, `tests`, `deploy`, `ci-config`

---

## Step 4: Prepare Per-Chunk Diffs

For each chunk, fetch its diff:

```bash
git diff $BASE_BRANCH...HEAD --no-color -- [file1] [file2] ...
```

For any **newly added files** in the chunk, also read the full file content using the Read tool so agents have complete context.

---

## Step 5: Create Output Directory

```bash
DATE=$(date +%Y-%m-%d)
BRANCH=$(git branch --show-current | sed 's/[^a-zA-Z0-9-]/-/g' | head -c 60)
OUTPUT_DIR="agent-projects/reviews/${DATE}-${BRANCH}"
mkdir -p "$OUTPUT_DIR"
for CHUNK_SLUG in [each chunk slug]; do
  mkdir -p "$OUTPUT_DIR/$CHUNK_SLUG"
done
```

Write a manifest so the consolidation agent knows what was reviewed:

```markdown
# Review Manifest: {BRANCH} vs {BASE_BRANCH}

**Date**: {DATE}
**Branch**: {BRANCH}
**Base**: {BASE_BRANCH}
**Review types**: {list of enabled types}

## Chunks

| Chunk | Files |
|-------|-------|
| {chunk-slug} | {comma-separated file list} |
```

Save as `{OUTPUT_DIR}/MANIFEST.md`.

---

## Step 6: Spawn All Review Agents in Parallel

**Spawn ALL agents in a single parallel batch.** Do not wait between chunks or types.

For every combination of (enabled review type) × (chunk), spawn one agent using the Task tool.

### Agent type → subagent_type mapping

| Flag | subagent_type | CI prompt file |
|------|--------------|----------------|
| `--security` | `security-reviewer` | `.claude/prompts/ci-security-review.md` |
| `--performance` | `performance-reviewer` | `.claude/prompts/ci-performance-review.md` |
| `--reliability` | `reliability-reviewer` | `.claude/prompts/ci-reliability-review.md` |
| `--general` | `principal-engineer` | `.claude/prompts/ci-pr-review.md` |

### Agent prompt template

```
You are performing a focused {REVIEW_TYPE} review of a specific chunk of code changes in the
cowork-mcp codebase. This is a **branch review** (not a PR review) — do not post to GitHub.

## Branch context
- Branch: {BRANCH}
- Base: {BASE_BRANCH}
- Chunk slug: {CHUNK_SLUG}
- Files in this chunk: {N}

## Changed files
{NEWLINE-SEPARATED FILE LIST}

## Diff
{CHUNK_DIFF}

{IF NEW FILES EXIST:}
## New file contents (added in this branch)
{FOR EACH NEW FILE: filename followed by full content}
{END IF}

---

## Your review checklist

Read `.claude/prompts/ci-{review-type}-review.md` for the full review checklist, finding
format, and severity definitions. Apply those standards exactly.

Key adaptations for this branch review (not a GitHub PR):
- Review ONLY changes in this diff — do not flag pre-existing issues
- **Do NOT post a GitHub PR comment** — write findings to a file (see output section)
- Apply the same severity levels, finding format, and verdict as defined in the CI prompt

## Required reading before reviewing
Before you review, read these files using your Read tool:
- `CLAUDE.md`
{REVIEW_TYPE_SPECIFIC_READS}

## Output

Write your findings to: `{OUTPUT_DIR}/{CHUNK_SLUG}/{REVIEW_TYPE}.md`

Use this exact structure:

---
# {REVIEW_TYPE_TITLE} Review: {CHUNK_SLUG}

**Date**: {DATE}
**Branch**: {BRANCH} vs {BASE_BRANCH}
**Files reviewed**: {N}
**Reviewer**: {subagent_type}

## Summary
[One paragraph assessment. Be specific about what was changed and whether it raises concerns.]

## Findings

[List all findings using the format from the CI prompt. If none, write:
"No findings — this chunk is clean from a {review-type} perspective."]

## Verdict
[Choose one:]
- ✅ PASS — no critical or important findings
- ⚠️ PASS WITH CHANGES — important findings exist; address before merge
- ❌ NEEDS REWORK — critical findings exist; must fix before merge
---

IMPORTANT: You must write this file. Do not return findings only in your response text.
Verify the file was written before finishing.
```

### Review-type-specific required reading

**Security:**
```
- `auth/token_store.py` — token storage invariants
- `server.py` — BearerAuthMiddleware implementation
```

**Performance:**
```
- `graph/client.py` — GraphClient singleton and HTTP client management
```

**Reliability:**
```
- `auth/token_store.py` — token storage and file locking patterns
- `graph/client.py` — GraphClient singleton lifecycle
```

**General:**
```
- `docs/CONTEXT.md` — architecture overview
```

---

## Step 7: Verify and Consolidate

After all agents complete:

1. Check that each expected output file was written:
   ```bash
   ls {OUTPUT_DIR}/**/*.md
   ```

2. Spawn a **general-purpose** agent to produce the consolidated report.

**Consolidation agent prompt:**

```
You are producing a consolidated code review report for a branch in the cowork-mcp codebase.

## Context
- Branch: {BRANCH}
- Base: {BASE_BRANCH}
- Date: {DATE}
- Review types run: {ENABLED_TYPES}
- Chunks reviewed: {N}

## Input: Read all these review files
{LIST OF ALL {OUTPUT_DIR}/{CHUNK}/{TYPE}.md files}

Also read `{OUTPUT_DIR}/MANIFEST.md` for the full chunk-to-file mapping.

## Your task

After reading all input files, produce a consolidated report at:
`{OUTPUT_DIR}/CONSOLIDATED.md`

### Deduplication rules
- If the same file+issue appears in multiple review types, merge into one finding and note which lenses caught it
- If the same anti-pattern appears in multiple chunks, list once with all file locations
- Keep distinct findings separate even if they are in the same file

### Verdict rules (strict precedence)
- ❌ NEEDS REWORK — if ANY per-chunk review is NEEDS REWORK
- ⚠️ PASS WITH CHANGES — if ANY per-chunk review is PASS WITH CHANGES (and none are NEEDS REWORK)
- ✅ PASS — only if every per-chunk review is PASS

### Output format

Write `{OUTPUT_DIR}/CONSOLIDATED.md` with this structure:

---
# Comprehensive Review: {BRANCH}

**Date**: {DATE}
**Branch**: {BRANCH} vs {BASE_BRANCH}
**Review types**: {ENABLED_TYPES}
**Chunks reviewed**: {N} | **Files reviewed**: {TOTAL_FILES}

## Executive Summary

[2-4 sentences. Overall health of the branch. Total critical/important/suggestion counts.
Call out the most significant finding. Be direct.]

**Finding counts**: 🔴 {N} critical | 🟡 {N} important | 🔵 {N} suggestions

---

## Overall Verdict

[❌ NEEDS REWORK / ⚠️ PASS WITH CHANGES / ✅ PASS]

[One sentence rationale — name the specific blocker(s) if rework needed.]

---

## 🔴 Critical Findings — Must Fix Before Merge

[If none: "No critical findings."]

### [File or feature area]
**Lens(es)**: {security | performance | reliability | general}
**File**: `path/to/file.py` (lines X-Y if known)

**Issue**: [What is wrong and how it could manifest]

**Recommendation**: [Specific fix]

**Rationale**: [Which invariant, OWASP category, or project rule this violates]

---

## 🟡 Important Findings — Should Fix Before Merge

### Security
[Findings...]

### Performance
[Findings...]

### Reliability
[Findings...]

### General
[Findings...]

---

## 🔵 Suggestions — Worth Considering

[Top suggestions only — cap at 10 total across all lenses.]

---

## Chunk × Review Matrix

| Chunk | Security | Performance | Reliability | General |
|-------|----------|-------------|-------------|---------|
| {chunk-slug} | ✅/⚠️/❌/— | ✅/⚠️/❌/— | ✅/⚠️/❌/— | ✅/⚠️/❌/— |

(Use — for review types that were not requested.)

---

*Generated by `/comp-review` · {DATE} · {BRANCH} vs {BASE_BRANCH}*
---

IMPORTANT: Write this file. Do not only return the content in your response text.
```

---

## Step 8: Report to User

After CONSOLIDATED.md is written, output a summary directly to the user:

```
## Comprehensive Review: {BRANCH}

**Base**: {BASE_BRANCH} | **Date**: {DATE}
**Chunks**: {N} | **Review types**: {ENABLED_TYPES}
**Output**: `agent-projects/reviews/{OUTPUT_DIR_NAME}/`

---

### Overall Verdict: [❌ NEEDS REWORK / ⚠️ PASS WITH CHANGES / ✅ PASS]

[Executive summary paragraph from CONSOLIDATED.md]

**Findings**: 🔴 {N} critical | 🟡 {N} important | 🔵 {N} suggestions

---

[IF any critical findings:]
### 🔴 Critical Findings ({N}) — Must Fix

[List each critical finding inline]

---

[IF important findings but no criticals:]
### 🟡 Important Findings ({N})

[Brief one-liner per finding, grouped by lens]

---

Full report: `agent-projects/reviews/{OUTPUT_DIR_NAME}/CONSOLIDATED.md`
Per-chunk reports: `agent-projects/reviews/{OUTPUT_DIR_NAME}/{chunk-slug}/`
```

---

## Notes

- **Parallel execution**: All review agents (Step 6) are spawned in a single parallel batch. With 3 chunks × 4 review types, that is 12 agents running concurrently.
- **Context discipline**: Each chunk agent sees ONLY its chunk's diff — not the full branch.
- **No GitHub posting**: This command writes to files. CI prompts are used as checklists — the actual `gh pr review` step is skipped.
- **Re-running**: Running `/comp-review` on the same branch on the same day overwrites that day's output directory. Rename the directory before re-running to preserve a run.
