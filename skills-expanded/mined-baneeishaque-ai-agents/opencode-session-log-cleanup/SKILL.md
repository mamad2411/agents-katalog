---
name: opencode-session-log-cleanup
description: Composer — discover, verify, and remove opencode logger-plugin session log artifacts by session ID.
category: OpenCode
---

# opencode-session-log-cleanup (v1)

> **Name:** opencode-session-log-cleanup<br>
> **Description:** Composer — discover, verify, and remove opencode logger-plugin session log artifacts by session
ID.<br>
> **Category:** OpenCode

## Description

Composer that locates all logger-plugin artifacts for a given opencode
session ID (monolithic `.jsonl` / `.turns.jsonl` / `.state.json` files plus
the per-turn directory layout under `.opencode/logs/`), presents the list
to the user for explicit verification, delegates removal to the
[`safe-file-cleanup`](../../general/file/safe-file-cleanup/SKILL.md) base
skill, and re-verifies that no artifacts remain.

## Composition Rationale

This skill is a composer. It does not reimplement file-removal logic;
instead it orchestrates two concerns:

1. **Discovery** — opencode-specific: enumerates `.opencode/logs/ses_<id>/`
   and the top-level `.opencode/logs/ses_<id>.*` artifacts emitted by the
   logger plugin.
2. **Removal** — generic: delegates to
   [`safe-file-cleanup`](../../general/file/safe-file-cleanup/SKILL.md) so
   that the same trash-aware, verified removal logic is reused by any
   future domain that needs to delete files safely.

The composer's domain-specific value-add is the opencode session-layout
knowledge and the explicit user-verification gate before any deletion.

Bidirectional discoverability: [`safe-file-cleanup`](../../general/file/safe-file-cleanup/SKILL.md) lists this composer
in its `## Composition by Higher-Level Skills` table.

## Related Skills

- [`opencode-current-session-id`](../opencode-current-session-id/SKILL.md) — sibling; resolves the current session
ID/title from logger logs.
- [`opencode-session-yaml-tool-call-extractor`](../opencode-session-yaml-tool-call-extractor/SKILL.md) — sibling; parses
the same YAML/JSONL log formats this skill removes.

## Environment & Dependencies

| Requirement | Version | Notes |
| ------------- | --------- | ------- |
| Python | 3.12+ | Stdlib only — no pip dependencies |
| `safe-file-cleanup` skill | — | Must be present at `../../general/file/safe-file-cleanup/` |

## CLI Contract

| Argument | Required | Description |
| ---------- | ---------- | ------------- |
| `session_id` | Yes | OpenCode session ID (e.g. `ses_<session-id>`) |
| `--logs-dir` | No | Logs directory (default: `.opencode/logs`) |
| `--remove-empty-parents` | No | Remove empty parent directories after cleanup |
| `--yes` | No | Skip user confirmation (use with caution) |

*Exit codes:*

- `0` — session logs removed and verified
- `1` — no logs found, or paths remain after cleanup
- `2` — base skill script missing or fatal error

## Protocol

1. Accept `session_id`.
2. Enumerate existing artifacts under `<logs-dir>/<session_id>.*` and
   `<logs-dir>/<session_id>/`.
3. If none found, exit 1 with a diagnostic.
4. Present the list to the user and require explicit `y` confirmation.
   The `--yes` flag bypasses this gate for non-interactive automation.
5. Shell out to `safe-file-cleanup`'s `scripts/safe_cleanup.py` with the
   discovered paths. Stream stdout/stderr.
6. Re-enumerate artifacts for the same `session_id`.
7. If any path remains, print a warning to stderr and exit 1.
8. Otherwise, print a success message and exit 0.

## Edge Cases

- **Session ID not found**: exits 1 with a clear message; no deletion attempted.
- **Partial removal**: if the base skill reports partial failure, this skill
  re-verifies and exits 1 if any path remains.
- **Base skill missing**: exits 2 immediately with the resolved script path.
- **Non-interactive automation**: `--yes` bypasses the confirmation gate;
  callers MUST ensure they have already performed an external verification step.

## Composition by Higher-Level Skills

None — this skill is a leaf composer in the opencode/ group.
