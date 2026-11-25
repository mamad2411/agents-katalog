---
name: agentic-loop-control
description: "Sets the control-flow rules for an agent loop: when it stops, when it continues, and how it fails. Use when writing or reviewing a Messages API loop, when an agent stops early, loops forever, or repeats the same tool call, or when deciding how a tool failure reaches the caller. Not for subagent design (use agent-orchestration); not for tool schemas or error payload shape (use tool-interface-design)."
license: MIT
---

# Agentic loop control

The loop is the one part of an agent that must be fully deterministic. Nearly every loop bug
traces to the same root cause: something the control flow should have decided was left to the
model's prose instead.

Fix the loop before anything else. A perfectly described tool inside a loop that mis-detects
completion is still a broken agent.

SDK method names, Agent SDK result fields, and the full `stop_reason` reference are in
[references/api-mechanics.md](references/api-mechanics.md). Porting notes for other frameworks are
in [references/porting.md](references/porting.md).

## 1. Decide completion from `stop_reason` alone

`stop_reason` is the only completion signal the API gives you. Treat `end_turn` as finished and
every other value as "not finished; find out why."

| `stop_reason` | What happened | What to do |
| --- | --- | --- |
| `end_turn` | Model finished on its own | Return. |
| `tool_use` | The turn contains `tool_use` blocks | Execute, append results, iterate. |
| `max_tokens` | Output truncated, possibly mid-`tool_use` with partial JSON | Raise the limit and retry, or repair the partial input. Parse tool input only from a complete turn. |
| `model_context_window_exceeded` | The response filled the context window | Treat as truncated; compact, trim, or escalate, because the same request cannot succeed. |
| `pause_turn` | A server-tool loop checkpointed | Send the paused assistant content back verbatim to continue. |
| `refusal` | Safety decline; `stop_details` names the category | Fall back to another model or escalate; the same request on the same model will refuse again. |
| `stop_sequence` | A configured stop sequence matched | Handle per your own protocol. |

Under structured output, `refusal` and `max_tokens` can both return a payload that violates your
schema. Schema guarantees hold only for a turn that ended normally.

## 2. Append both halves of every tool exchange

The Messages API is stateless: each request carries the whole conversation. A tool result that
never reaches `messages` is one the model cannot reason about, and the symptom is an agent that
calls the same tool over and over.

Append the assistant turn carrying the `tool_use` blocks **and** the user turn carrying one
`tool_result` per `tool_use_id`, in order, before the next request.

## 3. Take the highest rung of the loop ladder that works

1. **The SDK's tool runner.** It runs your tools, formats results, and iterates until the model
   stops calling tools. The default for ordinary agentic work.
2. **A server-hosted managed agent.** Anthropic runs the loop and a sandbox and persists event
   history. For long-running autonomous work you would rather not host.
3. **A hand-written `while` loop.** Only when you need something the managed loop will not do:
   human approval gates, conditional execution, custom batching, per-iteration policy checks,
   bespoke telemetry.

Hand-writing rung 3 when rung 1 would do is the most common piece of avoidable agent code, and it
is where rules 1 and 2 get broken.

## 4. Caps bound blast radius; they do not decide completion

Turn caps, iteration caps, and budget caps are circuit breakers. In the Agent SDK, a run stopped by
a cap reports an `error_*` result subtype. Log it and surface it as an incident, because returning
it as success hides the fact that the work is unfinished. An agent that routinely ends on the cap
has a decomposition problem, not a cap problem.

Keep the iteration counter as a backstop and let `stop_reason` decide completion.

## 5. Retry with the defect named, or escalate

This skill owns the retry boundary; other agent-craft skills point here.

A retry that does not tell the model what was wrong reproduces the same failure at full cost.
A retry payload carries three things: the original input, the output that failed, and the specific
validation error.

Retries fix format mismatches, misplaced values, and skipped arithmetic. They cannot conjure
information that is not in the source. For missing data, return `null` where the schema allows it,
or route to a human, because retrying for absent data is how fabrication enters a pipeline.

Categorize first:

| Category | Retryable | Action |
| --- | --- | --- |
| Transient: timeout, 5xx, rate limit | Yes, as-is | Backoff and retry |
| Validation: bad input shape | Yes, after fixing | Retry with the error text included |
| Business: policy limit, ineligible | No | Alternative path or escalation |
| Permission: wrong principal | No | Different credential or escalation |

## 6. Propagate failure with structure

This skill owns "empty is not unreachable"; tool-interface-design owns the error flag fields
(`is_error` / `isError`) that carry it.

Two catastrophic patterns:

- **Silent suppression.** An empty result marked success. The caller believes the operation ran
  and found nothing, so coverage gaps become invisible.
- **Whole-run abort.** One source fails and the run dies, discarding work that already succeeded
  and already cost money.

Attempt local recovery for transient failures, then propagate a structured partial result carrying
the failure category, what was attempted, any partial results, and suggested alternatives. Make a
valid empty result *structurally different* from an access failure: "the query ran and matched
nothing" is a success; "the source was unreachable" is not.

## Audit checklist

- [ ] Exactly one place decides the agent is done, and it reads `stop_reason`.
- [ ] Grep for `content[0]`, `.text.includes(`, `"DONE"`, `TASK_COMPLETE` in control flow; each
      hit is a rule 1 violation.
- [ ] `pause_turn`, `max_tokens`, `model_context_window_exceeded`, and `refusal` are each handled
      by name, and an unknown value raises rather than falling through to `break`.
- [ ] Every `tool_use` gets a matching `tool_result`, in order, before the next request.
- [ ] If the loop is hand-written, you can name the specific interception that justifies it.
- [ ] Hitting a cap logs and escalates rather than returning a normal-looking result.
- [ ] Retries carry the validation error text, and no retry path exists for missing source data.
- [ ] A caller can tell `results: []` (no match) from `results: []` (source down).
- [ ] One tool failure does not abort the run and discard completed work.

## When reviewing code

Without a checkout, review pasted loop code the same way. Report findings ranked by impact:

```text
<file>:<line> — rule <n> (<rule name>) — <fix in one sentence> — impact: high|medium|low
```

`high` = wrong completion, lost tool results, or silent failure; `medium` = a missing named
`stop_reason` branch or a retry without error context; `low` = a hand-written loop the tool runner
could replace. If nothing violates a rule, say so and list the checklist items you confirmed.

**Verify:** after fixes, re-run the audit checklist against the changed code.

## Patterns that hold up

<example>
Every exit named.

```js
while (true) {
  const res = await client.messages.create({ model, max_tokens, messages, tools });

  if (res.stop_reason === "end_turn") return res;

  if (res.stop_reason === "tool_use") {
    const toolResults = await runTools(res);          // one per tool_use_id
    messages.push({ role: "assistant", content: res.content });
    messages.push({ role: "user", content: toolResults });
    continue;
  }

  if (res.stop_reason === "pause_turn") {
    messages.push({ role: "assistant", content: res.content });  // verbatim
    continue;
  }

  if (res.stop_reason === "max_tokens") throw new TruncatedTurn(res);
  if (res.stop_reason === "model_context_window_exceeded") throw new ContextExhausted(res);
  if (res.stop_reason === "refusal") return escalate(res);
  throw new UnhandledStopReason(res.stop_reason);
}
```

The final `throw` is the point of the shape: a `stop_reason` shipped after you wrote this lands
somewhere loud instead of being silently read as completion.
</example>

<example>
A retry aimed at the actual defect.

```js
const retry = [{ role: "user", content:
  `Original document:\n${doc}\n\n` +
  `Your extraction:\n${JSON.stringify(failed)}\n\n` +
  `Validation error: line items sum to 450.00 but stated_total is 500.00. ` +
  `Re-extract every line item, including any on page 2.` }];
```

The model now knows which invariant broke and where to look, unlike "that was wrong, try again,"
which changes nothing about its information state.
</example>

<example>
A partial failure the caller can act on.

```json
{
  "status": "partial_failure",
  "errorCategory": "transient",
  "isRetryable": true,
  "attemptedAction": { "tool": "search_academic_db", "query": "grid storage policy", "dateRange": "2022-2024" },
  "partialResults": [{ "title": "Grid Storage Directive 2023", "source": "public register" }],
  "alternativeApproaches": ["Narrow to 2023-2024", "Try government_publications", "Use cached results"]
}
```

These field names are a convention for the inside of your result payload, not part of the Claude
API or MCP specification.
</example>

## Failure modes

**Text presence read as completion.**

```js
if (res.content[0].type === "text") return res;     // broken
```

A model can emit text alongside `tool_use` in the same turn. This returns mid-task with tools
unexecuted, and it fails intermittently, depending on whether the model narrated before calling.

**A loop bounded only by a counter.**

```python
for _ in range(10):
    res = call_model(messages)
    messages.append(res)        # tool results never appended
```

Two defects compounding: completion decided by exhaustion, and results that never reach the model,
so it re-requests the same tools until the counter runs out. It reads as "the model is dumb"; it is
actually rule 2.

**`pause_turn` treated as an error, or rewritten.** Aborting discards completed work. Summarizing
the paused content breaks the continuation contract. Append it verbatim.

**Retry with no error context.** Identical inputs produce a near-identical failure: three attempts
for 3x the cost and no new information. If the data is genuinely absent, the extra attempts
pressure the model to invent it.

**Empty marked success.** `{ "results": [], "status": "success" }` makes a source outage
indistinguishable from "nothing matched," so the caller reports a gap as a finding.
