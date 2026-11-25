---
name: git-pr-review-comments
description: Review the current PR and post the review as a GitHub comment. Use this skill whenever the user wants the review posted to GitHub as a PR comment. Trigger on phrases like "post review", "leave a review on the pr", "pr review comment", "pr에 코멘트", "pr 리뷰하고 코멘트 남겨줘", "리뷰 코멘트 달아줘", "github에 리뷰 남겨". Use this skill (not git-pr-review-local) when the user explicitly wants the review posted to GitHub.
---

Review the current PR and post the full analysis as a GitHub PR comment.

## Steps

0. **Check prerequisites** — run as a single Bash call:
   ```bash
   git rev-parse --git-dir 2>/dev/null && gh auth status 2>/dev/null
   ```
   If `git rev-parse` fails, tell the user this must be run inside a git repository and stop.
   If `gh auth status` fails, tell the user to run `gh auth login` first and stop.

1. **Verify a PR exists:**
   ```bash
   gh pr view --json number,title,baseRefName,headRefName,url 2>/dev/null
   ```
   If no PR exists, tell the user and stop — do not proceed.

2. **Get the diff:**
   ```bash
   gh pr diff --color=never 2>/dev/null
   ```

3. **Analyze** the diff using the review criteria below.
   - If the diff is empty, tell the user and stop — do not post.
   - If the diff is very large (>500 lines), focus on the highest-risk areas: new files, deleted validations, changed auth/security logic, and altered interfaces.

4. **Compose the full review** using the template below, then **write it to a temp file** using the Write tool (not a bash heredoc — shell escaping will corrupt multi-line markdown):
   - Write the complete review markdown to: `/tmp/pr_review_claude.md`
   - Encoding must be UTF-8.

5. **Show the review in the conversation** and ask: "이 내용을 PR에 코멘트로 남길까요? (Post this as a PR comment?)"

6. **If the user confirms**, post the comment — use the PR number captured in step 1:
   ```bash
   gh pr comment $(gh pr view --json number -q .number) --body-file /tmp/pr_review_claude.md
   ```

7. **Clean up:**
   ```bash
   rm -f /tmp/pr_review_claude.md
   ```

8. Output the PR URL and confirm the comment was posted.

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

## Comment template

Use this exact structure every time. The headers must stay identical.

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

---
*Posted by Claude Code*
```

## Rules

- Always write the review using the Write tool to `/tmp/pr_review_claude.md`, then post with `--body-file`. Never pass the body directly as a shell argument — special characters will break.
- Always show the review to the user before posting and ask for confirmation.
- Always include at least one "Well done" item — find something real, not generic praise.
- Omit Critical/Major/Minor sections entirely if there are no findings in that category — don't include empty sections.
- Cite exact file and line numbers whenever possible. Never say "somewhere in the code".
- Do not post if the diff is empty. Tell the user instead.
- Write review content in the same language the user used to invoke the skill (Korean → Korean review, English → English review).
