---
name: git-pr-review-local
description: Review local changes as if they were a pull request — shows the full review in the conversation without posting to GitHub. Use this skill whenever the user wants a PR review shown locally. Trigger on phrases like "pr review", "review this", "review my changes", "코드 리뷰", "pr 리뷰해줘", "리뷰해줘", "변경사항 리뷰". Use this skill (not git-pr-review-comments) when the user does NOT mention posting or leaving comments on GitHub.
---

Review the current PR (or local diff) and present the full analysis in the conversation.

## Steps

0. **Check prerequisites** — run as a single Bash call:
   ```bash
   git rev-parse --git-dir 2>/dev/null && gh auth status 2>/dev/null
   ```
   If `git rev-parse` fails, tell the user this must be run inside a git repository and stop.
   If `gh auth status` fails, tell the user to run `gh auth login` first and stop.

1. **Get the diff** — try in order, use the first that succeeds:

   a. If a PR is associated with the current branch:
   ```bash
   gh pr diff --color=never 2>/dev/null
   ```

   b. If no PR exists, find the merge base and diff from there — run as a single Bash call:
   ```bash
   BASE=$(git merge-base HEAD origin/main 2>/dev/null \
     || git merge-base HEAD origin/master 2>/dev/null \
     || git rev-parse --verify HEAD~1 2>/dev/null \
     || git rev-list --max-parents=0 HEAD) && \
   git diff "$BASE"...HEAD
   ```
   Note: the `git rev-list --max-parents=0 HEAD` fallback handles the initial commit case by diffing from the repo root.

2. **Get PR context** (if a PR exists):
   ```bash
   gh pr view --json title,body,baseRefName,headRefName 2>/dev/null
   ```

3. **Analyze** the diff against the review criteria below.
   - If the diff is very large (>500 lines), focus on the highest-risk areas: new files, deleted validations, changed auth/security logic, and altered interfaces. Don't attempt to exhaustively review every line — prioritize signal over coverage.

4. **Output** the full review using the markdown template below — nothing else before or after.

## Review criteria

Evaluate each changed file for:
- **Correctness** — logic errors, off-by-ones, wrong conditions, missing null checks
- **Security** — injection risks, exposed secrets, insecure defaults, OWASP top 10
- **Performance** — unnecessary loops, N+1 queries, blocking calls, large allocations
- **Maintainability** — naming clarity, code duplication, overly complex logic
- **Test coverage** — missing tests for new logic, untested edge cases
- **Style** — consistency with the surrounding codebase, dead code

Severity definitions:
- **Critical** — must fix before merge; correctness, security, or data-loss risk
- **Major** — should fix before merge; significant impact on quality or behavior
- **Minor** — nice to fix; style, naming, small improvements

## Output template

Use this exact structure every time. Keep section headers identical — they're used for parsing.

```markdown
## PR Review

**Branch:** `<head>` → `<base>`  
**Files changed:** <N>  

---

### ✅ Well done
- <specific thing done well>

---

### 🔴 Critical
- **`<file>:<line>`** — <concise description of the problem and why it matters>

---

### 🟠 Major
- **`<file>:<line>`** — <description>

---

### 🟡 Minor
- **`<file>:<line>`** — <description>

---

### 📋 Summary
<2–3 sentence overall assessment. State the risk level to merge as-is.>
```

## Rules

- Always include at least one "Well done" item — find something real, not generic praise.
- Omit Critical/Major/Minor sections entirely if there are no findings in that category — don't include empty sections.
- Cite exact file and line numbers whenever possible. Never say "somewhere in the code".
- Do not repeat the diff back. Just the findings.
- If the diff is empty, say so and stop.
- Write in the same language the user used to invoke the skill (Korean → Korean review, English → English review).
