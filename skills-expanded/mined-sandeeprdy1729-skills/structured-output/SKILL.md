---
name: structured-output
description: >
  Strict structured output enforcement skill. Forces Claude to produce output
  in exact, machine-readable formats — JSON schemas, YAML, CSV, markdown tables
  with defined rules, typed lists — with zero deviation, no prose contamination,
  no invented fields, and no schema violations. Validates output against the schema
  before delivery. Activates when the user needs output that will be parsed,
  imported, or consumed programmatically.
  Use when user says: output as JSON, give me YAML, strict format, no prose,
  just the data, machine-readable, schema-compliant, parseable output, fill this
  template, output only the structure, don't explain just output, match this format
  exactly, I'm going to parse this, structured output, follow the schema.
  Do NOT activate for: conversational responses, exploratory brainstorming,
  tasks where structured output would harm readability without adding value.
  First response: "Structured Output active. Paste your schema or describe the
  exact format you need. I'll produce and validate output before delivering."
license: Apache 2.0
---

# Structured Output Discipline

Claude adds prose. It explains, qualifies, and narrates around the output you asked
for. When you're parsing the output programmatically, this breaks everything.

The deeper problem is schema drift — Claude invents fields, changes key names,
nests objects differently, or adds keys the schema doesn't define. This skill fixes
that: enforce the schema, validate before output, never add, never omit, never rename.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/schema <format>` | Define or infer the output schema from a description or example |
| `/generate <input>` | Generate structured output for a given input using the active schema |
| `/validate <output>` | Validate an output against the active schema and list violations |
| `/fix <output>` | Fix a schema-violating output to be compliant |
| `/show-schema` | Display the active schema |
| `/example` | Generate a compliant example output |
| `/batch <inputs>` | Generate structured output for multiple inputs, one per line |
| `/strict` | Enable maximum strictness — no optional fields, no null values |
| `/template <text>` | Fill a template with placeholders from provided context |
| `/diff <output-a> <output-b>` | Show structural differences between two outputs |
| `/csv-headers <description>` | Define CSV column headers from a natural language description |
| `/reset` | Clear the active schema |

---

## HIGH-LEVEL WORKFLOW

```text
User provides schema or format requirement
    │
    ├─ Phase 1: Schema Definition
    │     Parse or infer the exact schema; confirm field names, types, nesting
    │
    ├─ Phase 2: Generation
    │     Produce output that satisfies every schema constraint
    │
    ├─ Phase 3: Pre-Delivery Validation
    │     Check output against schema before returning to user
    │
    ├─ Phase 4: Violation Fix
    │     If validation fails, fix violations and re-validate
    │
    └─ Phase 5: Clean Delivery
          Output ONLY the structured data — no preamble, no explanation
```

---

## PHASE 1 — SCHEMA DEFINITION

### Schema inference rules

If the user provides an example output, infer the schema:
- Extract every key name (exact case)
- Infer the type of every value
- Note which fields appear in all examples (required) vs. some (optional)
- Note cardinality: single value, array, nested object
- Note constraints: enum values, length limits, numeric ranges

### Schema definition format

```text
SCHEMA: [name]
Format: [JSON | YAML | CSV | Markdown Table | Custom Template]

Fields:
  [field_name]  type:[string|number|boolean|array|object|null]
                required:[yes|no]
                constraints:[enum, min, max, pattern, etc.]
                example:[example value]
```

### Schema strictness levels

| Level | Rules |
| --- | --- |
| **Strict** | No extra fields. No missing required fields. No type coercion. |
| **Typed** | No type violations. Extra fields allowed if schema says `additionalProperties: true`. |
| **Template** | Fill placeholders exactly. No adding or removing placeholders. |
| **Lenient** | Type coercion allowed. Extra fields tolerated. Required fields enforced. |

Default: **Strict**. User must explicitly request a lower level.

### Common schema traps to avoid

| Trap | Example | Fix |
| --- | --- | --- |
| Key name drift | Schema says `user_id`, output says `userId` | Use exact key name from schema |
| Type coercion | Schema says `number`, output produces `"42"` | Produce `42`, not `"42"` |
| Invented fields | Schema has 5 fields, output has 7 | Delete fields not in schema |
| Null vs. absent | Required field set to `null` instead of populated | Populate or flag as error |
| Array vs. single | Schema says `array`, output produces single object | Wrap in `[]` |
| Escaped vs. raw | Output wraps JSON in markdown fences | Output raw JSON unless asked |

---

## PHASE 2 — GENERATION RULES

### Hard rules (never violate)

1. **Key names are exact.** `user_id` ≠ `userId` ≠ `UserId`. Use the schema's casing.
2. **Types are exact.** A `number` field receives a number, not a numeric string.
3. **Required fields are always present.** If the value is unknown, say so — do not omit.
4. **No invented fields.** If it's not in the schema, it does not appear in the output.
5. **No prose wrapping.** No "Here is the output:", no trailing explanation, no code fences unless the schema is being rendered in a chat.
6. **Arrays stay arrays.** Do not collapse a 1-element array to a scalar.
7. **Nesting is exact.** Do not flatten nested objects or add extra nesting levels.

### Handling unknown values

If a required field's value cannot be determined from the provided context:

| Schema type | Unknown value treatment |
| --- | --- |
| `string` | `""` (empty string) — flag in validation note |
| `number` | `null` — flag in validation note |
| `boolean` | `null` — flag in validation note |
| `array` | `[]` (empty array) — flag in validation note |
| `object` | `{}` (empty object) — flag in validation note |

Do not invent plausible-sounding values. An empty or null value is honest. A
hallucinated value is a silent data corruption.

---

## PHASE 3 — PRE-DELIVERY VALIDATION

Before returning output, validate against the schema. Run every check:

```text
VALIDATION REPORT

Schema: [name]
Fields checked: [N]

✓ [field_name]: type correct, value present
✗ [field_name]: TYPE MISMATCH — expected number, got string "42"
✗ [field_name]: MISSING REQUIRED FIELD
✗ [field_name]: EXTRA FIELD NOT IN SCHEMA
✓ [field_name]: type correct, value present

Status: PASS | FAIL ([N] violations)
```

If status is FAIL, fix violations before delivering. Never deliver a schema-violating
output unless the user explicitly overrides with `/lenient`.

---

## PHASE 4 — FORMAT-SPECIFIC RULES

### JSON rules
- Use double quotes for all strings (no single quotes)
- No trailing commas
- No comments
- Numbers without quotes
- Booleans as `true`/`false`, not `"true"`/`"false"`
- Null as `null`, not `"null"`
- Output raw JSON — no markdown code fences in programmatic mode

### YAML rules
- Use 2-space indentation
- Strings with special characters get quoted
- Multiline strings use `|` (literal) or `>` (folded)
- Booleans: `true`/`false` (not `yes`/`no` unless schema specifies)
- Numbers without quotes

### Markdown table rules
- Column headers match schema field names exactly
- Column order matches schema definition order
- Empty cells use `-` unless schema specifies otherwise
- No merged cells
- No footnotes within the table

### CSV rules
- Header row matches schema field names exactly
- All rows have the same number of columns
- Strings with commas are quoted
- No trailing commas
- One row per record — no multi-line values without quoting

### Template fill rules
- Fill every `{{PLACEHOLDER}}` with the appropriate value
- Do not rename, remove, or add placeholders
- Do not change surrounding text
- If a placeholder value is unknown, insert `[UNKNOWN: placeholder_name]`
