---
name: itsol-functional-planning
description: "Define user-visible scope, behavior, and acceptance criteria under the resolved mode."
---

# ITSOL Functional Planning

Resolve and preserve `itsol-workflow-mode` before discovery or planning. Do not redefine its authority contract here.

## Scope

If the source describes a whole application, module, migration, or multi-phase capability, load `itsol-initiative-delivery` first and build full traceability/roadmap. Otherwise:

1. Inspect request, repository evidence, and `.itsol.md`; propagate all seven state fields.
2. Load `itsol-requirements-review` and inspect enough code, contracts, tests, and conventions to avoid asking repository-answerable questions.
3. Ask only about material ambiguity that cannot be resolved safely; do not invent product scope from internet defaults.
4. Keep current-tech research, proportionate verification, implementation review, and protected-action authority independent from planning ceremony. Include TDD only on explicit user request.

## Modes

**governed:** full Discovery Gate when incomplete; write and proportionately self-review `Draft` Business and Technical Plans; apply the effective review trigger; present each specific file for explicit user approval; run Technical Decision and execution-mode gates. Only genuine user approval becomes `Approved`.

**autonomous-planned:** create the same plans as `Draft`; self-review proportionately, use isolated review only when policy/material risk warrants it, resolve concrete findings, choose the documented recommendation, mark plans `Ready for execution`, and continue without approval pauses. Never call this user approval.

**direct:** create no persistent Business/Technical Plans, plan reviews, approvals, Decision Gates, plan paths, or execution-mode approval. Use `artifact_state: not-required`, resolve only material ambiguity, then route implementation and proportionate verification.

With `adaptive`, the main agent decides whether isolated review adds material value from scale, uncertainty, novelty, blast radius, and verification strength. Selected read-only review needs no extra user authorization; suggestions, wording, optional detail, and speculation are not blockers.

Load `itsol-execution-policy` when resource, stop, delegation, or completion state matters. It owns budgets and evidence; never use `maxTurns` or termination as completion. This skill supplements, not replaces, `itsol-workflow-mode`.

## Focused references

- [01-planning-gates.md](./references/01-planning-gates.md) — mode-specific discovery, decision, approval, and execution routing.
- [02-plan-review.md](./references/02-plan-review.md) — proportional self/Rubber Duck review.
- [03-deep-planning-interview.md](./references/03-deep-planning-interview.md) — governed discovery and autonomous ambiguity handling.
- [04-business-plan.md](./references/04-business-plan.md) — Business Plan template.
- [05-technical-plan.md](./references/05-technical-plan.md) — Technical Plan, verification, and delegation.

Read only references needed for the resolved mode. `direct` normally needs only [01-planning-gates.md](./references/01-planning-gates.md).
