---
name: pr-finish
description: >-
  Finish an open PR by batching review feedback, applying valid fixes, running
  verification, pushing once per batch, and monitoring CI with bounded waits.
  Use when the user asks to update code until PR review comments are handled,
  review-all has no valid blocking findings, and required checks pass.
---

# PR Finish

Use this skill to finish a PR without turning review and CI into an unbounded
loop. Keep `review-all` review-only; this skill owns the triage, fix, verify,
push, and bounded CI workflow.

## Rules

- Do not fix review comments one at a time.
- Fetch all current review state before editing: PR review bodies, inline review
  comments, issue comments, current head SHA, and check status.
- Triage every finding as `valid`, `already fixed`, `obsolete`, or `not actionable`.
- Apply all valid P0-P2 fixes in one batch.
- Treat P3 as optional unless it violates an explicit repo convention, is very
  cheap and clearly useful, or the user asks to fix all nits.
- Run focused tests for touched code first, then one final repo verification
  pass before pushing.
- Push once per batch.
- Run `review-all` once after the batch. If valid P0-P2 findings remain, do at
  most one more fix batch unless the user explicitly asks to continue.
- Do not rerun `review-all` after each individual fix.
- If only long e2e jobs remain pending after 10 minutes, report status and stop
  unless the user explicitly asked to wait for them.

## Procedure

### 1. Resolve PR Context

Find the PR for the current branch:

```bash
gh pr view --json number,url,title,headRefOid,reviewDecision,statusCheckRollup
```

If the branch has no PR, ask for the PR number.

### 2. Fetch Review State

Fetch summary reviews, issue comments, and checks:

```bash
gh pr view <pr> --json url,title,headRefOid,reviewDecision,latestReviews,reviews,comments,statusCheckRollup
```

Fetch inline review comments:

```bash
gh api repos/<owner>/<repo>/pulls/<pr>/comments --paginate
```

Use `gh` for GitHub operations. If an API call fails because of sandboxed
network access, rerun the same command with the required approval.

### 3. Triage Before Editing

Create a concise triage table before making changes:

| Source | File:Line | Priority | Finding | Status | Action |
| ------ | --------- | -------- | ------- | ------ | ------ |

Classification:

- `valid`: Still applies to current `HEAD` and should be fixed.
- `already fixed`: The code/docs/tests already address it.
- `obsolete`: The comment points at an old commit or moved code and no longer
  applies.
- `not actionable`: The finding is wrong, speculative, or asks for behavior
  outside the requested scope.

Only edit after the table is complete.

### 4. Fix In One Batch

Apply all valid P0-P2 fixes together. Keep edits narrow and aligned with the
repo's conventions. For P3, fix only when it is convention-backed or clearly
worth the small cost.

### 5. Verify

Run focused checks for touched code first. Examples:

```bash
go test ./internal/cli
go test ./internal/controller
```

Then run the repo's standard verification targets:

```bash
make test
make verify
```

Run broader targets such as `make test-integration` only when the touched code
or review findings justify it.

### 6. Commit And Push

Check the diff and status:

```bash
git status --short
git diff --stat
git diff --check
```

Commit with a scoped message and push once for the batch.

### 7. Run Review-All Once

After the push, run `review-all` once against the committed branch diff.

If `review-all` reports valid P0-P2 findings, do one more batched fix cycle:
triage all findings, fix them together, verify, commit, push. Do not continue
past that second cycle without explicit user confirmation.

If only P3 findings remain, report them as optional unless they violate a stated
repo rule.

### 8. Monitor CI With Bounds

Check status:

```bash
gh pr checks <pr>
```

If a check fails, inspect that job and fix the failure. If checks are passing or
only long e2e jobs remain pending, use this policy:

- Wait up to 10 minutes total for pending long jobs.
- If they still run after 10 minutes, report which jobs are pending and stop.
- Continue waiting only if the user explicitly asked to wait for all checks.

## Final Report

Keep the final response short:

- review findings fixed or triaged
- commits pushed
- local checks run
- PR check status
- any remaining pending long jobs or optional P3 items
