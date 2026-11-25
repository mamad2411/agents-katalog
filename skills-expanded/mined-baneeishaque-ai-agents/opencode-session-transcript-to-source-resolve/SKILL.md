---
name: opencode-session-transcript-to-source-resolve
description: >-
  Composer — resolve opencode session transcript references (single or `to N`
  ranges) in free text to the ACTUAL source log files under the session
  directory; transcripts are derived artifacts, source logs are the durable
  SSOT. Range expansion delegates to the file-glob-sort-by-regex-capture base
  primitive's --min/--max numeric-span filter — never re-implementing the
  glob+regex+sort pipeline.
category: OpenCode
---

# OpenCode Session Transcript To Source Resolve (v1)

> **Skill ID:** `opencode-session-transcript-to-source-resolve`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Composition Rationale

This skill is a **composer**: it owns ONLY the reference parsing and
transcript→source mapping. The deterministic glob+regex+sort pipeline for
expanding `to N` ranges lives in the base primitive
[`file-glob-sort-by-regex-capture`](../../file-glob-sort-by-regex-capture/SKILL.md)
— the composer shells out to its script (`--min`/`--max` numeric span), never
re-deriving the pipeline inline.

It answers the reverse direction of the transcript pipeline: the logger's
per-turn YAML files (`ses_<id>/NNN-<ts>.yaml`) are the **durable SSOT**;
`transcripts/NNN-<ts>-transcript.yaml` files produced by
[`opencode-session-yaml-conversation-extractor`](../opencode-session-yaml-conversation-extractor/SKILL.md)
are **derived artifacts**. When a session reference (in chat text, a doc, or a
forensic query) cites a transcript path, consumers that need the source logs
(machine analysis via
[`opencode-session-yaml-transcript-extractor`](../opencode-session-yaml-transcript-extractor/SKILL.md)
or
[`opencode-session-yaml-tool-call-extractor`](../opencode-session-yaml-tool-call-extractor/SKILL.md))
MUST resolve to the source first.

***

## 1. Environment & Dependencies

| Requirement | Minimum | Verification |
| :--- | :--- | :--- |
| Python | 3.11+ | `python3 --version` |
| base skill script | present | `test -f .agents/skills/file-glob-sort-by-regex-capture/scripts/sort-by-capture.py` |
| logger YAML logs | `ses_<id>/NNN-<ts>.yaml` | `.opencode/logs/` |

Stdlib only (argparse, json, os, re, subprocess, sys). The base script is
resolved via a relative path anchored to the composer's own location and
verified with `os.path.isfile` before any shell-out; a missing base script is
a distinct exit-2 diagnostic, NOT a silent re-implementation.

***

## 2. Operational Logic

### 2.1 Reference Syntax

The composer scans `--text` for opencode session-log path references in two
accepted shapes, each optionally followed by a `to N` range marker:

| Shape | Example | Meaning |
| :--- | :--- | :--- |
| Transcript | `.../ses_<id>/transcripts/NNN-<ts>-transcript.yaml to 36` | derived artifact; strip `-transcript`, ascend out of `transcripts/` |
| Source log | `.../ses_<id>/NNN-<ts>.yaml to 2` | already the durable file; unchanged |

The path may be absolute, `...`-abbreviated, or bare (`ses_<id>/...`), and may
be wrapped in backticks/quotes (chat-export artifacts). The leading `NNN` is
the per-session turn number; the `to N` marker is inclusive (`to 36` = turn
numbers 030 through 036).

### 2.2 Resolution Rules

1. **Transcript → source**: `NNN-<ts>-transcript.yaml` becomes `NNN-<ts>.yaml`
   (strip the `-transcript` suffix), and the reference ascends from
   `<session>/transcripts/` to `<session>/`. The leading turn number is
   preserved.
2. **Source log → unchanged**: the reference is already in source form.
3. **`to N` range** (only materialized with `--expand`): the session directory
   is listed and files whose leading 3-digit number falls in `[NNN, N]`
   (inclusive) are emitted. This is delegated to the base script:
   `sort-by-capture.py --directory <session-dir> --glob "0*-*.yaml"`
   `--regex "^(\d{3})-" --sort-type int --min <NNN> --max <N>`, consuming the
   `abspath` field of its JSONL stdout.

### 2.3 Session Directory Resolution

For `--expand`, the session directory must exist on disk. A bare or
`...`-abbreviated reference is resolved by (a) the path as written, else
(b) `<repo>/.opencode/logs/ses_<id>`, else (c) `<repo>/ses_<id>`, where
`<repo>` is the workspace root derived from the script's own location.

***

## 3. CLI Contract (Stable)

```bash
python3 scripts/resolve-transcript-refs.py --text "<reference text>" \
    [--expand] [--output <file>]
```

| Flag | Required | Description |
| :--- | :--- | :--- |
| `--text` | Yes | Free text containing opencode session-log references (transcript or source form, optional `to N` ranges) |
| `--expand` | No | Emit one absolute source-log path per line; ranges expanded via the base skill's numeric-span filter |
| `--output` | No | Write the payload to a file instead of stdout |

### Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | Success — at least one reference resolved |
| 1 | No session-log references found in `--text` |
| 2 | Usage/parse error, or the base script `sort-by-capture.py` is missing |
| 3 | Referenced session dir or source file not found (`--expand` only) |

### Output Semantics

- stdout carries ONLY the payload (safe to pipe); diagnostics go to stderr.
- default: one compact resolved reference expression per input reference —
  `<session-dir>/NNN-<ts>.yaml` for singles, `<session-dir>/NNN-<ts>.yaml to N`
  for ranges — reproducing the chat-natural form verbatim.
- `--expand`: one absolute source-log path per line (single → the one file;
  range → every file in the span, in ascending turn order).

***

## 4. Scripts

- [`scripts/resolve-transcript-refs.py`](scripts/resolve-transcript-refs.py) —
  Tier-1 Python CLI (stdlib only, no third-party deps). Shells out to the base
  primitive for range listing.

```bash
python3 scripts/resolve-transcript-refs.py \
    --text ".../<session-id>/transcripts/030-2026-08-11T06-12-54-496Z-transcript.yaml to 36" \
    --expand
```

***

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| :--- | :--- |
| _(none yet)_ | — |

***

## Related Skills

| Skill | Relationship |
| :--- | :--- |
| [`file-glob-sort-by-regex-capture`](../../file-glob-sort-by-regex-capture/SKILL.md) | Consumed base — range expansion shells out to its `--min`/`--max` numeric-span filter |
| [`opencode-session-yaml-conversation-extractor`](../opencode-session-yaml-conversation-extractor/SKILL.md) | Producer of the transcript artifacts this composer resolves away from |
| [`opencode-session-yaml-transcript-extractor`](../opencode-session-yaml-transcript-extractor/SKILL.md) | Consumer of the SOURCE logs — the resolution target |
| [`opencode-session-yaml-tool-call-extractor`](../opencode-session-yaml-tool-call-extractor/SKILL.md) | Consumer of the SOURCE logs — the resolution target |
| [`opencode-current-session-id`](../opencode-current-session-id/SKILL.md) | Sibling — resolves the ACTIVE session; this composer resolves REFERENCES to any session |

***

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

***

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).
