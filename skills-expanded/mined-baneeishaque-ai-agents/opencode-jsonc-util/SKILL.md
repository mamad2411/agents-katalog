---
name: opencode-jsonc-util
description: Base — read and validate OpenCode JSONC config files (strip `//` comments, trailing commas); consumed by opencode-remote-mcp-setup and opencode-permission-config.
category: Base-Utility
---

# OpenCode JSONC Utility Skill

Base primitive for reading and validating OpenCode's JSONC configuration format — files that permit `//`
comments and trailing commas, which standard `json.loads` rejects.

## JSONC Format Summary

OpenCode config files (`opencode.json`, `opencode.jsonc`) extend JSON with two relaxations:

1. **Trailing commas** are permitted before `]` and `}`.
2. **`//` comments** are permitted as full-line or inline (trailing) comments.

## Usage

### CLI

```bash
python3 scripts/read-jsonc.py <file-path>
```

- Reads the file, strips `//` comment lines and trailing commas, outputs valid JSON to stdout.
- Exit 0 on success, 1 on failure with diagnostic to stderr.

### Python

Import `read_jsonc` from `scripts/read-jsonc.py`:

```python
from read_jsonc import read_jsonc
data = read_jsonc("/path/to/opencode.json")
```

## Related Skills

- [`opencode-remote-mcp-setup`](../opencode-remote-mcp-setup/SKILL.md) — Consumes this skill for JSONC reading
- [`opencode-permission-config`](../opencode-permission-config/SKILL.md) — Consumes this skill for JSONC reading
- [`opencode-provider-persistence-config`](../opencode-provider-persistence-config/SKILL.md) — OpenCode credential storage details
- [`opencode-google-gemini-config`](../opencode-google-gemini-config/SKILL.md) — Gemini provider configuration
- [`opencode-config-preserve`](../opencode-config-preserve/SKILL.md) — OpenCode config preservation
