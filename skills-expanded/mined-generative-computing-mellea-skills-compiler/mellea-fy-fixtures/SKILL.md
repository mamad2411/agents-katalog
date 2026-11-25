---
name: mellea-fy-fixtures
description: '# Melleafy Step 4: Fixture Generation'
metadata:
  user-invocable: true
  disable-model-invocation: true
---

# Melleafy Step 4: Fixture Generation

**Version**: 4.2.1 | **Prereq**: Step 3 complete (skeleton emitted with finalised `run_pipeline` signature) | **Produces**: `fixtures_emission.json`

> **Schema**: Output `intermediate/fixtures_emission.json` MUST conform to `schemas/fixtures_emission.schema.json`

> **Output path rule** (Rule OUT-4): Step 4 produces **ONLY** `intermediate/fixtures_emission.json` in the intermediate directory. This JSON file contains fixture specifications that will be used by downstream processes. **DO NOT generate any Python source files** — no `fixtures/` directory, no `.py` files, no `__init__.py`. The fixture source code generation is handled by a separate process outside this skill.

> **CRITICAL**: This step generates ONLY the JSON specification file.

Step 4 generates fixture specifications for 5–8 test fixtures covering ≥3 C-categories. The output is a single JSON file conforming to the schema.

> **Rule 4-1 — JSON-only fixture specification**: Generate all fixture specifications in a single JSON object conforming to `schemas/fixtures_emission.schema.json`. The invocation receives the `run_pipeline` signature, the element mapping summary, and the C-category coverage requirement, and returns **one JSON object** — not Python source. **This skill's output is ONLY the JSON file.** Do not generate Python fixture files, do not create a `fixtures/` directory, do not write `__init__.py` or individual fixture modules.

---

## CRITICAL: Input parameter matching

**The keys in every fixture's `inputs` object MUST be identical to the parameter names of the `run_pipeline` function in `pipeline.py`.** This is not optional. A fixture with `{"text": "..."}` for a pipeline that expects `run_pipeline(user_query=...)` will fail at runtime with a `TypeError`. Before emitting JSON, verify the exact parameter names from the generated pipeline function. The schema cannot enforce this — it's the model's responsibility to match.

---

## Fixture structure

The model emits one JSON object saved as `intermediate/fixtures_emission.json`. **This is the only output of Step 4.**

_JSON output (conforms to `fixtures_emission.schema.json`):_

```json
{
  "fixtures": [
    {
      "id": "positive_case",
      "description": "Critical priority ticket — should escalate to L2 immediately",
      "inputs": {
        "ticket_text": "URGENT: Production database is returning 500 errors for all queries.",
        "priority": "critical"
      }
    },
    {
      "id": "clean_case",
      "description": "Routine request — should route to standard support queue",
      "inputs": {
        "ticket_text": "Can you update my email address in the portal?",
        "priority": "normal"
      }
    }
  ],
  "coverage_doc": "Fixture coverage:\n  C1 Identity: all fixtures\n  C2 Operating rules: positive_case\n  C6 Tools: positive_case"
}
```

## Required fixture categories

Generate at least one fixture per category. Not all categories apply to every skill — use judgment:

| Category                   | Purpose                                                        | When to include                                 |
| -------------------------- | -------------------------------------------------------------- | ----------------------------------------------- |
| **Positive case**          | Clear input triggering the skill's primary behaviour           | Always                                          |
| **Clean/negative case**    | Input where the skill finds nothing or produces minimal output | Always                                          |
| **Edge case (structural)** | Empty input, very short, very long, missing optional fields    | Always                                          |
| **Edge case (domain)**     | Input at the boundary of the skill's scope                     | When the skill has meaningful domain boundaries |
| **Mixed case**             | Combination of positive and negative signals                   | For analysis/diagnosis archetypes               |
| **Out-of-scope case**      | Input the skill should explicitly decline                      | When the spec defines "When NOT to Use"         |

---

## C-category coverage requirement

Fixtures must collectively exercise ≥3 dependency categories (C1–C9). This is R16's fixture coverage threshold. Document which categories each fixture exercises in the `description` field.

Example — a ticket-triage skill with C1 (persona), C2 (operating rules), and C6 (tool calls):

- Positive case exercises C1 (persona applied), C2 (escalation rule fires), C6 (Slack notification called)
- Clean case exercises C1 and C2 (no escalation, no tool call)
- Edge case (empty) exercises C2 (out-of-scope handling rule)

---

## Quality rules

- Inputs must have realistic, non-trivial data — not placeholder text like `"some input here"`
- The `description` field states the expected behaviour, not just what the input is
- Do NOT use real credentials, personal data, or production system identifiers in fixtures
- Fixtures should run without network access — if the pipeline makes tool calls, use mock tool implementations or `load_from_disk` with bundled fixture data

---

## Cross-checks before Step 4 declares done

The schema (`fixtures_emission.schema.json`) and `intermediate/fixtures_emission.json` together enforce most of the contract structurally. The model is responsible only for content correctness:

- Fixture count: 5 ≤ N ≤ 8 (enforced by `minItems`/`maxItems` in the schema)
- At least 3 distinct C-categories exercised across all fixtures (model self-check; documented in `coverage_doc`)
- Every fixture's `inputs` keys match the generated `run_pipeline` signature exactly (model self-check; verify against `pipeline.py` before emitting JSON)
- Every fixture has a non-empty, realistic `inputs` value (not placeholder text)
- `coverage_doc` is populated with C-category coverage notes
