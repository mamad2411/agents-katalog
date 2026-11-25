---
name: review-prod-ready
description: Use when comprehensive production-readiness code review is needed after implementation — dispatches up to 7 specialized parallel reviewers covering tests, plan completeness, architecture, complexity, DRY violations, suppressed warnings, and production readiness
argument-hint: [description or plan path]
effort: high
allowed-tools: Agent, Bash, Read, Grep, Glob
---

# Production-Ready Code Review

Dispatches up to 7 specialized review subagents **in parallel**. Each reviewer focuses on ONE dimension deeply, catching issues a single broad reviewer misses.

## Git Context (auto-detected)

**HEAD:** !`git rev-parse --short HEAD 2>/dev/null || echo "not a git repo"`
**Base:** !`git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null || echo "no base found"`
**Changed files:**
!`git diff --stat $(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null) HEAD 2>/dev/null || echo "run git diff manually"`

## Process

### 1. Read reviewer prompts

Read `${CLAUDE_SKILL_DIR}/reviewers.md` for the detailed prompt for each of the 7 reviewers.

### 2. Dispatch reviewers in parallel

Dispatch ALL applicable reviewers simultaneously using the Agent tool. Pass each reviewer:
- The git range from the context above
- The list of changed files above
- Their specific prompt from `reviewers.md`
- User context if provided: $ARGUMENTS

Each agent should:
- Read full content of changed files (not just the diff — bugs hide in unchanged lines nearby)
- Focus ONLY on their assigned dimension
- Output findings in the structured format below

**Skip reviewers that don't apply** (e.g., skip Plan Completeness if no plan exists, reduce count for small diffs <5 files).

### 3. Aggregate results

**Aggregation rules — do NOT soften findings:**
- Keep every reviewer's severity label EXACTLY as they assigned it. Do not downgrade Critical → Important to "seem balanced."
- Do not drop findings to shorten the report. If two reviewers flagged overlapping issues, merge them but preserve the HIGHER severity.
- Do not rewrite "what's wrong" descriptions to sound more polite. Keep the blunt language from the reviewer.
- The verdict at the bottom must reflect the findings, not a diplomatic compromise. If ANY Critical issue exists, verdict is **No** or **With fixes** — never **Yes**.
- If you feel tempted to soften a finding, that's a sign the reviewer was right and the author won't like it. Keep it.

After all reviewers complete, combine into a single report:

```
## Production Readiness Review

**Range:** BASE..HEAD | **Files:** N changed | **Date:** YYYY-MM-DD

### Critical Issues (must fix before merge)
[Combined from all reviewers, deduplicated, with source reviewer noted]

### Important Issues (should fix)
[Combined, deduplicated]

### Minor Issues (nice to have)
[Combined, deduplicated]

### Suppression Audit
| File:Line | Directive | Verdict | Reason |
|-----------|-----------|---------|--------|

### Verdict
**Ready to merge?** Yes / No / With fixes
**Top risks if merged as-is:**
1. ...
2. ...
3. ...
```

## Issue Format (for each reviewer)

Each finding must include:
- **Severity:** Critical / Important / Minor
- **File:line** reference
- **What's wrong** (specific, not vague)
- **Why it matters** (impact if not fixed)
- **Suggested fix** (if not obvious)
