# Resource-Thermo Coordinator
> **ID**: resource-thermo-coordinator
> **Layer**: RESOURCE THERMAL MANAGEMENT (PON22)
> **Priority**: CRITICAL — Prevent device overheating, memory bloat, CPU spikes from skill ecosystem
> **Token Cost**: 0 (runs locally, no LLM call)

## Purpose
Monitor and coordinate CPU temperature, RAM usage, and disk I/O across the 21-platform skill ecosystem. Automatically throttle or shed load when device gets warm or memory pressure rises.

## Triggers
- Device temperature > 45°C
- RAM usage > 80% (6.4GB on 8GB system)
- CPU sustained > 70% for >30s
- Disk I/O burst > 50MB/s sustained

## Rules

### R1: THERMAL THROTTLE
```
IF cpu_temp > 50°C:
  → Pause all background skill scanning
  → Delay lazy_load timer ×3 (180s → 540s)
  → Disable MCP lazy_init temporarily
  → Set skill_concurrency = 1 (was 4)
ELIF cpu_temp > 45°C:
  → Reduce skill_concurrency to 2
  → Delay lazy_load timer ×2
```

### R2: MEMORY PRESSURE RELIEF
```
IF free_ram < 10% (< 800MB on 8GB):
  → Purge ALL cached skill contents from memory
  → Force garbage collection
  → Keep only active skill + system prompt in RAM
  → Set max_cached_skills = 3
ELIF free_ram < 20% (< 1.6GB):
  → Purge skills not used in last 5 turns
  → Set max_cached_skills = 10
```

### R3: CPU SPIKE GUARD
```
IF cpu_usage > 70% sustained 30s:
  → Kill background indexing processes
  → Switch to on-demand skill loading (no preloading)
  → Set skill_load_batch_size = 1
```

### R4: DISK I/O THROTTLE
```
IF disk_io > 50MB/s sustained:
  → Disable catalog directory scanning
  → Use pre-built index file instead of readdir()
  → Batch symlink resolution to every 5 minutes
```

### R5: BATTERY AWARENESS
```
IF on_battery:
  → Reduce skill scanning frequency to every 300s (was 60s)
  → Disable quantum-fold background processing
  → Set prediction_engine to passive mode (no pre-computation)
```

## Execution Contract
1. **Session Start**: Read `/tmp/.resource_state` (if exists) for current thermal/CPU/RAM baseline
2. **Every Turn**: Quick-check `sysctl` + `vm_stat` + `ps` (cost: 0 tokens, ~5ms)
3. **If threshold exceeded**: Apply throttle rules immediately BEFORE any skill invocation
4. **Recovery**: When metrics return to normal, gradually restore concurrency over 60s ramp

## Config Integration
```yaml
resource_thermo:
  enabled: true
  cpu_threshold: 70
  ram_threshold_pct: 80
  temp_threshold: 45
  battery_mode: conservative
  throttle_multiplier: 3
  recovery_ramp_seconds: 60
```

## Safety
- NEVER block user-facing LLM calls (always allow the main prompt)
- NEVER kill the active AI process
- Only throttle BACKGROUND/optional skill operations
