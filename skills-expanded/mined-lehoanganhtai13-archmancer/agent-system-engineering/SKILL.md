---
name: agent-system-engineering
description: "Agent system engineering maps end-to-end responsibilities, architecture and cross-component hand-offs from an outcome to evidence. Use when planning or building an agent system, diagnosing long-running tasks or recovery, reviewing delegation and model/tool boundaries, or improving grounded answers, cost or change activation across components."
---

# Agent system engineering

This course map teaches responsibilities and hand-offs for systems in which an agent selects model and action steps toward an outcome. Start with the smallest system meeting the actual workload, authority, failure and evidence requirements. A responsibility is not a service: a single process can own several, and one shared store does not erase their contracts. Read [architecture](references/architecture.md) for boundaries, [system flows](references/system-flows.md) for hand-offs, and [engineering process](references/engineering-process.md) for the route from a requirement to evidence.

**Scope.** Use this skill to design, build, debug or review the agent system named by the current task. Component rules describe that target system; reading routes and engineering procedures guide your work on it. This separates product requirements from session instructions: actions remain governed by the current task and permissions, including when your own agent or harness is the target.

## One-screen map

| Responsibility | Question | Instructional home |
|---|---|---|
| task and interaction boundary | Who requests what, with which authority, and how can they cancel or receive the result? | [task and interaction boundary](../agent-runtime-and-interaction/references/task-and-interaction-boundary.md) |
| agent engine / harness | What step should execute next and when is work complete? | [agent engine / harness](../agent-harness-model-and-tools/references/agent-engine-and-harness.md) |
| model boundary | What request actually reaches the provider, and what response and usage came back? | [model boundary](../agent-harness-model-and-tools/references/model-boundary.md) |
| context and state management | What information enters this call, what persists, and what can be lost? | [context and state management](../agent-context-and-state/references/context-and-state-management.md) |
| action and tool boundary | Is a proposed action valid and authorized, and what actually happened? | [action and tool boundary](../agent-harness-model-and-tools/references/action-and-tool-boundary.md) |
| execution host and lifecycle | Who schedules, owns, stops and completes work, and recovers it if needed? | [execution host and lifecycle](../agent-runtime-and-interaction/references/execution-host-and-lifecycle.md) |
| evidence and knowledge access | What sources are visible, available, current and sufficient for the answer? | [evidence and knowledge access](../agent-evidence-and-knowledge/references/evidence-and-knowledge-access.md) |
| policy and configuration boundary | Which trusted settings and effective version govern this run? | [policy and configuration boundary](../agent-configuration-and-delivery/references/policy-and-configuration.md) |
| diagnostics, evaluation and resource control | What occurred, how well did it work, and what resources were consumed? | [diagnostics, evaluation and resource control](../agent-diagnostics-evaluation-and-resource-control/references/diagnostics-evaluation-and-resource-control.md) |
| delivery and operations | Which code and configuration reached the observed run? | [delivery and operations](../agent-configuration-and-delivery/references/delivery-and-activation-evidence.md) |

Trust and privacy cross every boundary: name an owner, threat model, allowed flows and enforcement points. The model proposes actions; trusted execution decides whether and how to act. A model instruction, screen or successful-looking response is not proof of authorization or effect.

When adding a capability or changing agent behavior through the harness, start with the [behavior-steering instinct map](../agent-harness-model-and-tools/SKILL.md#behavior-steering-instinct-map) to distinguish tool declarations, observations, committed-state echoes, result-specific guidance, transient reminders and changing context.

## Agent system engineering instinct map

Choose the simplest architecture that meets the agreed outcome and failure guarantees, naming what each added mechanism buys and what it makes slower or harder.

For capability design or problem-solving with a human counterpart, first use supported research or established practice to describe effective human performance, connect it to an option/check, and test transfer against agent differences; carry over only applicable human limits and label unsupported explanations as hypotheses; skip routine use and purely technical mechanisms without a counterpart ([design rule](references/engineering-process.md#design)).

| Need | Lever and trade-off | Build it as |
|---|---|---|
| Some steps are known, others depend on what we find. | **Coded workflow before adaptive loops and children** buys predictable execution; adaptation buys flexibility at calls, variable latency and verification cost. Delegate only for separable work or useful isolation. [Depth](references/architecture.md#architecture-trade-off-ladder) | Workflow function; bounded agent loop and child-run launcher only for adaptive steps. |
| Several responsibilities must work together. | **Co-located modules before separate services** keep contracts with fewer hops and simpler operations; distribute for actual independent ownership, scaling or isolation, accepting consistency and rollout costs. Capability plugins preserve isolation, removability and parallel development through an explicit contribution contract, declared ordering and a core-owned common module. [Depth](references/architecture.md#architecture-trade-off-ladder) | Capability plugins wired by an external composition root through core-owned interfaces; keep services co-located until required. |
| Work must finish after a caller or process disappears. | **Durable state and recovery** buy continuity at commit, fencing and reconciliation cost; a queue adds scheduling delay when used. Keep synchronous delivery if suitable, and add only the survival guarantees required. [Depth](references/architecture.md#architecture-trade-off-ladder) | Durable run record and checkpoint store; recovery worker with guarded ownership. |
| The next run must remember progress or learned information. | **Persistence and memory** save recovery or rediscovery but retain stale and sensitive state and require correction/forgetting; persist for the agreed horizon and verify indispensable constraints survive. [Depth](references/architecture.md#architecture-trade-off-ladder) | Versioned state store; scoped memory write/read functions for cross-session facts. |
| Several consumers need consistent routing, credentials or settings. | **Shared gateway or managed configuration** centralizes real control obligations at hop, availability and compatibility cost; start with local adapters/constants when sufficient and prove effective activation. [Depth](references/architecture.md#architecture-trade-off-ladder) | Local model adapter and validated configuration; shared gateway or configuration resolver when justified. |
| We need a reliable result without building a whole platform first. | **One complete verified slice** buys early feedback at limited coverage; broad generality adds lasting integration and maintenance cost. Include already-required failure guarantees, then expand only for demonstrated pressure. Capability plugins preserve isolation, removability and parallel development through an explicit contribution contract, declared ordering and a core-owned common module. [Depth](references/architecture.md#architecture-trade-off-ladder) | Assembled request-path function wiring model, tools, context and host; integration test checking its result and required failure paths; add capability plugins through the contribution contract without changing sibling tools. |

## Route by task

1. **New design:** state the desired outcome, actors, authority, workload, failure tolerance and evidence; read architecture and choose the applicable flows. Name the target model(s) early as a design input, because instructions, tool schemas, context and evaluation are tuned for them. Write ownership and interfaces before choosing deployment or technology. A fixed sequence can be a coded workflow; otherwise begin with a bounded agent and synchronous execution when those premises suffice. Add durable jobs, persistent state or a configuration service only for the continuity, liveness or independent-change pressure each addresses.
2. **Add a capability:** identify the new outcome, inputs, model-visible schema, action authority and effect; trace admission through completion and add both positive and counterfactual checks. Include context, lifecycle and privacy only where affected.
3. **Long-running work or continuity:** trace [flow 2](references/system-flows.md#2-long-running-task) and consult the host and context chapters. Distinguish a logical turn, a retry attempt and an external operation; decide what must survive a crash and what requires reconciliation.
4. **Debug:** first identify the actual run, revision, effective configuration and observed symptom. Trace its hand-offs, compare input and output at the first divergence, distinguish unavailable evidence from an absent result, and test a falsifiable cause at the responsible boundary.
5. **Optimize latency or cost:** establish the target and constraints, locate the measured bottleneck and freeze the comparison policy before any experiment. Compare provider-effective requests for caching; preserve correctness and trust constraints over cache reuse. If the requirement is a hard spend cap, distinguish an atomic monetary hold from an attribution reservation or a delayed spend check. Read [optimization](references/engineering-process.md#optimize).
6. **Review or harden:** follow each effect and data carrier across trust boundaries, then compare requirements to checks and evidence. Report missing proof and scope, not a pass inferred from a model declining to call a tool.
7. **Change provider, deployment or configuration:** verify exact adapter behavior and effective request, then trace activation to the observed run; a configuration fingerprint alone does not prove code identity. Introduce a gateway or independently managed configuration only when its shared policy, custody, routing, attribution or freshness pressure warrants it.
8. **Ground an answer:** identify authority, query, version, source lineage, omissions and errors; a failed search is not evidence that no answer exists. Start with available files, SQL or a search API; build an owned corpus only when its lifecycle is a product responsibility. Use [flow 5](references/system-flows.md#5-knowledge-grounded-answer).

## How to use the material

For the seven chapter skills, open [harness, model and tools](../agent-harness-model-and-tools/SKILL.md), [runtime and interaction](../agent-runtime-and-interaction/SKILL.md), [configuration and delivery](../agent-configuration-and-delivery/SKILL.md), [context and state](../agent-context-and-state/SKILL.md), [evidence and knowledge](../agent-evidence-and-knowledge/SKILL.md), [diagnostics, evaluation and resource control](../agent-diagnostics-evaluation-and-resource-control/SKILL.md), or [trust and privacy](../agent-trust-and-privacy/SKILL.md).

When an available specialist covers a narrower method — one framework's API, wording a standalone prompt, judge statistics, verifying current external facts — use it for that method; use these chapters for system contracts and the hand-offs they affect.

For each requirement write its owner, interface, failure behavior and a check with expected evidence and a counterfactual. Optional mechanisms begin with their premise; if the premise does not hold, omit them. A worked example illustrates one set of premises and is not a mandatory topology. Provider-specific facts are route- and version-dependent; qualify them on the actual model, client and deployment instead of promoting an example to a universal default.

Trust and privacy has its own [cross-cutting chapter](../agent-trust-and-privacy/references/trust-and-privacy.md), including threat models, enforcement and data lifecycle.
