---
name: deploy-kimi-k3-on-rtx-pro-6000
description: Deploy and serve Moonshot Kimi-K3 (2.8T MoE, hybrid KDA+MLA attention, native vision via MoonViT-3d) from Unsloth's GGUF quantizations (unsloth/Kimi-K3-GGUF) via llama.cpp on a Linux server with 8x NVIDIA RTX PRO 6000 Blackwell Server Edition (96 GB, sm_120) GPUs. Unlike vLLM/SGLang's tensor-parallel all-in-VRAM serving, this is CPU+GPU hybrid inference (llama-server's --n-cpu-moe / --override-tensor): routed MoE experts split between GPU-resident (fast) and CPU-resident (AVX-512 compute; AMX is not used for MoE experts) depending on how much VRAM you dedicate — or, with a quant that fits the 765 GiB pool (UD-IQ2_XXS, or a locally REAP-sliced UD-Q2_K_XL-REAP770), fully GPU-resident at ~2x the decode speed, so the full ~2.8T-parameter model runs on hardware with far less combined VRAM than its weight size — the tradeoff SGLang/sglang-kt-KTransformers are built to avoid but don't yet support for this model (SGLang has Kimi-K3 support only for the native MXFP4 checkpoint, no GGUF path; sglang-kt/KTransformers has no Kimi-K3 support at all as of 2026-09). Vision requires building from an unmerged fork (unslothai/llama.cpp PR #70) since mainline llama.cpp's Kimi-K3 support (merged 2026-08-15) is text-only; BUILD_SOURCE switches between the two. Quant level is chosen at deploy time via QUANT= (any subdirectory in the repo, e.g. UD-Q2_K_XL, UD-Q4_K_XL) with a sizing/feasibility gate before download. Use when deploying or serving Kimi-K3 GGUF quants on RTX PRO 6000 Blackwell / sm_120 hardware, choosing a --n-cpu-moe split, wiring up MoonViT-3d vision in llama.cpp, or troubleshooting a build against the Unsloth vision fork vs mainline llama.cpp for this model.
---

# Deploy Kimi-K3 (GGUF, llama.cpp) on 8x RTX PRO 6000 Blackwell Server Edition (sm_120)

Serve **Kimi-K3** (2.8T MoE; hybrid Kimi Delta Attention + MLA; native MoonViT-3d vision; 1M
context) from **Unsloth's GGUF quantizations**, via **llama.cpp built from source** — OpenAI-
compatible API on a configurable port, **CPU+GPU hybrid** (not TP-across-VRAM), weights bind-
mounted read-only from local NVMe.

**Why llama.cpp, why GGUF, why hybrid — not vLLM/SGLang/TP:** at UD-Q2_K_XL the checkpoint is
~861 GB — larger than an 8x96 GB VRAM pool (768 GB) can hold even before KV cache, so a pure-VRAM
tensor-parallel engine (the pattern `deploy-kimi-k26-on-rtx-pro-6000` uses) is a non-starter no
matter how many GPUs you throw at it. Two ways to bridge that gap both get called "CPU offload,"
and only one of them works here:
- **Layer-wise weight streaming** (vLLM `--cpu-offload-gb`, SGLang `--cpu-offload-gb`
  `--offload-group-size`) shuttles whole weight tensors GPU<->CPU every forward pass while the GPU
  still does the math — decode becomes PCIe-bound. At this model's scale (~800 GB of experts) it's
  unusable, not just slow.
- **Expert-granular hybrid inference** — llama.cpp's `-ncmoe/--n-cpu-moe` (or the finer-grained
  `-ot/--override-tensor`) — keeps routed MoE experts CPU-resident and **computes them on the CPU**
  (AMX/AVX-512), while attention, shared experts, and the vision tower stay GPU-resident. The GPU
  never waits on a PCIe copy of an expert it's about to run; it just doesn't run the CPU-resident
  ones. This is the only approach that makes sense for a model this size on this hardware, and it's
  what this skill deploys.
- **SGLang's KTransformers backend (sglang-kt)** does the same expert-granular split
  architecturally, and would be the natural fit (attention+KV cache TP across your GPUs, experts
  split GPU/CPU via `--kt-num-gpu-experts`) — but has **no Kimi-K3 support** as of 2026-09
  (kvcache-ai/ktransformers#2109, open, unresolved). Revisit this skill if that lands; it would
  likely outperform llama.cpp's hybrid path (KTransformers' own reported numbers for other
  trillion-parameter MoE models: 220+ tok/s aggregate, ~299ms median inter-token latency).
- **SGLang mainline** has native Kimi-K3 support (day-0, 2026-07-27) but only for the **native
  MXFP4 checkpoint** — no GGUF loading path for this architecture. Doesn't apply to Unsloth's
  quants at all.

**Hardware target:** 8x **RTX PRO 6000 Blackwell Server Edition** (GB202, 96 GB, sm_120) — 765 GiB of
VRAM in total, which is the number that matters most: a quant that fits it entirely decodes ~2x faster
than the hybrid path (REFERENCE.md "All-VRAM quants"). Host CPU: 2x Xeon 6730P with AVX-512 (+AMX,
which turns out to be irrelevant to the experts — REFERENCE.md "Build flags") and 1 TiB RAM for the
hybrid path. Needs the NVIDIA driver (>=570, open kernel module), Docker, nvidia-container-toolkit — **no host
CUDA toolkit needed** (the build happens inside Docker, which ships its own).

**Why build from source in Docker (not a stock image, unlike kimi-k26):** no upstream llama.cpp
release — mainline or the fork — ships a prebuilt image with both CUDA sm_120 kernels and this
host's AMX/AVX-512 CPU kernels baked in; both repos are also young enough (mainline K3 support:
2026-08-15; the fork: still unmerged) that you want a pinned commit, not a moving `latest`. Build
once per `BUILD_SOURCE`, keep the image, rebuild only when bumping the pin.

## Workflow

1. **Verify host** — `nvidia-smi` (GPU count/VRAM), `lscpu | grep -i amx` (confirms the AMX path is
   available; note if absent, don't fail — just document the fallback is slower), free disk on
   local NVMe for the chosen quant (step 3 sizes this precisely), GPU containers work via CDI:
   ```bash
   docker run --rm --device nvidia.com/gpu=all --entrypoint nvidia-smi nvidia/cuda:13.0.0-base-ubuntu24.04
   ```
   **Check `nvidia-smi` for who else is using the GPUs before claiming any** — this hardware target
   is commonly a shared pool (see kimi-k26's REFERENCE.md "Access model" for the sharing
   convention this skill inherits). A hybrid deploy can be tuned to use fewer GPUs (lower
   `--n-gpu-layers` / a `GPU_ARGS` device subset, more CPU-resident experts) if the full pool isn't
   free — see step 3's `--n-cpu-moe` note.

2. **Choose the quant** — AskUserQuestion *"Which Kimi-K3 GGUF quant?"* if not already decided by
   the deploy context. Three are verified end-to-end on this hardware (2026-09-05, all with
   text+vision+tool-call `verify.sh` and a perplexity/KLD gate — REFERENCE.md "Quant gate"):
   - **`UD-Q2_K_XL`** (19 shards, 802 GiB) — hybrid, ~130 GiB of experts on CPU: the reference quality
     (GSM8K 98.0 / HumanEval 97.0 / MBPP 98.5 %), 5.8 tok/s single-stream with TTFT 4.6 s, 16.0 tok/s
     aggregate at c8 (`-ub 4096`; the CPU and 130 GiB of RAM stay busy while it runs).
   - **`UD-IQ2_XXS`** (16 shards, 662 GiB; experts mostly IQ1_M) — fits VRAM: 13.9 tok/s single-stream,
     ~25 tok/s aggregate at c4–c8. KLD 0.37 / 84.6 % top-token agreement vs Q2_K_XL, yet on the task
     check (200 GSM8K, 164 HumanEval, 200 MBPP) it scores 97.5 / 95.7 / 97.0 % — KLD overstates its damage.
   - **`UD-Q2_K_XL-REAP770`** (one 697 GiB file, made locally: Q2_K_XL with the 14 % least-used experts
     sliced off — REFERENCE.md "REAP expert slicing") — fits VRAM at near-Q2_K_XL quality (KLD 0.047 /
     95.4 %): ~86 ms/token at 8 slots with `--fit-target 4096` (a 6144 margin silently spills 2–3
     expert layers to the CPU and costs 40 %), 17.9 tok/s aggregate at c16, TTFT 3.6 s at c1; with the
     interactive profile (2 slots + DSpark) 12.96 tok/s / 62 ms single-stream. **Task check: GSM8K 98.0 %,
     but HumanEval 86.6 % and MBPP 85.5 % vs 95.7 / 97.0 % for IQ2_XXS** (REFERENCE.md "Quant gate") — the
     expert cut damages code generation despite the far better KLD; not the right default for coding use.
   Other Unsloth quants are mechanically supported (`QUANT=<dir-name>`) but unvetted; **`UD-TQ2_0`
   is known to produce corrupted logits on these GPUs** — any new IQ/TQ quant must pass the gate before
   it is served. Step 3's sizing gate refuses downloads that cannot fit disk or VRAM+RAM.

3. **Download** — sizing-gated, into the HF hub cache, pinned to a commit:
   ```bash
   bash scripts/download.sh unsloth/Kimi-K3-GGUF <commit-sha> UD-Q2_K_XL
   ```
   The script sums the quant directory's bytes via the HF tree API **before** downloading anything,
   compares against free disk (`df`) and a rough VRAM+RAM feasibility check, and refuses (with the
   numbers) if it won't fit — see REFERENCE.md "Sizing gate." Also fetches `mmproj-BF16.gguf`
   (~0.9 GB, needed for vision) and, separately, the small non-weight files from `moonshotai/Kimi-K3`
   (tokenizer/config only — the benchmark client needs an HF-format tokenizer, which the GGUF repo
   doesn't ship; see REFERENCE.md "Tokenizer for benchmarking").

4. **Choose the build source** — AskUserQuestion *"Vision now (unmerged fork) or text-only
   (mainline)?"* if not already decided:
   - **`BUILD_SOURCE=fork` (default, needed for vision)** — `unslothai/llama.cpp` PR #70
     (`kimi-k3-vision-only` branch), pinned to its current head commit. Unmerged, third-party;
     expect to re-pin as it evolves (it already superseded one earlier attempt, PR #48).
   - **`BUILD_SOURCE=mainline` (text-only)** — `ggml-org/llama.cpp` at/after commit `ad1de39`
     (2026-08-15, Kimi-K3 text merge). No `--mmproj`, no vision. Switch to this once vision lands
     upstream (tracking issue `ggml-org/llama.cpp#28264`) to drop the fork dependency.
   ```bash
   BUILD_SOURCE=fork     bash scripts/build_image.sh   # -> kimi-k3-llamacpp:fork-<shortsha>
   BUILD_SOURCE=mainline bash scripts/build_image.sh   # -> kimi-k3-llamacpp:mainline-<shortsha>
   ```
   Compiles CUDA (sm_120) + CPU (AMX tile/int8/bf16, AVX-512) kernels from source — see
   REFERENCE.md "Build" for the exact cmake flags and expected build friction (young code on both
   sides of `BUILD_SOURCE`).

   **Smoke-test the image before committing to the real checkpoint** — a tiny public GGUF proves
   the build + GPU/CDI plumbing work in seconds, vs. discovering a broken image after a ~15min+
   cold load of the real ~861 GB model:
   ```bash
   IMAGE=kimi-k3-llamacpp:fork-<shortsha> bash scripts/smoke_test.sh
   ```
   A pass means "the image works," not "Kimi-K3 will load" — it doesn't exercise the
   architecture-specific flags (`--numa`, `--cache-type-*`, `--n-cpu-moe`) that only matter once
   the real model loads.

5. **Launch**:
   ```bash
   QUANT=UD-Q2_K_XL BUILD_SOURCE=fork bash scripts/serve_docker.sh   # foreground; DETACH=1 to daemonize
   ```
   Knobs that matter (all env vars of `serve_docker.sh`): `IMAGE` (pin it — several images coexist),
   `BATCH`/`UBATCH` (**4096 for hybrid** — halves TTFT by copying the CPU experts once per prompt;
   **2048 for all-VRAM**), `EXTRA_ARGS` (all-VRAM needs `--fit-target 6144`, otherwise the CUDA
   scratch pool OOMs on the first request after a full load), `DOCKER_ENV` (e.g.
   `GGML_CUDA_DISABLE_GRAPHS=1` for A/Bs), `N_CPU_MOE` (manual split), `CACHE_RAM` (0 only when
   benchmarking). Container: CDI GPUs (`GPU_ARGS`, defaults to all 8 — override to a subset if the pool
   isn't free), weights `:ro`, `--ipc=host`, `--network host` bound to the host's Tailscale IP (falls
   back to loopback-only if Tailscale isn't up) — matches the tailnet-direct access model, not
   NCCL/RDMA-related (this is a single-process multi-GPU layer-split, no all-reduce). Also always
   sets `--numa distribute`, `--cache-type-k f16 --cache-type-v f16`, and
   `--threads/--threads-batch <physical core count>` — these are Kimi-K3/hardware requirements, not
   tuning choices (REFERENCE.md "Runtime requirements that are NOT tunable"; that section also
   covers two host/launch prerequisites this step depends on, `numa_balancing=0` and `--load-mode
   none`, both **required**, not optional — skipping either measured as a 20+-minute single-request
   stall, not just slower). GPU/CPU expert split defaults to `--fit` (this build's llama.cpp
   auto-sizes it from live free VRAM — leave `-ngl`/`--n-cpu-moe` unset) rather than a hand-picked
   number. Override with `N_CPU_MOE=<N>` (switches to `-ngl 999 --n-cpu-moe N`, pinning exactly N
   layers' experts to CPU) only if you need a deterministic split instead of `--fit`'s live choice
   (REFERENCE.md "Tuning --n-cpu-moe"). Cold load reads the full quant upfront (`--load-mode none`)
   — expect it to take a while (~17 min measured for 802 GB); watch `docker logs -f kimi-k3` for
   "listening on http://".

6. **Verify** — health, models, text, vision (fork build only):
   ```bash
   bash scripts/verify.sh
   ```
   Vision debug (dumps `content`/`reasoning_content` for a solid-color probe image, same pattern as
   kimi-k26's): `python3 scripts/vision-probe.py --model kimi-k3`.
   Optional throughput check: use the **`llm-inference-benchmark`** skill — same tool and
   methodology as kimi-k26 (`bench_sweep.sh`, sustained-load sweep, saturation knees). Given the
   CPU+GPU hybrid path has no prior baseline on this hardware, start with a **reduced grid**
   (`CONC="1 4 8 16 32" PROMPTS_PER=4`) rather than the tool's default before committing to a wider
   sweep — the throughput ceiling here is unknown and could make the default grid very slow.
   Tokenizer: `MODEL_REPO=moonshotai/Kimi-K3` (step 3 already cached it). Results and baselines go
   in `llm-inference-benchmark`'s REFERENCE.md, not here — see that skill.

7. **Productionize** (optional — only if this deployment should survive as a standing service; a
   one-off eval can stop after step 6). One static **`kimi-k3.service`** driven by
   **`/etc/kimi-k3.env`** (selects `QUANT`/`BUILD_SOURCE`/`IMAGE`/`N_CPU_MOE`/`PORT`), same
   env-file pattern as kimi-k26 — plus, optionally, **`kimi-k3-interactive.service`** with
   `/etc/kimi-k3-interactive.env` (few slots + DSpark speculative decoding for single-stream latency;
   `scripts/kimi-k3-interactive.env.example`). The two units `Conflicts=` with each other because they
   share the GPUs: starting either stops the other. Install both the same way:
   ```bash
   sudo install -m755 scripts/serve_docker.sh /usr/local/bin/
   sudo mkdir -p /var/lib/kimi-k3
   sudo cp scripts/kimi-k3.env.example /etc/kimi-k3.env   # EDIT: QUANT, BUILD_SOURCE, IMAGE, HF_HOME (BARE values!)
   sudo cp scripts/kimi-k3.service /etc/systemd/system/kimi-k3.service
   sudo systemctl daemon-reload
   ```
   **This skill does not enable the unit for you** — whether it should boot-enable or stay
   on-demand (started manually when needed, e.g. to avoid permanently claiming a shared GPU pool)
   is a deployment-time decision, not a property of the skill. Boot-enabled: `sudo systemctl enable
   --now kimi-k3`. On-demand: `sudo systemctl start kimi-k3` when needed, `stop` when done — document
   the choice you made in the deploy directory's own README, not here.
   ⚠ Same warning as kimi-k26: keep `/etc/kimi-k3.env` values **bare** — systemd `EnvironmentFile`
   folds an inline `# comment` into the value.

## Key facts (don't relearn these the hard way)
- **This is not TP.** llama.cpp splits layers/tensors across GPUs (`--split-mode`, default
  `layer`) and offloads MoE experts to CPU (`--n-cpu-moe`) — there's no NCCL, no `--ipc=host`
  all-reduce dependency the way kimi-k26's SGLang/vLLM TP=8 has. `--ipc=host` here is just
  llama.cpp's own worker IPC, a much lighter requirement.
- **`--n-cpu-moe` is a knob, not a fact you look up once.** More GPUs (or more VRAM per GPU)
  dedicated to this deployment → lower `--n-cpu-moe` → more experts GPU-resident → faster. It's
  reproducible per (quant, GPU count, GPU memory) combination — re-tune if any of those change.
  See REFERENCE.md.
- **Zero CPU experts is the lever, not faster CPU experts.** Measured 2026-09-05: the hybrid's decode
  is bound by llama.cpp's sequential 8-GPU layer split plus ~30 CPU splits per token, not by DRAM
  bandwidth (458 GB/s measured; the CPU experts read ~2.4 GB/token) and not by AMX (never used for
  MoE). All-VRAM gives 2x; nothing on the CPU side does. Prefill in hybrid mode is bound by the
  per-micro-batch copy of every CPU expert to GPU0 — hence `UBATCH=4096` (REFERENCE.md "Where the time
  goes").
- **Speculative decoding pays only at low concurrency, and only with both shipped patches.** No MTP
  head in the checkpoint. The RadixArk DSpark draft converts and works once (a) the draft sits on the
  GPU holding the target's `output.weight` (`--spec-draft-device CUDA7` on an 8-GPU layer split —
  anywhere else aborts in graph reservation) and (b) the image carries `kimi-k3-rs-rollback.patch`
  (bounded recurrent-state rollback for KIMI_K3 — without it the host-side state checkpoint per draft
  step costs more than the drafts save). Measured on IQ2_XXS at 4 slots: **+23 % on free-form prompts,
  +72 % on copy-heavy ones at c1; a loss at c4** (verify batches multiply MoE expert reads). Needs
  ~9 GB free on the draft's GPU plus room for the snapshots — use a per-device `--fit-target` list.
  `ngram-mod` is ≈ neutral. Details, memory math and the debug recipe: REFERENCE.md "Speculative decoding".
- **Vision lives only in the fork.** If `BUILD_SOURCE=mainline`, don't pass `--mmproj` — the
  mainline binary has no MoonViT-3d support and will error or silently ignore it depending on
  version; `serve_docker.sh` only adds the `--mmproj` flag when `BUILD_SOURCE=fork`.
- **The GGUF repo has no HF-format tokenizer.** `unsloth/Kimi-K3-GGUF` is 171 files, all GGUF
  shards + README — nothing an `AutoTokenizer` can load. Benchmarking (or anything else that needs
  the tokenizer client-side) uses `moonshotai/Kimi-K3` instead, cached for its small non-weight
  files only (step 3).
- **Sizing gate is disk-and-memory, not just disk.** Unlike kimi-k26's `download.sh` (which only
  checks disk space, because the whole checkpoint always lands entirely in VRAM), this skill's
  gate also flags when a quant's total size exceeds combined VRAM+RAM — a hybrid deploy can *in
  principle* run at any split, but if the model doesn't fit in VRAM+RAM at all, it can't run at
  any split either.
- Both `BUILD_SOURCE` paths are **young code** (mainline K3 support: 2026-08-15; the fork:
  unmerged, actively changing) — expect build friction that kimi-k26's mature stock images never
  had. Treat REFERENCE.md's "Build gotchas" as a living section, not a fixed troubleshooting list.

## When startup crashes or hangs
See **[REFERENCE.md](REFERENCE.md)**: build flags and gotchas for both `BUILD_SOURCE` paths, the
sizing gate's exact math, `--n-cpu-moe` tuning method, tokenizer-for-benchmarking setup, and
productionization details not covered above. Two symptoms with known causes: **`CUDA error: out of
memory` in `alloc` on the first request after a successful all-VRAM load** → raise `--fit-target`
and use `-ub 2048` ("All-VRAM quants"); **a new quant that loads and talks but scores KLD ≫ 1 in the
gate** → broken sm_120 kernel for that type, don't serve it ("Quant gate").
