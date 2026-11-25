---
name: system-info
description: Gather system information including OS, CPU, memory, disk usage, and network details. Useful for diagnostics and environment checks.
allowed-tools: Bash, Read
metadata:
  version: "1.0.0"
  requires-secrets: []
  author: Patrity
  tags: [official, diagnostics]
  repository: "https://github.com/Patrity/cognova-skills"
  installed-from: "cognova-skills"
---

# System Info

Gather system information for diagnostics and environment checks.

## Usage

When the user asks about their system, environment, or wants diagnostics:

```bash
python3 ~/.claude/skills/system-info/system-info.py [--json] [--section SECTION]
```

### Sections

- `os` - Operating system details
- `cpu` - CPU information
- `memory` - RAM usage
- `disk` - Disk usage
- `network` - Network interfaces
- `all` - Everything (default)

### Examples

- `/system-info` - Full system report
- `/system-info --section memory` - Just memory info
- `/system-info --json` - Machine-readable output
