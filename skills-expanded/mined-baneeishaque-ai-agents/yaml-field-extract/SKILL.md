---
name: yaml-field-extract
description: Base primitive — extract a value from a YAML file by dot-separated key path, with multi-document support
category: General
---

# YAML Field Extract (v1)

## Scope & Intent

**In scope:**
- Extract a single value from a YAML file by dot-separated key path (e.g. `session.id` → `data["session"]["id"]`)
- Multi-document YAML support via `--doc-index`
- Output raw value as string (JSON for compound types)

**Out of scope:**
- YAML writing or mutation
- Shell environment variable substitution
- JSON-only files (use `jq`)

## Environment & Dependencies

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.12+ | |
| PyYAML | any | PEP 723 inline metadata — `uv run --script` |

## CLI Contract

| Argument | Required | Description |
|----------|----------|-------------|
| `--file` | Yes | Path to YAML file |
| `--key` | Yes | Dot-separated key path (e.g. `session.id`) |
| `--doc-index` | No | Document index for multi-doc YAML (default: 0) |

**Output:** raw value to stdout (string, or JSON for dict/list).

**Exit codes:**
- `0` — value found and printed
- `1` — key not found or file issue
- `2` — PyYAML not installed

## Protocol

1. Verify `--file` exists and is readable.
2. Run `python3 scripts/extract-field.py --file <path> --key <dot-path> [--doc-index N]`
3. Consume stdout (the extracted value).

## Edge Cases

- **Key not found**: exits 1, no output
- **Multi-doc YAML**: use `--doc-index` to select the document (default: first)
- **Compound values (dict/list)**: output as JSON
- **Empty YAML file**: exits 1

## Prohibited Actions

- Do NOT parse YAML manually in calling scripts — always use this script.
- Do NOT hardcode key paths — pass them via `--key`.

## Script Reference

`extract-field.py`:
1. Reads YAML file via `yaml.safe_load_all()`
2. Selects document by `--doc-index`
3. Navigates dot-path through dict keys via `dot_get()`
4. Outputs value as string (JSON for compound types)

## Composition by Higher-Level Skills

- `opencode-current-session-id` — composer that uses this skill to extract `session.id` and `title` from YAML headers

## Related Skills

- [`file-glob-sort-by-mtime`](../file/file-glob-sort-by-mtime/SKILL.md) — sibling base; provides the YAML file path by mtime ordering
