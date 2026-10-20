---
name: agent-architecture-design
description: >
  Guides designing the control loop, state/memory model, and tool boundaries
  for an LLM-driven agent. Use when a user asks to "design an agent
  architecture," choose between a ReAct loop / plan-and-execute / finite-state
  agent, decide on single-agent vs multi-agent decomposition, define how an
  agent should manage state and memory across turns, or review whether an
  existing agent's control flow is safe to run unattended.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Agent Architecture Design

## Purpose

An "agent" is a loop: an LLM repeatedly observes state, decides on an action
(call a tool, ask the user, or finish), and updates state based on the
result, until some termination condition is met. Getting this loop's shape
wrong is the single biggest source of production incidents in agentic
systems — not model quality. Agents that loop forever, that accumulate
unbounded context, that hold too many high-privilege tools in one prompt, or
that have no checkpoint for a human to intervene, fail in ways that are
expensive, hard to debug, and sometimes destructive. This skill defines a
small set of proven architecture patterns (ReAct-style loop, plan-and-execute,
finite-state/graph) and the state, memory, and control-flow decisions that
make an agent safe and debuggable to operate, independent of which model or
vendor SDK is driving it.

## When to use

- Starting a new agent project and deciding "should this be one prompt with
  tools, a ReAct loop, or a directed graph of steps?"
- An existing agent occasionally loops, stalls, or takes an unexpected
  destructive action, and you need to redesign its control flow.
- Deciding whether a task needs one agent with many tools or several
  narrower agents (see [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md)).
- Designing how an agent's memory persists across sessions (vs. what lives
  only in the current context window).
- Code review of an agent's main loop before it is given write access to
  production systems (files, cloud APIs, payment systems, ticketing).
- Adding a human-in-the-loop approval checkpoint to an agent that currently
  runs fully autonomously.

## Prerequisites & environment

- Working knowledge of an LLM API that supports structured tool/function
  calling (the concept is portable across Anthropic, OpenAI, Google, and
  open models — exact request/response shapes differ by vendor).
- A chosen orchestration surface: a raw API loop you write yourself, or a
  framework/runtime (e.g. an agent SDK, LangGraph-style graph runtime, or a
  CLI agent host like Claude Code). This skill is framework-agnostic; adapt
  the patterns to whichever runtime you use.
- Access to the tools/APIs the agent will call, ideally in a sandboxed or
  staging environment before granting production credentials.
- A way to capture traces/logs of each loop iteration (even a structured
  log file is enough to start).

## Step-by-step guidance

1. **Write down the termination condition before writing any prompt.**
   Every agent loop needs an explicit "done" signal: a tool call that means
   completion, a structured final-answer format, or a supervisor check. If
   you cannot state in one sentence how the loop knows to stop, do not start
   building.

2. **Pick a control-flow pattern that matches the task's shape:**
   - **ReAct-style loop** (reason → act → observe, repeat): best for
     open-ended tasks where the next step genuinely depends on the last
     tool result (debugging, research, exploratory coding).
   - **Plan-and-execute**: the model first emits a multi-step plan, then a
     (possibly separate, cheaper) executor runs each step; best when steps
     are largely independent and you want a reviewable plan before any
     action runs.
   - **Finite-state / graph**: fixed set of named states and explicit
     transitions (e.g. `triage → gather_info → draft → approve → send`);
     best for compliance-sensitive or repeatable business processes where
     you want to reason about which states can reach which other states.

3. **Bound the loop explicitly.** Set a hard maximum iteration count and a
   wall-clock timeout, independent of the model's own judgment about when
   it's done. Fail closed (stop and surface an error) rather than fail open
   (silently keep going or silently give up and claim success).

   ```python
   MAX_ITERATIONS = 12
   TIMEOUT_SECONDS = 180

   def run_agent_loop(task, tools):
       start = time.monotonic()
       for i in range(MAX_ITERATIONS):
           if time.monotonic() - start > TIMEOUT_SECONDS:
               return AgentResult(status="timeout", partial=state.transcript)
           response = llm.call(messages=state.messages, tools=tools)
           if response.stop_reason == "end_turn":
               return AgentResult(status="done", output=response.text)
           if response.stop_reason == "tool_use":
               for call in response.tool_calls:
                   result = dispatch_tool(call, allowlist=tools)  # see agent-tool-use-patterns
                   state.messages.append(tool_result_message(call, result))
       return AgentResult(status="max_iterations_exceeded", partial=state.transcript)
   ```

4. **Design the state/memory model as two tiers.** Keep a small *working
   state* (current task, plan, last N tool results) that lives in the
   context window, and a separate *persisted memory* (a database, vector
   store, or file) for anything that must survive across sessions or is too
   large to keep in-context. Never treat the raw conversation transcript as
   your only memory store — it grows unbounded and degrades reasoning
   quality long before it hits a hard token limit.

5. **Define tool boundaries per agent, not per task.** List every tool the
   agent can call and classify each as read-only, reversible-write, or
   irreversible-write. Irreversible-write tools (send email, delete
   resource, execute payment) should require either a dedicated
   confirmation step in the state machine or a human-in-the-loop gate — do
   not rely on prompt instructions alone to prevent misuse.

6. **Add a human checkpoint at the highest-leverage point**, not
   everywhere. For a finite-state design, this is usually a dedicated state
   (`awaiting_approval`) the graph cannot exit without external input. For
   a ReAct loop, it's a policy check inside `dispatch_tool` that intercepts
   specific tool names.

7. **Instrument before you optimize.** Log, at minimum: the input to each
   LLM call, the tool calls it emitted, the tool results, and the final
   stop reason. Without this, pitfalls like loops and context bloat are
   invisible until they cause an incident.

8. **Decide single-agent vs multi-agent last, not first.** Start with the
   simplest single agent with a well-scoped tool set; only split into
   multiple agents once you have concrete evidence of context overload,
   role confusion, or the need for parallel independent workstreams (see
   [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md) for
   when that split is justified).

## Best practices

- Treat the agent loop's termination and iteration cap as safety-critical
  code, not a minor implementation detail — review it like you would review
  authentication logic.
- Prefer fewer, well-scoped tools over many overlapping ones; tool
  proliferation increases both hallucinated tool calls and prompt size (see
  [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md)).
- Keep the system prompt's description of "what this agent is for" narrow.
  A narrowly scoped agent is both easier to evaluate and less prone to
  scope creep mid-task.
- Make every state transition in a finite-state design observable
  externally (emit an event), so a supervising process or human can watch
  progress without parsing free-text output.
- Separate "planning" model calls from "execution" model calls when cost or
  latency matters — a cheaper/faster model can often execute a
  well-specified plan step, reserving the strongest model for planning and
  ambiguous judgment calls (see
  [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md)).
- Version your system prompt and tool schemas together; a tool schema
  change without a matching prompt update is a common source of silent
  regressions.
- Design for idempotent retries: if a tool call's result is ambiguous (e.g.
  a network timeout after a write), the agent should be able to safely
  check current state rather than blindly retrying a non-idempotent action.

## Common pitfalls

- **Symptom:** Agent runs for minutes issuing tool calls that don't make
  progress, eventually timing out or exhausting a rate limit.
  **Fix:** Enforce a hard iteration cap and a "no progress" detector (e.g.
  compare the last two tool calls; if identical, break and surface the
  stall rather than retrying silently).

- **Symptom:** Agent's context window fills with entire raw outputs of
  every tool call (full file contents, entire API responses), degrading
  reasoning quality on later turns even though the token limit hasn't been
  hit yet.
  **Fix:** Summarize or truncate tool results before appending to state;
  keep only what later steps actually need, and move anything bulky to
  persisted memory that can be fetched again on demand.

- **Symptom:** A single "god agent" with 30+ tools spanning unrelated
  domains (billing, infra, customer messaging) occasionally calls the wrong
  tool for a superficially similar request.
  **Fix:** Split by domain into narrower agents or narrower tool subsets
  activated per task, rather than exposing the full tool surface on every
  call.

- **Symptom:** An irreversible action (e.g. deleting a cloud resource,
  sending a customer email) executes because the agent "decided" the task
  was done, with no external checkpoint.
  **Fix:** Move irreversible tools behind an explicit approval state or a
  policy layer in the dispatcher, never rely on prompt wording ("ask before
  deleting") as the only safeguard.

- **Symptom:** Errors from a tool call are swallowed and the agent reports
  success anyway.
  **Fix:** Propagate tool errors into the next model turn as explicit
  failure content (not silently retried or hidden), and require the loop's
  terminal state to distinguish `done`, `failed`, and `partial`.

## Worked example

**Task:** an internal agent that triages incoming support tickets, drafts a
reply, and — only after a human approves — sends it.

Finite-state design:

```
states:
  triage:        classify ticket category + urgency (read-only tools: search_kb, get_ticket)
  gather_info:   pull account/order history if category requires it (read-only tools)
  draft_reply:   produce a draft reply grounded in gathered context
  awaiting_approval:  present draft to a human reviewer; no tools available here
  send:          call send_reply tool (irreversible-write, only reachable from awaiting_approval)
  escalate:      hand off to a human agent directly (terminal state, no send)

transitions:
  triage -> gather_info | escalate
  gather_info -> draft_reply | escalate
  draft_reply -> awaiting_approval
  awaiting_approval -> send | draft_reply (reviewer requests changes)
```

Loop bound: max 6 state transitions per ticket, 60s timeout per LLM call.
Every transition emits a `ticket.state_changed` event with ticket id, from
state, to state, and the tool calls made in that state — this is what an
observability dashboard and later
[agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md)
checks consume. The `send` state is the only place `send_reply` (an
irreversible-write tool) is even present in the tool list passed to the
model, so a prompt-injection attempt from ticket content cannot cause a
send from an earlier state — the tool literally isn't offered.

## Cross-references

- [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md)
- [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md)
- [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md)
- [mcp-server-development](../mcp-server-development/SKILL.md)
