---
name: wildix-send-message
description: Use when asked to send a message to an x-bees, collaboration 7, x-hoppers chat channel on behalf of a bot or user. Triggers on requests like "send a message to channel X", "notify channel", "post to chat", "reply to message", "send file", "attach file to message".
license: MIT
metadata:
  author: Wildix
allowed-tools: >-
  Bash, Glob, Skill
---

# Send Message

Send a text message (with optional file attachments or as a reply) to an x-bees, collaboration 7, or x-hoppers channel — either as a bot or on behalf of a user.

## Peer Skills

Before running, check if required peer skills are installed:
```bash
Glob ~/.claude/skills/wildix-auth/SKILL.md
# If missing: npx skills add Wildix/agent-skills --s wildix-auth -y
```

See [`peers.yaml`](peers.yaml) for full peer manifest.

## Choosing a Token

```
BOT_TOKEN in .env?
  YES → use bot mode (no auth needed)
  NO  → user wants to send as themselves?
          YES → get ID_TOKEN via wildix-auth skill
          NO  → ask: "Provide BOT_TOKEN or send as your user account?"
                  BOT_TOKEN provided → save to .env, use bot mode
                  user account       → get ID_TOKEN via wildix-auth skill
```

---

## Mode 1: Simple text message

**Bot:**
```bash
bash <BASE_DIR>/scripts/send-message.sh "<channelId>" "<text>"
```

**User (pass ID_TOKEN via env):**
```bash
ID_TOKEN="$ID_TOKEN" bash <BASE_DIR>/scripts/send-message.sh "<channelId>" "<text>"
```

---

## Mode 2: Reply to a message (quote)

Pass `--reply-to <messageId>` — the server renders the quoted message in the UI automatically.

```bash
# Bot:
bash <BASE_DIR>/scripts/send-message.sh "<channelId>" "<replyText>" \
  --reply-to "<messageId>"

# User (token via env):
ID_TOKEN="$ID_TOKEN" bash <BASE_DIR>/scripts/send-message.sh "<channelId>" "<replyText>" \
  --reply-to "<messageId>"
```

The `messageId` is the 32-char ID from a previous message (available in chat history).

The script automatically fetches the original message to build the full `quote` object (API requires `messageId`, `channelId`, `createdAt`, `user`).

---

## Mode 3: Send with file attachments

### Step 1 — upload each file

```bash
# Bot:
ATTACH1=$(bash <BASE_DIR>/scripts/upload-file.sh "<channelId>" "/path/to/file.pdf")
ATTACH2=$(bash <BASE_DIR>/scripts/upload-file.sh "<channelId>" "/path/to/image.png")

# User (token via env):
ATTACH1=$(ID_TOKEN="$ID_TOKEN" bash <BASE_DIR>/scripts/upload-file.sh "<channelId>" "/path/to/file.pdf")
ATTACH2=$(ID_TOKEN="$ID_TOKEN" bash <BASE_DIR>/scripts/upload-file.sh "<channelId>" "/path/to/image.png")
```

`upload-file.sh` outputs a `MessageAttachment` JSON string. It internally:
1. Requests a presigned S3 URL from the API
2. Uploads the file binary to S3
3. Fetches file metadata and returns it as JSON

### Step 2 — send message with attachments

```bash
# Bot:
bash <BASE_DIR>/scripts/send-message.sh "<channelId>" "<text>" \
  --attach "$ATTACH1" \
  --attach "$ATTACH2"

# User (token via env):
ID_TOKEN="$ID_TOKEN" bash <BASE_DIR>/scripts/send-message.sh "<channelId>" "<text>" \
  --attach "$ATTACH1"
```

---

## Mode 4: Reply with attachments

Combine `--reply-to` and `--attach`:

```bash
ATTACH=$(bash <BASE_DIR>/scripts/upload-file.sh "<channelId>" "/path/to/file.pdf")

bash <BASE_DIR>/scripts/send-message.sh "<channelId>" "<text>" \
  --reply-to "<messageId>" \
  --attach "$ATTACH"
```

---

## API

| Operation | Endpoint |
|-----------|----------|
| Send message | `POST /v2/conversations/channels/{channelId}/messages` |
| Request upload URL | `POST /v2/conversations/channels/{channelId}/files` |
| Upload binary | `PUT <presignedUploadUrl>` (S3, no auth header) |
| Get file metadata | `GET /v2/conversations/channels/{channelId}/files/{fileId}` |

**Send message body fields:**
- `text` — message text (required unless attachments present)
- `quote.messageId` — messageId to reply to
- `attachments` — array of `MessageAttachment` objects from upload step

---

## .env format

`<BASE_DIR>/.env`:
```
BOT_TOKEN=wsk-v1-...
```

---

## Common Mistakes

| Problem | Fix |
|---------|-----|
| Using AccessToken instead of IdToken | Always use IdToken (from wildix-auth) for user-mode sends |
| Passing raw file path to `--attach` | First run `upload-file.sh`, pass its JSON output to `--attach` |
| `file` command not found | On macOS `file` is built-in; on minimal Linux: `apt install file` |
| S3 upload 403 | Presigned URL expired — re-run `upload-file.sh` (URLs are short-lived) |
