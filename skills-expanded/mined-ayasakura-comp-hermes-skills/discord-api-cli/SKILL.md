---
name: discord-api-cli
description: Extract the bot token from the running pi-discord-gateway process and use curl for direct Discord API calls (posting media, fetching channels/members, etc.). Use when you need to programmatically interact with Discord beyond what the discord/ tools provide.
---

# Discord API via CLI

Extract the Discord bot token from the running gateway process and use it with `curl` for direct Discord REST API calls.

## Extract bot token

The bot token is stored in the environment of the `pi-discord-gateway` process:

```bash
TOKEN=$(tr '\0' '\n' < /proc/$(pgrep -f pi-discord-gateway | head -1)/environ | grep DISCORD_BOT_TOKEN | cut -d= -f2-)
```

Verify it:
```bash
echo "${TOKEN:0:20}..."   # should start with MTU (base64-encoded user ID prefix)
echo "Length: ${#TOKEN}"   # should be ~72 characters
```

## Posting images to a channel

```bash
curl -s -X POST "https://discord.com/api/v10/channels/$CHANNEL_ID/messages" \
  -H "Authorization: Bot $TOKEN" \
  -F "file=@/path/to/image.png" \
  -F "content=Your message here"
```

Returns JSON with the message object. Extract the CDN URL from `attachments[0].url` for sharing.

## Getting channel info (guild ID, member count)

```bash
curl -s "https://discord.com/api/v10/channels/$CHANNEL_ID" \
  -H "Authorization: Bot $TOKEN"
```

## Getting channel members

Discord doesn't expose channel member lists directly. Get members from the guild (server) instead:

```bash
# First get guild_id from channel info response, then:
curl -s "https://discord.com/api/v10/guilds/$GUILD_ID/members?limit=1000" \
  -H "Authorization: Bot $TOKEN"
```

Returns paginated member list. For large guilds, paginate with `after=<user_id>`.

## Important constraints

- **DO NOT mass-DM users** — sending unsolicited DMs to every channel member violates Discord ToS and can get the bot banned
- Always check user privacy settings before attempting DMs
- Rate limit yourself: wait 3-5 seconds between API calls
- Check API responses for errors (HTTP 429 = rate limited, 403 = permissions, 404 = not found)

## Common API endpoints

| Action | Method | Endpoint |
|---|---|---|
| Send message | POST | `/channels/{id}/messages` |
| Send file/image | POST | `/channels/{id}/messages` with `multipart/form-data` |
| Get channel info | GET | `/channels/{id}` |
| Get guild members | GET | `/guilds/{id}/members?limit=1000` |
| Get guild info | GET | `/guilds/{id}` |
| List roles | GET | `/guilds/{id}/roles` |
| Pin message | PUT | `/channels/{id}/pins/{message_id}` |

See https://discord.com/developers/docs for full API reference.

## Safety notes

- Never log or expose the full bot token in chat output
- Always verify the token length (~72 chars) before using it
- If a user has DMs disabled, the DM will fail silently with HTTP 403 — skip them gracefully