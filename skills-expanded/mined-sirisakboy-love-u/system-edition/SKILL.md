---
name: system-edition
description: Optimize a Linux workstation/server for minimal CPU, RAM, and storage usage, maximum stability, prevention of interruptions, and memory/swap efficiency. Uses optimize_system.sh which tunes CPU governor/boost, vm.swappiness/cache pressure, zRAM, storage cleanup, TCP/network buffers, logind/screen/DPMS interruptions, and kernel security hardening (kexec, dmesg, core dumps). Supports --dry-run for preview without root.
metadata:
  version: "1.3.0"
  language: en
  optimized: true
  icon: "⚙️"
  tags:
    - linux
    - system
    - optimization
    - performance
    - kernel
    - sysctl
    - cpu
    - ram
    - network
  github: "https://github.com/sirisakboy/sell/tree/main/.claude/skills/system-edition/"
  import-mode: read-only
  sync: auto-from-source
---

# System Edition Optimizer (v1.3.0)

A self-contained Bash script (`optimize_system.sh`) that tunes a Linux system for **minimal CPU, RAM & storage usage, maximum stability, fewer interruptions, and efficient memory/swap**.

Run with `--dry-run` first to preview every change without needing root.

## Quick start

```bash
# Preview all optimizations (no root needed)
./optimize_system.sh --dry-run

# Apply everything persistently (requires root)
sudo ./optimize_system.sh --all --persistent

# Run only specific categories
sudo ./optimize_system.sh --ram --storage
```

## What it does

| Category | Tuning | Key settings |
|----------|--------|--------------|
| **CPU** | Governor, disable boost, scheduler | `cpu_scaling_governor=ondemand`, `kernel.sched_autogroup_enabled=0` |
| **RAM** | Swappiness, cache pressure, zRAM | `vm.swappiness=10`, `vm.vfs_cache_pressure=50`, zRAM (2G, lz4) |
| **Storage** | Package cache, journal, old logs | `apt-get clean/autoremove`, `journalctl --vacuum-time=2d` |
| **Network** | TCP buffers, congestion control | `tcp_congestion_control=bbr`, `tcp_fastopen=3`, larger rmem/wmem |
| **Interruptions** | Wi-Fi power, DPMS, auto-suspend | `iw dev power_save off`, `xset s off`, `HandleLidSwitch=ignore` |
| **Security** | Kernel hardening | `kexec_load_disabled=1`, `dmesg_restrict=1`, `core_pattern=/bin/false` |

## Options

```
--cpu              CPU governor/boost + scheduler tunables
--ram              vm.swappiness/cache pressure + zRAM
--storage          apt clean, journal vacuum, old logs
--network          TCP buffer + congestion control tuning
--interruptions    Wi-Fi/DPMS/screen timeout + auto-suspend + crash daemons
--security         kexec/dmesg/kptr/perf/core-dump hardening
--all              Run every category (default)
--dry-run          Preview changes without applying (no root needed)
--persistent       Also write sysctl settings to /etc/sysctl.d/99-system-edition.conf
--governor NAME    CPU governor: ondemand | performance | powersave (default: ondemand)
--skip-zram        Do not attempt to enable zRAM compression
--quiet / -q       Suppress console output (still logs to /var/log/system-edition.log)
--help / -h        Show full help
```

## Examples

```bash
sudo ./optimize_system.sh                          # optimize everything
sudo ./optimize_system.sh --ram --storage          # only RAM + storage
./optimize_system.sh --dry-run                     # preview, no root needed
sudo ./optimize_system.sh --all --persistent       # everything + persistent config
sudo ./optimize_system.sh --network --governor performance
```

## Log file

All output is written to `/var/log/system-edition.log` (when run as root).

## Source

Built from MotorBoy_TH's original system optimization scripts, integrated and optimized into a single pipeline in `skills/system-edition/scripts/optimize_system.sh`.
