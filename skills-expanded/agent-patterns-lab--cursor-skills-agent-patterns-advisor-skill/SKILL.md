---
name: agent-patterns-advisor
description: >-
  Expert architect for agentic systems: pattern selection, distributed
  multi-agent design, cross-network communication, feedback loops,
  self-improving agents, shared state, memory strategies, fail recovery,
  dynamic parallelism, long-running agents, voice-to-agent delegation,
  and agent skills systems. Use when planning architecture, choosing between
  patterns (pipeline, orchestrator, supervisor, mesh, reflection, map-reduce),
  deciding protocols (A2A, MCP, HTTP, queues), designing resilience,
  or reviewing distributed agent systems. Covers LangGraph primitive mapping
  without overlapping code templates owned by langgraph-example-implementation.
---

# Agent Patterns Advisor

## Responsibility

This skill is the **architect** of the agent system. It owns design decisions, pattern selection, and architectural reviews.

Use it to:
- choose the right agent pattern and justify why it is the simplest viable option
- design distributed multi-agent systems and cross-network communication
- design feedback loops, self-improving agents, and evaluation strategies
- plan shared state, team resources, and memory architecture
- design fail recovery that resumes from checkpoints, not from scratch
- plan dynamic parallelism (spawning N agents at runtime)
- design long-running agents that operate for hours or days
- architect voice/conversation systems that delegate to background agents
- design agent skills and capability extension systems
- map any pattern to LangGraph primitives and APIs
- review existing designs for pattern fit, resilience, and operability

Do not use it to:
- write code templates, module layouts, or FastAPI boilerplate; use [`../langgraph-example-implementation/SKILL.md`](../langgraph-example-implementation/SKILL.md)
- look up specific library APIs, compare platforms, or find reference papers; use [`../agent-tools-and-platforms/SKILL.md`](../agent-tools-and-platforms/SKILL.md)
- scaffold folders, Docker files, or READMEs; use [`../example-scaffolder/SKILL.md`](../example-scaffolder/SKILL.md)
- own the test plan; use [`../tester/SKILL.md`](../tester/SKILL.md)

## Operating Principles

1. **Simplest viable pattern.** Start with a single graph and escalate only when forced by ownership, trust, deployment, or resource boundaries.
2. **One responsibility per agent.** An agent that does two things should be two agents.
3. **Thin transport, thick domain.** Business logic belongs in LangGraph nodes or domain modules, not in HTTP handlers.
4. **Debuggability over cleverness.** Explicit edges over dynamic routing. Named nodes over anonymous lambdas. Traces over printf.
5. **Fail-forward design.** Every multi-step workflow should be resumable, not restartable.
6. **Opinionated but reasoned.** State your position clearly, explain trade-offs, and tell the user what would change your recommendation.

## Design Escalation Path

Escalate only when the current level cannot satisfy the requirement:

1. **Single graph or pipeline** in one process.
2. **Router or orchestrator** with specialist agents in one process.
3. **Supervisor** when output must be reviewed or corrected before proceeding.
4. **Reflection loop** when quality requires iterative self-critique.
5. **Map-reduce / dynamic parallelism** when N parallel workers are needed at runtime.
6. **Subgraph composition** when a reusable sub-workflow has its own state shape.
7. **Distributed agents with A2A** when services must be independently deployed, discovered, or owned by different teams.
8. **Queue or durable execution engine** when work must outlive HTTP requests or needs retries, throttling, and backpressure.

---

## Pattern Taxonomy

### Single-Process Patterns

| Pattern | When to use | LangGraph primitive | Main trade-off |
|---------|-------------|--------------------|----|
| **Single graph** | One workflow, one runtime | `StateGraph` | Simplest, but least flexible |
| **Pipeline** | Sequential, deterministic steps | `StateGraph` with linear edges | Simple, rigid ordering |
| **Router** | One entry dispatches to the right specialist | Conditional edges | Fan-out quality depends on routing |
| **Orchestrator** | Coordinator plans and delegates to workers | `StateGraph` with planner + worker nodes | Easy to reason about, centralized |
| **Supervisor** | Coordinator evaluates and corrects worker output | Orchestrator + evaluator node with loop | Better quality, more latency |
| **Reflection** | Iterative self-critique improves output | Generate → Reflect → conditional loop | Quality gains, cost multiplied per iteration |
| **Map-reduce** | N parallel workers determined at runtime | `Send()` API + state reducers | True parallelism, reducer design matters |
| **Hierarchical** | Teams of agents with team leads | Nested `StateGraph` or subgraph nodes | Clear boundaries, more wiring |

### Distributed Patterns

| Pattern | When to use | Protocol | Main trade-off |
|---------|-------------|----------|----|
| **Orchestrator-Worker (A2A)** | Central coordinator delegates to remote specialists | A2A `message/send` + MCP for tools | Easy to reason about, single point of coordination |
| **Pipeline (A2A)** | Sequential agents across services, each transforms | A2A with Artifacts | Simple flow, rigid ordering across network |
| **Peer-to-Peer Mesh** | Loosely coupled agents collaborate as equals | A2A with Agent Cards for discovery | Flexible, harder to debug and govern |
| **Event-Driven** | Agents react to events, no direct coupling | Message queue / event bus | Decoupled, eventual consistency, harder to trace |

---

## Distributed Multi-Agent Architecture

### The Three Best Approaches

**1. Orchestrator-Worker via A2A + MCP (recommended default)**

A central orchestrator service discovers specialist agents through Agent Cards, delegates subtasks via A2A `message/send`, and aggregates results. Each specialist accesses its tools through MCP.

- Best when: one team owns the workflow but specialists may be developed independently.
- Cross-network: orchestrator needs Agent Card URLs of remote agents. Use an agent registry or well-known discovery endpoints. Auth via JWT with `act`/`sub` claims.
- LangGraph mapping: orchestrator is a `StateGraph` where each "call remote agent" step is an async node that uses an A2A client.

**2. Pipeline with A2A Artifacts**

Agents are chained sequentially. Agent A's output becomes Agent B's input via A2A Artifacts. Each agent is independently deployed and can be replaced without changing the pipeline.

- Best when: work is naturally sequential and each stage is owned by a different team.
- Cross-network: each agent publishes its Agent Card. The pipeline coordinator (or each agent directly) forwards artifacts to the next stage.
- LangGraph mapping: each stage is a separate LangGraph deployment. A thin orchestrator or event-driven trigger chains them.

**3. Peer-to-Peer with Agent Cards**

Agents discover each other through Agent Cards and collaborate without a central coordinator. Each agent decides which peers to consult based on the task.

- Best when: agents are loosely coupled, the collaboration pattern is emergent, and no single entity owns the workflow.
- Cross-network: requires a shared agent directory or registry. AGNTCY-style distributed directories are emerging but not production-ready; curated registries are the pragmatic choice.
- LangGraph mapping: each agent is a LangGraph deployment with a `tools` list that includes "call peer agent" tools wrapping A2A clients.

### Cross-Network Communication

When agents are defined by other teams in different networks:

1. **Agent Cards** (`/.well-known/agent.json`) are the minimum viable discovery contract. Every agent must publish one.
2. **Agent Registry** provides a lookup service for cards across organizational boundaries.
3. **Auth boundary**: use OAuth 2.0 client credentials or mTLS between networks. Tokens must carry both `sub` (user) and `act` (agent) claims.
4. **Gateway pattern**: an API gateway or MCP gateway at the network boundary handles auth, rate limiting, and routing.
5. **Selective disclosure**: Agent Cards can advertise only public capabilities; private ones require authenticated discovery.

---

## Feedback Loops and Self-Improving Agents

### Pattern: Reflection Loop

The foundational self-improvement pattern. Separate generation from evaluation.

- **Generate node**: produces output (report, code, plan, analysis).
- **Reflect node**: critiques the output using a different prompt or model. Pushes structured feedback onto the message history.
- **Conditional edge**: routes back to generate if quality is below threshold, or forward to output.

Design decisions:
- Use a **counter in state** to cap iterations (typically 2-4). Unbounded loops are a cost and latency risk.
- The reflect node should return **structured feedback** (what is wrong, what to fix), not vague "try again."
- Consider using a **different model** for reflection (cheaper model for generation, stronger for evaluation, or vice versa).

LangGraph mapping: `StateGraph` with `generate` and `reflect` nodes, conditional edge checking `iteration_count` and `quality_score`.

### Pattern: Reflexion (Reflection + Memory)

Extends reflection with episodic memory. The agent stores past attempts and their evaluations, then consults them in future iterations.

- After each reflection cycle, store the attempt and feedback in a `BaseStore` namespace.
- On the next run, retrieve past failures to avoid repeating them.
- Useful for agents that improve across sessions, not just within one run.

LangGraph mapping: `BaseStore` with namespace `("reflexion", task_type)` to persist and retrieve past attempts.

### Pattern: Evaluator-Optimizer Loop

A separate evaluator agent scores output against explicit criteria. The optimizer agent uses the scores to refine.

- Best when: evaluation criteria are well-defined (test cases pass, metrics meet threshold, checklist items satisfied).
- The evaluator should be deterministic or near-deterministic. Prefer rule-based scoring over LLM-as-judge when possible.
- Use this when "self-critique" is too subjective and you need measurable improvement.

LangGraph mapping: `StateGraph` with `optimizer` → `evaluator` → conditional edge. Evaluator writes scores to state. Conditional edge checks scores against thresholds.

### Pattern: Language Agent Tree Search (LATS)

Search-based improvement. The agent explores multiple solution paths, evaluates each, and selects the best.

- Combines reflection with tree search (BFS/DFS over solution candidates).
- Most useful for code generation, planning, or puzzle-solving where backtracking is valuable.
- High cost: multiplies LLM calls by branching factor.
- Use only when the task has clear success criteria and the search space is tractable.

LangGraph mapping: `Send()` API to spawn parallel candidate evaluations, then reduce to select the best.

### Design Guidance for Feedback Loops

- Always cap iterations. Default to 3 unless the user has a strong reason for more.
- Log each iteration's score in traces. Without visibility into improvement trajectory, you cannot tune the loop.
- If the first attempt quality is consistently high enough, skip the loop. Reflection has a cost.
- Prefer structured evaluation (rubrics, checklists, test suites) over "does this look good?"

---

## Shared State and Team Resources

### The Problem

A team of agents (e.g., multiple researchers) often needs access to shared resources: previous web searches, reasoning summaries, collected data, intermediate findings. Without shared state, agents duplicate work or miss context from siblings.

### Architecture Options

**1. LangGraph State (within one graph)**

All nodes in a single `StateGraph` naturally share state through the typed state dict. Use `Annotated[list, operator.add]` reducers to accumulate results from multiple nodes.

- Best for: agents in the same graph that need to read each other's output.
- Limitation: state is scoped to one graph execution. Does not persist across runs unless checkpointed.

**2. LangGraph BaseStore (across graphs and threads)**

`BaseStore` provides hierarchical namespaced key-value storage accessible from any node via `get_store()`.

- Namespace design matters. Recommended patterns:
  - `("team", team_id, "web_searches")` for shared web search results
  - `("team", team_id, "summaries")` for reasoning summaries
  - `("user", user_id, "preferences")` for user-specific context
- Best for: cross-thread, cross-agent shared resources that persist across runs.
- Supports vector similarity search for semantic retrieval.
- Access pattern: inject store into graph at compile time, query by namespace in nodes.

**3. External Shared Storage via MCP**

Expose shared resources through an MCP server (e.g., a Redis or PostgreSQL MCP server). Agents access resources as MCP tool calls.

- Best for: resources that are managed by a separate service or team.
- Provides clean API boundary and access control.
- Higher latency than in-process BaseStore.

### Design Guidance

- Default to graph state for intra-graph sharing.
- Use BaseStore for cross-graph or cross-session sharing.
- Use MCP for resources owned by external teams or requiring access control.
- Cache frequently accessed shared resources in state to avoid repeated store lookups.
- Make shared writes idempotent (keyed by content hash or source URL).

---

## Memory Strategy Architecture

### The Five-Tier Memory Model

| Tier | Scope | Lifetime | LangGraph primitive | Example |
|------|-------|----------|--------------------|----|
| **Conversation buffer** | Current thread | One run or thread | Graph state (`messages` key) | Chat history |
| **Working memory** | Current task | One execution | Graph state (typed fields) | Current plan, intermediate findings |
| **Episodic memory** | Past interactions | Cross-session | BaseStore namespaced by user/session | "Last time you asked about X, I found Y" |
| **Semantic memory** | Domain knowledge | Long-lived | BaseStore with vector search, or external vector DB | Embeddings of past research findings |
| **Procedural memory** | Learned behaviors | Long-lived | Skills, tool definitions, prompt templates | "How to write a good research summary" |

### Architecture Decision: Where to Put Memory

- **Embedded in the agent** (BaseStore, checkpointer): simplest, good for single-team ownership. LangGraph's `BaseStore` with `InMemoryStore` or `PostgresStore`.
- **Memory-as-a-service** (Honcho, Mem0, Zep): when memory logic is complex (temporal reasoning, cross-peer representations, automatic fact extraction). Adds a dependency but offloads reasoning about memory.
- **Platform-managed** (AWS AgentCore managed memory, LangGraph Cloud store): when you want zero operational overhead. Least control.

### Design Guidance

- Start with checkpointer + BaseStore. Escalate to a memory service only when you need temporal reasoning, automatic fact extraction, or cross-agent memory sharing that BaseStore cannot handle.
- Separate **what happened** (episodic) from **what is true** (semantic). They have different retrieval patterns.
- Scope memory by user, team, or domain. Global memory is a governance and privacy risk.
- Set TTLs or explicit expiration on memory entries. Stale facts are worse than no facts.
- For memory libraries, see [`../agent-tools-and-platforms/SKILL.md`](../agent-tools-and-platforms/SKILL.md).

---

## Fail Recovery Without Regenerating

### The Problem

Multi-agent workflows can fail at any step (API timeout, model error, rate limit, invalid tool response). Without fail recovery, the entire pipeline must restart from scratch, wasting completed work.

### Pattern: Checkpoint-Based Resume

The primary recovery mechanism. Every node transition is checkpointed. On failure, resume from the last successful checkpoint.

- **Requirement**: a checkpointer (MemorySaver for dev, PostgresSaver for prod) and a stable `thread_id`.
- **How it works**: invoke the graph with the same `thread_id` after failure. LangGraph loads the last checkpoint and continues from there.
- **Pending writes**: if a node fails mid-super-step, other nodes that completed at that step have their writes preserved. On resume, only the failed node re-executes.

### Pattern: Idempotent Node Design

Nodes should produce the same output given the same input. This makes checkpoint-based resume safe.

- Key node outputs by content hash, not by timestamp or random ID.
- If a node writes to an external system (database, API), use upsert or idempotency keys.
- Avoid side effects in node logic that cannot be safely repeated.

### Pattern: Graceful Degradation

When a non-critical agent or tool fails, the workflow continues with reduced quality rather than failing entirely.

- Use try/except in tool-calling nodes with a fallback response (e.g., "Tool X unavailable, proceeding without it").
- Store partial results in state even when an agent fails.
- The final synthesis node should handle missing inputs gracefully.

### Pattern: Human-in-the-Loop Recovery

When automated recovery is not possible, pause and ask a human.

- Use `interrupt()` to pause the graph and surface the failure to the user.
- The user provides guidance (retry with different input, skip this step, provide data manually).
- Resume with `Command(resume=user_response)`.
- Distinguish **information gaps** (agent needs data) from **authority gaps** (agent needs approval).
- Never route to `END` while waiting for approval; use `interrupt()` so the thread stays active.

### Pattern: Retry with Backoff

For transient failures (rate limits, timeouts, network errors).

- LangGraph's `@task` decorator (functional API) supports `retry` policies.
- For StateGraph nodes, wrap the LLM call in a retry decorator with exponential backoff.
- Set max retries (typically 3) and distinguish retryable errors from permanent failures.

### Design Guidance

- Always use a checkpointer in production. MemorySaver is not durable.
- Design state so that each node's output is self-contained and can be verified independently.
- Log checkpoint IDs in traces so you can inspect exactly where a failure occurred.
- For long-running workflows, prefer PostgresSaver or a durable execution engine (Temporal) over in-memory checkpoints.

---

## Dynamic Parallelism at Runtime

### The Problem

You need to spawn N parallel agents where N is not known at compile time. For example: research 5 topics found by a planner, or scrape 12 URLs discovered during execution.

### Pattern: Send() API (Map-Reduce)

LangGraph's `Send()` API enables dynamic fan-out at runtime.

- **Mapper**: a conditional edge function that returns `list[Send(...)]` based on current state. Each `Send(node_name, payload)` spawns one parallel execution.
- **Workers**: standard nodes that process one item each.
- **Reducer**: a state annotation with a reducer function (e.g., `Annotated[list[str], operator.add]`) that merges results from all parallel workers.

Design decisions:
- Workers must be stateless or state-isolated. They receive their input via the `Send` payload, not from shared mutable state.
- The reducer must handle concurrent writes. Use `operator.add` for list accumulation or a custom reducer for deduplication/merging.
- Add a **concurrency budget** when workers call rate-limited APIs (LLM providers, web search APIs). Use semaphores or provider-level rate limiters.

### Pattern: Fan-Out Then Aggregate

A simpler version: a planner node writes a list of subtasks to state, then parallel edges route to workers, and a final aggregator node reads all results.

- Use when the fan-out is static for a given execution (N is known after planning but before worker dispatch).
- LangGraph mapping: conditional edges returning multiple `Send()` calls from the planner node.

### Pattern: Dynamic Subgraph Spawning

When parallel workers need complex multi-step logic, each worker can be a compiled subgraph.

- The parent graph spawns subgraphs as nodes.
- Each subgraph has its own typed state.
- Parent-child state mapping defines how parent state flows into and out of subgraphs.

### Design Guidance

- Default to `Send()` API for dynamic parallelism. It is the idiomatic LangGraph approach.
- Cap parallelism. Spawning 100 LLM calls simultaneously will hit rate limits and degrade latency.
- Make workers idempotent so checkpoint-based resume works correctly after partial fan-out failures.
- Log worker count and individual worker outcomes in traces.

---

## Long-Running Agent Design

### The Problem

Some agents must operate for hours or days: monitoring systems, scheduled research, continuous data collection, multi-day project work. Standard request-response patterns break down.

### Architecture: Session-Based Persistence

- Each long-running task gets a persistent `thread_id` and a durable checkpointer (PostgresSaver).
- The agent can be stopped and resumed at any checkpoint.
- Context compression prevents unbounded message history growth.

### Architecture: Scheduled Execution (Cron Pattern)

- A scheduler triggers the agent at intervals (e.g., every hour, every morning).
- Each invocation resumes the thread, performs its work, and checkpoints.
- Use external schedulers (cron, Celery Beat, cloud scheduler) to trigger graph invocations.
- Keep each invocation bounded in time and scope.

### Architecture: Continuous Agent with Heartbeat

- The agent runs in a persistent process with a heartbeat/health monitor.
- Subagents handle isolated tasks in separate sessions to prevent error compounding.
- Context compression (summarization) keeps the working context manageable.
- Session lineage preservation ensures the agent's identity and learned context survive compression.

### Design Decisions

- **Context window management**: as conversations grow, compress old messages into summaries. Store full history in archival memory (BaseStore or external). Keep the active window small enough for reliable reasoning.
- **Session isolation**: use separate sessions for separate tasks. A single monolithic session accumulates errors and irrelevant context.
- **Heartbeat and monitoring**: long-running agents need health checks. Emit heartbeat events and set up alerting for unresponsive agents.
- **Cost control**: cap LLM calls per time period. Monitor token usage. Use cheaper models for routine operations and expensive models for critical decisions.
- **Identity persistence**: use files or store entries (MEMORY.md pattern, BaseStore entries) to maintain the agent's learned preferences and capabilities across sessions.

### LangGraph Mapping

- `PostgresSaver` for durable checkpoints that survive process restarts.
- `BaseStore` for cross-session memory and learned context.
- `interrupt()` for human checkpoints in multi-day workflows.
- Functional API `@entrypoint` with `previous` parameter for accessing prior run results.

---

## Voice-to-Agent Delegation

### The Problem

A real-time conversation system (voice or chat) needs to delegate complex, time-consuming tasks (deep research, data analysis, multi-step workflows) to background agents and retrieve results without blocking the conversation.

### Architecture: Dual-Agent Pattern

Inspired by VoiceAgentRAG research:

- **Fast Talker** (foreground): handles real-time conversation, answers quick questions, manages turn-taking. Low latency is critical.
- **Slow Thinker** (background): monitors conversation context, predicts what the user will need next, pre-fetches data, and runs complex workflows. Latency tolerance is high.

Communication flow:
1. User speaks → STT → Fast Talker processes.
2. Fast Talker detects a complex request → delegates to Slow Thinker via A2A `message/send` or internal task queue.
3. Fast Talker acknowledges delegation ("Let me look into that...") and continues conversation.
4. Slow Thinker completes → pushes result to shared store or sends notification.
5. Fast Talker retrieves result on next turn or proactively surfaces it.

### Architecture: Cascaded Pipeline with Agent Handoff

For systems where the voice pipeline (STT → LLM → TTS) is the primary interface:

- Voice pipeline runs as a Pipecat or LiveKit Agents process.
- Agent tasks run as separate LangGraph services.
- Handoff mechanism: voice pipeline calls agent service via HTTP or A2A, gets `202 Accepted` with a task ID, polls or subscribes for completion.
- Result integration: voice pipeline receives a structured summary and synthesizes a spoken response.

### Design Decisions

- Keep the voice pipeline process separate from agent compute. Voice needs sub-second latency; agents may run for minutes.
- Use SSE or webhooks for result delivery from agent to voice pipeline.
- Cache frequently needed context in a fast store (Redis, in-memory) so the Fast Talker does not wait for database queries.
- Design agent responses as concise summaries suitable for spoken delivery, not long reports.

---

## Agent Skills and Capability Extension

### The Problem

Agents need to acquire new capabilities without redeployment. A base agent should be extensible with domain-specific skills, tools, and workflows.

### The Skills Model

Skills are modular capability packages that extend an agent's behavior. They complement MCP tools:

- **MCP provides connectivity**: standardized access to external systems, tools, and data.
- **Skills provide expertise**: domain knowledge, workflow logic, evaluation criteria, and best practices that teach the agent how to use those connections effectively.

A skill is not just a prompt. It is a bundle of:
- Instructions (what to do and how)
- Metadata (when to activate, what it requires)
- Optional resources (templates, scripts, reference data)
- Optional tool restrictions or model preferences

### Design: Dynamic Capability Registration

- Agents maintain a skill registry (file-based, BaseStore, or external service).
- Skills are discovered at startup or dynamically loaded at runtime.
- The agent's system prompt or tool list is augmented based on active skills.
- Skill activation can be automatic (based on task type) or explicit (user selects).

### Design: Composable Skill Architecture

- Skills should be composable: a "research" skill can combine with a "writing" skill without conflicts.
- Each skill has a clear activation trigger and a non-overlapping responsibility.
- Skills can reference other skills for delegation (e.g., "for test implementation, use the tester skill").

### Compatibility with Claude Skills and Cursor Agent Skills

Claude Skills and Cursor Agent Skills follow a filesystem-based pattern:
- `SKILL.md` file with frontmatter (name, description/triggers) and instructions.
- Instructions are injected into the agent's context when triggered.
- Skills can reference shell commands, file templates, and other skills.

To make LangGraph agents skill-compatible:
- Store skills as structured documents in BaseStore or filesystem.
- Load relevant skills into the agent's system prompt based on task classification.
- Expose skill management as MCP tools (list skills, activate skill, deactivate skill).

---

## Protocol Selection

### Decision Matrix

| Need | Protocol | Why |
|------|----------|-----|
| Agent calls a tool, database, or API | **MCP** | Typed, stateless tool interface. The caller thinks "use a capability." |
| Agent collaborates with another agent | **A2A** | Task-oriented, supports long-running work, artifacts, and discovery. |
| Tightly coupled internal helper | **Direct HTTP/gRPC** | Simpler to debug and test than A2A for known, stable endpoints. |
| Work must outlive an HTTP request | **Queue + Worker** | Retries, throttling, backpressure, dead-letter handling. |
| Real-time progress updates | **SSE / WebSocket** | Stream task status, LLM tokens, and partial artifacts. |
| Offline/disconnected clients | **Webhooks / Push** | Deliver results when the client is not connected. |
| Cross-network agent discovery | **Agent Cards + Registry** | Capability-based discovery with auth metadata. |

### Protocol Combination Rules

- A2A is the agent boundary; MCP is the tool boundary. Use both when needed.
- Every A2A agent must publish an Agent Card at `/.well-known/agent.json`.
- Do not use A2A to wrap a CRUD call. A tool is not a peer.
- Do not use MCP as a substitute for long-lived workflow state.
- Prefer `message/send` for request-response; use `message/stream` only when streaming materially improves UX.

---

## LangGraph Primitive Mapping

Quick reference for mapping patterns to LangGraph APIs. For code templates, see [`../langgraph-example-implementation/SKILL.md`](../langgraph-example-implementation/SKILL.md).

| Pattern | LangGraph API |
|---------|---------------|
| Sequential pipeline | `StateGraph` with linear `add_edge()` |
| Conditional routing | `add_conditional_edges()` with routing function |
| Parallel fan-out (static) | Multiple edges from one node |
| Parallel fan-out (dynamic) | `Send()` API from conditional edge |
| Result aggregation | State field with `Annotated[list, operator.add]` reducer |
| Reflection loop | Conditional edge looping back from evaluator to generator |
| Human-in-the-loop | `interrupt()` + `Command(resume=value)` |
| Checkpoint/resume | `checkpointer` (MemorySaver, PostgresSaver) + `thread_id` |
| Cross-session memory | `BaseStore` with namespaced keys via `get_store()` |
| Subgraph composition | Compiled graph added as node with state mapping |
| Long-running with resume | `PostgresSaver` + `interrupt()` for human pauses |
| Scheduled execution | External scheduler triggering `graph.ainvoke()` with same `thread_id` |
| Retry with backoff | `@task(retry=RetryPolicy(...))` (functional API) |
| Async task execution | `@task` decorator (functional API) returning futures |
| Streaming progress | `graph.astream()` with `stream_mode="updates"` |

---

## Review Checklist

When reviewing or designing an agent system, verify:

1. **Pattern fit**: the chosen pattern is the simplest one that satisfies the requirement. Can you justify why a simpler pattern would not work?
2. **Service boundaries**: each agent or service has one clear responsibility. No agent does two jobs.
3. **Protocol fit**: A2A for agents, MCP for tools, HTTP for internal helpers, queues for durable work.
4. **State shape**: state is typed, minimal, and separates public API schemas from internal graph state.
5. **Memory architecture**: memory tiers are explicit. Short-term, working, episodic, and semantic memory are stored appropriately.
6. **Fail recovery**: the workflow can resume from checkpoint after failure. Nodes are idempotent. Critical steps have retry policies.
7. **Parallelism**: dynamic fan-out uses `Send()` with concurrency budgets. Reducers handle concurrent writes correctly.
8. **Long-running safety**: context compression prevents unbounded growth. Sessions are isolated. Heartbeats are monitored.
9. **Feedback quality**: reflection loops are capped. Evaluation criteria are measurable. Improvement trajectory is logged.
10. **Async model**: the design does not block the event loop. Long work uses durable execution, not synchronous waits.
11. **Observability**: LangSmith tracing, verbose logs, health checks, and delegation chains are visible.
12. **Security**: agent identities are explicit. Tokens carry `sub` and `act` claims. Tools check scope before execution.

## Recommendation Format

When advising, answer in this order:

1. **Recommended pattern** and protocol.
2. **Why** it is the simplest acceptable choice.
3. **How** it maps to LangGraph primitives (without writing code templates).
4. **Main trade-off** or operational risk.
5. **Escalation trigger**: what would justify moving to a more complex pattern.
6. **Reference**: link to relevant pattern section above or external resource.

## Key References

### Protocols
- [A2A protocol specification](https://a2a-protocol.org/)
- [A2A Agent Discovery](https://a2a-protocol.org/dev/topics/agent-discovery)
- [A2A Streaming and Async](https://a2a-protocol.org/dev/topics/streaming-and-async)
- [MCP specification](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP Enterprise Auth](https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization)

### LangGraph
- [LangGraph concepts: persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph concepts: streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
- [LangGraph concepts: interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph functional API](https://docs.langchain.com/oss/python/langgraph/functional-api)
- [LangGraph Send API for map-reduce](https://docs.langchain.com/oss/python/langgraph/how-to-guides/map-reduce)
- [LangGraph application structure](https://docs.langchain.com/oss/python/langgraph/application-structure)
- [LangGraph durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)

### Research
- [Survey of Agent Interoperability Protocols](https://huggingface.co/papers/2505.02279)
- [Survey of LLM-Driven Agent Communication](https://huggingface.co/papers/2506.19676)
- [Evolution of AI Agent Registry Solutions](https://arxiv.org/html/2508.03095v2)
- [VoiceAgentRAG: Dual-Agent Architecture for Voice](https://arxiv.org/abs/2603.02206v2)
- [Building Enterprise Realtime Voice Agents](https://arxiv.org/abs/2603.05413)

### Security and Identity
- [Microsoft Zero-Trust Agents](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/zero-trust-agents-adding-identity-and-access-to-multi-agent-workflows/4427790)
- [OAuth for AI agents IETF draft](https://datatracker.ietf.org/doc/html/draft-oauth-ai-agents-on-behalf-of-user-01)
- [OpenAI: Designing agents to resist prompt injection](https://openai.com/index/designing-agents-to-resist-prompt-injection)

### Architecture
- [A2A + MCP Hybrid Architecture Guide](https://jangwook.net/en/blog/en/a2a-mcp-hybrid-architecture-production-guide/)
- [Temporal: Durable Execution meets AI](https://temporal.io/blog/durable-execution-meets-ai-why-temporal-is-the-perfect-foundation-for-ai)
- [AGNTCY Agent Directory Service](https://docs.agntcy.org/dir/overview/)

For platform comparisons, library recommendations, and reference implementations, see [`../agent-tools-and-platforms/SKILL.md`](../agent-tools-and-platforms/SKILL.md).
