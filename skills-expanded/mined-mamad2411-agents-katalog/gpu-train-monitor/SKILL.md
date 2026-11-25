---
name: gpu-train-monitor
description: Monitor multi-GPU training jobs, check GPU utilization, parse training logs, track loss curves, and provide real-time status reports. Trigger when user asks about training progress, GPU status, loss monitoring, or says "现在怎么样了", "训练进度", "GPU状态", "check training".
---

# GPU Training Monitor

Monitor and analyze multi-GPU training jobs on the current server.

## When Triggered

Run this skill whenever the user asks about:
- Training progress or status ("现在怎么样了", "训练到哪了")
- GPU utilization or memory ("GPU占用", "显存")
- Loss curves or training metrics
- Log file analysis
- WandB run status

## Execution Steps

### Step 1: GPU Status Snapshot

```bash
# Always start with GPU overview
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits
```

Report in this format:
```
| GPU | 利用率 | 显存 (已用/总量) | 温度 |
|-----|--------|-----------------|------|
| 0   | 95%    | 42.1/48.0 GB    | 72°C |
```

### Step 2: Training Process Detection

```bash
# Find active training processes
ps aux | grep -E 'python.*train|accelerate|torchrun|deepspeed' | grep -v grep
```

For each detected process:
- Identify the training script and config
- Find the associated log file (check nohup.out, logs/, wandb/)
- Determine GPU assignment (CUDA_VISIBLE_DEVICES)

### Step 3: Log Analysis

Parse the most recent training log to extract:

1. **Current progress**: epoch/step, estimated time remaining
2. **Loss trend**: last 10-20 reported loss values, direction (decreasing/stable/diverging)
3. **Learning rate**: current LR and schedule
4. **Throughput**: samples/sec or steps/sec
5. **Errors/Warnings**: any OOM, NaN, or other issues

```bash
# Tail recent log entries
tail -100 <log_file> | grep -E 'loss|step|epoch|lr|error|warning|eval'
```

### Step 4: WandB Integration (if applicable)

If WandB is configured:
- Check for active WandB runs
- Report the WandB dashboard URL
- Summarize recent logged metrics

### Step 5: Status Report

Output a concise Chinese status report:

```markdown
## 训练状态报告 (YYYY-MM-DD HH:MM)

### GPU 状态
[GPU table from Step 1]

### 训练进度
- **任务**: [script name / experiment name]
- **当前**: Step X / Total Y (XX%)
- **Loss**: X.XXX (趋势: ↓下降中)
- **速度**: X.X steps/sec
- **预计完成**: ~HH:MM

### 问题检测
- [Any warnings, OOM risks, or anomalies]

### 建议
- [Actionable suggestions: increase batch size, check learning rate, etc.]
```

## Key Rules

1. **Always check GPU first** - even if the user asks about logs, start with GPU status
2. **Detect stalled training** - if loss hasn't changed for >100 steps, flag it
3. **Memory efficiency** - if GPU memory utilization < 50%, suggest increasing batch size
4. **Multi-job awareness** - if multiple training jobs exist, report all of them
5. **Chinese output** - report in Chinese, keep technical terms in English
6. **Proactive suggestions** - don't just report, suggest optimizations

## Common Patterns

### Loss Not Decreasing
Check: learning rate too low, data loading issues, gradient accumulation config, model frozen layers

### OOM Risk
Check: batch size, gradient checkpointing, mixed precision, image resolution settings

### Slow Training
Check: data loading bottleneck (num_workers), GPU utilization gaps, unnecessary logging frequency
