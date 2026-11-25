---
name: wildix-get-last-chats
description: Use when asked to list chats, show the inbox, browse recent conversations, or find a chat by name in x-bees, collaboration 7, or x-hoppers. Returns the user's chat list sorted by last activity. NOT for resolving a chat by its ID — use wildix-get-chat for that.
license: MIT
metadata:
  author: Wildix
allowed-tools: >-
  Bash, Glob, Skill
---

# Get Last Chats

Returns the user's x-bees inbox — a list of chats sorted by last activity.

**This skill fetches the user's chat list (inbox).** It is not designed for resolving a specific chat by its ID or raw channel ID. For that, use the `wildix-get-chat` skill.

## Peer Skills

Before running, check if `wildix-auth` is installed:
```bash
Glob ~/.claude/skills/wildix-auth/SKILL.md
# If missing: npx skills add Wildix/agent-skills --s wildix-auth -y
```

See [`peers.yaml`](peers.yaml) for full peer manifest.

## Flow

1. **Get x-bees IdToken** via `wildix-auth` skill — **REQUIRED, do not skip**
2. **Run the script**

```bash
ID_TOKEN="$ID_TOKEN" bash <BASE_DIR>/scripts/get-chats.sh [limit] [offset]
```

`limit` — number of chats to return (default: 30)
`offset` — skip this many chats (default: 0); use for pagination

**Pagination example:** to get page 2 with 30 chats per page, use `limit=30 offset=30`.

## API

`GET https://api.x-bees.com/v2/conversations/channels?limit={limit}&offset={offset}`

Authorization: `Bearer <IdToken>`

## Display results

The API returns channels already sorted by last message date (most recent first). **Do not re-sort the list** — preserve the original order from the API response.

```
Chats: {total}

1. {name} ({type}, {memberCount} members)
   channelId: {channelId}
```
