---
name: opencode-session-write-extractor
description: Base — extract Tool: write JSON payloads (filePath + content) from opencode session export markdown files; domain-agnostic primitive for any file recovery workflow.
category: Meta-Automation
---

# OpenCode Session Write Extractor Skill

> **Skill ID:** `opencode-session-write-extractor`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Extract `Tool: write` JSON payloads from opencode session export files
(markdown format with tool call/response structure). This is a
**domain-agnostic base primitive** — it knows nothing about any specific
file. It parses the session markdown, locates tool invocations where
`**Tool: write**` is used, and emits the `filePath` + `content` pairs
as JSONL to stdout or a file.

**Composition**: Consumed by `file-recovery-from-session` (composer) for
recovering written files. Could be reused for any purpose involving
`Tool: write` payload extraction (e.g., auditing, diffing, CI checks).

## Composition Rationale

This primitive exists as its own base skill because `Tool: write` is a
distinct payload type in the OpenCode session export format — it carries
`filePath` + `content` directly, without the indirection of a shell
command. Multiple downstream consumers (recovery, audit, CI) need to
parse these payloads independently, so a shared SSOT prevents regex
drift across consumers.

## Environment & Dependencies

| Requirement | Minimum | Verification |
|-------------|---------|--------------|
| Python | 3.12+ | `python3 --version` |
| opencode CLI | session export format v1 | N/A (parses exported markdown) |

```bash
python3 --version
```

## Operational Logic

### Input

- **Session file**: Path to opencode session export (`.md` format)
- **Optional file pattern**: Glob to filter write payloads by `filePath`
  (e.g., `**/implementation-plans/*.md`, `*.json`)

### Processing

1. Read session file as UTF-8 text
2. Split into top-level sections by `---` separator
3. For each section containing `**Tool: write**`:
   4. Locate `**Input:**` followed by a `` ```json `` code fence
   5. Extract the JSON text between the opening and closing fences
   6. Parse JSON, extract `filePath` and `content`
   7. If `--file-pattern` provided, filter by fnmatch on `filePath`
   8. Emit each matching payload as a JSONL line

### JSONL Output Format

Each line is a JSON object with exactly two keys:

```json
{"filePath": "/absolute/path/to/file.md", "content": "file contents here..."}
```

### CLI Contract

```bash
python3 scripts/extract-session-writes.py (--session <path> | --yaml <path>) [--file-pattern <glob>] [--output <path>]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--session` | One of | Path to opencode session export (.md) |
| `--yaml` | One of | Path to opencode logger-plugin YAML log (monolithic `.yaml` file OR per-turn `ses_<id>/` directory) — extracts `Tool: write` calls via the `opencode-session-yaml-tool-call-extractor` base skill |
| `--file-pattern` | No | Glob pattern to filter write payloads by filePath |
| `--output` | No | Write JSONL to file instead of stdout |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — at least one write payload extracted |
| 1 | No write payloads found matching criteria |
| 2 | Parse error reading session file |
| 3 | Session file not found |

## Composition by Higher-Level Skills

| Composer Skill | Purpose |
|----------------|---------|
| `file-recovery-from-session` | Extract write payloads → write to disk → verify content |
| `session-full-change-audit` | Include write payloads in unified change audit → mergeable JSONL with `_source: "write"` |

## Scripts

- [`scripts/extract-session-writes.py`](scripts/extract-session-writes.py) —
  Tier-1 Python CLI (see
  [Scripting Language Selection Rules §3.1](../../../ai-agent-rules/scripting-language-selection-rules.md))

## Related Skills

- [`opencode-session-edit-extractor`](../opencode-session-edit-extractor/SKILL.md) —
  Parallel base skill for `Tool: edit` payload extraction
- [`opencode-session-diff-extractor`](../opencode-session-diff-extractor/SKILL.md) —
  Parallel base skill for git diff extraction from session exports
- [`opencode-session-bash-write-extractor`](../opencode-session-bash-write-extractor/SKILL.md) —
  Parallel base skill for bash heredoc file writes
- [`file-recovery-from-session`](../file-recovery-from-session/SKILL.md) —
  Composer that consumes this skill for file recovery
- [`session-full-change-audit`](../session-full-change-audit/SKILL.md) —
  Composer that includes this skill's output in unified change audits

## Traceability

- Origin: 2026-07-04 — recovery of `2026-07-03-document-uptimerobot-mcp-workflow.md` after accidental deletion

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

Internal use — OleoVista Aceros workspace.
