---
name: social-media-clients
description: "Social media platform CLI tools — Xiaohongshu (RedNote/小红书) via `xhs`, X/Twitter via `xurl`, and Yuanbao (元宝) group messaging. Each section covers auth setup, command reference, and common workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [social-media, xiaohongshu, rednote, twitter, x, yuanbao, cli]
    related_skills: [content-retrieval, media]
---

# Social Media CLI Clients

Unified guide for interacting with social media platforms via their CLI tools. Each platform has a separate section with auth, commands, and workflows.

**General safety rules for all platforms:**
- Do not share cookies/credentials in chat logs
- Prefer read-only operations; ask confirmation before destructive actions
- Verify auth status before attempting operations
- Use JSON output (`--json`) for machine-readable parsing
- Never paste credential files or tokens into conversation context

---

## Section A: Xiaohongshu (RedNote / 小红书)

CLI: `xhs` — search, read posts, browse favorites, user profiles, interactions.

### Prerequisites

```bash
pip3 install xhs
xhs status              # Already logged in as MinimX
xhs login --qrcode       # QR code login if needed
```

### Command Reference

```bash
xhs search "keyword" --sort popular --page 1 --json
xhs read <note_id_or_url> --json
xhs favorites
xhs whoami
xhs user <user_id>
xhs feed
xhs hot
xhs like <note_id>
xhs comment <note_id> "text"
xhs my-notes
xhs notifications
xhs unread
```

### Common Pattern

```bash
xhs search "Claude Cowork" --sort latest --json
xhs read "https://www.xiaohongshu.com/explore/<id>?xsec_token=<token>" --json
```

### Pitfalls

- `xsec_token` required in URLs for read operations
- Login cookies expire; re-auth with `xhs login --qrcode`
- `--limit` flag removed; use `--page` for pagination
- Short URLs (xhslink.com) need resolution via curl redirect

---

## Section B: X/Twitter

CLI: `xurl` (official X developer platform CLI) — posts, search, DMs, media, v2 API.

### One-Time User Setup (user runs manually)

```bash
# 1. Register app at https://developer.x.com
# 2. Register locally:
xurl auth apps add my-app --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
# 3. Authenticate (opens browser):
xurl auth oauth2 --app my-app YOUR_USERNAME
# 4. Set as default:
xurl auth default my-app
```

### Command Quick Reference

```bash
xurl whoami
xurl user @handle
xurl search "query" -n 10
xurl timeline -n 20
xurl mentions -n 10
xurl post "Hello world!"
xurl reply POST_ID "Nice post!"
xurl quote POST_ID "My take"
xurl delete POST_ID
xurl like POST_ID / xurl unlike POST_ID
xurl repost POST_ID / xurl unrepost POST_ID
xurl bookmark POST_ID / xurl unbookmark POST_ID
xurl follow @handle / xurl unfollow @handle
xurl following -n 20 / xurl followers -n 20
xurl block @handle / xurl unblock @handle
xurl dm @handle "message"
xurl dms -n 10
xurl media upload photo.jpg
```

### Raw API Access

```bash
xurl /2/users/me
xurl -X POST /2/tweets -d '{"text":"Hello"}'
```

### Safety (Mandatory)

- **Never** read, print, or send `~/.xurl` contents to LLM context
- **Never** use `--verbose` / `-v` in agent sessions (leaks auth headers)
- **Never** use inline-secret flags (`--bearer-token`, `--client-id`, etc.)
- Auth issues: direct user to manual OAuth flow

---

## Section C: Yuanbao (元宝) Group Interaction

Built-in gateway tools for Yuanbao group chat — @mention users, query info/members, send DMs.

### How It Works

Your text reply IS the message sent to the group/user. Include `@nickname` in your reply for automatic @mention.

### Available Tools

| Tool | Use |
|------|-----|
| `yb_query_group_info` | Group name, owner, member count |
| `yb_query_group_members` | Find user, list bots, list all members |
| `yb_send_dm` | Send private message with optional media |

### @Mention Workflow

1. `yb_query_group_members(group_code, action="find", name="<target>", mention=true)`
2. Get exact nickname from response
3. Include `@nickname` in your reply text — gateway handles conversion

### Send DM Workflow

```json
yb_send_dm({ "group_code": "535168412", "name": "用户aea3", "message": "hello" })
```

### Notes

- `group_code` from chat_id: `group:328306697` → `328306697`
- Groups called "派 (Pai)" in Yuanbao app
- Do NOT use `send_message` tool for Yuanbao DMs — use `yb_send_dm`