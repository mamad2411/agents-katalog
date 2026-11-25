---
name: tool-interface-design
description: "Designs and reviews tool and MCP tool definitions so an agent picks the right tool and calls it correctly. Use when writing a tool definition, when the agent picks the wrong tool or passes bad parameters, or when tool responses flood the context window. Not for MCP server setup or config scope (use mcp-integration); not for enforcing call order (use deterministic-enforcement); not for output schemas (use output-contracts)."
license: MIT
---

# Tool interface design

A tool is a contract between a deterministic system and a non-deterministic one. Design it for an
agent with a limited context window, not for a developer with a debugger.

Descriptions come first. Expanding a description is the cheapest and highest-leverage fix for
almost every tool-selection problem. Classifiers, routers, few-shot examples, and consolidation are
what you reach for *after* the descriptions are genuinely good.

This skill owns tool descriptions, the tool-result error flags, forced `tool_choice`, and the
tool-count thresholds (deferred loading, programmatic calling). Beta identifiers, measured savings,
and per-model restrictions are in [references/api-mechanics.md](references/api-mechanics.md).
Porting notes are in [references/porting.md](references/porting.md).

## 1. Description depth dominates tool performance

Anthropic's tool-use docs call detailed descriptions by far the most important factor in tool
performance, and suggest at least three to four sentences per tool, more for a complex one.

Cover five things:

1. What the tool does.
2. When to use it, **and when not to**.
3. What each parameter means and how it changes behavior.
4. Caveats and limits, including what the tool does *not* return.
5. Explicit boundaries against the neighboring tools it gets confused with.

Write it the way you would brief a new hire: make implicit context explicit (query formats, niche
terminology, relationships between the underlying resources). Name parameters unambiguously
(`user_id`, not `user`). For nested or format-sensitive inputs, add schema-validated
`input_examples` as a supplement to the description rather than a substitute.

Tool names match `^[a-zA-Z0-9_-]{1,128}$`.

## 2. Namespace by service and resource

With dozens of servers and hundreds of tools in play, overlapping or vaguely named tools cause
confusion. Group with common prefixes: `tracker_search` / `chat_search` by service,
`tracker_projects_search` / `tracker_users_search` by resource. Prefix versus suffix has
measurable, model-dependent effects, so choose one by evaluation and then stay consistent.

## 3. Build for the workflow, not for the endpoint

The common error is wrapping existing functions one-for-one. Agents have different affordances than
programs: computer memory is cheap, agent context is not. A tool that returns all contacts so the
agent can scan them is brute-force search charged to the context window.

| Instead of | Build |
| --- | --- |
| `list_users` + `list_events` + `create_event` | `schedule_event`, which finds availability and books |
| `read_logs` | `search_logs`, returning matching lines with surrounding context |
| `get_customer_by_id` + `list_transactions` + `list_notes` | `get_customer_context` |
| `create_pr` + `review_pr` + `merge_pr` | one tool with an `action` parameter |

Fewer, more capable tools reduce selection ambiguity. Give each a clear, distinct purpose, because
consolidation is not a license to build a god-tool.

## 4. Return high signal, and cap the volume

**Quality.** Return fields the agent can reason about: `name`, `file_type`, `modified` rather than
`mime_type`, `256px_image_url`, `acl_hash`, `shard`. Keep a stable identifier (a slug or ID) when the
agent will need it for a follow-up call, and drop opaque internal references it can never use. When
some callers need the IDs and some do not, expose a `response_format` enum (`concise` |
`detailed`) and let the agent choose.

**Quantity.** Implement pagination, range selection, filtering, and truncation with sensible
defaults on anything that can grow, and set a token ceiling on every response. When you truncate,
say so and steer: tell the agent to make several small targeted searches rather than one broad one.
Trimming results after the fact, and Claude Code's MCP output limits, are owned by context-economy.

Response structure (JSON vs XML vs Markdown) measurably affects performance with no universal
winner. Pick by evaluation.

## 5. Errors are prompts

A validation failure is a chance to teach the correct call. Return specific, actionable guidance and
a correctly formatted example, because an opaque code or a stack trace gives the agent nothing to
change.

```text
Bad:  "Error: 400 Bad Request"
Bad:  "ValidationError at $.filters[0].op"
Good: "Invalid `date_range`: expected ISO 8601 like '2026-01-15/2026-03-31', got 'last quarter'.
       Resolve relative dates before calling. Example: {\"date_range\": \"2026-01-01/2026-03-31\"}"
```

Flag failures with the protocol's own field: the Claude API uses `is_error: true` on the
`tool_result` block (snake_case); MCP uses `isError: true` on the tool result (camelCase). Normalize
at your boundary. Fields such as `errorCategory` and `isRetryable` are in neither specification;
adopt them as a convention inside your payload. The retry categories and the rule that an empty
result must look different from an unreachable source are owned by agentic-loop-control.

## 6. Size the tool set by the documented thresholds

"Four or five tools per agent" is folklore. The documented guidance:

- Selection accuracy degrades past roughly 30–50 available tools.
- Under 10 tools, or tiny definitions, plain tool calling is the better fit.
- At 10+ tools, definitions over roughly 10k tokens, or many aggregated MCP servers, use the **tool
  search tool**: add it to `tools` and set `defer_loading: true` on the tools that should not load
  up front. Keep the three to five most-used tools non-deferred. At least one tool has to stay
  non-deferred, and a deferred tool cannot carry `cache_control`.
- When the agent would call many tools in sequence and pipe results between them, consider
  **programmatic tool calling**: Claude orchestrates your tools from inside code execution, so
  intermediate results never enter context. It does not combine with strict tools, with disabling
  parallel tool use, or with forcing a specific tool.

Role-scoping still matters, for a different reason: a synthesis agent holding a search tool will
research instead of synthesize. Scope by capability boundary; size by these thresholds.

## 7. Set `tool_choice` deliberately

| Value | Semantics | Use for |
| --- | --- | --- |
| `auto` | Claude decides whether and which to call; default when tools are present | General operation |
| `any` | Must call one of the tools | Guaranteeing a call among several schemas, where supported |
| `{type: "tool", name: "X"}` | Forces that exact tool | A mandatory first step, where supported |
| `none` | No tool use; default when no tools | A turn that must be prose |

Forced choice (`any` or a named tool) is model- and setting-dependent. Manual extended thinking
rejects it, and some current models reject it outright with a 400. Check the model's docs before
relying on it; the portable default is `auto` plus `strict: true` on the tools for guaranteed-valid
inputs, or structured outputs when you need a fixed JSON answer. Where forced choice works, the API
prefills the assistant turn, so the model emits no prose before the call; use `auto` on a turn that
also needs narration.

`strict: true` gives grammar-constrained sampling over the tool name and input. Reserve it for tools
where a schema violation does real damage, because strict schemas share a per-request complexity
budget (owned by output-contracts). Changing `tool_choice` also affects prompt caching; see
context-economy.

## Audit checklist

- [ ] Every description runs three or more sentences and states when *not* to use the tool.
- [ ] Every pair of confusable tools has a boundary sentence pointing at the other.
- [ ] Parameter names are unambiguous; complex inputs carry examples.
- [ ] Names are namespaced by service, consistently prefix- or suffix-style.
- [ ] No tool exists purely because an endpoint exists; chains the agent always performs have been
      collapsed.
- [ ] No tool returns unbounded results; there is a token ceiling and a pagination default.
- [ ] Responses carry no fields the agent cannot use (mime types, ACL hashes, shard numbers, epoch
      millis).
- [ ] A `response_format` (or equivalent) lets the agent ask for less.
- [ ] Every error names the defect and shows a correct example.
- [ ] Tool count under 10 uses plain calling; 10+ or heavy definitions use deferred loading with
      three to five hot tools resident.
- [ ] Forced `tool_choice` appears only on a model documented to support it, and never on a turn
      that also needs prose.
- [ ] Strict schemas are scoped to high-stakes tools.

## When reviewing code

Without a checkout, review pasted tool definitions the same way. Report findings ranked by impact:

```text
<file>:<line> — rule <n> (<rule name>) — <fix in one sentence> — impact: high|medium|low
```

`high` = misrouting between confusable tools, unbounded responses, or forced `tool_choice` on a
model that rejects it; `medium` = thin descriptions, opaque errors, missing namespacing; `low` =
response fields the agent cannot use. If nothing violates a rule, say so and list the checklist
items you confirmed.

**Verify:** after fixes, re-run the audit checklist, and send one request per changed tool to
confirm the API accepts the definitions.

## Patterns that hold up

<example>
Descriptions with explicit boundaries.

```text
get_customer:
  "Look up a single customer by email address, phone number, or customer ID (format C-NNNN).
   Returns the profile: legal name, contact details, account status, loyalty tier, and account
   creation date. Use this to verify identity before any account-affecting action, and to
   resolve a human-supplied identifier into a customer ID for other tools. Returns at most one
   record; if the identifier is ambiguous it returns all candidate matches with ambiguous: true
   and takes no action. Does not return orders, transactions, or support history. For order
   questions, use lookup_order."

lookup_order:
  "Retrieve one order by order number (#NNNNN) or carrier tracking ID. Returns status, line
   items, shipping and delivery events, and refund eligibility with the reason when ineligible.
   Use when the user references a specific order or shipment. Does not return customer profile
   data and cannot search by customer; resolve identity with get_customer first. To list a
   customer's orders, use list_customer_orders."
```

Purpose, triggers, negative triggers, the ambiguity contract, and the deliberate omissions are all
present, so misrouting becomes structurally unlikely rather than probabilistically discouraged.
</example>

<example>
A consolidated tool replacing a chain.

```python
@tool   # your SDK's tool decorator; the docstring becomes the description
async def get_customer_context(customer_id: str, response_format: str = "concise") -> str:
    """Compile everything needed to act on a customer in one call: profile, the five most recent
    orders, open support tickets, lifetime value, and refund history for the last 12 months.
    Use at the start of any customer-facing task instead of chaining get_customer,
    list_transactions, and list_notes. response_format "concise" omits internal IDs and
    timestamps; "detailed" includes the IDs required to call process_refund or
    update_subscription. Does not include payment instrument details."""
```
</example>

<example>
Errors and empty results the agent can act on.

```json
// validation failure: teaches the correct call
{ "is_error": true,
  "content": [{ "type": "text", "text":
    "Invalid `order_id`: expected '#NNNNN' (5 digits), got 'last one'. Resolve the reference to a concrete order first: call list_customer_orders(customer_id) and pick from the result. Example: {\"order_id\": \"#88912\"}" }] }

// business rule: retrying cannot help (convention fields live inside the text payload)
{ "is_error": true,
  "content": [{ "type": "text", "text":
    "{\"errorCategory\": \"business\", \"isRetryable\": false, \"message\": \"Refund of 750.00 GBP exceeds the 500.00 GBP auto-approval limit. Escalate for manager approval via create_approval_request; retrying this call will fail the same way.\"}" }] }

// queried successfully, nothing matched: not an error
{ "is_error": false,
  "content": [{ "type": "text", "text":
    "resultCount: 0. No customer matched that address. The directory was reachable and the query completed; there is no such record. Ask the user for an alternate identifier." }] }
```
</example>

A deferred-loading configuration with a hot set kept resident is in
[references/api-mechanics.md](references/api-mechanics.md).

## Failure modes

**Minimal descriptions, then a classifier to compensate.** `get_customer: "Retrieves customer
information"` next to `lookup_order: "Retrieves order details"` never tells the model the boundary,
so it guesses. A routing model in front buys latency, infrastructure, and a second thing to keep in
sync; few-shot examples add tokens to every request; merging the tools destroys the distinction.
Expand the descriptions first, then check the system prompt for keyword-sensitive instructions
overriding them.

**One tool per endpoint.** `list_contacts` returning 4,000 records, unpaginated `list_orders`, and a
`get_note` / `get_note_tags` / `get_note_author` / `get_note_attachments` quartet. That is the
endpoint's shape, not the workflow's, and the agent burns its window reading records to find one.

**Raw payloads full of fields the agent cannot use.**

```json
{ "results": [{ "id": "a3f9c1e8-4b2d-4f77-9c21-d8e0ab5512ff",
  "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "thumb_256_url": "https://cdn/...", "acl_hash": "9f2b...", "shard": 14,
  "created_ts_ms": 1738291200123, "title": "Q3 plan" }] }
```

Most of these tokens are unusable. Return `{"title": "Q3 plan", "file_type": "docx", "modified":
"2026-01-31"}` in concise mode, and include the `id` only in detailed mode or when a follow-up call
needs it.

**Piling on tools, or deferring all of them.** Eighteen resident un-namespaced tools on one agent
sits below the degradation band but wastes prefix tokens on every request and mixes roles, so the
agent reaches for off-role tools. Deferring every tool is an API error.

**Forcing a tool on a model or turn that cannot take it, or strictness everywhere.** On a model that
rejects forced choice the request fails outright; where it works, the prefill suppresses the
explanation you wanted. Blanket strictness exhausts the strict-schema budget and adds grammar
compilation latency on every schema change.
