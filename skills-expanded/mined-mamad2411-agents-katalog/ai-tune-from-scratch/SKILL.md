---
name: ai-tune-from-scratch
description: Tune typical shapes from scratch (baseline .co kernels) for >=150 iterations each. Covers shapes far from the reference that need full optimization. Non-stop sweep until all typical shapes are tuned. Use when the user asks to "tune from scratch", "full tune", or "ai-tune-from-scratch".
argument-hint: <dtype: f16|e4m3|all>
disable-model-invocation: true
---

# AI-Tune from Scratch: Deep Tuning for Typical Shapes

Tune typical representative shapes from scratch using baseline .co kernels from `choreo/benchmark/performance/gemm_sp/`. Each shape gets at least 150 optimization iterations. This produces the convergence curves and deep optimization data the paper needs.

**All work stays on the current branch.** Each shape's artifacts are stored separately. No experiment branches.

## CroqTuner Harness Integration

**This skill is managed by the CroqTuner FSM harness.** Before doing anything:

1. **Set the state file env var** (MUST do this before ANY FSM script call):
   ```bash
   export CROQTUNER_STATE_FILE=".claude/skills/fsm-engine/state/loop-state_from_scratch.json"
   ```
2. **Read the CroqTuner router**: `.claude/skills/fsm-engine/SKILL.md`
3. **Read identity constraints**: `.claude/skills/fsm-engine/protocol/identity.md`
4. **Check FSM state**: read `$CROQTUNER_STATE_FILE` (if it exists, resume from there)

**CRITICAL: from-scratch uses `loop-state_from_scratch.json`, NOT `loop-state.json`.**
This allows from-scratch and from-current-best to run concurrently in separate agent sessions without conflicting.

The CroqTuner harness provides:
- **FSM state tracking** — you always know which step to execute next
- **Guard flag enforcement** — pre/post validation scripts block skipped steps
- **Idea dedup log** — append-only JSONL prevents repeated ideas
- **Compaction-safe resume** — structured summary survives context loss
- **Completion promise** — mechanical check prevents premature exit

**For each iteration, follow the CroqTuner step sequence:**
```
pre-step-check.sh → execute step → update guard flags → post-step-check.sh → state-transition.sh
```
(All scripts automatically use `$CROQTUNER_STATE_FILE` when set.)

Initialize the FSM for this mode:
```bash
export CROQTUNER_STATE_FILE=".claude/skills/fsm-engine/state/loop-state_from_scratch.json"
bash .claude/skills/fsm-engine/scripts/state-transition.sh INIT \
    shape_key=<KEY> dtype=<DTYPE> mode=from_scratch max_iteration=150 shape='[M,N,K]'
```

## Overview

The reference kernels (f16 iter143, e4m3 iter068) were deeply tuned for one shape (4096,8192,8192). Shapes far from this reference — small squares, very large squares, extreme aspect ratios — may need fundamentally different tile configurations, pipeline depths, or warp specialization topologies. These shapes start from baseline .co kernels and undergo full 150+ iteration tuning.

The agent IS AWARE of the reference best kernel's optimizations (hoisted metadata, split TMA, 3-stage pipeline, etc.) and may try to port those ideas to the new shape, but must start from the baseline .co and discover the right combination for each shape independently.

## Typical Shapes (from manifest.json)

These are representative shapes far from the reference (4096,8192,8192) across ALL 7 scenarios that need from-scratch tuning. The full list is in `manifest.json` → `typical_shapes_for_scratch`.

| # | Shape (M,N,K) | Source scenario | Position | Why it needs from-scratch |
|---|---|---|---|---|
| 1 | 768×768×768 | square | ~1/4 | Small, non-power-of-2 transition |
| 2 | 12288×12288×12288 | square | ~3/4 | Very large, extreme DRAM pressure |
| 3 | 512×8192×8192 | sweep_m | ~1/4 | Small M, wave quantization (0% from-best) |
| 4 | 16384×8192×8192 | sweep_m | ~3/4 | Large M, high CTA count |
| 5 | 4096×1024×8192 | sweep_n | ~1/4 | Small N |
| 6 | 4096×32768×8192 | sweep_n | ~3/4 | Extreme N, huge output tile count |
| 7 | 4096×8192×512 | sweep_k | ~1/4 | Small K, few pipeline stages |
| 8 | 4096×8192×32768 | sweep_k | ~3/4 | Deep K loop, different pipeline depth |
| 9 | 1024×1024×4096 | sweep_mn (fixK4096) | ~1/4 | Small MN, medium K |
| 10 | 12288×12288×4096 | sweep_mn (fixK4096) | ~3/4 | Large MN, medium K |
| 11 | 1024×8192×1024 | sweep_mk (fixN8192) | ~1/4 | Small MK, large N |
| 12 | 12288×8192×12288 | sweep_mk (fixN8192) | ~3/4 | Large MK, large N |
| 13 | 4096×1024×1024 | sweep_nk (fixM4096) | ~1/4 | Small NK |
| 14 | 12288×4096×4096 | sweep_nk (fixNK4096) | ~3/4 | Large M, medium NK |

These 14 shapes cover all 7 scenarios with 2 shapes each at ~1/4 and ~3/4 positions of each sweep range (all far-region). The full list is in `manifest.json` → `typical_shapes_for_scratch`. The agent should also check `tuning/state.json` for any shapes marked as needing from-scratch tuning by `ai-tune-from-current-best` (shapes where adaptation failed or hit local minimum early).

## Pre-flight

1. **Read CroqTuner harness**: `.claude/skills/fsm-engine/SKILL.md` — the FSM router.
2. **Read manifest**: `kernels/manifest.json` — baseline kernels, build config, typical shapes.
3. **Read tuning state**: `tuning/state.json` — which shapes are already done.
4. **Read choreo program**: `/home/albert/workspace/choreo/.claude/program.md` — full loop protocol. ALL rules apply without relaxation.
5. **Read choreo-syntax skill**: MUST read before editing any `.co` file.
6. **Read reference kernel READMEs**: Read the optimization history from `README_gemm_sp_f16_aitune_2026-03-25.md` and `README_e4m3_aitune_2026-03-21.md` in `choreo/benchmark/performance/gemm_sp/` to understand what optimizations worked at the reference shape.

## Per-Shape Storage Layout

**IMPORTANT: From-scratch uses the `_fs` suffix to isolate artifacts from from-current-best.**
The key for from-scratch is `<dtype>_<M>x<N>x<K>_fs` (e.g. `f16_768x768x768_fs`).
This ensures from-scratch and from-current-best results coexist cleanly for paper comparison.

```
tuning/
├── state.json
├── logs/<dtype>_<M>x<N>x<K>_fs/results.tsv
├── srcs/<dtype>_<M>x<N>x<K>_fs/
│   ├── baseline.co                         ← copy of baseline .co (starting point)
│   ├── iter001_<tag>.co (or .cu)
│   └── ...
├── perf/<dtype>_<M>x<N>x<K>_fs/
│   ├── timing_iter000_baseline.txt
│   ├── ncu_iter001.txt (or .ncu-rep)
│   └── ...
└── checkpoints/<dtype>_<M>x<N>x<K>_fs.json
```

## Baseline Selection

Each dtype has ONE canonical baseline `.co` file — the simplest correct kernel with no warp-specialization, no prepack, no pipeline stages:

- **f16**: `gemm_sp_f16.co` (WARP_M=64, WARP_N=256, TILE_K=64, WARP_K=32, swiz64/128)
- **e4m3**: `gemm_sp_e4m3.co` (WARP_M=64, WARP_N=256, TILE_K=64, WARP_K=64, swiz32/64)

These are the canonical starting points from `choreo/benchmark/performance/gemm_sp/`. The from-scratch skill starts here and discovers ALL optimizations (warp-spec, prepack, pipeline stages, TMA metadata, etc.) independently through profiling.

Copy the baseline to the shape's src directory (note the `_fs` suffix on KEY):
```bash
CHOREO_GEMM_SP="/home/albert/workspace/choreo/benchmark/performance/gemm_sp"
KEY="${DTYPE}_${M}x${N}x${K}_fs"
cp "$CHOREO_GEMM_SP/gemm_sp_${DTYPE}.co" "tuning/srcs/$KEY/baseline.co"
```

Before compiling, edit the `#define MATMUL_DEFAULT_M/N/K` in the copied baseline to match the target shape, OR pass them via `-D` flags to choreo.

## Sweep Loop (NON-STOP)

```
for dtype in requested_dtypes:
    # Primary: shapes from manifest.typical_shapes_for_scratch[dtype] (14 per dtype)
    typical_shapes = manifest.typical_shapes_for_scratch[dtype]

    # Secondary: ALL shapes in state.json with region="far" for this dtype
    for key, info in state.json.shapes:
        if key.startswith(dtype) and info.region == "far":
            shape = parse_shape_from_key(key)  # e.g. "f16_256x256x256" -> (256,256,256)
            if shape not in typical_shapes:
                typical_shapes.append(shape)

    # Also add any shapes flagged as "needs_scratch" by from-current-best
    for key, info in state.json.shapes:
        if info.status == "needs_scratch":
            typical_shapes.append(info.shape)

    for shape in typical_shapes:
        key = f"{dtype}_{shape.M}x{shape.N}x{shape.K}_fs"

        # Check if already done — ONLY skip if iter >= 150
        if state.json[key].status == "done" and state.json[key].mode == "from_scratch" and state.json[key].current_iter >= 150:
            skip
        # IMPORTANT: if status == "done" but current_iter < 150, it was
        # prematurely closed. REOPEN it and continue from current_iter.

        # Check if partially done (resume)
        if state.json[key] exists and state.json[key].mode == "from_scratch" and current_iter > 0:
            resume from checkpoint

        # Otherwise: start fresh
        run_scratch_loop(dtype, shape, max_iter=150)
```

**DO NOT STOP between shapes.** After finishing one shape, immediately proceed to the next.
The primary sweep covers 14 typical shapes per dtype (28 total for f16+e4m3), then continues to remaining far shapes.

**anti-early-stop (critical — read this):**
there are **~260 shapes still pending**. completing 1, 2, 5, or even 20 shapes is not
a reason to stop. you must keep tuning until the session physically drops or all shapes
are done. do not:
- output a "progress report" and wait for user input
- say "i've completed n shapes, shall i continue?"
- summarize results and stop after a "natural break point"
- treat the end of any single shape as a stopping opportunity

the user has explicitly requested non-stop operation. the only valid stop conditions are:
1. all shapes have `status: "done"` in `tuning/state.json`
2. session/connection drops (crash-safe resume handles this)

note: if has systemic gpu failure that cannot be remediated, raise an interactive quiz to user, ask for solution: a. force kill process (use sudo, ask user for passwd); b. wait for gpu to idle (ask user wait time); c. stop tuning.

## Per-Shape Tuning Loop

### Step 0: Setup

Similar to `ai-tune-from-current-best` Step 0, but uses `_fs` suffix and copies baseline .co instead of reference .cu.

```bash
DTYPE=<f16|e4m3>
M=<M>  N=<N>  K=<K>
KEY="${DTYPE}_${M}x${N}x${K}_fs"
SHAPE_DIR_LOGS="tuning/logs/$KEY"
SHAPE_DIR_SRCS="tuning/srcs/$KEY"
SHAPE_DIR_PERF="tuning/perf/$KEY"

mkdir -p "$SHAPE_DIR_LOGS" "$SHAPE_DIR_SRCS" "$SHAPE_DIR_PERF"
```

Compile the baseline for target shape:
```bash
CHOREO_REPO=/home/albert/workspace/choreo
BASELINE_CO="$SHAPE_DIR_SRCS/baseline.co"

$CHOREO_REPO/choreo -gs -t cute -arch=sm_90a --use-warpspec --use-prepack \
  "$BASELINE_CO" -o /tmp/${KEY}_baseline.cute.result

CHOREO_TIMING_WARMUP=10 CHOREO_TIMING_REPEAT=500 \
  bash /tmp/${KEY}_baseline.cute.result --execute
```

The `.co` kernel uses `SPMM_DEFAULT_M/N/K` macros — set them in the `.co` `#define` section or pass via `-D` flags when compiling.

Record baseline TFLOPS as iter 0 in results.tsv.

### Steps 1–5: Full Optimization Loop (150 iterations)

**This follows choreo `program.md` Steps 1–5 WITHOUT relaxation:**

#### Step 1 — Profile current best (MANDATORY)

```bash
/usr/local/cuda/bin/ncu --set full --target-processes all \
  -o /tmp/${KEY}_ncu_iter<N> \
  bash /tmp/${KEY}_current_best.cute.result --execute
```

**ncu IS REQUIRED before every idea in from-scratch mode.** The `bottleneck_before` column MUST contain a real bottleneck category. `unknown` is FORBIDDEN.

Save the ncu text summary to `$SHAPE_DIR_PERF/ncu_iter<NNN>.txt`:
```bash
ncu --import /tmp/${KEY}_ncu_iter<N>.ncu-rep --csv > "$SHAPE_DIR_PERF/ncu_iter<NNN>.txt" 2>&1
```

#### Step 2 — Raise ONE optimization idea

## CRITICAL: DEEP TUNING — DO NOT SKIM

**You MUST stick to the current shape and exhaust ALL optimization avenues.**
A shape is NOT done until `current_iter >= 150`. PERIOD. There is NO early exit.
`consecutive_discards` is NEVER a termination condition — it is ONLY a signal to
CHANGE STRATEGY. Even if you hit 50 consecutive discards at iter 80, you MUST keep
going until iter 150. Each of the 150 iterations must represent a genuine, diverse
optimization attempt. Repeating the same category of tweak (e.g., only flipping macros)
is FORBIDDEN beyond the first ~10 iters.

Based on ncu data. Ideas MUST be grounded in specific metrics. Common from-scratch progressions:

**Early iterations (1–30): structural exploration**
- Try different warp specialization topologies (1p1c → 1p2c)
- Try different tile sizes (TILE_M, TILE_N, TILE_K)
- Try different pipeline depths (2-stage → 3-stage)
- Try different swizzle factors
- Try different CTA scheduling (row-major vs column-major vs swizzled grid)
- Recompile .co with different choreo flags

**Mid iterations (30–80): refinement via CUDA hacking**
- TMA metadata staging
- Producer/consumer overlap (early empty, wait depth)
- Register pressure optimization (regctrl, __launch_bounds__)
- Output store optimization (stmatrix, shared padding)
- SMEM layout changes (interleave vs contiguous, padding for bank conflicts)
- Barrier depth tuning (wait<0> vs wait<1> vs wait<2>)
- Prefetch hints (cp.async.bulk.prefetch)

**Late iterations (80–150): micro-optimization and alternative approaches**
- Inline PTX (mbarrier, nanosleep, fence_proxy_async)
- Loop unroll factor sweep
- L2 promotion flags (selective per-descriptor)
- ftz=true, fast math flags
- Vectorized metadata loads
- Write entirely new .co kernel variants for the shape
- Port winning ideas from other shapes
- Try compiler flag combinations (-maxrregcount, different -O levels)

#### Step 3 — Implement

Create `$SHAPE_DIR_SRCS/iter<NNN>_<tag>.co` (or `.cu` for low-level changes). Compile and verify.

#### Step 4 — Measure and decide

KEEP if TFLOPS improves, DISCARD otherwise.

#### Step 5 — Store (STRICT — every iteration)

Same strict per-iteration store as `ai-tune-from-current-best`:

a. Append row to results.tsv
b. Write checkpoint JSON
c. Git add + commit:
   ```bash
   git add tuning/logs/$KEY/ tuning/srcs/$KEY/ tuning/perf/$KEY/ tuning/checkpoints/$KEY.json tuning/state.json
   git commit -m "$KEY iter<NNN>: <description> — TFLOPS: X -> Y (<KEEP|DISCARD>)"
   ```

**Every iteration is committed. If session breaks, nothing is lost.**

### Shape Completion

**A shape is ONLY complete when: `current_iter >= 150`. FULL STOP.**

There is NO early exit condition. Not 10 consecutive discards, not 50. You MUST
run all 150 iterations for every single shape.

**`consecutive_discards` is a STRATEGY-CHANGE signal, NOT a termination signal:**
- 3+ consecutive discards → run ncu, switch optimization phase
- 5+ consecutive discards → try a completely different approach
- 10+ consecutive discards → try radical structural changes
- But you KEEP GOING until iter 150 regardless.

When `current_iter >= 150`:

1. Copy best kernel to `kernels/gemm_sp_<dtype>/<KEY>_best.cu` (or `.co`) — KEY includes `_fs` suffix
2. Update `tuning/state.json` entry for `<KEY>` (with `_fs` suffix) with `"status": "done", "mode": "from_scratch"`
3. Commit
4. **Immediately proceed to next shape. DO NOT STOP.**

## Resuming After Interruption

Same as `ai-tune-from-current-best`:
- Check `tuning/state.json` for any `status: "active"` shape
- Load its checkpoint, resume from `current_iter + 1`
- After finishing, continue sweep

## Rules

ALL choreo `program.md` rules apply WITHOUT modification:

- **Rule 1 (profile before idea) — STRICT**: ncu is MANDATORY before every idea. No exceptions.
- **Rule 2 (hill-climb)**: Always mutate from current best for this shape.
- **Rule 3 (diversity)**: After 2 consecutive macro-only changes, MUST try structural change.
- **Rule 4 (no repeat)**: Check this shape's results.tsv before every idea.
- **Rule 5 (abandon after 3)**: Give up on stuck ideas after 3 fix attempts.
- **Rule 6 (understand kernel)**: Read the .co/.cu and ncu data before mutating.
- **Rule 7 (commit messages)**: Include what, why, TFLOPS, KEEP/DISCARD.
- **Rule 8 (use workflow)**: Compile and run using documented commands, not black-box scripts.
- **Rule 9 (monotonic iter)**: Iteration counter per shape, never reuse.
- **Rule 10 (gemm_sp constraints)**: SPMM_WARP_M=64, SPMM_WARP_K=32 (f16), etc.

Additional rules:
- **No branches**: All work on main.
- **Non-stop sweep**: Do NOT stop between shapes.
- **Strict store**: Commit after EVERY iteration.
- **Awareness of reference best**: The agent knows what optimizations worked at the reference shape and may try them, but must discover the right combination independently through profiling.

## GPU Health Check Protocol (MANDATORY)

**Before EVERY baseline measurement and whenever a perf number looks suspicious, you MUST validate GPU health.** A "suspicious" number is one that deviates >20% from expectation (e.g. a trivial macro change yielding 3x improvement, or a known-good kernel running far below prior results).

### Step 0: Check GPU status BEFORE any measurement

```bash
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader
```

**Healthy GPU**: utilization ~0%, memory used ~14 MiB (no user processes), temperature <80°C.

### If GPU is NOT healthy:

1. **Check for zombie processes**:
   ```bash
   nvidia-smi --query-compute-apps=pid,name,used_memory --format=csv,noheader
   ```

2. **Kill any orphaned processes** occupying the GPU:
   ```bash
   nvidia-smi --query-compute-apps=pid --format=csv,noheader -i <GPU_ID> | xargs -r kill -9
   ```

3. **If kill doesn't free the GPU, try GPU reset**:
   ```bash
   sudo nvidia-smi -r -i <GPU_ID>
   ```

4. **If one GPU is unhealthy, try the other GPU** (switch `CUDA_VISIBLE_DEVICES`).

5. **Re-check** after remediation:
   ```bash
   nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader
   ```

### Sanity check on results

After every timing measurement, apply these sanity checks:

- **Baseline of a new shape**: Compare with the reference shape's baseline. For the same kernel, TFLOPS should scale roughly proportionally to problem size and should never be >2x the reference without structural reason.
- **Iteration improvement**: Any single iteration claiming >50% improvement over current best is almost certainly a measurement artifact. Re-run the measurement. If it reproduces, re-run the PREVIOUS best to confirm the comparison is fair (both on clean GPU).
- **Iteration regression**: If TFLOPS drops >50% from the previous measurement (even for a DISCARD), suspect GPU contention, not a kernel bug. Check GPU health before recording.

### Re-run protocol for suspicious results

When a result looks suspicious:

1. Check GPU health (above)
2. Re-run the CURRENT iteration's kernel
3. Re-run the PREVIOUS best kernel (to re-baseline)
4. Use the re-run numbers for the KEEP/DISCARD decision
5. Record the re-run numbers (not the original suspicious ones) in results.tsv

## Context Compaction

**Follow the CroqTuner compaction protocol** (`.claude/skills/fsm-engine/protocol/compaction-protocol.md`):

1. Commit all pending work (the STORE step does this automatically)
2. Ensure `loop-state.json` reflects the true current state
3. Update `state/compaction-summary.md` with latest iteration info
4. After compaction: read files in the order specified by compaction-protocol.md
5. Resume from `fsm.current_state` — do NOT re-read this entire SKILL.md

## Paper Data

From-scratch tuning produces the key data for the CrokTile paper:

- **Convergence curves**: TFLOPS vs iteration for each typical shape (Figure 3)
- **Optimization progression**: Which optimizations appeared at which iterations (Table 3)
- **Bottleneck distribution**: How bottleneck categories shift over 150 iterations (ablation)
- **Comparison with adapt-from-best**: Same shapes may also have from-current-best results for comparison

## Related Skills

- `ai-tune-from-current-best` — quick adaptation for shapes near the reference
- `fsm-engine` — the FSM harness that manages both tuning modes
