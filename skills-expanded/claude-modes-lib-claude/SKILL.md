# Libraries

Core libraries and utilities.

## Contents

| File | Purpose |
|------|---------|
| `mode-loader.sh` | Activate, deactivate, and manage modes |
| `skill-analyzer.py` | Analyze skills and suggest mode assignments |

## Usage

### mode-loader.sh

Sourced by CLI. Provides:
- `list_modes()` - List available modes
- `activate_mode()` - Activate a mode
- `deactivate_mode()` - Deactivate current mode
- `mode_status()` - Show current mode

### skill-analyzer.py

```bash
python3 lib/skill-analyzer.py --skills-dir ~/.claude/skills
python3 lib/skill-analyzer.py --format json
python3 lib/skill-analyzer.py --semantic  # Requires embeddings setup
```
