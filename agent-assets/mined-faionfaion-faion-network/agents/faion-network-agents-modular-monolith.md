# Modular Monolith

## Summary

**One-sentence:** Single-deployable architecture with strict module boundaries: one bounded context per module, schema-per-module, public-API-only calls, import-linter enforced in CI.

**One-paragraph:** Single-deployable architecture with strict module boundaries: one bounded context per module, schema-per-module, public-API-only calls, import-linter enforced in CI. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Team ≤10 with unvalidated domain boundaries and one shared database is acceptable today.
- Refactoring a big-ball-of-mud monolith — boundaries first, extraction later.
- Planning future microservices extraction (modular monolith is the prerequisite step).
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Team ≤10 with unvalidated domain boundaries and one shared database is acceptable today.
- Refactoring a big-ball-of-mud monolith — boundaries first, extraction later.
- Planning future microservices extraction (modular monolith is the prerequisite step).

## Skip If (ANY kills it)

- Modules already need independent scaling (traffic profiles differ ≥10×) — go straight to microservices.
- Polyglot stacks required (different runtimes per module) — single deployable cannot host them.
- Throwaway prototype where module ceremony adds no value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bounded-context list | table (module → context → owner) | team |
| Module dependency graph (target state) | diagram | architect |
| CI configuration | .github/workflows/* or equivalent | devops |
| Import-linter / depguard / ArchUnit installed | config file | devops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[monolith-architecture]] | Modular monolith is a specialization of the monolith style. |

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
| `design-module-graph` | opus | Domain modelling — bounded contexts + their public APIs. |
| `scaffold-modules` | sonnet | Mechanical: create module skeletons + import-linter config. |
| `audit-boundary-violations` | haiku | Grep / linter scan for forbidden cross-module imports. |

## Templates

| File | Purpose |
|------|---------|
| `templates/module-layout.md.j2` | Reference module layout (Python / Go / Java agnostic). |
| `templates/module-layout.md` | Reference module layout (Python / Go / Java agnostic). Generated from `templates/module-layout.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/import-linter.toml` | import-linter contract enforcing module isolation in CI. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-modular-monolith.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[monolith-architecture]]
- [[system-design-process]]
- [[patterns-overview]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (contexts, graph, CI, linter)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
