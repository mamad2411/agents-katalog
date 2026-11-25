---
name: opencode-session-path-attribution
description: >-
  Base — sweep opencode logger per-turn session logs and attribute tool calls
  to sessions by path token (cross-session forensic): which session touched
  path X, when, with what exact command; consumes the
  opencode-session-yaml-tool-call-extractor CLI, locates the logger via
  opencode-installed-plugin-lookup.
category: OpenCode
---

# OpenCode Session Path Attribution (v1)

## Composition Rationale

This skill is a **base primitive**: it owns ONLY the cross-session sweep
logic (session-dir discovery, newest-first ordering, turn-filename time
windows, token matching against stringified args) that the dangling-link
composer and ad-hoc "who did this" forensics reuse. It composes:

1. [`opencode-session-yaml-tool-call-extractor`](../opencode-session-yaml-tool-call-extractor/SKILL.md)
   — per-turn-file subprocess consumer of its stdout JSONL contract
   (SSOT for YAML parsing; never re-implemented here)
2. [`opencode-installed-plugin-lookup`](../opencode-installed-plugin-lookup/SKILL.md)
   — locates the logger plugin and its output convention
   (never the re-implemented locator)

The extractor answers "what did session S do"; this skill answers
"which session(s) did X, and when".

***

## 1. Environment & Dependencies

| Requirement | Minimum | Verification |
| --- | --- | --- |
| Python | 3.12+ | `python3 --version` |
| extractor base skill | present | sibling script at repo root |
| logger YAML logs | `ses_<id>/NNN-<timestamp>.yaml` | `.opencode/logs/` |

Stdlib only. The extractor requires PyYAML — see its Environment section.

## 2. Operational Logic

### 2.1 Session & Turn Selection

- `--logs` default: **discovered** via Base #2 (`--plugin logger --json`),
  falling back to `<repo>/.opencode/logs`.
- All `ses_*` directories walked, **newest-mtime first**; `--session`
  restricts the set (each `ses_` prefix optional).
- Inside a session dir, turn files (`NNN-<timestamp>.yaml`) are processed in
  filename (chronological) order; `000-header-*` files are skipped.
- `--since` / `--until` windows are enforced on the **turn-filename
  timestamp** (`2026-08-07T04-14-05-689Z` → aware UTC datetime).

### 2.2 Matching

A record matches when **ALL** `--path` tokens appear (substring,
**case-sensitive**) in the record's stringified `args` (`json.dumps` of the
raw `args` dict — never a pretty-print or partial dict). `--tool` filters
are passed through to the extractor.

### 2.3 Output Record

| Key | Type | Meaning |
| --- | --- | --- |
| `session_id` | str | session id, `ses_` prefix stripped |
| `timestamp` | str | ISO-8601 UTC from the turn filename |
| `file` | str | turn file name (chronology-proof) |
| `tool` | str | tool name from the extractor record |
| `index` | int | extractor's per-session global call index |
| `args` | dict | raw args of the matched call (unchanged) |
| `match` | list[str] | the matched `--path` tokens |

stdout carries ONLY the payload (JSONL by default; `--json` = JSON array);
diagnostics go to stderr.

***

## 3. CLI Contract (Stable)

```bash
python3 scripts/attribute-path-to-session.py \
    [--logs <dir>] [--session <id>] ... \
    --path <token> ... [--tool <name>] ... \
    [--since <ISO>] [--until <ISO>] [--json] [--output <file>]
```

| Flag | Required | Description |
| --- | --- | --- |
| `--logs` | No | logger logs dir; default = Base #2 discovery |
| `--session` | No | restrict sweep to this session id (repeatable) |
| `--path` | Yes | token that must appear in stringified args (repeatable) |
| `--tool` | No | filter turns to this tool (repeatable) |
| `--since` / `--until` | No | turn-filename time window (naive = UTC) |

### Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | at least one matching tool call found |
| 1 | no matches in the scanned calls |
| 2 | usage error, missing extractor, or logs dir absent |

Note the deliberate distinction: exit **2** for infrastructure problems —
callers must never mistake an uninstalled extractor for "no record".

***

## 4. Scripts

- [`scripts/attribute-path-to-session.py`](scripts/attribute-path-to-session.py)
  — Tier-1 Python CLI (stdlib + subprocess composition)

***

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`git-commit-dangling-link-audit`](../../git-commit-dangling-link-audit/SKILL.md) | drift gate: for each DANGLES target, runs this script with `--path <target-token>` to produce an evidence card (which session moved it) |

***

## Related Skills

| Skill | Relationship |
| --- | --- |
| [`opencode-current-session-id`](../opencode-current-session-id/SKILL.md) | sibling — resolves the ACTIVE session; attribution sweeps any session |
| [`session-full-change-audit`](../../session-full-change-audit/SKILL.md) | sibling — answers "what changed"; attribution adds WHO/WHEN |
| [`scratch-artifact-naming`](../../general/file/scratch-artifact-naming/SKILL.md) | evidence cards typically land in a session-scoped scratch dir |

***

## 7. Traceability

- Origin: incident — a `mv`-based reorder of `planning-artifact-*` files, discovered ad-hoc via
  logger YAML forensics.
- Created 2026-08-08

***

## 8. Changelog

See [CHANGELOG.md](CHANGELOG.md).
