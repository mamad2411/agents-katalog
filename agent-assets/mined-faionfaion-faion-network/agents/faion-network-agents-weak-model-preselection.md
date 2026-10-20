# Weak-Model Preselection

## Summary

**One-sentence:** Run a cheap fast model to filter / classify / extract refs, then pass only the filtered slice to the expensive strong model.

**One-paragraph:** Strong models cost 5-30x per token. The expensive part of a hard task is reasoning over the right context, not finding the right context. A small model is usually plenty for tag / classify / rank / extract-refs tasks and can run on the full corpus to produce a 100x shorter input for the big model. This methodology codifies four cascade variants (filter-then-reason, reference-extract-then-load, classify-then-route, rank-then-rerank), the cost-savings audit format, and the safety rule that a weak filter never serves as sole gatekeeper for high-stakes decisions (medical / legal / security — use it as ranker only).

**Ефективно для:**

- RSS / news / log pipelines: cheap-model filter перед Opus reasoning — економія 60-90%.
- Long-doc QA: weak model extracts relevant passages → strong model reasons лише над виборкою.
- Multi-route applications: weak classifier → routes to a specialized strong-model prompt.
- Будь-який pipeline, де &gt; 70% input — це noise, який strong model не повинен бачити.

## Applies If (ALL must hold)

- Input is long (&gt; 5K tokens) with high noise ratio (relevant content &lt; 30%).
- A cheap model exists for the filter task (classification / extraction / ranking).
- The strong-model step is the dominant cost in the pipeline.

## Skip If (ANY kills it)

- Short inputs (&lt; 1K tokens) — routing overhead exceeds savings.
- High-stakes gates (medical / legal / security) where weak-model false negative is catastrophic.
- Tasks requiring full-context emergent insight (long-context literary analysis).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Weak-model client | Haiku / GPT-4.1-nano / open-source | your provider |
| Strong-model client | Opus / GPT-4.5 / Gemini Ultra | your provider |
| Filter eval set | input + ground-truth keep_flag list | labeled fixture set |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: weak-filter-strong-reasoner, never-sole-gatekeeper-high-stakes, filter-eval-required, cost-savings-audit, escape-hatch-required | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit_noise_ratio` | haiku | Token counting + simple relevance heuristic. |
| `label_and_eval` | haiku | Mechanical eval; ground-truth pre-supplied. |
| `tune_threshold` | sonnet | Light judgment to balance recall/precision. |
| `measure_savings` | haiku | Cost arithmetic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-savings-report.md.j2` | Markdown skeleton for the cost-savings audit report |
| `templates/cost-savings-report.md` | Markdown skeleton for the cost-savings audit report Generated from `templates/cost-savings-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weak-model-preselection.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[two-pass-reason-then-extract]]
- [[trajectory-eval-otel]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
