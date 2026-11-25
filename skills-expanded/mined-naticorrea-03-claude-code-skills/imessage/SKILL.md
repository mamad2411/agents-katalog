---
name: imessage
description: Read and send iMessages via local macOS capabilities (no third-party API). Two modes. Send mode drafts a message and uses AppleScript (`osascript`) on explicit "send it" and requires only Automation, Messages permission (scoped, revocable). Read mode pulls from `~/Library/Messages/chat.db` via sqlite3 and requires Full Disk Access for Terminal, which is a broad permission, so it is opt-in only. Trigger on phrases like "text [person]", "iMessage [person]", "draft an imessage", "read my texts from [person]", "what did [person] text me", "/imessage". Defaults to drafts-only, never auto-sends.
---

# imessage

Read and send iMessages locally. No MCP server, no cloud API. Two modes with very different permission costs.

**Requires a Mac with iMessage set up:** Messages must be signed into your Apple ID and able to send from this Mac. macOS only, this does not work on Windows, Linux, or from a phone alone.

## When to use

- "Text Alex that I'm running 10 min late"
- "Draft an iMessage to [person] saying..."
- "Send Sam a quick text about..."
- "What did [person] text me yesterday?"
- "Pull up my last thread with [person]"

Do NOT use for:
- Slack or other chat apps (use their own tools)
- Email (use an email tool)
- SMS to non-Apple recipients without confirming the contact has iMessage (AppleScript can still route as SMS via the iPhone bridge, but only if Continuity is on)

## Modes

### Send mode (default, low-permission)

1. Confirm recipient and message. Match the tone to the recipient (casual with friends, more measured with colleagues).
2. Show the draft. Wait for "send it" or equivalent.
3. On approval, send via AppleScript:

```bash
osascript <<'APPLESCRIPT'
tell application "Messages"
  set targetService to 1st service whose service type = iMessage
  set targetBuddy to buddy "PHONE_OR_APPLE_ID" of targetService
  send "MESSAGE_TEXT" to targetBuddy
end tell
APPLESCRIPT
```

Replace `PHONE_OR_APPLE_ID` with the recipient's phone (E.164, e.g. `+19175551234`) or Apple ID email. Replace `MESSAGE_TEXT` with the drafted body, escaping quotes and backslashes for AppleScript.

**Permission required:** System Settings, Privacy & Security, Automation, enable Messages under Terminal (or iTerm, or whatever shell host Claude Code runs in).

**Permission NOT required:** Full Disk Access. Send mode does not read chat.db.

### Read mode (opt-in, high-permission)

Required for: pulling thread history, searching past messages, triaging recent texts.

**Cost:** Reading `~/Library/Messages/chat.db` requires Full Disk Access for Terminal. FDA is a broad, system-level permission. Once granted, the terminal binary can read all protected user data (Photos, Health, banking caches, and more), not just iMessages. This is the OS design, not a skill choice.

Before invoking read mode for the first time in a session, warn the user once:

> Heads up: reading iMessages needs Full Disk Access on Terminal, which is a broad permission. Send-only mode doesn't need it. Want me to proceed with read access, or stick to drafts and sends?

If the user confirms, proceed:

```bash
# Copy first to avoid locking conflicts with Messages.app
cp ~/Library/Messages/chat.db /tmp/chat.db.snap
sqlite3 /tmp/chat.db.snap "SELECT datetime(message.date/1000000000 + 978307200, 'unixepoch', 'localtime') as ts, handle.id as sender, message.is_from_me, message.text FROM message LEFT JOIN handle ON message.handle_id = handle.ROWID WHERE message.text IS NOT NULL ORDER BY message.date DESC LIMIT 20;"
rm /tmp/chat.db.snap
```

Schema notes:
- `message.date` is nanoseconds since 2001-01-01 UTC. Convert: `date/1000000000 + 978307200` gives Unix epoch.
- `handle.id` is the other party's phone or Apple ID.
- `message.is_from_me` is 1 if you sent it, 0 if received.
- `message.text` is null for attachment-only messages and reactions; check the `attributedBody` blob for newer iOS versions.
- Threads/conversations live in the `chat` table joined via `chat_message_join`.

Always copy chat.db to /tmp first, query the copy, delete the copy. Direct queries against the live file can lock when Messages.app is open.

## Recipient lookup

When the user says "text Alex", resolve the contact:

1. If you already have the person's phone (E.164) or Apple ID, use it.
2. You can keep a simple lookup file at `~/.claude/data/contacts.json` mapping names to handles, and read it if it exists. Do not create it if it is missing.
3. If the person is not found, ask once: "What's [name]'s phone or Apple ID?"

Do NOT scrape Contacts.app via AppleScript without confirming; that adds another permission surface.

## Hard rules

- Drafts only by default. Never send without an explicit "send it" from the user in the same turn.
- One recipient at a time unless the user says "group" or names multiple people. A group send needs the existing chat's identifier (AppleScript can't address a group by member list alone), so confirm the exact target before sending.
- Never auto-reply to incoming messages. Read mode is read-only; deciding what to answer is the user's call.
- If AppleScript send fails (no Automation permission, Messages.app not running, recipient not on iMessage), surface the error and the draft so the user can paste manually.
- Do not store message bodies in any log or cache.

## First-run setup

When the user first invokes this skill, check whether permissions are configured. If `osascript -e 'tell application "System Events" to return name of every process'` fails with a permission error, the Automation permission isn't granted yet. Direct the user to:

System Settings, Privacy & Security, Automation, Terminal (or iTerm), enable Messages

For read mode, additionally:

System Settings, Privacy & Security, Full Disk Access, enable Terminal (or iTerm)

After granting, the terminal app must be fully quit and relaunched. The Claude Code session needs to restart inside the newly-permissioned terminal.
