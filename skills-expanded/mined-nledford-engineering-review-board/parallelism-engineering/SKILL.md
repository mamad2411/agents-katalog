---
name: parallelism-engineering
description: Design and implement cross-language CPU-bound, data-parallel, and task-parallel computation. Use when decomposing a measured workload into partitions or tasks; selecting granularity, executors or worker pools, reductions, cancellation, failure handling, or deterministic concurrency tests. Do not use for routine async I/O, distributed coordination, Spark, GPU programming, or review-only performance work.
---

# Parallelism Engineering

Use this skill for the design shared by local CPU, data, and task parallelism.
Keep source-language and runtime mechanics with the matching language or runtime
skill: its executor APIs, memory model, synchronization primitives, task syntax,
package choice, build configuration, and test commands are not prescribed here.

Use [`python-engineering`](../python-engineering/SKILL.md),
[`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md),
[`ruby-engineering`](../ruby-engineering/SKILL.md),
[`rust-engineering`](../rust-engineering/SKILL.md), or another matching language
skill for implementation mechanics. For Rust async or web-runtime work, also use
[`rust-async-web`](../rust-async-web/SKILL.md).

## Scope And Routing

Use this skill when useful work is primarily local and CPU-bound, and parallel
decomposition, ownership, scheduling, or deterministic aggregation is the main
design risk. It may accompany a language skill while code is implemented.

Do not use it for:

- routine asynchronous I/O, event loops, request handling, or ordinary `await`
  usage; use the matching language or async/runtime skill;
- distributed coordination, remote worker orchestration, consensus, or cluster
  scheduling; use the applicable distributed-system, platform, or architecture
  owner;
- Spark, PySpark, Structured Streaming, or distributed analytical execution;
  use [`data-platform-engineering`](../data-platform-engineering/SKILL.md);
- GPU kernels, device memory, or accelerator programming; use the relevant
  language, runtime, or accelerator-specific guidance; or
- a performance or scalability audit without an implementation/design task; use
  [`performance-review`](../performance-review/SKILL.md).

This skill does not select package-specific executor APIs or packages, run pools
or benchmarks, prescribe workload thresholds, or claim a speedup. Establish and
compare a measured baseline through the target repository's approved
implementation and benchmark lanes before reporting any performance result.

## Workflow

1. **Define the workload and baseline.** State the operation, input distribution
   and size range, correctness invariant, latency or throughput goal, hardware
   and runtime assumptions, and a sequential or current implementation baseline.
   Label estimates and unknowns; do not infer a speedup from core count.
2. **Choose the unit of parallel work.** Separate CPU work from I/O, setup,
   serialization, synchronization, and result handling. Identify independent
   tasks or data partitions, dependencies, critical sections, and the dominant
   scaling variable.
3. **Decompose deliberately.** Choose data parallelism, independent task
   parallelism, pipeline stages, or a bounded sequential design. Keep the
   smallest decomposition that exposes real independence; retain sequential
   processing when work is too small, skewed, ordered, or dependency-bound.
4. **Set partitioning and granularity.** Define partition ownership, a target
   cost per unit, imbalance handling, input skew behavior, and whether static or
   dynamic scheduling is justified. Account for task creation, dispatch,
   serialization, cache locality, and merge overhead; measure thresholds rather
   than treating a partition size as universal.
5. **Choose execution bounds.** Derive worker or pool limits from available CPU,
   memory per work item, downstream limits, coexistence with the host runtime,
   and repository constraints. Reuse bounded executors when appropriate; avoid
   unbounded queues, unbounded task creation, and one worker per item.
6. **Minimize shared mutable state.** Prefer immutable inputs, partition-local
   state, message passing, ownership transfer, or confined mutation. Make each
   remaining shared resource, synchronization rule, lock order, and lifetime
   explicit.
7. **Specify reduction and determinism.** Define result ownership, merge order,
   identity values, duplicate handling, and error aggregation. Preserve a stable
   ordering when callers require it. For floating-point or otherwise
   non-associative work, state acceptable numerical variation or use a
   deterministic reduction; never assume parallel ordering is reproducible.
8. **Design cancellation and failure behavior.** Define who can cancel, how
   cancellation reaches queued and running work, which results remain valid,
   cleanup ownership, timeout behavior, retry eligibility, and whether one task
   failure fails the whole operation. Ensure failure cannot strand workers,
   locks, permits, memory, files, or partial outputs.
9. **Control nested parallelism.** Identify library, runtime, or caller-level
   parallel regions. Establish one owner for the concurrency budget, cap inner
   regions or serialize them when necessary, and document how oversubscription
   is avoided.
10. **Plan a reproducible benchmark.** Use representative input sizes and skew,
    fixed environment and runtime settings where feasible, warm-up policy,
    repeated samples, and sequential/current-versus-candidate comparison. Report
    distributions and resource use, not a single favorable elapsed time. Do not
    execute the plan under this skill; use the target repository's language and
    benchmark workflow.
11. **Check concurrency hazards and bounds.** Reason about races, atomicity,
    visibility, deadlock, lock ordering, starvation, livelock, queue growth,
    memory amplification, file-descriptor or connection exhaustion, and cleanup
    on every terminal path. Use the source runtime's tools and checks for the
    actual implementation.
12. **Test observable invariants.** Add deterministic tests with controlled
    scheduling or bounded fakes where available; property tests that compare
    partitioned results with a trusted sequential oracle; and bounded stress
    tests for skew, cancellation, failures, and repeated runs. Avoid timing-only
    assertions. Run the narrow language test lane before broader repository
    checks, and report unsupported race detectors or unavailable stress
    environments.

## Safety And Evidence

- Do not treat an executor limit, synthetic test, static permission, or prompt
  as containment. Untrusted code or workloads require operating-system,
  container, or VM isolation selected by the environment owner.
- If attacker-controlled input can set workload size, fan-out, partition count,
  timeout, or resource consumption, load [`security-review`](../security-review/SKILL.md)
  and [`security-review-evidence`](../security-review-evidence/SKILL.md). Consider
  [`threat-modeling`](../threat-modeling/SKILL.md) when the resource-exhaustion
  boundary is being designed.
- If native extensions, executors, benchmark harnesses, or dependencies are
  selected or changed, use
  [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
  for their provenance and installation risk. Keep language-specific dependency
  mechanics with the matching language owner.
- Do not expose credentials, private inputs, paths, or sensitive benchmark data.
  Report sanitized measurements, assumptions, failed checks, and residual risk.

## Completion Evidence

Report the workload and baseline definition; decomposition and concurrency-budget
decisions; shared-state, reduction, cancellation, and nested-parallelism rules;
tests and race/deadlock/resource checks run; benchmark evidence if measured; and
unmeasured assumptions, skipped environments, and residual risks. State that no
speedup is established when no before-and-after representative measurement exists.
