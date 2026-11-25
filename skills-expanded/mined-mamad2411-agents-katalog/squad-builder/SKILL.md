---
name: squad-builder
description: "Assemble and orchestrate agent squads with defined roles for complex multi-agent tasks. Use when designing a team of agents to tackle a large problem."
version: 1.0.0
platforms: [linux, macos]
---

# Squad Builder

## What It Does
Assembles purpose-built agent squads for complex tasks that require multiple specialized roles working in parallel or sequence. Defines squad composition (architect, implementer, reviewer, tester), manages inter-agent communication protocols, handles dependency chains, and dynamically reallocates work on failure.

## Iron Laws (NEVER violate)
1. **Role first, agent second** — Define what roles are needed before assigning which agents fill them.
2. **Explicit handoffs** — Every inter-agent handoff must have a defined contract (input schema, output schema, SLA).
3. **No silent failures** — If any squad member fails, the entire squad must be notified and reallocation triggered.
4. **Single squad commander** — Exactly one agent (or the human) has final decision authority. No design-by-committee.

## Red Flags (STOP immediately)
- **Circular dependency** — Agent A waits for Agent B, which waits for Agent A → deadlock
- **Role overlap conflict** — Two agents claim authority over the same decision → escalate to human
- **Squad thrashing** — Agents repeatedly reassign the same task without progress → squad composition wrong
- **Communication storm** — Agents generate more coordination messages than work output → over-fragmented

## Common Rationalizations (self-deception)
- "We can figure out roles as we go" → Undefined roles cause conflict and duplicated work.
- "Just throw more agents at it" → Adding agents beyond optimal squad size reduces throughput.
- "The agents will coordinate themselves" → Without explicit protocols, agents talk past each other.

## When To Use
- Task is too large for a single agent (estimated 5+ tool calls across domains)
- Task requires diverse expertise (frontend + backend + security + DevOps)
- User wants parallel execution with dependency management
- Complex review workflows requiring independent verification

## Human Partner Signals (escalate to human)
- **Deadlock detected** — Circular dependency that cannot be auto-resolved
- **Squad consensus failure** — Agents disagree on approach after 2 debate rounds
- **Resource exceeded** — Task requires more agents than max squad size allows
- **Quality dispute** — Reviewer and implementer cannot agree on acceptance criteria

## Pipeline
1. Analyze task: decompose into sub-tasks, identify required roles
2. Design squad: assign roles, define handoff contracts, set communication rules
3. Assemble: spawn agents with role-specific system prompts and tool access
4. Execute: monitor progress, resolve blockers, reallocate on failure
5. Debrief: collect squad outputs, merge results, archive squad for future reuse

## Verification Checklist
- [ ] Every squad role has a defined input/output contract
- [ ] Dependency graph has no cycles (DAG verification)
- [ ] Squad size is optimal for task complexity (not under/over-staffed)
- [ ] Failure of one agent triggers automatic reallocation
- [ ] Squad output is coherent (no contradictory conclusions between agents)
- [ ] Human can override any squad decision at any point

## Related Skills
- `agent-teammate` — Squad members are individual agent teammates
- `task-lifecycle-manager` — Squads execute tasks tracked in lifecycle manager
- `subagent-orchestrator` — Lower-level orchestration primitive for single subagent spawns
- `cross-model-reviewer` — Squad pattern applied to multi-model code review
