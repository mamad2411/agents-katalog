---
name: chats
description: Interact with SuperAGI Sales platform via the Chat CLI
platform: [linux, macos]
---

# SuperAGI Chat CLI

## Install & Auth

```bash
curl -fsSL https://superagi.com/install.sh | bash
```

Pre-built binary. No build steps, no Go, no Bazel. Installs to `~/.local/bin/superagi`.

```bash
superagi --version   # verify
```

Auth — set API key (generated at Settings > API Keys in the SuperAGI web UI):

```bash
export SUPERAGI_API_KEY=your-key
```

Or persistent config at `~/.superagi/config.json`:

```json
{"base_url": "https://api.superagi.com", "api_key": "your-key"}
```

Every command also accepts `--api-key` and `--base-url` flags to override.

One binary, one API key — covers both CRM (`superagi crm`) and Chat (`superagi chat`).

---

## Mental Model

**Chat is SuperAGI's internal team messaging** (like Slack). It's for team communication, not customer-facing.

- **Groups = conversations.** A group can be a private channel, a public channel, a DM (1:1), a group DM (multi-person), or a self-DM (notes to self). The `type` field in responses distinguishes them.

- **Messages live inside groups.** Every message belongs to a group (identified by `group-id`). You cannot send a message without knowing the group.

- **Threads live inside messages.** A `thread-id` (UUID) groups replies together within a conversation. When a new message is created, its `thread_id` equals its own `id` — it becomes its own thread root. Replies set `thread-id` to the root message's ID.

- **`recipient-type` and `recipient-id`** identify the conversation context for message operations. These are integers. The agent CANNOT guess these values — it must discover them from group list responses first. In practice, `recipient_id` = group ID and `recipient_type` = `0` for standard group conversations, but **always read them from the API response** rather than hardcoding.

- **`sender-user-id`** allows posting a message AS another user. This is how AI agents send notifications — the message appears to come from the agent user, not the authenticated API caller.

- The CLI outputs JSON. Pipe through `jq` for filtering/formatting.

---

## Discovery Chain

The agent should ALWAYS list groups first before attempting to send or read messages:

```bash
# 1. See the 6 subcommand groups
superagi chat --help

# 2. See operations within a group (run --help on any subcommand)
superagi chat groups --help
superagi chat messages --help

# 3. Discover real groups — get IDs, types, names, recipient info
superagi chat groups list-groups --type all --limit 10

# 4. List only MY conversations
superagi chat groups list-groups-user-me --limit 10

# 5. Find a specific conversation
superagi chat groups list-groups --type dms --search "John"

# 6. Read messages in a group (need group-id from step 3/4)
superagi chat messages list-messages-group --group-id <ID> --limit 20

# 7. Discover threads in a conversation (need recipient-type and recipient-id from step 3/4)
superagi chat messages list-messages-threads --recipient-type <N> --recipient-id <N> --limit 10

# 8. Read thread replies (need thread-id from step 7)
superagi chat messages list-messages-thread-replies --group-id <ID> --thread-id <UUID> --limit 20
```

**If the agent doesn't know the group-id** → list groups first.
**If the agent doesn't know recipient-type/recipient-id** → get them from the group list response.
**If the agent doesn't know thread-id** → list threads first.

Never hardcode IDs. Always discover them.

---

## Gotchas — Things That Will Trip You Up

### 1. Pagination is --limit + --offset, NOT --page/--page-size

This is different from CRM. Default limits vary by endpoint (20-50), max is 1000. Message list responses return `total_count: -1` — they don't compute exact totals, they rely on `has_more` instead.

### 2. recipient-type is an integer, not a string

Don't guess `"dm"` or `"group"` — it's a number (e.g., `0`). Discover valid values from `list-groups` or `list-groups-user-me` responses, which include `recipient_type` and `recipient_id` fields on each conversation.

### 3. list-groups vs list-groups-user-me return different JSON keys

- `list-groups` → response key is `"conversations"`
- `list-groups-user-me` → response key is `"groups"`

Same pagination structure, different wrapper key. Parse accordingly.

### 4. Creating groups requires --type "private" or "public"

The `--type` flag accepts exactly two values: `private` or `public`. NOT `group`, `channel`, `dm`, etc. DMs and group DMs are created through a different flow (via message sending with user IDs), not through `create-groups`.

### 5. Editing vs Updating messages — different operations, different params

| Operation | Command | Use for | Required context |
|-----------|---------|---------|-----------------|
| Quick text edit | `patch-messages <id>` | Changing message text only | `--group-id` |
| Full update | `update-messages <id>` | Pinning, task linking, text, all fields | `--recipient-type`, `--recipient-id`, `--thread-id` |

`patch-messages` (PATCH) is lightweight. `update-messages` (PUT) is the full operation. Don't mix up their required params.

### 6. create-messages-link-task needs 3 query params alongside the body

`--recipient-type`, `--recipient-id`, and `--thread-id` are **all required** as query params, plus the `message_id` path param and `--task-id` in the body. Missing any of these causes an error.

### 7. Threading requires the parent message's UUID

To reply in a thread: `create-messages --thread-id <UUID> --recipient-id <N> --recipient-type <N>`. The thread-id is the root message's `id` field (a UUID like `fa4ea261-276b-11f1-856f-1a1f78a089b4`). A thread-id is the same as the root message's id — when you create a new message, its `thread_id` = its own `id`.

### 8. also-send-to-channel is for threaded replies

`--also-send-to-channel` on `create-messages` posts the reply both in the thread and in the main group conversation (like Slack's "also send to #channel" checkbox). Only meaningful when `--thread-id` is set.

### 9. system-message changes rendering

`--system-message` makes the message render as a system notification in the UI — different styling, not attributed to a person. Use for automated alerts, not regular conversation.

### 10. Presence is not implemented

`create-realtime-presence` returns HTTP 400: "presence feature not implemented in the new real-time system". `create-realtime-typing` works fine.

### 11. Group member roles are uppercase strings

Valid roles: `ADMIN`, `MEMBER`, `MODERATOR`. Pass them uppercase.

### 12. delete-messages requires full conversation context

Deleting a message requires `--recipient-type`, `--recipient-id`, AND `--thread-id` as query params alongside the `message_id` path param. You can't delete with just the message ID.

---

## How Chat Connects to the Rest of SuperAGI

- **Messages ↔ CRM Tasks**: `create-messages-link-task <msg_id> --task-id <UUID>` connects a conversation to an action item. The task appears in CRM > Tasks and the message shows a task link in the UI.

- **Agent posting**: `--sender-user-id N` on `create-messages` lets automated systems post as a specific user. Use cases: deal stage change notifications, lead assignment alerts, daily summary bots.

- **Groups as deal rooms**: Create a group per deal (`create-groups --name "Acme Deal Room" --type private`) for focused collaboration. Link related messages to the deal's tasks.

- **Search**: `list-messages-group --search "keyword"` searches within a group. There's no global message search across all groups via CLI — search one group at a time.

- **CRM CLI** (`superagi crm`) manages the data — leads, deals, contacts, tasks.
- **Chat CLI** (`superagi chat`) manages the communication — messages, threads, groups.
- They connect via task linking: find a task ID from CRM, link a chat message to it.
- Both use the same auth, same binary, same API key.
