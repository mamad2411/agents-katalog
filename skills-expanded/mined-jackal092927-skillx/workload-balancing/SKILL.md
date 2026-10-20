---
skillx:
  name: workload-balancing
  purpose: Improve throughput of the chosen parallel TF-IDF/search design by partitioning and scheduling work to reduce idle time and stragglers.
  role: secondary-support
  scope_in:
    - partition document/query work units for already-selected process-based parallel execution
    - choose static vs dynamic scheduling based on workload skew
    - tune chunk granularity to trade off scheduling overhead vs straggler risk
  scope_out:
    - not for selecting the core concurrency primitive
    - not for modifying TF-IDF correctness semantics or ranking behavior
    - not for complex distributed schedulers or elaborate balancing frameworks
  requires:
    - a functioning parallel path from python-parallelization
    - observability into per-chunk runtime variability
    - a partitionable workload (documents, shards, or query batches)
  preferred_tools:
    - static chunking for near-uniform cost workloads
    - dynamic submission/queueing for skewed cost workloads
    - coarse-enough chunks to amortize process and IPC overhead
  risks:
    - over-partitioning into tiny tasks
    - under-partitioning that creates stragglers
    - balancing logic overhead exceeding throughput gains
    - accidental nondeterminism in output assembly policy
  precedence:
    - never override correctness-equivalence constraints set by python-parallelization
    - performance tuning is valid only after correctness is stable
  examples:
    - input: Parallel TF-IDF search has some slow batches; improve utilization across 8 workers.
      expected_behavior: adjust chunking/scheduling to reduce idle workers and stragglers without changing output semantics.
---

# Objective Order (Bundle-Aware)

1. Respect correctness and execution semantics defined by `python-parallelization`.
2. Improve worker utilization and reduce tail latency.
3. Minimize scheduling overhead while preserving determinism requirements.

# Role Contract

Apply this skill **after** a valid parallel architecture exists.
It does not choose whether to parallelize; it improves how work is distributed within that design.

Typical responsibilities:
- choose static vs dynamic partitioning,
- define chunk size policy,
- identify and reduce straggler patterns.

# Conflict Resolution Rules

If balancing suggestions conflict with other skills:
- defer to `python-parallelization` for semantic correctness and assembly guarantees,
- coordinate with `memory-optimization` when chunk choices inflate memory footprint.

When in doubt, prefer slightly less aggressive balancing over semantic risk.

# Practical Guidance

Start simple:
- static chunking for uniform workloads,
- dynamic scheduling only when runtime skew is real.

Avoid tiny tasks that spend more time in scheduling/IPC than useful compute.
Validate gains with end-to-end timing, not only per-task micro-metrics.
