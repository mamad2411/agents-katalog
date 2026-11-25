# CPU-Cool Guard
> **ID**: cpu-cool-guard
> **Layer**: CPU THERMAL MANAGEMENT (PON26)
> **Priority**: HIGH — Keep device cool and smooth (adem)
> **Token Cost**: 0

## Problem
Background skill operations (scanning, indexing, prefetching, prediction engine pre-computation) consume CPU cycles that heat up the device. On 8GB/low-core systems, this causes thermal throttling and fan noise.

## Rules

### CG1: BACKGROUND OPERATION BUDGET
```
→ Total CPU budget for ALL background skill operations: 15% (1 core max)
→ If current CPU usage > 60%, background budget = 5%
→ If current CPU usage > 80%, background budget = 0% (ALL STOP)
→ Background operations include: skill scanning, index rebuild, prediction pre-compute, cache warm
```

### CG2: NICE PRIORITY
```
→ ALL skill background processes run at nice priority 19 (lowest)
→ Never compete with user-facing AI/LLM calls
→ OS scheduler gives them CPU only when system is idle
```

### CG3: BATCH & DELAY
```
→ Never process more than 50 skills in one batch
→ Between batches: sleep 2 seconds (let CPU cool)
→ If temperature rises during batch: pause 10s
→ Maximum 3 batches per minute
```

### CG4: FAN NOISE REDUCTION
```
→ Detect fan speed via `smc -k F0Ac -r` (if available)
→ If fan > 4000 RPM:
  → Pause ALL background processing for 60s
  → Resume only when fan < 3000 RPM
→ Alternative: monitor CPU temp via powermetrics
```

### CG5: THERMAL PROFILE
```
COOL (< 40°C): Full operation, all background tasks allowed
WARM (40-50°C): Reduce background to 50%, delay batches 5s
HOT (50-60°C): Background OFF, emergency mode, only user-facing calls
CRITICAL (> 60°C): EVERYTHING OFF except the LLM call itself
```

## Implementation (macOS)
```bash
# Quick CPU temp check (no sudo needed with osx-cpu-temp if installed)
# Fallback: use load average as proxy
uptime | awk -F'load average' '{print $2}'
# load > 2.0 on 4-core = thermal risk
```

## Config
```yaml
cpu_cool_guard:
  enabled: true
  background_cpu_budget_pct: 15
  nice_priority: 19
  batch_size: 50
  batch_delay_seconds: 2
  thermal_pause_seconds: 10
  max_batches_per_minute: 3
  fan_threshold_rpm: 4000
  profiles:
    cool: 40
    warm: 50
    hot: 60
```
