# Structured Output Mode Picker

## Summary

**One-sentence:** Four constrained-decoding modes ship in 2026 SDKs and they are not interchangeable — pick by use case (extraction / action / DSL / legacy).

**One-paragraph:** Produces a decision-record naming the correct constrained-decoding mode for an agent stage: JSON mode (valid JSON only), Structured Outputs strict (full schema compliance), tool call (schema + function dispatch), or grammar mode (XGrammar / Outlines / GBNF for arbitrary CFGs including SQL, regex, custom DSLs). Maps each mode to its use case: extraction → SO strict; agent action → tool call; custom DSL or local-model output → grammar; legacy fallback → json mode (only when strict SO is unsupported). Wrong mode is the single biggest silent-correctness regression in 2026 structured-output design.

**Ефективно для:** будь-якої нової агентської стадії або міграції legacy `response_format={"type": "json_object"}` коду, де треба знати чи перемикатися на strict SO, tool call або grammar mode.

## Applies If (ALL must hold)

- A new agent stage or pipeline step needs constrained decoding.
- Multiple modes are technically available from the chosen provider.
- The output consumer is one of: extraction (typed parse), action (dispatch to function), DSL (SQL/regex/custom grammar), legacy free-form JSON.
- The team can afford a one-shot eval comparison between candidate modes on ≥10 rows.

## Skip If (ANY kills it)

- Free-form chat where structure is undesirable.
- Pure transformation tasks fully solvable by deterministic code (skip the LLM entirely).
- Chosen provider only supports one mode — pick is forced.
- Free-form ranking / brainstorm where any structure hurts.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case description | one paragraph | product spec |
| Provider list + supported modes | YAML matrix | `provider-modes.yml` |
| Output consumer name | enum | `extraction`/`action`/`dsl`/`legacy` |
| Per-row eval set (≥10 rows) | JSONL | `evals/<stage>/gold.jsonl` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/strict-mode-required-fields` | Strict SO constrains the schema shape; required reading if SO is the pick. |
| `geek/ai/ai-agents/structured-tool-errors` | Tool-call mode requires error envelopes; required if tool call is the pick. |
| `geek/ai/ai-agents/semantic-field-naming` | Field names matter under every mode; pair with the rename pass. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pick-by-consumer, never-json-for-typed, never-SO-for-action, grammar-for-DSL, fallback-only-if-no-strict | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision-record: chosen_mode, alternatives_considered, rationale, eval_delta | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: json-mode-for-typed-extraction, SO-for-dispatch, tool-call-for-DSL, grammar-for-extraction, mode-mismatch-between-providers | ~700 |
| `content/04-procedure.xml` | medium | Step-by-step: identify consumer → list available modes → run shortlisted eval → write decision-record | ~700 |
| `content/06-decision-tree.xml` | essential | Picks the mode from consumer × provider × output shape | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Classify the use case | sonnet | Pattern-matching against four canonical consumers. |
| Run candidate-mode eval | sonnet | Mechanical harness execution. |
| Write the decision-record | opus | Captures product judgement; opus weighs tradeoffs cleanly. |
| Migrate legacy json-mode code | sonnet | Refactor plumbing, deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mode_examples.py` | Four side-by-side minimal calls — one per mode — using openai / anthropic / outlines bindings. |
| `templates/decision-record.md.j2` | Markdown skeleton for the SO-mode decision record (chosen, alternatives, rationale, eval delta). |
| `templates/decision-record.md` | Markdown skeleton for the SO-mode decision record (chosen, alternatives, rationale, eval delta). Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-output-mode-picker.py` | Validates the decision-record JSON against `02-output-contract.xml`. | After authoring the decision-record, before merging the migration PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[strict-mode-required-fields]] — applies when SO strict is the chosen mode.
- [[structured-tool-errors]] — applies when tool-call is the chosen mode.
- [[refusal-field-strict-schema]] — strict SO needs a refusal field.
- [[semantic-field-naming]] — every mode benefits from the rename pass.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the mode from three observables: output consumer (extraction / action / DSL / legacy), provider support (does the provider ship strict SO + tool-call + grammar?), and output shape (JSON / SQL / regex / arbitrary CFG). Use it whenever the choice between modes is contested; the tree is intentionally short because the mapping is mostly mechanical once the consumer is named.
