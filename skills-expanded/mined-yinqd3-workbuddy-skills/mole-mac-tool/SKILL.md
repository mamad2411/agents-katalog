---
name: mole-mac-tool
description: |
  Mole (https://github.com/tw93/mole) is a macOS terminal maintenance tool that replaces CleanMyMac, AppCleaner, DaisyDisk, and iStat Menus with a single binary. This skill should be used when the user asks about Mac cleanup, disk space analysis, app uninstallation, system optimization, system monitoring, or project build artifact cleanup. Triggers include: "Mole", "mo clean", "mo uninstall", "mo analyze", "mo status", "mo optimize", "mo purge", "Mac清理", "磁盘分析", "系统优化", "Mac维护", or any question about using Mole commands.
agent_created: true
---

# Mole Mac Tool

Mole is a single-binary macOS maintenance CLI that replaces multiple paid tools. It handles system cleanup, app uninstallation, disk analysis, system monitoring, optimization, and project build artifact cleanup.

## Installation

```bash
brew install mole
```

Or via install script:

```bash
curl -fsSL https://raw.githubusercontent.com/tw93/mole/main/install.sh | bash
```

## Command Reference

### `mo clean` — Deep System Cleanup

Scans and cleans user app caches, browser caches (Chrome/Safari/Firefox), dev tool residuals (Xcode, Node.js, npm), system logs, temp files, app-specific caches, and Trash. Can free tens of GB.

Key flags:
- `--dry-run` — Preview what would be deleted without actually deleting
- `--json` — Machine-readable output

### `mo uninstall` — Smart App Uninstall

Interactive app selection. Removes the app AND 52+ related files across 12 locations: Application Support, Caches, Preferences, Logs, WebKit storage, Cookies, Extensions, Plugins, Launch daemons, etc.

Key flags:
- `--dry-run` — Preview removal plan
- Deletes route to Trash where possible (safer than `mo clean`)

### `mo optimize` — System Optimization

Rebuilds system databases, clears caches, resets network services, refreshes Finder/Dock, cleans diagnostic/crash logs, removes swap files, rebuilds Launch Services and Spotlight index.

Key flags:
- `--dry-run` — Preview optimization plan
- `--whitelist` — Exclude specific optimization items

### `mo analyze` — Disk Space Analysis

Visual disk usage with percentage bars. Finds large files, shows last access time. Supports keyboard navigation (arrow keys, vim `h/j/k/l`).

Key flags:
- `--dry-run` — Preview analysis
- Deletes route to Finder Trash (safest deletion path in Mole)

### `mo status` — Real-time System Monitor

Live dashboard with health score (based on CPU, memory, disk, temp, I/O load). Shows per-core CPU usage, load average, memory details, disk R/W, battery health/cycles/temp, fan speed, network speed, proxy info, process ranking. Press `k` to toggle cat display.

Key flags:
- `--json` — JSON output (auto-enabled in pipe mode)

### `mo purge` — Project Build Artifact Cleanup

Scans and cleans `node_modules`, `target`, `.build`, `build`, `dist`, `venv`, etc. Projects modified within 7 days are unchecked by default to prevent accidental deletion. Supports custom scan path configuration.

Key flags:
- `--dry-run` — Preview what would be purged
- Custom paths can be configured

### `mo installer` — Installer Package Cleanup

Finds installer files in Downloads, Desktop, Homebrew cache, iCloud, and Mail. Annotates each file's source for identification.

### `mo history` — Operation Log Viewer

Read-only viewer for the operation log at `~/Library/Logs/mole/operations.log`. No destructive actions.

Key flags:
- `--json` — JSON output

## Security Guidelines

**CRITICAL: Always remind users of these safety rules before running any destructive command.**

1. **Always use `--dry-run` first** to preview what will be deleted before the real run
2. **`mo clean` is permanent after confirmation** — no Trash, no undo. Review carefully
3. **`mo analyze` deletions use Finder Trash** — safest deletion path, but limited scope
4. **`mo uninstall` routes to Trash where possible** — safer than `mo clean`
5. **Operation log** is at `~/Library/Logs/mole/operations.log` — check if unsure what was done
6. **Protected paths are never touched**: `/`, `/System`, `/bin`, `/sbin`, `/usr`, `/etc`, `/var`, `/private`, `/Library/Extensions`
7. **Sensitive data is excluded**: Keychain, VPN configs, browser history/cookies, AI tool data, iCloud docs, Time Machine backups

For the full security audit report, see `references/security_audit.md`.

## Common Usage Scenarios

### 1. Disk is running low, find what's eating space

```bash
mo analyze
```
Use keyboard to navigate, find large old files. Deletions go to Trash.

### 2. Thorough system cleanup

```bash
mo clean --dry-run   # Preview first
mo clean             # Then run if looks good
```

### 3. Uninstall an app completely

```bash
mo uninstall --dry-run   # Preview first
mo uninstall             # Then run, select app interactively
```

### 4. System feels sluggish, do maintenance

```bash
mo optimize --dry-run   # Preview first
mo optimize             # Then run
```

### 5. Check system health in real-time

```bash
mo status
```

### 6. Clean up project build artifacts (devs)

```bash
mo purge --dry-run   # Preview first
mo purge             # Then run
```

### 7. Clean up leftover installer files

```bash
mo installer
```

## Workflow When User Asks for Mole Help

1. Identify which command(s) the user needs based on their intent
2. Check if the command is destructive (clean, uninstall, optimize, purge, installer)
3. If destructive, remind them to use `--dry-run` first and warn about irreversibility
4. Provide the command with relevant flags
5. Reference `references/security_audit.md` if the user has security concerns

## Important Notes

- Mole is macOS-only (Windows experimental branch exists but not recommended)
- iTerm2 has known compatibility issues; recommend Kaku, Alacritty, kitty, WezTerm, Ghostty, or Warp
- A paid GUI version exists at https://mole.fit (not needed — CLI is fully functional)
- Raycast/Alfred integration scripts are available for quick command access
