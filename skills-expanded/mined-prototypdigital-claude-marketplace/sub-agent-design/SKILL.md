---
profiles:
  - agentic
name: sub-agent-design
description: Design a sub-agent system — scope responsibilities, define communication contracts, wire orchestration, and add integration tests.
---

# sub-agent-design

Use this skill when you need to break a complex agentic task into a coordinated set of sub-agents with defined responsibilities and communication contracts.

## Triggers

- A single agent is doing too many things (context overloads, inconsistent outputs, hard-to-test)
- A workflow has parallelizable phases that run independently and could be done concurrently
- An orchestrator needs to delegate specialized work (code review, search, synthesis) to purpose-built agents
- A new agentic feature requires planning before implementation

## Required behavior

### Phase 1 — Scope the work

1. State the top-level goal the system must achieve in one sentence.
2. List all distinct responsibilities required. Group related items.
3. Identify which responsibilities are parallelizable (no data dependency between them).
4. Draw the agent topology: which agents exist, what each does, who calls whom.

Output format:

```text
Orchestrator: <name> — routes tasks, aggregates results, handles errors
├── Sub-agent A: <name> — <one-line responsibility>
├── Sub-agent B: <name> — <one-line responsibility>
└── Sub-agent C: <name> — <one-line responsibility> [runs after A]
```

### Phase 2 — Define communication contracts

For each agent, document the interface:

```text
Agent: <name>
Input:  { <field>: <type>, ... }
Output: { <field>: <type>, ... }
Preconditions: <what must be true before calling>
Postconditions: <what the caller can rely on>
Error: <what is returned/thrown on failure; retry policy>
```

Reject ambiguous types — `object` and `any` are not contracts.

### Phase 3 — Implement

1. Write each agent as a separate file under `llm/agents/`.
2. Wire the orchestrator: call agents in topological order; run parallel agents concurrently.
3. Add a typed schema for each agent's input and output (TypeScript types or JSON Schema).
4. Handle partial failures explicitly — one sub-agent failing should not silently corrupt the final output.

### Phase 4 — Integration test

For each critical path through the agent graph:

1. Write a deterministic test fixture (fixed input, no external calls).
2. Assert the tool call sequence (which agent was called, in what order, with what input).
3. Assert the final output matches the postcondition.
4. Add one failure-path test: one agent returns an error — assert the orchestrator handles it correctly.

## Anti-patterns to flag

- An agent that does both retrieval and synthesis (split into two)
- Shared mutable state between parallel agents (use message passing instead)
- An orchestrator that retries indefinitely on transient errors (add a max-retry cap with backoff)
- Sub-agents that call each other directly (all communication goes through the orchestrator)
- Missing error contracts (every agent must define what failure looks like)

## Output checklist

- [ ] Agent topology diagram (text or Mermaid)
- [ ] Communication contracts for all agents
- [ ] Implementation files under `llm/agents/`
- [ ] Orchestrator wiring (calls, error handling, parallelism)
- [ ] Integration tests for the critical path and at least one failure case
