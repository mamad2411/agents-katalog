# System Design Process

## Summary

**One-sentence:** Five-phase process (Understand → Scope → Design → Validate → Document) turning a product brief into a buildable architecture package: requirements, NFR back-of-envelope, C4 L1+L2, and ADRs.

**One-paragraph:** Five-phase process (Understand → Scope → Design → Validate → Document) turning a product brief into a buildable architecture package: requirements, NFR back-of-envelope, C4 L1+L2, and ADRs. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Greenfield service or major rewrite where the architecture is not yet committed.
- Pre-implementation phase where requirements + NFRs need numeric translation.
- Architecture-review preparation for an external stakeholder or buyer.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Greenfield service or major rewrite where the architecture is not yet committed.
- Pre-implementation phase where requirements + NFRs need numeric translation.
- Architecture-review preparation for an external stakeholder or buyer.

## Skip If (ANY kills it)

- Trivial CRUD module fitting in an existing service.
- Throwaway prototype or spike — design ceremony unjustified.
- Existing architecture package is current and matches the brief.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product brief / one-pager | doc | PM |
| Stakeholder list | table | PM |
| Constraints (timeline, budget, team) | table | team |
| Existing architecture diagrams (if any) | diagram | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[quality-attributes]] | Phase 2 NFRs land here as scenarios. |
| [[decision-tree-process]] | Each ADR follows the decision-tree-process methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `phase1-understand` | sonnet | Question elicitation: scope, stakeholders, success criteria. |
| `phase2-scope-nfrs` | opus | Numeric back-of-envelope; NFR translation. |
| `phase3-design` | opus | C4 L1+L2 + key ADRs. |
| `phase4-validate` | sonnet | Capacity check, anti-pattern scan, peer review. |
| `phase5-document` | haiku | Compose the architecture package. |

## Templates

| File | Purpose |
|------|---------|
| `templates/architecture-package.md.j2` | Package skeleton aggregating phases 1-5. |
| `templates/architecture-package.md` | Package skeleton aggregating phases 1-5. Generated from `templates/architecture-package.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/c4-context.mmd` | C4 L1 (system context) Mermaid skeleton. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-system-design-process.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[quality-attributes]]
- [[decision-tree-process]]
- [[patterns-overview]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (brief, stakeholders, constraints, current diagrams)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
