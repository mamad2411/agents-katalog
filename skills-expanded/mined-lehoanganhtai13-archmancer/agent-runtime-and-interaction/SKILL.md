---
name: agent-runtime-and-interaction
description: "Task and interaction boundary and execution host and lifecycle admit work, manage run ownership and deliver results. Use when planning task admission, scheduling or cancellation; building durable recovery, streaming or reconnect; diagnosing duplicated requests, stalled runs, ambiguous effects or lost output; or reviewing lifecycle and capacity behavior."
---

# Runtime and interaction

Use this area to select and validate the execution host and lifecycle responsibility: scheduling, starting, stopping, bounding and completing work. This is a logical responsibility, not a required process or service. One application can combine it with other boundaries while keeping each hand-off explicit. Start with an in-process call when the request lifetime and process lifetime are acceptable boundaries; add durable machinery only when the required survival or scheduling contract demands it.

**Scope.** Use this skill to design, build, debug or review the agent system named by the current task. Component rules describe that target system; reading routes and engineering procedures guide your work on it. This separates product requirements from session instructions: actions remain governed by the current task and permissions, including when your own agent or harness is the target.

## Route the task

1. Read [task and interaction boundary](references/task-and-interaction-boundary.md) for admission, caller authority, submission identity and result retrieval. Establish the desired outcome, caller and trigger, authority, time and resource limits, and what the caller must observe when work finishes or fails. User calls, queued events and scheduled triggers can all enter through the task and interaction boundary. An admitted task is not necessarily a started run, and an accepted run is not necessarily complete.
2. Read [execution host and lifecycle](references/execution-host-and-lifecycle.md) for the minimum request path, run identity, states, completion, cancellation, capacity decisions, failure paths, and evidence. Compare the decision table against actual pressures before choosing a queue or separate worker.
3. If work must survive request or process failure, read [durable execution and recovery](references/durable-execution-and-recovery.md). Establish ownership, stable operation and logical-turn identities, effect intent and reconciliation before enabling replay. A queue or a heartbeat alone does not make an external effect exactly once.
4. If a client receives streamed output or can reconnect, read [output streaming and reconnect](references/output-streaming-and-reconnect.md). Specify partial and terminal events, retained cursors, explicit gaps, authoritative history, and what to show when a terminal or a run decision is missing.
5. Follow [system flow 2](../agent-system-engineering/references/system-flows.md) for the complete long-running task across boundaries. Ask [context and state management](../agent-context-and-state/references/context-and-state-management.md) what checkpoint content, provenance, admission and loss policies mean; the host schedules checkpoint operations and respects their receipts, but does not define the contents.

## Responsibility at each hand-off

The task and interaction boundary authenticates and authorizes admission and presents the desired outcome. The host records or carries an admitted run, enforces start and completion ownership, and supplies deadlines and cancellation to the engine. The agent engine / harness selects the next model step, observation, action, delegation or completion. The model boundary handles model request and response fidelity; the action and tool boundary authorizes and executes proposed effects. Context and state management owns what information enters a call and its persistence and continuity semantics. The host preserves and checks the admitted settings version where consistency requires it. Diagnostics, evaluation and resource control join evidence and cost to the correct run and attempt.

Neither a shared database nor a single process erases those contracts. Trust and privacy apply across them: preserve caller authority, minimize retained data, fence stale writes and coordinate deletion with any active writer. A client-generated message id is not proof of server deduplication. A result frame is a view; when persistence is required, its claimed completion must follow a verified durable decision and any required receipt.

## Select by pressure

Escalate execution machinery by the survival, interaction and effect guarantees the caller needs, including the wait and operational cost it introduces.

For capability design or problem-solving with a human counterpart, first use supported research or established practice to describe effective human performance, connect it to an option/check, and test transfer against agent differences; carry over only applicable human limits and label unsupported explanations as hypotheses; skip routine use and purely technical mechanisms without a counterpart ([design rule](../agent-system-engineering/references/engineering-process.md#design)).

| Need | Lever and trade-off | Build it as |
|---|---|---|
| One short task may end with its caller | **In-process execution** avoids durable coordination but loses work with the request or process; start here with deadlines and truthful outcomes when that loss is acceptable. [Lifetime choices](references/execution-host-and-lifecycle.md#3-decision-table-minimal-and-extended) | Async invocation function with deadline, cancellation signal and return value. |
| Work must continue after the caller leaves | **A background handle** decouples the connection but still loses work on process death; add durable records and recovery only for required host-loss survival, paying commit and ownership costs. [Recovery](references/durable-execution-and-recovery.md#2-minimum-recovery-contract) | Host-owned background task and lookup handle; durable run store and recovery loop only for survival. |
| Work must wait for resources or run independently | **Queueing and separate workers** buy scheduling and isolation but add caller-paid queue delay, delivery duplicates and cross-process compatibility; start with bounded local concurrency and add each for its own pressure. [Scheduling costs](references/execution-host-and-lifecycle.md#3-decision-table-minimal-and-extended) | Concurrency semaphore first; queue producer and separately owned worker when required. |
| People need progress now and continuity after reconnect | **Streaming** buys earlier visibility, not proof of completion; cursors and retention add storage, privacy, gaps and reconciliation. Begin final-only if sufficient, then add only the promised interaction guarantees. [Delivery choices](references/output-streaming-and-reconnect.md#1-premise-and-event-contract) | Event publisher and stream decoder; retained event log with cursor/replay handler for reconnect. |
| A stop request must interrupt silent work | **Cooperative cancellation** is simpler but may wait on a blocked call; a watcher and upstream close add races and coordination. Extend for the required stop bound and measure actual stop separately from terminal output. [Cancellation choices](references/execution-host-and-lifecycle.md#3-decision-table-minimal-and-extended) | Host cancellation token checked around awaited work; watcher closing the upstream call if required. |
| A timed-out action might already have happened | **Intent, stable keys and owner reconciliation** add persistence and sometimes manual delay but avoid blind duplicate effects; recover matching receipts first and replay only under verified idempotency. [Effect recovery](references/durable-execution-and-recovery.md#2-minimum-recovery-contract) | Effect-intent journal keyed by logical operation; reconciliation function at the effect owner. |

A scheduler can use a queue such as a broker, a database-backed queue, or another owned delivery mechanism. These are alternatives, not mandatory services. A queued identifier does not carry authority on its own. If a separate delivery record and run state commit separately, cover every enqueue path with a transactional outbox or a verified reconciliation procedure.

## Workflow and evidence

Design the smallest lifecycle satisfying the task: enumerate transitions and writer guards; define what happens when the request disconnects, the deadline expires, cancellation races an effect, or the host stops. If durable work is required, trace a crash at each boundary and decide whether to resume, reconcile, fail safely or ask for manual reconciliation. If streaming is required, walk through loss of the connection, retained-event expiry and terminal publication failure. For each conditional mechanism, name the pressure, owner, failure evidence, and a check that would falsify the claimed guarantee.

Build an admission-to-result path before optional scaling. Qualify cancellation with both an active and a silent upstream, and compare terminal record, effects, last public frame and actual upstream stop separately. Where real processes and stores are in scope, verify the intended entrypoint and listener identity before treating a successful response as evidence; fixtures alone establish only their own scope. Diagnose a stuck run by first locating the last committed state and its owner, then the next required hand-off; distinguish a rejected admission, an accepted but undelivered run, a live attempt, an ambiguous effect and a completed record whose output was not delivered.

Optimize only after observing connection occupancy, queue age, workload mix, execution slots, rates of failure and cancellation, effect ambiguity, and client experience. Record workload, units, effective configuration and uncertainty; no capacity, retry or retention value in an example is a portable threshold. Verify liveness separately from readiness to use the stores and scheduler. If parent work awaits children, avoid exhausting every execution slot with blocked parents.

## Related boundaries

- Read [model boundary](../agent-harness-model-and-tools/references/model-boundary.md) and [model gateway and reliability](../agent-harness-model-and-tools/references/model-gateway-and-reliability.md) for effective requests and conditional shared gateway behavior.
- Read [configuration and delivery](../agent-configuration-and-delivery/SKILL.md) for settings, compatibility, activation and revision-to-run evidence; those contracts have their own owner.

Provider-specific transport behavior belongs to the model boundary; do not assume a retry, stream termination, usage report, or billing outcome is identical across providers. Treat unmeasured routes as unmeasured and qualify the effective adapter before relying on one.
