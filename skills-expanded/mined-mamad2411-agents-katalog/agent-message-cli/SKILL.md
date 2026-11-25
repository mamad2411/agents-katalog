---
name: agent-message-cli
description: Use this skill when an agent needs to report completed work or to send message to a user via the agent-messenger CLI. This is the tool agents use to send task completion reports, status updates, and work summaries to users after finishing their tasks. Trigger on any request involving reporting work results, notifying users of task completion, or sending work summaries via `agent-messenger`. Also use for related CLI operations like registering/logging in, reading conversations, editing or deleting messages, adding reactions, watching for real-time messages, or configuring the server URL.
---

# agent-message CLI

The agent-message CLI is a Go-based command-line client for the agent-message messaging platform. It connects to a REST + SSE backend and lets you send/receive direct messages, manage reactions, and configure the server.

## Quick Reference

**Install**: `npm install -g agent-message`
**Config file**: `~/.agent-message/config` (JSON)
**Default server**: `http://localhost:45180` (API), `http://localhost:45788` (Web)

After installing, start the server first with `agent-message start`, then use `agent-message <command>` for all other commands. Starting the local stack does not rewrite CLI traffic automatically. Regular commands still use the configured `server_url` unless you pass `--server-url` or update config.

## Global Flags

```
--config <path>       Path to config file (default: ~/.agent-message/config)
--server-url <url>    Override server URL for this command only
```

---

## Authentication

### Register a new account
```bash
agent-message register <account-id> <password>
# account-id: 3-32 chars, [A-Za-z0-9._-]
# password: 4-72 characters
# Output: registered <account-id>
# Side effect: saves token to config (no separate login needed)
```

Registration creates the authentication `account_id` and initializes the public `username` to the same value.

### Login
```bash
agent-message login <account-id> <password>
# Output: logged in as <account-id>
# Side effect: saves/updates a local profile for this account_id and makes it active
```

### Logout
```bash
agent-message logout
# Output: logged out
# Clears the active profile token locally; attempts remote logout (warns if server unreachable)
```

### Check current user
```bash
agent-message whoami
# Output: <username>
```

### Manage public usernames
```bash
agent-message username set <username>
agent-message username clear
```

Use `username set` to change the public name other users see in conversations.
If the username is empty, the server falls back to `account_id` automatically.
When choosing a username for a wrapper, bot, or task-specific account, prefer a name that is clearly related to the chat topic or role so the recipient can infer context quickly.

### List and switch saved profiles
```bash
agent-message profile list
# Output (one per line):
# * alice
#   bob logged_out

agent-message profile current
# Output: <active-profile-name>

agent-message profile switch <username>
# Output: switched to <username>
```

---

## Conversations

### List all conversations
```bash
agent-message ls
# Output (one per line):
# <conversation-id> <other-user-username>
```

### Open (or create) a conversation
```bash
agent-message open <username>
# Output: <conversation-id> <username>
# Creates the conversation if it doesn't exist yet
```

### Manage conversation titles
```bash
agent-message title set <username> "<title>"
agent-message title clear <username>
```

Use `title set` to store a short title on the DM conversation itself.
The web message list shows this title above the username when it is present.
If a conversation does not already have a title, it is usually better to set one based on the actual chat content or task, for example the feature name, bug being fixed, or report topic, rather than leaving it blank.
Prefer short, descriptive titles that help the recipient understand the thread at a glance.

---

## Messages

### Send a message
```bash
agent-message send <username> "<text>"
agent-message send "<text>"              # sends to configured master
agent-message send --to <username> "<text>"
# Output: sent <message-id>
```

If `master` is configured, `agent-message send "<text>"` sends to that default recipient.
Set it once with:

```bash
agent-message config set master jay
```

Recipient resolution rules:
- `send <username> "<text>"` uses the explicit positional username
- `send "<text>"` uses the configured `master`
- `send --to <username> "<text>"` overrides `master` for one command

### Send a json_render message
Use `--kind json_render` to send a structured rich message rendered by the web client using shadcn components.

```bash
agent-message send <username> '<json-spec>' --kind json_render
agent-message send '<json-spec>' --kind json_render       # sends to configured master
agent-message send --to <username> '<json-spec>' --kind json_render
```

The JSON spec follows this schema:
```json
{
  "root": "<element-id>",
  "elements": {
    "<element-id>": {
      "type": "<ComponentType>",
      "props": { ... },
      "children": ["<child-id>", ...]
    }
  }
}
```

**Example — badge + text in a stack:**
```bash
agent-message send alice '{
  "root": "stack-1",
  "elements": {
    "stack-1": { "type": "Stack", "children": ["badge-1", "text-1"] },
    "badge-1": { "type": "Badge", "props": { "text": "Agent" } },
    "text-1": { "type": "Text", "props": { "text": "Hello from CLI" } }
  }
}' --kind json_render
```

The web client renders the spec visually; the CLI shows `[json-render]` as a placeholder when reading these messages back.

### Print the authoritative json_render catalog prompt
Use this when an agent needs the exact `catalog.prompt()` output generated from the server's current catalog.

```bash
agent-message catalog prompt
```

This uses the currently configured `server_url` and calls `GET /api/catalog/prompt`.
If you want to target a local stack started with `agent-message start` or `agent-message start --dev`, update your config first:

```bash
agent-message config set server_url http://127.0.0.1:45180
agent-message catalog prompt
```

### Component Catalog

| Component | Required props | Optional props | Children |
|-----------|---------------|----------------|----------|
| `Alert` | `title` | `message`, `type` (`success`\|`info`\|`warning`\|`error`) | No |
| `Avatar` | `name` | `src`, `size` (`sm`\|`md`\|`lg`) | No |
| `Badge` | `text` | `variant` (`default`\|`secondary`\|`destructive`\|`outline`) | No |
| `Card` | — | `title`, `description`, `maxWidth` (`sm`\|`md`\|`lg`\|`full`), `centered` | Yes |
| `Grid` | — | `columns` (number), `gap` (`sm`\|`md`\|`lg`\|`xl`) | Yes |
| `Heading` | `text` | `level` (`h1`\|`h2`\|`h3`\|`h4`) | No |
| `Image` | `alt` | `src`, `width`, `height` | No |
| `Progress` | `value` (0–100) | `max`, `label` | No |
| `Separator` | — | `orientation` (`horizontal`\|`vertical`) | No |
| `Skeleton` | — | `width`, `height`, `rounded` | No |
| `Spinner` | — | `size` (`sm`\|`md`\|`lg`), `label` | No |
| `Stack` | — | `direction` (`horizontal`\|`vertical`), `gap` (`none`\|`sm`\|`md`\|`lg`\|`xl`), `align` (`start`\|`center`\|`end`\|`stretch`), `justify` (`start`\|`center`\|`end`\|`between`\|`around`) | Yes |
| `Table` | `columns` (string[]), `rows` (string[][]) | `caption` | No |
| `Text` | `text` | `variant` (`body`\|`caption`\|`muted`\|`lead`\|`code`) | No |

**More complex example — card with a progress bar and table:**
```json
{
  "root": "card-1",
  "elements": {
    "card-1": { "type": "Card", "props": { "title": "Deploy Status" }, "children": ["stack-1"] },
    "stack-1": { "type": "Stack", "props": { "gap": "md" }, "children": ["progress-1", "table-1"] },
    "progress-1": { "type": "Progress", "props": { "value": 75, "label": "Building..." } },
    "table-1": { "type": "Table", "props": { "columns": ["Step", "Status"], "rows": [["Build", "done"], ["Test", "running"], ["Deploy", "pending"]] } }
  }
}
```

**Flags:**
- `--kind text` (default) — plain text
- `--kind json_render` — structured JSON rendered by the web client

### Read messages
```bash
agent-message read <username>
# Output (one per line):
# [1] <message-id> <sender>: <text>
# [2] <message-id> <sender>: <text>
# ...

agent-message read <username> --n 50   # fetch last 50 messages (default: 20)
```

**Important:** The `read` command stores a local index (1, 2, 3…) that `edit`, `delete`, `react`, and `unreact` reference. Always run `read` before using those commands in a session.

Special message display:
- Deleted messages: `deleted message`
- JSON render messages: `[json-render]`

### Watch for real-time messages
```bash
agent-message watch <username>
# Streams new messages as they arrive (SSE)
# Blocks until Ctrl-C
# Output per message: <message-id> <sender-username>: <text>
```

---

## Message Mutations (require prior `read`)

All mutation commands use the **1-based index** from the most recent `read` output. Run `read <username>` first to establish the index.

### Edit a message
```bash
agent-message edit <index> "<new text>"
# Output: edited <message-id>
```

### Delete a message
```bash
agent-message delete <index>
# Output: deleted <message-id>
# Soft-deletes: message shows as "deleted message" to others
```

### Add a reaction
```bash
agent-message react <index> 👍
# Output: reaction added <message-id> 👍
# Running again with the same emoji toggles it off
```

### Remove a reaction
```bash
agent-message unreact <index> 👍
# Output: reaction removed <message-id> 👍
```

---

## Configuration

### Show config file path
```bash
agent-message config path
# Output: /Users/you/.agent-message/config
```

### Read config
```bash
agent-message config get              # full config as JSON
agent-message config get server_url   # single key value
agent-message config get master
```

### Write config
```bash
agent-message config set server_url https://api.example.com
agent-message config set master jay
agent-message config unset server_url   # reset to default (http://localhost:45180)
agent-message config unset master
```

**Supported keys:** `master`, `server_url`

---

## Config File Format

```json
{
  "server_url": "http://localhost:45180",
  "token": "<session-token>",
  "master": "jay",
  "last_read_conversation_id": "<uuid>",
  "read_sessions": {
    "<conversation-id>": {
      "conversation_id": "<uuid>",
      "username": "bob",
      "index_to_message": { "1": "<msg-id>", "2": "<msg-id>" },
      "last_read_message": "<msg-id>"
    }
  }
}
```

---

## Common Workflows

### First-time setup
```bash
# Configure server (if not localhost:8080)
agent-message config set server_url http://my-server:8080

# Register
agent-message register myusername 1234

# Or login if already registered
agent-message login myusername 1234

# Optional: set the default recipient for agent reports
agent-message config set master jay
```

### Send and receive messages
```bash
# Start a conversation and send a message
agent-message open alice
agent-message send alice "hey!"

# Or set a default recipient once and omit the username
agent-message config set master alice
agent-message send "hey!"

# Read the conversation
agent-message read alice

# Reply
agent-message send "how are you?"
```

### Edit or react to a message
```bash
# Read to establish the index
agent-message read alice

# Edit message at index 2
agent-message edit 2 "corrected text"

# React to message at index 1
agent-message react 1 ❤️
```

### Monitor incoming messages
```bash
agent-message watch alice
```

---

## Tips

- The `--server-url` flag overrides config for a single command — useful for targeting a non-default server without changing the saved config.
- The `master` config key sets the default recipient for `send`; use `--to <username>` when you need a one-off override.
- `edit`, `delete`, `react`, `unreact` all rely on the index from the last `read` in the same session. If you forget to read first, you'll get "index not found in last read session".
- Reactions toggle: `react 1 👍` twice removes the reaction (same as `unreact 1 👍`).
