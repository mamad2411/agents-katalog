# Serverless Cost Optimization

## Summary

**One-sentence:** Cost-reduction report for a serverless workload: memory right-sizing, batching, downstream call reduction, idle-PC removal; ships before/after spend + break-even RPS vs containers.

**One-paragraph:** Cost-reduction report for a serverless workload: memory right-sizing, batching, downstream call reduction, idle-PC removal; ships before/after spend + break-even RPS vs containers. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Lambda / Functions monthly bill > $500 OR > 30% of total cloud spend.
- Workload showing under-utilisation (PC > 50% idle, memory > 2× p95 used).
- FinOps mandate to reduce cloud cost or improve unit economics.
- Output produces `report` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Lambda / Functions monthly bill > $500 OR > 30% of total cloud spend.
- Workload showing under-utilisation (PC > 50% idle, memory > 2× p95 used).
- FinOps mandate to reduce cloud cost or improve unit economics.

## Skip If (ANY kills it)

- Workload spend < $100/month — optimisation overhead exceeds savings.
- Architecture migration to containers already planned — focus there.
- SLO already at risk; perf-first work has priority.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Monthly Lambda / Functions cost broken down by function | billing data | FinOps |
| Function-level metrics (memory used p95, duration p95, RPS) | metrics data | SRE |
| Downstream service cost (DynamoDB, SQS, S3 PUT) | billing data | FinOps |
| Provisioned concurrency config + utilisation | data | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[serverless-foundations]] | Foundational FaaS understanding. |
| [[serverless-cold-start-optimization]] | Cost mitigations may interact with cold-start tuning. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-spend` | haiku | Aggregate per-function cost + memory + duration. |
| `right-size` | sonnet | Bounded recommendation per function. |
| `batch-and-reduce-downstream` | sonnet | Identify request batching + downstream call reduction opportunities. |
| `publish-report` | sonnet | Compose cost report with before/after. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-report.md.j2` | Report skeleton: per-function before/after + actions + savings. |
| `templates/cost-report.md` | Report skeleton: per-function before/after + actions + savings. Generated from `templates/cost-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/memory-tuning.json` | AWS Lambda Power Tuning input/output sample. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-serverless-cost-optimization.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[serverless-foundations]]
- [[serverless-cold-start-optimization]]
- [[serverless-architecture-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (billing, metrics, downstream cost, PC data)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
