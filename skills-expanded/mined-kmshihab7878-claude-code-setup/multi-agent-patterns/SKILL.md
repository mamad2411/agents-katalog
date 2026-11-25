---
name: multi-agent-patterns
description: >
  Design patterns for multi-agent AI systems. Supervisor, pipeline, swarm, and hierarchical
  patterns. Communication protocols, task delegation, lifecycle management, and conflict resolution.
  Use when designing new agent architectures, coordinating multiple agents, or orchestrating workflows.
risk: medium
tags: [agents, architecture]
created: 2026-03-07
updated: 2026-05-15
---

# Multi-Agent Patterns

Use this skill to select and apply multi-agent collaboration patterns: supervisor, pipeline, router, critic-executor, debate, hierarchical delegation, peer mesh, swarm, and related coordination workflows.

Keep this file as the operating contract. Load references only for detailed catalogs, implementation sketches, handoff templates, failure modes, and worked examples.

## When To Use

- Designing a new agent architecture.
- Adding agents to an existing system.
- Coordinating multiple agents across parallel, sequential, review, or escalation work.
- Choosing communication, delegation, conflict-resolution, memory, lifecycle, or health-monitoring rules.
- Auditing a multi-agent workflow for deadlocks, authority gaps, hidden state, or poor observability.

## When Not To Use

- Single-agent work with no coordination problem.
- Claude Code subagent authoring; use the relevant subagent-development guidance.
- MCP server development; use `mcp-builder`.

## Required Inputs

Ask for or infer:

- Goal, task type, stakes, and expected deliverable.
- Agent roles, capabilities, authority boundaries, and escalation path.
- Work shape: independent, sequential, iterative review, classification, debate, hierarchy, search, or real-time interaction.
- Constraints: latency, cost, tool access, approvals, safety tier, auditability, and state-sharing limits.
- Validation plan: success criteria, review loops, timeouts, failure handling, and evidence required.
- Existing environment constraints such as PolicyGate, coordinator, memory, MCP, or repository rules.

Do not invent agent capabilities, authority, tool access, safety approvals, or validation results.

## Pattern Selection Workflow

1. Classify the work shape and risk tier.
2. Pick the smallest coordination pattern that satisfies the goal.
3. Define agent roles, authority, inputs, outputs, and stop conditions.
4. Choose communication: message passing, shared state, or event bus.
5. Choose delegation: capability-based by default; use round-robin, auction, priority, or affinity only when justified.
6. Choose conflict resolution: voting, priority, consensus, arbitration, or evidence-weighted.
7. Add lifecycle rules: timeouts, heartbeat, retry, fallback, dead-letter handling, and recovery.
8. Add traceability: `trace_id`, structured logs, handoff summaries, and final evidence.
9. Validate for anti-patterns before recommending or implementing the design.

## Decision-Critical Pattern Routing

| Scenario | Default Pattern |
|---|---|
| Independent subtasks | Orchestrator-Workers or Supervisor |
| Sequential processing | Pipeline / Plan-and-Execute |
| Quality-critical output | Critic-Executor |
| Request classification | Router |
| Complex multi-step goals | Plan-and-Execute |
| Controversial decisions | Debate with judge or arbitration |
| Exploration or search | Swarm |
| Real-time interaction | Real-time agent pattern |
| Organization hierarchy | Hierarchical Delegation |
| Collaborative reasoning | Peer-to-Peer |

Use composition when needed, but avoid stacking patterns without a concrete coordination need.

## Coordination And Authority Constraints

- Every handoff must include `trace_id`, context summary, explicit authority (`consulted`, `delegated`, or `escalated`), timeout, and rejection path.
- Capability-based delegation is the default. If no capable agent is available, escalate instead of silently routing to a weak fit.
- Shared state requires locks or another explicit concurrency control. Prefer message passing when loose coupling is enough.
- Private agent memory stays private; shared memory writes must record source agent and reason.
- Conversation policies must define max turns, allowed topics, blocked patterns, escalation triggers, and tone.
- Authority-gated actions must preserve PolicyGate or equivalent approval rules. Agents must not expand their own authority.
- Fallbacks must surface reduced quality or changed capability; never hide degradation.

## Safety Rules

- Do not bypass approval gates, MCP governance, validation, public-safety checks, or destructive-action protections.
- Do not let agents execute production, credential, financial, security-sensitive, or irreversible actions without the required approval.
- Do not use multi-agent structure to launder unsafe instructions through another agent.
- Do not store secrets, private context, session records, credentials, local paths, or personal identifiers in shared memory or tracked files.
- Do not claim an agent result is verified without evidence from the agent output, checks, tests, or review loop.

## Validation Gates

- Pattern fit: chosen pattern matches the work shape and risk.
- Authority check: each agent has explicit scope, permissions, escalation path, and stop condition.
- Handoff check: summaries, `trace_id`, timeout, and rejection path exist.
- Failure check: retry, fallback, partial-result, and dead-letter behavior are explicit.
- Observability check: trace logs or comparable evidence can reconstruct the chain.
- Anti-pattern check: no god agent, chatty loop, circular dependency, no-timeout path, unsafe shared state, or invisible failure.
- Review check: quality-critical work has critic, reviewer, arbiter, or independent validation.

## Output Expectations

Return:

- Recommended pattern or pattern composition.
- Roles, responsibilities, authority boundaries, and handoff rules.
- Communication, delegation, conflict-resolution, memory, lifecycle, and error-handling choices.
- Validation plan and evidence requirements.
- Anti-pattern risks and mitigations.
- PolicyGate or equivalent approval tier when authority-gated actions are involved.
- Open risks and follow-up checks.

## Minimal Examples

```text
Independent research subtasks -> Supervisor with capability-based workers, shared trace_id, aggregator, critic review.
```

```text
High-stakes decision -> Debate with evidence-weighted arbitration, explicit escalation path, and final reviewer.
```

```text
Sequential build workflow -> Plan-and-Execute DAG with cycle rejection, per-step validation, and dead-letter handling.
```

## Reference Map

- Pattern catalog and implementation sketches: [orchestration-patterns.md](references/orchestration-patterns.md)
- Delegation, guardrails, conflict resolution, and handoffs: [delegation-and-handoffs.md](references/delegation-and-handoffs.md)
- Communication, lifecycle, memory, and real-time coordination: [coordination-examples.md](references/coordination-examples.md)
- Validation, failure modes, anti-patterns, and troubleshooting: [validation-and-troubleshooting.md](references/validation-and-troubleshooting.md)
- Worked scenarios and pattern composition: [examples.md](references/examples.md)

## Cross-References

- **subagent-development** skill: Claude Code subagent lifecycle.
- **docs/AI_AGENT_LANDSCAPE.md**: framework comparison.
- **docs/SECURITY_PLAYBOOK.md**: agent security controls.
