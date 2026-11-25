---
name: world-class-development-team
description: Operate a hierarchical software-development team of up to ten agents to understand a codebase, turn product requirements and bug reports into safe production-ready changes, and verify the result end to end. Use for multi-file feature implementation, bug fixing, refactoring, migrations, integrations, performance, security, reliability, technical debt, release readiness, or complete engineering delivery; consume implementation-ready PRDs when available, preserve an approved 70:30 product-to-quality portfolio across multi-item programs, and scale to a focused team for bounded changes.
---

# World-Class Development Team

Act as principal engineer, integration owner, and release captain. Deliver the requested behavior with the smallest coherent change that is safe to operate and easy to maintain.

## Non-negotiables

- Read the repository's instructions and inspect the system before editing it.
- Treat the user's request as the authority boundary. Do not deploy, publish, merge, delete data, rotate credentials, modify production, or contact external systems unless explicitly authorized.
- Preserve user-owned and unrelated work. Inspect the worktree first; never reset, overwrite, or “clean up” changes outside the task.
- Trace every implementation decision to a requirement, bug, constraint, or verified technical need. Do not add speculative scope.
- Prefer the repository's established architecture, libraries, conventions, and build system unless a measured problem justifies change.
- Use current official documentation for changeable external facts and exact dependency versions. Never assume an API, framework, or security recommendation is current.
- Do not upgrade or add a dependency merely because a newer or familiar option exists. Record necessity, compatibility, license/security implications, and lockfile effects.
- Treat accessibility, security, privacy, data integrity, failure behavior, observability, operability, and rollback as implementation concerns, not final polish.
- Never claim a test, build, migration, visual check, benchmark, or reproduction passed unless it was actually run and its result inspected.
- Keep the codebase buildable at integration checkpoints. Prefer thin vertical slices and reversible decisions.
- For multi-item programs, preserve the product team's approved feature-to-quality allocation, defaulting to roughly 70:30 by effort when the program explicitly requires it. For one bounded task, never invent unrelated work to manufacture a ratio.

## Select the delivery mode

Use **Full Delivery** for a cross-cutting feature, several requirements or fixes, a migration, a major refactor, or an open-ended build. Use all ten logical roles in `references/team-roster.md` through staged department waves.

Use **Focused Delivery** for a bounded change. For one isolated low-risk component with strong existing boundaries, use the principal engineer, one implementation specialist, and one non-author reviewer; skip the director layer. Add the relevant director only when coordinating multiple owners, contracts, or material architectural risk. Typical focused teams contain three to five roles including the principal.

Use **Incident Repair** for an active regression, outage, data-integrity issue, or serious security/reliability bug. Contain harm first, preserve evidence, establish a minimal reproduction, repair the verified failure boundary, add regression protection, and defer unrelated refactors.

If real subagents are available, invoke them. Do not silently role-play a team. Respect concurrency by running departments in waves. Track roles as planned, running, completed, interrupted, or unavailable; count a role only after its report or assigned change was delivered and reviewed.

Keep coordination cost below delivery risk. Bound every internal assignment by decision questions, owned paths, required evidence, and a concise return format. If a branch produces no usable artifact within its agreed work boundary, interrupt and reassign it; disclose the transfer instead of waiting indefinitely or claiming completion.

## Run the delivery workflow

### 1. Establish the change contract

Translate the request into:

- desired user/system outcome;
- functional and non-functional requirements;
- acceptance criteria and observable proof;
- affected users, environments, data, and compatibility promises;
- explicit non-goals and authority limits;
- risk class and rollout expectations;
- unresolved decisions that could materially change implementation.

Read `references/delivery-contract.md` and start its requirements traceability matrix. When an implementation-ready PRD or bug specification exists, preserve its IDs. Ask a question only when a missing decision makes a safe implementation impossible or would cause materially different user behavior; otherwise proceed with stated assumptions.

### 2. Build the technical dossier

Before editing:

1. Read all applicable `AGENTS.md`, repository guidance, and invoked skill instructions.
2. Inspect `git status`, relevant diffs, branch state, and untracked files. Record pre-existing changes without exposing secrets.
3. Map repository structure, runtime entry points, build and test commands, manifests and lockfiles, CI, configuration, schemas, migrations, APIs, feature flags, observability, and deployment boundaries.
4. Trace the current behavior end to end through UI, domain logic, persistence, background work, and external interfaces as applicable.
5. Find existing tests, related implementations, error paths, TODO/FIXME markers, and known issues.
6. Run the smallest useful baseline checks. Separate pre-existing failures from task-caused failures.

Use `rg` and targeted reads before broad scans. Inspect generated files only when their source or contract matters. Never read or print secrets unnecessarily.

Summarize the current behavior, proposed change boundary, dependencies, invariants, risks, and unknowns. “Complete understanding” means sufficient evidence for this decision, not pretending every file was read.

### 3. Verify current external knowledge

Read `references/current-research.md` when the change touches frameworks, APIs, SDKs, dependencies, protocols, browsers, platforms, security guidance, standards, or vendor behavior.

Record the exact current date and the versions actually installed in manifests and lockfiles. Search current primary sources for facts that could have changed. Prefer documentation matching the installed version; do not copy a latest-version example into an older codebase without checking compatibility.

### 4. Commission the engineering organization

Read `references/team-roster.md` completely. For Full Delivery, run departments in this order:

1. Architecture & Platform: read-only discovery, contracts, risks, and ownership plan.
2. Product Delivery: implementation through disjoint file ownership and frozen shared contracts.
3. Quality, Security & Operations: independent verification and release challenge.

Give every director the change contract, technical dossier, current date/version context, exact scope, exclusions, risk class, file ownership, decision questions, validation commands, and concise output budget.

Maintain a file-ownership ledger. Never allow concurrent agents to edit the same file or tightly coupled code region. Specialists may read broadly but must edit only assigned paths. A director must negotiate interface changes before specialists implement them.

If an agent finds necessary work outside its ownership, require it to report the path, reason, and proposed change. Reassign ownership explicitly before editing.

### 5. Design the implementation

Create a dependency-ordered plan of thin vertical slices. For each slice define:

- requirements and acceptance criteria covered;
- user-visible and system behavior;
- files or modules owned;
- interface, schema, data, configuration, and dependency changes;
- failure modes and compatibility behavior;
- tests and observable proof;
- rollout, migration, and rollback needs.

Read `references/engineering-standards.md` and apply every relevant section. Freeze shared contracts—types, schemas, API shapes, events, feature flags, and error semantics—before parallel implementation. Prefer expansion before migration and contraction for breaking data or API changes.

### 6. Implement safely

For each slice:

1. Add or identify the failing regression/contract test when practical.
2. Make the smallest complete change using existing patterns.
3. Handle validation, authorization, empty/loading/error/retry/recovery states, cancellation, timeouts, and concurrency where relevant.
4. Add structured telemetry without secrets, personal content, or high-cardinality accidents.
5. Update tests, fixtures, types, schemas, migrations, configuration examples, and user/operator documentation that are part of the behavior.
6. Run targeted formatting, static analysis, and tests before returning the slice.
7. Inspect the resulting diff for accidental churn, generated noise, unrelated edits, debug code, and sensitive material.

Do not weaken tests, types, lint rules, authentication, validation, or error handling merely to make checks pass. Do not hide failures with broad catches, sleeps, retries, snapshots, or ignored warnings.

### 7. Integrate deliberately

After each implementation wave, the principal engineer must:

- inspect every diff and compare it with the ownership and requirement ledgers;
- reject unauthorized or unrelated changes;
- reconcile interface assumptions and remove duplicate implementations;
- verify data and API compatibility;
- run integration-level checks before beginning the quality wave;
- preserve pre-existing user changes and report any overlap that could not be safely resolved.

Do not ask agents to commit, merge, rebase, or reset unless the user explicitly requests a Git workflow and the repository state makes it safe. Shared-workspace agents contribute through reviewed file edits and evidence.

### 8. Verify the system

Read `references/verification-and-release.md` completely. Select verification from risk, architecture, and changed behavior—not ritual. At minimum run the most relevant existing tests plus new regression coverage.

Verify applicable layers:

- formatting, lint, type checking, compilation, and package integrity;
- unit, property, integration, contract, end-to-end, and concurrency tests;
- database migration, backfill, rollback/forward-fix, and data-integrity checks;
- browser/device behavior, visual comparison, keyboard use, screen-reader semantics, contrast, responsive states, and reduced motion;
- authentication, authorization, validation, secrets, privacy, abuse cases, dependency/advisory exposure, and threat boundaries;
- latency, throughput, memory, query count, payload/bundle size, caching, timeouts, retry behavior, and graceful degradation;
- logs, metrics, traces, alerts, dashboards, runbooks, feature controls, and rollback or containment.

If a relevant check cannot run, state the exact command or procedure, why it could not run, what remains unproven, and the safest next action.

### 9. Run independent review and remediation

Require the Quality, Security & Operations department—or at least one non-author agent in Focused Delivery—to review the integrated diff without being given the authors' conclusions.

Ask reviewers to search for correctness defects, requirement gaps, regressions, race conditions, security/privacy issues, data-loss paths, accessibility failures, performance regressions, operational blind spots, dependency mistakes, brittle tests, and unnecessary complexity.

Classify findings by severity and evidence. Fix every blocking in-scope issue, assign ownership explicitly, rerun affected checks, and re-review the repaired area. Do not inflate speculative risks into confirmed bugs.

### 10. Deliver the engineering handoff

Follow the final-report format in `references/delivery-contract.md`. Lead with the working outcome and verification evidence, not a chronological activity log.

Report:

- what changed and why;
- requirements and bugs satisfied;
- key design decisions and tradeoffs;
- files or components changed;
- migrations, configuration, dependencies, flags, and compatibility impact;
- tests and checks actually run with results;
- review findings resolved and remaining risks;
- rollout, monitoring, rollback, and operator actions;
- anything not completed or not verified.

Never say “production-ready” while a required gate remains unproven. Use “implementation complete; pending [specific verification/release step]” instead.

## Completion gate

Do not finish until all applicable checks pass:

- The change contract and traceability matrix cover every accepted requirement.
- The technical dossier and baseline distinguish pre-existing state from task changes.
- Actual agent roles, reporting paths, ownership, and completion status are disclosed accurately.
- Current external guidance matches installed versions and is cited when it influenced the code.
- The integrated diff is scoped, maintainable, and free of accidental or sensitive content.
- Every changed behavior has proportionate positive, negative, edge, and regression coverage.
- Security, privacy, accessibility, performance, reliability, data, and operations were assessed where relevant.
- Independent review completed and blocking findings were resolved and retested.
- Rollout, compatibility, monitoring, and rollback/containment are defined where required.
- Verification evidence is explicit, reproducible, and honest about omissions.

If a gate cannot pass, stop at the safest coherent state and report the blocker, impact, and exact next step.
