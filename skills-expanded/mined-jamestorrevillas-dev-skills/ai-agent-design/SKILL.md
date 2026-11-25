---
name: ai-agent-design
description: Use this skill when building AI agents, designing multi-agent systems, integrating LLMs into applications, building RAG pipelines, working with vector databases, implementing MCP servers, or designing agent communication and orchestration patterns. Trigger on keywords like: agent, LLM, RAG, embeddings, vector DB, orchestration, tool use, memory, intent clarification, MCP, LangChain, LangGraph, CrewAI, AutoGen, Microsoft Agent Framework.
---

# AI Agent Design

## Core Philosophy

Agents are not magic — they are systems with inputs, outputs, memory, tools, and decision logic. Design them with the same rigor as any production software. Every agent should have a clear purpose, defined boundaries, and explicit failure modes.

## Agent Design Principles

### 1. Clarify Intent Before Acting
An agent must ask clarifying questions when the user's intent is ambiguous — before executing any irreversible action. Use this pattern:
- Is the goal clear? If not, ask one focused question.
- Are the constraints known? (scope, output format, data sources)
- What does success look like?

### 2. Specification Before Code
Before writing agent logic, generate a spec or task list file:
1. Define the agent's role and responsibilities
2. List all tools it needs access to
3. Define input/output contracts
4. Identify failure modes and fallback behavior
5. Then write the code

### 3. Single Responsibility
Each agent should do one thing well. Prefer a team of specialized agents over one general-purpose agent.

---

## Orchestration Patterns

| Pattern | When to Use | Description |
|---|---|---|
| Sequential | Linear pipelines | Agents chain in fixed order (draft → review → publish) |
| Supervisor | Complex multi-module tasks | Lead agent routes to specialized workers |
| ReAct | Autonomous problem solving | Combines reasoning (Thought) + acting (Tool Use) |
| Group Chat | Collaborative tasks | Multi-agent communication with human oversight |
| DAG | Stateful workflows | Directed acyclic graph for cyclical, stateful orchestration |

---

## Framework Selection Guide

| Framework | Best For | Status |
|---|---|---|
| **LangGraph** | Complex stateful agents, cyclical workflows, multi-agent orchestration, production-grade | ✅ Active — GA May 2025 |
| **LangChain** | Simple RAG pipelines, linear workflows, quick prototypes | ✅ Active — use for RAG, not for agents |
| **CrewAI** | Role-based multi-agent teams ("Manager", "Researcher", "Writer") | ✅ Active |
| **Microsoft Agent Framework** | Enterprise agents in Azure ecosystem — replaces AutoGen + Semantic Kernel | ✅ Active — Public Preview Oct 2025, GA targeted Q1 2026 |
| **AutoGen** | Legacy — still works but no new features | ⚠️ Maintenance mode since Oct 2025 |
| **Custom (MCP)** | Lightweight, portable, interoperable agent tools via open standard | ✅ Active |

### LangChain vs LangGraph — Which to Use
The LangChain team now explicitly recommends this split:
- **LangGraph** → for agents: stateful, cyclical, multi-agent, long-running tasks
- **LangChain** → for RAG and linear pipelines: simple document Q&A, step-by-step transforms

LangGraph is built on top of LangChain — you can use both together, starting with LangChain and dropping to LangGraph when you need more control.

---

## RAG Pipeline Design

### Standard RAG Flow
```text
User Query → Embed Query → Vector Search → Retrieve Chunks → Augment Prompt → LLM → Response
```

### Chunking Strategy (2026 Best Practice)
- Use **semantic chunking** — break on meaning, not character count
- Chunk size: 256–512 tokens for precision; 1024 for narrative content
- Always include metadata: source, page, section, timestamp

### Hybrid Search (Recommended)
Combine dense vectors (semantic) + sparse vectors (keyword) for best recall:
```text
Final Score = α × Dense Score + (1 - α) × Sparse Score
```

### Vector Database Selection
| DB | Best For |
|---|---|
| pgvector | Existing PostgreSQL stack, simple use cases |
| Pinecone | Managed, production-scale, minimal ops |
| Weaviate | Multi-modal, hybrid search built-in |
| Milvus | High-performance, self-hosted, large scale |
| Chroma | Local dev, prototyping |

---

## Agent Memory Architecture

| Type | Description | Implementation |
|---|---|---|
| In-context | Current conversation window | Chat history array |
| External short-term | Session-scoped memory | Redis / in-memory store |
| External long-term | Persistent across sessions | Vector DB + metadata |
| Episodic | Summarized past interactions | Summarization chain → vector store |

**Context Rot Warning:** Long context windows degrade agent quality over time. Implement a summarization step every N turns to maintain relevance.

---

## Tool Use & Function Calling

### Tool Definition Pattern
Every tool needs:
```yaml
name: descriptive_tool_name
description: When to use this tool and what it does (be explicit)
parameters:
  - name: param_name
    type: string
    description: What this parameter expects
    required: true
```

### Tool Use Best Practices
- Tools should be **idempotent** where possible
- Always validate tool outputs before passing to the next step
- Implement timeouts and retries for external tool calls
- Log all tool invocations for debugging

---

## Agent Communication Patterns

### Intent Clarification Protocol
When an agent receives an ambiguous request:
1. **Identify the ambiguity** — what specifically is unclear?
2. **Ask one question** — the most important one, not all of them
3. **Propose a default** — "I'll assume X unless you tell me otherwise"
4. **Confirm before irreversible actions** — always ask before deleting, publishing, or sending

### Progress Reporting
For long-running tasks, agents should report:
```text
[Step 1/4] Fetching documents... ✓
[Step 2/4] Chunking and embedding... ✓
[Step 3/4] Querying vector store...
```

### Error Communication
```text
✗ Tool failed: [tool_name]
Reason: [specific error]
Fallback: [what I'm doing instead]
```

---

## MCP (Model Context Protocol)

MCP is the open standard for connecting agents to external tools and data sources. Use it when building portable, interoperable agent tools.

### MCP Server Structure
```text
my-mcp-server/
├── server.py (or index.ts)
├── tools/
│   └── my_tool.py
└── README.md
```

### When to Use MCP vs Direct Integration
- Use **MCP** when the tool needs to be reusable across multiple agents/platforms
- Use **direct integration** for project-specific, one-off tool implementations

See `mcp-builder` skill for detailed MCP server implementation guidance.

---

## Security & Safety

- **Never** allow agents to execute arbitrary code without sandboxing
- Implement **rate limiting** on all LLM API calls
- **Validate and sanitize** all inputs before passing to tools
- Log all agent decisions for auditability
- Implement **guardrails** to prevent runaway token costs or recursive loops
- Use **system prompt injection protection** — separate user input from system instructions with clear delimiters

---

## Resilient Agent Design (Self-Healing)

Agents fail in production. Design for recovery from the start.

### Validate-and-Retry Loop (LoopAgent Pattern)
```text
Generate output → Validate output → If invalid: feedback + regenerate
Max iterations: 3  ← circuit breaker to prevent infinite loops
```

### Plan–Validate–Execute–Observe–Replan
```text
PLAN:     Generate plan, check feasibility before acting
EXECUTE:  Take action
OBSERVE:  Did it succeed? Check outputs, run tests
REPLAN:   If observation shows failure → adjust and retry
STOP:     If max retries hit → report failure clearly, ask for help
```

### Agent Fallback Hierarchy
```text
Primary approach fails → Try alternative approach
Alternative fails     → Request clarification from developer
Clarification absent  → Safe default action or graceful stop
```

### Output Validation Before Presenting
- Run tests/lint on generated code before presenting
- Verify output format matches requirements
- Use a separate validator step (different model or prompt) to check generator output
- Never present unverified output as done

### Circuit Breaker for Agents
Set hard limits to prevent runaway behavior:
- Max tool call iterations per task (e.g. 10)
- Max token spend per session
- Max retries per failing step (e.g. 3)
- Timeout per tool invocation

See `self-healing-mindset` skill for the full resilience philosophy and code patterns.
