---
name: cursor-review-and-ship
description: Review the current branch for bugs, intent fit, and test coverage; run or write tests; commit focused work; open or update a PR.
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

## Codex mirror boundary

Resolve the named skill, tool, connector, and account against what is actually available in this Codex session before following the upstream steps. Do not infer connection, authentication, credits, or runtime parity from this mirror. Preserve the external product named upstream and report a concrete missing capability when required.

## Codex publication boundary

Treat repository review, local edits, pushing a branch, opening or updating a PR, and merging as distinct effects. Verify the target repository and current user authorization for each external write. If push or PR publication is not yet authorized, complete the local branch, diff, checks, and draft PR text so approval is the final step. Do not merge unless separately requested. Preserve the upstream review and CI workflow within those boundaries.

# Review and ship

## Trigger

Reviewing changes before shipping. Close key issues, verify behavior, and open or update a PR.

## Workflow

1. Gather context: diff against base branch, uncommitted changes, recent commits, changed files, and user intent from recent relevant chats if useful.
2. Run targeted tests for changed behavior. If no focused tests exist, decide whether to add them or document the gap.
3. Review for correctness, regressions, security, and intent fit. Use parallel subagents for larger diffs.
4. Fix critical issues before finalizing and re-run affected tests.
5. Commit selective files with a concise message.
6. Push branch and open or update a PR.

## Suggested Checks

```bash
git fetch origin main
git diff origin/main...HEAD
git status
gh pr checks --json name,bucket,state,workflow,link
```

## Guardrails

- Prioritize correctness, security, and regressions over style-only comments.
- Keep commits focused and avoid unrelated file changes.
- If pre-commit checks fail, fix the issues rather than bypassing hooks.
- Use `gh pr checks` instead of GitHub Actions-only commands when judging PR readiness.

## Output

- Findings summary (critical, warning, note)
- Tests run and outcomes
- PR URL
