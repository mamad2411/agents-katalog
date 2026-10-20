---
skillx:
  name: python-parallelization
  purpose: Own the primary concurrency design for CPU-bound TF-IDF indexing and batch search, while preserving exact output equivalence to the sequential baseline.
  role: primary
  scope_in:
    - choose and implement process-based parallel execution for independent TF-IDF/index/search work units
    - define worker model, serialization boundaries, and deterministic result assembly
    - establish correctness-equivalence checks against sequential behavior before accepting speedup claims
  scope_out:
    - not for distributed cluster orchestration
    - not for changing TF-IDF semantics, ranking rules, or tokenization behavior
    - not for memory-tuning details or chunk policy fine-tuning beyond what is needed to make parallel execution valid
  requires:
    - a known-correct sequential reference path
    - picklable worker-call boundaries for process execution
    - CPU-bound hotspot confirmation or strong prior from workload shape
  preferred_tools:
    - concurrent.futures.ProcessPoolExecutor
    - multiprocessing-style process workers for compute-heavy steps
    - explicit equivalence checks between sequential and parallel outputs
  risks:
    - GIL-limited threading used on CPU-heavy paths
    - non-picklable callables or state breaking worker execution
    - hidden shared mutable state causing correctness drift
    - speedup claims accepted without output-equivalence validation
  precedence:
    - correctness-equivalence dominates all optimization guidance
    - if another skill recommendation conflicts with output equivalence, reject that recommendation
  examples:
    - input: Parallelize TF-IDF indexing and query batches on 8 cores while keeping results identical to the current engine.
      expected_behavior: choose process-based parallelism, keep deterministic output assembly, and validate equivalence before discussing speedup.
---

# Objective Order (Bundle-Aware)

1. Preserve exact correctness vs. sequential baseline.
2. Obtain real multi-core speedup on CPU-bound work.
3. Keep overhead bounded so gains survive outside toy inputs.

# Role Contract

Use this skill as the **decision owner** for:
- whether to parallelize,
- which process primitive to use,
- what worker boundaries are valid,
- and how final results are reassembled deterministically.

Do not delegate these core decisions to `workload-balancing` or `memory-optimization`.
Those skills refine execution once this core design is stable.

# Conflict Resolution Rules

If guidance conflicts:
- `python-parallelization` keeps authority on correctness-equivalent execution semantics.
- `workload-balancing` may adjust chunking/scheduling only if equivalence remains intact.
- `memory-optimization` may reduce copies/temporaries only if equivalence and worker stability remain intact.

Reject any change that improves benchmark timing but alters output behavior.

# Practical Guidance

Parallelize independent units such as document partitions or query batches.
Use bounded worker counts and avoid per-item process spawning.
Keep worker functions top-level/picklable and keep shared mutable state out of the hot path.

Treat this as the first skill in the application order:
**parallel design first, then balancing, then memory discipline hardening.**
