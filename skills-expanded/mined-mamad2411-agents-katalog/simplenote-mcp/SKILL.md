---
name: simplenote-mcp
description: Read, create, update, search, and delete notes in Simplenote via MCP. Use when the user asks to save notes, create reminders, manage a knowledge base, search notes, or interact with Simplenote in any way.
---

# Simplenote MCP

## Prerequisites

1. **Package installed:** `@automattic/simplenote-mcp` (npm)
2. **MCP config exists:** `~/mcp.json` with a `simplenote` server entry
3. **Logged in:** `~/.config/simplenote-mcp/auth.json` has valid credentials

If any prerequisite is missing, run setup first:

```bash
npx -y @automattic/simplenote-mcp setup
```

Then add to `~/mcp.json`:

```json
{
  "mcpServers": {
    "simplenote": {
      "command": "npx",
      "args": ["-y", "@automattic/simplenote-mcp"]
    }
  }
}
```

## How to Call

The MCP server uses **stdio JSON-RPC**. Send all messages in a single pipeline:

```bash
(
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"agent","version":"1.0"}}}'
sleep 1
echo '{"jsonrpc":"2.0","method":"notifications/initialized"}'
sleep 0.5
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"TOOL_NAME","arguments":{...}}}'
sleep 4
) | timeout 12 npx -y @automattic/simplenote-mcp 2>/dev/null
```

**Critical:** The `sleep` delays are required. Skip them and messages get lost.

## Available Tools

| Tool | Type | Arguments |
|------|------|-----------|
| `list_notes` | Read | `{tag?, limit?, include_deleted?}` |
| `search_notes` | Read | `{query, limit?, include_deleted?}` |
| `get_note` | Read | `{id, include_deleted?}` |
| `list_tags` | Read | `{}` |
| `get_note_history` | Read | `{id, limit?}` |
| `get_note_version` | Read | `{id, version}` |
| `create_note` | Write | `{content, tags?, markdown?, pinned?}` |
| `update_note` | Write | `{id, content?, tags?, markdown?, pinned?}` |
| `trash_note` | Write | `{id}` |
| `restore_note` | Write | `{id}` |
| `revert_note` | Write | `{id, version}` |

## Common Operations

### List notes

```bash
# Replace TOOL_NAME with list_notes
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_notes","arguments":{"limit":20}}}'
```

### Search notes

```bash
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_notes","arguments":{"query":"search term","limit":10}}}'
```

### Create a note

```bash
# First line becomes the title
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"create_note","arguments":{"content":"Note Title\n\nBody content here...","tags":["tag1","tag2"],"markdown":true}}}'
```

### Update a note (FULL replacement!)

```bash
# IMPORTANT: get_note first, modify content, then update
# The content field REPLACES the entire note
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"update_note","arguments":{"id":"NOTE_ID","content":"Full new content"}}}'
```

### Trash / Restore

```bash
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"trash_note","arguments":{"id":"NOTE_ID"}}}'
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"restore_note","arguments":{"id":"NOTE_ID"}}}'
```

## Parsing Responses

The response is JSON-RPC. Extract the result with:

```bash
| python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        d = json.loads(line)
        if d.get('id') == 2:
            content = d.get('result',{}).get('content',[])
            for c in content:
                if c.get('type') == 'text':
                    print(c['text'])
    except: pass
"
```

## Gotchas

1. **`content` replaces entire note** — always `get_note` first, then modify, then `update_note`
2. **Tags replace entire list** — provide full tag list on update, not just the new one
3. **`sleep` delays are mandatory** — `sleep 1` after init, `sleep 0.5` after initialized, `sleep 3-5` after tool call
4. **Write mode** — requires `writeMode: true` in `~/.config/simplenote-mcp/config.json`
5. **Token expiry** — if `list_notes` returns empty but account has notes, re-run `npx @automattic/simplenote-mcp setup`
6. **No project-specific info** — this skill is generic. Do not hardcode credentials, usernames, or note IDs.

## When to Use

- User says "save this to Simplenote" / "create a note" / "search my notes"
- User wants to manage a knowledge base, reminders, or task list in Simplenote
- User asks to read or update existing Simplenote notes
- Any interaction with Simplenote as a note-taking backend

