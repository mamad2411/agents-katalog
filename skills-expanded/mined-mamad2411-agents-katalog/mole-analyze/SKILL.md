---
name: mole-analyze
description: "Use Mole to explore macOS disk usage with an interactive TUI or JSON output. Run this skill whenever the user mentions analyzing disk space, finding large files, exploring disk usage, checking storage, or using `mo analyze`. Covers overview mode, directory scanning, file navigation, large file detection, deleting files, JSON output, and custom path analysis."
---

# Mole Analyze Skill

> **Author**: Anton Gulin · **Tool**: [opencode-skill-creator](https://github.com/antongulin/opencode-skill-creator) · **GitHub**: [@antongulin](https://github.com/antongulin) · **Registry**: [skills.sh](https://www.skills.sh/docs)

Use this skill when you need to help a user explore disk usage on macOS using Mole's `analyze` command.

## Overview

`mo analyze` provides an interactive disk usage analyzer (built with Bubble Tea) that lets users navigate directories, find large files, and delete files directly. It also supports JSON output for scripting.

## Command Reference

### Basic Usage

```bash
mo analyze                          # Overview mode: scan Home, Library, Applications, System
mo analyze /path/to/dir             # Analyze a specific directory
mo analyze --json                   # Output analysis as JSON (no TUI)
mo analyze /Volumes/Backup          # Analyze an external drive
mo analyze --json /path             # JSON output for specific path
mo analyze --help                   # Show help
```

### Flags

| Flag | Description |
|------|-------------|
| `--json` | Output analysis as JSON instead of TUI |
| `--help` | Show help |

### Environment Variable

```bash
MO_ANALYZE_PATH=/custom/path mo analyze  # Set analysis path via env var
```

## Interactive TUI Controls

When running `mo analyze` without `--json`, a full-screen TUI opens with these controls:

| Key | Action |
|-----|--------|
| `↑/↓` or `j/k` | Navigate entries (skips zero-size entries) |
| `Enter` or `→` or `l/L` | Enter selected directory |
| `Esc` or `←` or `h/H` | Go back to parent directory |
| `q` or `Q` or `Ctrl+C` | Quit |
| `r` or `R` | Refresh/rescan current directory |
| `t` or `T` | Toggle large files view |
| `Space` | Toggle multi-select for batch operations |
| `Delete` or `Backspace` | Delete selected file(s)/dir(s) (confirms first) |
| `o` or `O` | Open selected file in Finder/application |
| `f` or `F` | Reveal selected file in Finder |
| `p` or `P` | Quick Look preview selected file |

### Multi-Select Workflow

1. Navigate to items, press `Space` to select each
2. Status bar shows item count and total size
3. Press `Delete` to remove all selected items
4. Confirm by pressing `Enter`

## Overview Mode Entries

When run without a path argument, `mo analyze` enters overview mode showing:

1. **Home** — User home directory
2. **User Library** — `~/Library` (renamed for clarity)
3. **Applications** — `/Applications`
4. **System Library** — `/Library`
5. **Hidden Insights** — System locations that silently accumulate disk usage (e.g., `~/Library/Group Containers/`, Time Machine snapshots, Mail downloads, etc.)

Each is scanned asynchronously with a progress indicator.

## JSON Output

When `--json` is passed or stdout is piped, `mo analyze --json /path` outputs structured JSON:

```json
{
  "path": "/Users/username",
  "total_size": 123456789,
  "total_files": 54321,
  "entries": [
    {
      "name": "Library",
      "path": "/Users/username/Library",
      "size": 50000000,
      "is_dir": true,
      "last_access": "2026-05-10T14:30:00Z"
    }
  ],
  "large_files": [
    {
      "name": "big-file.dmg",
      "path": "/Users/username/Downloads/big-file.dmg",
      "size": 4294967296
    }
  ]
}
```

## Workflow Patterns

### Pattern 1: Interactive Disk Exploration (Recommended)

```bash
mo analyze
```

Opens a full-screen TUI showing overview of key system directories. Navigate using keyboard controls to drill into folders, find large files, and optionally delete them.

### Pattern 2: Analyze a Specific Directory

```bash
mo analyze ~/Downloads
```

Scans the specified directory and opens the TUI with results.

### Pattern 3: JSON Output for Scripting

```bash
mo analyze --json /path/to/dir
```

Useful for programmatic analysis or piping to other tools.

### Pattern 4: Check External Drive

```bash
mo analyze /Volumes/ExternalDrive
```

Analyze space usage on an external volume.

### Pattern 5: Find and Remove Large Files

In the TUI:
1. Navigate to a directory
2. Press `t` to toggle large files view
3. Use `Space` to select multiple files
4. Press `Delete` and confirm to move to Trash

## Performance Notes

- Scans are cached on disk for fast re-entry
- Large directories use parallel scanning with controlled concurrency
- Progress indicators show files scanned and bytes scanned
- Overview mode scans paths asynchronously to stay responsive

## Safety Guidance

- Deleted files go to Trash (recoverable) — no `--permanent` flag exists here
- The delete confirmation requires pressing Enter after the prompt
- Multi-select allows batch deletion — warn about total size before confirming
- The `r` key refreshes the current directory (useful after deletions)
- Cache is invalidated after deletions to reflect accurate state

## Exit Codes

- `0`: Normal exit (quit or finished)
- `1`: Path resolution error

## Related Commands

- `mo status` — Check overall system health and disk free space
- `mo clean` — Clean up caches and temporary files (complementary)
- `mo uninstall` — Remove unused applications

