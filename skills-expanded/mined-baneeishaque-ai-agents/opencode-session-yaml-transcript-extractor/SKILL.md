---
name: opencode-session-yaml-transcript-extractor
description: >-
  Extract the per-turn transcript (session header, user text, assistant
  thinking, tool calls) from opencode logger-plugin YAML session logs as
  chronological JSONL with global index and turn identity.
category: Base-Utility
---

# OpenCode Session YAML Transcript Extractor (v1)

## Composition Rationale

This skill is a **base primitive**: it owns the deterministic
YAML-log → per-turn transcript extraction logic (layout discovery,
multi-document parsing, turn grouping, chronological ordering,
field truncation). It is the **superset** of the sibling
[`opencode-session-yaml-tool-call-extractor`](../opencode-session-yaml-tool-call-extractor/SKILL.md):
in addition to tool calls it emits the `user_text` and `thinking`
records that make problem identification, rejected-path detection, and
workflow reconstruction possible in downstream analysis composers.

It was extracted as its own skill because tool-call-only extraction is
insufficient for session *analysis* — a composer reconstructing
"problem → solution → executed workflow" needs the full narrative, and
any future analysis domain (summarization, debugging forensics, fidelity
scans, acceptance-criteria checks) needs the same primitive. Inlining it
into one composer would split the SSOT.

It is a **parallel base** to `opencode-session-yaml-tool-call-extractor`
(both parse the same layouts independently; the transcript base does NOT
shell out to the tool-call base because it needs per-turn context the
tool-call JSONL contract does not carry).

***

## 1. Environment & Dependencies

| Requirement | Minimum | Verification |
| --- | --- | --- |
| Python | 3.11+ (3.12 recommended) | `python3 --version` |
| PyYAML | any | `python3 -c "import yaml"` |

PyYAML is the only third-party dependency (PEP 723 / pip or system
package manager). The script imports `yaml` at module top; a missing
package produces an exit-2 diagnostic — install it with
`python3 -m pip install pyyaml` or the system package manager before use.

***

## 2. Operational Logic

### 2.1 Input Layouts

The opencode logger plugin writes two YAML layouts, both accepted by
`--input`:

| Layout | Path | Content |
| --- | --- | --- |
| Monolithic | `.opencode/logs/ses_<id>.yaml` | Multi-document YAML (`---` separated): doc 1 = session header (`session:` key); docs 2..N = turns |
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

A turn document carries BOTH the `user:` block and the `assistant:`
block in the SAME YAML document. `assistant` and `tool_calls` are lists
but may appear as a single dict — both shapes are normalized. Turns
without tool calls still emit their `user_text` / `thinking` records —
narrative elements MUST NOT be dropped.

### 2.3 Output Record

One JSONL record per narrative element, chronological order:

```json
{"index": 0, "turn": -1, "kind": "session_header", "id": "ses_...", "title": "..."}
{"index": 1, "turn": 0, "kind": "user_text", "role": "user", "text": "...", "time": "..."}
{"index": 2, "turn": 0, "kind": "thinking", "role": "assistant", "text": "..."}
{"index": 3, "turn": 0, "kind": "tool_call", "role": "assistant", "tool": "bash", "args": {...}, "result": "..."}
```

| Key | Type | Meaning |
| --- | --- | --- |
| `index` | int | Global 0-based counter across the whole session |
| `turn` | int | Per-turn ordinal; `-1` for the session header record |
| `kind` | str | `session_header` \| `user_text` \| `thinking` \| `tool_call` |
| `role` | str | `user` \| `assistant` (absent on `session_header`) |
| `tool` | str | Tool name (`write`, `edit`, `bash`, `skill`, ...) — `tool_call` only |
| `args` | dict or str | Raw tool arguments; a truncated JSON string when `--truncate` is active |
| `result` | str | Raw tool result text (may be large) |
| `text` | str | User message or thinking body |
| `time` | str | Optional per-message timestamp when present in the YAML |

### 2.4 Filter Semantics

- `--kind` filters record kinds; a `session_header` record is emitted
  only when `--kind session_header` is passed (or no `--kind`).
- `--tool` filters `tool_call` records only; `user_text` / `thinking`
  records always pass through (they carry the context for the tool
  calls). This lets a composer request "bash only" while keeping the
  narrative.
- `--truncate N` truncates `text`, `args` (JSON-dumped), and `result`
  to N chars with a `<truncated ...>` marker; `args` becomes a JSON
  string instead of an object when truncation is active.

***

## 3. CLI Contract (Stable)

```bash
python3 scripts/extract-yaml-transcript.py --input <path> \
    [--kind user_text|thinking|tool_call|session_header] \
    [--tool <name>] [--truncate <N>] [--output <file>]
```

| Flag | Required | Description |
| --- | --- | --- |
| `--input` | Yes | Monolithic `.yaml` file OR per-turn directory of `NNN-*.yaml` files |
| `--kind` | No | Record kind filter (repeatable) |
| `--tool` | No | Tool name filter for `tool_call` records (repeatable) |
| `--truncate` | No | Truncate `text` / `args` / `result` fields to N chars |
| `--output` | No | Write JSONL to file instead of stdout |

### Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | Success — at least one record found |
| 1 | No records found matching criteria |
| 2 | Parse failure (YAML error) or missing PyYAML |
| 3 | Input path not found |

### Output Semantics

- stdout carries ONLY the JSONL payload (no diagnostics) — safe to pipe
- Informational messages go to stderr (`Found N record(s)`)
- Malformed YAML in one file logs a stderr warning and continues
- Records are emitted with `ensure_ascii=False`

***

## 4. Scripts

- [`scripts/extract-yaml-transcript.py`](scripts/extract-yaml-transcript.py) —
  Tier-1 Python CLI (stdlib + PyYAML)

***

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`opencode-session-problem-solution-workflow-analysis`](../opencode-session-problem-solution-workflow-analysis/SKILL.md) | Consumes this base FIRST: shells out to `scripts/extract-yaml-transcript.py --input <session> --truncate <N>` via subprocess, parses the stdout JSONL, and formats the per-turn chronology (user text, thinking, tool calls) into its report skeleton at its step 1. |

***

## Related Skills

| Skill | Relationship |
| --- | --- |
| [`opencode-session-path-attribution`](../opencode-session-path-attribution/SKILL.md) | Sibling consumer of the same YAML layouts — cross-session path forensics |
| [`opencode-current-session-id`](../opencode-current-session-id/SKILL.md) | Sibling — resolves the CURRENT session ID/title from the same logs (different primitive) |
| [`opencode-session-diff-extractor`](../../opencode-session-diff-extractor/SKILL.md) | Parallel base — parses git-diff blocks from `.md` session exports (different input format) |
| [`opencode-session-yaml-conversation-extractor`](../opencode-session-yaml-conversation-extractor/SKILL.md) | Parallel base — emits conversation-only YAML (user.text + assistant.response, agent iff compaction) with structure-preserving round-trip; drops thinking/tool_calls |

***

## 7. Traceability

- Origin: created as the base layer for the opencode-session problem/solution/workflow analysis composer; the
  script logic generalizes the ad-hoc summarizer + narrative dumper scripts used during the source
  analysis (2026-08-05).
- Source of truth for the YAML layout: the opencode logger-plugin artifacts
  under `.opencode/logs/`
- Created 2026-08-11

***

## 8. Changelog

See [CHANGELOG.md](CHANGELOG.md).
