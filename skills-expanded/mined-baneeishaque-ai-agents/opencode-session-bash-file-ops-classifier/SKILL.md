---
name: opencode-session-bash-file-ops-classifier
description: Base — classify bash command strings (from `opencode-session-bash-block-extractor`) into file operation types: write, append, delete, copy, move, other.
category: Meta-Automation
---

# OpenCode Session Bash File Ops Classifier (v1)

> **Skill ID:** `opencode-session-bash-file-ops-classifier`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Classify bash command strings into file operation types.

Reads JSONL input (one `{"command": "..."}` per line) from
[`opencode-session-bash-block-extractor`](../opencode-session-bash-block-extractor/SKILL.md)
or any source producing the same format. Outputs one JSONL line per
classified file operation with structured metadata.

**Detected operation types:**

| Type | Patterns matched |
|---|---|
| `overwrite` | `cat > /path << 'DELIM'\n...\nDELIM` |
| `append` | `cat >> /path << 'DELIM'\n...\nDELIM` |
| `delete` | `rm`, `rm -rf`, `rm -f`, `git rm` |
| `copy` | `cp` (with or without `-r`) |
| `move` | `mv`, `git mv` |
| `other` | Any command not matching the above |

## Composition Rationale

This skill is a domain-agnostic base primitive — it classifies ANY bash
command string, not just those from OpenCode sessions. Downstream
composers use it for session auditing, CI pipeline analysis, and
security reviews.

## Environment & Dependencies

| Requirement | Minimum | Verification |
|---|---|---|
| Python | 3.12+ | `python3 --version` |

## Operational Logic

### Input

JSONL from stdin or `--input` file, each line:

```json
{"command": "rm -rf /tmp/foo"}
```

### Processing

1. For each input line, extract the `command` field
2. Apply regex dispatch in this order:
   - **Heredoc patterns** (`cat >/>>`): one result per heredoc block
   - **Delete patterns** (`rm`, `git rm`): extract target path
   - **Copy patterns** (`cp`): extract source and target paths
   - **Move patterns** (`mv`, `git mv`): extract source and target paths
   - **Fallback**: classify as `other`
3. Apply optional `--operation` filter
4. Emit filtered results as JSONL

### JSONL Output Format

```json
{
  "command": "cat > /tmp/foo << 'EOF'\nhello\nEOF",
  "operation": "overwrite",
  "target": "/tmp/foo",
  "source": null,
  "content": "hello"
}
```

For `delete`/`copy`/`move` operations, `content` is `null`. For `other`,
all of `target`, `source`, `content` are `null`.

### CLI Contract

```bash
# Pipe from block extractor:
python3 scripts/extract-bash-blocks.py --session <path> \
  | python3 scripts/classify-bash-file-ops.py [--operation <type>]

# Or read from file:
python3 scripts/classify-bash-file-ops.py --input ops.jsonl
```

| Flag | Required | Description |
|---|---|---|
| `--input` | No | JSONL input file (default: stdin) |
| `--operation` | No | Filter: write, append, overwrite, delete, copy, move, other, all (default: all) |
| `--output` | No | Write JSONL to file instead of stdout |

### Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success — at least one file operation classified |
| 1 | No file operations found after filtering |
| 2 | Parse error reading input |
| 3 | Input file not found |

## Scripts

- [`scripts/classify-bash-file-ops.py`](scripts/classify-bash-file-ops.py) —
  Tier-1 Python CLI

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`session-file-ops-audit`](../session-file-ops-audit/SKILL.md) | Pipes block extractor output → classifier → formats as human-readable report |
| [`session-full-change-audit`](../session-full-change-audit/SKILL.md) | Pipes block extractor output → classifier → merges into unified JSONL stream alongside write/edit/bash-write payloads |

## Related Skills

- [`opencode-session-bash-block-extractor`](../opencode-session-bash-block-extractor/SKILL.md) —
  Upstream block extractor (produces the JSONL this skill consumes)
- [`opencode-session-bash-write-extractor`](../opencode-session-bash-write-extractor/SKILL.md) —
  Superseded predecessor (limited to heredoc writes only)
- [`opencode-session-path-attribution`](../opencode/opencode-session-path-attribution/SKILL.md) —
  sibling — attribution consumes classified-op evidence (move/delete cards)

## Supersession

This skill, combined with
[`opencode-session-bash-block-extractor`](../opencode-session-bash-block-extractor/SKILL.md),
supersedes `opencode-session-bash-write-extractor` for detecting ALL bash
file operations, not just heredoc writes. See
[`opencode-session-bash-write-extractor/SKILL.md`](../opencode-session-bash-write-extractor/SKILL.md#supersession)
for details.

## Traceability

- Origin: Layer 2 of a 3-layer architecture
- Created 2026-07-04

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

Internal use — OleoVista Aceros workspace.
