# Semantic Field Naming

## Summary

**One-sentence:** Field NAMES are part of the prompt — rename generic placeholders into semantically-loaded names and let the model's training-time priors do the work.

**One-paragraph:** Renames generic fields (`val`, `flag`, `output`, `final_choice`) to specific, English, lower_snake_case names that encode unit, direction, cardinality and format (`age_years`, `is_returning_customer`, `confidence_0_to_1`, `body_markdown`). Structured-output bridges turn the schema into part of the conditioning prompt, so a single rename can swing accuracy by tens of points (Instructor 2024-09: `final_choice` → `answer` lifted a benchmark from 4.5% to 95%). The methodology produces a side-by-side rename rubric per field plus a Pydantic migration diff.

**Ефективно для:** будь-якої Pydantic-моделі або JSON Schema, що йде в structured-output виклик і має поля з безіменними cryptic-назвами (`val`, `flag`, `output`, `data`, `result`).

## Applies If (ALL must hold)

- A structured-output call (`response_format=json_schema`, Anthropic tool-use, Instructor, pydantic-ai) is used in production.
- At least one field name is generic (`val`, `flag`, `output`, `result`, `data`, `field1`, single-letter).
- The schema is owned by the team (no external API contract pinning the names).
- The team can afford a one-shot A/B regression test on ≥5 evaluation rows.
- English is acceptable for field names (LLMs have the strongest priors on English snake_case).

## Skip If (ANY kills it)

- Field names are pinned by an external API contract you cannot change (use `validation_alias` + new internal model instead, see [[strict-mode-required-fields]]).
- The schema is purely internal storage (no LLM ever sees the JSON Schema or field names).
- Localised schemas where field names must be in a non-English language for regulatory reasons.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Pydantic model file(s) | `*.py` | repo source tree (`models/`, `schemas/`) |
| Current eval baseline | JSONL of `{input, expected}` rows | `evals/<feature>/gold.jsonl` |
| Schema dump | JSON Schema produced by `Model.model_json_schema()` | `python -c "import json; from m import M; print(json.dumps(M.model_json_schema()))"` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/strict-mode-required-fields` | Strict-mode constraint applies before renaming — keeps schema submittable. |
| `geek/ai/ai-agents/field-descriptions-as-prompts` | Field descriptions complement names; do not duplicate the rename signal. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules: specific names, units in name, bool direction, enum semantics, English-only, ≥2 tokens, no `_value`/`_data` suffixes, non-English token translation with `validation_alias` (fm-03-mixed-language) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the rename rubric output: per-field `old`, `new`, `reason`, `category` | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: redundant suffixes, generic alphabet fields, mixed language, single-letter, plural mismatch, empty-string sentinel | ~700 |
| `content/05-examples.xml` | essential | Worked examples: Instructor 90-point swing, currency confusion, boolean direction, neromedia pipeline, enum semantics | ~800 |
| `content/06-decision-tree.xml` | essential | Picks the rename target based on type + role (numeric → unit suffix, bool → is_/has_, enum → semantic literals) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Audit existing schema for generic names | sonnet | Mechanical regex-like scan, deterministic output. |
| Propose semantically loaded replacements | opus | Naming carries product judgement; opus picks priors with higher recall. |
| Apply renames + Pydantic migration | sonnet | Diff plumbing, deterministic. |
| A/B accuracy regression check | sonnet | Runs eval harness, summarises delta. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rename-rubric.md.j2` | Side-by-side template: `old_name → new_name`, reason, evidence row(s). |
| `templates/rename-rubric.md` | Side-by-side template: `old_name → new_name`, reason, evidence row(s). Generated from `templates/rename-rubric.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pydantic-rename.py` | Skeleton Pydantic model showing legacy `validation_alias` pattern for safe migration. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-semantic-field-naming.py` | Validates the rename rubric output against the `02-output-contract.xml` schema. | After the rename pass, before opening the migration PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[strict-mode-required-fields]] — pairs with rename: rename + nullable encoding go together.
- [[structured-output-mode-picker]] — renames matter most under strict / FSM-grammar modes.
- [[stream-json-orchestration]] — orchestrator code observes the renamed fields downstream.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the rename target from the field's type and role: numeric → suffix the unit (`age_years`, `monthly_spend_usd`); boolean → prefix the direction (`is_paid`, `has_promo_code`); enum-mapped string → semantic literal vocabulary (`approve|reject`, `low|medium|high|critical`); string with format constraint → encode format in the name (`body_markdown`, `slug_kebab`, `iso_published_date`). Use it whenever the question is "what new name encodes the strongest prior", not "should I rename at all".
