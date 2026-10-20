# Strict-Mode Schemas: Required-Everything + No Additional Properties

## Summary

**One-sentence:** Strict-mode structured outputs compile the schema into a finite-state grammar that rejects optional fields and unknown properties.

**One-paragraph:** Produces a Pydantic 2 model (and the JSON Schema it emits) that satisfies the OpenAI Responses / Chat-Completions `strict: true` compiler: every property declared on every object is listed in `required`, every object sets `additionalProperties: false`, and optional semantics are encoded by `T | None = None` (nullable type, still required). Applies identically to Anthropic tool-use input schemas, Azure OpenAI strict mode, and Gemini `responseSchema` with strict enforcement.

**Ефективно для:** будь-якого Pydantic / JSON-Schema коду, що йде в OpenAI Responses API з `response_format={type: "json_schema", strict: true}` або Anthropic tool-use, і ламається з помилкою `400 additionalProperties must be false when strict is true`.

## Applies If (ALL must hold)

- A structured-output call uses strict mode: OpenAI `response_format={type: "json_schema", strict: true}`, Anthropic tool-use, Azure parse API, or Gemini `responseSchema` with strict.
- Schema is generated from Pydantic 2 (or hand-rolled JSON Schema) and owned by the team.
- The team can tolerate the model emitting `null` for fields that are conceptually optional.
- A CI step can be added to assert the emitted schema against `assert_strict_schema()`.

## Skip If (ANY kills it)

- Local Outlines / XGrammar pipelines that support standard JSON-Schema optional fields natively — required-everything wastes tokens for no grammar gain.
- Loose JSON mode (`response_format={type: "json_object"}`) — there is no grammar; strict-mode rules do not apply.
- Schemas intentionally accept arbitrary additional properties (metadata bags) — strict mode is the wrong tool; split into typed sub-object + audit field.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Pydantic model file | `*.py` | `models/`, `schemas/` |
| Schema dump | JSON Schema produced by `Model.model_json_schema()` | one-liner CLI |
| Strict-mode target | `openai` / `anthropic` / `azure` / `gemini` | runtime config |
| Failure log (if any) | `400` body from the provider | provider error response |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/structured-output-mode-picker` | Confirms strict mode is the right pick for this call. |
| `geek/ai/ai-agents/semantic-field-naming` | Rename before adding strict constraints; the two are paired. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules: required-everything, additionalProperties:false, nullable-not-optional, CI assertion, ConfigDict(extra="forbid"), plus the three tree-branch encodings (fm-01 sentinel rewrite, fm-02 non-nullable money + refusal, fm-05 metadata-bag split or drop-strict) | ~1500 |
| `content/02-output-contract.xml` | essential | JSON Schema for the strict-mode audit report: model path, violations, fix patches | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: empty-string sentinel, missing required, missing additionalProperties, nullable int-money, metadata-bag-in-strict | ~700 |
| `content/04-procedure.xml` | medium | Migrate Pydantic to strict: scan → add `extra="forbid"` → convert Optional[X] to `X | None` → assert → ship | ~800 |
| `content/06-decision-tree.xml` | essential | Picks the encoding (nullable / split-bag / drop-strict) per field shape | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scan model for strict-mode violations | sonnet | Mechanical AST walk. |
| Convert legacy Optional[X] → X | None | sonnet | Refactor mechanic. |
| Decide whether a metadata bag should stay or split | opus | Modeling judgement. |
| Generate the `assert_strict_schema` CI test | sonnet | Boilerplate code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/strict_pydantic.py` | Reference Pydantic 2 model with `ConfigDict(extra="forbid")`, nullable fields, and an `assert_strict_schema()` helper that walks the emitted schema. |
| `templates/strict.schema.json` | Equivalent hand-rolled JSON Schema that passes the OpenAI strict-mode compiler. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strict-mode-required-fields.py` | Validates the strict-mode audit report against the `02-output-contract.xml` schema. | After running the audit pass, before opening the migration PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[semantic-field-naming]] — pair rename + strict encoding in the same PR.
- [[structured-output-mode-picker]] — decides whether strict mode is even the right pick.
- [[refusal-field-strict-schema]] — companion rule for refusal handling under strict mode.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the encoding from the field's logical role: hard-required scalar → keep as `T`; sometimes-absent scalar → `T | None = None` (nullable, still required); arbitrary metadata bag → split into typed sub-object + separate audit field; field that can never be present (deprecation) → remove from schema entirely. Use it whenever the question is "how do I express optional under strict mode without violating the FSM-grammar invariant".
