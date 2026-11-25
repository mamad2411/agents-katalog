---
name: architect-design
description: >
  Structured design process for the architect agent. Guides from grill conclusions
  to complete NOTES.md + tech-spec.md plus needed domain documentation updates
  through constraint gathering, module identification, interface design,
  alternative exploration, and risk analysis. Use when the architect needs to
  produce design decisions and technical specifications.
---

# Architect Design

Structured design process: from grill/domain-modeling conclusions to complete `NOTES.md` + `tech-spec.md` + any needed domain documentation updates.

## Vocabulary

Use [design-vocabulary.md](design-vocabulary.md) throughout — module, interface, depth, seam, deletion test, leverage, locality. Do not drift into "component," "service," "API," or "boundary."

## Inputs

- Grill conclusions (assumptions exposed, constraints identified)
- `CONTEXT.md` domain glossary (from `/aiops-setup`)
- `docs/adr/` existing architecture decision records
- `.scratch/<feature>/VERDICT.md` (if prototyper ran)
- `graphify-out/graph.json` (if `/code-graph` has been run — query via `/code-graph query god-nodes`, `/code-graph query communities` for overview)

## Process

### Step 1: Constraint gathering

Extract constraints from all inputs. Classify:

- **Hard constraints**: cannot be violated (existing ADRs, platform limits, team capacity, compliance)
- **Soft constraints**: preferences that can be traded off (performance targets, code style, library preferences)

List constraints explicitly in `NOTES.md` Context section. Reference ADRs by number — do not re-litigate settled decisions unless friction is real enough to warrant revisiting (mark clearly).

### Step 1.5: Graph validation (if code graph available)

If `graphify-out/graph.json` exists, validate constraints against the actual code structure:

1. Query `/code-graph query modules` to get the current module inventory
2. For each constraint referencing existing modules, verify the module exists and matches the constraint's assumptions
3. Query `/code-graph query deps <module>` to check dependency claims
4. Flag any constraint that contradicts the graph (e.g., "Module A doesn't depend on Module B" but the graph shows it does)

Record graph-validated constraints in `NOTES.md` with `[graph-verified]` tags.

### Step 2: Module identification

Identify the modules needed to satisfy the requirements. For each candidate module:

1. **Deletion test**: imagine deleting it. Does complexity vanish (pass-through → merge into caller)? Or does complexity reappear across N callers (earning its keep → keep it)?
2. **Depth assessment**: is the interface small relative to the behaviour it hides? Deep = high leverage for callers. Shallow = interface nearly as complex as implementation → merge or split.
3. **Scope check**: does the module own a coherent slice of the problem, or is it a grab-bag?

Label each module as **new** (greenfield) or **deepening** (refactoring existing shallow modules into one deep one).

### Step 3: Dependency mapping

For each module, map its dependencies and decide the integration strategy:

| Dependency type | Examples | Integration |
|----------------|----------|-------------|
| **In-process** | Pure computation, in-memory state | Merge directly into module, no seam needed |
| **Local-substitutable** | PGlite for Postgres, in-memory FS | Test with stand-in; seam stays internal |
| **Remote but owned** | Internal microservices, internal APIs | Define interface at seam; production transport + in-memory test double |
| **True external** | Stripe, Twilio, third-party | Inject behind interface; mock for tests |

Rule: **don't introduce a seam unless at least two implementations are justified** (typically production + test). A single-implementation seam is just indirection.

### Step 4: Interface design

For each module, design the interface:

- **Minimize entry points**: fewer methods = fewer tests needed = higher leverage per method
- **Simplify parameters**: what can the interface hide from callers?
- **Accept dependencies, don't create them**: inject what the module needs, don't hardcode it
- **Return results over side effects**: prefer pure outputs when possible
- **Document everything a caller must know**: invariants, ordering, error modes, configuration, performance

The interface is the test surface — callers and tests cross the same seam.

### Step 5: Explore alternatives

For the **most critical** module (highest risk, most callers, or deepest impact), design ≥2 radically different interfaces:

- **Design A**: minimize interface — 1–3 entry points, maximum leverage per entry point
- **Design B**: maximize flexibility — support many use cases and extension points
- **Design C** (if applicable): optimize for the most common caller — default case trivial

Compare: which design gives callers the most capability per unit of interface they learn? Where does change concentrate? Where are the seams?

Pick the strongest, or propose a hybrid. Record in `NOTES.md`:
- **Chosen approach**
- **Rationale**: why this one
- **Rejected alternatives**: at least one, with reason for rejection
- **Constraints imposed**: what this decision locks in

### Step 6: Domain documentation pass

Before finalizing the design artifacts, run a short `/domain-modeling` pass:

1. Extract new or changed domain terms from the design.
2. Add only project-specific domain language to `CONTEXT.md`; skip general engineering terms.
3. Check each design decision against the ADR threshold: hard to reverse, surprising without context, and a real trade-off with alternatives.
4. Create `docs/adr/NNNN-slug.md` only for decisions that meet all three criteria; otherwise skip the ADR.
5. Record the outcome in `NOTES.md` so downstream agents know whether domain docs were changed or intentionally left alone.

### Step 7: Specification output

Produce the primary design artifacts:

**`NOTES.md`** — design decisions, trade-off analysis, constraints:
- Problem statement (one sentence)
- Context (existing system, known constraints, relevant ADRs)
- Design decisions (chosen + rejected + rationale + constraints imposed)
- Domain docs (CONTEXT.md updates, ADRs created, ADRs skipped with brief reason)
- Scope (in scope / out of scope)
- Open questions (blocking items must be resolved before planner)

**`tech-spec.md`** — technical specification:
- Architecture (module relationship description)
- Module inventory (each module: interface, depth assessment, dependencies, integration strategy)
- Data model (entities, fields, types)
- API contracts (method + path + request/response for each interface)
- Sequence (step-by-step interaction between modules)
- Risks (risk + impact + mitigation)

## Constraints

- Do not write implementation code (interface signatures and pseudocode only)
- Every design decision must list at least one rejected alternative with reason
- Name modules using `CONTEXT.md` domain terms; if introducing a new term, add it to `CONTEXT.md`
- ADRs stay optional: write one only when the `/domain-modeling` ADR threshold is met
- Existing ADRs are not re-litigated unless friction warrants it (mark explicitly)
- Open questions with blocking items must be flagged — planner cannot start until resolved
- Label each module as **new** or **deepening** existing modules
