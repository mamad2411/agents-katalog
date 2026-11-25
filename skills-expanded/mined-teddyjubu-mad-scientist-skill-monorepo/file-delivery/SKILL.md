---

name: file-delivery
description: Complete file delivery system — outbound (VPS→Telegram) and inbound (Telegram→VPS or URL→VPS). Always use this when producing or receiving files.

---
## What This Skill Does

This skill Complete file delivery system — outbound (VPS→Telegram) and inbound (Telegram→VPS or URL→VPS). Always use this when producing or receiving files.

## Quick Reference

| Direction | Command | Example |
|---|---|---|
| VPS → Telegram | `hermes-send-file "/path" "caption"` | `hermes-send-file /tmp/report.pdf "Q1 Financial Report"` |
| Telegram → VPS | `hermes-fetch-telegram-file "/path"` | `hermes-fetch-telegram-file ~/docs/brief.docx` |
| URL → VPS | `hermes-fetch-url "https://" "/path"` | `hermes-fetch-url "https://drive.google.com/..." ~/docs/file.pdf` |

---

## Outbound: VPS → User (Telegram)

**When**: After saving or producing ANY file — PDF, report, CSV, image, audio, archive.

> **Default choice: Telegram direct.** For files up to 50 MB, `hermes-send-file` is the simplest and fastest path. Do not over-engineer with OAuth, rclone, Google Drive API, or HTTP servers first. If Telegram works, use it.

```bash
hermes-send-file "/path/to/file.pdf" "Descriptive caption"
```

### Decision Tree
```
Is file ≤ 50 MB?
├── YES → Use hermes-send-file immediately (fastest, zero setup)
└── NO  (50–200 MB)
     ├── Try Catbox.moe upload (one-liner, no auth)
     └── If Catbox fails → compress/split the file and retry
     
> 200 MB → Compress or split first, then retry at ≤ 50 MB tier
```

### What NOT to Try First (lesson hard-learned)
These paths have been attempted and failed on this VPS — do not restart the investigation from scratch:
- **OAuth / browser sign-in flows** — requires Charles's browser interaction, tokens expire, complex setup
- **rclone** — not configured on host
- **Google Drive API / gog CLI** — token exists in keyring but Drive scope not authorized
- **Python http.server + URL** — Charles has no browser on the VPS to download
- **Serve file via Traefik** — adds unnecessary complexity for a one-time transfer

If Telegram fails (size, rate limit), THEN escalate to Catbox. Only if Catbox also fails should you investigate other paths — and surface the error to Charles rather than spending >60 seconds debugging OAuth/rclone/etc.

### Rules
1. Always run `hermes-send-file` IMMEDIATELY after saving — before telling the user anything
2. Use a descriptive caption, not just the filename
3. If it succeeds: "Check your Telegram, the file is there."
4. If it fails: tell the user AND show the local file path as fallback
5. Never just print a file path and expect the user to retrieve it

---

## Inbound Method A: User Forwards File in Telegram

**When**: User says "I'm sending you X, save it to Y" or simply forwards a document to the bot.

### Steps
1. User forwards the file to your Telegram bot
2. You run:
   ```bash
   hermes-fetch-telegram-file "/path/to/save.docx"
   ```
   Or auto-detect filename:
   ```bash
   hermes-fetch-telegram-file   # saves to /tmp/telegram-downloads/ with original name
   ```

### How It Works
- Scans the bot's last 50 messages for documents, photos, videos, or audio
- Downloads the most recent file the user sent
- Saves to your specified path

### Pitfalls
- File must be forwarded to the bot FIRST, then you run the command
- If the user sent the file before you started listening, they need to forward it again
- Google Docs/Sheets links must be exported as .pdf or .xlsx first — the API can't download GDrive native formats

---

## Inbound Method C: Fetch from URL

**When**: User provides a link (Google Drive, Dropbox, WeTransfer, direct URL).

### Steps
1. User gives you the URL
2. You run:
   ```bash
   hermes-fetch-url "https://example.com/file.pdf" "/path/to/save.pdf"
   ```
   Or auto-detect filename:
   ```bash
   hermes-fetch-url "https://example.com/file.pdf"
   ```

### Google Drive Special Format
For Google Drive share links, convert to direct download:
- Share link: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
- Direct download: `https://drive.google.com/uc?export=download&id=FILE_ID`

### Pitfalls
- Dropbox links: change `?dl=0` to `?dl=1` for direct download
- WeTransfer links expire after 7 days — download quickly
- Some sites block `curl` — if it fails, try `browser_navigate` and download via browser

---

## Verification

Before using, confirm scripts exist:
```bash
which hermes-send-file
which hermes-fetch-telegram-file
which hermes-fetch-url
```

## Delivery to Current Chat vs Home Channel

**`hermes-send-file` ALWAYS sends to `TELEGRAM_HOME_CHANNEL`** — it ignores any delivery target argument. It ignores `origin` and ignores explicit `telegram:CHAT_ID` arguments. The script is hardcoded to use `TELEGRAM_HOME_CHANNEL` from the environment.

If the user says "send it here in this chat" and they are NOT in the Home channel, you have two options:

**Option A: `hermes-send-file` with target (if the script supports it)**
Run the command and check output — if it says `Sent to Telegram (chat: <HOME_CHANNEL_ID>)` then it went to Home, NOT origin. You must use Option B instead.

**Option B: Use `MEDIA:` prefix in your response**
```
MEDIA:/path/to/file.png
```
This delivers the file as an inline photo in the CURRENT chat (origin). Include a caption in your text response.

### Rules
- If user is in their Home channel → `hermes-send-file` works fine
- If user is in a DM/private chat → `hermes-send-file` sends to Home silently (user won't see it there) → use `MEDIA:` instead

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `hermes-send-file`: "chat not found" | `TELEGRAM_HOME_CHANNEL` has invalid value — set to numeric chat ID in `.env` |
| `hermes-send-file`: "command not found" | Verify at `/usr/local/bin/hermes-send-file` and `/usr/local/bin` is in PATH |
| `hermes-send-file`: files report SUCCESS but user says they don't see them | `hermes-send-file` sends to Home channel (597734298), not the current chat. User might be in a DM. Use `MEDIA:/path` to deliver to current chat instead. |
| `hermes-fetch-telegram-file`: "no file found" | User must forward the file to bot first |
| `hermes-fetch-url`: Google Drive fails | Convert to `uc?export=download&id=` format |
| Catbox upload fails | VPS may block outbound to catbox.moe — check firewall |
