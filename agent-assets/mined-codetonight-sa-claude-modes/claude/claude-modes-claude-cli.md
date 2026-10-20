# CLI

Command-line interface for claude-modes.

## Contents

| File | Purpose |
|------|---------|
| `modes` | Main CLI entry point |

## Usage

```bash
modes list              # List available modes
modes activate <name>   # Activate a mode
modes deactivate        # Deactivate current mode
modes status            # Show current mode
modes analyze           # Analyze skills
modes create <name>     # Create new mode
modes sync              # Sync with upstream
```

## Installation

Add to PATH:
```bash
export PATH="$PATH:$HOME/.claude/cli"
```
