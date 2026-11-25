---
name: mole-status
description: "Use Mole to monitor macOS system health with live metrics including RAM usage, disk usage, uptime, and overall system status. Run this skill whenever the user mentions checking system health, viewing status, monitoring performance, or using `mo status`. Covers live dashboard interpretation, health metrics, and related monitoring commands."
---

# Mole Status Skill

> **Author**: Anton Gulin · **Tool**: [opencode-skill-creator](https://github.com/antongulin/opencode-skill-creator) · **GitHub**: [@antongulin](https://github.com/antongulin) · **Registry**: [skills.sh](https://www.skills.sh/docs)

Use this skill when you need to help a user check macOS system health using Mole's `status` command.

## Overview

`mo status` launches a live system health dashboard (built with Bubble Tea) that shows real-time system metrics in an interactive TUI.

## Command Reference

### Basic Usage

```bash
mo status          # Launch live system health dashboard
mo status --help   # Show help
```

### Flags

| Flag | Description |
|------|-------------|
| `--help` | Show help |

The status command has no other flags — it's designed as a live monitoring tool.

## What It Shows

The status dashboard displays these real-time metrics:

- **Memory usage** — RAM used vs total (GB)
- **Disk usage** — Disk used vs total (GB)
- **Disk usage percentage** — Percentage of disk space used
- **Uptime** — System uptime in days
- **Additional system info** — macOS version, architecture, kernel, SIP status, free disk space (shown by `mo --version` and `mo help`)

## Workflow Patterns

### Pattern 1: Quick Health Check

```bash
mo status
```

Opens the TUI dashboard. The user can inspect metrics and press `q` to quit.

### Pattern 2: Free Disk Space Quick Check

Before cleanup operations, check free space:

```bash
mo status
```

Or use:

```bash
mo --version
```

Which shows a concise system summary including free space.

### Pattern 3: System Information

For a non-interactive system summary:

```bash
mo --version
```

Outputs:
- Mole version
- macOS version
- Architecture
- Kernel
- SIP status
- Disk free space
- Install method (Homebrew/Manual)
- Shell
- Channel (stable/nightly)

## Metrics Interpretation

- **Memory (RAM)**: Higher used GB may indicate memory pressure. If > 80% of total, suggest closing unused apps.
- **Disk**: If > 85% used, suggest `mo clean --dry-run` to preview cleanup potential.
- **Uptime**: Long uptime (> 30 days) may benefit from a restart to clear temporary system caches.
- **SIP (System Integrity Protection)**: Disabled SIP can indicate deeper system access but reduces security.

## Safety Guidance

- The status command is read-only — it never modifies system files
- All metrics are collected from standard macOS tools (`sysctl`, `df`, `sw_vers`, `uname`, `csrutil`)
- No sudo required for any status information

## Related Commands

- `mo clean` — Free up disk space after checking status
- `mo optimize` — Refresh caches and services
- `mo analyze` — Deep-dive into disk usage
- `mo --version` — System info and free space in non-interactive mode

## Examples

Common workflows combining status with other commands:

```bash
# 1. Check current disk usage
mo status

# 2. Preview what can be cleaned
mo clean --dry-run

# 3. Actually clean
mo clean

# 4. Verify freed space
mo status
```

