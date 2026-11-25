---
name: scaffolding-langgraph
description: |
  Builds production-grade, stateful, long-running AI agents with LangGraph: explicit StateGraphs, conditional edges, Send fan-out, durable checkpointing, cross-thread memory, and human-in-the-loop interrupts.
  Use when designing multi-step pipelines with branching logic, agents that pause and resume across hours or days, workflows where each step is addressable and evaluable, map-reduce / parallel-specialist patterns, per-user cross-thread memory, deploying to LangGraph Platform or self-host, or whenever the user names LangGraph.
  Covers StateGraph, TypedDict/Pydantic state, reducers, Command, Send, Memory/Sqlite/Postgres checkpointers, BaseStore, interrupt() / Command(resume), subgraphs, streaming, prebuilts (create_agent, ToolNode), Functional API, retry/cache/timeout, durability, recursion_limit, deployment, LangSmith, and testing.
  NOT for simple tool-use loops (prefer scaffolding-openai-agents) or raw LangChain without the graph layer.
---

# Scaffolding LangGraph

Build stateful, durable agents as explicit state graphs. The graph is the program; state flows through nodes and reducers; checkpointers persist threads so runs can pause for hours, days, or human input and resume exactly where they left off.

## When to reach for LangGraph (vs. an agent loop)

Choose LangGraph when **any** of these apply:
- Workflow has **branching logic** that should be explicit (not buried in a prompt).
- Agent must **pause and resume across processes / days** (HITL approval, async waits).
- You need **per-node evals** — each step is an addressable, replayable unit.
- Multiple specialists need to **share typed state** rather than pass messages.
- You need **dynamic fan-out** (per-item parallel work) — Send API.
- You need **per-user memory** that outlives a single thread — Store.

Plain LLM-with-tool-loop? Use `scaffolding-openai-agents` or LangGraph's `create_agent` prebuilt.

## Before implementation

Gather context before writing code:

| Source | Gather |
|---|---|
| **Codebase** | Existing graph(s), state schemas, checkpointer config, deployment target (Platform vs self-host) |
| **Conversation** | Async vs sync, persistence backend, HITL needs, parallel/fan-out shape, latency vs durability tradeoffs |
| **References below** | API patterns, version-specific imports, anti-patterns |
| **User guidelines** | Team conventions for state design, naming, observability |

### Required clarifications (ask only what's not already known)

1. **Runtime model**: sync or async (`invoke`/`stream` vs `ainvoke`/`astream`)?
2. **Persistence backend**: dev-only (`InMemorySaver`), single-process (`SqliteSaver`), or production (`PostgresSaver` / `AsyncPostgresSaver`)?
3. **Cross-thread memory**: needed (`Store`) or single-thread is fine?
4. **HITL**: any approval / clarification / edit-in-place steps?
5. **Deployment target**: LangGraph Platform, self-host with `langgraph build`, or library embedded in an existing service?

### Optional clarifications

6. Fan-out / map-reduce required (`Send`)?
7. Multi-agent shape (supervisor / swarm / hierarchical)?
8. PII in state (need `EncryptedSerializer`)?
9. Observability target (LangSmith env vars vs custom tracing)?

Ask only for **their** specifics — not for LangGraph concepts; those live in `references/`. Avoid asking everything in one message; start with #1–3, follow up as needed.

## Official documentation

| Resource | URL | Use for |
|---|---|---|
| LangGraph docs (Python) | https://docs.langchain.com/oss/python/langgraph/ | Authoritative API, concepts, deployment |
| LangGraph API reference | https://langchain-ai.github.io/langgraph/reference/ | Class/method signatures |
| LangGraph Platform | https://docs.langchain.com/langgraph-platform/ | Managed deployment, auth, scheduling |
| LangSmith | https://docs.smith.langchain.com/ | Tracing and evals |
| GitHub | https://github.com/langchain-ai/langgraph | Source, examples, issues |

When in doubt, fetch the latest patterns via the `fetch-library-docs` skill rather than relying on memory — LangGraph evolves quickly and import paths shift between minor versions.

## Install

```bash
pip install -U langgraph langchain langchain-core
# Persistence
pip install langgraph-checkpoint-postgres psycopg[binary,pool]   # Postgres
pip install langgraph-checkpoint-sqlite                          # SQLite
# Optional
pip install langgraph-cli[inmem]                                  # local dev server
```

Set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY=...` in env to get free traces of every node, edge, and LLM call.

## Core mental model — six concepts

1. **State schema** — `TypedDict` (preferred) or `pydantic.BaseModel` describing every key the graph reads/writes. Optionally split into `input_schema`/`output_schema` and a private "overall" schema.
2. **Reducers** — `Annotated[type, reducer_fn]` merges concurrent updates. Default is overwrite. `add_messages` for chat history, `operator.add` for accumulating lists, custom callables for anything else.
3. **Nodes** — functions `(state) -> partial_state_dict`. Optionally accept a second `Runtime[Context]` arg for runtime context, store access, and retry info.
4. **Edges** — static (`add_edge`), conditional (`add_conditional_edges`), `Command(goto=...)` returned from a node, or `Send(...)` for dynamic fan-out.
5. **Checkpointer** — saves state per super-step keyed by `thread_id`. Required for resume, HITL, time travel.
6. **Store** — `BaseStore` for **cross-thread** memory (per-user, per-namespace). Lives alongside the checkpointer.

## Minimum viable graph

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.messages import AnyMessage, HumanMessage, AIMessage

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def respond(state: State):
    return {"messages": [AIMessage(content="hello")]}

graph = (
    StateGraph(State)
    .add_node("respond", respond)
    .add_edge(START, "respond")
    .add_edge("respond", END)
    .compile()
)
graph.invoke({"messages": [HumanMessage("hi")]})
```

For chat-shaped agents, `from langgraph.graph import MessagesState` gives a built-in `{messages: Annotated[..., add_messages]}` schema. Subclass it to add your own keys.

## Conditional edges and `Command`

```python
from typing import Literal
from langgraph.types import Command

def should_continue(state: State) -> Literal["tools", "__end__"]:
    return "tools" if state["messages"][-1].tool_calls else END

builder.add_conditional_edges("llm", should_continue, ["tools", END])

# Or update + route in one return from inside a node:
def plan(state) -> Command[Literal["research", "answer"]]:
    return Command(update={"plan": "..."}, goto="research")
```

Prefer `Command` when routing decision and state update share the same data.

## Dynamic fan-out — the `Send` API

A conditional edge can return `list[Send(node_name, partial_state)]` to spawn N parallel invocations of a node — each with its own input. The reducer on the result key merges them back.

```python
from langgraph.types import Send

def fan_out(state):
    return [Send("worker", {"item": x}) for x in state["items"]]

builder.add_conditional_edges("plan", fan_out, ["worker"])
```

This is the right tool for map-reduce, per-section writers, parallel research, and any "do X for each Y" pattern. See [references/control-flow.md](references/control-flow.md).

## Checkpointing

Compile with a checkpointer; pass `thread_id` in config; runs are durable.

```python
# Dev / tests
from langgraph.checkpoint.memory import InMemorySaver
graph = builder.compile(checkpointer=InMemorySaver())

# Production async
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
async with AsyncPostgresSaver.from_conn_string(DB_URI) as cp:
    graph = builder.compile(checkpointer=cp)
    async for ch in graph.astream(inputs, {"configurable": {"thread_id": "u-42"}}, stream_mode="values"):
        ...
```

Variants: `PostgresSaver` (sync), `SqliteSaver`/`AsyncSqliteSaver` (single-process). Run `.setup()` exactly once per fresh DB. Encrypt at rest with `EncryptedSerializer`. Deep dive: [references/checkpointing.md](references/checkpointing.md).

## Cross-thread memory — Store

Checkpointers persist **one thread**. To share memory across threads/users, attach a `BaseStore` and access it via `Runtime`:

```python
from langgraph.store.postgres.aio import AsyncPostgresStore
from langgraph.runtime import Runtime
from dataclasses import dataclass

@dataclass
class Context:
    user_id: str

async def call_model(state: MessagesState, runtime: Runtime[Context]):
    ns = (runtime.context.user_id, "memories")
    hits = await runtime.store.asearch(ns, query=state["messages"][-1].content, limit=3)
    ...
    await runtime.store.aput(ns, str(uuid.uuid4()), {"data": "..."})

builder = StateGraph(MessagesState, context_schema=Context)
graph = builder.compile(checkpointer=cp, store=store)
graph.invoke(inputs, config, context=Context(user_id="1"))
```

See [references/store.md](references/store.md).

## Human-in-the-loop

```python
from langgraph.types import Command, interrupt

def review(state):
    answer = interrupt({"kind": "approve", "plan": state["plan"]})
    return {"approved": answer == "yes"}

graph.invoke(inputs, config)                # pauses; result has __interrupt__
graph.invoke(Command(resume="yes"), config) # resumes; interrupt() returns "yes"
```

Requires a checkpointer. Side effects must run **after** `interrupt()` (the node re-runs from the top on resume). Patterns and pitfalls: [references/human-in-the-loop.md](references/human-in-the-loop.md).

## Subgraphs

Compile a graph and use it as a node. Cross to the parent with `Command(graph=Command.PARENT, goto=..., update=...)`. Stream subgraph events with `subgraphs=True`. See [references/subgraphs.md](references/subgraphs.md).

## Streaming

```python
async for mode, chunk in graph.astream(inputs, config,
        stream_mode=["values", "updates", "messages", "custom"],
        subgraphs=True):
    ...
```

Modes: `values` (full snapshot), `updates` (per-node diffs), `messages` (LLM tokens), `custom` (`get_stream_writer()` from inside a node), `debug` (verbose).

## Prebuilts and Functional API

- `from langgraph.prebuilt import ToolNode, tools_condition` — drop-in tool execution + routing.
- `from langgraph.prebuilt import create_react_agent` (older) or `from langchain.agents import create_agent` (newer) — opinionated ReAct loop you can compose into a larger graph.
- `@entrypoint` / `@task` (Functional API) — write durable workflows as plain functions when graph topology is overkill.

See [references/prebuilts.md](references/prebuilts.md).

## Production knobs

- **Per-node retry/cache/timeout**: `add_node(name, fn, retry_policy=RetryPolicy(...), cache_policy=CachePolicy(ttl=120), timeout=TimeoutPolicy(...))`.
- **Durability mode**: `invoke(..., durability="async"|"sync"|"exit")`. `async` is default; choose `sync` for max safety, `exit` for max throughput.
- **Recursion limit**: `invoke(..., config={"recursion_limit": 50})` — guards runaway loops; raises `GraphRecursionError`.
- **Runtime context**: `context=Context(...)` on invoke; access via `Runtime[Context]` parameter on a node.

See [references/runtime-policies.md](references/runtime-policies.md).

## Deployment and observability

- Define `langgraph.json` (`graphs`, `dependencies`, `env`) — required for LangGraph Platform and `langgraph dev`/`langgraph build`.
- LangGraph Platform provides managed checkpointer, store, scheduler, /runs API, /threads API.
- Self-host with the prebuilt Docker image or compile your own server around the graph.
- LangSmith via env vars (`LANGSMITH_TRACING`, `LANGSMITH_API_KEY`) traces every node + LLM call. Add tags/metadata via `config={"tags": [...], "metadata": {...}}`.

See [references/deployment.md](references/deployment.md).

## Testing

A node is `(state) -> partial_state` — unit test as a function. Component-test slices with `update_state(as_node=...)` + `invoke(None, ..., interrupt_after=...)`. Replay regressions from a captured `checkpoint_id`. See [references/testing.md](references/testing.md).

## Common mistakes

- **Missing reducer on a list/dict key** — concurrent nodes overwrite. Use `add_messages` / `operator.add` / custom.
- **Returning the entire state** from a node — return only changed keys.
- **`interrupt()` without checkpointer** — raises. Always compile with one.
- **Side effects before `interrupt()`** — they run twice on resume; move them after, or to a separate node.
- **Reusing `thread_id`** across unrelated runs — phantom replays. Use UUIDs scoped per logical conversation.
- **Routing logic in a prompt** — defeats the point. Branch with `add_conditional_edges` / `Command` / `Send`.
- **`.setup()` on every cold start** — slow. Run once at deploy.
- **Subgraph + own checkpointer** when parent already has one — they conflict. Subgraphs inherit.
- **Two `recursion_limit` defaults** — default 25; bump it for fan-out workflows or long ReAct loops.

## Reference files

Read only the file(s) relevant to the current task:

| File | Read when |
|---|---|
| [references/state-and-reducers.md](references/state-and-reducers.md) | Designing schemas, picking reducers, Pydantic state, input/output/private schemas |
| [references/control-flow.md](references/control-flow.md) | Conditional edges, `Command`, `Send` map-reduce/fan-out, recursion limits |
| [references/checkpointing.md](references/checkpointing.md) | Persistence backends, threads, time travel, encryption |
| [references/store.md](references/store.md) | Cross-thread memory, namespaces, semantic search, Runtime context |
| [references/human-in-the-loop.md](references/human-in-the-loop.md) | `interrupt()`, approve/edit/clarify, interrupt-in-tool |
| [references/subgraphs.md](references/subgraphs.md) | Composition, `Command.PARENT`, multi-agent supervisor |
| [references/prebuilts.md](references/prebuilts.md) | `create_agent`, `ToolNode`, `tools_condition`, Functional API |
| [references/runtime-policies.md](references/runtime-policies.md) | Retry/cache/timeout, durability, recursion, error types |
| [references/deployment.md](references/deployment.md) | `langgraph.json`, Platform vs self-host, LangSmith |
| [references/testing.md](references/testing.md) | Node, component, HITL, replay tests |
