---
name: ml-inference-perf
description: "Measure latency, throughput, memory, and optimization tradeoffs. Use for latency/throughput/resource benchmarking; ml-training-cost covers training."
---

# ml-inference-perf

Measure latency, throughput, memory, and optimization tradeoffs.

## Choose this workflow

Use for latency/throughput/resource benchmarking; ml-training-cost covers training.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML deployment methods](../../references/packs/ml-deployment.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Inspect supplied performance evidence or plan measurement; apply for requested benchmark code or bounded runs.

**Pack prerequisites:** Versioned model and preprocessing artifacts, input/output schema, runtime/dependencies, operating targets, and authorized environment. Validate artifact trust before loading formats that can execute code. Packaging or writing monitoring configuration does not deploy a model or enable a hosted service.

- **Infer from evidence:** Read artifact format/trust, preprocessing schema, serving runtime, compatibility and existing rollout controls.
- **Reasonable default:** Prepare packaging/configuration and isolated checks without treating them as a live deployment.
- **Ask only when needed:** Resolve the target, rollback compatibility and operating limits before rollout or load generation; missing production access does not block packaging.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Latency, throughput, memory, batching, warmup, and optimization tradeoffs.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Specify hardware, precision, batch/concurrency and payload distribution as comparable benchmark conditions.
2. Separate load and warmup from steady state, and measure bounded authorized workloads, including tail behavior within caps.
3. Identify bottlenecks and check quality after any optimization.

## Technical method

- **Inspect:** Measure preprocessing, transfer, model compute, postprocessing, batching and queue time with representative inputs.
- **Method:** Compare latency distribution, throughput, memory and quality at the actual workload/concurrency; synchronize device timing where required.
- **Avoid misdiagnosis:** Timing asynchronous GPU dispatch without synchronization underreports work; throughput gains may violate tail-latency requirements.
- **Check the result:** Warm up deliberately, retain cold-start evidence and verify optimized predictions against reference tolerances and quality constraints.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML deployment worked example](../../references/examples/ml-deployment.md).


## Decision branches

- **When quantization or batching improves speed:** Re-evaluate quality, memory and latency under the same workload before accepting it.
- **When the request is for local preparation or implementation:** Write the requested benchmark with warmup, workload and correctness controls; report speed claims only for measured hardware and inputs.

## Deliver and verify

- Benchmark protocol or results with conditions, sample size, cold/warm/tail metrics and quality comparison, and an optimization recommendation or authorized patch.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Tail latency and throughput are reported under stated load; quantization gains include a quality comparison.

## Stop and recover

- No production load or paid hardware implicitly. A single warm request cannot establish capacity.

## Example requests

- **Normal (plan):** Plan a bounded benchmark for cold/warm latency and throughput at fixed quality.
- **Edge (plan):** Benchmark batched inference under a latency deadline without hiding warmup cost.
- **Blocked (inspect):** Plan a benchmark with no authorized hardware or production traffic budget.
