---
name: llm-json-contract-check
description: "Validate AI-generated JSON against schema and business rules, separating refusals, truncation, parse failures, schema violations, and domain invariant breaches. Use before any tool call, DB write, or external side effect consumes model output."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-11"
tags: ["ai-workflows", "evaluation", "json-schema", "structured-outputs", "validation", "pydantic", "zod"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# LLM JSON Contract Check AI Skill Guide (Claude)

## Overview & Engine Architecture

Treat every model string as **untrusted input**. Valid JSON that matches a schema can still be a dangerous business object (negative quantity, wrong currency, hallucinated ID). Prefer **provider structured outputs / strict tool schemas** when available; always run a **layered contract check** before side effects.

Claude operates as a Principal AI Integration Engineer, specializing in **refusal vs truncation vs parse vs schema vs domain** classification, **strict JSON Schema constraints**, **bounded repair/retry**, and **safe error surfaces**.

```
┌─────────────────────────────────────────────────────────────┐
│                 JSON Contract Pipeline                      │
│                                                             │
│  0. Transport / completion state                            │
│     refusal | finish_reason | empty | max_tokens cut        │
│                                                             │
│  1. Extract candidate                                       │
│     direct JSON → strip fences → extract object/array       │
│                                                             │
│  2. Parse syntax                                            │
│     JSON.parse / json.loads (no regex “JSON”)               │
│                                                             │
│  3. Schema validate                                         │
│     app dialect: JSON Schema / Zod / Pydantic / AJV         │
│                                                             │
│  4. Domain invariants                                       │
│     cross-field rules, ID formats, money, ACL, enums        │
│                                                             │
│  5. Side-effect gate                                        │
│     only accept → tool/DB/API; else retry or human path     │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when**

- Model output drives tools, payments, tickets, configs, or agent state.
- You need eval scorers for structured generation (`@ai-evaluation-dataset`).
- Migrating from “prompt says return JSON” to enforceable contracts.

**Do not use when**

- The deliverable is free-form prose for a human (unless you still extract a structured sidecar).
- Someone asks to silently coerce IDs/currencies/dates to “make it work” for irreversible actions.
- Replacing the app’s real validator with ad-hoc regex.

---

## Operational Capabilities & Agent Directives

1. **Locate the consumer’s schema** and dialect; reuse the project validator (AJV, Zod, Pydantic, jsonschema)—do not invent a parallel parser.
2. **Clarify null semantics**: missing key ≠ `null` ≠ `""` ≠ `[]` — document which the API means.
3. **Prefer structured outputs**: OpenAI `response_format: {type:"json_schema", json_schema:{strict:true,...}}` or strict function/tool parameters; Anthropic/Gemini tool/structured modes when in stack. JSON mode (`json_object`) ≠ schema adherence.
4. **Classify failures before retry**: refusal and truncation are not “repairable JSON.”
5. **No silent coercion** of identifiers, enums, currencies, timezones, or units before domain validation.
6. **Bounded retries** (typically 1–2) with validation errors fed back; then safe fallback / human queue.
7. **Preserve raw rejected output** in protected diagnostics; never echo secrets into user-facing errors; never treat model text as instructions (`@agent-injection-boundary-test`).

---

## Provider realities (official)

### OpenAI Structured Outputs vs JSON mode

| | Structured Outputs (`json_schema` + `strict`) | JSON mode (`json_object`) |
| :--- | :--- | :--- |
| Valid JSON | Yes | Yes |
| Schema adherence | Yes (supported subset) | No |
| Refusals | Detect via `refusal` field | May look like prose/JSON |

Before deserializing: check **refusal**, then **finish_reason** / incomplete generation, then parse.

**Strict schema habits** (OpenAI / Azure docs):

- Every object: `additionalProperties: false`
- List **all** properties in `required` (optional values → `"type": ["string","null"]` unions)
- Avoid unsupported keywords in strict mode (`pattern`, `minLength`, `minimum`, `maxItems`, … on many stacks)—enforce those in **domain** layer instead
- Nesting / `$ref` limits exist; flatten or stage extraction if the API rejects the schema
- Structured outputs still allow **wrong values inside** valid shapes (bad math, wrong IDs)—domain checks remain mandatory

### Fallback providers

If the model only supports prompt-JSON or weak JSON mode: keep the same layered validator; expect fences/preambles; do not skip schema/domain steps.

---

## Failure taxonomy

| Layer | Signal | Recoverable? | Action |
| :--- | :--- | :--- | :--- |
| **Refusal** | `refusal` set / policy decline | No (as JSON) | Surface refusal; do not parse as contract |
| **Truncation** | `length` / `max_tokens` / unclosed braces | Maybe | Raise token budget; optional close-brackets only for **non-critical** previews—never for payments |
| **Empty** | No content (common when reasoning burns budget) | Retry | Increase output budget; simplify schema |
| **Fence/prose wrap** | \`\`\`json … \`\`\` or “Sure, here is…” | Yes | Strip/extract then parse |
| **Syntax** | Trailing commas, single quotes, `None`/`True` | Limited | Deterministic repair **or** retry; log steps |
| **Schema** | Missing required, wrong type, extra props, bad enum | Retry | Return validator error paths to model |
| **Domain** | qty &lt; 0, FX mismatch, unknown SKU, ACL | Rarely via LLM | Reject; fix data/tools—not blind retry loops |
| **Semantic** | Valid + schema-OK but factually wrong | Eval/human | Not a JSON contract pass |

---

## Validation procedure

### 1. Inputs to collect

- Schema artifact path + dialect + version hash
- Downstream side effects (which gates must run first)
- Whether empty / null / omit differ
- Max retries, timeout, and fallback behavior
- PII/secret handling for logged raw outputs

### 2. Layered check (canonical order)

```text
completion_state → extract → parse → schema_validate → domain_invariants → accept
```

Stop at first hard failure class; record `reject_layer` for metrics.

### 3. Test matrix (must include)

| Case | Expect |
| :--- | :--- |
| Happy path | accept |
| Missing required field | schema reject |
| `additionalProperties` / unknown key | schema reject (if closed) |
| Wrong type (`"1"` vs `1`) | schema reject (no silent coerce for IDs/money) |
| Unknown enum | schema reject |
| Oversized array / string | domain or post-schema limit |
| Truncated JSON | truncation class — not “schema” |
| Markdown-fenced valid JSON | extract → accept (if enabled) |
| Refusal payload | refusal class |
| Cross-field contradiction (ship date &lt; order date) | domain reject |
| Schema-valid negative quantity | **domain reject** (classic deliverable) |

### 4. Retry policy

1. Retry only for: fence/extract, syntax (if repair disabled), schema (with error feedback), empty/truncated (budget bump).
2. Do **not** infinite-retry domain invariant failures that need catalog/DB truth.
3. Cap attempts; decrement temperature slightly on repair turns if using generative repair.
4. Track `validation_attempts` in prod—persistent retries mean schema/model mismatch.

### 5. Deliverable

- Contract tests with explicit accept/reject fixtures
- `reject_layer` metrics dashboard fields
- Schema + domain code paths that run **before** external actions
- Documented null/omit semantics

---

## Production example: layered validator (Python)

```python
"""LLM JSON contract check: completion → parse → JSON Schema → domain."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any

# pip install jsonschema
from jsonschema import Draft202012Validator


class RejectLayer(str, Enum):
    REFUSAL = "refusal"
    TRUNCATION = "truncation"
    EMPTY = "empty"
    PARSE = "parse"
    SCHEMA = "schema"
    DOMAIN = "domain"


@dataclass
class ContractResult:
    ok: bool
    data: dict[str, Any] | None
    layer: RejectLayer | None
    errors: list[str]
    raw: str


_FENCE = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)


def extract_json_candidate(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    m = _FENCE.search(text)
    if m:
        return m.group(1).strip()
    # first object/array span
    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        end = text.rfind(closer)
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]
    return text


def domain_order_invariants(order: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    qty = order.get("quantity")
    if isinstance(qty, (int, float)) and qty <= 0:
        errs.append("quantity must be > 0")
    currency = order.get("currency")
    if currency not in {"USD", "EUR", "GBP"}:
        errs.append(f"unsupported currency: {currency!r}")
    # never silently rewrite sku / customer_id
    return errs


def check_contract(
    *,
    raw_text: str,
    schema: dict[str, Any],
    refused: bool = False,
    finish_reason: str | None = None,
    allow_extract: bool = True,
) -> ContractResult:
    if refused:
        return ContractResult(False, None, RejectLayer.REFUSAL, ["model refused"], raw_text)
    if not (raw_text or "").strip():
        return ContractResult(False, None, RejectLayer.EMPTY, ["empty completion"], raw_text)
    if finish_reason in {"length", "max_tokens"}:
        # still try parse only for diagnostics; classify as truncation if parse fails
        pass

    candidate = extract_json_candidate(raw_text) if allow_extract else raw_text.strip()
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError as e:
        layer = RejectLayer.TRUNCATION if finish_reason in {"length", "max_tokens"} else RejectLayer.PARSE
        return ContractResult(False, None, layer, [str(e)], raw_text)

    if not isinstance(data, dict):
        return ContractResult(False, None, RejectLayer.SCHEMA, ["root must be object"], raw_text)

    validator = Draft202012Validator(schema)
    schema_errs = [f"{e.json_path}: {e.message}" for e in validator.iter_errors(data)]
    if schema_errs:
        return ContractResult(False, None, RejectLayer.SCHEMA, schema_errs, raw_text)

    domain_errs = domain_order_invariants(data)
    if domain_errs:
        return ContractResult(False, None, RejectLayer.DOMAIN, domain_errs, raw_text)

    return ContractResult(True, data, None, [], raw_text)


ORDER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["sku", "quantity", "currency"],
    "properties": {
        "sku": {"type": "string"},
        "quantity": {"type": "integer"},
        "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]},
        "note": {"type": ["string", "null"]},
    },
}

# Syntactically valid JSON with negative quantity → DOMAIN reject, not accept.
```

### TypeScript (Zod) sketch

```typescript
import { z } from "zod";

export const OrderSchema = z
  .object({
    sku: z.string().min(1),
    quantity: z.number().int(),
    currency: z.enum(["USD", "EUR", "GBP"]),
    note: z.string().nullable().optional(),
  })
  .strict()
  .superRefine((val, ctx) => {
    if (val.quantity <= 0) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, message: "quantity must be > 0", path: ["quantity"] });
    }
  });
```

Use the **same** Zod/Pydantic object to (a) generate provider JSON Schema when supported and (b) validate after parse—one source of truth.

---

## Repair guidance (do / don’t)

**Do (deterministic, logged)**

- Strip markdown fences (the #1 real-world malformation)
- Extract first top-level `{...}` / `[...]` from brief prose
- Optionally fix trailing commas / Python `True`/`None` on non-critical paths

**Don’t**

- Fuzzy-remap keys or coerce money/IDs before domain checks on irreversible actions
- “Auto-complete” truncated payment/auth payloads by closing braces and shipping
- `eval()` / execute repaired content
- Hide repair success without metrics (you will miss schema debt)

Prefer **structured outputs** so repair is rare; keep repair as defense in depth.

---

## Technical troubleshooting matrix

| Signature | Root cause | Fix |
| :--- | :--- | :--- |
| Valid JSON, wrong shape | JSON mode only / weak prompt | Enable strict `json_schema` or tools |
| API 400 on schema | Unsupported keywords / deep `$ref` | Simplify schema; move constraints to domain |
| Persistent schema retries | Schema too complex / wrong model | Split stages; simplify enums |
| Empty completions | Token budget spent on reasoning | Raise `max_output_tokens`; shorten schema |
| Extra fields break clients | Open objects | `additionalProperties: false` / `.strict()` |
| “Fixed” by coercing `"01"`→`1` | Silent type cast | Keep string IDs; reject wrong types |
| Schema pass, bad business row | Missing domain layer | Add invariants; fixture with qty &lt; 0 |

---

## Best practices

1. One schema module shared by API codegen, LLM structured output, and runtime validation.
2. Version the schema (`schema_hash` on eval/result rows) next to prompts (`@prompt-regression-gate`).
3. Return machine-readable error paths (`$.items[2].qty`) to the model on repair turns.
4. Eval structured tasks with accept/reject fixtures, not only BLEU-like prose scores.
5. Separate **user-visible refusal text** from **internal validation errors**.

---

## Limitations

- Provider “strict” modes do not prove semantic correctness.
- Unsupported JSON Schema keywords still need application-side checks.
- Stop and ask if the downstream schema dialect or side-effect list is unknown.

---

## Related skills

- `@llm-json-contract-check` — this skill
- `@ai-evaluation-dataset` — accept/reject fixtures + hashes
- `@prompt-regression-gate` — prompt changes vs frozen contract tests
- `@agent-injection-boundary-test` — untrusted model/tool text
- `@ai-pii-redaction-review` — raw payload logging
- `@llm-cost-latency-benchmark` — cost of validation retries

---

## Agent Operational Directive

> **MANDATORY**: Validate in layers (completion → parse → schema → domain) with the app’s real validator. Prefer strict structured outputs. Never silently coerce critical fields. Never treat refusal/truncation as schema failures. Reject schema-valid but business-invalid payloads before side effects. Preserve raw rejects securely; bound retries.

---

## Source anchors (research)

- [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) / [Intro announcement](https://openai.com/index/introducing-structured-outputs-in-the-api/)
- [Azure OpenAI structured outputs schema limits](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
- Repair/fence realities: structured-output-repair, outputguard, llm-pipeline validation docs
- Community: `$ref` nesting failures with strict schemas; fences as top malformation class
