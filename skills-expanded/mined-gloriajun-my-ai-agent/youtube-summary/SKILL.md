---
name: youtube-summary
description: "Summarize a YouTube video, or search/manage YouTube channel subscriptions for monitoring. Use when the user shares a YouTube link, asks for a summary, wants to find reliable YouTube channels, or wants to register/manage channel monitoring."
metadata:
  {
    "openclaw":
      {
        "emoji": "▶️",
        "requires": { "bins": ["curl"] }
      }
  }
---

# YouTube Skill

Handles YouTube video summarization, channel search, and monitoring subscription management.

---

## Actions

| action | mode | required fields | description |
|---|---|---|---|
| `summarize` | `summary` | `url` or `query` | Summarize a video by URL or keyword search |
| `search-channels` | `channel` | `query` | Search YouTube channels by keyword |
| `subscribe` | `channel` | `channel_id` or `channel_handle`, `channel_name`, `slack_thread_ts` | Register a channel for monitoring |
| `unsubscribe` | `channel` | `channel_id` | Remove a channel from monitoring |
| `list-subscriptions` | `channel` | (none) | List all monitored channels |

---

## Execution

### Video Summary (URL)

```bash
curl -s -X POST "${N8N_WEBHOOK_BASE_URL}?type=youtube&mode=summary&action=summarize" \
  -H "Content-Type: application/json" \
  --max-time 60 \
  -d '{"url":"<YouTube URL>"}'
```

### Video Summary (keyword search)

```bash
curl -s -X POST "${N8N_WEBHOOK_BASE_URL}?type=youtube&mode=summary&action=summarize" \
  -H "Content-Type: application/json" \
  --max-time 60 \
  -d '{"query":"<search keyword>"}'
```

### Channel Search

```bash
curl -s -X POST "${N8N_WEBHOOK_BASE_URL}?type=youtube&mode=channel&action=search-channels" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"query":"<search keyword>"}'
```

**Success**: `status === "ok"` + `channels` array — display the channel list.  
Each item fields: `channel_name`, `channel_handle`, `channel_id`, `channel_url`, `description`

### Subscribe to Channel

Pass the current Slack message's `thread_ts` (or `message_ts`) as `slack_thread_ts`. New video notifications will be posted as replies to that thread.

```bash
curl -s -X POST "${N8N_WEBHOOK_BASE_URL}?type=youtube&mode=channel&action=subscribe" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"channel_id":"<UC...>","channel_name":"<name>","channel_handle":"<@handle>","slack_thread_ts":"<thread_ts>"}'
```

If `channel_id` is unknown, provide `channel_handle` only (auto-resolved):

```bash
curl -s -X POST "${N8N_WEBHOOK_BASE_URL}?type=youtube&mode=channel&action=subscribe" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"channel_handle":"@fireship","channel_name":"Fireship","slack_thread_ts":"<thread_ts>"}'
```

**Success**: `status === "ok"` + `message` field

### Unsubscribe from Channel

```bash
curl -s -X POST "${N8N_WEBHOOK_BASE_URL}?type=youtube&mode=channel&action=unsubscribe" \
  -H "Content-Type: application/json" \
  --max-time 15 \
  -d '{"channel_id":"<UC...>"}'
```

**Success**: `status === "ok"` + `message` field

### List Monitored Channels

```bash
curl -s -X POST "${N8N_WEBHOOK_BASE_URL}?type=youtube&mode=channel&action=list-subscriptions" \
  -H "Content-Type: application/json" \
  --max-time 15 \
  -d '{}'
```

**Success**: `status === "ok"` + `channels` array (or empty list message)

---

## Response Handling

Parse the curl output as JSON.

**Success** (`status === "ok"`): Present the result fields to the user.  
**Failure** (`status !== "ok"`, non-JSON, or empty output): Inform the user that the request failed. Include the `message` field if present, otherwise describe the issue briefly.

---

## Agent Behavior

- **Channel search then subscribe**: Show search results first; call subscribe only after the user selects a specific channel.
- **`slack_thread_ts` on subscribe**: Always pass the current message's `thread_ts` or `message_ts` exactly as received.
- **New video notifications**: Tell the user that new videos from subscribed channels will be notified automatically at 09:30 KST daily, posted as a reply in this thread.

---

## Language

Respond in the same language the user used.
