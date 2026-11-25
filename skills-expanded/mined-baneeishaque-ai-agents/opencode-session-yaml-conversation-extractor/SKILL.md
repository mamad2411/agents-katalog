---
name: opencode-session-yaml-conversation-extractor
description: >-
  Extract a conversation-only YAML transcript from opencode logger-plugin YAML
  session logs — keeps user.text and assistant[].response (plus agent only when
  compaction), drops thinking/tool_calls/model/time/duration, preserves YAML
  structure via ruamel.yaml round-trip. Parallel base to
  opencode-session-yaml-transcript-extractor (which emits all-fields JSONL).
category: Base-Utility
---

# OpenCode Session YAML Conversation Extractor (v1)

> **Skill ID:** `opencode-session-yaml-conversation-extractor`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Composition Rationale

This skill is a **base primitive**: it owns the deterministic
YAML-log → conversation-only-YAML extraction logic (layout discovery,
multi-document round-trip parsing, field filtering, conditional agent
retention, structure-preserving output). It is a **parallel base** to the existing all-fields YAML transcript
extractor: both parse the same opencode logger-plugin YAML layouts
independently, but they serve different contracts:

| | all-fields JSONL extractor (parallel base) | this skill |
| :--- | :--- | :--- |
| Output format | JSONL | YAML (structure-preserving) |
| Fields kept | ALL (header, user, thinking, tool_call) | conversation-only (user.text, assistant.response, agent iff compaction) |
| Library | PyYAML `safe_load` (structure-lossy) | ruamel.yaml round-trip (preserves comments, styles, ordering) |
| Consumer | analysis composers (problem/solution/workflow) | archival / readable-transcript use cases |

It was extracted as its own skill because the parallel all-fields
extractor's contract (all-fields JSONL for machine analysis) is
fundamentally incompatible with conversation-only structure-preserving
YAML: the two need different libraries, different field rules, and
different output shapes, and the parallel extractor already has a
composer (`opencode-session-problem-solution-workflow-analysis`) that
depends on its exact JSONL contract.

***

## 1. Environment & Dependencies

| Requirement | Minimum | Verification |
| :--- | :--- | :--- |
| Python | 3.11+ (3.12 recommended) | `python3 --version` |
| ruamel.yaml | any | `python3 -c "import ruamel.yaml"` |

ruamel.yaml (NOT PyYAML) is the only third-party dependency. PyYAML's
`safe_load_all` is structure-lossy and cannot preserve comments, scalar
styles, or key ordering — it is unsuitable for this skill's
structure-preserving contract. The script imports `ruamel.yaml` and
`ruamel.yaml.comments.CommentedMap` at module top; a missing package
produces an exit-2 diagnostic — install it with
`python3 -m pip install ruamel.yaml` or the system package manager before
use.

***

## 2. Operational Logic

### 2.1 Input Layouts

The opencode logger plugin writes two YAML layouts, both accepted by
`--input`:

| Layout | Path | Content |
| :--- | :--- | :--- |
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
    time: ...
    response: |-
    duration: ...
    duration_ms: ...
```

A turn document carries BOTH the `user:` block and the `assistant:`
block in the SAME YAML document. `assistant` and `tool_calls` are lists
but may appear as a single dict — both shapes are normalized.

### 2.3 Field Rules (conversation-only)

For each YAML document:

1. **Header document** (has `session:` key): pass through unchanged —
   keep `session` + `model` + `title` (structural identity: session id,
   creation timestamp, model, and title are useful archival metadata and
   are not user/response text).
2. **Turn document** (has `user:` and/or `assistant:`):
   - `user`: keep only `text`; drop `time`.
   - `assistant` (normalize list-or-dict to list): for each entry, build a
     new entry containing:
     - `agent` ONLY if `entry.get("agent") == "compaction"` (keep when
       compaction, drop when build)
     - `response` (the assistant's reply text)
     - ordering: `agent` (if present) BEFORE `response`
     - drop: `model`, `thinking`, `tool_calls`, `thinking_duration`,
       `thinking_duration_ms`, `time`, `duration`, `duration_ms`
     - **skip the entry entirely if it has no `response`** (entries that
       only produced tool calls with no textual reply are dropped)

### 2.4 Output Contract

- **Per-turn dir input**: for each `NNN-<ts>.yaml`, write
  `<NNN-<ts>>-transcript.yaml` into the output directory. Header file
  `000-header-*.yaml` → `000-header-*-transcript.yaml`.
- **Monolithic file input**: write one `<session-id>-transcript.yaml`
  (multi-document YAML, `---` separated) into the output directory.
- Structure is preserved via ruamel.yaml round-trip: comments, scalar
  styles, key ordering, and `---` separators are retained.
- **Derived artifacts**: every `*-transcript.yaml` file this skill writes is a
  DERIVED artifact. The source logs (`ses_<id>/NNN-<ts>.yaml`) remain the
  durable SSOT. Readers holding only a transcript path who need the source
  files (e.g. for machine analysis via
  [`opencode-session-yaml-transcript-extractor`](../opencode-session-yaml-transcript-extractor/SKILL.md)
  or
  [`opencode-session-yaml-tool-call-extractor`](../opencode-session-yaml-tool-call-extractor/SKILL.md))
  MUST resolve via
  [`opencode-session-transcript-to-source-resolve`](../opencode-session-transcript-to-source-resolve/SKILL.md).

***

## 3. CLI Contract (Stable)

```bash
python3 scripts/extract-yaml-conversation.py --input <path> \
    [--output-dir <dir>]
```

| Flag | Required | Description |
| :--- | :--- | :--- |
| `--input` | Yes | Monolithic `ses_<id>.yaml` file OR per-turn `ses_<id>/` directory of `NNN-*.yaml` files |
| `--output-dir` | No | Output directory. Default: `<input>/transcripts` (dir input) or `<input-dir>/transcripts` (file input) |

### Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | Success — at least one turn document processed |
| 1 | No turn documents found (header-only input) |
| 2 | Parse failure (YAML error) or missing ruamel.yaml |
| 3 | Input path not found |

### Output Semantics

- stdout: NOT used for payload — script writes files; brief diagnostics
  go to stderr only (`Written: <path>`, `Found N file(s)...`,
  warnings).
- ruamel.yaml round-trip settings: `typ="rt"`, `preserve_quotes=True`,
  `width=4096`, `indent(mapping=2, sequence=4, offset=2)`.

***

## 4. Scripts

- [`scripts/extract-yaml-conversation.py`](scripts/extract-yaml-conversation.py) —
  Tier-1 Python CLI (stdlib + ruamel.yaml). See scripting-language-selection-rules.md
  intro (Tier 1 default) +  4 (YAML/JSON data manipulation).

```bash
python3 scripts/extract-yaml-conversation.py \
    --input .opencode/logs/ses_<id> \
    --output-dir .opencode/logs/ses_<id>/transcripts
```

***

## 5. Composition by Higher-Level Skills

This is a base primitive with no composers yet. Future composers
(session conversation viewer, session archive, cross-session
conversation diff) may consume this base.

| Composer | Composition Mechanism |
| :--- | :--- |
| _(none yet)_ | — |

***

## Related Skills

| Skill | Relationship |
| :--- | :--- |
| [`opencode-session-yaml-transcript-extractor`](../opencode-session-yaml-transcript-extractor/SKILL.md) | Parallel base — emits all-fields JSONL (header, user, thinking, tool calls); preferred when the full narrative including thinking is required |
| [`opencode-session-yaml-tool-call-extractor`](../opencode-session-yaml-tool-call-extractor/SKILL.md) | Parallel base — emits tool-call-only JSONL |
| [`opencode-current-session-id`](../opencode-current-session-id/SKILL.md) | Sibling — resolves the current session's ID/title from the same logs |
| [`opencode-session-transcript-to-source-resolve`](../opencode-session-transcript-to-source-resolve/SKILL.md) | Composer — resolves the transcript paths this skill produces back to the source logs (the reverse direction) |

***

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

***

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).
