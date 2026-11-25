---
name: opencode-installed-plugin-lookup
description: >-
  Base — read-only registry lookup of installed opencode plugins: enabled
  status (config 'plugin' array vs auto-loaded plugins/*.ts dirs), plugin
  file paths, and the logger output convention (.opencode/logs); composes
  opencode-jsonc-util for JSONC config parsing.
category: OpenCode
---

# OpenCode Installed-Plugin Lookup (v1)

## Goal

Read-only visibility into which opencode plugins exist and whether they are
enabled, and — for the logger — where its logs land. No writes, no sentinel
probes, no config mutation: it answers "is plugin X installed / enabled,
where does it live, where does it write".

## Composition

- [`opencode-jsonc-util`](../../opencode-jsonc-util/SKILL.md) — JSONC config
  parsing via subprocess call to `scripts/read-jsonc.py` (never re-rolled).
- No other bases — the registry probe itself is this skill's SSOT.

## When to Use

- You need the plugin registry of the current machine (installed vs
  enabled, file paths, logger logs convention).
- A higher-level skill must locate the logger layout before consuming
  `.opencode/logs/` (see
  [`opencode-session-path-attribution`](../opencode-session-path-attribution/SKILL.md),
  which calls this skill's script with `--plugin logger --json`).

## Registry Semantics

| Source | Meaning |
| --- | --- |
| User config `plugin` array | explicitly enabled plugins (`opencode.json` JSONC at `~/.config/opencode/opencode.json`) |
| Project config `plugin` array | `.opencode/opencode.json` (if present) |
| `~/.config/opencode/plugins/*.ts` | auto-loaded plugin files (opencode loads every `.ts` present) |
| `.opencode/plugins/*.ts` (project) | auto-loaded project plugin files |
| `.opencode/logs/` | logger output convention (echoed for `logger`) |

`status` classification:

- `enabled-config`: present in a config `plugin` array
- `enabled-auto-dir`: file exists under a plugins dir (auto-loaded)
- `missing`: neither (only reachable via explicit `--plugin` with a name
  that exists nowhere — see exit codes)

## CLI

```bash
python3 scripts/locate-installed-plugins.py [--plugin <name> ...] [--json]
```

| Flag | Meaning |
| --- | --- |
| `--plugin` | filter to one or more plugin names (repeatable) |
| `--user-config` | override user config path |
| `--project-config` | override project config path |
| `--json` | emit one JSON array instead of JSONL |
| `--output` | write to file instead of stdout |

Output record (JSONL by default):

```json
{"name": "...", "enabled": true, "status": "enabled-config",
 "config_file": "...", "plugin_files": ["..."],
 "logs_dir": "...", "logs_convention": "..."}
```

Exit codes: `0` success, `1` requested `--plugin` names not found, `2`
usage error (unreadable config, missing opencode-jsonc-util).

## Prohibited Actions

- Do NOT re-implement JSONC parsing — always delegate to
  `opencode-jsonc-util`'s parser.
- Do NOT mutate any config/plugin file — this skill is strictly read-only.

## Related Skills

- [`opencode-session-path-attribution`](../opencode-session-path-attribution/SKILL.md)
  — consumer (before sweeping logs)
- [`opencode-session-yaml-tool-call-extractor`](../opencode-session-yaml-tool-call-extractor/SKILL.md)
  — consumer of the logger layout
- [`opencode-current-session-id`](../opencode-current-session-id/SKILL.md)
  — sibling for active-session resolution
