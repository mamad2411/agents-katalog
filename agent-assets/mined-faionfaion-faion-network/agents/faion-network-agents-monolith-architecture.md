# Monolith Architecture

## Summary

**One-sentence:** Single-deployable architecture (Monolith First): vertical-slice or layered internal layout, ACID transactions, single deploy pipeline; ships when team ≤10 and boundaries unclear.

**One-paragraph:** Single-deployable architecture (Monolith First): vertical-slice or layered internal layout, ACID transactions, single deploy pipeline; ships when team ≤10 and boundaries unclear. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Team < 10 developers OR MVP / startup where speed-to-market dominates.
- Domain boundaries are unclear or evolving; bounded contexts not yet validated.
- Limited DevOps maturity — no Kubernetes / distributed-systems operations capacity.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Team < 10 developers OR MVP / startup where speed-to-market dominates.
- Domain boundaries are unclear or evolving; bounded contexts not yet validated.
- Limited DevOps maturity — no Kubernetes / distributed-systems operations capacity.

## Skip If (ANY kills it)

- Independent per-feature scaling already needed (traffic profiles differ measurably).
- Team is ≥10 with independent release cadences blocking each other — adopt modular-monolith first.
- Different modules need fundamentally different tech stacks (polyglot mandate).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Functional requirements list | doc / spec | PM / team |
| Single deployable target (VM / container) | infra plan | devops |
| Test pyramid (unit / integration / e2e) | test plan | QA / team |
| Single deploy pipeline (build → test → deploy) | CI config | devops |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `internal-layout-design` | sonnet | Pick vertical-slice vs layered + sketch directory layout. |
| `deploy-pipeline-scaffold` | sonnet | Wire build → test → deploy in single pipeline. |
| `scaling-strategy` | haiku | Read traffic profile + apply scale-up / scale-out heuristics. |

## Templates

| File | Purpose |
|------|---------|
| `templates/monolith-layout-vertical.md.j2` | Vertical-slice layout reference (Django/FastAPI-style). |
| `templates/monolith-layout-vertical.md` | Vertical-slice layout reference (Django/FastAPI-style). Generated from `templates/monolith-layout-vertical.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/deploy-pipeline.yaml` | Single deploy pipeline skeleton (GitHub Actions-style). |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-monolith-architecture.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[modular-monolith]]
- [[system-design-process]]
- [[patterns-overview]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (functional list, single deployable, test pyramid, single pipeline)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
