# Cloud Provider Selection Decision Tree

## Summary

**One-sentence:** Routes a workload to AWS, Azure, GCP, or none-of-the-above by walking existing-investment, workload-type, and budget-sensitivity branches; emits a provider+runner-up ADR.

**One-paragraph:** Routes a workload to AWS, Azure, GCP, or none-of-the-above by walking existing-investment, workload-type, and budget-sensitivity branches; emits a provider+runner-up ADR. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Greenfield project with no existing cloud footprint and a buyer ready to commit to one hyperscaler.
- Adding a secondary provider for a single workload (e.g. GCP for ML on top of an AWS estate).
- Compliance-gated decision that needs a structured audit of certifications and data residency.
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Greenfield project with no existing cloud footprint and a buyer ready to commit to one hyperscaler.
- Adding a secondary provider for a single workload (e.g. GCP for ML on top of an AWS estate).
- Compliance-gated decision that needs a structured audit of certifications and data residency.

## Skip If (ANY kills it)

- Contractual or organisational mandate already pins the provider — record it and skip the tree.
- Deployment is cloud-agnostic (Kubernetes on Hetzner / bare metal) — the tree assumes hyperscaler.
- You are picking a single service (e.g. managed Postgres) — that is a service comparison, not a provider decision.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing identity / productivity stack | table (AD / Workspace / none) | ops |
| Workload profile | doc listing dominant workloads + RPS / GB / GPU needs | team |
| Compliance matrix | table of required certifications + data-residency regions | legal |
| Cost envelope | monthly budget + 12-month projection | finance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trade-off-decision-matrix]] | Cloud choice consumes the weighted-matrix scoring shape. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-investment-axis` | haiku | Mechanical: check stack for AD / Workspace / neutral markers. |
| `score-provider-fit` | sonnet | Bounded judgement: workload-type → provider strengths. |
| `draft-adr` | sonnet | Compose the decision record with rationale + runner-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cloud-provider-adr.md.j2` | MADR-style ADR skeleton recording the chosen provider, runner-up, and elimination rationale. |
| `templates/cloud-provider-adr.md` | MADR-style ADR skeleton recording the chosen provider, runner-up, and elimination rationale. Generated from `templates/cloud-provider-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/provider-comparison.json` | Provider scoring matrix consumed by the decision script. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-tree-cloud-provider.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[decision-tree-tech-stack]]
- [[decision-tree-process]]
- [[trade-off-decision-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (investment stack, workload profile, compliance matrix, cost envelope)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
