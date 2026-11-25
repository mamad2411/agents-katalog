---
name: task-decomposition
audience: team
description: Goal decomposition heuristics, dependency DAG construction, sub-agent assignment protocols, and multi-agent orchestration patterns. Use when breaking complex goals into sub-tasks, constructing execution plans, or coordinating work across multiple specialized agents.
---

# Task Decomposition

> "Divide each difficulty into as many parts as is feasible and necessary to resolve it."
> -- Rene Descartes, *Discourse on the Method*

## Core Philosophy

Decomposition is the fundamental act of engineering: taking something too large to hold in mind and breaking it into pieces small enough to reason about, execute, and verify independently.

The quality of a decomposition is not measured by how many sub-tasks it produces, but by three properties: **completeness** (the sub-tasks collectively achieve the goal), **independence** (each sub-task can be executed by a single agent without requiring another), and **verifiability** (each sub-task has an observable "done" criterion). A decomposition lacking any of these properties will produce coordination failures, redundant work, or unverifiable outcomes.

**Why DAGs, not lists:** A flat task list implies sequential execution and hides dependency information. A DAG makes dependencies explicit, reveals parallelization opportunities, identifies the critical path, and makes the impact of a single failure visible. Every decomposition should be a graph, not a list.

**Non-Negotiable Constraints:**
1. **Complete** — the sub-tasks collectively achieve the goal
2. **One agent, one sub-task** — each sub-task is executable by a single agent without needing another mid-task
3. **Verifiable** — every sub-task has an observable "done" criterion
4. **A DAG with explicit dependencies** — if B needs A's output, that edge is in the graph, and B does not start before A is done
5. **Report gaps honestly** — never assign a sub-task to the wrong agent to hide a capability gap

## Workflow

Decomposition proceeds in four moves: choose a strategy, set granularity, build the dependency DAG, then assign each sub-task to an agent.

### Decomposition Strategies

#### Strategy 1: Functional Decomposition

Split by capability, feature, or functional area. Use when the goal describes a system with identifiable, separately-implementable features whose domains map cleanly to different agent types. Apply by listing functional requirements → grouping into areas → creating one sub-task per area → extracting shared prerequisites (database schemas, shared types, configuration) as their own prerequisite sub-tasks.

```
Goal: "Add user authentication and an admin dashboard to the application"

  T1: Define auth data model (schemas, entities)         -> tdd-agent
  T2: Implement authentication flow (login, logout, JWT) -> tdd-agent [depends: T1]
  T3: Write auth integration tests                       -> test-generation-agent [depends: T2]
  T4: Build admin dashboard UI                           -> tdd-agent [depends: T1]
  T5: Review auth implementation for security            -> code-review-agent [depends: T2]
  T6: Document auth API and admin features               -> documentation-agent [depends: T2, T4]
```

#### Strategy 2: Data-Flow Decomposition

Split by data transformation stages. Use when the goal describes a pipeline, ETL process, or data transformation where the work naturally flows from input to output through stages with clearly different technical concerns. Apply by tracing transformations from input to output → creating one sub-task per stage → identifying parallel branches.

```
Goal: "Build a pipeline that ingests sensor data, detects anomalies, and generates daily reports"

  T1: Implement data ingestion layer     -> tdd-agent
  T2: Build anomaly detection model      -> model-optimization-agent [depends: T1]
  T3: Implement the data validation layer -> tdd-agent [depends: T1]
  T4: Build report generation service    -> tdd-agent [depends: T2]
  T5: Generate test data and validate    -> test-generation-agent [depends: T1]
  T6: Document pipeline architecture     -> documentation-agent [depends: T2, T4]
```

#### Strategy 3: Temporal Decomposition

Split by lifecycle phase. Use when the goal spans the full development lifecycle (design through deployment) and earlier phases produce artifacts that later phases consume. Apply by identifying phases (research, design, implement, test, deploy, document) → creating sub-tasks per phase → applying functional or data-flow decomposition within each oversized phase → looking for cross-phase parallelization (documentation often starts during implementation).

```
Goal: "Migrate the payment service from .NET Framework 4.8 to .NET 10"

  T1: Research breaking changes and compatibility  -> research-agent
  T2: Assess current codebase migration readiness  -> migration-orchestrator [depends: T1]
  T3: Audit dependencies for .NET 10 compatibility -> dependency-audit-agent [parallel: T2]
  T4: Execute migration plan                       -> migration-orchestrator [depends: T2, T3]
  T5: Generate regression test suite               -> test-generation-agent [depends: T4]
  T6: Review migrated code for issues              -> code-review-agent [depends: T4]
  T7: Update documentation for .NET 10             -> documentation-agent [depends: T4]
```

#### Strategy 4: Risk-Ordered Decomposition

Split by risk level, isolating uncertain or high-risk work into early probe sub-tasks for fast validation. Use when the goal involves significant technical uncertainty or some parts may be infeasible. Design probe sub-tasks to fail fast, then gate the remaining plan on probe results.

```
Goal: "Add a new payment provider whose API reliability and rate limits are unproven"

  T1: Spike the provider SDK against the sandbox API    -> research-agent [PROBE]
  T2: Validate rate limits and failure modes under load -> research-agent [PROBE, parallel: T1]
  --- GATE: All probes must pass before proceeding ---
  T3: Implement the provider client with retries        -> tdd-agent [depends: T1, T2]
  T4: Audit the new SDK dependency for CVEs             -> dependency-audit-agent [parallel: T3]
  T5: Review the integration for correctness/security   -> code-review-agent [depends: T3]
  T6: Document the provider integration                 -> documentation-agent [depends: T3]
```

### Granularity Heuristics

| Split When | Stop When |
|-----------|-----------|
| Sub-task requires two different agents | Sub-task maps to a single agent and a single concern |
| Sub-task has multiple independent deliverables | Further splitting creates sub-tasks without meaningful "done" criteria |
| Description uses "and" connecting unrelated actions | Further splitting creates more coordination cost than execution cost |
| Cannot be completed in a single focused session | Three or more resulting sub-tasks would go to the same agent in sequence with no branching |
| Both autonomous and approval-required components exist | Sub-task is already a well-understood operation for the assigned agent |
| Failure of one part would not block the other | — |

### Dependency DAG Construction

Build the graph: for each sub-task T, list the inputs it requires → if an input is produced by another sub-task P, add edge P→T → if no sub-task produces a required input, flag as GAP. Verify every output is either consumed by a downstream sub-task or is a final deliverable.

**Cycle detection:** Run topological sort (Kahn's algorithm): compute in-degree for every node → queue all nodes with in-degree 0 → dequeue a node, add to sorted order, decrement successors' in-degrees → if sorted order is missing nodes, a cycle exists among the missing nodes.

**Critical path:** Assign effort weights (S=1, M=2, L=3) → find the longest path (sum of weights) → this is the minimum total duration → sub-tasks NOT on the critical path have slack. Focus monitoring on critical path sub-tasks.

### Sub-Agent Assignment Protocol

For each sub-task: identify the primary domain → select the agent whose domain best matches → if multiple agents fit, prefer tighter domain focus, then higher autonomy, then the agent already assigned other sub-tasks in the same track. If no agent matches, check if the sub-task can be decomposed further, merged with an adjacent sub-task that has a match, or the approach changed. If still unassignable, report the gap to the user — never assign to the wrong agent to avoid a gap.

**Load on demand — `references/operating-guide.md`:** Domain Principles, Anti-Patterns, AI Discipline Rules, Error Recovery.

## State Block

```
<decomposition-state>
mode: understand | decompose | assign | sequence | monitor
goal: [concise goal summary]
strategy: [functional | data-flow | temporal | risk-ordered | hybrid]
sub_tasks_total: [count]
sub_tasks_assigned: [count]
sub_tasks_unassignable: [count]
dag_valid: [true | false | not_constructed]
critical_path_length: [estimated effort units]
parallel_tracks: [count of independent parallel chains]
agents_involved: [list of agent names]
last_action: [what was just completed]
next_action: [what should happen next]
</decomposition-state>
```

State transitions: UNDERSTAND → DECOMPOSE (goal analyzed) → ASSIGN (DAG constructed) → SEQUENCE (all assigned or flagged) → MONITOR (plan approved) → COMPLETE. Any state can return to UNDERSTAND if the goal changes; MONITOR can return to DECOMPOSE if a failure requires re-planning.

## Output Template

**Goal Analysis:** Stated goal | Deliverables (numbered) | Constraints (tech stack, conventions, timeline, scope) | Assumptions (with how to verify) | Open questions (blocking vs. non-blocking)

**Decomposition Plan:** Strategy + rationale | Sub-tasks table (ID, Name, Agent, Inputs, Outputs, Done Criteria, Effort S/M/L)

```
Dependency DAG example:
T1 ──> T2 ──> T5
  └──> T3 ──> T5
T4 (independent) ──> T6
T5 ──> T6

Critical Path: T1 → T2 → T5 → T6 (8 effort units)
Waves: [1] T1, T4 | [2] T2, T3 | [3] T5 | [4] T6
```

**Progress Report:** Wave N | table of ID, Name, Agent, Status (COMPLETED/IN_PROGRESS/BLOCKED), Notes | Critical path status | Blockers | Next wave

Full templates: `references/orchestration-patterns.md`

## Integration with Other Skills

- [Decomposition Heuristics](references/decomposition-heuristics.md) — Detailed strategies for when to split, when to stop, and which strategy fits which goal type
- [Orchestration Patterns](references/orchestration-patterns.md) — Multi-agent execution patterns, DAG construction, cycle detection, and failure recovery protocols
