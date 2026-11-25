---
name: jsonl-content-extractor
description: Generic primitive for extracting typed content blocks from JSONL files using a key-path navigation with optional value narrowing at each level. Domain-agnostic — works with any JSONL schema.
category: Text-Manipulation
---

# JSONL Content Extractor Skill (v1) — Base Primitive

Generic primitive that reads a JSONL file, navigates a user-specified key path into each line,
and separates content blocks into matched vs. unmatched output based on configurable value
filters at each path level.

Composers define the key path and match criteria; this skill executes the mechanical extraction
and produces machine-parseable JSON.

***

## 1. Composition Rationale

This skill is a **base primitive** — it owns ONLY the generic JSONL key-path extraction logic.
It accepts a JSONL file, a sequence of key names (each optionally narrowed by allowed values),
and produces two JSON arrays: matched items and unmatched items.

Composers that would invoke this skill:

- [`claude-session-exporter`](../claude-session-exporter/SKILL.md) — exports Claude/MCP session
  files by extracting `message.content[]` blocks with type filtering

The primitive was extracted because multiple future composers (exporters for Copilot sessions,
ChatGPT exports, generic JSONL audit tools) could reuse the same key-path navigation and
filtering logic without duplicating the extraction mechanics.

***

## 2. CLI Contract (Stable)

Located at [`scripts/extract.py`](./scripts/extract.py).

```bash
python3 scripts/extract.py \
  --file <path> \
  --key <name>[:<val1>,<val2>,...] \
  --key <name>[:<val1>,<val2>,...] \
  ... \
  --output-matched <path> \
  --output-unmatched <path>
```

### Arguments

| Argument | Repeatable | Description |
| :--- | :---: | :--- |
| `--file` | ❌ | Path to input JSONL file (required) |
| `--key` | ✅ | A key in the navigation path, optionally with comma-separated narrowing values after a colon (e.g. `type:tool_use,text`). The terminal key MUST have values. |
| `--output-matched` | ❌ | Path to write matched items JSON (required) |
| `--output-unmatched` | ❌ | Path to write unmatched items JSON (required) |

### Navigation Logic

For each JSONL line (parsed as a JSON object):

1. Start at the line object.
2. For each `--key` in sequence:
   - If current node is an **array** → apply remaining keys to every element, collect results.
   - If current node is an **object** → drill into `object[key]`.
   - If current node is a **scalar** → terminal value reached.
   - If the key has values (e.g. `type:val1,val2`): at array level, filter to items whose
     `[key]` equals one of the values; at object level, skip the line if `object[key]` is not
     in the values.
3. At the terminal level, the value is compared against the final key's value list to classify
   as matched or unmatched.

### Output Schema

Each file is a JSON array of objects:

```json
{
  "line": 337,
  "line_data": { },
  "content_index": 0,
  "matched": true,
  "value": "tool_result",
  "block": { }
}
```

| Field | Type | Description |
| :--- | :--- | :--- |
| `line` | int | 1-indexed line number in the input JSONL |
| `line_data` | object | The full parsed JSONL line object (composer uses this for context) |
| `content_index` | int | Index within the terminal array (0 if terminal is a scalar) |
| `matched` | bool | `true` if the terminal value matched the final `--value` filter |
| `value` | string | The terminal value extracted at the final key |
| `block` | object | The object containing the terminal value (the array item or leaf object) |

***

## 3. Examples

### Extract Claude session content blocks by type

```bash
python3 scripts/extract.py \
  --file session.jsonl \
  --key message \
  --key content \
  --key type:tool_use,tool_result,text,thinking \
  --output-matched matched.json \
  --output-unmatched unmatched.json
```

### Only assistant messages with tool_use

```bash
python3 scripts/extract.py \
  --file session.jsonl \
  --key type:assistant \
  --key message \
  --key content \
  --key type:tool_use \
  --output-matched matched.json \
  --output-unmatched unmatched.json
```

***

## 4. Programmatic API

```python
from scripts.extract import extract_blocks

matched, unmatched = extract_blocks(
    filepath="session.jsonl",
    keys=[("message", None), ("content", None), ("type", ["tool_use", "text"])],
)
```

Returns two lists of result dicts matching the JSON output schema.

***

## 5. Ownership & Evolution

- **Primitive maintainer**: This skill. The key-path navigation logic should remain generic.
- **Composer maintainer**: [`claude-session-exporter`](../claude-session-exporter/SKILL.md)
  and any future JSONL-format-specific composers.
- **Breaking changes**: Any change to the output schema or CLI flags must be mirrored in all
  known composers (listed in §1).

***

## 6. Security & Portability

- The script never executes or evaluates the extracted content.
- No credentials, hardcoded paths, or user-specific data are embedded.
- Output is pure JSON — the caller determines rendering and presentation.
