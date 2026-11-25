---
name: opencode-session-yaml-tool-call-extractor
description: >-
  Base — extract every assistant tool call (tool, args, result) from opencode
  logger-plugin YAML logs (monolithic ses_<id>.yaml OR per-turn ses_<id>/
  directory of NNN-*.yaml files) as chronological JSONL; domain-agnostic
  primitive for any YAML-log analysis or file-change recovery workflow.
category: OpenCode
---

# OpenCode Session YAML Tool-Call Extractor (v1)

## Composition Rationale

This skill is a **base primitive**: it owns ONLY the deterministic
YAML-log → tool-call extraction logic (layout discovery, multi-document
parsing, chronological ordering) that the file-changes extractor family
reuses. It was extracted because five sibling extractors
(`opencode-session-write-extractor`, `opencode-session-edit-extractor`,
`opencode-session-bash-block-extractor`,
`opencode-session-bash-file-ops-classifier`,
`opencode-session-bash-write-extractor`) each need to find
`tool_calls` inside the opencode logger-plugin YAML artifacts;
inlining that parse into every consumer would duplicate the SSOT and
silently diverge bug fixes.

Composers shell out to `scripts/extract-yaml-tool-calls.py` and consume
its stdout JSONL contract. See the `## Composition by Higher-Level Skills`
table for the exact mechanism per consumer.

***

## 1. Environment & Dependencies

| Requirement | Minimum | Verification |
| --- | --- | --- |
| Python | 3.12+ | `python3 --version` |
| PyYAML | any | `python3 -c "import yaml"` |

PyYAML is the only third-party dependency (PEP 723 / pip or system
package manager). The script imports `yaml` at module top; a missing
package produces a traceback — install it with
`python3 -m pip install pyyaml` or the system package manager before use.

***

## 2. Operational Logic

### 2.1 Input Layouts

The opencode logger plugin writes two YAML layouts, both accepted by
`--input`:

| Layout | Path | Content |
| --- | --- | --- |
| Monolithic | `.opencode/logs/ses_<id>.yaml` | Multi-document YAML (`---` separated): doc 1 = session header (`session:` key); docs 2..N = turns (`user:` / `assistant:`) |
| Per-turn directory | `.opencode/logs/ses_<id>/` | One file per turn: `000-header-*.yaml` + `NNN-<timestamp>.yaml`; filename order = chronological order |

### 2.2 Turn Schema

```yaml
---
user:
  text: |-
    ...
  time: ...
assistant:
  - agent: build
    model: {id: ..., provider: ...}
    thinking: |-
    tool_calls:
      - tool: write
        args: {filePath: ..., content: ...}
        result: |-
```

`assistant` and `tool_calls` are lists but may appear as a single dict —
both shapes are normalized. Turns without `tool_calls` are skipped.

### 2.3 Output Record

One JSONL record per tool call, chronological order
(per-turn file order, then in-list order):

```json
{"index": 0, "tool": "bash", "args": {"command": "..."}, "result": "..."}
```

| Key | Type | Meaning |
| --- | --- | --- |
| `index` | int | Global 0-based tool-call counter across the whole session |
| `tool` | str | Tool name (`write`, `edit`, `bash`, `skill`, ...) |
| `args` | dict | Raw tool arguments (unchanged from YAML) |
| `result` | str | Raw tool result text (may be large) |

***

## 3. CLI Contract (Stable)

```bash
python3 scripts/extract-yaml-tool-calls.py --input <path> \
    [--tool write] [--tool edit] [--output <file>]
```

| Flag | Required | Description |
| --- | --- | --- |
| `--input` | Yes | Monolithic `.yaml` file OR per-turn directory of `NNN-*.yaml` files |
| `--tool` | No | Filter to one tool name (repeatable) |
| `--output` | No | Write JSONL to file instead of stdout |

### Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | Success — at least one tool call found |
| 1 | No tool calls found matching criteria |
| 2 | Parse failure (YAML error, read error) |
| 3 | Input path not found |

### Output Semantics

- stdout carries ONLY the JSONL payload (no diagnostics) — safe to pipe
- Informational messages go to stderr (`Found N tool call(s)`, warnings)
- Malformed YAML in one file logs a stderr warning and continues
- Records are emitted with `ensure_ascii=False`

***

## 4. Scripts

- [`scripts/extract-yaml-tool-calls.py`](scripts/extract-yaml-tool-calls.py) —
  Tier-1 Python CLI (stdlib + PyYAML)

***

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`opencode-session-write-extractor`](../../opencode-session-write-extractor/SKILL.md) | `--yaml` mode runs this script with `--tool write`, consumes `args.filePath` + `args.content`, emits its `{filePath, content}` JSONL contract |
| [`opencode-session-edit-extractor`](../../opencode-session-edit-extractor/SKILL.md) | `--yaml` mode runs this script with `--tool edit`, consumes `args.filePath` + `args.oldString` + `args.newString`, emits its `{filePath, oldString, newString}` JSONL contract |
| [`opencode-session-bash-block-extractor`](../../opencode-session-bash-block-extractor/SKILL.md) | `--yaml` mode runs this script with `--tool bash`, consumes `args.command`, emits its command-list JSONL contract |
| [`opencode-session-bash-write-extractor`](../../opencode-session-bash-write-extractor/SKILL.md) | `--yaml` mode runs this script with `--tool bash`, consumes `args.command`, runs its heredoc parser on each command |
| [`session-full-change-audit`](../../session-full-change-audit/SKILL.md) | `--yaml` mode passes the YAML input through this script once, then dispatches the JSONL records to the four extractor pipelines above |
| [`opencode-session-path-attribution`](../opencode-session-path-attribution/SKILL.md) | per-turn-file subprocess consumer — sweeps every turn file via this script and matches path tokens on the stringified args |

***

## Related Skills

| Skill | Relationship |
| --- | --- |
| [`opencode-current-session-id`](../opencode-current-session-id/SKILL.md) | Sibling in the `opencode/` group — resolves the current session ID/title from the same logger logs |
| [`opencode-session-path-attribution`](../opencode-session-path-attribution/SKILL.md) | Consumer — sweeps every turn file through this skill's CLI for cross-session path forensics |
| [`opencode-installed-plugin-lookup`](../opencode-installed-plugin-lookup/SKILL.md) | Sibling — locates the logger plugin and its logs convention before extraction |
| [`opencode-session-diff-extractor`](../../opencode-session-diff-extractor/SKILL.md) | Parallel base skill — parses git-diff blocks from `.md` session exports (not present in YAML logs) |
| [`opencode-session-yaml-transcript-extractor`](../opencode-session-yaml-transcript-extractor/SKILL.md) | Parallel base skill — per-turn transcript JSONL (user text + thinking + tool calls) over the same YAML layouts; this skill's superset |
| [`opencode-session-problem-solution-workflow-analysis`](../opencode-session-problem-solution-workflow-analysis/SKILL.md) | Sibling composer — reconstructs problem/solution/executed-workflow reports over the transcript base (adjacent analysis domain) |
| [`jsonl-content-extractor`](../../jsonl-content-extractor/SKILL.md) | Parallel base skill — key-path extraction over JSONL (different input format) |

***

## 7. Traceability

- Origin: created as Phase A of the YAML-log upgrade for the file-changes
  audit skill family
- Source of truth for the YAML layout: the opencode logger-plugin artifacts
  under `.opencode/logs/`
- Created 2026-07-31

***

## 8. Changelog

See [CHANGELOG.md](CHANGELOG.md).
