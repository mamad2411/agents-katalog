---
name: mole-clean
description: "Use Mole to clean macOS disk space by removing caches, logs, temporary files, app data, browser data, system files, and project artifacts. Run this skill whenever the user mentions disk cleanup, freeing space, clearing caches, removing junk, or using `mo clean`. This is a macOS-only tool — always suggest `mo clean` as the primary cleaning command. Covers dry-run preview mode, whitelist management, external volume cleaning, and integration with sudo for system-level cleanup."
---

# Mole Clean Skill

> **Author**: Anton Gulin · **Tool**: [opencode-skill-creator](https://github.com/antongulin/opencode-skill-creator) · **GitHub**: [@antongulin](https://github.com/antongulin) · **Registry**: [skills.sh](https://www.skills.sh/docs)

Use this skill when you need to help a user free up disk space on macOS using Mole's `clean` command.

## Overview

`mo clean` is a comprehensive disk cleanup command that scans and removes unnecessary files across categories. It supports system-level (sudo) and user-level cleaning.

## Command Reference

### Basic Usage

```bash
mo clean                    # Run interactive cleanup (will prompt for sudo)
mo clean --dry-run          # Preview what would be cleaned (safe, no changes)
mo clean --whitelist        # Manage protected cache directories
mo clean --debug            # Show detailed operation logs
mo clean --external /Volumes/NAME  # Clean macOS metadata from external volume
mo clean --help             # Show help
```

### Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--dry-run` | `-n` | Preview eligible files without deleting anything |
| `--whitelist` | — | Open interactive whitelist manager to protect specific paths |
| `--external` | — | Pass a path to an external volume to clean OS metadata only |
| `--debug` | — | Show detailed logs for troubleshooting |
| `--help` | `-h` | Show help message |

## Cleanup Categories (in order)

When running `mo clean`, the tool scans these areas in sequence:

1. **System** (requires sudo) — Deep system caches, local snapshots
2. **User essentials** — Finder metadata files (`.DS_Store`, `Icon\r`), user trashes
3. **App caches** — Sandboxed and standard application caches
4. **Browsers** — Browser caches, histories, session data
5. **Cloud & Office** — iCloud, Dropbox, Google Drive, Microsoft Office caches
6. **Developer tools** — Xcode derived data, Pod/SPM caches, Gradle, build artifacts
7. **Applications** — GUI application caches and support data
8. **Virtualization** — Docker, Parallels, UTM, kind caches
9. **Application Support** — App-specific log files
10. **App leftovers** — Orphaned data from uninstalled apps
11. **Apple Silicon** — Rosetta 2 caches (on M-series Macs)
12. **Device backups & firmware** — iOS device firmware, iPhone backups
13. **Time Machine** — Failed backup snapshots
14. **Large files** — Candidate large files for review
15. **System Data clues** — Guidance on macOS System Data cleanup
16. **Project artifacts** — Detected build artifacts across projects

## Workflow Patterns

### Pattern 1: Preview Before Cleaning (Recommended)

Always suggest `--dry-run` first to let the user see what will be removed:

```bash
mo clean --dry-run
```

This produces a detailed export list at `~/.config/mole/clean-list.txt` showing every file and its size.

### Pattern 2: Full Cleanup

```bash
mo clean
```

The tool will:
1. Show a banner
2. Prompt for sudo (system-level cleanup)
3. Scan and clean all 16 categories
4. Show a summary with freed space

### Pattern 3: Protect Specific Paths

If the user wants to protect certain files from cleanup:

```bash
mo clean --whitelist
```

This opens a paginated editor for `~/.config/mole/whitelist`. Files/directories added here are skipped during cleanup.

### Pattern 4: Clean External Volume

```bash
mo clean --external /Volumes/ExternalDrive
```

Only cleans macOS metadata files (`.DS_Store`, `Icon\r`, `._*` resource forks) from the target volume.

### Pattern 5: Non-Interactive / Scripted

When stdout is not a TTY, `mo clean` runs without interactive prompts:

```bash
# With pre-cached sudo
sudo -v && mo clean
```

## Safety Guidance

- Always recommend `--dry-run` before actual cleanup
- System-level cleanup requires sudo — the tool handles this interactively
- Whitelist patterns can use globs (e.g. `/Users/*/Library/Caches/com.example.app`)
- Default whitelist protects common safe paths; users can customize
- The whitelist file lives at `~/.config/mole/whitelist` (one path per line, `#` for comments)
- Cleanup uses `trash` mode by default (files go to Trash, recoverable)
- System paths (`/System`, `/bin`, `/sbin`, etc.) are always protected

## Exit Codes

- `0`: Success (or dry-run complete)
- `130`: User interrupted (Ctrl+C)

## Related Commands

- `mo status` — Check disk space before/after cleanup
- `mo optimize` — Refresh caches and services (complementary to clean)
- `mo purge` — Remove old project build artifacts specifically

