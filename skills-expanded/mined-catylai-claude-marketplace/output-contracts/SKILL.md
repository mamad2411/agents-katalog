---
name: output-contracts
description: "Makes agent output consistent and honest. Use when output format or judgement varies between runs, when extraction returns empty or invented fields, or when designing a JSON schema an agent fills. Covers categorical criteria, severity defined by example, reasoned few-shot examples, and schemas that let the model say a value is absent. Not for retry mechanics (use agentic-loop-control); not for citations or human-review routing (use provenance-and-escalation); not for tool descriptions (use tool-interface-design)."
license: MIT
---

# Output contracts

Several distinct defects usually get treated as one. Keep them apart, because each has a different
fix and applying the wrong one burns tokens without moving the metric.

| Defect | Fix | Not the fix |
| --- | --- | --- |
| Invalid JSON or schema violation | Constrained decoding: structured output, or a strict tool schema | More instructions, more retries |
| Inconsistent judgement on ambiguous cases | Two to four *reasoned* few-shot examples | A bigger model, a stricter schema |
| Fabricated values for absent data | Nullable fields plus an `"unclear"` enum | Few-shot, retries |
| Vague or arbitrary flagging | Explicit categorical criteria | "Be conservative", confidence filters |

Criteria come before examples; examples come before more instructions; a schema comes before either
for anything mechanical.

This skill owns structured-output guarantees and the strict-schema complexity budget. The numeric
limits, SDK helper names, and parameter history are in
[references/structured-output-limits.md](references/structured-output-limits.md). Porting notes are
in [references/porting.md](references/porting.md).

## 1. Give categorical criteria, not dispositions

"Be conservative" and "only report high-confidence findings" are moods, not instructions. An agent
cannot apply them consistently because they contain no boundary.

Replace them with categorical statements that have a concrete trigger, including what to skip.

```text
Bad:  "Review this code. Be conservative. Only report high-confidence findings."

Good: "Flag a comment only when the claimed behaviour contradicts the actual behaviour.
       Report bugs and security vulnerabilities. Skip minor style preferences and
       conventions that are consistent within this module."
```

Filter by criteria rather than by the model's self-reported confidence, which is poorly calibrated,
so a threshold silently becomes an arbitrary cut. If one finding category has a high false-positive
rate, disable that category temporarily to protect trust in the others, then fix its criteria
before re-enabling it. A reviewer who has learned to ignore your output is a harder problem than a
missing category.

## 2. Define severity by example, not by adjective

Prose definitions ("critical means a serious security impact") collapse under pressure. Code
examples do not. Two or three examples per level, drawn from your actual codebase, beat a page of
definitions. See the first example under "Patterns that hold up".

## 3. Use two to four reasoned few-shot examples, for the right defects

Few-shot is the right first move when output is inconsistently *formatted*, when judgement on
ambiguous cases varies run to run, or when extraction returns empty fields for data that
demonstrably exists, such as values stated in narrative prose rather than in a labelled field.

Two requirements. Each example includes the **reasoning**, not just input and output, because the
reasoning is what generalizes to cases you did not enumerate. And the examples cover the scenarios
that are actually failing, not the easy ones.

Route other defects to the technique that owns them: malformed JSON is a schema problem,
fabrication is a nullable-field problem, and tool misrouting is a description problem
(tool-interface-design).

## 4. Use first-class structured output, and know its limits

Structured output is a real API feature rather than a tool-use trick, in two independent halves:

- **JSON output:** an output format carrying a JSON schema constrains the response text via
  constrained decoding.
- **Strict tool use:** `"strict": true` on a tool definition guarantees the tool name and input
  conform to the input schema.

Use them together when you need both valid tool calls and a structured final answer. The SDK
helpers (Pydantic in Python, Zod in TypeScript) strip JSON Schema keywords the API does not support,
then validate the response against your *original* schema, so you keep those constraints.

What it guarantees: syntactic validity and schema conformance on a turn that ended normally. What it
does **not** guarantee:

- **Semantic correctness.** Sums that do not add up, values in the wrong field, a plausible
  invention in a required field. Validate separately (section 6).
- **A conforming payload on a refusal or on truncation.** Check `stop_reason` before parsing.
- **Enum capitalization.** A returned value may differ from your enum only in casing. Compare
  case-insensitively, and keep enum values distinct beyond case.
- **Property order matching your schema.** Required properties are emitted first, then optional
  ones. If order matters, mark everything required.

Costs: strict schemas share a per-request complexity budget (strict tool count, optional
parameters, union-typed parameters), plus internal grammar-size limits and a compilation timeout.
Grammars are compiled and cached, so the first request on a new schema is slower. Structured output
injects a system prompt, so input tokens rise slightly, and changing the output format invalidates
the conversation's prompt cache (owned by context-economy). It does not combine with citations or
with message prefilling; it works with batch and streaming.

Keep sensitive personal data out of schema property names, enum values, const values, and pattern
regexes, because schemas are cached separately from message content and do not get the same data
protections.

## 5. Design the schema to make honesty possible

The schema is your primary defense against fabrication, and it works by giving the model a
legitimate way to say "not present."

- Make source-dependent fields optional or nullable (`"type": ["string", "null"]`). A required
  field the source does not contain is an instruction to invent something.
- Add an `"unclear"` enum member for genuine ambiguity, and `"other"` plus a detail string for
  extensibility.
- Put format-normalization rules in the prompt as well as the schema: ISO 8601 dates, decimal
  currency without symbols, country codes.
- Keep `required` minimal and meaningful: only what is true of every valid record.

This is in tension with the strict-mode complexity budget, since optional and union-typed fields are
exactly what those limits count. Resolve it by making nullability deliberate (nullable on fields
that genuinely may be absent, required on the rest) rather than defaulting everything to optional.

## 6. Build self-checks into the schema, then validate semantics

Ask the model to emit the evidence of its own correctness, then check it in code:

- `calculated_total` alongside `stated_total`, and compare them.
- `conflict_detected: boolean` with the conflicting values attached.
- Detected-pattern fields, so systematic errors show up in aggregate rather than one at a time.
- A source span or excerpt per extracted field, so a value can be traced back to text.

The error strings from this validator are what a targeted retry needs. When to retry and when to
return `null` or escalate instead is owned by agentic-loop-control (rule 5).

## Audit checklist

- [ ] Grep the system prompt for "be conservative", "high-confidence", "use your judgement",
      "only if you're sure"; each is a missing criterion.
- [ ] Severity is defined by code example rather than prose.
- [ ] There is an explicit skip list, not only an include list.
- [ ] No routing or filtering decision depends on self-reported confidence.
- [ ] JSON comes from constrained decoding, not from prompt instructions plus a try/except.
- [ ] Count the instructions about JSON *syntax*; each is a schema fix waiting to happen.
- [ ] Source-dependent fields are nullable rather than all-required.
- [ ] There is an `"unclear"` enum value and an `"other"` plus detail string.
- [ ] Normalization rules are stated in the prompt, not merely implied.
- [ ] The schema carries self-check fields and there is a semantic validator downstream.
- [ ] Refusal and truncation stop reasons are handled before parsing.
- [ ] Enum comparisons are case-insensitive; no two enum values differ only by case.
- [ ] Output parsing does not depend on property order.
- [ ] Strict schemas fit the complexity budget.
- [ ] Few-shot examples include reasoning and come from actual failures.
- [ ] No personal or sensitive data is embedded in property names, enums, or patterns.

## When reviewing code

Without a checkout, review pasted prompts, schemas, and parsing code the same way. Report findings
ranked by impact:

```text
<file>:<line> — rule <n> (<rule name>) — <fix in one sentence> — impact: high|medium|low
```

`high` = required fields that force invention, parsing without a `stop_reason` check, or no semantic
validation; `medium` = dispositional criteria, confidence filters, examples without reasoning;
`low` = enum casing or property-order assumptions. If nothing violates a rule, say so and list the
checklist items you confirmed.

**Verify:** after fixes, run the extraction on at least one document that lacks an optional field
and confirm the field comes back `null` rather than invented.

## Patterns that hold up

<example>
Explicit criteria with skip rules and example-defined severity.

```text
Report a finding only if it matches a category below. Report nothing else.

Bug: code whose behaviour differs from what the surrounding code or comments require.
  Example: `if (user.role = "admin")` (assignment in a condition).
Security: untrusted input reaching a sink without validation, or a secret generated,
  stored, or compared unsafely.
  Example: `session_id = str(random.random())`
Stale comment: report only when the claimed behaviour contradicts the actual behaviour.
  Skip comments that are merely terse, outdated in style, or missing.

Skip: naming conventions, import order, formatting, patterns that are consistent within
the module, and anything you would describe as a preference.

Severity by example:
  critical  query = f"SELECT * FROM users WHERE id = {user_input}"
  high      session_id = str(random.random())
  minor     userName next to user_name in the same file
```

Every decision has a stated trigger and a stated exclusion, so two runs on the same input produce
the same set and a false positive traces to a criterion you can edit.
</example>

<example>
A reasoned example covering the actual failure mode.

```text
Input (narrative prose, no table: the format that was returning empty fields):
  "We agreed to net-45 terms on the renewal, and the buyer confirmed PO 44-8812 covers it."

Extraction:
  { "payment_terms": "net 45", "purchase_order": "44-8812" }

Reasoning:
  Payment terms and PO numbers are frequently stated in prose rather than in a labelled
  field. "net-45" is a payment term even though the document has no "Payment Terms:" label,
  and "PO 44-8812" is a purchase order reference even though it appears mid-sentence.
  Extract from prose whenever the value is unambiguous; use null only when the document
  genuinely does not state it.
```

The reasoning transfers to phrasings not in the examples. An input-output pair alone teaches only
the two strings.
</example>

<example>
Structured output with a validating SDK helper.

```python
from pydantic import BaseModel
from typing import Literal

class LineItem(BaseModel):
    description: str
    amount: float

class Invoice(BaseModel):
    invoice_number: str                       # required: every valid invoice has one
    vendor_name: str
    invoice_date: str                         # required, ISO 8601 per the prompt
    line_items: list[LineItem]
    stated_total: float
    calculated_total: float                   # self-check
    payment_terms: str | None = None          # nullable: often absent
    purchase_order: str | None = None         # nullable: often absent
    document_type: Literal["invoice", "credit_note", "receipt", "unclear", "other"]
    document_type_detail: str | None = None   # required when document_type == "other"

response = client.messages.parse(             # the helper builds the output format from the model
    model=MODEL, max_tokens=4096,
    output_format=Invoice,
    messages=[{"role": "user", "content":
        "Extract invoice data. Dates as ISO 8601 (YYYY-MM-DD). Amounts as decimals with no "
        f"currency symbol. Use null for anything the document does not state.\n\n{doc}"}],
)
if response.stop_reason in ("refusal", "max_tokens"):
    return route_to_human(response, reason=response.stop_reason)   # payload may not match
inv = response.parsed_output
```

Nullable fields give the model a truthful option; `"unclear"` absorbs the document that fits no
type, and `"other"` the one that fits a type you did not list; normalization lives in the prompt
where the model can act on it; and `calculated_total` makes the arithmetic auditable.
</example>

<example>
Semantic validation after schema validation.

```python
def validate(inv: Invoice) -> list[str]:
    errs = []
    line_sum = sum(li.amount for li in inv.line_items)
    if abs(line_sum - inv.stated_total) > 0.01:
        errs.append(f"line items sum to {line_sum:.2f} but stated_total is {inv.stated_total:.2f}")
    if abs(inv.calculated_total - inv.stated_total) > 0.01:
        errs.append("calculated_total disagrees with stated_total")
    if inv.document_type == "other" and not inv.document_type_detail:
        errs.append("document_type 'other' requires document_type_detail")
    if not ISO_DATE.match(inv.invoice_date):
        errs.append(f"invoice_date '{inv.invoice_date}' is not ISO 8601")
    return errs
```

Every one of these passes schema validation and is still wrong. This is the layer constrained
decoding does not provide, and the error strings are what a targeted retry needs.
</example>

<example>
A classification that always has a valid answer, without forcing a tool. Forced `tool_choice` is
model-dependent (see tool-interface-design), so put the choice in the output schema instead.

```json
{
  "output_config": { "format": { "type": "json_schema", "schema": {
    "type": "object",
    "properties": {
      "document_type": { "type": "string", "enum": ["invoice", "credit_note", "unclear"] },
      "reason":        { "type": "string" },
      "closest_match": { "type": ["string", "null"] }
    },
    "required": ["document_type", "reason", "closest_match"],
    "additionalProperties": false } } }
}
```

The schema guarantees a structured answer on every normal turn, and `"unclear"` plus `reason` gives
the model a correct option when no type fits, so it does not force a credit note into the invoice
shape. Route each type to its own extraction schema in a second request.
</example>

## Failure modes

**Dispositional instructions, and confidence as a stand-in for criteria.** "Be conservative" has no
boundary, so the finding set varies between runs on identical input and nobody can say which run was
right. A 0.8 confidence filter looks rigorous but cuts arbitrarily, discarding real findings and
keeping confident-sounding false ones.

**More instructions in response to inconsistency.** "Return valid JSON. Use double quotes. No
markdown fences. Seriously, just JSON." fights a syntax problem with prose: tokens on every request,
never 100%, and the residual failures still need a parser fallback. Use instructions for semantics
the schema cannot express (which value goes in which field, how to normalize) and the schema for
syntax.

**Examples without reasoning, drawn from the easy cases.** Three well-formatted invoices teach
nothing about the narrative-prose invoice that was actually failing, and with no reasoning nothing
generalizes past the literal pattern.

**Every field required, so the model must invent.** Under constrained decoding the model *cannot*
omit a required field, so when the invoice has no PO it emits a plausible one. You have converted a
missing value into a confident wrong value, which is strictly worse because it now passes
validation.

**Treating structured output as a correctness guarantee.** Constrained decoding guarantees shape,
not truth. Sums that do not add up, values swapped between fields, and invented required values all
serialize perfectly.

**Blanket strictness, or a schema that cannot compile.** Dozens of strict tools with dozens of
optional parameters exceed the complexity budget and return a schema-complexity error or hit the
compilation timeout. Even when it compiles, every schema edit pays first-request grammar latency
again.
