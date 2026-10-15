---
name: schema-first-prompting
description: >-
  Design Pydantic models and LLM prompt templates for structured extraction
  pipelines. Use when creating, editing, or reviewing Pydantic models that
  serve as LLM output schemas, or when writing prompt templates that pair
  with those models. Trigger: "pydantic model", "structured output",
  "extraction schema", "LLM output model", "schema design".
---

# Schema-First Prompting

Design the Pydantic model first, then write the prompt. The model is the structural contract; the prompt carries only what the schema cannot encode. Be brief, clean, elegant, and internally consistent.

## 1. Don't say the same thing twice

Schema owns shape — names, types, nesting, constraints. Prompt owns intent — tone, audience, rhetorical rules. If the same fact lives in both places, delete the duplicate.

| What | Where |
|---|---|
| Shape, types, limits | Pydantic model (`Field`, validators) |
| Fixed values from variant/slot | Code, after validation |
| Rhetorical / quality rules | Prompt |
| Which schema to use | Caller (conditional model + prompt) |

When the API supports structured output or tool parameters tied to JSON Schema, put structure there. Keep user/system messages to **task, context, and behavior**.

If native structured output is unsupported and you must inject the schema into the prompt, avoid injecting raw JSON Schema (`model_json_schema()`), as it is highly token-inefficient. Instead, use type-definition pseudo-code (TypeScript-style interfaces), which can reduce token usage by up to 60% while being clearer to the model's attention mechanism.

**The prompt should not restate:** field names, types, nesting, required vs optional, defaults, or key enumerations the schema already covers.

**Keep in the prompt:** intent and tone, constraints the schema cannot encode ("no proper nouns from the input", "at most 50 words"), inputs and template variables, conditional blocks via variables — not by asking the model to "ignore" a section.

### No contradictions

If a field says `max_length=5`, the prompt must not say "3–8 items." Pydantic constraints are exact; the model reads prompt numbers as vibes. Contradictions create hidden bugs worse than either version alone.

### Template variables for branches

```python
USER_PROMPT = """You are extracting a plan.

{extra_instructions}

Source text:
{source}
"""
# Caller sets extra_instructions="" or extra_instructions=RISKS_BLOCK when using PlanWithRisks.
```

The model never sees instructions for a branch that is not in the schema.

### Review checklist

When reviewing a prompt/model pair, verify:

- **Names match**: prompt uses the same field and concept names as the schema.
- **Constraints match**: counts, limits, optionality, and branch behavior are identical.
- **Responsibilities match**: prompt asks only for what the schema expects; schema models only what the LLM must produce.

## 2. Put reasoning first

Field order in a schema is not cosmetic. Autoregressive models commit to tokens left to right, so if your schema puts `decision` before `reasoning`, the model fills in an answer before it thinks.

- **Reasoning / chain-of-thought fields first** — before the target data they inform.
- **High-level decisions before details** — `tone` or `strategy` before `body_text`.
- **Independent fields before dependent ones** — if B depends on A, A comes first.

A dedicated reasoning field in a nested model can improve quality for that step. It costs tokens — use it when the task is hard, not on every leaf. Do not duplicate the same instruction in the prompt if the field description already states how to reason.

## 3. Don't ask for what you already know

If a value can be derived from a lookup table, variant, or existing metadata, keep it out of the schema. The LLM should only touch fields that require reading the input and making a judgment.

### Derive fixed values in code

If a value is fixed once you know the variant or slot, derive it with a mapping, `match`, or helper — not by asking the model.

### Use separate models, not optional fields

Do not use `risk_section: RiskAssessment | None` plus prompt prose saying "omit when low-risk." That asks the model to make a structural decision you already know the answer to. Select a different root model **before** the LLM call.

```python
class RiskAssessment(BaseModel):
    summary: str
    severity: Literal["low", "medium", "high"]

class PlanWithRisks(BaseModel):
    outline: OutlineSection
    summary: str = Field(description="Closing summary.")
    risk_section: RiskAssessment

class PlanWithoutRisks(BaseModel):
    outline: OutlineSection
    summary: str = Field(description="Closing summary.")
    # risk_section does not exist on this model at all
```

### What belongs in the schema

| Include | Exclude |
|---|---|
| Text, labels, lists the model must author | Values derived from variant/slot |
| Structure the model must choose | Defaults your code will apply |
| Fields downstream truly consume | "Helper" fields merged in after validation |

## 4. Design for how LLMs work

A schema is an interface to a language model. Design around what the model is good and bad at, not what looks clean in an ORM.

### Separate LLM models from API and DB models

LLM extraction shapes, API request/response types, and persistence rows have different fields and invariants. One "god model" for all layers leaks fields across boundaries. Keep scratchpad and reasoning fields for the LLM that users and databases should never see.

### Ask for decisions, not estimates

LLMs are poor at absolute numeric values — millisecond durations, pixel coordinates, precise word counts. They are much better at categorical decisions: which severity level, which item ranks first, which bin. Reframe numbers as choices wherever possible. If you must ask for a number, keep the range small and well-defined in the field description.

### Match structure to task difficulty

If a task is easy, do not add reasoning fields or scaffolding "just in case." Extra fields cost tokens and can *reduce* quality by forcing justification. If a task is hard (multi-entity extraction, long-range consistency), invest in reasoning fields and break the work into steps. The right amount of structure depends on observed difficulty, not importance.

### Scope the context per step

Dumping an entire manuscript into one call and asking for a complex nested output is a recipe for degraded quality in the tail. Break large pipelines into focused steps, each with its own schema, where the input is scoped to what that step needs. Use prompt caching for shared context (style guides, instructions), but restart the generation context for each step so the model's attention is fresh. This is not just a cost optimization — it directly improves output quality on later fields.

## 5. Start with the tightest schema that works

Begin with the simplest schema that could work. Add reasoning fields, submodels, and constraints only when the output proves they are needed. Complexity should be earned by failure, not anticipated by speculation.

The prompt suggests; the schema enforces.

Bad: "please make sure the list has 3–5 items."
Good: `min_length=3, max_length=5` in the model.

---

## Schema shape

### One model per shape

Each distinct output shape gets its own model. Optional fields that only apply to some shapes are a smell — use a discriminated union or separate models (see [section 3](#3-dont-ask-for-what-you-already-know)).

### Discriminated unions

**Fixed slots** — when the parent model has named fields, the field name tells you the shape. Do not add a `kind` inside each child that repeats what the field name says.

```python
class OutlineSection(BaseModel):
    title: str = Field(description="Section heading.")
    bullets: list[str] = Field(default_factory=list, max_length=8)

class DocumentPlan(BaseModel):
    outline: OutlineSection
    summary: str = Field(description="Closing summary: 2-3 sentences.")
```

**Tagged union** — when a single value must be one of several shapes, you need a discriminator for deserialization:

```python
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

class SearchStep(BaseModel):
    kind: Literal["search"] = "search"
    query: str

class AnswerStep(BaseModel):
    kind: Literal["answer"] = "answer"
    text: str

Step = Annotated[
    Union[SearchStep, AnswerStep],
    Field(discriminator="kind"),
]

class Plan(BaseModel):
    steps: list[Step]
```

`kind` is the wire-format tag the model must emit so the union parses. Do not mirror it as a second field (`action`, `step_type`).

### Avoid single-string wrappers

Every nested model should earn its keep by adding real structure, clearer validation, or a stable reusable concept. A `BaseModel` with one `str` field adds nesting without structure — use a plain field with `Field(description=...)` on the parent. Keep a dedicated model when there are **at least two** meaningful fields, or when you are grouping a stable sub-object at a known serialization boundary that will genuinely grow. "Will grow" means there is a concrete next field on the roadmap — not a hypothetical one.

```python
# Bad — wrapper adds nothing
class ClosingSummary(BaseModel):
    text: str = Field(description="2-3 sentences.")

class Report(BaseModel):
    closing: ClosingSummary

# Good
class Report(BaseModel):
    closing: str = Field(description="Closing summary: 2-3 sentences.")
```

### Base classes

Extract a shared base only when several shared fields justify it. One duplicated field across two models is clearer than a `_Base` with a single line.

## Field design

- **Mutable defaults**: `default_factory=list`, never `[]`.
- **Descriptions**: `Field(description=...)` guides the model; avoid internal jargon. If a field has long or subtle rules, put them in the description so they travel with the schema.
- **Dead fields**: if nothing produces or consumes a field, drop it. Drop "legacy" aliases too.
- **Names**: short, specific, readable in code and JSON Schema. Prefer names that describe the actual concept, not the implementation accident. Avoid vague names like `data`, `info`, `payload`, `value`, `type2`, or `misc`. Avoid ornamental naming: if `BannerCopy` says it, do not name a field `banner_copy_text_value`. Keep siblings parallel — `quote_text` / `quote_source`, not `quoteAttributionLine`. Rename awkward names early; small schema names spread into prompts, validators, logs, tests, and downstream code.
- **Nullable vs empty**: use `str | None = None` when missing differs from empty. Under strict constrained decoding, omitted keys are not allowed — all fields must be marked as required, using nullable types (`["string", "null"]`) for optional values while keeping the key in `required`.
- **Closed sets**: for `Enum` or `Literal`, include an escape hatch (`OTHER`, `UNKNOWN`) when the model must say "none of the above."
- **Bounded extras**: open-ended `dict[str, str]` invites huge blobs. Prefer `list[SmallObject]` (or `(key, value)` tuples) with `max_items` plus a short description of the cap. Note that `max_items` is stripped during strict-mode sanitization for OpenAI, so keep Python-side validation.
- **Entity relationships**: model IDs explicitly (`parent_id`, `friend_ids: list[int]`), not free-text names. Downstream code should not parse prose for links.
- **Known structure**: nested models, `max_length` / `max_items`, enums or `Literal` where the LLM must pick from a closed set. However, some providers' strict modes forbid validation keywords — see strict mode section below.
- **Unknown structure**: `dict[str, Any]`, loose `list[dict[str, Any]]` — use only where the content is genuinely open-ended. A known concept should not be `dict[str, Any]`.

## Strict mode and validation

### Provider-specific strict mode

Not all providers handle JSON Schema validation keywords the same way. Know what your target supports before relying on field-level constraints.

Write your Pydantic models with full validation (`max_length`, `ge`, `le`, `max_items`, etc.). Then apply a provider-specific sanitizer only where required. This gives you one authoritative model with the tightest constraints, and a thin adapter layer per provider.

**OpenAI (`strict=True`):** forbids `maxLength`, `maxItems`, `minimum`, `maximum`, and similar validation keywords in JSON Schema. Sending a model with `Field(ge=0, le=150)` results in an immediate 400 error. `additionalProperties` must be `false`; empty dictionary annotations (`dict[str, Any]`) will cause immediate failure. Implement a schema sanitizer that strips these constraints from the JSON Schema before sending, while keeping the unmodified Pydantic model for Python-side validation.

**Anthropic (tool use):** accepts standard JSON Schema validation keywords including `maxLength`, `minLength`, `pattern`, `minimum`, `maximum`, `minItems`, and `maxItems`. Pydantic models with `Field(ge=0, le=150)` or `Field(max_length=500)` work as-is. However, the model may still occasionally violate soft constraints, so keep Python-side validation as a safety net.

### Sanitizers

LLM completions are untrusted input. Do not assume the model returns clean JSON — raw text may include markdown fences or leading prose. Extract JSON (or use the provider's native structured output) before `model_validate` / `model_validate_json`.

Sanitizers and validators are complementary: pre-parse cleanup vs. post-parse rules.

**Do:** coerce `None` → `""`, list → joined string where needed, strip overlong strings, `pop()` keys that are not on the model (LLM hallucinated extras).

**Don't:** re-implement defaults or `Literal` enforcement the validator already applies; keep dead branches for old shapes.

### Validation feedback loop

When `model_validate()` fails due to hallucinations or missed constraints, do not simply drop the data. Catch the Pydantic `ValidationError` and feed the exact error message (e.g., `"Value error, Name must contain a space"`) back to the LLM in a new user prompt, commanding it to self-correct its previous output. Libraries like Instructor automate this retry loop by catching validation errors and returning them directly to the model alongside the original completion payload.

## Production

Prompts are artifacts, not immortal strings. Separate fixed wording from runtime data. Track changes in source control — when behavior shifts, you need a diff and a rollback story. Keep a small golden set of inputs with expected or acceptable outputs; rerun when the model or prompt changes. Subjective tasks still need criteria: length, must-include fields, forbidden patterns. Log latency, token use, and validation failures per prompt version so regressions surface before users report them.
