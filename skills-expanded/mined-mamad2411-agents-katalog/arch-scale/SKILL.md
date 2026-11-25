---
name: arch-scale
description: "Identify bottlenecks for a specified workload and growth scenario. Use for workload-driven capacity design; perf measures and repairs a specific bottleneck, and test-load executes an authorized workload."
---

# arch-scale

Identify bottlenecks for a specified workload and growth scenario.

## Choose this workflow

Use for workload-driven capacity design; perf measures and repairs a specific bottleneck, and test-load executes an authorized workload.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Architecture methods](../../references/packs/architecture.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; workload shape, expected growth, SLOs, current metrics, and resource limits.

**Pack prerequisites:** Readable source, infrastructure/configuration definitions, and any supplied system documentation. Runtime telemetry is optional evidence, never assumed available. Architecture proposals remain plans until implementation is requested.

- **Infer from evidence:** Trace current entry points, data owners, deployment units and documented constraints before proposing boundaries.
- **Reasonable default:** Prefer extending an existing owner while scale or organizational evidence is absent; mark capacity estimates as assumptions.
- **Ask only when needed:** Ask for an unresolved consistency, compatibility or ownership requirement only if it changes the design; missing telemetry limits capacity claims, not source mapping.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Capacity constraints and targeted scaling strategy; no speculative whole-system rewrite.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. State workload shape, service objectives and measured constraints: arrival rate, service time distribution, concurrency, queue age and resource saturation. Separate observed production data from assumptions or synthetic samples.
2. Locate the limiting serial/shared boundary before recommending replicas, caching, queues or extraction. Model steady-state and burst behavior, failure recovery and downstream limits with explicit units.
3. Compare options against the bottleneck and consistency requirements. Define admission control/backpressure and degradation before adding unbounded concurrency; scaling callers can overload the shared dependency.
4. Propose a bounded measurement or authorized load experiment with rejecting observations and recovery. Report the capacity range established by evidence and what remains unknown; do not invent traffic or throughput.

## Technical method

- **Inspect:** Obtain workload shape, service-time distribution, concurrency limits, queue age and dependency quotas.
- **Method:** Locate the first saturated shared resource; estimate concurrency from throughput and mean time only under stated steady-state assumptions, then measure tail behavior.
- **Avoid misdiagnosis:** Adding replicas can exhaust a database connection budget or amplify retries before increasing throughput.
- **Check the result:** Compare a bounded workload at the same mix and revision, including saturation, queue recovery and downstream limits.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Architecture worked example](../../references/examples/architecture.md).


## Decision branches

- **When a shared database or serialized step dominates:** Quantify that constraint before recommending application replicas or new services.

## Deliver and verify

- Bottleneck model, assumptions, capacity experiments, scaling sequence, and cost factors.
- Assumptions, limiting resource, incremental options and a bounded benchmark plan.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A serialized database operation is not solved by app replicas alone; estimates identify their workload assumptions.

## Stop and recover

- No invented capacity numbers or automatic provisioning. Missing measurements yield an instrumentation/benchmark plan first.

## Example requests

- **Normal (plan):** Plan capacity experiments for a tenfold increase in checkout traffic.
- **Edge (plan):** Plan growth for a service bottlenecked by a serialized inventory update.
- **Blocked (inspect):** Assess scale without production metrics; avoid invented throughput estimates.
