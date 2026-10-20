# Claude-Modes

Purposeful skill loading for Claude Code.

## What This Is

Claude-Modes organizes skills into **modes** - operating contexts that load only relevant skills on demand. Instead of loading all skills (token waste), you activate the mode for your current task.

## Quick Start

```bash
modes list              # See available modes
modes activate code     # Activate code mode
modes status            # Check current mode
modes deactivate        # Deactivate mode
```

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `modes/` | Mode definitions and foundation |
| `skills/` | Skill files organized by domain |
| `lib/` | Core libraries |
| `cli/` | CLI entry point |
| `templates/` | Templates for creating modes/skills |
| `docs/` | Documentation |

## Foundation

Foundation skills (in `modes/foundation.md`) are ALWAYS active. They cannot be disabled by any mode. Mode-specific skills stack on top.
