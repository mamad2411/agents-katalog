---
name: claude-session-exporter
description: Export Claude/MCP session JSONL files into structured markdown — extract message content blocks by type with matched/unmatched separation.
category: Metrics & Reporting
---

# Claude Session Exporter Skill (v1) — Composer

Composer skill that exports Claude desktop / VS Code session JSONL files into human-readable
markdown documentation. Uses the [`jsonl-content-extractor`](../jsonl-content-extractor/SKILL.md)
base primitive for the mechanical extraction; adds Claude-specific schema knowledge and markdown
rendering.

***

## 1. Composition Rationale

This skill is a **composer**: it does NOT re-implement JSONL key-path extraction. It delegates
to the base primitive [`jsonl-content-extractor`](../jsonl-content-extractor/SKILL.md) via its
public CLI contract.

**Composition mechanism:**

The composer extracts from four distinct paths in a single pass:

1. **User text** (`type:user → message → content`):
   raw text of user messages (no type filter — captures everything the user typed).
2. **Typed content blocks** (`message → content → type:<types>`):
   assistant reply blocks (tool_use, tool_result, text, thinking) and tool results
   attached to user turns — excluding empty/whitespace-only text blocks.
3. **Skill listing attachments** (`attachment → type:skill_listing`):
   tool/skill attachments included in messages.
4. **Hook infos** (`hookInfos`):
   hook metadata entries at the line level (e.g. GitKraken/on-stop hooks).

Paths 1 and 2 are complementary: user text captures the question/intent, typed blocks
capture the structured assistant response and tool outputs.

For each path the base is called once with the appropriate key path. All matched results
are merged and rendered to `<session-id>-extracted.md`. Unmatched items from lines that
had zero matches across ALL paths go to `<session-id>-other.md`.

**Domain-specific value-add:**

- Knows the Claude session JSONL schema (`type` field for user/assistant distinction,
  `message.content[]` with typed blocks, `attachment` for skill listings,
  `hookInfos` for hook metadata).
- Default type filters: `tool_use`, `tool_result`, `text`, `thinking` (excludes `redacted_thinking`).
- Automatically skips text blocks whose content is only whitespace/newlines.
- Markdown rendering tailored for each source: user text inline, typed blocks with role
  labels, attachments and hook infos as JSON fences.
- Unmatched deduplication: items from a line that matched ANY path are excluded from
  the "other" file.
- Thin — every deterministic step is delegated to the base primitive.

Bidirectional discoverability: the base skill lists this composer in its `## Composition by Higher-Level Skills` table.

***

## 2. Environment & Dependencies

- Python 3.12+
- The `jsonl-content-extractor` base skill must exist at `../jsonl-content-extractor/` (sibling directory).

***

## 3. CLI Contract

Located at [`scripts/export-session.py`](./scripts/export-session.py).

```bash
python3 scripts/export-session.py \
  --file <path> \
  [--type <type> --type <type> ...] \
  [--output-dir <dir>]
```

### Arguments

| Argument | Repeatable | Default | Description |
| :--- | :---: | :---: | :--- |
| `--file` | ❌ | — | Path to Claude session JSONL file (required) |
| `--type` | ✅ | `tool_use`, `tool_result`, `text`, `thinking` | Content types to extract. If omitted, all common types are exported. |
| `--output-dir` | ❌ | current directory | Directory for output files |

### Output Files

| File | Content |
| :--- | :--- |
| `<session-id>-extracted.md` | Matched content blocks — formatted as markdown with line numbers, role labels, and type annotations |
| `<session-id>-other.md` | Unmatched content blocks — items that did not match the type filter |

The `session-id` is derived from the JSONL filename (the UUID portion before `.jsonl`).

***

## 4. Markdown Output Format

Each content block is rendered as:

```markdown
## Line <N> (<role> — <content_type>)
\`\`\`json
{...block content...}
\`\`\`
```

Block types are rendered with appropriate presentation:

| Content Type | Presentation |
| :--- | :--- |
| `text` | Rendered as-is (markdown text) |
| `tool_use` | JSON fenced block of the tool call |
| `tool_result` | JSON fenced block of the result |
| `thinking` | Italicized or fenced block |
| `redacted_thinking` | Note indicating redacted content |

***

## 5. Examples

```bash
# Export with defaults (all common types)
python3 scripts/export-session.py --file session.jsonl

# Export only tool_use and text blocks
python3 scripts/export-session.py --file session.jsonl --type tool_use --type text

# Export to a specific directory
python3 scripts/export-session.py --file session.jsonl --output-dir ./exports
```

***

## 6. Related Skills

- [`jsonl-content-extractor`](../jsonl-content-extractor/SKILL.md) — base primitive used for the mechanical extraction
- [`copilot-chat-history-analysis`](../copilot-chat-history-analysis/SKILL.md) — analogous skill for CSV-based chat analysis
