# Field Descriptions as Inline Mini-Prompts

## Summary

**One-sentence:** Treats every schema `description=` as an inline micro-prompt that names format, units, edge cases, and forbidden patterns, lifting structured-extraction accuracy 60%+ on PARSE-style benchmarks for ~10 tokens per field.

**One-paragraph:** Treat every `description=` on a schema field as a tiny prompt the model sees right before it generates that field. Be explicit about format, range, units, edge cases, and forbidden patterns. PARSE research (2025) showed that optimising field descriptions yields 60%+ improvement in extraction accuracy. Making relationships explicit in descriptions improves complex-reasoning accuracy by up to 40%.

**Ефективно для:** будь-якої схеми structured output, де поля мають неочевидний формат, одиниці виміру, або де модель колись помилялася на крайових випадках.

## Applies If (ALL must hold)

- A schema has fields with non-trivial semantics (units, formats, edge cases).
- Format-compliance metric matters (downstream parsers depend on exact shape).
- The provider supports schema descriptions (Pydantic, JSON Schema, Anthropic tool input).
- Eval data exists to measure compliance lift.

## Skip If (ANY kills it)

- Description would duplicate enum members verbatim (the enum already constrains decoding).
- Schema is so large that descriptions blow the cold-cache budget; strip only on cache-warm calls.
- Description would contradict the field name — rename the field instead, do not paper over with a description.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Schema definition | Pydantic BaseModel or JSON Schema | Application code |
| Failure-mode log | List of past mis-fillings per field | Eval harness |
| Field inventory | List of fields needing description audit | Schema review |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `embedded-scratchpad-field` | Scratchpad descriptions are the highest-leverage application of this rule. |
| `enum-constraints-closed-vocabularies` | Enum-valued fields use descriptions to disambiguate when to pick each value. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules: always-present, 1-3 sentences, format-units-edge-forbidden, reference-dependencies, no-reasoning-asks | ~900 |
| `content/02-output-contract.xml` | essential | Pattern catalog of good descriptions per field shape | ~900 |
| `content/03-failure-modes.xml` | essential | Empty, duplicate, reasoning-asking, contradictory descriptions | ~700 |
| `content/06-decision-tree.xml` | essential | Routing: when to add, when to omit, when to split into fields | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate descriptions for a schema | haiku | Mechanical mapping per the pattern catalog |
| Audit descriptions for staleness | sonnet | Pattern detection + edge-case reasoning |
| Design descriptions for novel domain | opus | Edge cases unknown without deeper analysis |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-numeric.py` | Numeric field with units, range, rounding rule |
| `templates/pattern-constrained-string.py` | Constrained string with format + example |
| `templates/_smoke-test.json` | Minimum valid extracted record for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-field-descriptions-as-prompts.py` | Audits a schema dump for missing or weak descriptions | Pre-commit on schema changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[embedded-scratchpad-field]]
- [[enum-constraints-closed-vocabularies]]
- [[decimal-as-string-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether the field has non-trivial semantics. Branches then ask whether format/units are obvious, whether edge cases exist, whether the model has mis-filled before. Each leaf gives the description-shape rule that should be applied.
