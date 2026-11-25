---
name: opencode-session-bash-write-extractor
description: Base — extract file writes from Tool: bash command strings in opencode session exports, parsing cat >/>> heredoc patterns; domain-agnostic primitive for recovering files created via shell.
category: Meta-Automation
---

# OpenCode Session Bash Write Extractor Skill

> **Skill ID:** `opencode-session-bash-write-extractor`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Extract file-write operations from `Tool: bash` command strings in
opencode session export markdown files. This is a **domain-agnostic base
primitive** — it parses the session markdown, locates `**Tool: bash**`
blocks, and scans the `command` string for heredoc file writes matching
`cat >` or `cat >>` patterns.

**Supported patterns:**

- `cat > /path/to/file << 'DELIMITER'\n<content>\nDELIMITER` — create/overwrite
- `cat >> /path/to/file << 'DELIMITER'\n<content>\nDELIMITER` — append
- `cat > file << 'DELIM'\n...\nDELIM\nchmod +x file` — create + chmod

**Known limitations (not supported):**

- `python3 -c "open().write()"` inline scripts
- `echo > file`, `printf > file` patterns
- Multi-command chains where `>` appears in non-heredoc context
- Heredocs without quoted delimiters (e.g., `<< EOF` without quotes)

## Supersession

This skill is superseded for general bash file-operation detection by the
2-layer pipeline:

1. [`opencode-session-bash-block-extractor`](../opencode-session-bash-block-extractor/SKILL.md) —
   extracts raw command strings from ANY `Tool: bash` block
2. [`opencode-session-bash-file-ops-classifier`](../opencode-session-bash-file-ops-classifier/SKILL.md) —
   classifies command strings into write, delete, copy, move, or other

The modern pipeline covers `rm`, `cp`, `mv`, and `git` variants in
addition to heredoc writes. This skill's scripts are preserved for
backward compatibility — [`file-recovery-from-session`](../file-recovery-from-session/SKILL.md)
still consumes this skill directly for write recovery (it does NOT need
the broader audit capability).

**Composition**: Consumed by `file-recovery-from-session` (composer) for
recovering bash-created files. Could be reused for auditing shell-based
file operations in sessions.

## Composition Rationale

This primitive exists as its own base skill for historical and practical
reasons. While the broader 2-stage pipeline
(`opencode-session-bash-block-extractor` →
`opencode-session-bash-file-ops-classifier`) supersedes it for general
bash file-op detection, this skill's heredoc-specific regex is more
precise for its narrow purpose — it extracts the actual file content
from heredoc blocks, which the general pipeline does not do.
`file-recovery-from-session` consumes this skill directly because
recovery needs the content, not just the operation classification.

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
- **Optional file pattern**: Glob to filter writes by `filePath`
- **Optional mode filter**: `overwrite`, `append`, or `all` (default)

### Processing

1. Read session file as UTF-8 text
2. Locate all `**Tool: bash**` blocks with JSON input
3. For each block, parse `command` string from JSON
4. Apply regex: `cat\s+(>|>>)\s+(\S+)\s*<<\s*'(\w+)'\s*\n(.*?)\n\3`
   (DOTALL, multiline)
5. For each match, extract:
   - Operation: `overwrite` (`>`) or `append` (`>>`)
   - Target path: captured group 2 (resolved to absolute path)
   - Content: captured group 4 (lines between heredoc markers)
6. If `--mode` is `overwrite` or `append`, filter by operation type
7. If `--file-pattern` provided, filter by fnmatch on `filePath`
8. Emit each matching write as a JSONL line

### JSONL Output Format

Each line is a JSON object with three keys:

```json
{"filePath": "/absolute/path/to/file.py", "content": "file contents...", "mode": "overwrite"}
```

### CLI Contract

```bash
python3 scripts/extract-bash-writes.py --session <path> [--file-pattern <glob>] [--mode overwrite|append|all] [--output <path>]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--session` | Yes | Path to opencode session export (.md) |
| `--file-pattern` | No | Glob pattern to filter writes by filePath |
| `--mode` | No | Filter by operation: `overwrite`, `append`, or `all` (default: `all`) |
| `--output` | No | Write JSONL to file instead of stdout |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — at least one write operation extracted |
| 1 | No matching write operations found |
| 2 | Parse error reading session file |
| 3 | Session file not found |

## Composition by Higher-Level Skills

| Composer Skill | Purpose |
|----------------|---------|
| `file-recovery-from-session` | Extract bash writes → write to disk → verify content |
| `session-full-change-audit` | Include bash heredoc writes in unified change audit → mergeable JSONL with `_source: "bash-write"` |

## Scripts

- [`scripts/extract-bash-writes.py`](scripts/extract-bash-writes.py) —
  Tier-1 Python CLI (see
  [Scripting Language Selection Rules §3.1](../../../ai-agent-rules/scripting-language-selection-rules.md))

## Related Skills

- [`opencode-session-write-extractor`](../opencode-session-write-extractor/SKILL.md) —
  Parallel base skill for `Tool: write` payload extraction
- [`opencode-session-edit-extractor`](../opencode-session-edit-extractor/SKILL.md) —
  Parallel base skill for `Tool: edit` payload extraction
- [`opencode-session-bash-block-extractor`](../opencode-session-bash-block-extractor/SKILL.md) —
  Upstream block extractor; combined with
  `opencode-session-bash-file-ops-classifier` supersedes this skill for
  general bash file-op detection
- [`opencode-session-bash-file-ops-classifier`](../opencode-session-bash-file-ops-classifier/SKILL.md) —
  Superseding classifier (paired with bash-block-extractor)
- [`file-recovery-from-session`](../file-recovery-from-session/SKILL.md) —
  Composer that consumes this skill for bash-heredoc file recovery
- [`session-full-change-audit`](../session-full-change-audit/SKILL.md) —
  Composer that includes this skill's output in unified change audits

## Traceability

- Origin: 2026-07-04 — alongside the write/edit extractors, during the file-recovery skills
  full-scope expansion

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

Internal use — OleoVista Aceros workspace.
