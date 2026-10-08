# Resource-Thermal Guard
> **ID**: resource-thermal-guard
> **Layer**: DEVICE PROTECTION (PON36)
> **Priority**: CRITICAL — Prevent overheating, RAM exhaustion, CPU spikes from 8789 skills
> **Token Cost**: 0 (pure local monitoring)

## Problem
8,789 skills across 21 platforms = 184K+ symlinks. On 8GB RAM MacBook, this causes:
- Spotlight indexing CPU spikes (unless .metadata_never_index)
- readdir() overhead when AI scans skill folders
- Memory-mapped file accumulation from skill reads
- Background process bloat from MCP servers + skill scanners

## 7 Guard Rules

### G1: SPOTLIGHT DISABLED
```
→ .metadata_never_index exists in ALL skill directories
→ Verify every session start: if missing, create immediately
→ Prevents mds_stores process from scanning 8789 files × 21 dirs
→ Saves ~200MB RAM + 15% CPU during indexing
```

### G2: DIRECTORY SCAN PROHIBITED
```
→ AI must NEVER readdir() on skill folders directly
→ Use .skill_index.json (pre-built JSON index, 1 file read)
→ Only rebuild index if stale >24h, at nice 19
→ Eliminates 184K symlink resolution overhead
```

### G3: MEMORY CAPS
```
→ Max process RSS: 2GB (hard kill if exceeded)
→ Max cached skills in memory: 5 (purge oldest)
→ Purge ALL caches every 5 turns
→ Force gc.collect() after purge
→ If free RAM < 800MB: emergency purge + minimal mode
→ If swap > 1GB: ALL background OFF, skill loading OFF
```

### G4: CPU BUDGET
```
→ Background CPU budget: 15% max (1 core)
→ All background procs: nice 19 (lowest priority)
→ Batch operations: 50 items max, 2s delay between batches
→ Max 3 batches per minute
→ If CPU > 70% sustained 30s: background OFF
→ If load average > 2.0: skip all background ops
```

### G5: THERMAL PROFILES
```
COOL (< 40°C): Full operation, all optimizations active
WARM (40-50°C): 50% background, delay timers ×2
HOT (50-60°C): Background OFF, emergency minimal mode
CRITICAL (> 60°C): LLM-only, NO skills loaded at all
→ Check every turn (5ms, 0 tokens)
→ Recovery: gradual ramp over 60s when temp drops
```

### G6: BATTERY MODE
```
IF on_battery_power:
→ 5× slower timers (60s → 300s)
→ Prediction engine OFF (no pre-computation)
→ Quantum-fold background OFF
→ MCP lazy_init delay: 600s (10 min)
→ Cache purge every 3 turns (was 5)
→ Goal: maximize battery life
```

### G7: ZERO-OVERHEAD PRINCIPLE
```
Skill ecosystem overhead limits:
→ RAM: < 50MB total overhead
→ CPU: < 5% average
→ Disk I/O: < 1% average
→ Background CPU: < 15% (1 core max)
→ Process count: 0 new processes (all inline)
→ If ANY limit exceeded: immediately shed load
```

## Implementation
```bash
# Quick resource check (0 tokens, ~5ms)
load=$(uptime | awk -F'load average' '{print $2}' | awk -F',' '{print $1}' | tr -d ' ')
free_mb=$(vm_stat | awk '/Pages free/ {print int($3)*16/1024}')
echo "Load: $load | Free: ${free_mb}MB"
# If load > 2.0 or free < 800: throttle
```

## Config
```yaml
resource_thermal_guard:
  enabled: true
  spotlight_disabled: true
  directory_scan: false  # use index
  max_process_rss_mb: 2048
  max_cached_skills: 5
  purge_every_n_turns: 5
  emergency_ram_mb: 800
  emergency_swap_mb: 1024
  background_cpu_pct: 15
  nice_priority: 19
  batch_size: 50
  batch_delay_s: 2
  max_batches_per_min: 3
  thermal_profiles:
    cool: 40
    warm: 50
    hot: 60
  battery_conservative: true
  zero_overhead: true
```
