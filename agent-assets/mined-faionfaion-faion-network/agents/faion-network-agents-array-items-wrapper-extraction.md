# Array Items Wrapper for Extraction

## Summary

**One-sentence:** Wraps variable-cardinality structured-output extraction in a typed envelope `{items[], total_found, truncated}` so strict-mode validators accept it and zero/one/many cases stay isomorphic.

**One-paragraph:** Strict-mode JSON Schema (OpenAI, Azure) rejects top-level arrays because `additionalProperties` is object-only. Even on lenient providers, a bare list collapses zero / one / many into incompatible shapes (`[]`, `null`, single dict, single-item list). This methodology wraps any extraction with `{items: [...], total_found: int, truncated: bool}` and adds the implementation guidance — JSON Schema, Pydantic model, and a few-shot prompt note that produces the wrapper consistently.

**Ефективно для:** Команд, де model іноді повертає `null`, іноді `[]`, іноді `[ent]`, іноді одиничний dict — і парсер падає на edge-кейсі через 2 тижні; envelope усуває весь клас багів за один schema-rewrite.

## Applies If (ALL must hold)

- Extraction has variable cardinality (entities, citations, line items, search hits).
- Output is consumed by deterministic parser (not free-form prose).
- Strict-mode SO is desired or required.
- Total count and truncation diagnostics are useful downstream.
- Streaming UI is not required (envelope blocks streaming until close).

## Skip If (ANY kills it)

- Hard-coded N (exactly 3 suggestions) — use a fixed-length tuple type.
- Single-entity extraction — wrap is overhead.
- Streaming UI that renders items as they arrive.
- Provider does not support strict-mode AND robust try/except handles legacy shapes.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Entity schema | JSON Schema or Pydantic model | Domain owner |
| Provider + SO mode | string (OpenAI strict, Anthropic tool, etc.) | Eng |
| Expected cardinality range | min, typical, max | Domain owner |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/strict-mode-required-fields/AGENTS.md` | Strict-mode requirements anchor the wrapper rules. |
| `geek/ai/ai-agents/enum-constraints-closed-vocabularies/AGENTS.md` | Related pattern for closed-vocabulary fields. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: top-level object, metadata fields, total_found honest, r1 (shape chosen by cardinality / strict-mode / streaming) | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for the envelope | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: variable-card? → strict-mode? → wrap or stream | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate_envelope_schema` | haiku | Mechanical schema transformation. |
| `verify_against_strict_mode` | sonnet | Per-provider strict-mode rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the envelope. |
| `templates/output.example.json` | Filled example. |
| `templates/items_wrapper.py` | Python (Pydantic) skeleton for the envelope. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate that an output instance matches the envelope. | Per inference call. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[strict-mode-required-fields]] — strict-mode requires this pattern.
- peer: [[enum-constraints-closed-vocabularies]] — combine for fully-typed extraction.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is cardinality variable? (2) is strict-mode required? (3) does a streaming UI need partial items? Leaves point to "wrap", "use streaming top-level", or "fixed-length tuple".
