---
name: system-info
description: Probe system resources — CPU, RAM, disk, GPU/CUDA/MPS — and translate findings into experiment design recommendations. Run this at the start of any compute-intensive project.
---

# System Info

Gather a complete picture of available compute before designing or launching experiments. After collecting the data, produce a structured profile and write it to `memory/system-profile.md` in the project sandbox.

---

## When to Use

- At the start of any project involving training, fine-tuning, or large-scale data processing
- When a training run is unexpectedly slow or crashes (re-run to check resource pressure)
- Before deciding batch size, number of workers, mixed precision settings, or dataset size

---

## Step 1 — Detect OS

```bash
uname -s
```

- `Linux` → use Linux commands below
- `Darwin` → use macOS commands below
- `Windows` → use PowerShell commands below (limited support)

---

## Step 2 — CPU

**Linux:**
```bash
lscpu | grep -E "Model name|Socket|Core|Thread|MHz"
nproc
```

**macOS:**
```bash
sysctl -n machdep.cpu.brand_string
sysctl -n hw.physicalcpu hw.logicalcpu
```

Record: model name, physical cores, logical cores (threads).

---

## Step 3 — RAM

**Linux:**
```bash
free -h
```

**macOS:**
```bash
sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}'
vm_stat | grep -E "Pages free|Pages active|Pages inactive|Pages wired"
```

Record: total RAM, available RAM. On macOS, note that `vm_stat` pages are 16KB each.

---

## Step 4 — Disk

**Linux / macOS:**
```bash
df -h .
```

Run from within the project `sandbox_root` to see available space on the relevant partition.

Record: total disk, used, available on the partition where the project lives.

---

## Step 5 — GPU Detection

### Check for NVIDIA GPU (Linux / Windows WSL)

```bash
nvidia-smi --query-gpu=name,memory.total,memory.free,utilization.gpu,driver_version --format=csv,noheader
```

If `nvidia-smi` is not found, no NVIDIA GPU is available.

Also check CUDA availability via Python:
```bash
python3 -c "import torch; print('CUDA:', torch.cuda.is_available()); print('Device count:', torch.cuda.device_count()); [print(f'  GPU {i}:', torch.cuda.get_device_name(i)) for i in range(torch.cuda.device_count())]"
```

### Check for Apple Silicon MPS (macOS)

```bash
python3 -c "import torch; print('MPS available:', torch.backends.mps.is_available()); print('MPS built:', torch.backends.mps.is_built())"
```

Also check chip type:
```bash
sysctl -n machdep.cpu.brand_string   # shows "Apple M1/M2/M3/M4"
system_profiler SPHardwareDataType | grep "Chip"
```

### Fallback — CPU only

If neither CUDA nor MPS is available, record `compute: cpu-only`.

---

## Step 6 — Python and Deep Learning Environment

```bash
python3 --version
python3 -c "import torch; print('PyTorch:', torch.__version__)"
python3 -c "import torch; print('cuDNN:', torch.backends.cudnn.version())" 2>/dev/null || echo "cuDNN: not available"
```

If torch is not installed, note it — the project setup step will need to install it.

---

## Step 7 — Write System Profile

Write findings to `memory/system-profile.md` inside the project sandbox. Use this template:

```markdown
# System Profile

- **Collected**: <YYYYMMDD_HHMMSS>
- **OS**: <Linux x86_64 | macOS Darwin arm64 | ...>

## CPU
- **Model**: <e.g. Apple M3 Pro | Intel Core i9-13900K>
- **Physical cores**: <N>
- **Logical cores**: <N>

## RAM
- **Total**: <e.g. 36 GB>
- **Available**: <e.g. 28 GB>

## Disk (project partition)
- **Total**: <e.g. 1 TB>
- **Available**: <e.g. 420 GB>

## Compute
- **Type**: <NVIDIA GPU | Apple MPS | CPU only>
- **Device**: <e.g. NVIDIA A100 80GB | Apple M3 Pro (integrated) | N/A>
- **VRAM / Unified memory**: <e.g. 80 GB | 36 GB shared | N/A>
- **CUDA version**: <e.g. 12.2 | N/A>
- **MPS available**: <yes | no>

## Python Environment
- **Python**: <version>
- **PyTorch**: <version | not installed>
- **cuDNN**: <version | not available>

## Experiment Implications
<filled in during Step 8>
```

---

## Step 8 — Derive Experiment Implications

After collecting the profile, reason about what it means for the project goal. Add an `## Experiment Implications` section to `memory/system-profile.md`. Consider:

**Batch size:**
- NVIDIA GPU with ≥40GB VRAM → large batches (512+) viable
- NVIDIA GPU with <16GB VRAM or MPS → moderate batches (64–256), watch for OOM
- CPU only → small batches (8–32), training will be slow; flag this clearly

**Mixed precision:**
- NVIDIA Ampere (A100, RTX 30xx/40xx) or newer → `torch.float16` or `bfloat16` safe
- Apple MPS → `torch.float16` supported; `bfloat16` not supported on all models
- CPU → keep `float32`

**Number of dataloader workers:**
- Set to min(physical_cores - 1, 8) as a safe default

**Disk:**
- If available disk < 10 GB, warn — checkpoints and datasets may fill it
- Note available space explicitly so the user can plan

**Estimated training time:**
- If CPU only and project involves a non-trivial model, flag that training may take hours and recommend checkpointing aggressively (every N steps, not just per epoch)

Example output:
```markdown
## Experiment Implications
- **Compute**: MPS (Apple M3 Pro). Use `device = "mps"`. Mixed precision not recommended.
- **Batch size**: Start with 64. Increase if memory allows; watch `mps` backend for silent OOM.
- **Workers**: 4 (physical cores: 6, leaving 2 for system)
- **Disk**: 420 GB available — sufficient for checkpoints and shakespeare_char dataset.
- **Estimated time**: shakespeare_char on MPS ~15–30 min. CPU fallback ~2–4h.
- **Recommendation**: Checkpoint every 500 iterations given MPS instability on long runs.
```

---

## Output

| File | Description |
|---|---|
| `memory/system-profile.md` | Full system profile + experiment implications |

This file is read by other agents (executor, orchestrator) when configuring training runs. It does not need to be included in every checkpoint — write it once at project start and update it only if hardware changes.

---

*Credit: originally sourced from clawhub.ai*
