---
name: helpdesk-pr-queue-closeout
description: "Oldest-first Helpdesk dev PR queue closeout orchestrator. Use when Ben asks to drain, close out, babysit, green, reply to review threads, or merge eligible open Helpdesk pull requests targeting dev. Requires live GitHub truth, clean isolated worktrees, full PR blast-radius fan-out, patch-or-fix for bugfix or behavior PRs, non-mock proof, evidence replies on every review thread, current-head checks, explicit current merge authorization, GitHub issues for non-blocking follow-ups, and worktree cleanup after verified dev merge. Do not use for promote, ship to main, production deploys, or generic single-PR review unless the task is queue closeout."
---

# Helpdesk PR Queue Closeout

## Purpose

Use this skill to act as the Codex lead orchestrator for Helpdesk open PR queues
targeting `dev`. Process one PR at a time, starting with the oldest live open PR,
and keep going from fresh GitHub truth until the queue is empty or every remaining
PR is blocked or currently ineligible.

This is not the `promote` skill. It must not handle dev-to-main release trains,
production deploys, Render deploys, or migration cutovers.

## Required References

Load only the reference needed for the current step:

- `references/github-closeout.md` for GitHub queries, review-thread GraphQL, final
  gate commands, and follow-up issue commands.
- `references/worktree-lifecycle.md` for route-card, worktree, lock, and cleanup
  rules.
- `references/report-template.md` when writing per-PR or queue status reports.

Before running the mandatory gates, read the canonical `$blast-radius` and
`$patch-or-fix` skill bodies. Do not replace those skills with summaries here.

## Run Modes

- `merge-dev`: Ben currently asked to merge/drain/merge eligible PRs in this run.
- `merge-ready`: no current merge instruction; make PRs ready and stop before merge.
- `status-only`: read-only queue status; do not create worktrees, mutate branches,
  reply to threads, or run merge gates unless Ben expands the scope.

Skill purpose is not merge authorization. Merge authorization must be a current Ben
instruction for the named PR or eligible queue.

## Preflight

1. State: `WORKFLOW BUDGET: xhigh | multi-subagent | expanded tools`.
2. For normal closeout, run `enterprise-precheck --skill helpdesk-pr-queue-closeout`.
   If it exits non-zero, stop and report stderr verbatim. Skip only for
   `status-only` or purely read-only invocations.
3. Read the latest route card before any repo mutation. Missing, stale, wrong-cwd,
   wrong-repo, wrong-base, old-head, contradictory, or `allowed_to_edit_here=false`
   cards fail closed for mutation.
4. Fetch current truth: `git fetch origin --prune`.
5. List open PRs targeting `dev` from live GitHub, sorted by `createdAt` ascending.
   Use `gh --repo anotherben/helpdesk` for every GitHub command.
6. Capture for each candidate: number, title, URL, author, base/head repo and
   branch, `maintainerCanModify`, draft state, `headRefOid`, mergeability,
   review decision, required checks, status rollup, and paginated GraphQL
   `reviewThreads` by thread ID.
7. Detect existing active closeout worktrees, branches, or locks for the same PR.
   Stop or coordinate instead of running two lanes against one branch.

## Per-PR Loop

Handle the oldest currently eligible PR first.

Do not skip ahead unless the current PR is blocked by source evidence, missing
permission, draft state, unsafe branch authority, unresolved owner input,
unmergeable conflicts you cannot safely resolve, or a required proof surface that
Ben has not waived. Record blocker evidence, preserve any useful worktree, then
refresh the live oldest-first list.

### Worktree And Branch Authority

- Use one isolated clean worktree per PR, with a unique slug containing PR number
  and head SHA. Prefer:
  `/Users/ben/.codex/bin/codex-new-worktree <slug> --repo /Users/ben/helpdesk`.
- Reread or regenerate the route card inside the PR worktree after checkout,
  rebase, conflict resolution, or `headRefOid` change. Mutate only when
  `allowed_to_edit_here=true`.
- Before pushing fixes, prove the head repo and branch are writable and appropriate
  for Codex. Do not push to forks or another author's branch without explicit
  permission.
- No force-push unless Ben explicitly approves `--force-with-lease` for the named
  PR branch.
- If approval identity matters, close or replace via `~/.codex/bin/codex-pr-create`.
- Draft PRs are blocked/not merge-eligible unless Ben explicitly authorizes
  conversion.

### Mandatory Gates

- Run `$blast-radius` in PR Review mode with full queue-closeout fan-out. Do not use
  Lite for merge decisions. The artifact must include change set, mandatory pattern
  sweep, live schema section when applicable, adversarial matrix, review trap replay,
  finding closure ledger, stable finding IDs, mechanical verdict, and start/end
  review-thread state.
- Merge-ready is blocked by any HIGH or CRITICAL finding; any MEDIUM finding unless
  Ben or an explicitly delegated reviewer accepts it as truly non-blocking and
  outside the merge-safety path with a GitHub issue; important UNTESTED adversarial
  cells; blocked live schema proof; stale or wrong-head artifacts; prior unclosed
  findings; or unresolved review threads.
- Run `$patch-or-fix` before merge for bugfixes and behavior changes. Require the
  full canonical output: Evidence Ledger, Assumption Ledger, Boundary Ledger,
  Specialist Reviews, Causal Chain, Structural Checks, Falsification, Required Fix,
  Verification, JSON handoff packet, and validation.
- Docs-only or chore PRs require evidence-backed `patch-or-fix: NOT APPLICABLE`;
  do not fake a FIX verdict.
- Non-FIX blocks merge unless Ben gives per-PR contained-patch approval with owner,
  deadline, GitHub issue, preserved diagnostics, no unresolved review threads, and
  no fix-now recurrence path.

### Proof Rules

- Do not add new mock tests as regression or proof.
- Mock-only proof never counts. Supplemental existing mocks may remain only when
  they are not the proof surface.
- DB mocks, mocked runtime shapes, fixture-only proof, source-string-only checks, or
  count-only proof inside the radius are findings, not supporting evidence.
- DB-touching changes need real DB/schema proof.
- UI behavior needs browser proof.
- Integration proof stays read-only unless Ben approves the exact Shopify/REX object
  and scope. Substitute proof must not claim equivalence to unauthorized write proof.
- Run focused tests, final-head proof, and `npm run local:canary` before merge.
  A blocked canary blocks merge unless Ben explicitly accepts a per-PR waiver after
  the blocker is evidence-classified as environment/tooling and affected surfaces
  have stronger focused proof.

### Review Conversations

- Query review threads with paginated GraphQL by thread ID at the start, after
  fixes/replies, and immediately before merge. Counts alone are insufficient.
- Reply on the exact review thread, not only as a top-level PR comment.
- Each evidence reply must include thread URL or ID, final commit SHA, changed
  files/symbols, proof commands and results, artifact paths, and live/schema/runtime
  proof where relevant.
- Resolve a thread only after the evidence reply and only when the issue is fixed or
  proven not applicable. Do not resolve threads needing reviewer, owner, or Ben
  judgment; unresolved human approval; or disputed product scope.
- After the final push/reply cycle and before the final review-thread query, run:
  `node scripts/review/copilot-review-wait.cjs --repo anotherben/helpdesk --pr <PR>`.

### Current-Head Discipline

If `headRefOid` changes after checkout, a fix, rebase, conflict resolution, review
reply, async reviewer update, or final poll, rerun the affected gates:
`$blast-radius`, `$patch-or-fix`, review-thread queries, and verification.

Conflict resolution is a new code change and must be retraced.

Final pre-merge truth bundle:

- `git fetch origin --prune`
- `gh pr checks --repo anotherben/helpdesk --required <PR>`
- `gh pr view --repo anotherben/helpdesk --json baseRefName,headRefName,headRefOid,isDraft,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup`
- paginated GraphQL review-thread query with timestamp and unresolved thread IDs

Block merge when the base is not `dev`, the PR is draft, `mergeStateStatus` is not
clean/mergeable, required checks are not passing, review decision is blocking,
current head is stale, or any review thread is unresolved.

### Merge

Merge only when `merge-dev` mode is active and all gates pass on the final head.

- Merge only PRs targeting `dev`.
- Never push directly to `main`.
- Never use `--auto` or `--admin`.
- Prefer: `gh pr merge --repo anotherben/helpdesk --rebase <PR>`.
- After merge, verify the merge commit is contained in `origin/dev` before cleanup.

## Follow-Ups

- `fix-now` and recurrence-path issues must be resolved before merge.
- Real non-blocking follow-ups must become GitHub issues before merge-ready or
  merge, with issue URL/number, owner, scope, proof target, and source artifact links
  recorded in the PR report.
- If issue creation fails, block or get explicit Ben exception.
- Do not create issues for `note-only` observations.

## Cleanup

Preserve evidence before cleanup. Do not delete the only copy of blast-radius,
patch-or-fix, canary, DB, browser, or thread artifacts. Artifact writes must obey the
route card; otherwise use approved scratch and record the limitation.

Remove only clean merged, closed, or explicitly abandoned PR worktrees after:

- `origin/dev` containment is verified,
- `git status --porcelain` is clean,
- artifacts are committed, attached, or exported, and
- no local evidence or unpushed fixes need preservation.

Use `git worktree remove` and `git worktree prune`. Do not use `rm -rf`.

Preserve blocked worktrees with local evidence or unpushed fixes and report the path.

## Completion Standard

After each PR, report using `references/report-template.md`.

The queue is complete only when a fresh live GitHub list shows no remaining eligible
open PRs targeting `dev`, or every remaining PR has a recorded blocker and revisit
condition.
