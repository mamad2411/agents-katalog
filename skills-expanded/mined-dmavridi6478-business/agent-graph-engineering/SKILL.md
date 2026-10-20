---
name: agent-graph-engineering
description: How to design multi-agent systems as directed graphs (Nodes/Edges/State) instead of single-agent loops — covering the 3 building blocks, 3 actionable design rules, and a zero-code manual starting method.
---

# Agent Graph Engineering

## The core problem with agent loops

A single agent in a loop:
- Accumulates messy, compounding context
- Repeats the same mistakes (no fresh perspective)
- Can't do real parallel work
- Burns tokens endlessly without converging

Graphs fix this by assigning each job to a fresh, specialized agent with a
clear hand-off contract.

## The 3 building blocks

**NODES** — specialized workers, each with one job:
- Research node: gathers information only
- Code node: writes/runs code only
- Review node: checks output only

**EDGES** — the rules for handing work between nodes:
- Conditions: "if quality check fails → back to code node"
- Routing: "if confident → proceed to plating; if uncertain → ask human"

**STATE** — the shared notebook every node reads from and writes to:
- Accumulates the work product as it moves through the graph
- Each node appends its output; nothing is lost between hand-offs
- The verifier reads the full state, not just the last node's output

## Why this beats a loop

| Loop | Graph |
|---|---|
| One agent, one context | Multiple agents, fresh context per node |
| Same mistakes repeat | Separate verifier catches errors |
| Sequential only | Parallel nodes possible |
| Unbounded token burn | Hard stops and budgets per node |

## 3 design rules (actionable)

### Rule 1: Draw before you build
Sketch nodes and arrows on paper or a whiteboard **before writing any code**.
If you can't draw the graph, you can't engineer it.

```
[Research] → [Code] → [Quality Check]
                ↑              |
                └──── fail ────┘
                        |
                      pass
                        ↓
                   [Plating] → [Done]
```

### Rule 2: Never let the same agent check its own work
Separate verifier = higher quality, fewer hallucinations.
This is the single highest-leverage rule. Apply it always.

### Rule 3: Add hard stops and budgets
Every graph needs:
- **Max steps/iterations** — stops infinite retry loops
- **Token/cost limit** — caps runaway spending
- **Clear success condition** — defines when "done" is actually done

Without all three, the graph runs forever and burns money.

## Zero-code starting method (manual graph)

1. Pick one task you keep looping on
2. Break it into 3–4 clear, distinct jobs
3. Run each job in a separate Claude chat with a clear role instruction
4. Use a final "reviewer" chat that reads all outputs and merges/checks

That is a graph — manual version. Build the manual version first; automate
only after the structure proves itself.

## Relationship to other skills

- **`night-shift-workflow`** — scheduling and approval gates for unattended
  workflows; graph design is the upstream step (design the graph, then decide
  which nodes can run unattended)
- **`web-task-scoping`** — task decomposition; the output of scoping is the
  node list for a graph
- **`multi-agent-orchestrator`** agent — runs a concrete retrieve→validate→write
  graph on a specific task; this skill is the design methodology behind that pattern
