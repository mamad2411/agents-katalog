---
name: agent-orchestration-patterns
version: 1.0.0
min_mindforge_version: 10.0.7
status: stable
triggers: agent orchestration pattern, supervisor worker pattern, agent pipeline topology, agent debate pattern, agent consensus protocol, map reduce agents, handoff protocol design, multi-agent coordination, agent topology design, swarm pattern design, agent composition, failure propagation pattern
compose:
  - tool-design
---

# Agent Orchestration Patterns

## When this skill activates

This skill activates when designing multi-agent systems, choosing coordination topologies, implementing handoff protocols, or debugging agent-to-agent communication failures. It applies to any system where two or more autonomous agents must collaborate, compete, or chain their outputs to accomplish a goal.

## Mandatory actions when this skill is active

### Before

1. **Map the problem space** — Identify all subtasks. Determine which require sequential execution (dependencies) and which are independent (parallelizable).
2. **Assess complexity** — Single-agent tasks masquerading as multi-agent problems waste coordination overhead. Only orchestrate when genuine specialization or parallelism is needed.
3. **Define boundaries** — Each agent must have a clear responsibility boundary. Overlapping responsibilities cause conflicts. Gaps cause dropped tasks.
4. **Choose state strategy** — Decide upfront: shared state (agents read/write common store) or isolated state (agents communicate only via messages).

### During

#### Pattern Catalog

**1. Supervisor/Worker (Hub and Spoke)**
- **Topology** — One coordinator agent decomposes the task and dispatches subtasks to N worker agents. Workers report results back to the supervisor.
- **When to use** — Task is decomposable into independent units. Workers are interchangeable or specialized but non-overlapping.
- **Supervisor responsibilities** — Task decomposition, worker assignment, result aggregation, error handling, timeout enforcement.
- **Worker responsibilities** — Execute assigned subtask, report structured results, signal failure early.
- **Pitfall** — Supervisor becomes bottleneck. Mitigate with async dispatch and parallel worker execution.

**2. Pipeline (Sequential Chain)**
- **Topology** — Agent A's output becomes Agent B's input. Linear flow through N stages.
- **When to use** — Tasks have natural ordering (research → draft → review → publish). Each stage transforms or enriches the previous output.
- **Stage contract** — Each stage must define its input schema and output schema. Type mismatch between stages is the most common pipeline failure.
- **Error handling** — Fail the pipeline on any stage failure. Partial results from earlier stages should be preserved for debugging.
- **Optimization** — Streaming between stages reduces latency. Agent B can begin processing as Agent A emits output.

**3. Debate (Adversarial)**
- **Topology** — Two or more agents argue opposing positions. A synthesizer agent evaluates arguments and produces a final decision.
- **When to use** — High-stakes decisions where bias is a risk. Architecture choices, security reviews, strategic decisions.
- **Protocol** — Round 1: each debater states position with evidence. Round 2: each debater rebuts opponent's position. Round 3: synthesizer produces verdict with reasoning.
- **Constraint** — Debaters must not see each other's initial positions until after Round 1. Prevents anchoring.
- **Pitfall** — Debates can be unproductive without strict structure. Always time-box rounds.

**4. Consensus (Agreement Required)**
- **Topology** — All agents must agree on the output. Disagreement triggers re-evaluation.
- **When to use** — Safety-critical decisions. Deployment approvals. Security assessments. Changes where false positives are acceptable but false negatives are dangerous.
- **Protocol** — Each agent independently evaluates. If all approve: proceed. If any reject: block and surface the dissenting reasoning.
- **Threshold variants** — Unanimous (all agree), Majority (>50%), Supermajority (>66%), Quorum (minimum N must vote).
- **Pitfall** — Consensus is expensive. Reserve for decisions where the cost of a wrong answer far exceeds the cost of deliberation.

**5. MapReduce (Parallel Processing)**
- **Topology** — Map phase: split input into N chunks, dispatch to N parallel agents. Reduce phase: aggregate results into final output.
- **When to use** — Large inputs that can be processed independently (code review across files, document analysis, test execution).
- **Map function** — Must produce non-overlapping chunks. Overlap causes duplicate work or conflicting results.
- **Reduce function** — Must handle partial failures gracefully. If 1 of 10 map workers fails, the reduce should still produce useful output from the other 9.
- **Scaling** — Add more workers linearly. Bottleneck is the reduce step, not the map step.

#### Handoff Protocol Design

Every agent-to-agent handoff must include a structured message:

```json
{
  "task_id": "unique-identifier",
  "from_agent": "agent-name",
  "to_agent": "agent-name",
  "task": "clear description of what to do",
  "context": "relevant background (minimal, not full history)",
  "constraints": ["must not modify X", "timeout 30s"],
  "acceptance_criteria": ["output matches schema Y", "all tests pass"],
  "artifacts": ["file paths or data references"]
}
```

- **Minimal context** — Send only what the receiving agent needs. Full history causes confusion and wastes tokens.
- **Explicit acceptance criteria** — The receiving agent must know when it has succeeded.
- **Typed artifacts** — Reference files or data by path/ID, not by embedding content in the message.

#### Failure Propagation Strategies

| Strategy | Behavior | Use When |
|----------|----------|----------|
| Fail-fast | Abort immediately, surface error | Critical path, no recovery possible |
| Retry | Repeat N times with backoff | Transient failures (network, rate limits) |
| Escalate | Notify supervisor, request human input | Ambiguous failures, policy decisions |
| Degrade | Continue with partial results, flag gaps | Non-critical subtasks, best-effort acceptable |
| Circuit-break | Stop retrying after N failures, return cached/default | Dependency is unreliable |

#### State Management

- **Shared state** — All agents read/write a common store (database, shared memory). Simpler but requires conflict resolution (optimistic locking, CRDTs).
- **Isolated state** — Agents maintain private state, communicate only via messages. Safer but requires explicit state transfer in handoffs.
- **Hybrid** — Shared read-only state (project context, configuration) + isolated write state (each agent's working memory). Best balance for most systems.

#### Decision Matrix: When to Use Which Pattern

| Scenario | Pattern |
|----------|---------|
| Task decomposes into independent subtasks | MapReduce or Supervisor/Worker |
| Tasks must execute in order | Pipeline |
| High-stakes decision needs scrutiny | Debate or Consensus |
| One coordinator manages many executors | Supervisor/Worker |
| System must tolerate partial failures | MapReduce with degraded reduce |
| Speed is critical, tasks are independent | MapReduce with max parallelism |

### After

1. **Validate handoff contracts** — Test that each agent produces output matching the next agent's expected input schema.
2. **Test failure modes** — Simulate each failure propagation path. Verify the system degrades gracefully, not catastrophically.
3. **Measure overhead** — Coordination cost should be <20% of total execution time. If higher, simplify the topology.
4. **Document topology** — Create a diagram showing agent relationships, handoff directions, and failure paths.

## Self-check before task completion

- [ ] Pattern choice is justified by task structure (not over-engineered)
- [ ] Each agent has clear, non-overlapping responsibilities
- [ ] Handoff protocol includes task, context, constraints, and acceptance criteria
- [ ] Failure propagation strategy is defined for every inter-agent connection
- [ ] State management approach is explicit (shared vs isolated vs hybrid)
- [ ] Coordination overhead is measured and acceptable (<20% of total time)
- [ ] All agent-to-agent contracts are typed and validated
- [ ] System degrades gracefully under partial failure conditions
