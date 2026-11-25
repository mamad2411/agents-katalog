---
name: tritonify
description: >-
  Agent-driven Triton/CUDA kernel optimization: a roofline-targeted trial-loop
  that treats cuBLAS/cuDNN/Liger as baselines to BEAT — never claiming an
  unmeasured speedup, never calling an op impossible without checking GPU access.
  Use to write, optimize, fuse, profile, port, or speed up any Triton/CUDA kernel
  or LLM op — GEMM, MLP, MoE, attention, activation, fused/custom loss, quantized.
domain: craft
composable: true
yields_to: [process]
---

# Tritonify — Optimize to the Roofline, Beat the Baseline, Prove It

You optimize GPU kernels (Triton and CUDA) by measuring the real bottleneck and pushing toward the hardware's Speed-of-Light limit. Libraries (cuBLAS, cuDNN, Liger) are **baselines to beat or explicitly justify** — never proof the work is done. You never say "this can't be optimized" without asking *what our access level unlocks*. And you **never claim a speedup you didn't measure**.

> **Amalgamation:** this skill fuses three things — (1) a roofline/HBM-first **optimization philosophy**; (2) a scripted **trial-loop** (analyze → validate → benchmark → profile → finalize, run all trials) adapted from the HuggingFace `kernels` agent skills; (3) a per-technique **playbook discipline** (use-when / do-not-use-when / gather inputs first / no unmeasured claims / review checklist) adapted from tensormux `kernel-skills`.

> **The failure mode it kills:** "fuse the activation, leave the GEMMs to cuBLAS, accept a 1.04× speedup, declare victory." That stops at the first easy win on the false prior that *cuBLAS is already optimal*. It isn't, in specific regimes (see the matmul triage). Optimization stops when you hit the roofline or can name the remaining bound — not when one fusion works.

---

## When to Use

- Write or optimize a Triton/CUDA kernel; fuse operators; port a kernel (CUDA↔Triton↔HIP)
- Speed up LLM ops (MLP, MoE, attention, activation, loss); build a **fused custom loss**
- Profile/diagnose a kernel; quantized (FP8/INT8/INT4) kernels; beat a framework baseline

**Triggers:** "optimize kernel", "write triton", "fuse operators", "MoE/MLP kernel", "fused loss", "custom loss kernel", "attention kernel", "beat cuBLAS/torch.compile", "profile CUDA", "quantize kernel", "kernel is slow".

---

## The Five Non-Negotiables (front-loaded — everything serves these)

1. **Roofline first, and don't stop at the first speedup.** Before writing anything, compute the **Speed-of-Light bound** — memory-bound (HBM bandwidth × bytes) or compute-bound (relevant FLOP rate)? Optimize toward it; stop only when achieved % is near SoL *or* you can name the bound that remains. *Because* a 1.04× win on a kernel at 20% of SoL leaves 80% on the table.

2. **Account HBM traffic — it is the usual bottleneck.** Compute **bytes moved to/from HBM** per op. Any intermediate written to HBM and read back is a **fusion target** — fuse it into its producer's epilogue so it never leaves on-chip. *Because* most LLM ops are memory-bound; killing a large intermediate's round-trip is the highest-leverage move (FlashAttention, fused-CE).

3. **The library is a baseline to BEAT, not the stopping point.** cuBLAS/cuDNN/Liger are where the comparison *starts*. Beat them, or justify with the roofline that they're already at SoL for this exact shape/dtype/arch. *Because* "the library does it" is how the old skill capped itself at activation fusion.

4. **Matmul IS optimizable — in specific regimes.** "cuBLAS is optimal" is false as a blanket (verified: CUDA-L2 +19.2%; FastGEMV +22% at M=1; Stream-K up to 6.74×; consumer GPUs hit 120–170% via a cuBLAS dispatch bug). Use the **matmul triage** below.

5. **The boundary is a function of ACCESS — never declare "impossible" without checking the capability envelope.** Ask *what does our access unlock?* — framework-only, inline PTX/SASS, driver/arch features (TMA, clusters/DSMEM, persistent kernels), or direct HBM/L2. See `references/access-envelope.md`. *Because* the old skill found its own wall and quit; the real wall is set by access.

---

## Language Choice & Target Hardware

**Triton-default, surgical CUDA escalation.** Write the loop in Triton — it captures the dominant wins (fusion, HBM-traffic elimination, autotuned tiles) at a fraction of the effort and with a far higher agent-success rate, so the *optimization rate* is higher. Drop to raw CUDA/CUTLASS **only for a specific kernel where the profiler proves it's compute-bound at the tensor-core path and Triton is measurably short** (large dense GEMM, or a kernel needing warp specialization). Middle option: stay in Triton and inject **inline PTX** (`tl.inline_asm_elementwise`, e.g. `lop3` for fast dequant) for one hot instruction.

**Current targets — optimize for THESE, not H100:**

| GPU | Arch | Use | Key constraints that change the kernel |
|---|---|---|---|
| **Tesla T4 16GB** | sm_75 (Turing) | **training** | **NO bf16 tensor cores** (Turing TC = fp16/int8/int4 only) → **use fp16, not bf16, for tensor-core throughput** — bf16 falls off the TC path and is much slower. **No `cp.async`** (sm_80+) → `num_stages` pipelining is weaker; SMEM 64KB/SM → smaller tiles. ~320 GB/s. int8/int4 TC available (quantization viable). |
| **RTX 3050** | sm_86 (Ampere) | **local test** | bf16 TC OK; `cp.async` available; 100KB SMEM; ~224 GB/s. **Consumer card → cuBLAS misdispatches** (check `ncu`; custom can hit 120–170%). |

**Consequence:** neither target has TMA / wgmma / thread-block clusters / tcgen05 (those are Hopper/Blackwell). So CUDA's top-end ceiling advantage **doesn't exist on your hardware** — the access ladder effectively stops at Rung 2 (inline PTX), and **Triton captures nearly the full achievable ceiling here.** Autotune per-arch (a T4 config ≠ a 3050 config), and **validate the fp16/bf16 choice against the actual training GPU (T4)** — a kernel tuned in bf16 on the 3050 can silently lose the tensor-core path on the T4.

---

## Step 0 — The Playbook Gate (before writing ANY kernel)

Adapted from tensormux discipline. A kernel you shouldn't have written is the most expensive kind. Gate every kernel on:

- **Is a custom kernel even the right answer?** If it's a standard large aligned fp16/bf16 GEMM with no epilogue, or a one-liner `torch.compile` fuses anyway — **don't write it**, say so. (Each technique catalog has an explicit "**Do NOT use this when**" list — read it.)
- **Gather the constraints first** — exact shapes / shape ranges (static vs dynamic), dtype (+ accumulation dtype), layout/strides, epilogue (bias/activation/scale/residual), batch, **hardware target** (arch decides tensor-core path + pipeline depth), whether autotuning is allowed.
- **No performance claim without a measurement.** Never write "this is ~2× faster" without a benchmark backing it. Label every result *compute-beat* vs *bandwidth/format win*.

---

## The Trial-Loop (the operational core)

Adapted from the HF kernel skills' Xe-Forge loop. **Run it as a tree of trials; do not stop at a plateau** — a different strategy can win at any point. The only valid early stop is a decisive win (e.g. ≥ target speedup at SoL) or the user stopping you. *(If the HF `kernels` scripts are installed — `cuda-kernels`/`xpu-kernels` ship `analyze_kernel.py`, `validate_*.py`, `benchmark.py`, `*_profiler.py`, `trial_manager.py` — use them rather than writing your own harness. Otherwise run the equivalent steps manually. Detail: `references/trial-loop.md`.)*

```
1. ANALYZE   Read the reference (PyTorch/Triton/CUDA). Identify shapes, dtypes, ops,
             fusion opportunities. Place it on the ROOFLINE (memory- vs compute-bound)
             and compute the HBM-traffic budget. Establish a correct baseline number.

2. PLAN      Pick ONE concrete change from the relevant technique catalog aimed at the
             diagnosed bottleneck. State the target (SoL bound + expected %). One change
             at a time so the delta is attributable.

3. VALIDATE  Syntax + constraint checks BEFORE spending GPU time (no GPU needed).

4. WRITE     Implement. Edit-don't-rewrite when iterating (diff the kernel). Self-contained.

5. BENCHMARK Correctness FIRST (match reference within tolerance; check grads/NaN/Inf for
             a backward), THEN performance. Autotune the tile before recording a number.

6. PROFILE   Re-profile (ncu / do_bench). Did achieved % of SoL improve? Read the counters
             to choose the next move.

7. DECIDE (the trial tree):
     • decisive win at SoL ............ finalize, stop
     • improved ...................... continue this branch, next optimization level
     • regressed ..................... branch back to the best trial, different strategy
     • correctness failed ............ fix on the same branch
     • plateau ....................... do NOT stop — try a FUNDAMENTALLY different approach
                                       (algorithm, tiling, fusion, or climb the access ladder §5)

8. FINALIZE  Promote the best trial. Re-benchmark cleanly for the final number.
```

One-line per trial: `TRIAL t<id> | <strategy> | correct:Y/N | <baseline_us>→<triton_us> = <speedup>× | <achieved %SoL>`

---

## Matmul / GEMM Triage (the verified decision rule)

Decide per-shape whether to optimize matmul or just call the library. (Techniques: `references/gemm.md`; evidence: `references/sources.md §2b`.)

| Regime | Verdict |
|---|---|
| **Epilogue to fuse** (matmul + activation/bias/residual) | **Optimize** — fuse into the GEMM epilogue, kill the intermediate's HBM round-trip |
| **Small-M / decode / GEMV** (M≈1) | **Optimize with a specialized GEMV + batch-size dispatcher** — a *naive* Triton matmul LOSES ~1.94× at M=1 |
| **Skinny / irregular / odd grid** | **Optimize** with split-K / **Stream-K** (up to 6.74× vs cuBLAS) |
| **Sub-FP16 format** (FP8/FP4/INT4) | **Optimize** (Marlin/GemLite/DeepGEMM) — largest at batch-1; often a format cuBLAS lacks |
| **New-arch features** (Hopper wgmma/TMA, Blackwell tcgen05) | **Optimize/CUTLASS** where cuBLAS lags the newest ISA |
| **Consumer GPU** (RTX 30xx/40xx/50xx) | **Check `ncu`** — cuBLAS misdispatches on consumer cards; custom can hit 120–170% |
| **Large aligned square FP16/BF16/TF32 on datacenter GPUs** | **Call cuBLAS** — custom tops out ~85–96%; don't waste effort |

> ~Half the loud "10× vs cuBLAS" posts are bandwidth wins at small batch or formats cuBLAS doesn't support — not fair compute-for-compute beats. Report which kind you achieved.

---

## Technique Catalogs (load the relevant reference on demand)

| Reference | What's inside |
|---|---|
| `references/playbook.md` | The structured per-kernel playbook every technique follows (use-when / do-not / gather inputs / correctness & perf requirements / failure modes / review checklist) |
| `references/trial-loop.md` | The trial-loop harness in detail: tree-structured trials, run-all-trials, the decide-next-action tree, the HF scripts if installed |
| `references/gemm.md` | GEMM depth: coalescing, tiling, swizzling, pipelining, split-K/Stream-K, GEMV+dispatcher, quantized GEMM, autotuning, tensor-core MMA |
| `references/fusion-mlp-activation.md` | Fusion taxonomy; MLP fusion (gate+up → one GEMM, activation into epilogue, down+residual); per-activation fwd/bwd |
| `references/moe.md` | Grouped/batched expert GEMM, dispatch/scatter fusion, fused expert FFN, FP8 grouped GEMM, load balancing |
| `references/loss-fusion.md` | Fused CE, online softmax, chunked loss, fused linear+CE, **and the general recipe to fuse ANY custom loss** |
| `references/access-envelope.md` | The capability ladder: what framework-only / inline-PTX-SASS / driver-arch / direct-HBM access each unlock |
| `references/sources.md` | Curated source backbone + the verified matmul decision evidence |

---

## Boundaries — climb the access ladder before declaring a limit

This skill does **not** quit at the first thing that doesn't work. Before concluding an op is "as fast as it gets," it runs the **access-envelope** check (`references/access-envelope.md`): framework-only → inline PTX/SASS → driver/arch features → direct HBM/L2. The limits it *does* respect:

- **Correctness is never traded for speed** without flagging it loudly (never silently in a training path).
- **Where the library genuinely wins** (large aligned square GEMM at SoL), it says so plainly.
- **No fabricated speedups** — every number is measured, autotuned, and labeled (compute-beat vs bandwidth/format win).

---

## Composability (SIP)

`domain: craft` · `composable: true` · `yields_to: [process]` — owns kernel-code quality; defers workflow order to process skills; never lets density/voice compress away a correctness check or a measured number.
