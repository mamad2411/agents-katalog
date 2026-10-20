# /anima-train — Auto Pre-Flight + GPU Training Launch

Use this skill when: you need to prepare and launch training on the GPU server. It handles everything: venv check, data verification, batch size finder, multi-GPU config, and training launch with nohup.

## What This Skill Does

1. **Pre-flight check** — venv, PYTHONPATH, data paths, model weights
2. **GPU batch finder** — auto-detect optimal batch size for 70% VRAM on L4/A6000
3. **Multi-GPU config** — set up DDP/FSDP for all available GPUs
4. **Training launch** — nohup + disown (survives Claude crash)
5. **Monitoring setup** — tail log, GPU watch

## Instructions

### Step 1: Environment Check

```bash
# Check venv exists and is healthy
ls .venv/bin/python || (echo "MISSING VENV — creating..." && uv venv .venv --python python3.11 && uv sync)
source .venv/bin/activate
unset PYTHONPATH

# Verify torch + CUDA
python -c "import torch; print(f'torch={torch.__version__}, CUDA={torch.cuda.is_available()}, GPUs={torch.cuda.device_count()}')"
```

### Step 2: Data Verification

Read `ASSETS.md` and verify every READY/DONE asset exists on disk:

```bash
python scripts/check_assets.py 2>/dev/null || echo "No check_assets.py — manual verify needed"
```

For each model/dataset path in ASSETS.md:
- Check `ls -d <path>` exists
- Check it's not empty (`du -sh <path>`)
- If MISSING: report and ask user whether to proceed or download first

### Step 3: Find Training Config

Look for training config in this priority order:
1. `configs/paper.toml` — paper-exact hyperparameters
2. `configs/training_cuda.yaml` — CUDA training config
3. `configs/train.yaml` — generic training config
4. `configs/default.toml` — fallback

Read the config. Extract:
- batch_size
- learning_rate
- epochs
- model architecture
- data paths

### Step 4: GPU Batch Size Finder

Target: **70% VRAM utilization** (leaves headroom for gradient spikes)

```python
import torch, gc

def find_optimal_batch(model_fn, input_fn, target_util=0.70, device='cuda:0'):
    torch.cuda.empty_cache()
    gc.collect()

    total = torch.cuda.get_device_properties(device).total_mem
    target_bytes = total * target_util

    # Measure model footprint
    model = model_fn().to(device)
    torch.cuda.synchronize()
    model_mem = torch.cuda.memory_allocated(device)

    available = target_bytes - model_mem

    # Binary search for batch size
    lo, hi = 1, 512
    best = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        try:
            torch.cuda.empty_cache()
            batch = input_fn(mid).to(device)
            with torch.cuda.amp.autocast():
                out = model(batch)
                if hasattr(out, 'loss'):
                    out.loss.backward()
                elif isinstance(out, dict) and 'loss' in out:
                    out['loss'].backward()
            torch.cuda.synchronize()
            used = torch.cuda.memory_allocated(device)
            if used <= target_bytes:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
            del batch, out
            model.zero_grad()
        except RuntimeError:  # OOM
            hi = mid - 1
            torch.cuda.empty_cache()

    del model
    torch.cuda.empty_cache()

    vram_gb = total / 1e9
    print(f"[BATCH] GPU: {torch.cuda.get_device_name(device)}")
    print(f"[BATCH] VRAM: {vram_gb:.1f} GB")
    print(f"[BATCH] Optimal batch_size={best} (target {target_util*100:.0f}% of {vram_gb:.1f}GB)")
    return best
```

If `scripts/find_batch_size.py` exists, run it. Otherwise use the config batch_size but verify it doesn't OOM with a 2-step smoke test.

### Step 5: Multi-GPU Setup

Check available GPUs:
```bash
nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader
```

For N GPUs:
- If training script supports `--multi-gpu` or `--gpus`: use it
- If using PyTorch DDP: `torchrun --nproc_per_node=N --master_port=29500`
- If using DeepSpeed: `deepspeed --num_gpus=N`
- If single-GPU only: `CUDA_VISIBLE_DEVICES=0`

Set GPU IDs based on what's FREE (memory.used < 100MB).

### Step 6: Training Launch

ALWAYS use nohup + disown to survive Claude crash:

```bash
# Single GPU
PYTHONPATH="" CUDA_VISIBLE_DEVICES=0 \
  nohup .venv/bin/python -m anima_<module>.train \
    --config configs/paper.toml \
    2>&1 | tee /mnt/artifacts-datai/logs/project_<module>/train.log &
disown

# Multi-GPU (DDP)
PYTHONPATH="" \
  nohup torchrun --nproc_per_node=8 --master_port=29500 \
    -m anima_<module>.train \
    --config configs/paper.toml \
    2>&1 | tee /mnt/artifacts-datai/logs/project_<module>/train.log &
disown
```

Create log directory first:
```bash
mkdir -p /mnt/artifacts-datai/logs/project_<module>/
```

### Step 7: Verify Training Started

```bash
# Check process is running
ps aux | grep "anima_<module>" | grep -v grep

# Check GPU utilization
nvidia-smi

# Check log is growing
tail -5 /mnt/artifacts-datai/logs/project_<module>/train.log

# Watch live (Ctrl+C to stop watching, training continues)
tail -f /mnt/artifacts-datai/logs/project_<module>/train.log
```

### Step 8: Report

Output a summary:
```
TRAINING LAUNCHED: project_<module>
Config: configs/paper.toml
Batch size: <N> (auto-detected / from config)
GPUs: <N>x <GPU_NAME> (<VRAM>GB each)
Estimated VRAM: <N>% per GPU
Log: /mnt/artifacts-datai/logs/project_<module>/train.log
PID: <PID>
Monitor: tail -f /mnt/artifacts-datai/logs/project_<module>/train.log
Kill: kill <PID>
```

## Key Rules

- NEVER train without `unset PYTHONPATH` first
- NEVER guess batch size — always verify with smoke test or batch finder
- ALWAYS use nohup + disown (training MUST survive Claude disconnects)
- ALWAYS log to `/mnt/artifacts-datai/logs/project_<module>/`
- Target 70% VRAM — NOT higher (gradient accumulation spikes)
- Check ASSETS.md BEFORE training — don't train on missing data
- If config has `batch_size: "auto"`, run the batch finder
- If training fails in first 60 seconds, check the error and fix — don't retry blindly

## Server Context

```
SSH: ssh datai_srv7_development
Models: /mnt/forge-data/models/
Datasets: /mnt/forge-data/datasets/
Repos: /mnt/forge-data/repos/
Logs: /mnt/artifacts-datai/logs/
Exports: /mnt/artifacts-datai/exports/
GPUs: 8x L4 (23GB each) or 8x A6000 (48GB each)
Python: 3.11 (use python3.11 for venv creation)
```
