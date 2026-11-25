---
name: multi-agent-coding-coordination-network
description: Applies the first temporal-network instrument for measuring coordination in multi-agent AI coding teams, revealing that quadratic messaging cost is mostly a one-time handshake, files are the cheaper coordination channel where messaging dominates, and naming a coordinator creates no structural leadership. Use when designing multi-agent coding systems, configuring team size, or choosing coordination channels.
---

# Multi-Agent Coding Coordination Network

## Overview
The first instrument that makes multi-agent coding coordination measurable as a temporal network, revealing that the assumed quadratic communication cost is actually a one-time handshake, files are the cheaper one-to-many channel, and prompt-assigned leadership does not create structural leadership.

## When to Use
- Designing multi-agent coding systems with 2+ agents
- Configuring team size for multi-agent coding tasks
- Choosing between direct messaging vs shared files for coordination
- Evaluating whether a coordinator agent improves outcomes
- NOT for single-agent coding workflows
- NOT for human team coordination (different dynamics)

## Core Process / Workflow

### 1. Model Coordination as a Temporal Network
Represent each multi-agent run as a heterogeneous graph:
- Nodes: agents AND files (both are first-class)
- Edges: agent→agent (messages), agent→file (writes), file→agent (reads)
- Each edge carries: timestamp, byte size, token cost

### 2. Apply the Team Size Decision Framework

| Team Size | Messaging Pattern | Coordination Shape | File Channel Effect |
|-----------|------------------|-------------------|-------------------|
| 2-4 agents | Quadratic growth (real) | Task-dependent shape | Moderate savings |
| 4-8 agents | Growth slows (handshake completes early) | Sparse if chained, dense if distributed | 42% token savings on message-heavy work |
| 8-16 agents | Growth HALTS (switches to broadcast) | Near-zero named-peer network | Files already carry coordination; mandatory files add overhead |

### 3. Choose Coordination Channel by Task Type

**Distributed tasks** (shared spec, all-to-all knowledge needed):
- Default coordination: one-to-one messages
- Mandate shared files → 42% output token reduction at 8 agents
- Files replace repeated messaging

**Chained/pipeline tasks** (each agent owns consecutive steps):
- Default coordination: files (each step's output read by next)
- Do NOT mandate additional files → adds 17-10% overhead
- Files already carry the coordination

### 4. Do NOT Rely on Coordinator Assignment
- Naming one agent "coordinator" in its prompt creates NO communication hub
- No traffic concentrates on the coordinator
- No reliable success improvement (pre-registered null confirmed)
- Teams self-organize based on task structure, not prompt labels

### 5. Identify Interface Ownership Gaps
The most dangerous failure mode: an interface between two agents that no single agent owns.
- Symptom: repeated discussion of the same issue across runs with no resolution
- Diagnosis: check if the failing interface falls on a boundary between two different owners
- Fix: assign explicit ownership of the interface to one agent

## Key Evidence
- Study: Destefanis & Aste (UCL, arXiv:2608.16801v1)
- 1,902 graded runs + 244 sealed replication runs
- Two task types: distributed (shared spec) and chained (pipeline)
- Model pinned to claude-sonnet-4-6
- Pre-registered hypotheses with Benjamini-Hochberg correction
- Replication package: github.com/giuseppedestefanis/when-agents-coordinate

## Cross-Domain Synthesis
- The "handshake-then-core" pattern parallels the Claude Code expertise finding: most coordination effort is upfront, then sustained channels are narrow
- File-as-channel insight connects to MCP code execution pattern: files as progressive disclosure mechanism
- Coordinator null result parallels the SE Agent Building finding: organizational structure matters more than individual tool assignment

## A-Tech Alignment
- Open-source: instrument works with any runtime that logs tool calls
- Data privacy: coordination measurement from logs, no content exposure
- Financial freedom: 42% token reduction on message-heavy multi-agent work
- Practical implementation: temporal network parser released, applicable to any MCP-based system

## References
- See [references/evidence-base.md](references/evidence-base.md) for full network analysis, scaling arm results, sealed replication, and the unprompted answer-key seeking behavior.