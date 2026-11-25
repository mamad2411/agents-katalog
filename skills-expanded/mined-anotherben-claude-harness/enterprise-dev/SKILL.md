---
name: enterprise-dev
description: Full enterprise workflow for legacy enterprise-dev invocations. Use when starting a feature, significant refactor, enterprise hardening effort, GitHub issue intake/processing, or multi-stage bugfix that needs end-to-end workflow control, portable repo-local artifacts, and explicit proof scope.
---

# Enterprise

Portable enterprise workflow wrapper. This suite is repo-agnostic, publishable, and intended to generate repo-local overlays that travel with the repository.

## Core Rules

- Use a GPT-5.5 fresh baseline: state the outcome, success criteria, constraints, output shape, and stop rules; load detailed stage procedure only when it changes behavior.
- `/goal` is allowed as an enterprise intent front door for vague or product-shaped requests, but it is only an intake adapter. It never replaces `$enterprise`, `enterprise-precheck`, `enterprise-required-gates`, `enterprise-agent-session`, agent-session artifacts, `plan-360-audit`, `contract-manager`, review, forge, verify, PR-readiness, or merge gates.
- If `/goal` output is empty, skeletal, or missing exact source-read targets, a Mechanical Build Packet seed, and refusal conditions, treat the goal intake as failed or incomplete. Continue through enterprise discovery/brainstorm until those fields are source-grounded.
- A GitHub issue number or URL is also an enterprise intent front door. Fetch it live, normalize it into a GitHub Issue Intake Packet, and treat the issue body as intake, not proof. Use [github-issue-intake.md](references/github-issue-intake.md) and `python3 ~/.codex/skills/enterprise/scripts/github_issue_intake.py --repo <owner/name> --issue <number> --json` when `gh` is available.
- For GitHub issue intake, labels such as `bug` and `ready-for-agent` may reduce ambiguity but never bypass source reads, current branch verification, clean-worktree gates, plan/contract requirements, or review -> forge -> verify. Production-log, schema/query/data, integration, pricing/inventory/order, or lock/transaction issues start as `DEBUG` or `STANDARD_AFTER_SOURCE_VERIFICATION`, not freehand build.
- Suggested fixes inside an issue are alternatives to evaluate. They must become source-grounded plan/contract decisions with proof commands before build; do not copy a suggested patch directly from an issue body.
- Planning and contract quality may consume most of the lane. Do not rush to build while schema, tenant, identity, current-code, file-boundary, E2E, or evidence questions remain open.
- Keep proof scope explicit: `function-level`, `slice-level`, `domain-level`, or `full-system`.
- The hook-generated route card is the startup source of truth for route, edit boundary, clean-worktree need, and PR gates. Read `.codex/enterprise-state/hook-ledger/latest-route-card.json` when those requirements are unclear.
- Local agent, skill, hook, Codex config, or agent-platform maintenance outside the target repo is `NO_ENTERPRISE` when the route card says `LOCAL_AGENT_MAINTENANCE`. Do not run the helpdesk or target-repo enterprise pipeline for it unless repo files are also touched.
- `/goal` may be used as the enterprise intent front door for vague or product-shaped work, but it is only an intake adapter and never replaces `$enterprise`; it must hand off to path selection, source-read targets, build-packet seed, refusal conditions, and required gates before build.
- No production code before a locked contract, except a documented inline contract on `QUICK` path work.
- No completion claim before fresh verification evidence.
- Full proof is the only passing proof state. `PARTIALLY PROVED`, `UNPROVED`, missing edge-case proof, mock-only proof, stale proof, and wrong-head proof are failed gates, not warnings. They block done, PR-ready, merge-ready, ship-ready, and safe-to-merge claims.
- No PR-ready, merge-ready, ship-ready, or "ok to merge" claim until `enterprise-review`, `enterprise-forge`, and `enterprise-verify` are recorded in order against the current final diff and the `pr-readiness` or `merge` stage gate passes.
- If a lane may produce a PR, state `route_card.required_pr_gates` and `route_card.required_pr_body_sections` at intake instead of duplicating the chain in this skill body.
- `$enterprise` owns the mechanical gate runner. Do not ask the user to run `npm`, `node`, or harness commands to prove enterprise compliance; invoke `enterprise-required-gates --repo-root "$PWD" ...` yourself and report its result.
- Local enterprise start gates require a clean feature worktree cut from freshly fetched `origin/dev`. If the current branch is `dev`/`main`, stale versus `origin/dev`, or dirty before planning/contracting, stop and create a fresh worktree first.
- Use stable enterprise wrappers as the primary command surface in every worktree: `enterprise-agent-session`, `enterprise-required-gates`, and `enterprise-containment`. They prefer repo-local tooling when present and fall back to reviewed global tooling when old promotion worktrees lack repo-local gate files. Do not hardcode `python3 tools/enterprise-skills/...` as the primary command.
- Source edits must be contained by the current agent session's locked contract and mechanical build packet. `QUICK` may skip the full plan/audit/contract-manager chain, but it must still record `path_classification=QUICK`, a locked quick contract, and a mechanical build packet before source edits. Non-`QUICK` also requires plan, plan-360-audit, contract-manager, and contract history. `validate_enterprise_containment.py` fails planned source edits, build/review/verify/harness/PR/merge readiness, and Codex-authored commits if touched source files are outside `Allowed Runtime Paths` or `Allowed Test Paths`, or if no valid agent session/build packet exists.
- For `harness`, `pr-readiness`, and `merge`, that runner must also execute final proof scripts for PC trace, changed-file proof, structured proof, delegated worker artifacts when present, and PR readiness when applicable.
- Review feedback is part of the control system. Every accepted P1/P2/P3 review finding must be harvested into exactly one prevention target: contract postcondition, plan question, forge lens, verify command, CI/gate recommendation, repo trap, or skill eval.
- Every vague, `/goal`, or product-shaped intake must carry an `Intent Continuity Ledger` from brainstorm/design through plan, contract, build, review, forge, verify, and harness. The ledger maps original user words, business outcome, operator acceptance, non-goals, and proof command. If downstream artifacts cannot prove they still satisfy the original intent, recycle before build or completion.
- Enterprise solution artifacts must include `Alternatives And Decision Rationale` for load-bearing architecture/product choices. At least the incumbent/no-change option and one credible alternative must be rejected or selected with source evidence, operational tradeoff, and proof impact.
- Every touched or newly created file must have a `Touched File SRP Assessment` before source edits: current responsibility evidence, owner layer, one reason to change, known mixed responsibilities, `fix-now` / `follow-up` / `note-only` classification, and the smallest extraction or public-seam preservation needed. If the file is already doing multiple jobs and this work touches one of them, `fix-now` is mandatory unless the contract records a blocking reason and narrows the claim.
- Every database query, read, write, repair, projection, sync, reconciliation, migration, report, verifier, or live-proof query must have a `DB/Query Ownership Packet`: table/source owner, operation type, current DB/schema target, tenant/owner/supplier scoping, affected-row or readback expectation, bounded proof command, cleanup/rollback, and approved writer/reader seam. Ownership is required for reads as well as writes; direct SQL in mixed-owner files is a failed gate unless the contract explicitly owns that seam.
- High-risk async, queue, worker, order, invoice, inventory, pricing, label-printing, notification, or staff workflow lanes must define field-level producer-to-consumer contracts and lifecycle counterexamples during plan/contract. Do not wait for final PR review to discover quantity-field mismatches, bypassed synchronous confirmations, duplicate workers, stale running states, post-commit bookkeeping ambiguity, truthy non-success helper returns, lost retries, or UI rehydration gaps.
- Every `enterprise-plan` run must immediately run `plan-360-audit`, record `plan_360_audit`, and recycle blocking findings before contract or build.
- `contract-manager` is required before contract lock and before any non-`QUICK` source edits; record its artifact/status as `contract_review`.
- Build is mechanical. Non-`QUICK` build cannot start until the agent session records a `build_packet` artifact with exact paths, commands, postcondition order, refusal conditions, and architecture fields: `Module Boundary`, `Folder Placement`, `Public Seam`, `Owner Layer`, `Allowed Dependency Direction`, `Forbidden Imports`, and `Architecture Tests`.
- Schema/query/data claims require current code reads plus real database proof. Migrations, diffs, and mocks are not enough.
- UI, PDF upload, file upload, preview/download, modal, navigation, and rendered-output claims require headless browser proof when verified.
- Last-100-PR trap matrix is a standing lens: mock/runtime shape mismatch, missing affected-row checks, SQL tenant/owner/current-DB gaps, stale or dry-run-only evidence, route method/source drift, zero/falsy UI loss, duplicate helpers/writers, and unsafe substring environment checks.
- Repo-portable facts belong in committed `.codex/enterprise-state/` files.
- Machine-specific facts belong in gitignored local-machine state, not committed profiles.
- In-flight workflow state belongs in gitignored `.codex/enterprise-state/agent-sessions/<agent-id>.json`, not repo-global status files.
- For high-risk domains, fail closed if required docs, return legs, or downstream consumers remain untraced.

## Path Selection

Use the routing matrix in [workflow-routing.md](references/workflow-routing.md).

- `DISCOVER_ONLY`: initial repo uplift, environment setup, or portability refresh
- `NO_ENTERPRISE`: local agent, skill, hook, Codex config, or agent-platform maintenance outside the target repo
- `QUICK`: tiny, bounded changes with no meaningful architecture ambiguity
- `STANDARD`: clear feature or fix with moderate blast radius; still runs plan -> plan-360-audit -> contract-manager before build
- `FULL`: multi-stage work needing discovery, design, contract, adversarial review, and evidence pack
- `DEBUG`: bug or regression path when the problem is not yet understood; after root cause, continue through plan -> plan-360-audit -> contract-manager before build unless explicitly narrowed to `QUICK`

## Required Workflow

1. Decide the path, PR intent, and required final gates up front and say them plainly. Use the latest route card as the source of truth for edit permission, clean-worktree need, and PR gates.
2. If the prompt names a GitHub issue number or URL, fetch it live and normalize a GitHub Issue Intake Packet before choosing a build path. Reject stale transcript, copied issue text, or memory as the issue source of truth when `gh issue view` is available.
3. If the prompt begins with `/goal`, or goal mode is available and the ask is vague/product-shaped, normalize it into a Goal Intake Packet: outcome, success criteria, constraints, source-read targets, Mechanical Build Packet seed, and stop/refusal rules. Then immediately continue `$enterprise` path selection and required gates. Do not stop at goal intake.
4. Fetch `origin/dev` and cut a clean feature worktree before planning, contracting, or build artifacts. Do not continue in a dirty control-room/root checkout.
5. Resolve or mint the current agent id with `enterprise-agent-session ensure --repo-root "$PWD" --agent-id <agent-id> ...` and keep using that same agent session for the whole lane.
6. Immediately run `enterprise-required-gates --repo-root "$PWD" --stage start --agent-id <agent-id>` to prove the required gate machinery, eval contracts, overlay manifest, build-packet regression, architecture-contract regression, and fresh-worktree start gate are healthy.
7. If the repo profile is missing, stale, or contradicted by reality, run `enterprise-discover`.
8. Keep `.codex/repo-skills/<repo-family>-enterprise*` in sync with the committed repo profile.
9. Produce the upstream artifact for each downstream stage and record it in the current agent session. After plan, record `plan_360_audit`; before contract lock/build, record `contract_review`; before PR readiness or merge, record review, forge, and verification at the current code state.
10. Before entering any gated stage, run `enterprise-required-gates --repo-root "$PWD" --stage <stage> --agent-id <agent-id>` instead of hand-picking individual checks. If it fails, stop and surface the failing gate. From build onward, this includes the enterprise containment gate for source edits.
11. Before build, record `build_packet=<path>` in the current agent session. The packet may be the locked contract if it contains a complete `Mechanical Build Packet` section.
12. Stop if a required upstream artifact or required domain standard is missing.
13. State the final proof scope explicitly. If it is not truly `full-system`, say what remains unproven.

## Execution Discipline

- Reuse only the minimal skill subset required by the chosen path. Do not open every related skill just because it exists.
- Use `/goal` for ambiguous, vague, or product-shaped enterprise intake when it improves outcome/source grounding. Skip it for already locked stage-only work where the next gate and artifact are exact.
- Use GitHub Issue Intake for issue numbers, URLs, or prompts like `process gh issue <n>`. Skip brainstorm when the issue is specific and source-read targets are clear; route to `enterprise-debug` or `enterprise-plan` only after current source truth verifies the issue claims.
- If the task brief is already specific, approved, and bounded, do not invoke `brainstorming` just to restate the brief.
- For `QUICK`, `STANDARD`, or other bounded slice work, keep plan, contract, review, and verification artifacts concise and task-specific.
- Preserve time and attention for downstream completion. Do not spend the whole lane polishing upstream prose while review or verification is still unwritten.
- If the user asked for end-to-end completion, PR readiness, merge readiness, or "ok to merge", continue through review, forge, verify, and the `pr-readiness`/`merge` gate in the same lane until the gate passes or a real blocker stops you.
- The user's command is `$enterprise`; any `npm`, `node`, Python, browser, DB, or GitHub proof commands are agent-owned execution details. Run them as evidence and summarize outcomes, rather than handing the user a checklist to execute.
- If review, forge, or verify finds a new repeated failure class, route it through `enterprise-compound` or `enterprise-pr-review` before closing the lane so future plans/contracts inherit the prevention.
- Repeated PR-review failure classes must become upstream gates before closeout. Branch/reason-set proof,
  cast/index safety, proof-lane integrity, bounded live-proof queries, and artifact portability are default
  enterprise gate concerns; do not wait for GitHub review to discover them.

## Agent-Bound Enforcement

- Use [agent-session-model.md](references/agent-session-model.md) for the state split.
- Use [agent-stage-gates.md](references/agent-stage-gates.md) for stage-entry enforcement.
- Never use another agent's session file as the source of truth for your stage entry.

If the prompt explicitly states that the committed repo profile and repo-local overlay are already current, do not restart bootstrap work unless the prompt also describes new drift.

## Existing Codex Skills To Reuse

- `brainstorming` for feature design
- `writing-plans` for implementation plans
- `plan-360-audit` after every enterprise plan artifact
- `contract-manager` before contract lock or implementation
- `test-driven-development` for implementation
- `systematic-debugging` for root-cause work
- `code-reviewer` and `requesting-code-review` for review
- `verification-before-completion` for completion claims

## High-Risk Domain Rule

If the task touches money movement, orders, auth, privacy, regulated data, external integrations, user safety, or any end-to-end hardening claim:

- locate the repo's source-of-truth docs first
- trace downstream and return-leg consumers explicitly
- keep the proof label below `full-system` until every required leg is evidenced

If the repo has no clear source-of-truth docs for that domain, record the gap and fail closed on the enterprise claim.
