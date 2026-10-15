---
name: mole-uninstall
description: "Use Mole to completely remove macOS applications including their support files, caches, and preferences. Run this skill whenever the user mentions uninstalling apps, removing applications, app cleanup, deleting software, or using `mo uninstall`. Covers app scanning, name-based matching, interactive selection, dry-run mode, permanent deletion, and listing installable apps."
---

# Mole Uninstall Skill

> **Author**: Anton Gulin · **Tool**: [opencode-skill-creator](https://github.com/antongulin/opencode-skill-creator) · **GitHub**: [@antongulin](https://github.com/antongulin) · **Registry**: [skills.sh](https://www.skills.sh/docs)

Use this skill when you need to help a user remove macOS applications completely using Mole's `uninstall` command.

## Overview

`mo uninstall` finds all installed applications (including Homebrew casks), scans their sizes and last-used dates, and removes them along with leftovers.

## Command Reference

### Basic Usage

```bash
mo uninstall                          # Interactive TUI: scan, select apps, confirm delete
mo uninstall AppName                  # Directly uninstall a specific app by name
mo uninstall Safari Chrome             # Uninstall multiple apps at once
mo uninstall --dry-run AppName        # Preview what would be removed
mo uninstall --list                   # List all uninstallable apps (table or JSON)
mo uninstall --permanent AppName      # Delete permanently (skip Trash)
mo uninstall --debug                  # Show detailed operation logs
mo uninstall --help                   # Show help
```

### Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--dry-run` | `-n` | Preview app uninstall without modifying files |
| `--permanent` | — | Use `rm -rf` instead of Trash (not recoverable) |
| `--list` | — | List all detected apps in table or JSON format |
| `--debug` | — | Show detailed operation logs |
| `--help` | `-h` | Show help |

## App Name Arguments

Pass app names after flags. Matching is case-insensitive and supports:

- **Exact match** — `mo uninstall Slack`
- **Substring match** — `mo uninstall slack` (matches Slack, Slack Helper, etc.)
- **Multiple apps** — `mo uninstall Slack Discord Zoom`

If a name matches multiple apps, all are included.

## Workflow Patterns

### Pattern 1: List All Uninstallable Apps

```bash
mo uninstall --list
```

Shows a table with: NAME, BUNDLE ID, UNINSTALL NAME (Homebrew cask name if available), and SIZE. Output is JSON when piped:

```bash
mo uninstall --list | jq '.[] | select(.source == "Homebrew")'
```

### Pattern 2: Preview Before Uninstalling (Recommended)

```bash
mo uninstall --dry-run AppName
```

Shows what files would be affected without making changes.

### Pattern 3: Interactive Uninstall (No Arguments)

```bash
mo uninstall
```

1. Scans all applications from `/Applications`, `~/Applications`, `/Volumes/*/Applications`
2. Shows a paginated TUI with size and last-used info
3. User selects apps with Space, confirms with Enter
4. Shows uninstall summary with confirmation
5. Moves apps to Trash by default

### Pattern 4: Direct Uninstall by Name

```bash
mo uninstall Slack
```

1. Scans apps
2. Matches "Slack" against display names and `.app` bundle names
3. Shows matched apps with size and last-used
4. Prompts for confirmation
5. Proceeds with uninstall

### Pattern 5: Permanent Deletion (Skip Trash)

```bash
mo uninstall --permanent AppName
```

Files are deleted with `rm -rf` instead of being moved to Trash. **Not recoverable.** Only use when the user explicitly confirms they want permanent deletion.

## Uninstall Behavior

- **Default mode**: Move to Trash (recoverable). Controlled by `MOLE_DELETE_MODE=trash`
- **Permanent mode**: `MOLE_DELETE_MODE=permanent` — direct `rm -rf`
- **Metadata cache**: App metadata (size, last used) cached at `~/.cache/mole/uninstall_app_metadata_v1` for 7 days
- **Scan locations**: `/Applications`, `~/Applications`, Input Methods directories, `/Volumes/*/Applications`
- **Protected apps**: System apps and background-only apps are automatically excluded
- **Homebrew cask detection**: If an app was installed via Homebrew, the cask name is shown as the uninstall name

## Safety Guidance

- Default Trash mode is safe — files can be recovered
- `--permanent` is irreversible — warn the user before using
- Always suggest `--dry-run` or `--list` before destructive operations
- Background-only apps (e.g., login items, system services) are never shown
- Apps in `/System` are excluded automatically
- Bundle ID protection exists via `should_protect_from_uninstall` — system-critical bundle IDs are skipped

## Exit Codes

- `0`: Success or user cancelled
- `130`: Interrupted (Ctrl+C)

## Related Commands

- `mo status` — Check disk space before/after uninstall
- `mo clean` — Clean up leftover app data after uninstall
- `mo optimize` — Refresh services after removing large apps

