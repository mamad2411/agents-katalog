---
name: daily-domain-refactor-runner
description: Use when inspecting Helpdesk domains for SRP, README, write-boundary, table ownership, or service-migration opportunities and when running one selected domain refactor lane through enterprise gates, PR audits, review loops, and explicit dev merge authorization.
---

# Daily Domain Refactor Runner

## Overview

Use this skill to inspect `apps/api/src/domains/**`, choose one scoped SRP/domain migration lane, and run it through plan, build, review, verify, PR, and merge-ready gates. It may merge to `dev` only when Ben explicitly authorizes that specific merge and all gates pass.

Core rule: a green PR is not done until source, runtime, review, audit, and enterprise merge gates agree on the current head.

## Required Sub-Skills

- **REQUIRED PRECHECK:** Use `deep-think`.
- **REQUIRED CONTROL:** Use `nested-agent-control` for all delegated work.
- **REQUIRED TRACE:** Use `blast-radius` before implementation.
- **REQUIRED POST-FIX:** Use `patch-or-fix` after the implementation diff exists.
- **REQUIRED FINAL PROOF:** Use `scope-check` and `proof-chain` before PR submission and before merge-ready claims.
- **REQUIRED PR AUDITS:** Use `pr-schema-audit` and `code-variable-audit` before PR submission and again after a PR number exists.
- **REQUIRED LANE EXECUTOR:** Use `enterprise-refactor-to-green-pr` for PR-producing lanes.

## Read-Only Versus Mutating

Read-only inspection may continue when the route card is missing, but the output must say mutation is blocked. Use remote comparison for read-only freshness; do not update refs in a guarded root. For read-only freshness, compare current `HEAD` with the remote `dev` SHA from `ls-remote` and record both values.

Mutation requires a current route card or approved isolated worktree path that allows edits. If `$HELPDESK_REPO` is unset when a mutating lane begins, stop and ask for the guarded repo root instead of guessing.

## Hard Stops

Stop instead of mutating when:

- The latest route card is missing or says edits are not allowed in the current checkout.
- The checkout is dirty, on `dev` or `main`, stale versus `origin/dev`, or not a clean isolated worktree.
- Dependencies are not ready enough to run the focused tests; record missing packages such as `pg` as a blocker instead of claiming source-only proof.
- `enterprise-precheck --skill daily-domain-refactor-runner` or `enterprise-precheck --skill enterprise-refactor-to-green-pr` fails.
- A required enterprise stage gate fails.
- A plan lacks exact source files, owner tables, forbidden scope, verification commands, rollback or abort conditions, and review gates.
- A subagent is asked to do more than one job or edits outside assigned files.
- `$pr-schema-audit` cannot confirm its secret/readiness when DB-touching changes are in scope.
- `$code-variable-audit` or `$pr-schema-audit` reports unresolved HIGH or CRITICAL findings.
- Review threads remain unresolved, addressed GitHub conversations have not been resolved, required checks are not green, or `copilot-review-wait` has not passed.
- Ben has not explicitly authorized merging the specific PR.

## Daily Inspection

1. State `WORKFLOW BUDGET: xhigh | sequential-review subagents | normal tools` and the `NESTED AGENT CONTROL` header.
2. Prove the checkout is current enough for read-only assessment; record branch, head SHA, remote dev SHA, route-card status, vault-index claim state, and whether cortex/source tooling is usable.
3. Run the read-only dry-run script: `node /Users/ben/.codex/skills/daily-domain-refactor-runner/scripts/inspect-domain-refactor-opportunities.cjs --repo "$PWD" --count 10 --dry-run-report`.
4. Choose one lane. Do not run multiple PR lanes in parallel.
5. Read the domain README, flow doc, current domain files, legacy service owner files, ownership registry entries, tests, ratchets, and colocated `GOTCHAS.md` files.

## Plan Agreement Loop

Before coding, loop the plan through one-job reviewers:

1. Local lead writes a concrete plan with exact files, owner tables, seam, tests, and stop conditions.
2. `source-truth-mapper` checks source and caller evidence only.
3. `ownership-srp-reviewer` checks table owner path, write boundary, README contract, and SRP split.
4. `plan-adversary` tries to reject the plan for scope creep, missing proof, wrong seam, dependency gaps, stale docs, or stale branch assumptions.
5. Local lead revises the plan.
6. Proceed only when every reviewer returns `READY` with evidence and no HIGH finding remains.

If reviewers disagree and current source cannot resolve the disagreement, stop.

## Implementation Loop

Run the lane serially in a new clean worktree created by `codex-new-worktree` from `$HELPDESK_REPO`. Then run both enterprise prechecks named in Hard Stops, start the agent session, and pass the required plan/build/review/forge/verify stage gates before claiming readiness.

Implementation rules:

- Add or update tests first when behavior changes.
- Move the smallest safe write seam into `apps/api/src/domains/<domain>/**`.
- Update `apps/api/ownership/db-write-owners.json` only when ownership actually moved and live-test proof exists.
- Update the domain README and flow docs when the ownership/read/write contract changes.
- Keep routes thin; do not move SQL into routes.
- Do not introduce new grandfathered service writes.

After every patch, run these exact repo gates from the Helpdesk worktree: `npm run architecture:ratchet:test`, `node scripts/db-write-enforcement.cjs --mode audit --fail-on-unowned --fail-on-live-ownership`, and focused tests for the lane. If `architecture:ratchet:test` or its current SRP/domain architecture gate bundle is absent, stop as `ARCH_GATE_MISSING`; do not skip, raise a baseline, or claim architecture proof. Run `patch-or-fix`; if it returns `PATCH`, `PARTIAL FIX`, `FAIL: UNPROVEN`, or any unresolved HIGH issue, revise or stop.

## PR Gates

Before PR creation, run `$code-variable-audit` in local diff mode against `origin/dev...HEAD`. For DB-touching lanes, verify the `$pr-schema-audit` secret/readiness precondition without publishing and record that the full schema audit is pending until a PR number exists.

Create the PR only with `codex-pr-create --base dev`. The PR body must include `Regression check`, `Blast radius`, `Edge cases`, and `Conversations addressed`.

After PR creation, run `$pr-schema-audit` and `$code-variable-audit` against the PR number in dry-run mode; rerun both after the final runtime-relevant patch before merge-ready. Publication from audit skills requires explicit authorization.

Also run `copilot-review-wait`, required PR checks, live PR metadata, review-thread inspection, `scope-check`, `proof-chain`, and `enterprise-agent-session check-stage --stage merge` before any merge-ready claim.

## Review And Verify Loop

For every review finding:

1. Verify the finding against current source.
2. Fix valid findings inside the lane contract.
3. Re-run focused tests, architecture checks, audit scripts, and canary as applicable.
4. Push the new head.
5. Re-read review threads and checks.
6. Resolve addressed GitHub conversations after source proof confirms they are addressed.

Do not claim completion from stale local proof after a push.

Before merge-ready, run `npm run local:canary`, `copilot-review-wait`, required PR checks, `scope-check`, `proof-chain`, and the enterprise merge-stage check after the final runtime-relevant patch.

## Merge Rule

Only merge when Ben explicitly authorizes the specific PR merge in the current conversation, for example: `merge PR 123`.

Even with authorization, do not merge unless:

- PR head SHA matches the reviewed head.
- required checks are green.
- unresolved review threads are zero.
- addressed GitHub conversations are resolved.
- `copilot-review-wait` passed.
- `pr-schema-audit` and `code-variable-audit` are pass or explicitly dispositioned from source evidence.
- `scope-check` and `proof-chain` pass on the current head.
- `npm run local:canary` passed after the final runtime-relevant patch.
- enterprise merge stage passes.

After merge, prove containment on `origin/dev` with live PR state, merge commit data, and branch containment or compare evidence.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Starting from a clean branch without route permission | Current route/worktree permission is still required before mutation. |
| Moving code under `/domains` without changing ownership | The registry and write seam must reflect the real owner. |
| Letting one agent plan, build, and review | One agent, one job; the lead integrates. |
| Treating audits as optional | `$pr-schema-audit` and `$code-variable-audit` are PR gates. |
| Treating green PR as merge permission | Ben must explicitly authorize the merge. |

## Dry-Run Output

A valid dry run produces:

- current base SHA, remote dev SHA, and route-card status
- vault-index and cortex/tooling status
- dependency readiness status
- inspection script output
- one proposed lane with source files, owner tables, seam, tests, and stop gates
- subagent plan-review prompts
- PR/audit/merge gate checklist
- no edits, commits, pushes, PRs, or live writes
