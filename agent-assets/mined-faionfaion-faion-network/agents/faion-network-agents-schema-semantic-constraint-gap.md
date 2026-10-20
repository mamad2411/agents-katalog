# Schema Semantic Constraint Gap

## Summary

**One-sentence:** Produces a Schema Pair Record — a wire schema carrying only the keywords the provider actually compiles, a validation schema carrying the full contract, and a named code-level check plus counter for every semantic constraint the grammar silently drops.

**One-paragraph:** Constrained decoding guarantees SHAPE and nothing else. The provider compiles your JSON Schema into a grammar that masks the token distribution, so `JSON.parse` stops failing — but the grammar has no way to express a numeric range, a string length or a regular expression, so those keywords are stripped from the wire schema and enforced by nobody. On Anthropic (docs read 2026-08-03) `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`, `pattern` and `maxItems` are all unsupported; the official Pydantic and Zod helpers quietly fold them into the field `description` as prose. A single schema file that pretends to be both wire contract and validation contract therefore reports green while shipping out-of-range scores and overlong strings. This methodology splits the file in two, forces one post-validation with a counter per dropped keyword, records the transport divergence (Gemini's OpenAPI subset accepts `pattern` and ranges; Claude does not, so the same request validates differently per transport), and carries the one hard interoperability fork: enabling `citations` on a `document` or `search_result` block together with `output_config.format` returns a 400.

**Ефективно для:**

- Anyone treating a passing schema check as a correctness check — the most common false green in an LLM pipeline.
- Schemas whose only real protections are ranges, lengths and regexes, i.e. most extraction and scoring schemas.
- Multi-transport clients where the same schema is sent to Anthropic, Gemini and an OpenAI-compatible endpoint and is enforced at three different strengths.
- Any design that wants both machine-parseable output and provider-emitted citations, which is a two-call design or a 400.

## Applies If (ALL must hold)

- A JSON Schema is sent to a model as a structured-output or strict-tool contract.
- The schema contains at least one constraint that is not a type, an enum, `required` or `additionalProperties: false`.
- Something downstream consumes the parsed values without re-checking them.

## Skip If (ANY kills it)

- The schema is types and enums only — those ARE compiled, and there is nothing to drop.
- Output is free prose that no code parses; there is no schema to split.
- The consumer already re-validates every field against an independent full-Draft-7 validator and counts the failures — you have the outcome, the record is bookkeeping.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 states the gap; R2-R4 are the split and the enforcement; R5 is the citations fork; R6-R7 are the two ways the wire schema itself bites back. |
| `content/02-output-contract.xml` | The Schema Pair Record: every field, the per-transport unsupported keyword lists, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six production failure modes with symptom, cause and the rule that prevents each. |
| `content/06-decision-tree.xml` | Routing from observable schema and transport properties to split / post-validate / two-call. |
| `scripts/validate-schema-semantic-constraint-gap.py` | Validates a record; walks the wire schema for keywords the declared transport drops and demands a checker plus counter for each. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema-pair-record.yaml` | Fill-in record for a single-transport structured-output call; ships valid against the contract. |
| `templates/schema-pair-record-two-call.yaml` | The citations fork — call 1 structured, call 2 cited, neither doing both. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `structured-output-mode-picker` — picks json mode vs strict SO vs tool call vs grammar; this methodology starts after that choice and asks what the chosen mode does not enforce.
- `two-pass-reason-then-extract` — where the reasoning goes when a format contract is in play; the semantic gap is orthogonal and applies to both passes' outputs.
- `closed-set-output-validation` — the strongest instance of a post-validation: when the field's legal values are an enumerable set you supplied, membership replaces the regex entirely.
- `citation-contract-back-to-source` — the citation side of the 400 fork.
