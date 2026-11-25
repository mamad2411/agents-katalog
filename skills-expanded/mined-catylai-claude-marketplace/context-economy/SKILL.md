---
name: context-economy
description: "Cuts an agent's token cost and attention load. Use when cache hit rates are near zero, cost or latency per task is high, the window fills up, or a long session loses specifics. Covers cache-friendly prompt ordering, trimming tool results before they enter history, pinning transactional facts against summarization, and routing bulk work to batch. Not for loop control (use agentic-loop-control); not for subagent structure or resume-vs-fresh (use agent-orchestration); not for tool-count thresholds (use tool-interface-design)."
license: MIT
---

# Context economy

Context is the scarcest resource an agent has and the most commonly wasted. Two budgets are in
play: **attention**, what the model can reason about well, and **money**, what you are billed. Most
rules here improve both. Where they conflict, attention wins.

Structural fixes come before bigger windows. A larger window does not repair diluted attention.

This skill owns prompt-cache layout and invalidation, trimming at the tool boundary (including
Claude Code's MCP output limits), pinned facts, context editing and compaction, and batch routing.
Prices, per-model cache minimums, beta identifiers, and batch limits are in
[references/api-mechanics.md](references/api-mechanics.md). Porting notes are in
[references/porting.md](references/porting.md).

## 1. Aim for the smallest set of high-signal tokens

That is the design target, and it is not the same as "include everything relevant." Four
techniques carry most of the weight:

- **Right-altitude system prompts:** specific enough to guide behavior, flexible enough to read as
  strong heuristics rather than a brittle script.
- **Just-in-time retrieval over pre-loading:** let the agent navigate to what it needs via file
  structure, search, and targeted reads rather than stuffing candidate context in up front.
- **Structured note-taking:** persist findings outside the window and read them back (the
  scratchpad pattern is owned by agent-orchestration).
- **Subagent isolation and deliberate compaction:** push verbose investigation into a separate
  window that returns a summary, and prune on purpose rather than letting the window fill.

## 2. Lay the prompt out for the cache, then place the breakpoint

Mechanics to design around:

- The marker is `cache_control: {"type": "ephemeral"}` on a content block, with an optional
  one-hour `ttl` instead of the five-minute default.
- A request can carry at most four breakpoints.
- The minimum cacheable prefix is **model-specific**. Look it up for the model you ship, because a
  prefix under the threshold silently fails to cache, and that is the most common cause of a zero
  hit rate.
- A cache write costs more than base input and a read costs a small fraction of it, with the
  one-hour write costing more than the five-minute one. Choose the one-hour TTL only where a second
  hit inside the hour is likely.
- Prefix order is fixed: tools, then system, then messages. A change anywhere invalidates everything
  from that point onward.

So: constant content first (tool definitions, system instructions, long reference documents), then
the breakpoint at the end of the static block, then volatile content. Anything dynamic placed before
the static prefix (a timestamp, a session ID, a reordered tool list) breaks every cache hit for
every request.

Non-obvious invalidators: changing `tool_choice` or adding or removing images invalidates the
cached message blocks while tools and system survive; changing thinking or effort settings
invalidates message blocks and, on some models, more; changing the structured-output format
invalidates that conversation's cache.

## 3. Trim tool results before they enter history

A tool result is written into the conversation once and then re-sent on every subsequent request.
A 9,000-token response you needed four fields from costs you those 9,000 tokens for the rest of the
session.

Trim at the boundary, in one place for every caller: in your tool wrapper for an API agent, or in a
Claude Code `PostToolUse` hook that returns `updatedToolOutput` (hook mechanics are owned by
deterministic-enforcement). Claude Code warns on large MCP tool output and caps it by default; raise
the cap with `MAX_MCP_OUTPUT_TOKENS` only after trimming, and keep your own ceiling for tools the
cap does not govern. Have upstream agents return structured data (facts, citations, scores) rather
than verbose reasoning.

## 4. Pin transactional facts in a never-summarized block

Extract amounts, dates, order numbers, IDs, and statuses into a structured block included in every
prompt, and exclude it from summarization. In a multi-issue session, give each issue its own entry.

Progressive summarization is the wrong tool for transactional data. It deletes precisely the values
the agent needs to act, and it does so silently. Summarize narrative; pin facts.

## 5. Put key findings at the top of long inputs

Models under-weight the middle of long inputs. Any aggregated input leads with a key-findings
summary and uses explicit section headers below it. The same applies to a SKILL.md or a reference
file: the most important instruction goes near the top, because truncation takes the tail.

## 6. Use the platform's context controls rather than improvising

- **Server-side compaction** is the API docs' primary strategy for long-running conversations: it
  summarizes history for you. Reach for context editing when you need finer control over what is
  cleared.
- **Context editing** (an API beta) is configured with a `context_management` parameter carrying an
  `edits` array. The tool-result clearing edit clears the *oldest* tool results first, replacing
  them with a placeholder while preserving message structure and, by default, the tool call inputs.
  It takes a trigger threshold, a minimum amount to clear, a count of recent results to keep, and a
  list of tools to exclude. A second edit type clears thinking blocks. Clearing invalidates cached
  prefixes containing what it cleared, so pair it with a stable static prefix. A working call is in
  [references/api-mechanics.md](references/api-mechanics.md).
- **Auto-compaction** in Claude Code and the Agent SDK clears older tool outputs first, then
  summarizes. `PreCompact` / `PostCompact` hooks let you snapshot or re-inject state around it, and
  you can instruct what to preserve, for example the full list of modified files.
- **Compact or clear?** Compact when the thread is still on-task and you want continuity. Clear when
  switching tasks inside one session. When files on disk changed or the agent has lost its grip on
  specifics, start fresh with summary injection; that decision and its degradation tell are owned
  by agent-orchestration.

## 7. Keep token-heavy orchestration out of the window

Deferred tool loading and programmatic tool calling both keep volume out of context; when to use
them is owned by tool-interface-design.

A bigger window is the last option, not the first. Very large windows are real and usable, with a
price change above a documented threshold, but reach for them after the structural fixes and never
as a repair for diluted attention.

## 8. Route by latency tolerance

**Synchronous** for anything where a human or a pipeline is waiting: pre-merge CI, interactive
review, live support.

**The Message Batches API** for latency-tolerant volume: overnight reports, weekly audits, bulk
extraction. It is discounted against synchronous pricing, latency runs up to the batch window
(figures in [references/api-mechanics.md](references/api-mechanics.md)), result order is not
guaranteed (correlate by `custom_id`), and it does not stream. A batch item supports the same
features as a synchronous request, including tool use, server tools, multi-turn, thinking, and
structured outputs. A result that comes back with `pause_turn` is unfinished: continue it with the
paused content in a follow-up request. A client `tool_use` stop needs a new request, so genuinely
interactive client-tool loops belong on the synchronous API. Limits are in
[references/api-mechanics.md](references/api-mechanics.md).

Refine the prompt on a five-to-ten item sample first, then submit the full batch; resubmit only
failures by `custom_id`, modified (chunk oversized inputs, add format examples). Work SLAs backward
from the maximum processing window. Prompt caching applies in batches, and the one-hour TTL is often
the right choice there.

## Audit checklist

- [ ] Check cache-read token counts on a live request. Near zero on repeat calls means dynamic
      content is sitting before the static prefix.
- [ ] Nothing volatile (timestamp, session id, user name, reordered tools) sits above the last
      breakpoint.
- [ ] No more than four breakpoints, and the static prefix clears *your model's* minimum.
- [ ] TTL is chosen deliberately; one hour only where a second hit within the hour is likely.
- [ ] No tool result enters history untrimmed; you know the largest one in tokens.
- [ ] Transactional facts survive summarization and compaction verbatim.
- [ ] In long aggregated inputs, critical findings are in the first screen.
- [ ] Context editing or an auto-compaction window is configured rather than left to fill up.
- [ ] No latency-tolerant bulk workload runs synchronously at full price, and no blocking workload
      runs through batch.
- [ ] Batch results are correlated by `custom_id`, and paused results are continued.
- [ ] The batch prompt was validated on a small sample first.

## When reviewing code

Without a checkout, review pasted request-building code, hooks, and usage numbers the same way.
Report findings ranked by impact:

```text
<file>:<line> — rule <n> (<rule name>) — <fix in one sentence> — impact: high|medium|low
```

`high` = dynamic content before the cached prefix, untrimmed large tool results, or summarized
transactional facts; `medium` = unconfigured compaction, blocking work on batch, bulk work
synchronous; `low` = TTL choice or key-findings placement. If nothing violates a rule, say so and
list the checklist items you confirmed.

**Verify:** after fixes, send two identical requests and confirm the second reports non-zero cache
read tokens in `usage`.

## Patterns that hold up

<example>
Cache-friendly ordering with the breakpoint at the static boundary.

```python
response = client.messages.create(
    model=MODEL,
    max_tokens=4096,
    tools=TOOLS,                                  # stable: same order, same content, every call
    system=[
        {"type": "text", "text": SYSTEM_INSTRUCTIONS},
        {"type": "text", "text": POLICY_HANDBOOK,
         "cache_control": {"type": "ephemeral", "ttl": "1h"}},   # ends the static block
    ],
    messages=[*history, {"role": "user", "content": latest_turn}],   # volatile, after the prefix
)
```

Everything above the breakpoint is byte-identical across requests, so every call after the first
reads cheaply, and the one-hour TTL survives a slow human in the loop.
</example>

<example>
A case-facts block that is never summarized.

```json
{ "caseFactsBlock": {
  "customerId": "C-4421",
  "issues": [
    { "id": "I-1", "orderId": "#8891", "orderDate": "2026-03-03",
      "chargeCount": 3, "refundAmount": "247.83 GBP", "status": "pending_refund" },
    { "id": "I-2", "orderId": "#8903", "orderDate": "2026-03-09",
      "issue": "wrong_size_shipped", "status": "replacement_offered" } ] } }
```

Injected verbatim into every prompt and excluded from any summarization instruction. After four
rounds of summarization the narrative may degrade freely, but the agent still knows it owes 247.83
on order #8891 rather than "roughly two hundred."
</example>

<example>
Trimming at the tool boundary, once, as a Claude Code `PostToolUse` command hook registered with
the matcher `mcp__tickets__search_tickets`.

```js
#!/usr/bin/env node
// Reads the hook input as JSON on stdin; prints the replacement on stdout.
const input = JSON.parse(require("fs").readFileSync(0, "utf8"));

// tool_response is an object, not a string. MCP results usually carry the payload
// as JSON text inside content blocks, so unwrap that when present.
const raw = input.tool_response;
const blocks = Array.isArray(raw) ? raw : raw && raw.content;
const text = Array.isArray(blocks) ? (blocks.find(b => b.type === "text") || {}).text : undefined;
const r = text ? JSON.parse(text) : raw;
if (!r || !Array.isArray(r.results)) process.exit(0);   // unexpected shape: leave output as-is

const trimmed = {
  total: r.total_count,
  returned: Math.min(r.results.length, 10),
  tickets: r.results.slice(0, 10).map(t => ({
    id: t.id, subject: t.subject, status: t.status,
    updated: new Date(t.updated_at).toISOString().slice(0, 10),
  })),
  hint: r.total_count > 10
    ? `10 of ${r.total_count} shown. Narrow with status= or updated_after= rather than paging.`
    : undefined,
};

process.stdout.write(JSON.stringify({
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    // MCP output is passed through without schema validation; keep it as text content.
    updatedToolOutput: [{ type: "text", text: JSON.stringify(trimmed) }],
  },
}));
```

A 9,400-token payload becomes about 120 usable tokens, and the saving compounds because the trimmed
result is re-sent on every later request. For a built-in tool, the replacement has to match that
tool's output shape or Claude Code ignores it.
</example>

<example>
Key findings first.

```markdown
# Key findings (read first)
1. Refund path has no idempotency key -> duplicate charges possible (src/refund.ts:74), severity high
2. Session IDs generated from Math.random() (src/session.ts:88), severity high
3. 11 lower-severity findings, listed under "All findings" below

## Scope and method
## All findings
## Files reviewed
```

The two things that must not be missed sit in the first sixty tokens, above the region where
attention thins and above any truncation point.
</example>

## Failure modes

**Dynamic content before the static prefix.**

```python
system=[
    {"type": "text", "text": f"Current time: {datetime.now()}. Session: {uuid4()}"},   # breaks every hit
    {"type": "text", "text": LONG_POLICY_DOC, "cache_control": {"type": "ephemeral"}},
]
```

The first block changes on every request, so the cached prefix never matches and you pay the write
premium for a cache you never read. This is the most common caching bug, and it is invisible unless
you inspect cache-read token counts.

**Progressive summarization of transactional data.** Round one: "Customer C-4421 charged three
times 247.83 on order #8891, refund pending." Round four: "Customer has a billing issue involving
duplicate charges that is being resolved." The agent can no longer issue the refund, so it either
asks the customer to repeat themselves or confabulates a figure.

**Raw payloads into history, then a bigger window as the fix.** The cost is per request for the rest
of the session, so a handful of fat results dominates the bill and dilutes attention. A bigger
window makes the same waste affordable for longer.

**Pre-loading everything "so the agent has it."** Reading 340 files into one message inverts
just-in-time retrieval: the model must locate signal inside a huge low-signal block, exactly where
middle-of-input under-weighting bites, and you pay for all 340 whether or not two mattered.

**Blocking work moved to batch for the discount.** Batch has no latency SLA. The discount is
irrelevant next to a blocked merge queue.

**Assuming batch cannot do tools or multi-turn, or skipping the sample.** Teams either skip a
legitimate saving on a false premise, or submit 5,000 unsampled prompts and receive 5,000
identically malformed results. Ignoring a paused result silently truncates the work.
