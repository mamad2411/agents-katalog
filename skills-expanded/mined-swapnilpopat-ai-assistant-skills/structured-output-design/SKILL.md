---
name: structured-output-design
description: Force LLMs to emit machine-parseable outputs (JSON Schema, function calls, grammars) to cut output tokens, eliminate parse-retry loops, and remove fragile post-processing. Use when an LLM response feeds another system or you see frequent "the model returned malformed JSON" bugs.
source: self
date_added: 2026-05-01
---

# Structured Output Design

Free-text outputs are the most expensive and fragile thing an LLM can produce. Constrain them.

## When to Use

- LLM output is parsed by code downstream.
- You see retry loops because the model "almost" returned valid JSON.
- Output tokens dominate cost (chatty answers, verbose explanations).
- Multi-step pipelines where step N consumes step N-1's output.
- Tool / function calling, classification, extraction, routing.

## Why This Saves Tokens and Money

- **No prose padding.** "Here is the JSON you asked for: ```json ..." disappears.
- **No retries on malformed output.** Constrained decoding can't emit invalid structure.
- **Smaller `max_tokens`** safely — you know the worst-case shape.
- **Smaller models become viable** because the hard part (formatting) is offloaded to the decoder.
- **No second-pass "extract the JSON" call.**

## Mechanism Hierarchy (Strongest to Weakest)

| Mechanism | Guarantees | Cost | Use when |
| --- | --- | --- | --- |
| Constrained decoding (grammars, JSON Schema with `strict: true`) | Output is valid by construction | Sometimes higher latency | Anything machine-consumed |
| Function / tool calling | Valid args; provider validates | Tiny | Action selection, structured extraction |
| Provider "JSON mode" | Valid JSON, but not your schema | None | Quick wins where shape is loose |
| Prompted JSON ("respond with JSON like...") | Best-effort | None | Prototypes only — never production |

Use the strongest one your provider supports for the model in play.

## Provider Notes (2026)

- **OpenAI** — Structured Outputs with JSON Schema (`response_format: {type: "json_schema", strict: true}`); function calling with strict schemas. Guarantees a valid match.
- **Anthropic** — Tool use enforces tool input schemas; for free-form structured output, define a "respond_with" tool with the desired schema and force tool choice.
- **Google Gemini** — `responseSchema` + `responseMimeType: "application/json"` enforces a subset of OpenAPI schema.
- **Open-source / vLLM / llama.cpp** — Outlines, XGrammar, llguidance, lm-format-enforcer for grammar-constrained decoding.

## Schema Design Rules

1. **Closed shapes only.** `additionalProperties: false`. No "misc" or "extras" fields.
2. **Enums for everything categorical.** Forces the model into a small token set.
3. **Required everywhere it matters.** Optional fields cost more output and breed ambiguity.
4. **Bounded arrays.** Use `maxItems` to cap output size predictably.
5. **Bounded strings** where shape is known (enums, regex, max length).
6. **Avoid recursion / unions** unless the model's schema implementation supports them well — many don't.
7. **Top-level object, not array.** Easier to extend, plays nicer with streaming.
8. **Field order matters.** Put fields in the order the model should reason — earlier fields condition later ones.

## Prompting With a Schema

- Don't restate the schema in prose if the API already enforces it. Wastes input tokens.
- Do give field-level *meaning* in the schema's `description` — the model sees it.
- One example matching the schema beats five sentences of instructions.
- Forbid wrappers: "Output only the object. No prose. No code fences."

## Streaming Structured Output

- Use partial-JSON parsers (e.g., `partial-json`, `json-stream`) to start rendering as fields complete.
- Order fields so user-visible ones stream first; "reasoning" / metadata fields last.
- Cancel the stream the instant a field violates an invariant — saves output cost.

## Reasoning + Structure

When you want chain-of-thought *and* a clean output:

- Put a `reasoning: string` field **first**, then the answer fields.
- Or use a "scratch" tool the model calls before the final tool.
- Do **not** ask for "step by step" in prose then a JSON block — you'll pay for both and parsing breaks.
- Drop the reasoning field downstream if you don't need it; don't feed it to the next call.

## Migration: From Prompted JSON to Strict Schemas

1. Capture 100+ real outputs from the current free-text prompt.
2. Derive the schema from observed shapes (then tighten).
3. A/B: free-text vs strict. Compare success rate, output tokens, latency, retries.
4. Roll out with a fallback only if strict mode is unavailable for the model.
5. Delete the post-processing parser. It is now technical debt.

## Quick Wins Checklist

- [ ] All machine-consumed outputs use the strongest available constraint
- [ ] Schemas are closed (`additionalProperties: false`)
- [ ] Categorical fields are enums
- [ ] Arrays are bounded (`maxItems`)
- [ ] No prose instructions duplicating schema constraints
- [ ] `max_tokens` reduced to match worst-case schema size
- [ ] Parse-retry loop deleted from the call site
- [ ] Reasoning is a schema field, not a separate prose dump

## Anti-Patterns

- "Respond with JSON" in the prompt while the API supports strict mode — leaves reliability and tokens on the table.
- Open schemas with `additionalProperties: true` — the model fills them with junk.
- Asking for prose explanation *and* JSON in the same call.
- Free-text enums ("status: active | pending | disabled or similar") — the model invents values.
- Schemas so large they exceed the prompt savings (rare, but happens with deeply nested unions).
- Catching JSON parse errors and silently retrying — that's a budget leak; fix the root cause.

## References

- OpenAI Structured Outputs documentation
- Anthropic tool use and JSON output guidance
- Google Gemini `responseSchema` documentation
- Outlines, XGrammar, llguidance project docs (open-source constrained decoding)
- Related skills: `token-efficient-prompting`, `llm-cost-optimization`, `api-error-handling`
