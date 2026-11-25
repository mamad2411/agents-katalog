---
name: opencode-session-edit-extractor
description: Base — extract Tool: edit JSON payloads (filePath, oldString, newString) from opencode session export markdown files; domain-agnostic primitive for any edit-recovery or audit workflow.
category: Meta-Automation
---

# OpenCode Session Edit Extractor Skill

> **Skill ID:** `opencode-session-edit-extractor`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Extract `Tool: edit` JSON payloads from opencode session export files
(markdown format with tool call/response structure). This is a
**domain-agnostic base primitive** — it knows nothing about any specific
file. It parses the session markdown, locates tool invocations where
`**Tool: edit**` is used, and emits the `filePath`, `oldString`, and
`newString` values as JSONL to stdout or a file.

**Composition**: Consumed by `edit-application-from-session` (composer)
for applying edits to existing files. Could be reused for auditing edit
history, comparing old vs new content, or CI checks.

## Composition Rationale

This primitive exists as its own base skill because `Tool: edit` is a
distinct payload type in the OpenCode session export format — it carries
`filePath` + `oldString` + `newString`, which requires different parsing
from `Tool: write` or `Tool: bash` blocks. Separating edit extraction
from write extraction allows each parser to remain simple and lets
downstream consumers (edit-replay, audit, diff) reuse the same SSOT.

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
- **Optional file pattern**: Glob to filter edit payloads by `filePath`
  (e.g., `**/AGENTS.md`, `*.json`)

### Processing

1. Read session file as UTF-8 text
2. Split into top-level sections by `---` separator
3. For each section containing `**Tool: edit**`:
   4. Locate `**Input:**` followed by a `` ```json `` code fence
   5. Extract the JSON text between the opening and closing fences
   6. Parse JSON, extract `filePath`, `oldString`, and `newString`
   7. If `--file-pattern` provided, filter by fnmatch on `filePath`
   8. Emit each matching payload as a JSONL line

### JSONL Output Format

Each line is a JSON object with exactly three keys:

```json
{"filePath": "/absolute/path/to/file.md", "oldString": "existing text...", "newString": "replacement text..."}
```

### CLI Contract

```bash
python3 scripts/extract-session-edits.py --session <path> [--file-pattern <glob>] [--output <path>]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--session` | Yes | Path to opencode session export (.md) |
| `--file-pattern` | No | Glob pattern to filter edit payloads by filePath |
| `--output` | No | Write JSONL to file instead of stdout |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — at least one edit payload extracted |
| 1 | No edit payloads found matching criteria |
| 2 | Parse error reading session file |
| 3 | Session file not found |

## Composition by Higher-Level Skills

| Composer Skill | Purpose |
|----------------|---------|
| `edit-application-from-session` | Extract edit payloads → apply to existing files → verify |
| `session-full-change-audit` | Include edit payloads in unified change audit → mergeable JSONL with `_source: "edit"` |

## Scripts

- [`scripts/extract-session-edits.py`](scripts/extract-session-edits.py) —
  Tier-1 Python CLI (see
  [Scripting Language Selection Rules §3.1](../../../ai-agent-rules/scripting-language-selection-rules.md))

## Related Skills

- [`opencode-session-write-extractor`](../opencode-session-write-extractor/SKILL.md) —
  Parallel base skill for `Tool: write` payload extraction
- [`opencode-session-bash-write-extractor`](../opencode-session-bash-write-extractor/SKILL.md) —
  Parallel base skill for bash heredoc file writes
- [`opencode-session-diff-extractor`](../opencode-session-diff-extractor/SKILL.md) —
  Parallel base skill for git diff extraction from session exports
- [`edit-application-from-session`](../edit-application-from-session/SKILL.md) —
  Composer that consumes this skill for applying edits
- [`session-full-change-audit`](../session-full-change-audit/SKILL.md) —
  Composer that includes this skill's output in unified change audits

## Traceability

- Origin: 2026-07-04 — extracted alongside the write-extractor, during the file-recovery skills audit

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

Internal use — OleoVista Aceros workspace.
