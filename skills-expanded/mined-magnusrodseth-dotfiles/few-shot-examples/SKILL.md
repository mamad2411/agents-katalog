---
name: few-shot-examples
description: Best practices for designing few-shot (input→output) examples in prompts for AI and agentic applications. Use when writing or reviewing prompts that need consistent formatting, structured/JSON output, classification, extraction, edge-case handling, or hallucination reduction; or when the user mentions few-shot, multishot, in-context examples, or "show the model an example".
---

# Few-Shot Examples

Few-shot examples are concrete input→output pairs embedded in a prompt to guide the model by demonstration instead of description. They are the most reliable lever for output *format* and *edge-case behavior*, and the primary defense against hallucinated values.

## When to use them

Reach for few-shot examples when the task needs any of:

1. **Consistent formatting** — lock output to one structure across every call.
2. **Ambiguous / edge-case handling** — show how to handle the cases prose underspecifies (nulls, empties, conflicting inputs).
3. **Generalization** — demonstrate the pattern so the model applies it to novel inputs.

Prefer examples over longer prose instructions for these. Examples *show*; criteria *tell*. Use both together.

## Core rules

- **Wrap each example in XML tags.** Use `<example>` with nested `<input>` / `<output>`. This makes boundaries unambiguous and matches Claude's prompt-structuring conventions.
- **Vary the inputs, fix the output shape.** To teach normalization, map *different* input formats to the *same* canonical output (e.g. several date formats → one ISO-8601 string).
- **Always include a missing-data example.** Demonstrate that `null`/empty in → `null`/`partial_record` out is *correct*. This removes the model's incentive to fabricate. (See [REFERENCE.md](REFERENCE.md) for the canonical null-handling example.)
- **2–5 examples is usually enough.** Cover the common case plus the edge cases that matter; more examples cost tokens and context for diminishing returns.
- **Make examples representative, not adversarial.** They define the pattern, so every example should be one you'd be happy to see the model imitate.

## Quick start

```xml
<example><input>Date: March 15th, 2024</input><output>2024-03-15</output></example>
<example><input>Date: 15/03/2024</input><output>2024-03-15</output></example>
```

Two inputs, one output shape: the model learns to normalize, not just to copy.

## How few-shot fits with other techniques

- **Few-shot complements JSON schemas / tool_use, never replaces them.** A schema eliminates *syntax* errors (valid JSON, right fields). It does NOT eliminate *semantic* errors (right field, wrong value). Few-shot examples teach which value belongs where — the layer the schema can't enforce.
- **Pair with nullable-but-required schema fields** (`"type": ["string", "null"]`) so the model must explicitly acknowledge missing data instead of omitting or inventing it.
- **Use temperature 0** for the extraction/classification/structured tasks where few-shot matters most, so the demonstrated pattern is followed deterministically.
- **Validate empirically.** Run the prompt against a labeled dataset and grade outputs (code-based for format, model-based for content). Add/trim examples based on results; don't assume they help.

## Hard limitation

Few-shot examples teach *pattern and format* — they cannot manufacture information absent from the input. The same boundary applies as retry-with-error-feedback: examples fix **format errors**, never **missing information**. If the source lacks the data, the correct demonstrated behavior is to emit `null` / `partial_record`, not to fill the gap.

## Deeper material

See [REFERENCE.md](REFERENCE.md) for copy-paste patterns: null/hallucination handling, classification with extensible enums, schema redundancy for validation, and confidence/reasoning fields.
