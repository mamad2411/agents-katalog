---
name: session-close
description: "Close a coding-agent session with durable repository state, proportional verification, documentation reconciliation, and a useful handoff. Use when the user says close out, wrap up, end session, session report, doc sync, preserve work, or asks for a final commit and push before stopping."
metadata:
  version: 0.2.0
---

# Session Close

Turn active session into recoverable, reviewable handoff without absorbing unrelated work.

This is lightweight closeout. Use `retro-distill` for deeper pattern mining after major chunks or failures.

## Authority order

1. Read repository `AGENTS.md` and nested instructions governing changed paths.
2. Use repository-native closeout, worktree, documentation, and verification commands when defined.
3. Apply generic workflow below only where repository has no stronger rule.

## Workflow

### 1. Inventory live state

Capture:

```bash
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --porcelain
git diff --name-only
git diff --cached --name-only
git log --oneline -10
```

Identify owned paths, unrelated dirty paths, commits made this session, and unpushed commits. Do not clean or stage yet.

### 2. Map changes to obligations

For each owned change, identify:

- tests or probes required by affected surface
- documentation that describes changed behavior
- generated artifacts needing repository-native regeneration
- release or deployment boundary
- session log or handoff format required by repository

Use live paths and current code. Prior plans record intent, not necessarily final state.

### 3. Reconcile documentation

Update canonical docs when behavior, architecture, commands, data contracts, or operator workflows changed. Avoid documentation churn for implementation details with no durable effect.

If required doc cannot be updated, record explicit exception with reason and follow-up owner. Do not silently leave known drift.

### 4. Verify proportionally

Use `verify-honestly`:

- run cheapest probe capable of catching likely failure
- cite existing green deterministic gates instead of repeating them
- verify UI in browser when UI behavior changed
- name live or production gaps instead of implying coverage
- record exact commands and results

### 5. Write handoff

Use repository session-log format when present. Otherwise record concise Markdown with:

```markdown
## Scope
## Changes
## Files touched
## Decisions
## Verification
## Residual risks
## Next-session context
## Transferable lessons
```

Include only reusable lessons supported by session evidence. Do not turn routine closeout into speculative retrospective.

### 6. Make work durable

Follow repository's Git workflow. Under contention, use `git-under-contention`.

- Stage explicit owned paths only.
- Review cached diff and staged filenames.
- Commit complete logical unit, or labeled WIP when unfinished and repository permits it.
- Push authorized branch and confirm remote tip.
- Leave unrelated dirty paths untouched.
- Do not deploy unless user explicitly requested deployment.

If commits or pushes are not authorized, preserve files and report exact uncommitted or unpushed state.

### 7. Final state check

Re-run status and compare current HEAD with captured state. If HEAD moved during closeout, recheck generated files and documentation against new tip.

## Final response contract

Report:

- outcome
- commit and pushed branch, when applicable
- owned files changed
- highest verification level and evidence
- documentation reconciled or exceptions
- residual risks and deploy-gated checks
- single next action, only when work remains

## Checklist

- [ ] Current branch, root, and HEAD captured.
- [ ] Owned and unrelated changes separated.
- [ ] Durable behavior changes reflected in canonical docs.
- [ ] Generated artifacts refreshed by canonical command.
- [ ] Verification level named with exact evidence.
- [ ] Explicit paths staged and cached diff reviewed.
- [ ] Commit pushed or exact preservation gap reported.
- [ ] Final status checked without deleting unrelated work.

## Stop conditions

- Ownership of dirty or staged paths is unclear.
- Repository requires destructive cleanup or force operation.
- Required verification or docs sync exposes unresolved correctness issue.
- Push or merge would include unreviewed work from another session.

Preserve current state and report blocker instead of manufacturing clean closeout.

## Related skills

- `git-under-contention` protects shared repository state.
- `verify-honestly` defines verification claims.
- `retro-distill` performs deeper learning loop after closeout.
