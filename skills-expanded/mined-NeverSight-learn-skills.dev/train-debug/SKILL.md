---
name: train-debug
description: Diagnose and fix ML training issues including loss not converging, OOM errors, NaN gradients, multi-GPU failures, and performance bottlenecks. Trigger when user reports training problems, errors, or says "训练报错", "loss不降", "OOM", "训练失败", "debug training".
---

# Training Debugger

Systematic diagnosis and resolution of ML training issues.

## When Triggered

- Training crashes or produces errors
- Loss is not converging or diverging
- OOM (Out of Memory) errors
- NaN/Inf in loss or gradients
- Multi-GPU synchronization issues
- Training is unexpectedly slow
- Evaluation metrics not improving

## Diagnosis Framework

### Step 1: Triage (30 seconds)

Quickly classify the issue:

| 症状 | 类别 | 紧急度 |
|------|------|--------|
| 进程崩溃/error | CRASH | 高 |
| Loss = NaN/Inf | DIVERGE | 高 |
| GPU OOM | MEMORY | 高 |
| Loss 不下降 | PLATEAU | 中 |
| 训练极慢 | PERF | 中 |
| Eval指标差 | QUALITY | 低 |

### Step 2: Category-Specific Diagnosis

#### CRASH: 进程崩溃

```bash
# 1. Check the error message
tail -50 <log_file> | grep -B5 -A10 "Error\|Exception\|Traceback\|CUDA error"

# 2. Check GPU state
nvidia-smi

# 3. Check if it's a multi-GPU issue
# DDP rank mismatch, NCCL timeout, etc.
```

**Common fixes:**
- CUDA OOM → reduce batch_size, enable gradient_checkpointing
- NCCL timeout → increase timeout, check network
- PyArrow incompatibility → use custom Dataset class instead of HF datasets
- Version mismatch → check torch/transformers/peft versions

#### DIVERGE: Loss NaN/Inf

```python
# Check gradient norms
for name, param in model.named_parameters():
    if param.grad is not None:
        grad_norm = param.grad.norm()
        if torch.isnan(grad_norm) or grad_norm > 100:
            print(f"⚠️ {name}: grad_norm={grad_norm}")
```

**Diagnosis tree:**
1. Is learning rate too high? → reduce by 10x
2. Is there a data issue? (NaN in inputs) → check data pipeline
3. Mixed precision overflow? → use loss scaling or disable fp16
4. Gradient explosion? → enable gradient clipping (max_norm=1.0)

#### MEMORY: OOM

**Diagnosis:**
```bash
# Peak memory per GPU
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

**Resolution priority (try in order):**
1. Reduce batch_size (simplest)
2. Enable gradient_checkpointing=True
3. Enable mixed precision (fp16/bf16)
4. Reduce max_seq_length or image resolution
5. Use gradient accumulation (maintain effective batch size)
6. Enable DeepSpeed ZeRO-2 or ZeRO-3
7. Use LoRA/PEFT to reduce trainable parameters

#### PLATEAU: Loss 不下降

**Checklist:**
1. **Data loading**: Is data actually being loaded? (check dataloader iteration)
2. **Learning rate**: Is LR too small? Check warmup schedule
3. **Frozen parameters**: Are the right layers unfrozen?
4. **Label leakage**: Is the model seeing answers in input?
5. **Batch size too large**: Effective batch = per_gpu × num_gpu × grad_accum
6. **Overfitting prevention**: Is augmentation too aggressive?

**Quick test:**
```python
# Overfit on 1 batch to verify model can learn
trainer.train(max_steps=100, overfit_batches=1)
# If loss drops → data/LR issue
# If loss doesn't drop → model/architecture issue
```

#### PERF: 训练极慢

**Diagnosis:**
```bash
# Check GPU utilization pattern
watch -n 1 nvidia-smi  # Look for 0% utilization gaps

# Check data loading
# If GPU util oscillates between 0% and 100% → data loading bottleneck
```

**Fixes:**
1. Increase num_workers in DataLoader
2. Enable pin_memory=True
3. Pre-process data to avoid on-the-fly transforms
4. Use SDPA attention instead of manual attention
5. Enable torch.compile() for PyTorch 2.0+
6. Check disk I/O (data on SSD vs HDD)

### Step 3: Multi-GPU Specific Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| DDP hang | Training freezes | Check all GPUs reachable, increase NCCL_TIMEOUT |
| Uneven memory | One GPU OOM, others fine | Check model parallelism config, gradient bucket size |
| Slow sync | Training slower with more GPUs | Check inter-GPU bandwidth, reduce sync frequency |
| Loss mismatch | Loss differs across ranks | Ensure same random seed, check data sharding |

### Step 4: Fix and Verify

After applying fix:
1. Run for 50-100 steps to verify
2. Compare loss curve before/after
3. Check GPU utilization is healthy
4. Monitor for 10 minutes before declaring fixed

### Step 5: Report

```markdown
## 训练诊断报告

### 问题描述
[What user reported]

### 诊断结果
- **类别**: [CRASH/DIVERGE/MEMORY/PLATEAU/PERF]
- **根因**: [Root cause identified]
- **证据**: [Log snippets, GPU stats, etc.]

### 修复方案
1. [Applied fix with specific code changes]

### 验证结果
- Loss: X.XX → X.XX (after fix, 100 steps)
- GPU utilization: XX% → XX%
```

## Key Rules

1. **Don't guess, diagnose** - always check logs and GPU state first
2. **Minimal changes** - fix one thing at a time to identify root cause
3. **Backup before fixing** - save current checkpoint before making changes
4. **Report in Chinese** - with English error messages and technical terms
5. **Verify the fix** - always run a short test after applying the fix
