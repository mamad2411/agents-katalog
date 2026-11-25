---
name: mole-optimize
description: "Use Mole to optimize macOS system performance by refreshing caches, repairing configurations, and running maintenance tasks. Run this skill whenever the user mentions optimizing performance, speeding up their Mac, refreshing services, running maintenance, or using `mo optimize`. Covers dry-run mode, whitelist, diagnostics, system health checks, and database/index maintenance."
---

# Mole Optimize Skill

> **Author**: Anton Gulin · **Tool**: [opencode-skill-creator](https://github.com/antongulin/opencode-skill-creator) · **GitHub**: [@antongulin](https://github.com/antongulin) · **Registry**: [skills.sh](https://www.skills.sh/docs)

Use this skill when you need to help a user improve macOS system performance using Mole's `optimize` command.

## Overview

`mo optimize` performs system maintenance tasks: clearing caches that slow down the system, optimizing databases, repairing configs, and tuning services.

## Command Reference

### Basic Usage

```bash
mo optimize                  # Run full optimization (will prompt for sudo)
mo optimize --dry-run        # Preview what would be optimized
mo optimize --whitelist      # Manage protected optimization items
mo optimize --debug          # Show detailed operation logs
mo optimize --help           # Show help
```

### Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview optimization actions without modifying files |
| `--whitelist` | Open interactive whitelist manager for optimization items |
| `--debug` | Show detailed operation logs |
| `--help` | Show help |

## What It Does

The optimize command performs these operations:

1. **System health check** — Collects memory, disk, uptime, and system metrics
2. **Diagnostics** — Runs `health_json` generator to identify optimization opportunities
3. **Cache optimization** — Clears system and user caches that impact performance
4. **Database optimization** — Optimizes system databases and indexes
5. **Configuration repair** — Fixes damaged preference files and plists
6. **Service tuning** — Refreshes background services and daemons

## Workflow Patterns

### Pattern 1: Quick System Health + Optimization

```bash
mo optimize
```

The tool will:
1. Check system health (RAM, disk, uptime)
2. Request sudo for system-level tasks
3. Show optimization results

### Pattern 2: Preview Before Optimizing

```bash
mo optimize --dry-run
```

Shows what actions would be taken without making any changes.

### Pattern 3: Exclude Specific Items

```bash
mo optimize --whitelist
```

Opens the whitelist editor to protect specific optimization tasks from running.

### Pattern 4: Check System Health Only

Use `mo status` for a live system health dashboard. The optimize command includes a health snapshot at the start but is focused on actionable optimizations.

## Output Format

The command outputs a JSON-based diagnostics report that includes:

```json
{
  "memory_used_gb": 12.5,
  "memory_total_gb": 16,
  "disk_used_gb": 234,
  "disk_total_gb": 500,
  "disk_used_percent": 46.8,
  "uptime_days": 12.3,
  "optimizations": [
    {
      "action": "clear_dns_cache",
      "name": "Clear DNS cache",
      "description": "Flush DNS resolver cache",
      "safe": true
    }
  ]
}
```

## Safety Guidance

- System optimization requires sudo — the tool handles this interactively
- `--dry-run` is recommended before running optimizations
- The whitelist protects specific optimization tasks from running
- All optimization actions are designed to be safe (caches regenerate, configs have backups)
- The `bc` command is required for calculations — suggest `brew install bc` if missing
- System health data requires `awk`, `sysctl`, and `df` commands

## Dependencies

- `bc` — Required for numerical calculations. Install with `brew install bc`

## Exit Codes

- `0`: Success (or dry-run complete)
- `130`: Interrupted (Ctrl+C)

## Related Commands

- `mo status` — Live system health dashboard
- `mo clean` — Free up disk space (complementary)
- `mo analyze` — Explore disk usage in detail

