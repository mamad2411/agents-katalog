---
name: agent-orchestration
description: "Designs and reviews coordinator/subagent systems. Use when building or reviewing a multi-agent workflow, when output has topic-shaped gaps or uneven depth, or when choosing resume vs fork vs a fresh session after files changed. Covers whether delegation pays for itself, splitting work so coverage is complete, and passing context across isolated windows. Not for the message loop (use agentic-loop-control); not for caching or compaction (use context-economy)."
license: MIT
---

# Agent orchestration

Multi-agent systems cost several times the tokens of a single agent, which in turn costs several
times a chat turn (Anthropic's published figures are in
[references/platform-limits.md](references/platform-limits.md)). Earn that multiplier or do not
pay it.

Keep one diagnostic habit above all others: decomposition failures masquerade as subagent
failures. When the output is wrong, trace back to where the work was split before you change
anything downstream.

Porting notes for other frameworks are in [references/porting.md](references/porting.md).

## 1. Delegate for breadth or isolation, not for sophistication

Spawn subagents when the work is genuinely parallel across independent subtasks (breadth-first
research, per-file review, multi-source gathering), or when verbose investigation would otherwise
flood the coordinator's window.

Keep the work in one agent when:

- the task is single and focused, so the overhead buys nothing;
- the work depends on deep shared context, since rebuilding it inside each isolated window costs
  more than the fan-out saves;
- latency matters more than throughput.

One agent with good tools beats a multi-agent system on most tasks. Reach for delegation only
when you can say the independent subtasks out loud.

## 2. Hub and spoke

One coordinator decomposes the task, selects subagents, passes context, aggregates results, and
owns error handling. Route all inter-agent information through it: that is what buys
observability, uniform error handling, and controlled context flow.

Claude Code lets a subagent spawn its own subagents down to a configurable depth
(`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`); at the limit the spawn tool is withheld and the subagent
does the work itself. Keep any tree shallow and explicit, and route cross-branch information
through a parent.

Keep subagents from talking to each other directly, because the coordinator is the only vantage
point from which a coverage gap is visible.

## 3. Decomposition owns coverage

Missing scope, where whole topics are absent from the output, is almost always the coordinator's
split. It is not the subagents, not the search queries, not the agent count.

```text
Good:  "impact of AI on creative industries" -> [visual arts, music, writing, film, games]
Bad:   "impact of AI on creative industries" -> [visual arts]
```

Run iterative refinement: evaluate the synthesis for gaps and re-delegate until coverage is
sufficient. A single-pass fan-out has no mechanism for noticing what it never asked about.

## 4. Descriptions are for selection; prompts are for goals

The `description` is the selection mechanism. Claude matches the request against every available
agent's description, so it says what the agent does **and when to invoke it**, including when not
to. Vague descriptions cause silent misrouting that reads like a capability gap.

The subagent's prompt is its system prompt: scope it to the role and restrict `tools` to match.
Coordinator prompts specify goals rather than procedures, because subagents choose their own path
and over-specified steps waste tokens and suppress better strategies.

For the exact agent-definition fields, read the Claude Code sub-agents docs or the Agent SDK
reference rather than a copy here.

## 5. The prompt is the only channel in; the final message is the only channel out

The only content that crosses from parent to subagent is the spawn prompt, and the only thing that
comes back is the subagent's final message. The subagent does not see the parent's conversation,
the files the parent read, or any prior subagent's results. It does get its own system prompt, tool
definitions, and project-level configuration, none of which carry your task context. A fork-style
subagent is the exception; it inherits the parent conversation by design.

Therefore:

- Pass every fact the subagent needs, in full, in the prompt, because it cannot look up prior
  results.
- Pass findings as structured data that keeps content and source metadata together. Content
  stripped of its metadata is what produces unsourced synthesis downstream; the defect lives in
  the context passing, not in the synthesis agent.
- Use the filesystem as the other honest channel: have one subagent write a report to a path and
  tell the next to read that path.

Spawning is gated by the agent's own `tools` list. Omit the spawn tool from `tools` and the agent
cannot delegate. A pre-approval list only suppresses permission prompts, so adding the spawn tool
there grants nothing the agent did not already have.

## 6. Parallelize independent work; pick the session strategy by what changed

This skill owns the resume-vs-fresh decision; context-economy points here.

Issue independent spawns together rather than one per turn, because sequential spawns serialize
latency for no benefit. Claude Code caps concurrent subagents per session; raise or lower the cap
with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, and expect a spawn over the cap to fail rather than
queue. Read-only work parallelizes cleanly; keep stateful work (writes, edits, shell) against the
same files sequential.

| Situation | Use |
| --- | --- |
| Continuing work, files unchanged | Resume the session |
| Comparing alternatives from one baseline | Fork the session |
| Rewinding to a specific earlier point | Resume at that message |
| **Files changed, or context degraded** | **Fresh session plus summary injection** |

After files change, resuming is a trap: stale tool results stay in history and keep biasing
reasoning, so the agent recommends fixes already applied and cites deleted code. Start fresh,
inject a structured summary of prior findings, name the changed files, and re-analyze only those.

## 7. Fix uneven depth with structure, not with a bigger window

The symptom: thorough on early items, shallow on later ones; a pattern flagged in one file and
ignored in the next. That is attention dilution, and it is structural. The fix is a multi-pass
architecture: one focused pass per item, then a separate cross-item integration pass for data
flow, consistency, and contradictions. A larger window gives the same diluted attention more room.

Match the decomposition pattern to the task:

- **Fixed sequential pipeline** for predictable structured work: multi-file review, document
  processing, extraction, compliance checks. Consistent and debuggable.
- **Dynamic adaptive decomposition** for open-ended work of unknown scope: legacy exploration,
  security audits, research, debugging unfamiliar systems. The plan evolves as you learn.

Choosing the dynamic pattern for predictable work is the most common over-engineering here.

## 8. Review with a fresh instance; explore with a scratchpad

This skill owns the scratchpad pattern and the context-degradation tell; context-economy points
here.

A separate instance with no prior reasoning context will challenge decisions the generating
session would defend. Asking the same session to "now review your code" retains generation bias
and mostly produces ratification.

For extended exploration, keep a scratchpad file from the start. Write concrete findings (classes,
paths, dependency chains, coverage) and read it back instead of relying on conversation context.
Delegate verbose investigation to subagents that return structured summaries, inject phase-1
summaries into phase-2 prompts, compact proactively, and persist a crash-recovery manifest:
explored paths, key findings, current phase, next steps.

The tell for context degradation is the agent saying "this follows the typical pattern" instead of
naming the concrete class or method it found earlier.

## Audit checklist

- [ ] You can name the independent subtasks that justify the token multiplier.
- [ ] Every subagent description says when to use it and when not to.
- [ ] The coordinator's `tools` list actually includes the spawn tool.
- [ ] Subagent `tools` are scoped to the role rather than everything.
- [ ] No subagent prompt references information the subagent was never given ("the findings
      above", "as established earlier", "the file you read").
- [ ] Findings crossing an agent boundary carry source metadata.
- [ ] Independent spawns are issued together, not one per turn.
- [ ] No code path resumes a session after files on disk changed.
- [ ] Multi-item work has one pass per item plus a separate integration pass.
- [ ] Generated output is reviewed by a fresh instance.
- [ ] Long explorations keep a scratchpad and read it back.
- [ ] When output has a coverage gap, debugging starts at the decomposition.

## When reviewing code

Without a checkout, review pasted agent definitions and orchestration code the same way. Report
findings ranked by impact:

```text
<file>:<line> — rule <n> (<rule name>) — <fix in one sentence> — impact: high|medium|low
```

`high` = missing coverage, context the subagent never receives, or resume after files changed;
`medium` = vague descriptions, over-broad `tools`, sequential spawns; `low` = a missing scratchpad
or a same-session review. If nothing violates a rule, say so and list the checklist items you
confirmed.

**Verify:** after fixes, re-run the audit checklist against the changed definitions.

## Patterns that hold up

<example>
Role-scoped subagents with disambiguating descriptions.

```ts
const agents = {
  "source-gatherer": {
    description:
      "Gathers primary sources on one narrow subtopic and returns findings with full " +
      "provenance (url, document name, page, excerpt, retrieval date). Invoke once per " +
      "subtopic, in parallel. Not for synthesis or cross-source reconciliation.",
    prompt: SOURCE_GATHERER_PROMPT,
    tools: ["WebSearch", "WebFetch", "Write"],
  },
  synthesizer: {
    description:
      "Merges gathered findings into a cited report, preserving every claim-to-source " +
      "mapping and annotating conflicts rather than resolving them. Invoke once, after " +
      "all gathering completes. Not for fetching new sources.",
    prompt: SYNTHESIZER_PROMPT,
    tools: ["Read", "Write"],          // deliberately no search tool
  },
};
```

Each description says what, when, and when-not, so selection is decided by the roster rather than
by luck. Tool scoping makes the synthesizer structurally incapable of quietly re-researching
instead of synthesizing.
</example>

<example>
A spawn prompt that assumes nothing shared.

```text
Subtopic: AI in music production.
Scope: 2023-2026 only. Exclude consumer music generation.
Output: JSON array of findings, each with claim, source_url, document_name,
  page_number (if paginated), excerpt, publication_date, confidence.
Write the array to ./research/music.json and return only a five-line summary.
Context you need: this report frames "creative industries" as professional practice,
  not hobbyist tooling. An earlier phase established that "generative" is ambiguous here;
  always disambiguate to "generative composition" or "generative mastering".
```

Scope, output contract, file path, and the one piece of inherited judgement all travel in the
prompt. The summary-only return keeps the coordinator's window clean while the full data lands on
disk.
</example>

<example>
Per-item passes plus an integration pass.

```js
const perFile = await Promise.all(files.map(reviewOneFile));  // full attention each
const integration = await reviewCrossFile(perFile);           // data flow, contradictions
```

The integration pass is the only place that needs the whole picture, and it operates on structured
summaries rather than raw files, so it stays small.
</example>

<example>
Fresh session with summary injection after files changed.

```text
Prior analysis found issues in auth.ts, session.ts, and middleware.ts:
  - auth.ts:142 — token compared with == instead of a constant-time compare   [fixed]
  - session.ts:88 — session id generated from Math.random()                   [fixed]
  - middleware.ts:31 — CORS wildcard with credentials: true                   [fixed]
All three have since been modified. Re-analyze only those three files: verify each
fix is correct and check for regressions introduced by the change.
```
</example>

<example>
A scratchpad holding specifics outside the window.

```markdown
# Exploration scratchpad — Order Service   (phase 2 of 3)
## Established
- OrderRepository (src/repos/order.ts) implements Repository<T>; custom findById caching
- Chain: RefundProcessor -> OrderService -> OrderRepository -> PostgreSQL
- High risk: RefundProcessor has no retry around the payment call (src/refund.ts:74)
## Explored
src/repos/**, src/services/order*.ts, src/refund.ts
## Not yet explored
src/webhooks/**, migrations/
## Next
Trace the webhook replay path; confirm the idempotency key is persisted before the payment call.
```

Concrete names survive compaction, a crash, or a fresh session. Recovery is one read instead of a
re-exploration.
</example>

## Failure modes

**Narrow decomposition, then blaming the subagents.** Split to `[visual arts]`, then rewrite the
search queries, upgrade the subagent model, add more visual-arts agents. Music, writing, and film
were never requested, so no downstream change can find them, and the output looks complete because
nothing reports a gap.

**Assuming shared memory.** "Synthesize the findings from the research agents" reaches a
synthesizer that has never seen them. It reports nothing, or worse, generates plausible findings
from parametric knowledge and produces a confident unsourced report. Pass the findings, or the
paths they were written to.

**Content passed without metadata.** "Solar panel efficiency rose 25% in a decade" cannot be cited
by an agent that was never told where it came from. Teams then pressure the synthesis agent to add
citations, which produces fabricated ones.

**Peer-to-peer subagents, or sequential spawns.** The first destroys the coordinator's vantage
point: no single place knows what was covered or what failed. The second pays full serialization
latency for work with no dependencies.

**Resuming after code changed, or reviewing in the generating session.** The resumed session still
holds pre-fix file contents in tool results and reasons from them. The same-session review shares
the reasoning that produced the code and defends it.

**One pass over fourteen files, then reaching for a bigger window.** The defect is attention
dilution across items in a single pass; more window gives the same diluted attention more room.
