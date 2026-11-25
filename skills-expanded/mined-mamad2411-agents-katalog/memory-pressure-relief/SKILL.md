# Memory-Pressure Relief
> **ID**: memory-pressure-relief
> **Layer**: RAM MANAGEMENT (PON25)
> **Priority**: CRITICAL — 8GB RAM system, prevent OOM and memory bloat
> **Token Cost**: 0

## Problem
8GB RAM. CodeBuddy + Trae + Node processes already consume ~4GB. Skill ecosystem with 8,460 files + 177K symlinks adds inode cache pressure. Memory-mapped files from skill reads accumulate.

## Rules

### MP1: SKILL CACHE PURGE
```
EVERY 5 TURNS:
  → Purge all cached skill file contents from process memory
  → Keep only: current skill being used + system prompt + last 3 conversation turns
  → Force garbage collection: gc.collect() or equivalent
```

### MP2: CONTEXT WINDOW MANAGEMENT
```
IF context_size > 3500 tokens:
  → Summarize turns older than 5 (keep summary, discard raw)
  → Keep system prompt (always)
  → Keep last 3 turns (always)
  → Force context ≤ 3900 tokens (never hit 4026 limit)
```

### MP3: PROCESS MEMORY CAP
```
IF process_RSS > 2GB:
  → This AI process is using too much RAM
  → Purge ALL skill caches immediately
  → Switch to minimal mode (no background processing)
  → Set max_cached_skills = 0 (load on-demand only, read+discard)
```

### MP4: NODE PROCESS MANAGEMENT
```
→ Monitor node processes (CodeBuddy Helper, Trae Helper)
→ If total node memory > 4GB:
  → Suggest restarting the AI with fewer background services
  → Disable non-essential MCP servers temporarily
```

### MP5: SWAP PREVENTION
```
IF swap_used > 1GB:
  → CRITICAL: System is swapping to disk
  → Immediately purge ALL caches
  → Set skill_loading = OFF (no new skill loads until swap clears)
  → Set background_processing = OFF
```

## Config
```yaml
memory_pressure_relief:
  enabled: true
  max_process_ram_mb: 2048
  purge_every_n_turns: 5
  max_cached_skills: 5
  context_hard_limit: 3900
  swap_threshold_mb: 1024
  emergency_mode: false  # auto-set true when swap detected
```
