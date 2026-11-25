---
name: ml-engine
description: >-
  TPU-first ML research engine for reproducible distributed training and ablation studies. Use for
  PyTorch-XLA, JAX, TPU (v5e/v3/v2 pods), SPMD/GSPMD, FSDPv2, MoE/router, Pallas custom kernels,
  flash/splash attention, and sharded data pipelines. Triggers on: TPU, torch_xla, JAX,
  distributed, sharding, MoE, Pallas, SPMD, multi-pod, Kaggle TPU, and the /ml, /ml-train, /ml-
  debug, /ml-ablate (etc.) commands.
domain: process
composable: true
yields_to: [craft, voice]
---

# ml-engine

> [!IMPORTANT]
> This skill has reference files in the `references/` directory. You **MUST** read them at least once to understand the deep-dive content (TPU Setup, Training Loops, FSDPv2, SPMD, etc.) and call them whenever you need specific information from there.

TPU-first ML research engine. Builds reproducible distributed training pipelines for novel architecture ablations. PyTorch-XLA (torchtpu) is primary; JAX/torchax is first-class secondary. Targets v5e-8 (primary, Kaggle + GCP), v3-8 (legacy quota), v3-64 (multi-pod scaling). Uses modern `torch_xla` APIs: `torch_xla.step()`, `torch_xla.sync()`, `torch_xla.launch()`, `torch_xla.compile()`, FSDPv2, SPMD, `@assume_pure`, `scan_layers`.

---

## When to Use

- Distributed training on TPU with PyTorch-XLA or JAX
- Novel architecture components: MoE, router, custom FFN, custom LayerNorm
- Reproducible ablation studies with deterministic data pipelines
- SPMD / GSPMD sharding setup and debugging
- Attention kernel selection: Splash, Flash, SDPA on TPU
- Raw optimizer integration: `torch.optim`, `optax`, SyncFree AdamW
- `datasets` streaming with sharded loaders
- `wandb` logging on multi-host TPU runs
- Offline/online evaluation loops with checkpoint resumption
- Tensor manipulation with `einops` on TPU
- Multi-pod training: v3-32, v3-64, v4-128
- Pallas custom TPU kernels via `call_jax`
- Modern `torch_xla` APIs: `torch_xla.step()`, `torch_xla.sync()`, `torch_xla.launch()`, `torch_xla.compile()`
- FSDPv2 (GSPMD-based fully sharded data parallelism)
- `@assume_pure` for tracing optimization
- `scan` / `scan_layers` for compile-time reduction on homogeneous layers
- `torchax` — PyTorch frontend for JAX interoperability
- `torch.compile(model, backend='openxla')` — Dynamo integration
- Compilation caching via `xr.initialize_cache()`
- Eager mode via `torch_xla.experimental.eager_mode()`
- Checkpoint saving, resumption, distributed checkpointing
- Profiling training bottlenecks with XLA profiler

---

## Commands

> See `README.md` for full command documentation, parameters, and examples.

| Command | Purpose | Example |
|---------|---------|---------|
| `/ml [idea]` | **Godmode** — full research scaffold end-to-end | `/ml "sparse MoE with dynamic clamping"` |
| `/ml-train [model] [tpu] [strategy]` | Generate training script | `/ml-train moe v3-8 fsdp` |
| `/ml-mesh [tpu] [parallelism]` | Generate mesh setup | `/ml-mesh v3-64 2d-data-model` |
| `/ml-debug [issue]` | Debug XLA issues | `/ml-debug recompilation` |
| `/ml-benchmark [kernel] [seq-len]` | Benchmark attention kernel | `/ml-benchmark auto 2048` |
| `/ml-migrate [code]` | Migrate old API → modern | `/ml-migrate train.py` |
| `/ml-port [code] [mode]` | Port PyTorch → torch_xla native | `/ml-port model.py native` |
| `/ml-optimize [object] [method]` | Optimize XLA bottleneck | `/ml-optimize router pallas` |
| `/ml-plan [idea] [scope]` | Plan & template research | `/ml-plan "sparse MoE" full` |
| `/ml-ablate [var] [values]` | Run ablation matrix | `/ml-ablate top_k "1,2,4"` |
| `/ml-checkpoint [action] [path]` | Save/resume/inspect checkpoint | `/ml-checkpoint resume ./ckpt` |
| `/ml-profile [target] [steps]` | Profile training bottleneck | `/ml-profile step_fn 100` |

---

## Godmode: `/ml`

`/ml [research idea]` — full research scaffold in one command. Runs the full cycle: analyze → plan → implement → verify.

**What it produces:**
1. Research hypothesis + experiment matrix
2. Mesh setup for target TPU (auto-detected or specified)
3. Training script with correct strategy (SPMD/FSDPv2/DDP)
4. Data pipeline (streaming + sharding)
5. Attention kernel selection (Splash/Flash/SDPA)
6. wandb config + logging hooks
7. Eval loop + perplexity/metric setup
8. Reproducibility seed lock + config dict
9. Ablation matrix if research involves multiple variables
10. Pallas optimization plan if bottleneck detected

**When to use `/ml` vs individual commands:**
- `/ml` = new research idea, greenfield. Get full scaffold.
- Individual commands = targeted work on existing code. Get surgical output.

---

## Core Instructions

### 1. TPU Detection and Mesh Initialization

Detect TPU version and initialize mesh before any model or data setup. Use modern `torch_xla` APIs — never legacy `xm.xla_device()` — because the new `tpu_device()` context manager handles initialization, mesh setup, and error recovery automatically.

```python
import torch_xla
import torch_xla.core.xla_model as xm
import torch_xla.distributed.spmd as xs
from torch_xla import runtime as xr
import numpy as np

# Modern device access
device = torch_xla.device()
tpu_version = xm.get_tpu_env("TYPE", "v5litepod-8")  # v5litepod-8, v3-8, v2-8, etc.

# 1D mesh for data parallelism on v5e-8 / v3-8 / v2-8
num_devices = xr.global_runtime_device_count()  # SPMD-aware
mesh = xs.Mesh(np.arange(num_devices), (num_devices,), axis_names=("data",))
xs.set_global_mesh(mesh)
```

> See `references/tpu-setup.md` for single-host mesh, 2D sharding, and device placement.
> See `references/tpu-v5e.md` for v5e-specific setup, Kaggle integration, and best practices.
> See `references/torchtpu.md` for modern PyTorch XLA runtime (PJRT, torch.compile).
> See `references/multi-pod-training.md` for v3-64, torchrun, and distributed checkpointing.

### 2. Modern Training Loop

Use `torch_xla.step()` context manager. Replaces manual `xm.mark_step()` — because manual `mark_step()` is the #1 source of silent XLA recompilation bugs. Never use `xm.mark_step()` in new code.

```python
import torch_xla

def train(model, train_loader, optimizer, loss_fn):
    model.to('xla')
    for inputs, labels in train_loader:
        with torch_xla.step():
            inputs, labels = inputs.to('xla'), labels.to('xla')
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
    torch_xla.sync()
```

> See `references/training-loop-patterns.md` for multi-process (`torch_xla.launch`), DDP with XLA backend, compiled step functions, eager mode, and MpDeviceLoader.

### 3. SPMD Data Parallelism

Single-process multi-device training. Better throughput than DDP for most TPU workloads.

```python
import torch_xla.distributed.spmd as xs
from torch_xla import runtime as xr
import torch_xla.distributed.parallel_loader as pl

xr.use_spmd()

num_devices = xr.global_runtime_device_count()
mesh = xs.Mesh(np.arange(num_devices), (num_devices,), ('data',))
xs.set_global_mesh(mesh)

# Scale batch size — one process handles all devices
batch_size *= num_devices

train_loader = pl.MpDeviceLoader(
    train_loader,
    device,
    input_sharding=xs.ShardingSpec(mesh, ('data', None, None, None))
)
```

> See `references/spmd.md` for mesh setup, partition specs, and advanced sharding.

### 4. FSDPv2

Large model training. Requires SPMD mode and mesh with `fsdp` axis.

```python
import torch_xla.distributed.spmd as xs
from torch_xla.experimental.spmd_fully_sharded_data_parallel import SpmdFullyShardedDataParallel as FSDPv2
from torch_xla import runtime as xr
from torch_xla.distributed.fsdp.wrap import transformer_auto_wrap_policy
import functools

xr.use_spmd()
num_devices = xr.global_runtime_device_count()
mesh = xs.Mesh(np.arange(num_devices), (num_devices, 1), ('fsdp', 'model'))
xs.set_global_mesh(mesh)

auto_wrap_policy = functools.partial(
    transformer_auto_wrap_policy,
    transformer_layer_cls={DecoderLayer},
)
model = FSDPv2(model, auto_wrap_policy=auto_wrap_policy)
```

**Gradient checkpointing** (apply before FSDPv2 wrapper):

```python
from torch_xla.distributed.fsdp import checkpoint_module
model = FSDPv2(checkpoint_module(my_module), mesh)
```

> See `references/fsdp-v2.md` for full FSDPv2 setup, sharding output, and distributed checkpointing.

### 5. Dual-Framework Runtime (PT-XLA + JAX/torchax)

PT-XLA = primary. JAX = auxiliary ops (custom loss, routing, differentiable sort). `torchax` = PyTorch syntax on JAX backend.

> See `references/dual-framework.md` for DLPack zero-copy interop patterns and memory management.
> See `references/torchax.md` for torchax setup and PyTorch-on-JAX patterns.

### 6. Model Architecture Patterns

MoE routers, custom FFN (SwiGLU), RMSNorm — all with SPMD sharding annotations baked in.

> See `references/model-architecture.md` for full MoE, custom FFN, LayerNorm, router patterns.

### 7. Attention Kernel Selection

Auto-detect and select explicitly. Priority: Splash (v3+) → Flash → SDPA. Never silently fall back — because silent fallback to SDPA can mask a 2-3x throughput regression that only surfaces under production load.

> See `references/attention.md` for kernel benchmarking and fallback rules.
> See `references/pallas-custom-kernels.md` for Splash Attention via Pallas.

### 8. Data Pipeline

Stream from `datasets`, shard across TPU cores, deterministic sampling.

> See `references/data-pipeline.md` for multi-epoch streaming, XLA-Trainer patterns, and JAX pipelines.

### 9. Optimizer Compatibility

SyncFree AdamW preferred on TPU (~20% faster) — because the sync barrier in standard AdamW wastes TPU cycles waiting for all replicas. Raw instances only -- no wrapper magic.

> See `references/optimizers.md` for LR schedules and custom state handling.

### 10. Compilation Optimization

Three tools: compilation cache, `@assume_pure`, `scan_layers`.

> See `references/tracing-optimization.md` for `@assume_pure`, `scan_layers`, benchmarks, and AOTAutograd compatibility.
> See `references/compilation-cache.md` for `xr.initialize_cache()` and shared mounts.

### 11. `torch.compile` with OpenXLA

`torch.compile(model, backend='openxla')` for inference (2-18x speedup) and training steps (experimental).

> See `references/torchtpu.md` for Dynamo integration and performance benchmarks.

### 12. Eager Mode

Debugging only — because eager mode disables XLA graph fusion, dropping throughput 10-50x. Operations execute immediately -- no lazy graph. Combine with `@assume_pure` for selective compilation.

### 13. wandb Logging on TPU

Master process only. Aggregate before logging.

> See `references/wandb-logging.md` for initialization, metric aggregation, checkpoint artifacts, multi-host sync, and JAX logging patterns.

### 14. Evaluation Loops

Sharded inference, aggregate across devices.

> See `references/evaluation.md` for online/offline eval, perplexity calculation, accuracy, JAX eval, checkpoint resumption, and sharded inference.

### 15. Reproducible Ablations

Lock all RNGs. Version custom modules with string IDs. Log full config + git hash.

> See `references/ablations.md` for seed locking, config dicts, config hashing, module versioning, deterministic data, and environment capture.

### 16. Checkpointing

> See `references/fsdp-v2.md` for save/resume patterns and distributed checkpointing with FSDPv2.

### 17. Tensor Manipulation with einops

Use `einops` for all reshaping and einsum on TPU. XLA fuses better than manual `view` + `permute`.

> See `references/einops.md` for rearrange, einsum, reduce, JAX compatibility, and TPU-specific patterns.

---

## Boundaries

- Does NOT handle hyperparameter search (use Optuna / Ray Tune separately)
- Does NOT optimize inference serving (training focus only)
- Does NOT design model architectures from scratch (provides patterns for common novel components)
- Does NOT replace framework documentation (provides TPU-specific integration patterns)

## Self-Verification

Before declaring a training setup complete, verify:
- TPU version detected and mesh shape matches model sharding
- No XLA recompilation warnings in logs
- Loss is decreasing after 100 steps
- Memory usage is within TPU HBM limits
- All `xm.mark_step()` calls replaced with `tpu_step()` context manager
- Checkpoint save/load tested at least once

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: [craft, voice]
```

ml-engine owns **process** (training workflow, distributed setup, evaluation loops) and **content** (ML substance: tensor ops, sharding, attention kernels, optimizer state).

### When ml-engine Leads

- Any distributed training setup on TPU
- Model architecture component implementation (MoE, router, FFN, LN)
- Data pipeline with `datasets` streaming and sharding
- Optimizer integration and custom state handling
- wandb logging aggregation on multi-host TPU
- Evaluation loop construction and metric computation
- Reproducibility guardrails for ablation studies
- FSDPv2 setup and sharding configuration
- Tracing optimization (`@assume_pure`, `scan_layers`, compilation caching)
- `torch.compile` with OpenXLA backend integration
- SPMD mesh and partition spec configuration
- Checkpoint save, resume, and distributed checkpoint patterns
- Training profiling and bottleneck identification

### When ml-engine Defers

| Other Skill's Domain | What ml-engine Does |
|---------------------|------------------------|
| **Voice** (e.g. blogger) | Preserves factual content about training setup; voice skill rewrites prose tone. ml-engine owns all code, config, and metric content. |
| **Craft** (e.g. painter) | Preserves training code and data pipeline; craft skill adds UI/visualization for dashboards, plots, or reports. ml-engine provides raw metrics. |
| **Density** (e.g. caveman, compress) | SKILL.md and reference files are source files — not compressible. Conversational explanations about ml-engine can be compressed. |

### Layered Composition Rules

1. **Process + Content**: ml-engine is both process and content. When another content skill provides domain knowledge (e.g., NLP research findings), ml-engine shapes it into training code and config.

2. **Process + Craft**: ml-engine generates training scripts and metric logs. Craft skill consumes metrics to build visual dashboards. Boundary: ml-engine stops at raw CSV/tensor outputs; craft starts at visualization.

3. **Process + Voice**: ml-engine writes technical config and code. Voice skill rewrites user-facing explanations. Boundary: code blocks and config dicts are voice-agnostic.

### Pipeline Behavior

- **Upstream** (receives output from another skill): If a research skill provides novel architecture ideas, ml-engine implements them as sharded modules with TPU-compatible attention.
- **Downstream** (output feeds into another skill): ml-engine outputs training scripts, config files, and metric logs. Downstream skills (craft, voice) consume these for reporting or visualization.

### Conflict Signal

If a voice or craft skill attempts to modify code structure or sharding logic:

> `⚠️ Process conflict: voice/craft skill is modifying training loop structure or sharding annotations. Code structure preserved; prose/visual style applied to surrounding explanations only.`
