---
name: apple-mail-cli
description: "Access Apple Mail.app from CLI — search, read, send, compose via SQLite + emlx files + AppleScript"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Apple, Mail, macOS, email]
    related_skills: [apple-notes]
prerequisites:
  commands: [python3, osascript]
---

# Apple Mail CLI

A command-line tool (`mail`) to access Apple Mail.app without any cloud dependency. Combines:

- **Fruitmail's SQLite** approach for fast search/list/stats
- **Nathan Grigg's AppleScript** approach for send/compose
- **Direct emlx parsing** for body content and headers

## Location

`~/.local/bin/mail`

## Commands

| Command | Description |
|---------|-------------|
| `mail list` | List recent emails |
| `mail inbox` | Show inbox emails |
| `mail search --from @github` | Search by sender |
| `mail search --subject invoice` | Search by subject |
| `mail search --days 7 --unread` | Last 7 days unread |
| `mail show <id>` | Show email details |
| `mail show <id> --body` | Show with body content |
| `mail show <id> --headers` | Show email headers |
| `mail open <id>` | Open in Mail.app |
| `mail send --to x@y.com --from alt@ex.com --subject Hi --body Hello --yes` | Send email (optional `--from` to select sender account) |
| `mail compose --to x@y.com` | Open compose window |
| `mail accounts` | List accounts |
| `mail stats` | DB statistics |

## How it works

1. **Search/List**: Read-only SQLite on `~/Library/Mail/V{9,10,11}/MailData/Envelope Index`
2. **Body/Headers**: Read `.emlx` files (raw RFC822 message files stored by Apple Mail)
3. **Send/Compose**: AppleScript via `osascript` → Mail.app
4. **Open**: `open <emlx_file>` → Mail.app

## Sender override

Use `--from addr@example.com` to send from a specific account. The AppleScript sets the `sender` property of the outgoing message. Mail.app must have that account configured.

### Exchange (EWS) sending behavior

Exchange/EWS accounts handle AppleScript `send` ASYNCHRONOUSLY:
1. `make new outgoing message {sender:xxx}` → message is created
2. `send newMsg` → message goes to local Outbox, then Exchange server
3. Exchange creates a **server-side draft** in the Exchange Drafts folder
4. Exchange processes and delivers via its own SMTP
5. The draft **persists** — local AppleScript `delete` can't reliably remove it because the Exchange server re-syncs it

**Draft cleanup**: The tool attempts to delete Exchange drafts after sending, but this is best-effort. Exchange may re-create the draft on next server sync.

**iCloud delivery**: When sending from Exchange to iCloud (cross-provider), delivery takes 30-60 seconds. Rapid repeated sends may land in Junk/Spam on the receiving end.

**Default sending account**: AccountOrdering in `~/Library/Containers/com.apple.mail/Data/Library/Preferences/com.apple.mail.plist` determines which account `make new outgoing message` uses by default. The first entry in the array is the default.

### Known limitations in AppleScript

- `set account of newMsg to account "X"` → **error -10006** (cannot set account after creation)
- `make new outgoing message at end of outgoing messages of account "X"` → **error -1728** (cannot access outgoing messages of account through AppleScript)
- These constraints mean you CANNOT force the SMTP relay account in AppleScript. The account is determined at creation time by AccountOrdering.

## Technical details

- EMLX files named by message ROWID: `V<ver>/<acct_uuid>/<mbox>.mbox/<uuid>/Data/<n>/<m>/Messages/<id>.emlx`
- First line of emlx = content-length in bytes, rest = RFC822 message
- Apple epoch offset: +978307200 to convert to Unix timestamp
- Recipient types in DB: type=0 (TO), type=1 (FROM)
- Sender fallback: read From: header from emlx when recipients table has no from entry
- All outgoing Mail.app messages pass through the local Outbox first (`local://.../Outbox`)

## Gotchas

- Mail.app must be running for send/compose AppleScript commands
- Some IMAP accounts don't store FROM in the recipients table — falls back to emlx header parsing
- Always read-only on SQLite DB; uses `?mode=ro` URI parameter
- Chinese locale AppleScript doesn't support `message id N` syntax — use `open` command instead
- **Exchange (EWS) sending always creates server-side drafts** — this is normal Exchange behavior, not a tool bug. The email IS sent (appears in Exchange Sent Items). Draft cleanup is best-effort.
- **`sender` property controls account routing** — Setting `sender` in AppleScript routes the message through the account that owns that email address, regardless of AccountOrdering. Without `sender`, the first account in AccountOrdering is used.
- Cross-account delivery (Exchange → iCloud, Exchange → Gmail) adds 30-60s latency. Rapid repeated sends may land in recipient's Junk/Spam.

## Reference files

- `references/mail-db-schema.md` — complete DB schema, emlx file structure, timestamp conversion, Chinese mailbox URL decoding
- `references/exchange-send-debug.md` — Exchange EWS send behavior, AppleScript limitations, account routing, verification commands
