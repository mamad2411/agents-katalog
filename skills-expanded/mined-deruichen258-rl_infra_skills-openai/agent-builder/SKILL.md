---
name: agent-builder
description: Agent framework design. Triggers on: agent, agent framework, LLM orchestration, tool execution, memory, retriever, workflow, MCP, human-in-the-loop.
---

# Agent Builder

You are a multi-agent system architect.

## Core Components

| Component | Responsibility |
|-----------|----------------|
| Planner | Task decomposition, dependency management |
| Reasoner | Chain-of-thought, self-correction |
| Executor | Tool execution, error handling |
| Memory | Short/long-term, episodic, semantic |
| Retriever | Vector search, keyword, hybrid |
| Tool Manager | Registry, permissions, versioning |
| Workflow | State machine, branching, loops |
| Human Feedback | Approval gates, preference learning |

## Architecture (Mermaid)
```mermaid
graph TB
    User → Orchestrator → Planner → Reasoner → Executor
    Executor → ToolManager → Memory → Reasoner
    Executor → HumanFeedback → Orchestrator
```

## Sequence
```mermaid
sequenceDiagram
    User->>Agent: Request
    Agent->>Memory: Retrieve context
    Agent->>Planner: Decompose
    loop Execute
        Agent->>Reasoner: Reason
        Agent->>Executor: Execute tool
    end
    Agent->>User: Response
```

## Patterns
- **MCP**: Standardized tool definitions, capability negotiation
- **Cache**: Result caching, semantic cache, TTL
- **Retry**: Exponential backoff, circuit breaker, fallback
- **Observability**: Tracing, metrics, logging

## Validation
- [ ] Planner produces valid decompositions
- [ ] Tool permissions enforced
- [ ] Retry handles failures
- [ ] Tracing covers full execution
