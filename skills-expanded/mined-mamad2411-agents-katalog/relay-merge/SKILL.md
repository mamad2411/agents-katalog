---
name: relay-merge
argument-hint: "[run-id or PR-number]"
description: Merge a reviewed PR, clean up worktree/branch, and close GitHub issues. Use after relay-review returns LGTM.
compatibility: Requires gh CLI and git.
metadata:
  related-skills: "relay, relay-plan, relay-dispatch, relay-review, dev-backlog"
---

# Relay Merge

Explicitly merge a ready-to-merge PR and close the loop. **Requires relay-review PR comment.**

## Process

### 0. Gate check — verify relay-review completed

```bash
${CLAUDE_SKILL_DIR}/scripts/gate-check.js $PR_NUM
```

- Exit 0 (LGTM) → PR is ready to merge; proceed only if the user wants to land it now
- Exit 1 (no comment) → **STOP.** Run relay-review first
- Exit 1 (stale LGTM) → **STOP.** Run relay-review again for the latest commit
- Exit 1 (CHANGES_REQUESTED) → **STOP.** Re-dispatch or fix the branch first
- Exit 1 (ESCALATED) → **STOP.** Show unresolved issues to user

**Intentional skip** (hotfix, manual PR, trivial change):
```bash
${CLAUDE_SKILL_DIR}/scripts/gate-check.js $PR_NUM --skip "reason here"
```
This writes a `<!-- relay-review-skip -->` comment to the PR — maintaining audit trail even when review is bypassed. The skip reason is recorded on the PR for future reference.
`gate-check.js --skip` does not invoke any executor or reviewer, so it does not consume manifest `model_hints`.

**Do NOT merge without running gate-check.** This is the audit trail that review actually happened (or was intentionally skipped with documented reason).

### 1. Merge + finalize cleanup

```bash
RUN_ID=<run-id-from-dispatch>
node ${CLAUDE_SKILL_DIR}/scripts/finalize-run.js --repo . --run-id "$RUN_ID" --merge-method squash --json
```

This script:
- re-checks the latest PR audit trail and blocks merge if `review.last_reviewed_sha` is stale for the current HEAD
- merges the PR and only advances the manifest after GitHub reports the PR as `MERGED`
- best-effort deletes the remote branch after the merge is confirmed
- marks the manifest `merged`
- best-effort closes the linked issue
- removes the retained worktree, deletes the local merged branch, and runs `git worktree prune`
- records `cleanup.status` in the manifest

If the retained worktree is dirty, merge still succeeds but cleanup is recorded as `failed` and the manifest moves to `next_action=manual_cleanup_required`.

Emergency escape hatch:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/finalize-run.js --repo . --run-id "$RUN_ID" --skip-review "hotfix" --json
```

`finalize-run.js --skip-review` bypasses reviewer invocation, so `model_hints.review` is a non-consumer on that path.

#### Operator-only force finalize for non-ready runs

```bash
node ${CLAUDE_SKILL_DIR}/scripts/finalize-run.js --repo . --run-id "$RUN_ID" \
  --force-finalize-nonready --reason "reviewer-swap exhausted, diff clean per manual inspection" --json
```

Use this only when an operator has independently checked that the PR is mergeable but the manifest cannot reach `ready_to_merge`.
Typical cases: state stuck at `escalated` with a clean diff; reviewer-swap unavailable; manifest/PR state desync.
This path is loud on purpose: it records a `force_finalize` event before merge and writes `last_force` into the manifest.
`--force-finalize-nonready` requires `--reason <non-empty-text>`.
`--dry-run` is observation-only on this path: it does not append `force_finalize`.

Do not use it for retry loops.
Do not use it as a test shortcut.
Do not use it to paper over a wrong manifest state that should be repaired instead.

Audit every use:

```bash
jq 'select(.event == "force_finalize")' ~/.relay/runs/<repo-slug>/<run-id>/events.jsonl
```

#### Bootstrap artifact reconciliation

When a run predates an artifact writer that the run itself introduced, use the structured reconciliation command instead of encoding that fact in a force-finalize reason:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/relay-reconcile-artifact.js --repo . --run-id "$RUN_ID" \
  --artifact-path "~/.relay/runs/<repo-slug>/<run-id>/execution-evidence.json" \
  --writer-pr 267 --reason "run predates the artifact writer" --json
```

This stamps `bootstrap_exempt` in the manifest, emits `force_finalize` with `bootstrap_exempt: true`, and marks the run merged without invoking the PR merge path.

### 2. Sprint file update (if available)

If `backlog/sprints/` has an active sprint file, update it. If no sprint file exists, skip this step.

**Plan section** — mark completed (was `[~]` during review):
```markdown
- [x] #38 OAuth2 flow → PR #87 (merged)
```

**Progress section** — structured log entry with review round count:
```markdown
- 2026-03-25 10:50: #38 dispatched → PR #87 → reviewed (LGTM, round 1) → merged
```

**Running Context section** — capture learnings for remaining tasks:
```markdown
- OAuth2: PKCE flow using jose library. Tokens in httpOnly cookies.
```

### 3. Follow-up (if needed)

```bash
gh issue create --title "Follow-up: ..." --body "..."
```

Task file cleanup (move to `backlog/completed/`) happens at sprint end, not per-issue.

## Sprint File State Transitions

```
[ ] #N Task name                          ← not started
[~] #N Task name → PR #M (reviewing)     ← dispatched, review in progress
[x] #N Task name → PR #M (merged)        ← completed
```

## Sprint File Updates Summary

| Section | What to update | When |
|---------|---------------|------|
| **Plan** | `[~]` → `[x]` with PR ref | Every merge |
| **Progress** | Structured log with review rounds | Every merge |
| **Running Context** | Learnings that affect later tasks | When something was discovered |
| **Follow-up issues** | New GitHub issues | When review found out-of-scope work |
