# Technology Stack Selection Decision Tree

## Summary

**One-sentence:** Picks a backend language + framework + datastore by walking team-expertise, performance-need, ecosystem-fit, and hiring-supply branches; emits a stack ADR with rejected alternatives.

**One-paragraph:** Picks a backend language + framework + datastore by walking team-expertise, performance-need, ecosystem-fit, and hiring-supply branches; emits a stack ADR with rejected alternatives. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Greenfield service / module that owns its own runtime and dependencies.
- Major rewrite where current stack is the binding constraint.
- Adopting a new language / framework for a specific workload (ML, real-time, embedded).
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Greenfield service / module that owns its own runtime and dependencies.
- Major rewrite where current stack is the binding constraint.
- Adopting a new language / framework for a specific workload (ML, real-time, embedded).

## Skip If (ANY kills it)

- Stack mandated by org-wide platform policy — record the constraint and skip.
- Library swap inside an existing service — that is a dependency decision, not a stack decision.
- Throwaway prototype with < 1-month expected lifetime.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team expertise inventory | table (language → headcount → senior years) | team |
| Performance / scaling target | RPS / p95 / GB targets | PM / SRE |
| Hiring market signal | table (language → 6-month hire success) | HR / lead |
| Ecosystem dependencies | list of must-have libraries / SDKs | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trade-off-decision-matrix]] | Stack picks consume the weighted scoring shape. |
| [[decision-tree-process]] | Tech stack decisions are an instance of the six-phase process. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-team-expertise` | haiku | Mechanical headcount + senior-years aggregation. |
| `score-stack-fit` | sonnet | Bounded scoring: workload niche × ecosystem maturity. |
| `draft-stack-adr` | sonnet | Compose the ADR with rejected alternatives + rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tech-stack-adr.md.j2` | ADR skeleton for the chosen language + framework + datastore. |
| `templates/tech-stack-adr.md` | ADR skeleton for the chosen language + framework + datastore. Generated from `templates/tech-stack-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/stack-scoring.json` | Scoring payload for the candidate stacks. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-tree-tech-stack.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[decision-tree-process]]
- [[decision-tree-cloud-provider]]
- [[trade-off-decision-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (expertise, perf, hiring, ecosystem)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
