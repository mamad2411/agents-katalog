---
name: optimization-catalog
description: >
  Compatibility router for the shared optimization knowledge base and the language-specific
  optimization catalog skills. Use when: (1) selecting which optimization catalog skill to load,
  (2) the implementation language is not fixed yet, (3) a workflow still references the legacy
  optimization-catalog skill name, (4) deciding whether a finding is shared or language-specific,
  (5) updating the generalized knowledge-base structure.
---

# Optimization Catalog Router

Use this skill as a dispatcher. The shared root knowledge base remains the canonical location for algorithmic patterns that transfer across implementation languages. Language-specific overlays capture implementation details tied to a specific DSL or programming model.

## Load Order

1. Read the shared root knowledge under `docs/knowledge/optimizations/` and `docs/knowledge/anti-patterns/` when the pattern is algorithmic.
2. Load the language-specific optimization catalog skill for the chosen implementation language.
3. Read language overlays in `docs/knowledge/languages/<language>/...` only when the implementation details depend on that surface.

## Language-Specific Catalog Skills

| Language key | Load this skill | Language-specific knowledge root |
|--------------|-----------------|----------------------------------|
| `cutile-dsl` | `/optimization-catalog-cutile-dsl` | `docs/knowledge/languages/cutile-dsl/` |
| `cute-dsl` | `/optimization-catalog-cute-dsl` | `docs/knowledge/languages/cute-dsl/` |

## Classification Rule

- Shared root catalogs are for algorithmic patterns, workload-shape rules, and anti-patterns that transfer across DSLs.
- Language overlays are for implementation details that depend on a specific API, compiler behavior, code-generation surface, or scheduling model.
- When in doubt, keep the reusable mechanism in the shared root and add a language-specific overlay only for the implementation surface.

## Current Migration State

- The shared root catalogs in `docs/knowledge/optimizations/` and `docs/knowledge/anti-patterns/` remain the compatibility-preserving baseline.
- New language-specific overlays are being added under `docs/knowledge/languages/`.
- Existing references to the legacy root paths continue to work during the migration.

## Knowledge Base Principles

The goal of this catalog is to build reusable cuTile kernel design knowledge, not to accumulate device folklore.

Every entry must therefore be written as:

- a **pattern** or **anti-pattern** that can transfer across kernels,
- with a clear **context** describing when it applies,
- with explicit **performance metrics affected**,
- with evidence separated into **local validation**, and **generalized takeaway** when relevant.

Device and architecture facts are encouraged when they sharpen the rule:

- architecture families such as Blackwell or Hopper,
- architecture capabilities such as Tensor Cores, TMA, thread block clusters, scheduler behavior, or shared-memory limits,
- device-level specs such as peak FP16/BF16 TFLOP/s, peak memory bandwidth, ridge point, SM count, registers/SM, or SMEM capacity.

But those facts must be converted into reusable guidance. Entries should avoid collapsing into "kernel X on device Y liked config Z" unless that observation is only being used as evidence for a broader pattern.

## How This Catalog Works

1. **Index below** maps trigger conditions → optimization → detail file
2. **Orchestrator** reads index to pick optimizations based on profiling results
3. **Kernel designer** reads detail files to implement specific optimizations
4. **New optimizations**: create detail file in `docs/knowledge/optimizations/` + add row to index
5. **Failed optimizations**: create anti-pattern in `docs/knowledge/anti-patterns/` + add row below

## Optimization Index

| ID | Optimization | Trigger Conditions | Est. Impact | Pitfalls | Detail File |
|----|-------------|-------------------|-------------|----------|-------------|
| O1 | Split-KV proportional block allocation | Dual-path kernel has strongly unbalanced latent vs decompressed work; equal block split leaves one path starved | Very High | Requires a reduction kernel and intermediate tensors | `docs/knowledge/optimizations/split-kv.md` |
| O2 | Head grouping for shared-operand reuse | Same operand is reused across heads (for example latent `Z`) and `Bh=1` produces skinny per-head MMAs or near-zero TC utilization | Very High | Raises register pressure; not appropriate for per-head-only operands like decompressed `K/V` | `docs/knowledge/optimizations/head-grouping.md` |
| O3 | Independent path scheduling | After Split-KV, the latent and decompressed paths still want different streaming granularities or load scheduling | Low-Med | Gains are modest if register pressure and occupancy do not improve | `docs/knowledge/optimizations/independent-tiles.md` |
| O4 | Swizzle scheduling | Tiled kernel reuses one operand across neighboring CTAs and block order measurably affects L2 locality | Low | Compute-bound kernels may see only marginal benefit; 1D remap adds index overhead | `docs/knowledge/optimizations/swizzle.md` |
| O5 | Latency hints | Load/compute overlap tuning is needed after the kernel structure is already sound, and the per-path DRAM pressure differs enough that compiler guidance may help scheduling | Low | Difficult to isolate; hints are suggestions rather than guarantees | `docs/knowledge/optimizations/latency-hints.md` |
| O6 | CGA thread block clusters | Hopper+ kernel has genuine cross-CTA data sharing opportunity or needs to reason correctly about `num_ctas` semantics and cluster launch behavior | Medium | Hardware-specific and easy to misuse when there is no real sharing benefit | `docs/knowledge/optimizations/cga.md` |
| O7 | Fast math for online softmax | Online-softmax loop is heavy on `exp2`/division, larger tiles collapse compute throughput, and reduced-precision inference math is acceptable | High | Not a substitute for sane tiling; gains shrink if spills or bandwidth dominate | `docs/knowledge/optimizations/fast-math-online-softmax.md` |
| O8 | Causal K-loop split | Causal attention has many fully unmasked K-tiles, only diagonal/tail tiles need mask logic, and future tiles can be skipped | Medium-High | Can be neutral or negative if masking is no longer material on the target bottleneck | `docs/knowledge/optimizations/causal-k-loop-split.md` |
| O9 | Causal ProgramId remap | Triangular work causes wave-tail imbalance across CTAs and a simple launch-order reversal is available | Low-Med | Small gain if work distribution is already uniform or the grid is tiny | `docs/knowledge/optimizations/causal-program-id-remap.md` |
| O10 | Adaptive tile and occupancy autotuning | Best tile/occupancy point changes with sequence length or device envelope; fixed manual choice underfills short shapes or overcommits long ones | High | Search space can explode if not curated; cannot rescue a structurally broken kernel | `docs/knowledge/optimizations/adaptive-tile-autotuning.md` |
| O11 | Pipeline-driven low-occupancy scheduling | Large unavoidable per-CTA state forces one CTA/SM or very low occupancy, and the kernel must win via overlap and scheduling rather than more resident warps | High | Requires architecture/DSL support for fine-grained scheduling; cannot be faked with a monolithic CTA | `docs/knowledge/optimizations/pipeline-driven-low-occupancy.md` |

## Anti-Pattern Index

| ID | Anti-Pattern | Failure Mode | Source | Detail File |
|----|-------------|-------------|--------|-------------|
| A1 | Equal block split across heterogeneous paths | 50/50 block allocation for unequal latent vs decompressed work produces sequential bottlenecks instead of overlap | MLA-var6+ V0 | `docs/knowledge/anti-patterns/equal-block-split.md` |
| A2 | `TILE_M=1` combine/decompression | Single-row combine GEMMs disable Tensor Cores and leave a persistent tail at small `s` | MLA-var6+ V0/V2/V3 | `docs/knowledge/anti-patterns/tile-m-one-combine.md` |
| A3 | Underfilled persistent concurrency | Resident block budgets below the SM count leave the GPU idle and make overlap ineffective | MLA-var6+ V4 | `docs/knowledge/anti-patterns/underfilled-persistent.md` |
| A4 | Register-ceiling persistent stage | Persistent kernel lands at the register ceiling (`255` regs/thread), collapses occupancy, and becomes latency-bound | MLA-var6+ V4 | `docs/knowledge/anti-patterns/spill-heavy-persistent.md` |
| A5 | Blind large-tile port | Copying a tile shape from another device without revalidating registers, SMEM, local-memory traffic, and grid size crosses a resource cliff | FlashAttention learning chain | `docs/knowledge/anti-patterns/blind-large-tile-port.md` |
| A6 | Uniform causal masking | Paying full causal-mask logic on every K-tile wastes work even though most tiles are fully valid or fully skipped | FlashAttention learning chain | `docs/knowledge/anti-patterns/uniform-causal-masking.md` |
| A7 | Sub-16 MMA dimension | Shrinking any effective MMA dimension (`M`, `N`, or `K`) below `16` usually breaks Tensor Core coverage and explodes latency instead of fixing occupancy | FlashMLA V1 manual probes + Tensor Core shape constraints | `docs/knowledge/anti-patterns/sub-16-mma-dimension.md` |
| A8 | Blind dataflow flip | Rewriting a resource-sensitive Tensor Core kernel into an algebraically equivalent operand orientation changes codegen enough to reintroduce spills or worsen SMEM behavior | FlashMLA V1 → V2 | `docs/knowledge/anti-patterns/blind-dataflow-flip.md` |

## Cross-Referencing: Metrics → Optimizations

| Profiling Metric State | Likely Optimizations |
|----------------------|---------------------|
| Equal-duration kernels with obviously unequal work | O1 (Split-KV proportional block allocation) |
| `Bh=1` or per-head skinny MMAs on a shared operand | O2 (Head grouping) |
| Dual-path kernel plateaus near the ridge point after Split-KV | O3 (Independent path scheduling) |
| L2 hit < 90% and neighboring CTAs reload the same operand tiles | O4 (Swizzle scheduling) |
| Same kernel structure but different path-level memory pressure suggests compiler scheduling changes may matter | O5 (Latency hints) |
| Cross-CTA data sharing on Hopper+ or confusion about what `num_ctas` actually controls | O6 (CGA thread block clusters) |
| Tensor Core/MMA structure is sound, but online-softmax special functions dominate the hot loop | O7 (Fast math for online softmax) |
| Causal kernel still spends meaningful time in mask/control flow because many K-tiles are fully valid and future tiles are fully skipped | O8 (Causal K-loop split) |
| Causal/triangular workload shows tail imbalance across CTAs or waves finish unevenly | O9 (Causal ProgramId remap) |
| Short shapes underfill the GPU while long shapes prefer different tiles or occupancy hints | O10 (Adaptive tile and occupancy autotuning) |
| Registers/SMEM force one CTA/SM, eligible warps stay very low, and the kernel is compute-bound but still under-utilizes Tensor Cores | O11 (Pipeline-driven low-occupancy scheduling) |
| Combine stage has `TILE_M=1` and `TC Util = 0%` | A2 (`TILE_M=1` combine/decompression) |
| Persistent resident blocks < SM count or waves/SM < 1 | A3 (Underfilled persistent concurrency) |
| Persistent stage at `255` regs/thread with single-digit occupancy | A4 (Register-ceiling persistent stage) |
| Imported large tile causes register/SMEM cliffs, local-memory traffic, or abrupt grid shrinkage on the target device | A5 (Blind large-tile port) |
| Causal masking logic is paid uniformly across all K-tiles despite obvious fully-valid and fully-skipped regions | A6 (Uniform causal masking) |
| Candidate tile drives any effective MMA dimension below `16`, or Tensor Core FLOPs collapse far below algorithmic FLOPs after a "smaller tile" change | A7 (Sub-16 MMA dimension) |
| Proposed optimization is only an algebraic operand/dataflow flip, especially near a register or SMEM cliff | A8 (Blind dataflow flip) |

## Knowledge Base Update Protocol

For the full update protocol, detail file template, and step-by-step instructions, load the `/orchestration-workflow` skill.
