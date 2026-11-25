---
name: migrate
description: "Migrate Agent Teams configuration to the latest version. Use when upgrading versions."
user-invocable: true
allowed-tools: Bash(npx:*), Bash(cd:*), Read, Glob
---

# /migrate

Migrate Agent Teams configuration from an older version to the latest.

## Usage

```bash
npx create-agent-system migrate [--dry-run] [--target-version <ver>] [--yes]
```

Options:
- `--dry-run` — Preview changes only (no actual modifications)
- `--target-version` — Target version (default: 1.0)
- `--yes, -y` — Skip confirmation prompts

## Supported migration paths

| Source | Target | Changes |
|--------|--------|---------|
| v0.1 (no config) | v0.2 | Scan .claude/ files → generate config file |
| v0.2 | v1.0 | Update version, add language field |

## Flow

1. Auto-detect current version
2. Calculate migration path
3. Display changes
4. User confirmation
5. Execute migration
6. Validate result
