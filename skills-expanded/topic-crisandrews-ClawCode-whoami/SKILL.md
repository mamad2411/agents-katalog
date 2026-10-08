---
name: whoami
description: Show the sender's info — their ID, the channel they're using, and which agent they're talking to. Triggers on /whoami, /id, /quien, "quién soy", "who am I".
user-invocable: true
---

# Whoami

Show the current sender and session context. Useful for debugging on messaging channels.

## Steps

1. **Detect the surface**:
   - CLI: no `<channel source="...">`
   - WhatsApp: `<channel source="whatsapp">` with `user_id` (JID)
   - Telegram: `<channel source="telegram">` with user ID
   - etc.

2. **Extract sender info** from the message metadata if on a messaging channel.

3. **Get agent identity** from IDENTITY.md (name + emoji).

4. **Format the response**:

### CLI
```
You: local user
Agent: <Name> <emoji>
Workspace: <path>
Session: <id if available>
```

### WhatsApp
```
*You:* <user_id>
*Agent:* <Name> <emoji>
*Channel:* WhatsApp
```

### Telegram
```
**You:** <user_id>
**Agent:** <Name> <emoji>
**Channel:** Telegram
```

5. **Keep it short** — one card, no preamble.

## Notes

- On CLI, there's no sender ID — use "local user".
- On messaging channels, use the `user_id` from the `<channel>` metadata.
- This is the agent's version of OpenClaw's `/whoami` command.
