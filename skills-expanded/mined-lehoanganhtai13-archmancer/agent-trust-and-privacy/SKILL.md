---
name: agent-trust-and-privacy
description: "Trust and privacy define authority, protected data and enforcement across agent boundaries. Use when planning or reviewing principal and resource isolation, authorization, delegated authority, tool credentials or human approval; defending against prompt injection through retrieval, memory or other untrusted content; handling sensitive data, leakage, retention or deletion; or investigating uncertain protection evidence. Use when a model proposes an action or content crosses a trust boundary and the authorizing principal and effect need verification."
---

# Trust and privacy across an agent system

Start with [trust and privacy](references/trust-and-privacy.md) to map principals, protected resources, allowed effects, carriers, threat-model ownership and enforcement. Trust is a cross-cutting responsibility, not a required separate service. Select mechanisms by the actual threat, data and effect: a trusted local process can be small; shared resources, remote work or delegation add boundaries. The agent can propose an action, while the action owner verifies and enforces the authority to perform it.

**Scope.** Use this skill to design, build, debug or review the agent system named by the current task. Component rules describe that target system; reading routes and engineering procedures guide your work on it. This separates product requirements from session instructions: actions remain governed by the current task and permissions, including when your own agent or harness is the target.

Use the [architecture](../agent-system-engineering/references/architecture.md), [system flows](../agent-system-engineering/references/system-flows.md) and [engineering process](../agent-system-engineering/references/engineering-process.md) to trace the complete system. This skill supplies trust decisions; each component owns its operational interface and failure handling. A single process can implement several responsibilities without merging their contracts.

## Trust and privacy instinct map

Protect fixed authority and privacy guarantees first; choose optional controls by their threat coverage, friction, latency and lifecycle cost.

For capability design or problem-solving with a human counterpart, first use supported research or established practice to describe effective human performance, connect it to an option/check, and test transfer against agent differences; carry over only applicable human limits and label unsupported explanations as hypotheses; skip routine use and purely technical mechanisms without a counterpart ([design rule](../agent-system-engineering/references/engineering-process.md#design)).

| Need | Lever and trade-off | Build it as |
|---|---|---|
| Let the right person act without unnecessary interruptions. | **Scoped authority and bound approval** keep effects within a verified grant, but distributed grants add lifecycle work and confirmation adds user interruption; use the smallest valid carrier and require independent approval where policy demands it. [Depth](references/authority-and-approval.md#choosing-a-carrier) | Policy check inside the tool executor; exact approval record consumed with the protected write. |
| Documents may try to steer the assistant. | **Effect enforcement before screening** preserves fixed action limits; a detector adds fallible warning coverage at latency, spend and benign-block costs. Calibrate it for a named decision and keep authorization independent. [Depth](references/untrusted-content-and-injection.md#detection-as-a-measured-signal) | Deterministic executor gate; optional before-model screening hook returning a typed advisory result. |
| The assistant must use data without exposing raw values. | **Omission, projection, redaction, then protected references when needed** trade utility against exposure and mapping complexity; references add custody, availability, linkability and deletion obligations and do not guarantee all-input confidentiality. [Depth](references/sensitive-data-lifecycle.md#2-choose-controls-for-the-actual-pressure) | Producer projection/redaction function; protected mapping store and authorized tool-boundary resolver when needed. |
| Checks slow the request, but permission can change. | **Fresh checks versus cached proofs** trade dependency latency and availability against staleness and invalidation races; define the allowed freshness, bind reuse to subject/generation and refuse an unverifiable required proof. [Depth](references/protected-references-and-admission.md#1-admission-references-and-use) | Admission verifier and subject/generation-keyed proof cache with revalidation before use. |
| Keep enough to recover, and honour requests to forget. | **Purpose-limited retention and staged erasure** preserve useful continuity at exposure and coordination cost; minimize first, distinguish withdrawal from complete purge, and never acknowledge beyond verified copies and writer fences. [Depth](references/sensitive-data-lifecycle.md#2-choose-controls-for-the-actual-pressure) | Retention policy at each store; erasure coordinator with durable progress and commit-time writer fences. |

## Route to the right contract

| Question or symptom | Open | What it answers |
|---|---|---|
| Who is trusted, what is protected and where does enforcement happen? | [Trust and privacy](references/trust-and-privacy.md) | Threat model, component boundaries, conditional decisions and checks. |
| Can this actor perform this operation on this resource, including through a child or tool? | [Authority and approval](references/authority-and-approval.md) | Principal, operation, resource and version binding, credential propagation, delegation and exact independent approval. |
| Can a document, tool result, memory or child output steer the agent into an unauthorized action? | [Untrusted content and injection](references/untrusted-content-and-injection.md) | Provenance, source boundaries, deterministic effect controls and measured detection. |
| Where can sensitive data appear, persist or be deleted? | [Sensitive-data lifecycle](references/sensitive-data-lifecycle.md) | Carrier inventory, protection, retention and deletion across copies and in-flight writers. |
| How are protected references admitted and safely resolved? | [Protected references and admission](references/protected-references-and-admission.md) | Protected-reference handling and admission at the privacy boundary. |
| How does a forget or erasure request reach durable state and in-flight writers? | [Erasure and forget](references/erasure-and-forget.md) | Deletion and forgetting across persisted data and concurrent work. |

Read the [task and interaction boundary](../agent-runtime-and-interaction/references/task-and-interaction-boundary.md) for admission and user interaction, the [action and tool boundary](../agent-harness-model-and-tools/references/action-and-tool-boundary.md) for execution and truthful outcomes, and [evidence and knowledge access](../agent-evidence-and-knowledge/references/evidence-and-knowledge-access.md) for visibility and grounded results. Read [context and state management](../agent-context-and-state/references/context-and-state-management.md) when provenance, summaries, persistence or forgetting matter. For the operational contracts around a long-running task, read [execution host and lifecycle](../agent-runtime-and-interaction/references/execution-host-and-lifecycle.md).

## Working route

1. **Frame the boundary.** List actors, assets, actions, sources, destinations and their owners. Mark which callers, model outputs and external data can be controlled by an adversary. Record the expected outcome and unacceptable effects before selecting mechanisms.
2. **Trace one allowed and one denied request.** Follow verified identity and scope from admission to each protected read or effect. The receiving owner checks the actual principal, resource, operation and applicable version. Identify how the caller learns the difference between denial, unavailable verification and an uncertain effect.
3. **Select optional controls by premise.** Add durable authority for work crossing a process or time boundary; attenuate authority when delegating; require independently bound approval only when policy requires it; use screening when a measured signal serves a defined decision. Identify the policy and effect owner for each choice.
4. **Trace data.** Where sensitive data is involved, identify prompts, results, streams, logs, durable state and derivatives. Give each carrier an access and lifecycle policy; when forgetting is required, include stale in-flight writers and derived copies.
5. **Verify the actual boundary.** Test authorized and unauthorized cases in both directions, including the direct action path. A model choosing not to call is useful behavioral evidence but does not exercise an enforcement gate. Include unavailable dependencies, replay, version changes and genuine indirect ingress where applicable. Report evidence and uncertainty at the scope observed.
6. **Maintain the design.** Revisit trust mapping when a principal, source, tool, provider adapter, grant, policy or delivery path changes. If optimizing, establish the bottleneck and retain existing hard authority and privacy guarantees while comparing alternatives.

## Reading examples

For a local assistant that reads only trusted files and cannot mutate protected state, identify the local user's authority and data exposure, then omit remote delegation and approval mechanisms without copying a hosted architecture. For a multi-user assistant that reads uploaded documents and can update shared records, read the home chapter, both authority and injection leaves, and the sensitive-data leaf when those records contain protected data. For an asynchronous worker, also trace [long-running task flow](../agent-system-engineering/references/system-flows.md#2-long-running-task) and verify that a worker cannot substitute another task's authority. For an independently approved write, follow [human approval flow](../agent-system-engineering/references/system-flows.md#4-human-approval-of-an-effect) and test a changed proposal and replay.

## Evidence standard

Separate the existence of a policy from its enforcement, a proposed improvement from a built control, and a successful-looking response from an observed effect. A detector's unassessed result is not a zero-risk score. A failed retrieval is not proof of absence. A lost effect acknowledgement requires reconciliation; replay is safe only when idempotency is verified for the same operation and body, otherwise stop for manual reconciliation. Report an untested boundary as unverified and name its owner rather than assuming a sibling component supplies it.
