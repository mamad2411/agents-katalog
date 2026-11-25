# AGENTS.md

Shared guidance for any agent (Claude Code, Cursor, Aider, etc.) working in this repo.

> **Status:** the project is mid-pivot. The direction below is agreed; concrete schemas, file layouts, and tooling are still shaping. When code or older docs disagree with this file, treat this file as intent and ask before doing large structural work. See issue #13 for the full vision write-up.

## What this repo is

The canonical home for authoring, validating, and tracking **Spyre-aware Triton kernels** for IBM Spyre/AIU accelerators.

The validated Spyre-aware Triton kernel is the primary artifact. KTIR remains a useful downstream lowering reference, committed where it serves the kernel work, but it is no longer the deliverable.

## What "Spyre-aware" means

Kernels here should:

- Use **real-world shapes** that exercise nested loops, residual iteration, and scratchpad pressure — not toy shapes that conveniently avoid them.
- Reflect Spyre's execution model: **fixed 32 cores** (not unbounded GPU programs), explicit M/N/K inner-core looping that fits scratchpad.
- Use **`tl.make_tensor_descriptor`** for data IO. `tl.make_block_ptr` is deprecated upstream and Spyre's lowering targets the descriptor API — do not invest in the block-pointer path for new work.
- Be ready to absorb future Spyre-only ops (e.g., `reduce(..., scope="all_cores")`) as they land in Triton.

Three authoring invariants (T1, see below) summarize this: **tiles fit scratchpad, grid fits 32 cores, runtime-arg agnostic.**

## Validation tiers

Every kernel carries a status across these tiers. The inventory should make it obvious at a glance which kernels are production-ready, which are drafts, and what's planned.

- **T0 — Numerical equivalence:** matches a PyTorch/reference implementation within tolerance, validated on GPU.
- **T1 — Spyre-shape compliance:** satisfies the three authoring invariants above.
- **T2 — KTIR/Spyre validation:** output matches reference on `ktir_cpu` and/or real Spyre hardware where available.
- **T3 — Human-reviewed:** signed off by a domain expert.

When adding or changing a kernel, state which tiers it currently meets and which it targets.

## Non-goals

- **Not** a general Triton optimization repo — Spyre-aware specifically.
- **Not** a KTIR examples repo — KTIR lives here only as it serves the kernel work.
- **Not** vLLM-specific — vLLM is a source of kernels, not the scope.
- **Performance optimization is out of scope for now.** It is expected to follow once authoring/validation is solid. Don't propose perf work unless asked.

## How agents should work here

- **Reference kernels are the strongest signal.** Before drafting anything new, read existing kernels in `kernels/` for the patterns this repo prefers (descriptor IO, 32-core grids, scratchpad-conscious tiling). Match those patterns rather than importing GPU-tutorial idioms.
- **Keep originals.** GPU-shaped reference implementations stay around as numerical-validation oracles, even after a Spyre-aware rewrite lands. Don't delete them when porting.
- **Stay in the loop.** Agentic tooling (kernel-author, kernel-validator, inventory-updater style skills) is meant to give humans leverage, not autopilot. Stop at review checkpoints; surface gaps explicitly rather than papering over them.
- **Ask before large structural changes.** Repo layout, inventory schema, and per-kernel directory conventions are still being decided. A kernel-level change is fine; a sweeping reorg should wait for human direction.
- **Prefer `make_tensor_descriptor` in new code.** Existing `tl.make_block_ptr` call sites will be ported; don't add new ones.
