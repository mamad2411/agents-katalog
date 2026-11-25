---
name: enterprise-refactor-to-green-pr
description: End-to-end enterprise workflow for turning multiple refactor opportunities into serial green pull requests. Use when the user asks to identify refactor/domain opportunities, create lane plans, run Helpdesk enterprise gates, use specialist subagents, loop code reviews such as /review, CodeRabbit, Copilot, or GitHub review threads until no findings remain, create PRs, or merge approved refactor lanes to dev with proof.
---

# Enterprise Refactor To Green PR

## Operating Contract

Use this skill as the lead-orchestrator workflow. Keep Codex as integrator and decision owner; use subagents only for one bounded job at a time.

Hard stops:

- Do not edit a guarded root checkout unless the latest route card allows edits.
- Do not run lanes in parallel; finish or explicitly block one lane before starting the next.
- Do not push, create PRs, merge, or run external write canaries unless the user authorized that exact scope.
- Do not treat green local tests as done. A lane is PR-green only after current review threads are resolved, async review wait passes, required checks are green, and the enterprise merge-stage gate passes.
- Do not hide stale proof. If a final patch lands after review, forge, or verify, refresh those stage receipts before merge.

## Startup

1. State the workflow budget, delegation plan, and tool scope.
2. Read the latest route card.
3. Fetch and verify the target base, usually `origin/dev`.
4. Run the project startup checks required by local instructions, including vault-index health for Helpdesk work.
5. Load only the directly relevant skills and docs. For Helpdesk enterprise lanes, use the lean enterprise runtime docs and stage cards on demand.
6. If the user explicitly frames the work as a goal, create a goal with the lane objective; only set a token budget if the user supplied one.

When using subagents, also state `NESTED AGENT CONTROL: budget=<medium|high|xhigh> | mode=<solo|single-coordinator|sequential-review|parallel-workers> | active_limit=<n> | stop_gate=<condition>` and keep an agent ledger. Close completed agents before starting the next wave.

## Opportunity Discovery

Identify candidate refactor lanes from current source, architecture docs, ownership audits, route sprawl, large multipurpose files, repeated review findings, domain docs, and test gaps.

For each candidate, write a route card in the orchestration packet:

- `slug`, target branch, base SHA, and worktree path.
- Exact scope and explicit exclusions.
- Ownership tables, route boundaries, external integrations, tenant/auth boundaries, and no-write-canary limits.
- Required plan artifact path, usually `docs/plans/YYYY-MM-DD-<slug>-execution-plan.md`.
- Required enterprise artifacts, at minimum `.codex/enterprise-state/<slug>-entity-preflight.json` and `.codex/enterprise-state/<slug>-merge-readiness.json`.
- Proof commands, including architecture ratchets, focused route/service tests, schema or ownership checks, local canary, and review gates.

If the user asks for a fixed count, such as five refactor opportunities, produce exactly that many lane cards unless a hard blocker prevents it.

## Lane Execution

Run each lane serially:

1. Create a clean worktree from the shared repo with `codex-new-worktree <slug> --repo "$HELPDESK_REPO"`.
2. In the worktree, verify clean state and current base with `git fetch`, `git status --short --branch`, and `git rev-parse origin/dev`.
3. Start the enterprise session with `enterprise-precheck --skill enterprise` and `enterprise-agent-session ensure`.
4. Before implementation, write the plan artifact and enterprise state artifacts required by the packet.
5. Run the full enterprise sequence: plan, plan-360-audit, contract-manager, build packet, build, review, forge, verify, patch-or-fix, prove-it.
6. Use specialist subagents only for one job each. Record `agent_instance_id` or `subagent_session_id` in the lane proof. Good roles include `source-truth-mapper`, `domain-srp-reviewer`, `table-ownership-auditor`, `test-ratchet-engineer`, `builder`, `patch-or-fix-reviewer`, `prove-it-closer`, and `pr-closer`.
7. Keep edits inside the lane contract and preflight allowed paths. If a valid fix needs wider scope, stop and recycle the contract.

## Review Loop

After the lane branch is pushed and a PR exists, loop until there are no unresolved findings.

1. Read live PR state with `gh pr view` and the GitHub GraphQL `reviewThreads` query. Also harvest CodeRabbit review summaries, check annotations, and bot replies directly before claiming no findings remain.
2. If `/review` is available, run it on the current PR/worktree. Otherwise use the repo review skills and GitHub review threads as the source of truth.
3. For every finding:
   - Verify against current code before changing anything.
   - Fix valid findings with the smallest scoped patch.
   - For false positives, reply with concrete proof and resolve the thread.
   - If a thread is stale but still blocks gates, reply with the superseding head and resolve it.
4. After each patch:
   - Run focused proof and formatting/lint checks.
   - Commit and push.
   - Re-read review threads and rerun async review wait.
5. Continue the loop until no unresolved review threads remain, review checks are settled, the final review run produces no new findings, and required GitHub checks are green.

Use subagents in this loop for bounded passes only: one reviewer subagent to harvest findings, one patch subagent per isolated fix, or one proof subagent to run a specified command set. The lead must verify and integrate all outputs.

## PR Creation And Merge

Create Codex-authored PRs with `codex-pr-create`, not plain `gh pr create`.

Before any merge-ready or merge claim, run the async review wait script, the enterprise PR pre-merge sweep, `enterprise-agent-session check-stage --stage merge`, and required GitHub checks.

If GitHub has a stale `CHANGES_REQUESTED` review on a superseded commit and all associated threads are addressed or withdrawn, dismiss only that stale review with a specific reason. Never dismiss an unresolved current-head review.

Merge only after explicit user authorization and clean gates. For rebase merges, original branch-head SHA ancestry may not hold. Prove containment by checking the PR merge commit on `origin/dev`, comparing trees when appropriate, and reading `gh pr view` state, merged time, merge commit, and head SHA.

## Lane Report

After each lane, report:

- worktree path, branch, PR URL, and current or merge SHA,
- enterprise stage status,
- subagents used with `agent_instance_id` or `subagent_session_id`,
- files changed,
- tests and proof run,
- review threads resolved and any stale review dismissal,
- blockers or residual risk,
- whether to proceed to the next lane.

At the end, report all PRs, merge commits on `dev`, and any lanes intentionally left unmerged or blocked.
