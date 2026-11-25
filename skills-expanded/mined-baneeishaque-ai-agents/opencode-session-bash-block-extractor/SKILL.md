---
name: opencode-session-bash-block-extractor
description: Base — extract raw Tool: bash command strings from opencode session exports; domain-agnostic primitive for any bash-analysis workflow.
category: Meta-Automation
---

# OpenCode Session Bash Block Extractor (v1)

> **Skill ID:** `opencode-session-bash-block-extractor`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Extract raw `Tool: bash` command strings from opencode session export
markdown files. This is a **domain-agnostic base primitive** — it only
finds bash blocks and extracts the `command` field from each block's
JSON input. It does NOT classify or interpret the command.

**This skill does ONE thing**: given a session markdown file, produce
one JSONL line per `Tool: bash` block containing the raw command string.
Classification of what the command does (write, delete, copy, move)
belongs in a downstream skill.

## Composition Rationale

This primitive was extracted as its own base skill because multiple
downstream classifiers and composers need to parse `Tool: bash` blocks
from session exports. Previously each bash-analysis skill reimplemented
the same regex — this skill is the Single Source of Truth for finding
bash blocks in OpenCode session markdown.

Downstream consumers:

| Composer | Consumption Mechanism |
|---|---|
| [`opencode-session-bash-file-ops-classifier`](../opencode-session-bash-file-ops-classifier/SKILL.md) | Reads JSONL stdout from this skill's `extract-bash-blocks.py` via pipe or `--input` |
| [`session-file-ops-audit`](../session-file-ops-audit/SKILL.md) | Shells out to this skill's script, pipes output into the classifier |

## Environment & Dependencies

| Requirement | Minimum | Verification |
|---|---|---|
| Python | 3.12+ | `python3 --version` |
| opencode CLI | session export format v1 | N/A (parses exported markdown) |

## Operational Logic

### Input

- **Session file**: Path to opencode session export (`.md` format)

### Processing

1. Read session file as UTF-8 text
2. Locate all `**Tool: bash**` blocks with JSON input via regex
3. Parse each block's JSON and extract the `command` field
4. Emit each matching command as a JSONL line

### JSONL Output Format

Each line is a JSON object with one key:

```json
{"command": "cat > /path/to/file << 'EOF'\n...\nEOF"}
```

### CLI Contract

```bash
python3 scripts/extract-bash-blocks.py --session <path> [--output <path>]
```

| Flag | Required | Description |
|---|---|---|
| `--session` | Yes | Path to opencode session export (.md) |
| `--output` | No | Write JSONL to file instead of stdout |

### Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success — at least one bash block extracted |
| 1 | No bash blocks found |
| 2 | Parse error reading session file |
| 3 | Session file not found |

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`opencode-session-bash-file-ops-classifier`](../opencode-session-bash-file-ops-classifier/SKILL.md) | Reads JSONL from this skill's stdout; classifies each command string into a file operation type |
| [`session-file-ops-audit`](../session-file-ops-audit/SKILL.md) | Invokes this skill's script FIRST; pipes the output into the classifier, then formats the result as a human-readable report |
| [`session-full-change-audit`](../session-full-change-audit/SKILL.md) | Invokes this skill's script as first stage of 2-stage bash pipeline; pipes output into classifier, then merges into unified JSONL stream |

## Scripts

- [`scripts/extract-bash-blocks.py`](scripts/extract-bash-blocks.py) —
  Tier-1 Python CLI (see
  [Scripting Language Selection Rules §3.1](../../../ai-agent-rules/scripting-language-selection-rules.md))

## Related Skills

- [`opencode-session-bash-file-ops-classifier`](../opencode-session-bash-file-ops-classifier/SKILL.md) —
  Downstream classifier that consumes this skill's output
- [`opencode-session-bash-write-extractor`](../opencode-session-bash-write-extractor/SKILL.md) —
  Superseded predecessor (hand-wrote its own bash-block regex)

## Traceability

- Origin: 2026-07-04 — during session-bash-file-ops-extractor-suite expansion
- Created as Layer 1 of a 3-layer architecture

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

Internal use — OleoVista Aceros workspace.
