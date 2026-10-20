# Weekly RAG Spotcheck Protocol

## Summary

**One-sentence:** Produces a weekly checklist + report for RAG retrieval quality: 20-row sample, judge-score deltas, top regressions, action items routed to indexer / embedder / prompt owners.

**Ефективно для:** RAG owners running a weekly retrieval-quality cadence; PMs tracking recall regression as a leading indicator of churn; SREs gating index refresh on stable retrieval health.

**One-paragraph:** This methodology pins the recurring decision around "weekly-rag-spotcheck-protocol" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- RAG surface in production with ≥1k retrievals per week.
- Eval / judge harness exists OR can be set up.
- Owner exists for retrieval quality.
- Cadence is weekly or being introduced.

## Skip If (ANY kills it)

- RAG traffic <100 retrievals/week — sample size is unreliable.
- Surface has no eval / judge harness AND no plan to add one.
- Static FAQ surface with no embedding drift.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Last week's retrieval logs | JSONL | RAG telemetry |
| Stratified 20-row sample | JSONL | spotcheck owner |
| Judge scoring rubric | Markdown | eval owner |
| Previous week's report | Markdown | spotcheck owner |
| Owner for the protocol | handle / email | team roster |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-eval-harness-bootstrap-recipe]]` | judge harness exists and is stable |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_sample` | haiku | Mechanical sample from stratified pool. |
| `synthesize_regression` | sonnet | Per-row regression assessment. |
| `escalate_blocker` | opus | Cross-row pattern when multiple surfaces regress. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-rag-spotcheck-protocol.json` | JSON Schema for the Weekly RAG Spotcheck Protocol output contract |
| `templates/weekly-rag-spotcheck-protocol.md.j2` | Markdown skeleton with the required fields |
| `templates/weekly-rag-spotcheck-protocol.md` | Markdown skeleton with the required fields Generated from `templates/weekly-rag-spotcheck-protocol.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-rag-spotcheck-protocol.py` | Enforce the Weekly RAG Spotcheck Protocol output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[vector-db-tuning-runbook]] — adjacent when recall drops.
- [[verbatim-to-eval-row-recipe]] — feeds new rows into the spotcheck pool.
- [[agent-eval-harness-bootstrap-recipe]] — upstream harness setup.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
