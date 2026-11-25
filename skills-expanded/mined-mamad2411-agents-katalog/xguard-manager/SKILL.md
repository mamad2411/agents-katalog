---
name: xguard-manager
description: Read, replace, reset, export, and import XGuard policy options on the orchestrator. Use when you need to inspect current per-label policies for text or prompt scans, ship a refined policy, restore defaults, or back up the policy registry. Read-only by default; destructive operations require an explicit `--writable` flag.
---

# XGuard Policy Manager

Use this skill to manage XGuard policy options against the orchestrator's `/v1/manager/xguard/*` admin endpoints.

Each label's policy is the natural-language prompt text + threshold + action that the orchestrator applies when evaluating an XGuard call. See [docs/features/scanner-prompt-tuning.md](../../../docs/features/scanner-prompt-tuning.md) for how this fits into the scanner refinement lifecycle. Phase 4 (refine policy) is the typical use of this skill: fetch the current options, edit a policy, PUT the new version, then track FP/FN rates against the new `policyHash` in the audit log.

## Setup

The skill reads `ORCHESTRATOR_ENDPOINT` and `ORCHESTRATOR_ACCESS_TOKEN` from the project `.env` (or `.claude/skills/xguard-manager/.env` if you want skill-specific overrides). No additional setup beyond having those env vars set.

## Commands

```bash
node .claude/skills/xguard-manager/manage.mjs <command> [args] [options]
```

| Command | Description |
|---------|-------------|
| `get <mode>` | GET current options for the mode (`text` or `prompt`) |
| `defaults <mode>` | GET hardcoded defaults baked into the orchestrator |
| `put <mode>` | PUT new options for the mode (requires `--writable` + `--file`) |
| `reset <mode>` | POST reset back to defaults (requires `--writable`) |
| `export` | GET bulk export across all modes |
| `import` | PUT bulk import across all modes (requires `--writable` + `--file`) |

## Options

| Flag | Description |
|------|-------------|
| `--writable` | Allow destructive operations (PUT / POST). Required for `put`, `reset`, `import`. |
| `--file <path>`, `-f <path>` | Read the request body (JSON) from a file. Required for `put` and `import`. |
| `--output <path>`, `-o <path>` | Save response to a file (instead of printing to stdout). |
| `--quiet`, `-q` | Only print the response body, no connection headers. |
| `--timeout <s>`, `-t <s>` | Request timeout in seconds (default: 30). |

## Examples

```bash
# Inspect current prompt-mode options
node .claude/skills/xguard-manager/manage.mjs get prompt

# Save the current prompt-mode options to a file you can edit
node .claude/skills/xguard-manager/manage.mjs get prompt -o /tmp/prompt-policies.json

# See what the defaults look like (useful for scaffolding a new label)
node .claude/skills/xguard-manager/manage.mjs defaults prompt

# Ship an edited policy
node .claude/skills/xguard-manager/manage.mjs put prompt -f /tmp/prompt-policies.json --writable

# Wipe prompt-mode policies back to defaults (destructive)
node .claude/skills/xguard-manager/manage.mjs reset prompt --writable

# Back up the entire policy registry before a risky edit
node .claude/skills/xguard-manager/manage.mjs export -o /tmp/xguard-backup.json

# Restore from a backup
node .claude/skills/xguard-manager/manage.mjs import -f /tmp/xguard-backup.json --writable
```

## Safety

1. **Read-only by default**: `get`, `defaults`, and `export` always work without `--writable`.
2. **Destructive operations require explicit `--writable`**: `put`, `reset`, and `import` change orchestrator state and refuse to run without the flag.
3. **Always ask the user before using `--writable`**: policy changes are global — every subsequent scan will use the new policy text. Confirm the intent before running.
4. **Back up before editing**: run `export -o backup.json` before any non-trivial change so you can `import` to restore if needed.

## Typical workflow for refining a policy (Phase 4)

```bash
# 1. Snapshot current state for safe rollback
node .claude/skills/xguard-manager/manage.mjs export -o /tmp/xguard-backup-$(date +%Y%m%d).json

# 2. Pull the current options for the mode you're editing
node .claude/skills/xguard-manager/manage.mjs get prompt -o /tmp/prompt-current.json

# 3. Edit /tmp/prompt-current.json with the refined policy text

# 4. Ship it (after user confirms)
node .claude/skills/xguard-manager/manage.mjs put prompt -f /tmp/prompt-current.json --writable

# 5. Track FP/FN rate of new policyHash via the audit log + focused review
```

## Why this is separate from the postgres-query / clickhouse-query skills

Those query the audit *data* (verdicts, scores, matched terms). This skill manages the *policy* itself — the prompt text the orchestrator hands to XGuard. A typical tuning loop uses both: query data to identify FP patterns, edit the policy here, then re-query after new scans land under the new `policyHash`.
