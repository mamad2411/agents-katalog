---
name: openclaw-uninstall
description: |
  Cross-platform uninstall script for OpenClaw. Completely removes OpenClaw CLI and all residual files.
  Use when: (1) User wants to completely remove OpenClaw, (2) Cleaning up OpenClaw installation,
  (3) Uninstalling OpenClaw CLI (npm/pnpm/bun), (4) Removing OpenClaw desktop app (macOS),
  (5) Cleaning all OpenClaw data directories and config files.
---

# OpenClaw Uninstall

Downloads and executes the uninstall script to completely remove OpenClaw from the system.

## Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/billLiao/openclaw-uninstall/main/uninstall.sh | bash
```

Or run locally after downloading:
```bash
chmod +x uninstall.sh && ./uninstall.sh
```

## What Gets Removed

### CLI (auto-detected)
- npm: `npm uninstall -g openclaw`
- pnpm: `pnpm remove -g openclaw`
- bun: `bun pm rm -g openclaw`

### Data Directories
- `~/.openclaw`
- `~/.config/openclaw`
- `~/.local/share/openclaw`
- `~/openclaw-workspace`

### Config Files
- `~/.openclawrc`
- `~/.openclaw-config`
- `~/.openclaw.json`

### macOS Specific
- `/Applications/OpenClaw.app`
- `~/Library/LaunchAgents/com.openclaw.daemon.plist`

## Platform Support

| Platform | Script | Command |
|----------|--------|---------|
| Linux / macOS / WSL / MCP | `.sh` | `curl -fsSL https://raw.githubusercontent.com/billLiao/openclaw-uninstall/main/uninstall.sh \| bash` |
| Windows (CMD) | `.bat` | `curl -fsSL https://raw.githubusercontent.com/billLiao/openclaw-uninstall/main/uninstall.bat -o uninstall.bat && uninstall.bat` |
| Windows (PowerShell) | `.ps1` | `irm https://raw.githubusercontent.com/billLiao/openclaw-uninstall/main/uninstall.ps1 \| iex` |

### Platform Details
- **macOS**: Full support (CLI + app + LaunchAgent)
- **Linux**: Full support (CLI + data directories)
- **Windows CMD**: Use `uninstall.bat`
- **Windows PowerShell**: Use `uninstall.ps1`

## Warning

This action is irreversible. Make sure to backup any important data before running.