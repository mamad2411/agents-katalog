---
name: itsol-initiative-delivery
description: "Deliver multi-phase initiatives beyond one plan with traceability and resumable state."
---

# ITSOL Initiative Delivery

Use for a broad business source whose complete outcome needs multiple implementation and QA phases. This is a delivery-scope layer, not an authority mode: resolve `itsol-workflow-mode`, record `delivery_scope: initiative`, and normally use `autonomous-planned`. `direct` is not valid for an initiative.

## Contract

- Analyze the complete source before selecting work.
- Give every requirement a stable `REQ-NNN` and explicit disposition; never ship one slice as the whole initiative.
- Preserve the original source as an immutable snapshot and keep intent, traceability, roadmap, architecture, decisions, progress, and evidence in durable repository state.
- Decompose into dependency-aware, outcome-oriented vertical phases. Existing planning, proportionate verification, delegation, review, integration, and QA contracts apply inside each phase; TDD remains explicitly opt-in.
- Continue dependency-ready phases without routine approval pauses in `autonomous-planned`.
- Ask only for a material product, scope, data, security, rollout, architecture, or protected-action decision that cannot be safely recommended.

## Lifecycle

1. **Intake:** inspect the whole source and repository; extract requirements, acceptance criteria, constraints, unknowns, and initiative completion criteria.
2. **Roadmap:** assign every requirement to phases; record dependencies, outcomes, architecture, rollout/rollback, and system-QA coverage.
3. **Review:** self-review proportionately. Use isolated review only when policy or breadth, novelty, uncertainty, cross-phase dependency, or material risk justifies it; resolve concrete findings only.
4. **Phase loop:** plan, review, implement, review changed surfaces, integrate, run application-aware QA, and record fingerprint-bound evidence. Start the next dependency-ready phase automatically.
5. **Failure loop:** classify QA failure as `implementation-fix`, `plan-revision`, or `user-decision`; update affected artifacts, rerun applicable reviews, and execute fresh QA. A code change invalidates the affected final QA.
6. **Adapt/complete:** record discoveries and decisions, update living documents, and finish only when every requirement is dispositioned, phases and QA pass, decisions are closed, and documentation is synchronized.

## Decision and QA boundaries

Record ordinary technical choices autonomously. Ask one bundled question when equally plausible choices materially change product behavior, permissions, data, rollout, architecture, cost, or scope. Deferring or rejecting a requirement requires a resolved user decision.

Resolve `.itsol.md` QA policy before creating QA work:

- `off` skips the QA gate and must be reported as a policy skip, never as PASS;
- `evidence` accepts configured command/manual evidence without automatic specialists;
- `automatic` selects application-aware coverage;
- `strict` applies the strongest configured coverage.

QA is observed, not merely planned, and binds PASS to the implementation fingerprint. Use the real surface: browser UI, Electron/CDP, interactive CLI, API contract/integration/security, mobile runtime, data integrity/migration/rollback, or infrastructure readiness/observability/rollback. Do not replace required application checks with a generic test command.

Protected destructive/external actions retain separate authority. Do not hide gaps behind phase counts.

## Durable artifact layout

```text
.itsol/initiatives/<initiative-id>/
├── source/                    # immutable input
├── initiative.md             # normalized intent
├── requirements.md           # REQ-to-phase/evidence traceability
├── roadmap.md                # reviewed dependency-aware phases
├── architecture.md           # baseline and ADR links
├── progress.md               # current progress and next action
├── decisions/                # DEC/ADR records
├── qa/                       # fingerprint-bound verdicts
├── phases/<phase-id>-<slug>/ # phase plans/results/evidence
└── state.json                # canonical machine-readable state
```

Keep `.itsol.md` for stable repository policy, not initiative progress or temporary decisions. Update living artifacts after each material discovery and link decisions to requirements/phases.

## Requirement and phase contracts

Each requirement is `planned`, `in-progress`, `implemented`, `blocked`, `deferred`, or `rejected`. `deferred` and `rejected` require a linked user decision. Avoid invented percentage progress.

A phase defines outcome and requirement IDs, dependencies/contracts, mode-required artifacts, proportionate verification, ownership/review surfaces, integration and QA criteria, rollout/rollback, and observable `done_when` evidence. Complete it only after its requirements and integration/QA evidence are satisfied; phase completion does not complete the initiative.

## Execution state

Load `itsol-execution-policy` after workflow mode and propagate it through every phase and packet. Use bounded parallel batches and do not invent a whole-initiative numeric agent ceiling. Phase/initiative completion is evidence-based, never inferred from an agent stopping.

## Autonomous control loop

```text
load durable state
→ resolve decision/protected blocker
→ refresh stale roadmap review
→ choose dependency-ready phase
→ plan → review → delegate independent work → implement
→ review changed surfaces → integrate → application-aware QA
→ PASS: record requirement/phase evidence and continue
→ FAIL: fix, replan, or ask; rerun required reviews and fresh QA
```

If a session stops, leave canonical state and a resumable next action; never claim completion.

## Completion evidence

Require: all phases complete; every requirement `implemented`, `deferred`, or `rejected`; decisions and material findings closed; fingerprint-bound PASS for every phase and current final-system QA/regression PASS; synchronized docs/architecture; rollout/rollback evidence when relevant; and exact initiative `done_when` criteria. Final handoff reports outcomes, dispositions, decisions, verification, operational notes, and authorized deferrals.
