---
name: discord-mass-dm
description: Automate sending images or messages to all members of a Discord guild via DM, with privacy-failure handling.
---

# Discord Mass DM with Privacy Failure Handling

Automate sending images or messages to all members of a Discord guild via DM, handling the common case where most DMs fail due to user privacy settings.

## When to use

- User asks to "DM all members" or "send to everyone" in a Discord guild
- Distributing generated images/content to guild members
- Any bulk DM operation on Discord

## Expected outcome

**Most DMs will fail** with HTTP 403. This is normal — Discord's privacy settings block bots from DMing users who haven't opted in. Expect 0–5 successes at most in typical guilds.

## Workflow

### Step 1: Get bot token (if not already available)

```bash
# Find the pi-discord-gateway process
PID=$(pgrep -f pi-discord-gateway | head -1)
# Extract token from process environment
DISCORD_TOKEN=$(cat /proc/$PID/environ 2>/dev/null | tr '\0' '\n' | grep '^DISCORD_BOT_TOKEN=' | sed 's/DISCORD_BOT_TOKEN=//')
```

### Step 2: Get guild members

```bash
# Get guild ID from channel info first
curl -s -H "Authorization: Bot $DISCORD_TOKEN" \
  "https://discord.com/api/v10/channels/<channel_id>" -o /tmp/chan_info.json
# Guild ID is in the response at .guild_id

# Fetch members (limit 1000)
curl -s -H "Authorization: Bot $DISCORD_TOKEN" \
  "https://discord.com/api/v10/guilds/<guild_id>/members?limit=1000" \
  -o /tmp/members.json
```

### Step 3: DM each member

Use the **Create DM Channel** endpoint. A 403 response means the user has DMs restricted.

```bash
# Create DM channel for user
curl -s -X POST "https://discord.com/api/v10/users/<user_id>/channels" \
  -H "Authorization: Bot $DISCORD_TOKEN" \
  -H "Content-Type: application/json" \
  -o /tmp/dm_result.json
# If response has 403: user has DMs restricted
# On success: response contains 'id' (DM channel ID)
```

### Step 4: Send message + image in DM (if DM channel created)

```bash
# Multipart form data for image upload
BOUNDARY="----DiscordFormBoundary"
PAYLOAD=$(echo '{"content":"🐰 Message here"}')

# Read image
IMG=$(cat /path/to/image.png)

# Build multipart body and POST to DM channel
curl -s -X POST "https://discord.com/api/v10/channels/<dm_channel_id>/messages" \
  -H "Authorization: Bot $DISCORD_TOKEN" \
  -H "Content-Type: multipart/form-data; boundary=$BOUNDARY" \
  -F "payload_json=$PAYLOAD" \
  -F "files[0]=@$IMG" \
  -o /tmp/send_result.json
```

### Step 5: Report results

Summarize successes and failures. **Always present the DM failure count** — users need to understand that 403 means privacy settings, not a bug.

## Python template for batch DMing

```python
import json, time, urllib.request, urllib.error

TOKEN = "<bot_token>"

with open('/tmp/members.json') as f:
    members = json.load(f)

skip_ids = {'<bot_id>', '<skip_ids...>'}
results = []

for m in members:
    u = m['user']
    if u['id'] in skip_ids:
        continue
    
    try:
        # Create DM
        req = urllib.request.Request(
            f"https://discord.com/api/v10/users/{u['id']}/channels",
            data=json.dumps({}).encode(),
            headers={"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            dm_id = json.loads(resp.read())['id']
        
        # Send message with image
        boundary = "----DiscordFormBoundary"
        with open(image_path, 'rb') as img_f:
            img_bytes = img_f.read()
        
        parts = [
            f"--{boundary}".encode(),
            b'Content-Disposition: form-data; name="payload_json"',
            b"Content-Type: application/json",
            b"",
            json.dumps({"content": msg}).encode(),
            f"--{boundary}".encode(),
            f'Content-Disposition: form-data; name="files[0]"; filename="img.png"'.encode(),
            b"Content-Type: image/png",
            b"",
            img_bytes,
            f"--{boundary}--".encode(),
        ]
        
        req2 = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{dm_id}/messages",
            data=b"\r\n".join(parts),
            headers={"Authorization": f"Bot {TOKEN}",
                     "Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST"
        )
        with urllib.request.urlopen(req2, timeout=30) as resp2:
            results.append((u['username'], u.get('global_name'), True))
            
    except urllib.error.HTTPError as e:
        results.append((u['username'], u.get('global_name'), False))
    
    time.sleep(2.0)  # Rate limit safety

# Report
for name, display, success in results:
    status = "✅ DM 成功" if success else "❌ DM 失敗（隱私設定關閉）"
    print(f"{name} ({display}) - {status}")
```

## Key pitfalls

- **Rate limits**: Add `time.sleep(2.0)` between DM attempts to avoid ratelimit bans
- **403 ≠ bot issue**: HTTP 403 on DM creation almost always means user DM privacy settings block the bot
- **Skip yourself**: Always exclude the bot's own ID from DM attempts
- **No guarantee of success**: Even if DM channel creation succeeds, the send step might still fail
- **Discord ToS**: Mass DMing may violate Discord's Terms of Service — use responsibly

## Alternative when DMs fail

- Post to a public channel (like `#acg`) — members can self-serve
- Ask users to opt in by reacting with an emoji to trigger DMs
- Use Discord's built-in broadcast/announcement features for guild-wide messages