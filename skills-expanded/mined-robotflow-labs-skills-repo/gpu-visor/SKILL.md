# /gpu-visor — Instant GPU & Training Status

**Purpose:** Get full GPU, training, disk, and agent status in <2 seconds. Replaces all sleep-based monitoring.

**RULE:** Every agent MUST use this instead of `sleep 300 && tail`. No exceptions.

---

## Usage

```bash
# Full status (default)
bash /mnt/forge-data/scripts/gpu-visor.sh

# Filter by module
bash /mnt/forge-data/scripts/gpu-visor.sh --module frigg

# Alerts only (fastest)
bash /mnt/forge-data/scripts/gpu-visor.sh --alerts-only
```

## What It Shows

1. **GPU Status** — utilization %, VRAM used/total, temperature, which module owns each GPU
2. **Training Logs** — last line of each active module's log (last 24h only)
3. **Disk** — usage across artifacts, forge-data, root
4. **Active Agents** — tmux sessions
5. **Alerts** — stale logs (>10min), disk >90%, VRAM >85%

## Output Example

```
=== GPU VISOR — 2026-03-31 10:16:50 ===

GPU  |  Util |    VRAM Used/Total |  Temp | Module
-----+-------+--------------------+-------+---------------------------
  0   |    0% |      0 /  23034 MB |   72 C | IDLE
  4   |  100% |  15097 /  23034 MB |   74 C | project_frigg
  5   |  100% |  15095 /  23034 MB |   77 C | project_frigg

=== RECENT TRAINING (last 24h) ===
  project_frigg:     [Batch 80/334] loss=0.2867 lr=0.000100 (19s ago)

=== DISK ===
  /mnt/artifacts-datai      592G used, 809G free (43%)

=== ALERTS ===
  All clear
```

## When To Use

| Situation | Command |
|-----------|---------|
| Check if my training is running | `gpu-visor.sh --module MY_MODULE` |
| After launching nohup training | `gpu-visor.sh` (verify GPU picked up) |
| Periodic monitoring (every 2min) | `sleep 120 && gpu-visor.sh` |
| Something seems wrong | `gpu-visor.sh --alerts-only` |
| Before starting a new training | `gpu-visor.sh` (check which GPUs are free) |

## NEVER Do This

```bash
# BAD — blind 5-minute sleep, no visibility
sleep 300 && tail -5 train.log
sleep 400 && nvidia-smi
nohup training && sleep 600
```

## Instead Do This

```bash
# GOOD — instant, full picture
bash /mnt/forge-data/scripts/gpu-visor.sh

# GOOD — check your module specifically
bash /mnt/forge-data/scripts/gpu-visor.sh --module cornucopia

# GOOD — short sleep then visor (for monitoring loops)
for i in $(seq 1 10); do
  sleep 120
  bash /mnt/forge-data/scripts/gpu-visor.sh --module MY_MODULE
done
```

## Location

Script: `/mnt/forge-data/scripts/gpu-visor.sh`
Symlinked to all modules at: `.claude/rules/gpu-visor.sh`
