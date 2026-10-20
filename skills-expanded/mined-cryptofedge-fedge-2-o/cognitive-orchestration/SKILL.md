---
name: cognitive-orchestration
description: 'Advanced multi-agent orchestration and cognitive architecture management. Use when: (1) designing complex agent loops, (2) implementing Supervisor/Worker patterns, (3) managing isolated context windows between subagents, (4) performing Dreaming audits for long-term memory, (5) routing tasks based on cost-of-reversal, (6) setting up MCP servers for tool standardized access.'
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "anyBins": ["claude", "mcp"] },
        "patterns": ["Supervisor", "Orchestrator-Worker", "ReflexGrad", "Context-Isolation"]
      },
  }
---

# Cognitive Orchestration & Advanced AI Logic

This skill governs the high-level reasoning and architectural delegation of FEDGE 2.O. It is the "Brain" of the Lead Agent.

## Core Principles

### 1. Supervisor Topology
The Lead Agent acts as the **Supervisor**. It does not do the work; it **delegates**.
- **Input:** Complex user goal.
- **Decomposition:** Break into sub-tasks with clear success criteria.
- **Dispatch:** Send to specialized subagents (e.g., `credit-agent`, `trustfund-agent`).
- **Synthesis:** Gather results and present a unified answer.

### 2. Context Isolation
Subagents should **never** see the Lead's full context (SOUL.md, MEMORY.md, etc.) unless strictly necessary.
- Protects security and privacy.
- Reduces token burn and "context noise."
- Ensures specialists focus only on their domain.

### 3. The "Stuck-Counter"
If a subagent tool call fails twice or enters a loop:
- **Lead Interception:** The Lead Agent stops the subagent.
- **Re-planning:** Evaluate if the tool is broken, the prompt is bad, or the strategy is impossible.
- **Escalation:** Ask Fellito for guidance if re-planning fails.

### 4. Dreaming & Memory Curation
Long-term memory is not a dump; it is a **curated library**.
- **Audit:** Review last 72 hours of logs.
- **Extract:** Find durable facts (e.g., "Mando's new single drops Friday").
- **Promote:** Write those facts to `MEMORY.md`.
- **Discard:** Remove conversational noise.

## Tools & Protocols

- **MCP (Model Context Protocol):** Use for standardized tool access across environments.
- **A2A (Agent-to-Agent):** Standardized JSON headers for communication between subagents.
- **ReflexGrad:** Dynamic TODO lists that update based on sub-task outcomes.

---

## Learnings (August 2026 Upgrade)

- **Cost-of-Reversal:** Always use high-reasoning (Opus/4.5) for tasks that cannot be undone (e.g., deploying code, public posts).
- **persona-gating:** Use subagents with strict personas to prevent "helpfulness" from overriding "security" (e.g., a security auditor subagent).
- **hierarchical-rag:** Don't just search text; navigate the **Knowledge Graph** of Fellito's ecosystem.
