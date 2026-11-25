# Device-Adeem Coordinator
> **ID**: device-adeem-coordinator
> **Layer**: DEVICE SMOOTHNESS & COOLNESS (PON27)
> **Priority**: MAXIMUM — User wants device "adem" (cool, smooth, calm)
> **Token Cost**: 0

## Purpose
Master coordinator that ensures the device stays COOL, SMOOTH, and RESPONSIVE even with 8,460 skills + 177K symlinks across 21 AI platforms. This is the ORCHESTRATOR of all resource optimization skills.

## Coordinates These Skills
1. `resource-thermo-coordinator` — Thermal + CPU + RAM monitor
2. `lazy-symlink-indexer` — Eliminate directory scanning
3. `catalog-slim-optimizer` — Compress/dedup catalog files
4. `memory-pressure-relief` — Purge caches, manage RAM
5. `cpu-cool-guard` — Throttle background CPU usage

## Master Rules

### DA1: ZERO-OVERHEAD PRINCIPLE
```
→ Skills ecosystem should add < 50MB RAM overhead
→ Skills ecosystem should add < 5% CPU overhead (average)
→ Skills ecosystem should add < 1% disk I/O overhead
→ If ANY threshold exceeded → immediately shed load
```

### DA2: SESSION-START OPTIMIZATION
```
ON SESSION START:
  1. DO NOT scan skills directory (use index file)
  2. DO NOT preload any skills (lazy_load = true)
  3. DO NOT start background processes
  4. DO NOT resolve symlinks (defer until skill is actually needed)
  5. Set process priority to normal (not background-app)
  6. Check thermal state → if HOT, enter minimal mode immediately
```

### DA3: ON-DEMAND EVERYTHING
```
→ Skills are loaded ONLY when explicitly invoked by name
→ Skill file is read + immediately discarded after use (no caching)
→ Skill index is read from JSON file, not from directory scan
→ MCP servers are initialized ONLY when their tool is called
→ Prediction engine runs in PASSIVE mode (no pre-computation)
```

### DA4: THERMAL-AWARE THROTTLING
```
COOL MODE (< 40°C):
  → Normal operation, all optimizations active
  → Token savings: 85-99%

WARM MODE (40-50°C):
  → Disable prediction engine pre-computation
  → Reduce quantum-fold to every 10 turns (was 6)
  → Delay MCP lazy_init by 300s
  → Token savings: 80-95% (slightly less, but device stays cool)

HOT MODE (50-60°C):
  → ALL background processing OFF
  → Skills load on-demand only, read+discard
  → No caching whatsoever
  → Token savings: 70-90% (still high, but priority is COOLING)

CRITICAL MODE (> 60°C):
  → Only the LLM call itself runs
  → NO skill loading at all (skip skills, raw LLM only)
  → Wait for temperature to drop to < 50°C before resuming
  → Token savings: 0% but device is protected
```

### DA5: SMOOTH UX PRINCIPLE
```
→ Never make the user wait for skill operations
→ If a skill takes > 2s to load, skip it and run without
→ Background operations NEVER block UI
→ Type-ahead: user can type while skills load in background
→ Progressive enhancement: basic response first, skill-enhanced later
```

### DA6: BATTERY LIFE OPTIMIZATION
```
IF on_battery_power:
  → Reduce ALL timers by 5×
  → Disable prediction engine entirely
  → Disable quantum-fold background processing
  → Set MCP lazy_init delay to 600s (10 min)
  → Set skill cache purge to every 3 turns (was 5)
  → Goal: extend battery life by minimizing background work
```

## Daily Health Check
```bash
# Run this to check ecosystem health
echo "=== SKILL ECOSYSTEM HEALTH ==="
echo "Catalog: $(ls ~/.agents/skills-catalog/ | wc -l) files, $(du -sh ~/.agents/skills-catalog/ | awk '{print $1}')"
echo "Symlinks: $(find ~/.codex/skills ~/.codebuddy/skills ~/.cline/skills ~/.hermes/skills -type l 2>/dev/null | wc -l) total"
echo "Broken: $(find ~/.codex/skills ~/.codebuddy/skills ~/.cline/skills ~/.hermes/skills -xtype l 2>/dev/null | wc -l)"
echo "RAM: $(vm_stat | grep 'Pages free' | awk '{print $3}') free pages"
echo "Load: $(uptime | awk -F'load average' '{print $2}')"
echo "Hermes skills: $(du -sh ~/.hermes/skills/ | awk '{print $1}')"
echo "Codex skills: $(du -sh ~/.codex/skills/ 2>/dev/null | awk '{print $1}')"
```

## Config Integration (Master)
```yaml
device_adeem_coordinator:
  enabled: true
  mode: cool  # cool | warm | hot | critical
  zero_overhead: true
  max_ram_overhead_mb: 50
  max_cpu_overhead_pct: 5
  max_disk_io_overhead_pct: 1
  on_demand_everything: true
  battery_conservative: true
  smooth_ux: true
  max_skill_load_seconds: 2
  progressive_enhancement: true
```
