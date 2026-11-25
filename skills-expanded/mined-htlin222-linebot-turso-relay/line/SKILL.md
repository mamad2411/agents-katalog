---
name: line
description: Operate the linebot-turso-relay LINE bot from the CLI — resolve a person's display name to their LINE userId from the Turso archive, then send (push) a message to them, plus the supporting Messaging API operations (profile lookup, binary content download, reply context). Use when the user wants to "send/push a LINE message", "message <name> on LINE", "tell <someone> via the bot", "推訊息給某人", "用 lizard 發 LINE", "查某人的 LINE userId", or otherwise act *outbound* through the bot. For read-only querying of the archive (search/list/count forwarded messages) use the line-inbox skill instead.
allowed-tools: Bash(python3 *)
---

# LINE bot operations

Outbound + API operations for [linebot-turso-relay](https://github.com/htlin222/linebot-turso-relay). The bot captures forwarded messages into a Turso DB (read side = the **line-inbox** skill); this skill covers acting back out through LINE's Messaging API.

## Credentials

All operations authenticate with `LINE_CHANNEL_ACCESS_TOKEN` (bearer). It lives in the project `.env` alongside the Turso pair:

```
LINE_CHANNEL_SECRET=…        # HMAC for inbound webhook verification only
LINE_CHANNEL_ACCESS_TOKEN=…  # bearer for every api.line.me call below
TURSO_DATABASE_URL=…         # used by line-inbox for name→userId lookup
TURSO_AUTH_TOKEN=…
```

Resolve the repo root from this skill's base directory:

```bash
SKILL="<Base directory for this skill, as reported by the Skill tool>"
REPO="$SKILL/../../.."   # .claude/skills/line → repo root holding .env
```

**Never put the token on the command line** — read it from `.env` inside the script so it never appears in `argv`/process listing/shell history.

## Operation 1 — resolve a display name → userId

You can only push to a `U…` userId, and display names are neither unique nor stable. Resolve via the archive (uses the line-inbox script's DB access):

```bash
python3 "$REPO/.claude/skills/line-inbox/scripts/inbox.py" --json sql \
  "SELECT source_user_id, user_display_name, COUNT(*) AS n,
          MAX(datetime(line_timestamp_ms/1000,'unixepoch','+8 hours')) AS last_seen
   FROM messages WHERE user_display_name='<display-name>'
   GROUP BY source_user_id ORDER BY n DESC"
```

**Ambiguity rule — the one safety gate:** wrong-person is the only bad failure.
- **Exactly one** `source_user_id` row → safe to send.
- **Zero or two-plus** rows → STOP. Print the candidates (userId + `last_seen`) and have the user pick; send only with an explicit userId. Never auto-pick.

### Targeting a group or room

`to` also accepts a `C…` group id or `R…` room id (the bot must be a member — it is, if the chat appears in the archive). Groups/rooms carry **no display name** (`user_display_name` is the *speaker*, not the chat), so identify them by recent activity/content:

```bash
# groups the bot has seen, most recently active first
python3 "$REPO/.claude/skills/line-inbox/scripts/inbox.py" --json sql \
  "SELECT source_group_id, COUNT(*) AS n,
          MAX(datetime(line_timestamp_ms/1000,'unixepoch','+8 hours')) AS last_seen
   FROM messages WHERE source_group_id IS NOT NULL
   GROUP BY source_group_id ORDER BY last_seen DESC"

# which group/room a known message belongs to (find a message via line-inbox search first)
python3 "$REPO/.claude/skills/line-inbox/scripts/inbox.py" --json sql \
  "SELECT source_group_id, source_room_id FROM messages WHERE id=470"
```

## Operation 2 — send (push) a message

Proven recipe (this is the exact call validated end-to-end; `POST /v2/bot/message/push`):

```bash
LIZARD_ENV="$REPO/.env" python3 - <<'PY'
import os, json, pathlib, urllib.request, urllib.error
env = {}
for line in pathlib.Path(os.environ["LIZARD_ENV"]).read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip()
token = env["LINE_CHANNEL_ACCESS_TOKEN"]

to_id = "U…"            # userId (Operation 1), or a C… group / R… room id
text  = "your message"  # text only; ≤5000 chars

req = urllib.request.Request(
    "https://api.line.me/v2/bot/message/push",
    data=json.dumps({"to": to_id, "messages": [{"type": "text", "text": text}]}).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(req) as r:
        print("HTTP", r.status, "| request-id", r.headers.get("x-line-request-id"))
        print(r.read().decode() or "(empty body = success)")
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode())
PY
```

`200` with a `sentMessages` array = delivered. The `to` field also accepts a `source_group_id` / `source_room_id` to push into a group/room.

## Operation 3 — other Messaging API calls

Same bearer token; all against `api.line.me` (content uses `api-data.line.me`):

| Need | Call |
|---|---|
| Display name for a userId | `GET /v2/bot/profile/{userId}` → `{ "displayName": … }` |
| Download an attachment's bytes | `GET https://api-data.line.me/v2/bot/message/{messageId}/content` (LINE keeps it ~7 days; older archived bytes are in R2 — see line-inbox `attachments`) |
| Reply to an inbound event | `POST /v2/bot/message/reply` with `{ replyToken, messages }` — the Worker already does this; reply tokens are single-use and short-lived |

## Constraints & gotchas

- **Reachability:** push only reaches a userId who has added the bot as a friend and hasn't blocked it. You can only target IDs the bot has actually seen (they're in the DB).
- **Group push is public to the whole group** — everyone in it sees the message. Confirm the `C…` id maps to the chat you mean (via the activity/content query above) before sending; there's no recall.
- **Forwards lose the original sender:** `source_user_id` on a forwarded message is always *you*, the forwarder — never the original author. So name-resolution targets are people who DM'd the bot or spoke in a tracked group, not arbitrary contacts.
- **Push is metered:** replies are free/unlimited, push counts against LINE's monthly free-tier quota. Fine for personal volume; don't loop-blast.
- **Idempotency is inbound-only:** the dedup (`ON CONFLICT(webhook_event_id)`) protects ingest, not sends — a re-run of the push recipe sends again.
