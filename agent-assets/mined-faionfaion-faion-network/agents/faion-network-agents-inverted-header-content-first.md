# Inverted Header — Content First, Metadata Last

## Summary

**One-sentence:** Declares the body field BEFORE every metadata field (title, slug, tags, summary) in single-call structured-output schemas so titles condition on the actual body rather than become a blind label the body must rationalise.

**One-paragraph:** When one structured-output call must produce both a long-form body and metadata about that body (title, slug, summary, tags, sentiment), declare the body field FIRST in the schema and every metadata field AFTER it. The autoregressive model can only condition the title on tokens that already exist; if title is generated before body, the body is forced to fit a blind title; if body comes first, the title becomes a faithful summary of what was actually written. AWS Bedrock's 2026 SO design guide states it directly; Castillo's 2025 study measured a 13-percentage-point accuracy gap from field reorder alone.

**Ефективно для:** генерації статей, постів, описів продуктів, коду з підсумками — будь-якого SO-виклику, де метадані описують body.

## Applies If (ALL must hold)

- Single SO call produces both a body and metadata about it.
- Decoder honours field order (Pydantic v2, OpenAI strict, Outlines, XGrammar).
- Quality of the body matters AND quality of the metadata matters.

## Skip If (ANY kills it)

- Title is a hard input from the user — pass in the prompt, not the schema.
- Streaming UI needs the title before the body completes — split into two calls.
- Metadata is fully deterministic from the prompt.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Schema definition | Pydantic BaseModel or JSON Schema | Application code |
| Generation goal | Prompt describing the body to produce | Caller |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `embedded-scratchpad-field` | Same field-order discipline applied to reasoning. |
| `field-descriptions-as-prompts` | Metadata descriptions reference the body by backtick name. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Four testable rules: body-first, no title-first reorder, two-call escape hatch, dependency reference | ~900 |
| `content/02-output-contract.xml` | essential | Pydantic BlogPost schema with body-first ordering | ~800 |
| `content/03-failure-modes.xml` | essential | Title-first, streaming reorder, summary-first | ~700 |
| `content/06-decision-tree.xml` | essential | One-call vs two-call vs title-from-prompt | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Refactor schema to body-first | haiku | Mechanical reorder |
| Author new schema for body+metadata | sonnet | Order + descriptions need judgement |
| Decide one-call vs two-call for streaming UI | opus | Cost vs UI tradeoff |

## Templates

| File | Purpose |
|------|---------|
| `templates/blog_post_schema.py` | Pydantic BlogPost schema with body-first ordering |
| `templates/_smoke-test.json` | Minimum valid BlogPost output for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inverted-header-content-first.py` | Confirms body field appears before metadata fields in a JSON schema dump | Pre-commit on schema changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[embedded-scratchpad-field]]
- [[field-descriptions-as-prompts]]
- [[discriminated-union-output]]

## Decision tree

See `content/06-decision-tree.xml`. The root question is whether the call produces both body and metadata. Branches route to: body-first (one call), two-call (when streaming UI needs title first), or title-from-prompt (when user supplies title).
