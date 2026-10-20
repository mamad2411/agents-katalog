# Terse Default Tool Output, Verbosity Opt-In

## Summary

**One-sentence:** Tools default to compact summary output (one-line per hit + id + truncated flag) and accept a `format=full` opt-in with mandatory `reason`, validated by a CI envelope schema.

**One-paragraph:** Verbose-by-default tool outputs are the most common cause of context blowup in long agent loops — they bury the signal the model uses for the next step. SkillReducer (arXiv:2603.29919) reported a 2.8% absolute task-quality LIFT after compressing tool bodies ~40%. This methodology forces every list/search/query tool whose p95 output exceeds 500 tokens to default to a compact Markdown table including the primary key, expose a `format: Literal["summary","full"]` knob, always return `truncated` + `total_hits`, and require a `reason` argument when `format="full"` so raw-mode usage stays auditable.

**Ефективно для:**

- Довгі агент-loop'и: search_logs / list_files / query_db, де summary economiт по 3-5K токенів на виклик.
- MCP-агрегатори з 20+ tool'ів — без summary mode кожен виклик заливає контекст і модель плутає інструменти.
- Команди, які бачуть, що Claude/GPT агенти passують `format="full"` за замовчуванням — `reason`-аргумент зупиняє creep.
- CI-кріплення tool-контрактів: будь-який response без `truncated`+`total_hits` падає на валідаторі ще до deploy.

## Applies If (ALL must hold)

- Tool's measured p95 response token-count exceeds ~500 tokens at intended usage.
- Tool is invoked inside a multi-step agent loop where context budget is finite.
- Tool's output is used by the model to plan a next action (only IDs + a hint matter at that step).

## Skip If (ANY kills it)

- Tool's every field is load-bearing for the agent (e.g. `get_payment_invoice` for an audit task).
- Tool returns small, fixed-shape responses (`get_user(id)` returning 5 fields).
- Final-result tool at the end of the loop where the user wants the full answer rendered.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool source code | Python / TypeScript / Go | repo path |
| Sample queries | list of 20 representative inputs | recorded agent traces or query logs |
| Backend client w/ count API | function returning total-hits estimate | tool's data source (ES, DB, FS) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This is a foundational tool-design rule; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Background (why verbose output poisons the loop) + 5 testable rules: terse-default-required, primary-key-in-summary, explicit-truncation-flag, tokens-budget-doc, full-mode-justification; source links | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for tool-response envelope + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: summary-without-id, silent-truncation, format-full-default-creep | 650 |
| `content/04-procedure.xml` | essential | 4-step retrofit procedure measure → design → implement → wire-eval | 700 |
| `content/05-examples.xml` | recommended | search_logs retrofit: summary default with `format` opt-in vs full rows every call (python) | 350 |
| `content/06-decision-tree.xml` | essential | Branches on p95-tokens + tool-role + primary-key-availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `measure_worst_case` | haiku | Token-counting + percentile math; deterministic. |
| `design_summary_shape` | sonnet | Choosing minimum useful columns needs light judgment. |
| `implement_format_knob` | haiku | Filling a known template against the schema. |
| `wire_eval_gate` | sonnet | Picking thresholds + tying to existing dashboards. |

## Templates

| File | Purpose |
|------|---------|
| `templates/search_tool.py` | Reference Python tool with `format: Literal["summary","full"]`, primary-key in summary, `reason` requirement on full, `truncated` + `total_hits` always returned. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terse-default-tool-output.py` | Validate a tool response JSON against the envelope schema | CI on each tool deploy + on captured agent traces |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tool-description-as-prompt]] — tool description must declare the format modes and their token bands.
- [[verb-object-tool-naming]] — naming + namespace pair with this methodology's output shape.

## Decision tree

See `content/06-decision-tree.xml`. The tree first asks whether the tool's measured p95 response exceeds 500 tokens (skip if not), then whether the tool is a final-result or intermediate planning tool (final-result keeps full-by-default), then whether each row has a stable primary key (introduce one before applying summary mode if not). Each leaf references a rule from `01-core-rules.xml`.
