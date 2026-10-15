---
name: semantic-safe-implementation-refactor
description: "Use when the primary change is replacing an implementation while keeping the public surface and technology model materially stable. Triggers: rewrite a messy service behind the same interface, replace legacy logic with a clean module, reimplement a subsystem behind an existing contract, or introduce an adapter or facade so a new implementation can take over. Do not use when the main work is moving module, package, or caller boundaries (use `semantic-safe-module-boundary-migration`) or when a framework, runtime, version, module system, or programming model change is the main source of risk (use `semantic-safe-technology-migration`)."
---

# Semantic-Safe Implementation Refactor

This skill is a **Pipeline + Reviewer** for semantic-preserving implementation replacement. Choose it only when **implementation is the primary thing changing** and the external surface, module boundary, and technology model are intended to stay materially stable.

---

## Use When

Use when the user asks to:

- replace brittle legacy logic with a cleaner implementation behind the same interface or contract
- rewrite a component, service, handler, or workflow without intentionally changing its public behavior
- extract a cleaner subsystem behind an existing route, schema, event, adapter, or facade
- introduce a new implementation path and cut traffic over after equivalence is proven
- reimplement from observed semantics instead of copying the old control flow

Do **not** use for:

- tiny local fixes where a small edit is clearly safer than replacement
- speculative rewrites when the existing semantic contract has not been established
- redesigns that intentionally change product behavior, domain meaning, or public contracts without an explicit decision
- style-only cleanup or mechanical formatting changes
- module, package, path, or ownership moves where caller migration is the main work (use `semantic-safe-module-boundary-migration`)
- framework, runtime, library version, module system, or programming-model migrations where the technical change itself drives the plan (use `semantic-safe-technology-migration`)

## Boundary Test

Choose this skill only if the task can be summarized as:

> Keep the surface materially stable; replace the implementation safely.

If the task is mainly about **where a module lives or how callers reach it**, use `semantic-safe-module-boundary-migration`.
If the task is mainly about **upgrading or switching technology**, use `semantic-safe-technology-migration`.

---

## Operating Modes

- **`audit`** - read the current implementation, classify legacy behaviors, extract the semantic contract, find the replacement seam, and produce a refactor plan without editing files
- **`replace`** - implement the new module or path, add the minimum bridging changes for cutover, and update ADRs only if semantics or architecture intentionally changed

If intent is ambiguous, default to **`audit`**.

---

## Pipeline

`Intake → Detect Intent & Preservation Boundary → Extract Semantic Contract → Design Replacement Boundary ──[ADR Gate]──▶ Implement New Path → Verify Semantic Equivalence → Cut Over`

- **Intake** - identify the target surface: file, module, subsystem, handler, service, or flow; find existing tests, docs, contracts, and ADRs first.
- **Detect Intent & Preservation Boundary** - infer user intent, artifact intent, and system intent from evidence. State which layers must remain stable: behavior, contract, domain meaning, and public names.
- **Extract Semantic Contract** - map inputs, outputs, invariants, side effects, errors, naming, public/internal boundaries, and observable behavior. For control-sensitive or data-sensitive code, also trace the branch, exception, state-transition, and value-lineage paths that determine observable outcomes. Classify legacy behaviors as Intentional, Relied-upon accidental, Ambiguous, or Dead.
- **Design Replacement Boundary** - choose the smallest clean seam: new module behind the same interface by default, then façade, adapter, branch-by-abstraction, strangler path, or feature flag when conditions require.
- **ADR Gate** - if the refactor changes externally visible semantics, shared boundaries, architecture, data meaning, or long-lived contracts, stop. In `audit`, report the ADR requirement. In `replace`, **DO NOT** continue until the decision is recorded.
- **Implement New Path** - write the replacement code in a new module or isolated path first; touch old code only where needed for seams, adapters, or routing.
- **Verify Semantic Equivalence** - prove the new path preserves the contract; map evidence to each preserved layer.
- **Cut Over** - follow the cutover checklist; deprecate legacy entry points when safe; document residue.

Do **not** default to in-place mutation of tangled code when a replacement seam can be introduced.

---

## Execution

Load on demand:

1. **During `Detect Intent & Preservation Boundary`:** [references/intent-detection.md](./references/intent-detection.md)
2. **During `Extract Semantic Contract`:** [references/semantic-contract.md](./references/semantic-contract.md) and [references/legacy-debt-handling.md](./references/legacy-debt-handling.md)
3. **During `Design Replacement Boundary`:** [references/seam-selection.md](./references/seam-selection.md)
4. **When legacy behavior depends on branch structure, exception paths, state transitions, or value lineage:** [references/advanced-analysis.md](./references/advanced-analysis.md)
5. **During `Implement New Path` and cutover planning:** [references/workflow.md](./references/workflow.md)
6. **During `Verify Semantic Equivalence`:** [references/equivalence-checks.md](./references/equivalence-checks.md)
7. **During `Cut Over`:** [references/cutover-checklist.md](./references/cutover-checklist.md)
8. **Only if `ADR Gate` opens:** [references/adr-gate.md](./references/adr-gate.md)

Use [assets/refactor-plan-template.md](./assets/refactor-plan-template.md) as the output format for `audit` mode.

Read the existing implementation before proposing a rewrite. Prefer the smallest clean seam that lets the new implementation stand on its own.

---

## Core Rules

- **Semantics first**: preserve externally observable meaning, invariants, and domain intent unless an explicit decision says otherwise.
- **Intent is inferred, not guessed**: rank evidence as user constraints → tests → contracts → call sites → docs → comments → code shape.
- **State the preservation boundary**: declare which layers must stay stable before writing replacement code.
- **Classify before porting**: mark every notable legacy behavior as Intentional, Relied-upon accidental, Ambiguous, or Dead before the replacement is written.
- **Replace, do not accrete**: prefer a new module or isolated path over more branches in legacy code.
- **Contract before code**: extract the semantic contract before choosing abstractions or file layout.
- **Use flow analysis only when it clarifies semantics**: trace control-sensitive paths and data lineage to preserve observable behavior, not to cargo-cult legacy structure.
- **Bridge minimally**: touch legacy code only to create seams, adapters, or cutover points.
- **Prove equivalence**: map evidence to preserved layers; inspection alone is not enough.
- **Escalate intentional change**: if semantics, boundaries, or architecture change, open or update an ADR.
- **Expose residue**: call out remaining legacy paths, deprecated modules, partial migrations, and debt carry-forwards.

---

## Deliverables

### `audit`

Return using [assets/refactor-plan-template.md](./assets/refactor-plan-template.md):

- detected intent with confidence and evidence sources
- stated preservation boundary
- legacy behavior inventory with classes
- semantic contract
- replacement seam recommendation
- equivalence plan
- risk list and debt carry-forwards
- ADR requirement if the change is not purely semantic-preserving

Do **not** edit files.

### `replace`

Deliver:

- new or rewritten module(s) implementing the preserved contract
- minimal cutover or adapter edits in legacy call sites
- equivalence evidence mapped to the preserved layers
- completed cutover checklist with rollback notes
- ADR update only when semantics or architecture intentionally changed
- migration notes for deprecated paths or names

---

## Verification

- [ ] Existing behavior, interfaces, and constraints were read before redesigning internals.
- [ ] Intent was inferred from evidence in priority order, not guessed from code shape alone.
- [ ] The preservation boundary was stated before implementation.
- [ ] Legacy behaviors were classified before porting.
- [ ] A semantic contract was written down before implementation.
- [ ] The replacement was implemented in a new or isolated path where feasible.
- [ ] Legacy code was edited only for seam creation, bridging, or cutover.
- [ ] Equivalence evidence is mapped to the preserved layers.
- [ ] Cutover followed the checklist; rollback plan was defined.
- [ ] Intentional semantic or architectural changes triggered the ADR gate.
- [ ] Remaining legacy paths, deprecated names, and debt carry-forwards are called out.

---

## Final Standard

Result: the agent replaces brittle legacy implementation with cleaner code, proves the system still means and does the same thing, and leaves a clear record of every decision and residual debt—instead of deepening the hack.
