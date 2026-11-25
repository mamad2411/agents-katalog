---
name: nyx-lark
description: "Lark/Feishu integration via NyxID proxy. Replaces lark-cli — call Lark OpenAPI directly through nyxid proxy request with automatic credential injection."
version: 1.0.0
metadata:
  category: plain
  tag:
    - nyxid
    - lark
    - feishu
    - messaging
    - calendar
    - drive
  requires:
    bins: ["nyxid"]
---

# nyx-lark

This skill replaces all 20 lark-cli skills. Instead of `lark-cli <service> +<shortcut>`, use `nyxid proxy request <slug> <path>`. NyxID handles tenant token exchange (bot) and OAuth token injection (user) automatically.

## 1. Dual Service Architecture

Two NyxID services for Lark, matching lark-cli's `--as bot` / `--as user`:

| Service | Identity | Auth Method | Base URL | Path Convention |
|---------|----------|-------------|----------|-----------------|
| `api-lark-bot` | Bot (tenant_access_token) | Token exchange | `https://open.larksuite.com` | Paths start with `/open-apis/` |
| `api-lark` | User (user_access_token) | OAuth | `https://open.larksuite.com/open-apis` | Paths start with `/` (no `/open-apis/` prefix) |

Same API, different service — the base URL already contains the prefix for user.

The key difference: `api-lark-bot` base URL ends at the domain, so you must include `/open-apis/` in every path. `api-lark` base URL already includes `/open-apis`, so paths start directly with the API version segment.

```bash
# Bot: list chats — note the /open-apis/ prefix
nyxid proxy request api-lark-bot /open-apis/im/v1/chats

# User: list chats — no /open-apis/ prefix needed
nyxid proxy request api-lark /im/v1/chats

# Bot: send message — POST with JSON body
nyxid proxy request api-lark-bot "/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -m POST -d '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"hello\"}"}'

# User: get primary calendar
nyxid proxy request api-lark /calendar/v4/calendars/primary
```

If you accidentally double the prefix (e.g., `api-lark /open-apis/im/v1/chats`), the downstream URL becomes `/open-apis/open-apis/...` and returns 404.

## 2. Identity Routing Table

Which service to use for each Lark API domain:

| Domain | Service | Reason |
|--------|---------|--------|
| IM — bot messages, list chats | `api-lark-bot` | Org-level, bot identity |
| IM — send as user | `api-lark` | Needs user_access_token |
| Calendar — agenda, events, free/busy | `api-lark` | Personal calendar data |
| Contact — user lookup, search | `api-lark-bot` | User OAuth scope hard to obtain |
| Drive — upload, download, list files | `api-lark-bot` | drive scope only on bot |
| Doc — create, read, write documents | `api-lark` | docx scope available on user |
| Wiki — spaces, nodes | `api-lark-bot` | wiki scope only on bot |
| Task — CRUD, subtasks, tasklists | `api-lark-bot` | task scope only on bot |
| Sheets — read, write, append | `api-lark-bot` | sheets scope on bot |
| Base (Bitable) — tables, records | `api-lark-bot` | bitable scope on bot |
| Mail — send, reply, drafts | `api-lark` | Personal mailbox |
| Approval — instances, tasks | `api-lark-bot` | Org-level |
| VC / Minutes — meetings, transcripts | `api-lark-bot` | Org-level |

See `references/identity.md` for complete scope mapping.

## 3. First-Time Setup

### Bot setup (token exchange — NyxID handles transparently)

```bash
nyxid service add api-lark-bot
# Prompted for JSON credential:
#   app_id: your Lark app ID (e.g., cli_a940e30bf3b89eea)
#   app_secret: your Lark app secret
# Get these from: https://open.larksuite.com/app → your app → Credentials
```

### User OAuth setup (opens browser for consent)

```bash
nyxid service add api-lark --oauth --scope "\
contact:user.base:readonly,\
calendar:calendar.event:read,calendar:calendar.event:create,\
calendar:calendar.event:update,calendar:calendar.free_busy:read,\
calendar:calendar:read,\
docx:document,docx:document:readonly,docx:document:create,\
im:chat:read,im:message,im:message.send_as_user,\
im:message:readonly,im:message.group_msg:get_as_user,\
sheets:spreadsheet:readonly,\
approval:task:read,approval:instance:read,\
drive:drive:readonly,wiki:wiki:readonly,\
task:task:read,task:task:write,\
mail:mailbox:readonly,bitable:bitable:readonly"
```

### Verify both services work

```bash
# Bot: should return a JSON object with data.items[] containing chat_id, name, etc.
nyxid proxy request api-lark-bot /open-apis/im/v1/chats

# User: should return a JSON object with data.calendar_list[] containing calendar_id, summary, etc.
nyxid proxy request api-lark /calendar/v4/calendars
```

If either returns a scope error, see Section 5 (Scope Troubleshooting).

## 4. lark-cli Migration Cheat Sheet

Top 10 most common operations, showing lark-cli vs NyxID equivalent.

### 4a. Send a message (bot)

```bash
# lark-cli
lark-cli im +messages-send --as bot --chat-id oc_xxx --msg-type text --data '{"text":"hello"}'

# nyx
nyxid proxy request api-lark-bot "/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -m POST -d '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"hello\"}"}'
```

### 4b. List chats (bot)

```bash
# lark-cli
lark-cli im +chat-search --as bot

# nyx
nyxid proxy request api-lark-bot /open-apis/im/v1/chats
```

### 4c. View today's agenda (user)

```bash
# lark-cli
lark-cli calendar +agenda --as user

# nyx (replace CALENDAR_ID and timestamps)
nyxid proxy request api-lark "/calendar/v4/calendars/CALENDAR_ID/events?\
start_time=START_UNIX&end_time=END_UNIX"
```

### 4d. Create a calendar event (user)

```bash
nyxid proxy request api-lark "/calendar/v4/calendars/CALENDAR_ID/events" \
  -m POST -d '{"summary":"Meeting","start_time":{"timestamp":"1718280000"},"end_time":{"timestamp":"1718283600"}}'
```

### 4e. Get user info (bot)

```bash
# lark-cli
lark-cli contact +get-user --as bot --user-id ou_xxx

# nyx
nyxid proxy request api-lark-bot /open-apis/contact/v3/users/ou_xxx
```

### 4f. List files in drive (bot)

```bash
nyxid proxy request api-lark-bot /open-apis/drive/v1/files
```

### 4g. Create a document (user)

```bash
nyxid proxy request api-lark /docx/v1/documents \
  -m POST -d '{"title":"New Doc","folder_token":"fldcniHf40Vcv1"}'
```

### 4h. Create a task (bot)

```bash
nyxid proxy request api-lark-bot /open-apis/task/v2/tasks \
  -m POST -d '{"summary":"My task"}'
```

### 4i. Search messages (user)

```bash
nyxid proxy request api-lark "/im/v1/messages/search?query=keyword" \
  -m POST -d '{"query":"search term"}'
```

### 4j. Query free/busy (user)

```bash
nyxid proxy request api-lark "/calendar/v4/freebusy/list" \
  -m POST -d '{"time_min":"1718280000","time_max":"1718366400","user_id":{"user_id":"ou_xxx","id_type":"open_id"}}'
```

## 5. Scope Troubleshooting

### Bot scope missing

```bash
# Lark error includes helps[].url — open it to add the scope
open "https://open.larksuite.com/app/cli_a940e30bf3b89eea/auth?q=im:chat:readonly&op_from=openapi"
# Bot scopes take effect immediately after adding
```

### User scope missing

```bash
# 1. Delete all old OAuth credentials (they share a refresh token)
nyxid external-key list               # find Lark OAuth entries
nyxid external-key delete <id>        # delete each one

# 2. Re-add with correct scopes
nyxid service add api-lark --oauth --scope "new,scopes,here"
```

### Key gotchas

- Bot scope names differ from user scope names (e.g., `contact:contact.base:readonly` vs `contact:user.base:readonly`). Always check the Lark API docs for the correct scope variant.
- "Non-review permissions" (免审权限) still need explicit addition in the app console before they take effect. Not having them in the console means the scope string alone is insufficient.
- Max 32 scopes per OAuth request. If you need more, split across multiple service registrations with different slugs.
- After adding bot scopes, they take effect immediately. After adding user scopes, you must delete old OAuth tokens and re-authorize (the old refresh token remembers the original scope set).
- A 404 on a seemingly valid path usually means the path prefix is wrong. Double-check Section 1 for the correct prefix convention per service.

## 6. Pagination

Most Lark list endpoints return paginated results. The pattern is consistent across all APIs:

```bash
# First page
nyxid proxy request api-lark-bot /open-apis/im/v1/chats

# Response includes: "page_token": "xxx", "has_more": true
# Next page
nyxid proxy request api-lark-bot "/open-apis/im/v1/chats?page_token=xxx&page_size=50"
```

Default page size is 20. Maximum is typically 50 or 100 depending on the endpoint. Check the specific API reference for limits.

## 7. Reference Docs

| File | Description |
|------|-------------|
| `references/identity.md` | Complete bot vs user routing + scope mapping |
| `references/im.md` | Messages, chats, threads, reactions |
| `references/calendar.md` | Events, free/busy, RSVP, suggestions |
| `references/contact.md` | User lookup, org structure |
| `references/drive.md` | Files, folders, comments, permissions |
| `references/doc.md` | Document CRUD, media upload |
| `references/wiki.md` | Knowledge base spaces, nodes |
| `references/task.md` | Tasks, subtasks, tasklists |
| `references/sheets.md` | Spreadsheet cells, rows, filters |
| `references/base.md` | Bitable tables, fields, records, views |
| `references/mail.md` | Email send, reply, drafts, folders |
| `references/approval.md` | Approval instances, tasks |
| `references/vc.md` | Meetings, minutes, transcripts |
