---
name: xdna-programming
description: Program the AMD XDNA2 NPU on this Strix Halo box (Ryzen AI MAX+ 395, AIE2P / npu2, 8x4 cores) by either route — Triton kernels compiled by Triton-XDNA (Triton → MLIR-AIR → AIE), or hand-written IRON/mlir-aie dataflow designs + Peano (llvm-aie) C++ kernels run through XRT/pyxrt — and wire them into PyTorch (torch.compile backend "xdna" / torch-xdna, XDNA-vLLM, gemma-npu). Covers picking the route, the environment, transform schedules, resident tensors, memtile/cascade designs, packaging as tl.extra.npu ops, verifying against the CPU, honest NPU-vs-CPU measurement, the hardware's measured limits and every gotcha hit so far. Use whenever a task touches the NPU — writing, porting, tuning or debugging an NPU kernel or model, Triton-XDNA, IRON, ObjectFifo, aiecc, Peano, xclbin/ELF/insts.bin, pyxrt, xrt-smi, hw contexts, conv3x3 / qwen3_stack, torch-xdna, XDNA-vLLM, or requests like 「放到 NPU 跑」「手刻 NPU kernel」「NPU 為什麼比 CPU 慢」 — even when XDNA is not named.
---

# Programming the XDNA2 NPU (this box)

Everything here was measured or built on this machine (2026-09 → 2026-10). It is the
working knowledge behind Triton-XDNA's `tl.extra.npu.conv3x3` (52.6 TOPS, 86% of peak),
`tl.extra.npu.qwen3_stack` (OmniVoice's whole backbone step in one launch, 1.6-1.7x CPU
int8), torch-xdna, gemma-npu and XDNA-vLLM. Numbers carry their conditions; re-measure
before you lean on one for a decision.

## The one idea to keep

The NPU has **5x the CPU's int8 compute but half its DRAM bandwidth, and every launch
costs 0.1-0.4 ms** (a context switch 1-2 ms). An op only wins if it has high arithmetic
intensity **and** stays on the array long enough to amortize the launch — or if it runs
**concurrently** with CPU work. Per-op offload of small GEMMs, elementwise ops or decode
GEMVs loses to the Zen 5 CPU every time it has been tried here. So:

| situation | what has worked |
|---|---|
| big prefill GEMMs (M ≥ ~1k) next to CPU work | Triton int8 GEMM, overlapped with CPU (gemma-npu pipeline, XDNA-vLLM split) |
| a whole block of a model, called many times (diffusion steps, CNN layers) | hand-written design: the whole block in **one launch**, data stays on chip |
| an op that needs peak (conv, cascade reduction, weights stationary) | hand-written design + intrinsics kernel |
| decode / GEMV / batch-1 small layers | leave on the CPU (bandwidth-bound; NPU streams weights at 33-35 GB/s vs CPU 100-114) |

Measured roofs: NPU int8 51 TOPS (`xrt-smi validate`; 61 theoretical), DDR ~55 GB/s;
CPU int8 `torch._int_mm` 9.7 TOPS, bf16 4.4 TFLOPS, ~118 GB/s. The NPU's roof is higher
only above ~176 int8 ops/byte. Full table: `references/hardware.md`.

## Pick the route

1. **The model is PyTorch and you want it on the NPU with least effort** → torch-xdna:
   `model = torch.compile(model, backend="xdna")`, then `torch_xdna.report()`. It moves
   parameter GEMMs (W8A8), 3x3 convs and Qwen3-0.6B-shaped stacks; `policy="auto"` times
   NPU vs CPU per shape. Read `references/integration.md` first.
2. **A new op with tile semantics** (GEMM, elementwise, norm, softmax) → **Triton route**:
   `@triton.jit` + a transform schedule, compiled by Triton-XDNA. Fast to write; a DDR-fed
   GEMM tops out at ~7-10 TOPS. → `references/triton-route.md`
3. **Peak throughput, fusion across layers, weights or partial sums kept on chip, cascade
   chains, one launch per model step** → **hand-written route**: IRON design (Python,
   mlir-aie) + per-core C++ kernels (Peano), run with pyxrt, packaged as a
   `tl.extra.npu.<op>`. Days, not hours. → `references/handwritten-route.md`, starting
   from `assets/handwritten_op/` (tested, runs as is).
4. **LLM serving** → XDNA-vLLM (prefill GEMMs split CPU/NPU; decode stays on the CPU). →
   `references/integration.md`

Before building anything, estimate: FLOPs and bytes per launch, time at 51 TOPS / 55
GB/s, plus 0.1-0.4 ms per launch, vs the CPU at 9.7 TOPS / 118 GB/s. If the NPU estimate
is not clearly ahead, the plan needs fusion or overlap, or it should stay on the CPU.
Say so to the user rather than building it.

## Environment

```bash
source ~/src/Triton-XDNA/npu-env.sh             # sandbox venv (Python 3.13) + XRT + mlir-aie/air paths
export PEANO_INSTALL_DIR=~/src/Triton-XDNA/sandbox/lib/python3.13/site-packages/llvm-aie  # hand-written route
bash ~/.claude/skills/xdna-programming/scripts/npu_status.sh   # device, driver, who holds hw contexts, toolchain
```

The agent's Bash tool runs bash, but every call is a fresh shell: put the `source` in the
same command as the work. The user's terminal is fish: there, `bash -c 'source ...; python x.py'`.
Python must be 3.13 (`/opt/xilinx/xrt/python/pyxrt` is cp313 only). Other venvs on top of
the same stack: `~/src/omnivoice-npu/venv` (torch-xdna, OmniVoice), `~/src/XDNA-vLLM/.venv`.
No `/dev/accel/accel0` → the box booted with the IOMMU off: use the `npu-toggle` skill.

Toolchain in the sandbox: mlir_aie_no_rtti 1.4.5.dev51 (e040370), llvm-aie 22.0.0
(2026-10-12), mlir_air 2026-10-20, torch 2.14 CPU. The sandbox's installed Triton-XDNA
backend is a **hand-copied snapshot** of `~/src/Triton-XDNA` — check
`diff -rq amd_triton_npu/backend sandbox/lib/python3.13/site-packages/triton/backends/amd_triton_npu`
before trusting a feature (as of 2026-10-28 it lacks `resident.set_device_writes`).

## Workflow (either route)

1. **Baseline first.** Time the CPU doing the same thing (Inductor / `torch._int_mm` /
   oneDNN, 16 threads) on the same shapes. This is the number to beat.
2. **Start from working code**: a Triton-XDNA example (`examples/matmul_i8_k_loop`,
   `rms_norm`, `test_softmax`, `swiglu`, `resident_tensors`) or `assets/handwritten_op`.
   Run it unchanged first to prove the environment.
3. **Correctness before speed**: compare with a CPU reference on the same inputs — bit
   exact for integer math, a stated tolerance for bf16/bfp16 (~1% per GEMM stage). Test
   every build variant and the edges (1 row, max rows, padding). Details:
   `references/measurement.md` → Verification.
4. **Measure honestly** (`references/measurement.md`): NPU launch alone, op with host
   work, end to end; median of ≥10 after warm-up; interleaved A/B in one process; note
   `/proc/loadavg` (the box is shared). Report against the roofline. Never claim a
   speedup that was not measured.
5. **Explain where the time goes** before optimizing: launches × fixed cost, DDR bytes /
   55 GB/s, MAC time, host layouts. A hardware trace (`references/handwritten-route.md` →
   Trace) beats guessing.

## Gotchas that cost the most time (all in `references/troubleshooting.md`)

- **Two processes building in one `air_project` dir silently corrupt binaries, and the bad
  binary is cached.** Give each process its own `AMD_TRITON_NPU_AIR_PROJECT_PATH` **and its
  own cwd**: aircc writes its work files (core ELFs, PDIs, `full_elf_config.json`) to
  `<cwd>/air_project` and `params.txt` / `data.txt` to the cwd whatever the setting says, and
  `.build.lock` only guards the configured dir (verified 2026-10-28). Looked like a K=512
  int8 / K=768 bf16 miscompile.
- **The NPU does not snoop CPU caches.** Sync BOs to/from the device (XRT `sync`) or flush
  yourself; skipping the post-run sync gave 0.3-2% stale results.
- **Each compiled kernel (each grid / shape) is its own hardware context.** Triton-XDNA keeps
  `driver._MAX_LIVE_SESSIONS` (default 8; env `AMD_TRITON_NPU_XRT_MAX_SESSIONS` is read at
  `import triton`) and evicts beyond it: a rebuild costs ~35-80 ms. The FLM server already
  holds 10 contexts. Use one grid per shape and set the cap directly.
- **Cores start in floor rounding** (the sandbox wheel writes crRnd = 0 at core entry):
  fp32→bf16 matched torch for 51.5% of values; with
  `aie::tile::current().set_rounding(aie::rounding_mode::conv_even)` 100% (measured
  2026-10-28). Triton kernels can't call that: rewrite the core entry with the Peano wrapper
  (`references/triton-route.md` → Numerics). bf16 matmul operands run as **bfp16** (8 values
  share an exponent): ~1% error per GEMM whatever K.
- **`tl.exp` / `tl.sigmoid` use the AIE2P `exp2` instruction, a linear-mantissa
  approximation with up to ~6% error**: SiLU/GELU/softmax in Triton kernels carry ~7% worst
  per-element error. Check per-element error, not just RMS.
- **Triton elementwise BLOCK sizes: as large as L1 allows.** Each grid program costs
  ~2.6-2.9 µs and short DMA runs crawl: SwiGLU 2048x3072 took 18.9 ms at the examples'
  BLOCK=1024 vs 1.62 ms at 65536.
- **mlir-aie (the wheel) sets AIE2's saturation register index on AIE2P**: integer SRS never
  saturates (values wrap). Call `set_sat()` in the kernel (fixed on the fork, wheel not rebuilt).
- **Odd K-step counts disable ping-pong buffering** in Triton-XDNA GEMMs (lock stalls 35% vs
  13%): pad K to an even number of BLOCK_K steps.
- **mlir-aie and mlir-air Python bindings cannot share a process**: build IRON designs in a
  subprocess when Triton-XDNA is imported.
- **The transform schedule is read when a kernel compiles** (and at launch from
  `npu_config`): one `AIR_TRANSFORM_TILING_SCRIPT` per kernel; set/restore it around calls.
- **Single-op benchmarks hide whole-model regressions** (L3 pollution, sync cost, context
  thrash). Always A/B the full model.

## Where things live

| path | what |
|---|---|
| `~/src/Triton-XDNA` | compiler + `tl.extra.npu` ops (`amd_triton_npu/language/npu/`: conv3x3, qwen3_stack, fused_decode/prefill), examples. Push target: remote `fork` (AyaSakura-comp/Triton-XDNA, main); `origin` is amd — never push there |
| `~/src/torch-xdna` | `torch.compile(backend="xdna")`; `results/*.md` = the investigations (npu_investigation, npu_profile, conv3x3_cascade, omnivoice_npu) |
| `~/src/XDNA-vLLM` | vLLM 0.32 + `xdna_int8`; `docs/xdna/kernels.md` = how to add an NPU kernel; push main only |
| `~/src/gemma-npu` | HF Gemma 4 E2B with NPU prefill GEMMs pipelined against CPU attention; `serve.py` :8078 |
| `~/src/mlir-aie-latest` | mlir-aie source (fork: crSat fix); `programming_examples/`, `aie_kernels/`, and upstream agent skills in `skills/` (aie-code-creator, aie-kernel-opt, ...) |
| `~/src/llvm-aie-peano` | Peano worktree with the vector min/max legalizer fix (`build/bin/llc`) |
| `~/npu-fa` | hand-written flash-attention decode + GDN kernels (C++ XRT runner) |
| `~/xdna2-lab/wiki` | XDNA2 microarchitecture wiki (zh-TW; query via the `amd-llm-wiki` skill) |

Git: commit locally; push only when the user asks, and only to their own repos / `fork`
remotes. Never bare `git stash` (shared across worktrees).

## Reference files

- `references/hardware.md` — the array, memories, DMA limits, MAC rates, precision formats,
  every measured roof and fixed cost.
- `references/triton-route.md` — writing kernels for Triton-XDNA: schedules, resident tensors,
  config knobs, contexts, what fails to lower and why.
- `references/handwritten-route.md` — IRON designs, Peano kernels, cascade/memtile patterns,
  builds, pyxrt, merged contexts, packaging as `tl.extra.npu` ops, traces, kernel-level levers.
- `references/integration.md` — torch-xdna internals, adding a fused op to torch.compile,
  XDNA-vLLM, gemma-npu's CPU/NPU pipeline, FLM coexistence.
- `references/measurement.md` — verification recipes, timing and A/B rules, roofline reporting.
- `references/troubleshooting.md` — symptom → cause → fix for everything hit so far.
- `assets/handwritten_op/` — a complete hand-written op (kernel + IRON design + pyxrt host,
  32 cores, memtile split/broadcast/join), verified on this NPU.
- `scripts/npu_status.sh` — environment and device health check.
- `scripts/make_peano_wrap.sh OUT_DIR` — a wrapper Peano root for Triton-XDNA builds (log or
  rewrite core compiler calls; the round-to-nearest-even fix).
- `scripts/triton_rounding_check.py WORK_DIR` — which rounding mode Triton kernels get
  (~3 s); also the template for an isolated per-process build dir.

Reply to the user in Traditional Chinese (Taiwan) when they write Chinese.
