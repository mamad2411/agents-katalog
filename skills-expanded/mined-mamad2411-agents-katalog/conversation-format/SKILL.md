---
name: conversation-format
description: >
  This skill should be used when parsing Claude Code conversation files, reading
  conversation history, working with ".jsonl" conversation transcripts, extracting
  signal from conversation data, filtering noise entries, linking subagent files,
  detecting session boundaries, or understanding the Claude Code conversation storage
  format. Provides the JSONL schema, entry types, content block extraction rules,
  user message filtering logic, and subagent linking patterns needed by the retell
  pipeline.
version: 0.1.0
---

# Conversation Format

## Overview

Claude Code stores conversation transcripts as JSONL files in `~/.claude/projects/<encoded-path>/<uuid>.jsonl`. Each line is a JSON object with a `type` field that determines its shape and narrative value. A typical 15 MB conversation contains only ~338 KB of signal (~2.2%). The parser's job is to extract that signal deterministically, at zero token cost.

## File Locations

**Main conversations:**
```
~/.claude/projects/<encoded-path>/<conversation-uuid>.jsonl
```

Path encoding replaces `/` with `-` in the project's absolute path:
- `/Users/oliver/Desktop/Vault.nosync/vault` encodes to `-Users-oliver-Desktop-Vault-nosync-vault`

**Subagent transcripts** (same JSONL format):
```
<conversation-uuid>/subagents/agent-<agent-id>.jsonl
```

**Compact summaries** — system-generated conversation recaps from `/compact`. Filename pattern: `agent-acompact-*.jsonl`. These are NOT real subagent research. Skip them as subagent content, but they can serve as chapter bridges (they are high-quality "previously on..." summaries).

## Entry Types

### Signal entries (extract)

| Type | Key fields | Narrative value |
|------|-----------|-----------------|
| `user` | `message.content` (string or content blocks) | Human requests, reactions, pivots — drives the story |
| `assistant` | `message.content` (array of content blocks) | Responses, decisions, deliverables — the action |
| `system` with `subtype: turn_duration` | `durationMs` (milliseconds) | Pacing metadata ("after 3 minutes of research..."). Typical range: 5,000-300,000 ms. |

### Noise entries (drop entirely)

| Type | Why skip |
|------|----------|
| `progress` | Hook events, intermediate states — no narrative value |
| `file-history-snapshot` | Undo/restore snapshots — internal bookkeeping |
| `queue-operation` | Internal scheduling — never user-visible |
| `system` (other subtypes) | Metadata with no narrative content |

## Content Block Types

### Assistant content blocks

Assistant messages contain an array of content blocks. Extract in this priority:

| Block type | Fields | Extraction rule |
|-----------|--------|----------------|
| `text` | `type`, `text` | **Always extract** — visible response to user |
| `thinking` | `type`, `thinking`, `signature` | **Extract selectively** — internal reasoning, reveals decision-making. Use for "behind the scenes" narrative depth, but not every thinking block is interesting. Mundane implementation details should be skipped. |
| `tool_use` | `type`, `id`, `name`, `input` | **Extract name only** — shows what actions were taken. Drop `input` (verbose). |

### User content blocks

User message `content` can be a plain string OR an array of content blocks:

| Block type | Fields | Extraction rule |
|-----------|--------|----------------|
| `text` | `type`, `text` | **Always extract** — the user's actual words |
| `tool_result` | `type`, `tool_use_id`, `content`, `is_error` | **Drop** in most cases — raw tool output (file listings, grep results). **Exception:** check for embedded images and `agentId` patterns (see below). |

### Image extraction from tool_result blocks

Playwright screenshots are embedded as base64 in `tool_result` blocks:

```jsonc
{
  "type": "tool_result",
  "content": [
    {
      "type": "image",
      "source": {
        "type": "base64",
        "media_type": "image/png",
        "data": "iVBORw0KGgo..."  // base64-encoded image
      }
    }
  ]
}
```

The parser extracts these to an `assets/` directory and references them by filename in the event stream. Images are never sent to the LLM — they are extracted by the script and made available for the author to include in the final post.

## User Message Filtering Rules

Apply these filters in order to separate real user input from system noise:

1. **Drop** if content is only `tool_result` blocks (no `text` block present) — these are permission grants or pure tool output
2. **Drop** if content string is empty — permission grant (user hit Enter to approve a tool call)
3. **Drop** if content contains `<local-command-` or `<command-name>` tags — CLI command output (`/compact`, `/exit`, etc.)
4. **Strip** `<system-reminder>` tags from remaining text — injected system context, not user words
5. **Flag** messages containing "continued from a previous conversation" as continuation summaries — these contain rich recaps useful as chapter bridges

## Session Boundary Detection

A single JSONL file can span multiple context windows. Detect boundaries by:

1. **`sessionId` changes** — the field shifts to a new UUID between messages
2. **Continuation markers** — user message containing "continued from a previous conversation" with a rich summary of prior context
3. **`/compact` commands** — `<command-name>/compact</command-name>` indicates mid-session context compression

These are natural chapter breaks in the narrative. For editorial guidance on using them, see the `narrative-craft` skill.

## Subagent Linking

The main conversation's `tool_use` for an Agent call does NOT contain the subagent ID. The `agentId` appears only in the subsequent `tool_result`.

**Example — the Agent tool_use block (in assistant message):**

```jsonc
{
  "type": "tool_use",
  "id": "toolu_01ABC123...",
  "name": "Agent",
  "input": {
    "description": "Brand color research",
    "prompt": "Research color palettes for a premium SaaS brand...",
    "subagent_type": "general-purpose"
  }
}
```

**Example — the matching tool_result (in next user message):**

```jsonc
{
  "type": "tool_result",
  "tool_use_id": "toolu_01ABC123...",
  "content": "...agent output text...\n\nagentId: a4830b373be1203a0 (for resuming...)\n<usage>total_tokens: 51009\ntool_uses: 12\nduration_ms: 229671</usage>"
}
```

**Linking procedure:**
1. Find `tool_use` blocks with `name: "Agent"` — note the `id` and `input.description`
2. In the next user message, find the `tool_result` with matching `tool_use_id`
3. Regex the `agentId` from the tool_result text: `agentId:\s*([a-f0-9]+)`
4. Match to subagent filename: `agent-{agentId}.jsonl`
5. Extract the `<usage>` block — `total_tokens` and `duration_ms` are useful for pacing narrative

## PII and Secret Scanning

The parser scans extracted signal for common secret patterns: `sk-*`, `ghp_*`, `AKIA*`, `Bearer *`, `password=*`. Matches appear as `pii_warnings` in the manifest. The parser flags but does not auto-redact — false positives are likely. The author decides what to redact at the triage gate.

## Parser Script

The retell plugin includes a deterministic parser at `${CLAUDE_PLUGIN_ROOT}/scripts/parse-conversation.py`:

```bash
# Parse a conversation by UUID prefix
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse-conversation.py 8c439a20

# Parse with full path and custom output
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse-conversation.py /path/to/file.jsonl --output-dir ./artifacts

# Include subagent events
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/parse-conversation.py 8c439a20 --include-subagents
```

**Output:** `events.json` (ordered signal events) and `manifest.json` (metadata + token estimates + PII warnings).

## Preview Script

Discover conversations worth turning into blog posts:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preview-conversations.py      # Last 10
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preview-conversations.py 20    # Last 20
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/preview-conversations.py --json # Machine-readable
```

## Known Limitations

- **Path encoding is lossy** — `-` appears in both encoded `/` and real directory names. Validate decoded paths against the filesystem.
- **Token estimates use 4 bytes/token** — can be off by 30-50% for code or non-ASCII. The manifest reports `estimation_method` for transparency.
- **JSONL format is undocumented** — reverse-engineered from actual files. Any Claude Code update could change field names or entry types. The parser fails loudly on unknown entry types.
- **Thinking blocks carry cryptographic signatures** — treat as editorial source material, not directly publishable content. See the `narrative-craft` skill for usage guidelines.
- **Active conversations** — if the JSONL is being written to (another session is open), the parser should copy first or check mtime. The current implementation does not auto-detect this.
- **File permissions are owner-only (600)** — the pipeline must run as the local user who owns the conversation files.
