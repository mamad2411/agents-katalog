---
name: resolve-review
description: Fetch GitHub PR review comments, address each concern in code, resolve the threads, and update the PR. Use when the user types /resolve-review, says "address review comments", "fix PR feedback", "resolve review issues", or "respond to code review".
---

# resolve-review

End-to-end workflow: fetch PR review comments → implement fixes → quality gates → mark resolved → update PR.

## Quick start

```
/resolve-review          # uses current branch's open PR
/resolve-review 42       # targets PR #42 explicitly
```

## Workflow

### 1. Identify the PR

```bash
# If no PR number given, find the open PR for current branch
gh pr view --json number,title,url,headRefName

# Or target a specific PR
gh pr view <number> --json number,title,url,headRefName,baseRefName
```

### 2. Fetch all review comments

```bash
# Fetch inline review comments (on specific lines)
gh api repos/{owner}/{repo}/pulls/<number>/comments \
  --jq '[.[] | {id, path, line, body, resolved: false, author: .user.login}]'

# Fetch top-level review thread summaries
gh pr view <number> --json reviews \
  --jq '.reviews[] | select(.state == "CHANGES_REQUESTED") | {author: .author.login, body: .body}'

# Fetch general (non-inline) PR comments
gh api repos/{owner}/{repo}/issues/<number>/comments \
  --jq '[.[] | {id, body, author: .user.login}]'
```

Group comments by file and by theme. Print a numbered list before touching any code:

```
[1] src/auth/middleware.ts:42 — @reviewer: "This leaks the error message to the client"
[2] src/routes/user.ts:88  — @reviewer: "Missing input validation on email field"
[3] (general)              — @reviewer: "Please add integration tests for the happy path"
```

State your understanding of each concern — especially ambiguous ones — before writing any code. If a comment is genuinely unclear, note it and skip (do not guess).

### 3. Implement fixes

Work through the list in file order to minimize context switching.

- Scope each change to exactly what the comment asks — no extra refactors
- Read the relevant file before editing it
- Commit after each logically distinct fix:

```bash
git add <files>
git commit -m "fix: <short description> (review comment #<comment-id>)"
```

Reference the comment ID so the fix is traceable.

### 4. Pre-push quality gates (ALL must pass)

Run these in order. Stop and fix before moving on if any fail.

```bash
# Type checking
npx tsc --noEmit          # TS projects
# mypy .                  # Python

# Lint
npm run lint              # JS/TS
# ruff check .            # Python

# Tests
npm test                  # or: pytest, go test ./..., cargo test, bun test
```

Check for merge conflicts before pushing:

```bash
git fetch origin
git merge-base --is-ancestor origin/<base-branch> HEAD || echo "REBASE NEEDED"
```

If behind, rebase cleanly:

```bash
git rebase origin/<base-branch>
```

**Do not push if any gate fails or conflicts remain.**

### 5. Push & resolve threads

```bash
git push origin HEAD
```

After pushing, resolve each comment thread you addressed:

```bash
# Resolve an inline review comment thread
gh api repos/{owner}/{repo}/pulls/<number>/comments/<comment-id>/replies \
  -X POST -f body="Addressed in <commit-sha> — <one-line explanation>"

# For top-level review threads, mark the review as seen via a reply-review:
gh api repos/{owner}/{repo}/pulls/<number>/reviews \
  -X POST \
  -f body="All CHANGES_REQUESTED items addressed. See commits for details." \
  -f event="COMMENT"
```

Only resolve threads for comments you actually fixed. Leave genuinely skipped ones open with an explanation reply.

### 6. Update the PR description

Append a "Review Response" section to the PR body:

```bash
CURRENT_BODY=$(gh pr view <number> --json body --jq '.body')

gh pr edit <number> --body "$(cat <<'EOF'
${CURRENT_BODY}

---

## Review response

| # | Comment | Resolution |
|---|---------|------------|
| 1 | @author: "..." | Fixed in <sha> — explain what changed |
| 2 | @author: "..." | Fixed in <sha> — explain what changed |
EOF
)"
```

Return the PR URL to the user.

## Edge cases

| Situation | Action |
|-----------|--------|
| No open PR on branch | Report the error, ask user to provide PR number |
| Comment is already resolved | Skip it, note it in your summary |
| Comment asks for design change, not code | Flag to user before implementing — don't guess intent |
| Quality gate fails after fix | Fix the gate failure; never push broken code |
| Merge conflict during rebase | Resolve conflict, re-run gates, then continue |
| Ambiguous comment | Leave a reply asking for clarification; skip for now |
| PR is in DRAFT state | Implement and push, but note to user to un-draft before requesting re-review |

## Repo slug helper

```bash
# Get owner/repo from git remote
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

Use this wherever `{owner}/{repo}` appears above.

See [REFERENCE.md](REFERENCE.md) for language-specific quality gate commands and gh API pagination.
