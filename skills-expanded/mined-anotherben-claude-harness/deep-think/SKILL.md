---
name: deep-think
description: >
  Mandatory read-only pre-action and plan-review protocol for substantive coding,
  debugging, design, review, refactor, system-analysis, workflow, and business-context
  work. Use this skill to prevent first-match excitement by forcing source-grounded
  reading, explicit zoom-out system mapping, operator/business framing, root-cause,
  blast-radius, ownership, status/lifecycle coverage, plan viability, edge-case,
  SRP/refactor, schema/live-DB, headless UI, and verification thinking before
  implementation. Deep Think must not edit files, create worktrees, delegate coding,
  mutate systems, or fix bugs; it produces a decision-quality handoff only. Apply by
  default on bug fixes, feature work, refactors, plan reviews, code reviews, incidents,
  architecture, risky config, schema/query/data-sensitive work, and UI/PDF/file
  workflows. Exempt only pure chat and tiny low-risk housekeeping.
---

# Overview

Deep Think is the read-only preflight layer for substantive work. It runs before other
workflow or domain skills so the task is framed correctly before code or conclusions
happen.

This skill does **not** replace enterprise, debug, review, or domain guard skills. It
improves their input quality by forcing a deeper, source-grounded first pass. Deep
Think may prepare the work, but it must not silently become the implementation
pipeline for substantive changes.

Deep Think is a thinker, reviewer, and planner. It may inspect source, tests, logs,
schemas, contracts, policy, product notes, and workflow evidence. It must not patch,
commit, create branches or worktrees, resolve review threads, update implementation
plans, run migrations, mutate live systems, or delegate build work. Its output is a
decision-quality handoff for the next workflow stage.

## GPT-5.5 Baseline

- **Role**: act as the read-only pre-action reasoning and planning gate for risky work.
- **Goal**: prevent narrow problem framing, symptom patches, schema guesses, ownership drift, workflow blindness, business-case drift, and golden-path-only changes before any implementation or conclusion.
- **Success criteria**: current source truth is read, broader operator/business workflow is named, ownership and blast radius are named, edge cases are explicit, scope is locked, and verification evidence is planned at the right level.
- **Constraints**: do not rely on memory, migrations, diffs, mocks, or naming guesses when runtime code, live schema, logs, tests, or contract artifacts are available.
- **Output**: keep the precheck compact unless the task is high-risk; expand only where the extra detail changes the decision.
- **Stop rules**: always stop before implementation. Also stop before signoff when source truth, workflow/business context, ownership, blast radius, live data proof, or verification path is unclear.
- **Planning standard**: treat every implementation plan as a hypothesis until the objective, source evidence, sequencing, ownership, dependencies, acceptance criteria, proof level, rollback/abort conditions, and disconfirming cases are named.
- **Zoom-out standard**: for debugging, plan review, refactor planning, and confusing code areas, perform a concrete zoom-out pass before recommending a fix. Start one layer outward across callers, consumers, sibling modules, state/status cohorts, tests, and operator workflow; expand another layer only when root cause, ownership, lifecycle coverage, or verification is still unclear.
- **Adversarial standard**: when the path is ambiguous, compare credible alternatives or explicitly say why alternatives are not useful; include the strongest contrarian risk before recommending a plan.
- **Last-100-PR reviewer trap matrix**: before action on relevant work, check for deployable migration-runner compatibility, SQL literal/precedence/sargability/type hazards, concurrency/idempotence races, state-transition metadata cleanup, live-test production safety and portable env loading, mock/runtime shape vs real query shape, runtime shape parity for service/query/helper inputs, route method/source drift, affected-row checks after repair/update/delete, SQL tenant/owner/current-DB gaps, stale or dry-run-only proof artifacts, UI/rendered-output escaping and preview parity, docs/contracts with real paths and commands, valid falsy inputs including zero/false/empty string, duplicate helpers/writers, unsafe substring environment checks, and original-vs-transformed identity fields.

## 100% Quality Gate

Do not call this skill complete, correct, or ready unless it satisfies all of these:

1. It triggers for every substantive code, data, UI, review, debug, architecture, and risky config task.
2. It blocks action when current source truth has not been read.
3. It blocks schema/query/data-sensitive confidence based only on mocks, migrations, or diffs.
4. It requires live or migrated-integration DB proof when runtime database shape can break the task.
5. It requires headless browser proof for UI, PDF upload, file upload, preview/download, modal, navigation, and rendered-output workflows.
6. It forces root cause, ownership, blast radius, edge cases, SRP classification, scope lock, and verification planning before action.
7. It names governed artifacts and allowed-path constraints when the repo uses entity preflight, merge readiness, contracts, plans, or repo-local profiles.
8. It expands beyond the immediate bug or file into the operator workflow, business case, upstream/downstream process, rollout path, and success criteria.
9. It remains read-only: it must not edit, branch, commit, delegate coding, run mutating commands, or fix the bug from inside Deep Think.
10. It routes any implementation into the appropriate downstream workflow before edits, rather than continuing from precheck into implementation.
11. It reviews plans as executable risk objects, not prose: every plan must have objective, evidence, ordered tasks, dependencies, acceptance criteria, verification, rollback/abort conditions, and named non-goals.
12. It blocks plan approval when the plan lacks source-truth reads, ownership seams, path containment, test/proof mapping, rollout/merge gates, or unresolved-risk handling.
13. It adds alternatives and contrarian analysis for ambiguous or high-impact plans, then explains why the recommended path wins.
14. It requires a concrete zoom-out map for debugging, planning, and refactor work; broad-context language is not enough unless callers, consumers, siblings, states/statuses, tests, and workflow impact are named.
15. It enumerates lifecycle/status cohorts for stateful behavior before approving a query, filter, coverage calculation, or plan; do not fix one visible state while missing adjacent active states.
16. Its eval suite in `evals/evals.json` covers the required failure classes, and `scripts/validate_evals.py` passes.

## When To Use

Use Deep Think by default for:

- Bug fixing and debugging
- Feature implementation and API changes
- Refactors and cleanup work
- Code review and risk analysis
- Architecture or design decisions
- Risky operational or configuration changes

Exemptions:

- Pure conversational chat
- Tiny low-risk housekeeping with no behavioral risk, such as copy edits, comment-only
  wording tweaks, or formatting-only changes

If a task touches code, data flow, runtime behavior, ownership seams, or system design,
Deep Think applies.

## Read-Only Boundary

Deep Think is allowed to read, reason, and produce an operational handoff. It is not
allowed to implement.

Never do any of these inside Deep Think:

- Edit files or apply patches
- Create a feature worktree or branch
- Commit, push, open a PR, or resolve review threads
- Delegate implementation or ask a subagent to write code
- Update implementation plans or contracts as if the build lane has begun
- Run mutating database, migration, production, or live-system commands
- Convert the diagnosis directly into a quick fix

If the user asked for a fix, Deep Think still stops at the handoff. The next workflow
stage may implement after its own gates pass.

## Routing Gate After Thinking

Before ending the handoff, classify the next action:

- `NO_EDIT`: analysis, review, investigation, or test plan only. Stop after the precheck or handoff.
- `QUICK_DIRECT`: tiny, low-risk, bounded change with no schema/data/UI/PDF/integration/governed ownership risk. State why enterprise is not needed, then stop. Do not perform the edit inside Deep Think.
- `ENTERPRISE_REQUIRED`: feature work, significant bugfix, refactor, schema/query/data work, UI/PDF/file workflow, integration, governed entity/table work, multi-file behavior, or anything needing plan/contract/review/verify proof. Stop Deep Think and route to `enterprise` or the repo-local enterprise overlay before implementation.

In Helpdesk, prefer the repo-local enterprise overlay for `ENTERPRISE_REQUIRED`.
If governed artifacts are missing, the routing decision is still `ENTERPRISE_REQUIRED`
and the next step is the appropriate enterprise discovery/plan/contract stage, not
direct coding.

For non-`QUICK` enterprise work, the downstream route must include review -> forge
-> verify. Deep Think must not hand off a reviewed-but-not-forged lane directly to
verification or completion.

## Plan And Plan-Review Mode

Use this mode whenever the user asks for a plan, asks whether a plan is good, asks to
review another agent's plan, or provides a plan before implementation.

Deep Think must treat the plan as a falsifiable execution object. Do not reward
confident prose. Verify that the plan names what will be changed, why that change is
needed, which source truth supports it, what sequence avoids breakage, and how the
work will prove itself.

For plan creation, produce the smallest plan that can safely achieve the objective.
For plan review, lead with one verdict:

- `APPROVE`: the plan is specific, source-grounded, sequenced, contained, and verifiable.
- `REVISE`: the plan is directionally right but needs concrete fixes before execution.
- `BLOCK`: the plan is unsafe, ungrounded, missing ownership/proof, or likely to create avoidable damage.

Every plan review should check:

- Objective and success criteria: the plan solves the user's actual workflow problem, not just a nearby technical symptom.
- Source evidence: each major task points to real source files, symbols, configs, schemas, logs, docs, or live proof still required before editing.
- Ownership and containment: tasks stay inside the correct module, service, entity, table, contract, or allowed-path boundary.
- Sequencing and dependencies: tasks are ordered so tests, migrations, UI/API seams, data backfills, and review gates happen in a safe order.
- Acceptance criteria: each task has a clear done condition and a proof command or evidence artifact.
- State/status coverage: lifecycle-driven work enumerates all active, queued, submitted, approved, terminal, and excluded states before changing filters, guards, totals, or status transitions.
- Negative cases: the plan names what could falsify it, where it could fail, and when to stop or redesign.
- Alternatives: ambiguous plans compare at least two credible routes, or explicitly justify why one route is the only reasonable route.
- Rollback and rollout: risky work names rollback, feature flag, deployment, migration, or post-merge observation needs.
- Scope control: tempting cleanup is classified as `fix-now`, `follow-up`, or `note-only`.
- Final readiness: the verdict says exactly what must change before coding, or why execution can proceed through the proper workflow.

## Workflow

### 1. Restate the Ask

Before acting, state:

- What the user explicitly asked for
- Plausible alternate interpretations
- Important missing context or assumptions
- Whether the prompt describes a symptom, a desired outcome, or both

### 2. Map the Broader Context

Do not frame the work only around the failing line, reported symptom, or nearest
implementation detail. Before deciding what matters, name the broader context:

- Operator or customer workflow: who does this, when, and what happens before/after
- Business case: why this matters, what outcome is valuable, and what failure costs
- Program/lane context: active PR, branch, release, incident, deployment, or governed pipeline
- Upstream and downstream process: inputs, approvals, queues, jobs, external systems, and handoffs
- Success criteria: what "fixed", "ready", "safe", or "better" means from the user's workflow perspective
- Non-goals: adjacent business or workflow improvements that are tempting but outside this task

If the broader workflow or business case is unclear, say that explicitly and keep the
implementation recommendation conditional.

For debugging, planning, and refactor work, this step must include a bounded `zoom-out` pass:

- Current focus: the file, symbol, route, worker, UI flow, bug, or decision under review
- First ring: direct callers, upstream entry points, downstream consumers, sibling modules, tests, docs, and runtime jobs
- Escalation ring: one more layer only if the first ring does not explain root cause, ownership, lifecycle/status cohort, blast radius, or proof path
- State/status lifecycle: all statuses or phases that should count as the same business cohort, plus terminal or excluded statuses
- Ownership boundary: the module that owns the behavior versus modules that only consume or display it
- Disconfirming cases: the nearest sibling flow that would stay broken if the proposed fix only patches the first visible instance

For example, a coverage calculation over pre-submit purchase orders should not check only
one visible draft status. It should prove which statuses are part of the pre-submit cohort
such as draft, pending approval, approved, spend approved, submitted, cancelled, and closed,
then include or exclude each from source-grounded business rules.

### 3. Treat Plans As Hypotheses

When a plan exists or is being requested, evaluate it before accepting its framing:

- What is the plan trying to make true for the operator, customer, system, or release?
- Which assumptions does the plan depend on, and which are already proven by source?
- Which tasks are missing, duplicated, out of order, too large, or not independently verifiable?
- Which dependency, migration, schema, UI, auth, tenant, data, or deployment step can invalidate the plan?
- What would make the plan fail even if each individual task is completed?
- What is the leaner alternative, the safer alternative, and the reason they do or do not win?
- What is the readiness verdict: `APPROVE`, `REVISE`, or `BLOCK`?

Do not convert a vague plan into implementation momentum. If the plan does not expose
its proof path, ownership, containment, and stop conditions, classify it as `REVISE`
or `BLOCK`.

### 4. Read the Source of Truth Before Reasoning

Do not guess from memory, naming patterns, or “what this codebase probably does.”

Before proposing a fix, design, or review conclusion:

- Read the actual source of truth files, symbols, or configs for the path you are discussing
- Prefer authoritative symbol-level or file-level reads over inference
- Verify real function names, exports, schemas, route mounts, config keys, and call paths
- For schema, query, tenant, identity, money, order, invoice, inventory, or integration behavior, verify real database/runtime shape with live or migrated-integration proof when available
- For UI, PDF upload, file upload, preview/download, modal, navigation, or rendered-output behavior, plan headless browser proof rather than manual GUI confidence
- If filesystem or source access is unavailable, say so plainly instead of pretending certainty

For code work, “grounded” means you inspected the real implementation, not a remembered pattern.
For data-sensitive work, “grounded” also means you did not rely on mock-only, migration-only, or diff-only evidence.

### 5. Ground Truth Before Action

After reading the source, establish:

- Entry point, call path, or consumer path
- Root cause hypothesis, not just the crash site
- Same-file siblings, module siblings, and cross-module siblings
- Existing patterns or authoritative implementations already in the codebase

For bugs, search for the bug class, not just the reported instance.

For features, map existing seams and consumers before inventing a new path.

### 6. Map Blast Radius

For every likely change, identify the surrounding surface:

- Imports, call sites, route handlers, jobs, workers, webhooks, and scheduled tasks
- Data contracts, schemas, migrations, config, feature flags, or external integrations
- Tests that already cover the path and tests that should exist but do not
- Downstream assumptions that could break when behavior changes
- Required evidence level: unit, integration, live DB, E2E, headless browser, log/readback, or deploy proof

If you cannot describe the blast radius, you are not ready to implement.

### 7. Check Ownership and Source of Truth

Identify the authoritative seam before editing:

- Which module or service owns the behavior
- Which write path, registry, or contract is the source of truth
- Whether the path is governed, tenant-scoped, or owner-restricted
- Whether your planned change widens responsibility into the wrong layer
- Whether an entity preflight, merge-readiness artifact, contract, plan, or repo-local profile constrains the allowed paths

If ownership is ambiguous, stop and surface that before coding.

### 8. Sweep Edge Cases and Failure Modes

For substantive tasks, think through at least:

- Empty, null, missing, stale, partial, or duplicated input
- Max-size or high-volume input
- Retry, race, double-submit, or replay behavior
- Permission/auth failures
- Dependency failure, timeout, or degraded external responses
- State/status lifecycle drift: missing adjacent statuses, terminal-state leakage, stale transitions, or mismatched display/API/database names

Do not ship a golden-path-only answer.

### 9. Evaluate SRP and Refactor Opportunities

Always note SRP and cleanup opportunities, but classify them explicitly:

- `fix-now`: required to land the correct solution safely
- `follow-up`: valuable but not required for this task
- `note-only`: observed, but intentionally out of scope

Deep Think should reduce mess, not create scope creep. Do not smuggle a large refactor
into a focused fix unless the current structure makes a safe fix impossible.

### 10. Lock Scope and Verification

Before concluding, state:

- What you found or believe is true
- What the next workflow should change
- For plan work: the plan verdict, required revisions, and any blocked assumptions
- What Deep Think did not change
- What could still go wrong
- How you will verify behavior, blast radius, and regressions with fresh evidence
- Whether verification needs live DB proof, full E2E trace, or headless browser coverage
- Whether non-`QUICK` enterprise work also needs adversarial forge/recycle proof before verification
- Routing decision: `NO_EDIT`, `QUICK_DIRECT`, or `ENTERPRISE_REQUIRED`
- If `ENTERPRISE_REQUIRED`, the exact enterprise or repo-local enterprise stage to invoke next

### 11. Stop Conditions

Pause and escalate before coding if any of these are true:

- The next step is any implementation, patch, branch/worktree, PR, review-thread, migration, or live-system mutation
- You only found a symptom, not the cause
- The workflow/business objective is still too narrow or unclear
- Blast radius is still unknown
- Ownership or source-of-truth seams are unclear
- You have not read the actual implementation you are about to discuss or modify
- The fix appears to widen a governed or owner-restricted path
- A redesign is needed instead of another patch
- A plan is missing source evidence, task proof, ownership, sequencing, rollback/abort conditions, or acceptance criteria
- A plan review would approve work whose verification or merge/deploy gates are not named
- You are relying on “probably fine” rather than evidence
- Schema/query/data claims are based only on mocks, migrations, or diffs
- UI/PDF/file/rendered workflow claims lack a headless verification path
- The next action is implementation but the routing decision is `ENTERPRISE_REQUIRED`
  and enterprise/overlay stage entry has not started

## Checklist

Use this checklist before substantive action:

- Restated the actual ask and important assumptions
- Mapped the broader operator workflow, business case, upstream/downstream process, and success criteria
- Completed a concrete zoom-out map for debugging, planning, refactor, or confusing-code work
- For plan work, classified the plan as `APPROVE`, `REVISE`, or `BLOCK`
- For plan work, checked objective, assumptions, dependencies, task order, acceptance criteria, rollback/abort conditions, and proof mapping
- For state/status work, enumerated the full lifecycle cohort and terminal/excluded states before approving the plan
- For ambiguous work, compared credible alternatives or explained why alternatives are not useful
- Read the actual source-of-truth files, symbols, or configs
- Traced the entry point, consumer path, or failure path
- Searched for same-pattern siblings
- Mapped blast radius across consumers and tests
- Identified the ownership seam and source of truth
- Walked edge cases and failure modes
- Classified refactor opportunities as `fix-now`, `follow-up`, or `note-only`
- Locked scope and named verification steps
- Classified next action as `NO_EDIT`, `QUICK_DIRECT`, or `ENTERPRISE_REQUIRED`
- Stopped Deep Think before any edit, worktree, branch, PR, implementation delegation, or mutating command
- Routed substantive implementation to enterprise or the repo-local enterprise overlay as a handoff before edits
- Named the required proof level: unit, integration, live DB, E2E, headless browser, log/readback, or deploy proof
- Blocked mock-only, migration-only, diff-only, or manual-GUI-only confidence where stronger proof is required

## Templates

Use this template when presenting the preflight:

```markdown
DEEP THINK PRECHECK

- Ask: [what the user asked for]
- Interpretations / assumptions: [important alternatives or missing context]
- Broader context: [operator/customer workflow, business case, upstream/downstream process, active lane/release/incident context, success criteria]
- Zoom-out map: [focus, callers, upstream/downstream, sibling modules, lifecycle/status cohort, tests/docs, ownership boundary]
- Source read: [files, symbols, configs, or an explicit note that source access is unavailable]
- Root cause / objective: [what seems actually wrong or what outcome is required]
- Blast radius: [callers, consumers, contracts, tests, integrations]
- Ownership / source of truth: [authoritative seam, owner path, governed surface]
- Edge cases / failure modes: [null, empty, retry, race, stale data, auth, dependency failure]
- SRP / refactor opportunities:
  - fix-now: [...]
  - follow-up: [...]
  - note-only: [...]
- Scope lock: [what will change and what will not]
- Verification: [tests, checks, live DB/readback proof, E2E trace, headless browser proof where relevant, regression sweep]
- Plan verdict: [APPROVE | REVISE | BLOCK, with required changes before execution]
- Alternatives / contrarian risk: [credible alternatives considered, strongest reason the recommended path may be wrong]
- Routing decision: [NO_EDIT | QUICK_DIRECT | ENTERPRISE_REQUIRED, with next stage/skill if enterprise is required]
- Read-only boundary: [confirm Deep Think made no edits, branches/worktrees, mutating commands, or implementation delegation]
```

When finishing the task, explicitly confirm what you verified and whether any blast-radius,
ownership, or refactor follow-ups remain.
