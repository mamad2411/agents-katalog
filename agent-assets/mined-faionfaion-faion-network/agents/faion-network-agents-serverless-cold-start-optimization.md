# Serverless Cold Start Optimization

## Summary

**One-sentence:** Cold-start mitigation spec for FaaS: runtime + memory + bundle-size + provisioned concurrency / SnapStart choice, with measured before/after p99 numbers.

**One-paragraph:** Cold-start mitigation spec for FaaS: runtime + memory + bundle-size + provisioned concurrency / SnapStart choice, with measured before/after p99 numbers. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Function on a sync request path with p99 latency budget < 1s.
- Cold-start frequency observable in production (idle > N minutes).
- Latency SLO miss attributed to cold starts in incident analysis.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Function on a sync request path with p99 latency budget < 1s.
- Cold-start frequency observable in production (idle > N minutes).
- Latency SLO miss attributed to cold starts in incident analysis.

## Skip If (ANY kills it)

- Async event consumer with no user-facing latency budget.
- Workload is steady high-RPS where cold starts are negligible.
- Function already meets SLO with healthy headroom.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Latency budget (p50/p95/p99) | table | SRE |
| Baseline cold/warm latency measurement | data | QA / SRE |
| Runtime + memory config | deployment yaml | ops |
| Bundle size + import graph | data | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[serverless-foundations]] | Foundational FaaS understanding. |
| [[serverless-architecture-patterns]] | Cold-start may flip the pattern choice. |

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
| `measure-baseline` | haiku | Aggregate CloudWatch / Stackdriver cold vs warm latency. |
| `pick-mitigation` | sonnet | Bounded judgement: runtime swap vs PC vs SnapStart vs container. |
| `update-deployment` | haiku | Mechanical: edit IaC config + redeploy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cold-start-spec.md.j2` | Spec capturing baseline + chosen mitigation + post-fix numbers. |
| `templates/cold-start-spec.md` | Spec capturing baseline + chosen mitigation + post-fix numbers. Generated from `templates/cold-start-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/lambda-config.yaml` | Sample Lambda config with provisioned concurrency + SnapStart settings. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-serverless-cold-start-optimization.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[serverless-foundations]]
- [[serverless-architecture-patterns]]
- [[serverless-cost-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (budget, baseline, runtime, bundle)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
