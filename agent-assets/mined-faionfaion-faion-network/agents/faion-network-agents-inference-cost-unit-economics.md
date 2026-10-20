# Inference Cost Unit Economics

## Summary

**One-sentence:** Report quantifying per-feature inference cost (tokens × price + retrieval + tools), gross margin per feature, and the cost-per-successful-outcome — not cost-per-call.

**One-paragraph:** Report quantifying per-feature inference cost (tokens × price + retrieval + tools), gross margin per feature, and the cost-per-successful-outcome — not cost-per-call. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a report produced by an agent applying inference cost unit economics. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible report for inference cost unit economics across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- Every feature in scope emits an observable success event (ticket resolved, suggestion accepted, purchase completed) that can be counted per window.
- Every LLM call is logged with the provider `usage` object, the model id, the feature id, the attempt number and the outcome it served.
- Retrieval (embedding + vector store) and tool/API spend can be attributed to the feature, not only to the account.
- Finance can supply, per feature, attributed revenue, an allocation rule with its key, or a value proxy someone will sign.
- At least 7 days of production traffic exist for the window.

## Skip If (ANY kills it)

- Token counts are estimated from characters or sampled and extrapolated; the report figures would be inadmissible until logging is fixed.
- No feature has a success definition; only calls and sessions are countable, so there is no outcome to divide by.
- Feature is internal tooling with no revenue model or value proxy; track raw cost, do not compute margin.
- Feature is one-shot research with no recurring traffic; an ad-hoc cost report is enough.
- Fewer than 7 days of production traffic; the distribution and the tail cannot be read yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-call usage log: provider `usage` object, model id, feature id, attempt number, outcome id | JSONL or warehouse table from the LLM gateway | platform / ml-engineering |
| Provider price sheet: model id with dated snapshot, input/output/cached price per 1M, sheet date + URL, discount kind and % | table or the pricing page captured on the report date | finance / platform |
| Success definition and outcome count per feature | product spec + the event or table it is counted from | product |
| Retrieval and tool spend per feature (embedding calls, vector queries, external APIs) | vendor invoices joined to feature id | platform |
| Revenue attribution per feature: attributed revenue, allocation rule with key, or value proxy with derivation | finance sheet | product finance |
| Target gross margin per feature and the alerting pipeline the spend alert is wired into | finance target + observability config | product finance / SRE |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ai-feature-observability-four-pillars]] | Observability pillar 4 — cost — feeds this report |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: cost per successful outcome, four-component decomposition, provider usage counts, retry share, pinned price sheet, revenue basis, p95 tail, cost ceiling | 1950 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: pinned price sheet, provider-usage token source, per feature success definition, four cost lines, p50/p95/mean over >=7 days, retry share with the 15% gate, revenue basis, margin, ceiling and spend alert; valid + invalid examples, forbidden patterns | ~3700 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 950 |
| `content/04-procedure.xml` | essential | 8 steps: define success per feature, pin the price sheet, log provider usage, decompose into four cost lines, attribute to outcomes and measure retry share, report the distribution, compute margin on a stated basis, set ceiling and alert then publish | ~2000 |
| `content/05-examples.xml` | recommended | Complete two-feature report (support agent under ceiling, contract summariser over it with a retry loop and a long-context tail) with a note per non-obvious value, plus the bad report and the validator output the reviewer sees | ~2000 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cost_decomposition` | sonnet | Break cost into tokens / retrieval / tool components. |
| `outcome_attribution` | opus | Map calls → successful outcomes (not just calls). |
| `margin_synthesis` | opus | Cost-per-outcome + gross-margin per feature. |

## Templates

| File | Purpose |
|------|---------|
| `templates/unit-economics-report.md.j2` | Report skeleton |
| `templates/unit-economics-report.md` | Report skeleton Generated from `templates/unit-economics-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/cost-decomposition.json` | Cost-decomposition JSON schema |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in unit-economics report |
| `templates/_smoke-test.md` | Minimum viable filled-in unit-economics report Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inference-cost-unit-economics.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-call-site-inventory]]
- [[ai-feature-observability-four-pillars]]
- [[ai-feature-progressive-rollout]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
