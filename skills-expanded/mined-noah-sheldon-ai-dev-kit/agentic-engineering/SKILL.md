---
name: agentic-engineering
description: Agentic engineering patterns — agent orchestration, delegation contracts, multi-agent system design, memory graph usage, streaming/async pipelines, OOP decomposition, hierarchical delegation, context window management, and agent failure recovery.
origin: AI Dev Kit
---

# Agentic Engineering

Design, orchestrate, and operate multi-agent systems with clear delegation contracts,
OOP decomposition, memory graphs, and robust failure recovery.

## When to Use

- Building multi-agent systems where work must be delegated across specialized agents.
- Designing hierarchical agent topologies (orchestrator → specialists → tools).
- Implementing agent-to-agent communication, shared memory, or context passing.
- Debugging agent failures, context overflow, or delegation loops.
- Optimizing streaming/async pipelines for latency and throughput.
- Deciding between agent delegation, workflow orchestration, or direct tool-calling.

## Core Concepts

### 1. Agent vs Workflow vs Tool-Calling

Choose the right abstraction for the job:

| Pattern | When to Use | Example |
|---|---|---|
| **Tool-calling** | Single LLM call with structured function calls | Extract entities from text |
| **Workflow** | Deterministic DAG of steps with fixed routing | ETL pipeline: ingest → transform → load |
| **Agent** | LLM decides next action dynamically based on context | Research agent that plans its own queries |
| **Multi-agent** | Parallel specialists with an orchestrator for synthesis | Code review: security + performance + style agents |

**Decision tree:**
```
Is the task deterministic with fixed steps? → Workflow (DAG)
Does the LLM need to choose actions at runtime? → Agent
Can a single LLM call with tools handle it? → Tool-calling
Are there independent subtasks? → Multi-agent with parallel specialists
```

### 2. Delegation Contracts

Every agent interaction must follow a typed contract:

```python
from dataclasses import dataclass
from typing import Any, Optional
from enum import Enum


class AgentStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class AgentRequest:
    """Input contract for a delegated agent task."""
    task: str
    context: dict[str, Any]
    constraints: dict[str, Any]
    max_tokens: int = 4000
    timeout_seconds: int = 120


@dataclass
class AgentResponse:
    """Output contract from a delegated agent."""
    status: AgentStatus
    result: Any
    reasoning: str
    tokens_used: int
    follow_up_tasks: list[str]
    error: Optional[str] = None


# Example delegation
request = AgentRequest(
    task="Review the security implications of the auth module",
    context={"file_path": "src/auth.py", "change_type": "new"},
    constraints={"focus_areas": ["injection", "token_handling", "secrets"]},
    max_tokens=3000,
    timeout_seconds=60,
)
```

### 3. Multi-Agent System Design — OOP Decomposition

Model agents as classes with clear interfaces:

```python
from abc import ABC, abstractmethod
from typing import Protocol


class MemoryGraph(Protocol):
    """Shared memory layer agents can read/write."""
    def get(self, key: str) -> Any: ...
    def put(self, key: str, value: Any, ttl: int = 3600) -> None: ...
    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]: ...


class Agent(ABC):
    """Base agent with lifecycle hooks."""

    def __init__(self, name: str, memory: MemoryGraph, llm_client):
        self.name = name
        self.memory = memory
        self.llm = llm_client
        self.history: list[dict] = []

    @abstractmethod
    async def execute(self, request: AgentRequest) -> AgentResponse: ...

    def log(self, event: str, details: dict) -> None:
        self.history.append({"event": event, "details": details, "ts": time.time()})


class SecurityReviewerAgent(Agent):
    async def execute(self, request: AgentRequest) -> AgentResponse:
        file_content = self.memory.get(request.context.get("file_path", ""))
        prompt = self._build_review_prompt(file_content, request.constraints)
        result = await self.llm.chat(prompt)
        return AgentResponse(
            status=AgentStatus.SUCCESS,
            result=result["findings"],
            reasoning=result["reasoning"],
            tokens_used=result["usage"]["total_tokens"],
            follow_up_tasks=[],
        )
```

### 4. Hierarchical Delegation

```
┌──────────────────────────────────────┐
│          Orchestrator Agent          │  ← Plans, delegates, synthesizes
│   "Plan → Delegate → Review → Merge" │
└──────────────┬───────────────────────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
  ┌──────┐ ┌──────┐ ┌──────┐
  │Code  │ │Sec   │ │Perf  │     ← Specialist agents (run in parallel)
  │Agent │ │Agent │ │Agent │
  └──────┘ └──────┘ └──────┘
```

**Orchestrator implementation:**

```python
class OrchestratorAgent(Agent):
    def __init__(self, memory: MemoryGraph, llm_client, specialists: dict[str, Agent]):
        super().__init__("orchestrator", memory, llm_client)
        self.specialists = specialists

    async def execute(self, request: AgentRequest) -> AgentResponse:
        # Step 1: Plan — decide which specialists to invoke
        plan = await self._create_plan(request)

        # Step 2: Delegate — run independent specialists in parallel
        import asyncio
        tasks = []
        for specialist_name, sub_task in plan:
            agent = self.specialists[specialist_name]
            tasks.append(agent.execute(AgentRequest(
                task=sub_task,
                context=request.context,
                constraints=request.constraints,
            )))
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Step 3: Synthesize — merge findings
        synthesis = await self._synthesize(results, request)
        return AgentResponse(
            status=AgentStatus.SUCCESS,
            result=synthesis,
            reasoning="Aggregated from " + len(plan) + " specialist reviews",
            tokens_used=sum(r.tokens_used for r in results if isinstance(r, AgentResponse)),
            follow_up_tasks=synthesis.get("follow_ups", []),
        )
```

### 5. Memory Graph Usage

Agents share a structured memory layer:

```python
class InMemoryGraph(MemoryGraph):
    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}
        self._embeddings: dict[str, list[float]] = {}

    def put(self, key: str, value: Any, ttl: int = 3600) -> None:
        self._store[key] = (value, time.time() + ttl)

    def get(self, key: str) -> Any:
        entry = self._store.get(key)
        if entry and time.time() < entry[1]:
            return entry[0]
        self._store.pop(key, None)
        return None

    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        # Semantic search over stored embeddings
        query_vec = self._embed(query)
        scored = []
        for k, vec in self._embeddings.items():
            score = cosine_similarity(query_vec, vec)
            scored.append((k, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
```

**Memory types by scope:**
- **Session memory**: Short-lived, per-conversation (TTL = session duration)
- **Task memory**: Per-agent-task, cleared after response synthesis
- **Shared memory**: Cross-agent, persisted for the duration of the orchestration
- **Long-term memory**: Vector store across sessions for pattern learning

### 6. Streaming/Async Pipelines

```python
async def stream_agent_pipeline(
    agents: list[Agent],
    request: AgentRequest,
) -> AsyncGenerator[str, None]:
    """Stream partial results from each agent as they complete."""
    import asyncio

    async def run_agent(agent: Agent):
        response = await agent.execute(request)
        return (agent.name, response)

    tasks = [asyncio.create_task(run_agent(a)) for a in agents]
    for coro in asyncio.as_completed(tasks):
        name, response = await coro
        yield f"[{name}] status={response.status.value} tokens={response.tokens_used}\n"
        if response.result:
            yield f"{response.result}\n"
```

### 7. Context Window Management

**Strategies to stay within token limits:**

| Strategy | Description | When to Apply |
|---|---|---|
| **Sliding window** | Keep only the last N messages | Long conversations |
| **Summarization** | Compress early turns into a summary | When history > 75% of context |
| **Chunked retrieval** | Load context in chunks, not all at once | Large codebase or doc references |
| **Hierarchical context** | System prompt → session summary → current turn | Always |
| **Eager eviction** | Remove stale or low-relevance entries | Every turn |

```python
def prune_context(
    messages: list[dict],
    max_tokens: int = 100000,
    summary_threshold: int = 80000,
) -> list[dict]:
    current_tokens = count_tokens(messages)

    if current_tokens > summary_threshold:
        # Summarize early messages, keep recent ones verbatim
        summary = summarize(messages[:-5])
        return [{"role": "system", "content": summary}] + messages[-5:]

    if current_tokens > max_tokens * 0.9:
        # Hard prune to last 3 messages
        return messages[-3:]

    return messages
```

### 8. Agent Failure Modes and Recovery

```python
class AgentExecutionError(Exception):
    def __init__(self, agent_name: str, reason: str, retryable: bool = False):
        self.agent_name = agent_name
        self.reason = reason
        self.retryable = retryable
        super().__init__(f"Agent '{agent_name}' failed: {reason}")


async def execute_with_recovery(
    agent: Agent,
    request: AgentRequest,
    max_retries: int = 2,
) -> AgentResponse:
    """Execute an agent with exponential backoff retry and fallback."""
    for attempt in range(max_retries + 1):
        try:
            response = await asyncio.wait_for(
                agent.execute(request),
                timeout=request.timeout_seconds,
            )
            if response.status == AgentStatus.FAILED and attempt < max_retries:
                delay = 2 ** attempt
                await asyncio.sleep(delay)
                continue
            return response
        except asyncio.TimeoutError:
            if attempt < max_retries:
                continue
            return AgentResponse(
                status=AgentStatus.TIMEOUT,
                result=None,
                reasoning=f"Agent timed out after {request.timeout_seconds}s",
                tokens_used=0,
                follow_up_tasks=[],
                error="timeout",
            )
        except AgentExecutionError as e:
            if not e.retryable or attempt == max_retries:
                return AgentResponse(
                    status=AgentStatus.FAILED,
                    result=None,
                    reasoning=e.reason,
                    tokens_used=0,
                    follow_up_tasks=[],
                    error=str(e),
                )
```

**Common failure modes:**
- **Hallucination**: Agent invents facts — add retrieval constraints and confidence scoring
- **Token overflow**: Context exceeds window — apply pruning before execution
- **Delegation loop**: Agents keep delegating to each other — set max depth (default: 3)
- **Tool misuse**: Agent calls wrong tool — add tool selection guardrails in system prompt
- **Partial results**: Agent returns incomplete output — implement chunked retry with "continue from" prompt

## Anti-Patterns

- **God orchestrator** — one agent that does everything defeats the purpose of multi-agent design
- **Implicit contracts** — never pass vague natural language without structured request/response types
- **Unbounded memory** — memory graphs without TTL or eviction grow until context overflow
- **Sequential specialists** — run independent agents in parallel with `asyncio.gather`
- **No failure handling** — agents will fail; always implement retry + fallback + timeout
- **Shared mutable state** — use copy-on-read for context; never let agents mutate shared memory directly
- **Deep delegation trees** — limit hierarchy depth to 3 levels to avoid cascade failures

## Best Practices

1. **Always define typed contracts** (`AgentRequest` / `AgentResponse`) for delegation boundaries.
2. **Run independent specialists in parallel** using `asyncio.gather` with `return_exceptions=True`.
3. **Implement the orchestrator pattern**: Plan → Delegate (parallel) → Synthesize.
4. **Set hard limits**: max delegation depth (3), max retries (2), max tokens per agent call.
5. **Use memory graphs with TTL** and automatic eviction to prevent context overflow.
6. **Stream partial results** so the orchestrator can surface progress even when agents are slow.
7. **Prune context aggressively** at 80% of window; summarize at 75%.
8. **Log every delegation** with request, response, tokens, and status for observability.
9. **Test agents in isolation** before composing them in multi-agent pipelines.
10. **Design for failure first** — happy path is easy; recovery is what makes systems production-ready.

## Related Skills

- `autonomous-agent-harness` — Agent lifecycle, session isolation, and performance tracking
- `dmux-workflows` — Routing tasks to appropriate agents and skills
- `continuous-agent-loop` — Event-driven agent activation and backpressure handling
- `autonomous-loops` — Recurring agent task automation with monitoring
- `token-budget-advisor` — Context window allocation and cost estimation
