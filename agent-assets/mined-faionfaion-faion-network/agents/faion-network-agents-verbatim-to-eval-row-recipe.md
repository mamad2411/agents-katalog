# Verbatim To Eval Row Recipe

## Summary

**One-sentence:** Produces a recipe for converting a customer-zero feedback verbatim (chat message, support ticket, voice transcript) into a deduplicated, labelled eval row that lands in the regression set within one day.

**Ефективно для:** RAG / agent owners closing the customer-zero feedback loop fast; QA leads building a regression set from real failures; PMs measuring eval-row growth as a velocity metric.

**One-paragraph:** This methodology pins the recurring decision around "verbatim-to-eval-row-recipe" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Team runs an LLM-agent surface with live users.
- User feedback exists in a structured channel (Intercom / Zendesk / Slack-bot).
- Regression eval-set exists OR can be created.
- Owner exists for the eval-set.

## Skip If (ANY kills it)

- No customer feedback channel — bootstrap that first.
- Eval set is fully synthetic and frozen by design (e.g., regulator-supplied).
- Team is pre-PMF with <20 active users.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Feedback verbatim | text + metadata | support / chat |
| Existing eval-set manifest | JSONL | eval owner |
| Dedup index | vector index OR hash table | eval owner |
| Labeller | handle / email | team roster |
| Severity taxonomy | Markdown | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[eval-set-stratified-sampling-recipe]]` | downstream eval set keeps stratification balanced |

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
| `draft_eval_row` | haiku | Template fill from verbatim. |
| `synthesize_label` | sonnet | Per-row label + severity classification. |
| `escalate_ambiguity` | opus | Cross-row when same verbatim spans multiple eval rows. |

## Templates

| File | Purpose |
|------|---------|
| `templates/verbatim-to-eval-row-recipe.json` | JSON Schema for the Verbatim To Eval Row Recipe output contract |
| `templates/verbatim-to-eval-row-recipe.md.j2` | Markdown skeleton with the required fields |
| `templates/verbatim-to-eval-row-recipe.md` | Markdown skeleton with the required fields Generated from `templates/verbatim-to-eval-row-recipe.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-verbatim-to-eval-row-recipe.py` | Enforce the Verbatim To Eval Row Recipe output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[eval-set-stratified-sampling-recipe]] — adjacent eval-set design.
- [[weekly-rag-spotcheck-protocol]] — periodic eval consumer.
- [[agent-eval-harness-bootstrap-recipe]] — harness consuming these rows.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
