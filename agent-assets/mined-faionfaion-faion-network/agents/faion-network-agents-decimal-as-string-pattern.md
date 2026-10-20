# Decimal as Pattern-Constrained String

## Summary

**One-sentence:** Declares money, exact decimals, big integers, and structured identifiers as regex-patterned strings instead of JSON numbers, so strict-mode decoders mask invalid digit sequences at sampling time and the consumer parses to Decimal/int/datetime losslessly.

**One-paragraph:** For money, prices, exact decimals, large IDs, phone numbers, and any value where lossy float conversion would corrupt data, declare the schema field as `str` with a regex `pattern`, not `float` or `number`. The receiving side parses with `Decimal()` (or the language equivalent) only after the model has produced a known-good token sequence. The pattern constraint is enforced at sampling time on strict-mode and grammar-backed decoders, so the model cannot emit `19.999` when the schema demands two decimal places.

**Ефективно для:** будь-яких полів вартості, ідентифікаторів та форматованих стрічок, де точність текстового представлення критична для downstream-обробки.

## Applies If (ALL must hold)

- Currency (USD, EUR, BTC, etc.) is being captured.
- Exact decimals appear in finance, science, or engineering reports.
- Big integers larger than 2^53 must be carried (JSON number cannot hold them safely).
- Account numbers, credit cards, phone numbers, postal codes, ISBNs are in scope.
- Version strings (semver) or strict ISO-8601 timestamps are required.

## Skip If (ANY kills it)

- Counts, ranks, indices, scores — `int` is fine and saves tokens.
- Floating-point measurements where a few ULPs of drift do not matter (sensor noise, ML scores).
- Free-form numerics where the format is genuinely unknown — pattern-less string is safer than a wrong pattern.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Schema definition | Pydantic BaseModel or JSON Schema | Application code |
| Decoder mode | "strict" / grammar-backed / JSON-mode | Provider config (OpenAI strict, Anthropic tool input_schema, Outlines, XGrammar) |
| Field inventory | List of fields with their canonical surface form | Domain analyst |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `enum-constraints-closed-vocabularies` | Same sampling-time-mask principle, complementary tool for finite-value fields. |
| `field-descriptions-as-prompts` | Pair every pattern with a `description=` naming the format and giving an example. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Three testable rules: declare-as-string-with-pattern, pick-strictest-pattern, pair-with-description | ~800 |
| `content/02-output-contract.xml` | essential | Pattern catalog + good/bad examples | ~900 |
| `content/03-failure-modes.xml` | essential | Float drift, wide-open patterns, pattern-name mismatch | ~700 |
| `content/06-decision-tree.xml` | essential | Field-by-field routing: int vs pattern-str vs free-str | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate patterns for a field inventory | haiku | Mechanical lookup from the catalog |
| Audit an existing schema for pattern coverage | sonnet | Pattern recognition + edge cases |
| Design patterns for novel domain (custom IDs) | opus | Domain-specific edge cases require deeper analysis |

## Templates

| File | Purpose |
|------|---------|
| `templates/decimal_schema.py` | Pydantic invoice model with regex-patterned price and big-int ID fields |
| `templates/_smoke-test.json` | Minimum valid invoice JSON for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decimal-as-string-pattern.py` | Validates a JSON file against the price/ID patterns from the catalog | Pre-commit on any schema change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[enum-constraints-closed-vocabularies]]
- [[field-descriptions-as-prompts]]
- [[discriminated-union-output]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether the field's exact textual form matters downstream. The tree branches to `int` (counts/ranks), `float` (lossy-tolerant measurements), `str + pattern` (money/IDs/timestamps), or `str` without pattern (genuinely free-form text). Each leaf maps to a rule in `01-core-rules.xml`.
