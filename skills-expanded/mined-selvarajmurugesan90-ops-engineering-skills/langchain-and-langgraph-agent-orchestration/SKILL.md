---
name: langchain-and-langgraph-agent-orchestration
description: >
  Guides building LLM applications with LangChain's chain/agent abstractions
  and, for stateful multi-step agents, LangGraph's graph-based orchestration
  (nodes, edges, cycles, checkpointed persistence, human-in-the-loop
  interrupts). Use when a user asks to "build this with LangChain," "use
  LangGraph for a stateful agent," "add persistence/checkpointing to a
  LangChain agent," "add a human approval step in a LangGraph graph," "my
  LangChain agent loses state between turns," or is deciding between
  LangChain's `AgentExecutor`, a LangGraph graph, and a hand-rolled control
  loop.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# LangChain and LangGraph Agent Orchestration

## Purpose

LangChain provides two things that are easy to conflate: a set of composable
building blocks (prompt templates, model wrappers, retrievers, output
parsers, chained via LangChain Expression Language / `Runnable`), and a
higher-level `AgentExecutor` that wraps those blocks into a single-loop,
tool-calling agent. LangGraph is a separate, lower-level runtime built by the
same project specifically for agents whose control flow is not a single
linear loop — it models the agent as an explicit graph of nodes and edges,
supports cycles (a node can route back to an earlier node), and adds two
capabilities `AgentExecutor` does not have out of the box: durable
checkpointed state (so a run can pause, crash, and resume from its last
checkpoint) and first-class human-in-the-loop interrupts (a graph can pause
at a named node until a human approves, edits, or rejects the pending
state). This skill covers choosing between plain LangChain composition,
`AgentExecutor`, and LangGraph, and operating LangGraph's persistence and
interrupt features correctly. It is a framework-specific complement to
[agent-architecture-design](../agent-architecture-design/SKILL.md), which
covers the underlying control-flow patterns (ReAct loop, plan-and-execute,
finite-state/graph) in a vendor-neutral way — LangGraph is one concrete
runtime that implements the finite-state/graph pattern described there. For
tool access, LangChain/LangGraph agents can call tools defined directly in
Python or exposed via an MCP server; see
[mcp-server-development](../mcp-server-development/SKILL.md) for building
the tool-serving side, which this skill treats as an external dependency
rather than repeating.

## When to use

- Deciding whether a task needs plain LangChain chain composition (a fixed
  pipeline, no branching), `AgentExecutor` (a single ReAct-style tool-calling
  loop), or a LangGraph graph (multi-step, branching, cyclical, or needing
  persistence/human approval).
- Building an agent whose steps depend on prior results in ways a single
  linear chain can't express — retries, conditional branches, or loops back
  to an earlier step.
- Adding durable state to a LangChain/LangGraph agent so a long-running or
  multi-session workflow survives a process restart or crash mid-run.
- Adding a human-in-the-loop approval checkpoint before an irreversible tool
  call in an existing LangGraph graph.
- An agent built with `AgentExecutor` loses context, re-does completed work,
  or can't be paused/resumed, and the team is evaluating migrating it to
  LangGraph.
- Debugging a LangGraph graph that loops indefinitely, gets stuck at an
  interrupt, or fails to restore state correctly from a checkpoint.

## Prerequisites & environment

- Python (LangChain/LangGraph's primary, most mature ecosystem) or
  JavaScript/TypeScript (`langchain`/`langgraph` npm packages, closely
  mirroring the Python API but with some feature lag) — pick one and check
  current package versions before starting, since both projects have had
  breaking changes across major versions (notably the LangChain 0.1 → 0.2/0.3
  restructuring that split core, community, and partner packages).
- An LLM provider integration package (e.g. `langchain-anthropic`,
  `langchain-openai`) installed separately from `langchain-core` — recent
  LangChain versions moved provider-specific code out of the core package.
- For LangGraph persistence: a checkpointer backend — the in-memory
  `MemorySaver` for local development/testing only (state is lost on
  process exit), or a durable checkpointer (SQLite, Postgres, or a
  managed backend) for anything that must survive a restart.
- Tool definitions the agent will call, either as plain Python functions
  decorated with LangChain's `@tool`, or proxied from an MCP server via an
  MCP-to-LangChain adapter — confirm which integration path your LangChain
  version currently supports before assuming API shape.
- Clarity on which parts of the workflow are genuinely cyclical/branching
  (justifying LangGraph) versus a fixed sequence (better served by a plain
  LCEL chain) — reach for LangGraph only once a chain's limitations are
  concrete, mirroring the "justify the split" discipline in
  [agent-architecture-design](../agent-architecture-design/SKILL.md).

## Step-by-step guidance

1. **Start with the simplest abstraction that fits the task's shape.** A
   fixed sequence (retrieve → prompt → parse) is a plain LCEL chain:
   ```python
   from langchain_core.prompts import ChatPromptTemplate
   from langchain_core.output_parsers import StrOutputParser
   from langchain_anthropic import ChatAnthropic

   prompt = ChatPromptTemplate.from_messages([
       ("system", "Summarize the following ticket in one sentence."),
       ("human", "{ticket_text}"),
   ])
   model = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
   chain = prompt | model | StrOutputParser()
   result = chain.invoke({"ticket_text": ticket_body})
   ```
   No loop, no tool calls, no branching — a chain is the right tool and
   adding `AgentExecutor` or LangGraph here is unjustified complexity.

2. **Use `AgentExecutor` only for a single, bounded ReAct-style loop** with
   no need for persistence, human interrupts, or branching beyond
   tool-call/no-tool-call:
   ```python
   from langchain.agents import AgentExecutor, create_tool_calling_agent
   from langchain_core.tools import tool

   @tool
   def search_tickets(query: str) -> str:
       """Search support tickets by keyword. Returns matching ticket IDs."""
       return ticketing_backend.search(query)

   agent = create_tool_calling_agent(model, [search_tickets], prompt)
   executor = AgentExecutor(
       agent=agent, tools=[search_tickets],
       max_iterations=8, max_execution_time=60,   # bound the loop explicitly
   )
   result = executor.invoke({"input": "find open billing tickets"})
   ```
   `max_iterations`/`max_execution_time` are `AgentExecutor`'s equivalent of
   the hard iteration cap and timeout described in
   [agent-architecture-design](../agent-architecture-design/SKILL.md) — set
   both explicitly; the defaults are more permissive than most production
   use cases want.

3. **Move to LangGraph once the task needs cycles, branching, persistence,
   or a human checkpoint.** Model the agent as a typed state object and a
   graph of nodes:
   ```python
   from typing import TypedDict, Annotated
   from langgraph.graph import StateGraph, END
   from langgraph.checkpoint.memory import MemorySaver

   class TicketState(TypedDict):
       ticket_id: str
       category: str
       draft_reply: str
       approved: bool

   def triage(state: TicketState) -> TicketState:
       category = classify(state["ticket_id"])
       return {**state, "category": category}

   def draft(state: TicketState) -> TicketState:
       reply = generate_draft(state["ticket_id"], state["category"])
       return {**state, "draft_reply": reply}

   def route_after_triage(state: TicketState) -> str:
       return "escalate" if state["category"] == "legal" else "draft"

   graph = StateGraph(TicketState)
   graph.add_node("triage", triage)
   graph.add_node("draft", draft)
   graph.add_node("escalate", lambda s: {**s, "approved": False})
   graph.set_entry_point("triage")
   graph.add_conditional_edges("triage", route_after_triage, {"draft": "draft", "escalate": "escalate"})
   graph.add_edge("draft", END)
   graph.add_edge("escalate", END)

   app = graph.compile(checkpointer=MemorySaver())
   ```
   This is the finite-state/graph pattern from
   [agent-architecture-design](../agent-architecture-design/SKILL.md)
   expressed directly in LangGraph's API — nodes are states, edges (plain
   or conditional) are transitions.

4. **Add a human-in-the-loop interrupt at the highest-leverage node**, not
   everywhere, using `interrupt_before`/`interrupt_after` at compile time:
   ```python
   app = graph.compile(
       checkpointer=MemorySaver(),
       interrupt_before=["send_reply"],   # pause here every run until resumed
   )

   config = {"configurable": {"thread_id": "ticket-8842"}}
   app.invoke(initial_state, config=config)   # runs up to send_reply, then pauses

   # ... a human reviews the checkpointed state out-of-band ...

   app.invoke(None, config=config)            # resumes from the paused checkpoint
   ```
   Passing `None` as input on resume is deliberate — it tells LangGraph to
   continue from the last checkpoint rather than starting a new run; passing
   a real input restarts the thread instead.

   > **Warning:** compiling a graph that reaches an irreversible-write node
   > (sending a message, executing a payment, deleting a resource) with no
   > `interrupt_before` on that node means it will execute automatically the
   > first time the graph reaches it, with no human checkpoint at all. Do
   > not rely on prompt wording alone to prevent an irreversible action —
   > gate it structurally with `interrupt_before`, the same discipline
   > described for any irreversible tool in
   > [agent-architecture-design](../agent-architecture-design/SKILL.md).

5. **Choose a checkpointer backend deliberately for the deployment target.**
   `MemorySaver` is fine for local development and tests; anything
   long-running or multi-process needs a durable checkpointer:
   ```python
   from langgraph.checkpoint.sqlite import SqliteSaver
   # or, for production multi-instance deployments:
   # from langgraph.checkpoint.postgres import PostgresSaver

   with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
       app = graph.compile(checkpointer=checkpointer)
   ```
   Every checkpointed run needs a stable `thread_id` in `config`; reusing a
   `thread_id` across unrelated tasks corrupts that thread's history.

6. **Bound cycles explicitly.** A conditional edge that can route back to an
   earlier node (e.g. `draft -> review -> draft` on rejection) needs an
   explicit counter in state and a hard cap, or a rejection loop can run
   indefinitely:
   ```python
   def route_after_review(state: TicketState) -> str:
       if state.get("revision_count", 0) >= 3:
           return "escalate"          # fail closed after 3 rejected drafts
       return "draft" if not state["approved"] else END
   ```

7. **Stream intermediate state for observability**, rather than only
   consuming the final result — both `AgentExecutor` and LangGraph support
   streaming (`.stream()`/`.astream()`), which surfaces each tool call and
   state transition as it happens, matching the "instrument every loop
   iteration" guidance in
   [agent-architecture-design](../agent-architecture-design/SKILL.md).

8. **Compose multiple LangGraph graphs for multi-agent topologies** rather
   than hand-rolling a supervisor loop, when the task genuinely needs
   multiple specialized roles — a compiled graph can itself be a node in a
   parent graph. Confirm this split is justified per
   [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md) before
   introducing it; LangGraph makes multi-agent easy to wire, not automatically
   the right call.

## Best practices

- Default to the least powerful abstraction that fits: LCEL chain <
  `AgentExecutor` < LangGraph. Reaching for LangGraph on day one for a fixed
  three-step pipeline adds state-management overhead with no payoff.
- Keep LangGraph node functions small, pure, and independently testable —
  each node should be callable and assertable in isolation, the same way you
  would unit-test any function, rather than only testable end-to-end through
  the compiled graph.
- Treat `thread_id` as a real identifier with a lifecycle (create, resume,
  archive/expire), not an incidental config parameter — losing track of
  which `thread_id` corresponds to which real-world task makes checkpointed
  state unrecoverable in practice even though it's durably stored.
- Put `interrupt_before` only on nodes that perform irreversible or
  high-consequence actions (sending a message, executing a payment,
  deleting a resource), mirroring the "human checkpoint at the
  highest-leverage point" guidance in
  [agent-architecture-design](../agent-architecture-design/SKILL.md) — an
  interrupt on every node defeats the purpose and trains reviewers to
  rubber-stamp.
- Pin `langchain-core`, `langgraph`, and provider integration package
  versions together and upgrade them as a set — LangChain's ecosystem has a
  history of breaking changes across the core/community/partner package
  split, and mismatched versions fail in confusing ways (missing attributes,
  import errors) rather than a clear version-conflict message.
- Prefer typed state (`TypedDict`, a Pydantic model, or a dataclass) over a
  loose `dict` for LangGraph state — type errors in state shape are a common
  source of node-to-node bugs that a type checker catches before runtime.

## Common pitfalls

- **Symptom:** An `AgentExecutor`-based agent "forgets" earlier context or
  redoes work across what should be one continuous multi-turn session.
  **Fix:** `AgentExecutor` has no built-in cross-invocation persistence —
  each `.invoke()` call is independent unless you manage message history
  yourself. If the task genuinely needs durable, resumable state across
  turns or a process restart, migrate to LangGraph with a persistent
  checkpointer rather than hand-rolling message-history plumbing on top of
  `AgentExecutor`.

- **Symptom:** A LangGraph graph with a conditional edge routing back to an
  earlier node runs far longer than expected, or never terminates.
  **Fix:** Add an explicit counter field to state (e.g.
  `revision_count`) and check it in the conditional-edge function with a
  hard cap that routes to an escape/escalate node — do not rely on the
  model's own judgment about when to stop looping, per the loop-bounding
  guidance in
  [agent-architecture-design](../agent-architecture-design/SKILL.md).

- **Symptom:** Resuming a LangGraph run after an `interrupt_before` pause
  restarts the whole graph from the entry point instead of continuing from
  where it paused.
  **Fix:** Confirm you invoked with the same `thread_id` in `config` and
  passed `None` (not a fresh input dict) on resume — passing a new input
  value is interpreted as starting a new run on that thread, not continuing
  the paused one.

- **Symptom:** State checkpointed with `MemorySaver` disappears between
  requests in what looks like a production deployment.
  **Fix:** `MemorySaver` is process-local, in-memory state — it does not
  survive a process restart and does not work correctly behind multiple
  server instances/replicas. Swap in a durable, shared checkpointer
  (SQLite for single-instance durability, Postgres or another shared
  backend for multi-instance deployments) before treating persistence as
  production-ready.

- **Symptom:** Upgrading `langchain` breaks imports (`ModuleNotFoundError`,
  moved classes) with no code logic changes.
  **Fix:** Check whether the class moved to a separate `langchain-community`
  or provider-specific package (`langchain-anthropic`, `langchain-openai`)
  as part of LangChain's core/community/partner package split; pin
  `langchain-core`, `langchain`, and each provider package to versions
  tested together rather than upgrading one package in isolation.

## Worked example

**Scenario:** An internal support-ticket agent triages a ticket, drafts a
reply, and requires human approval before sending — the same workflow used
as the finite-state example in
[agent-architecture-design](../agent-architecture-design/SKILL.md), built
concretely in LangGraph with durable persistence and a human interrupt.

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

class TicketState(TypedDict):
    ticket_id: str
    category: str
    draft_reply: str
    revision_count: int

def triage(state: TicketState) -> TicketState:
    return {**state, "category": classify_ticket(state["ticket_id"])}

def draft_reply(state: TicketState) -> TicketState:
    reply = generate_reply(state["ticket_id"], state["category"])
    return {**state, "draft_reply": reply}

def send_reply(state: TicketState) -> TicketState:
    ticketing_backend.send(state["ticket_id"], state["draft_reply"])
    return state

graph = StateGraph(TicketState)
graph.add_node("triage", triage)
graph.add_node("draft_reply", draft_reply)
graph.add_node("send_reply", send_reply)
graph.set_entry_point("triage")
graph.add_edge("triage", "draft_reply")
graph.add_edge("draft_reply", "send_reply")
graph.add_edge("send_reply", END)

with SqliteSaver.from_conn_string("tickets_checkpoints.db") as checkpointer:
    app = graph.compile(checkpointer=checkpointer, interrupt_before=["send_reply"])

    config = {"configurable": {"thread_id": "ticket-8842"}}
    app.invoke({"ticket_id": "8842", "category": "", "draft_reply": "", "revision_count": 0}, config=config)
    # graph pauses before send_reply; state.draft_reply is now available for a
    # human reviewer to read via app.get_state(config)

    # ... later, after a reviewer approves in a separate process/session ...
    app.invoke(None, config=config)   # resumes and executes send_reply
```

Because `SqliteSaver` persists to disk, the pause can span a process
restart — a reviewer approving the draft an hour later (or after a
deployment) still resumes correctly from the same `thread_id`, which a
`MemorySaver`-backed graph could not survive.

## Cross-references

- [agent-architecture-design](../agent-architecture-design/SKILL.md) — the vendor-neutral control-flow patterns (ReAct loop, plan-and-execute, finite-state/graph) that LangGraph implements concretely; read this first for the underlying design principles.
- [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md) — when to compose multiple LangGraph graphs into a supervisor/worker or pipeline topology, and the coordination pitfalls that apply regardless of framework.
- [mcp-server-development](../mcp-server-development/SKILL.md) — building the tool-serving side an agent calls into; this skill covers wiring those tools into a LangChain/LangGraph agent, not building the MCP server itself.
- [crewai-and-autogen-multi-agent-frameworks](../crewai-and-autogen-multi-agent-frameworks/SKILL.md) — alternative higher-level multi-agent frameworks with a role-based abstraction, contrasted with LangGraph's lower-level graph model.
- [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md) — general tool-design principles (single-purpose tools, schema clarity) that apply to `@tool`-decorated functions in LangChain the same as any other agent tool surface.
