---
name: whatsapp-web
description: WhatsApp Web automation via Playwright and Chrome CDP. Use when the user needs to open WhatsApp Web, launch the WhatsApp Web browser, verify phone numbers on WhatsApp, send WhatsApp messages, read recent chat messages or chat history, read the last reply from a contact, list chats in the sidebar, count chats, count pinned chats, list unread chats, count unread messages, check if a number is registered on WhatsApp, add a new WhatsApp contact, save a number to contacts, automate WhatsApp Web login, or perform bulk number verification. Triggers include requests to "open WhatsApp Web", "buka WhatsApp Web", "launch WhatsApp", "check this number on WhatsApp", "send a WhatsApp message", "verify WhatsApp numbers", "read WhatsApp messages", "list WhatsApp messages", "show recent WhatsApp chat", "ambil pesan WhatsApp", "open WhatsApp chat", "batch check numbers", "list my WhatsApp chats", "ada berapa chat", "berapa pinned chat", "show pinned chats", "ada berapa chat yang belum dibaca", "unread chats", "pesan yang belum dibaca", "how many unread messages", "X bales apa", "apa chat terakhir X", "chat terakhir dari X", "last reply from X", "what did X say", "what did X reply", "add to contacts", "save contact", "add new contact", "simpan kontak", "tambah kontak", "save this number", "pin chat", "unpin chat", "pin this chat", "sematkan chat", "lepas sematan", "pin X", "unpin X", "create group", "new group", "buat grup", "bikin grup baru", "make a whatsapp group", "delete group", "hapus grup", "bubarkan grup", "kick all members", "keluar dan hapus grup", "teardown group", "exit group", "leave group", "keluar grup", "keluar dari grup", "delete chat", "hapus chat", "clear chat", "remove this chat", or any task requiring programmatic WhatsApp Web interaction. For any "open/launch/buka WhatsApp Web" request, run `scripts/login.py` WITHOUT `--wait` — the script exits immediately after opening the window so the agent stays responsive. Never use `--wait` unless the user explicitly asks the agent to wait for them to sign in. For reading messages, run `scripts/read_messages.py --from <name>`. For the last reply from a contact (prompts like "X bales apa"), run `scripts/last_reply.py --from <name>`; add `--any-direction` if the user wants the very last message regardless of who sent it (prompts like "apa chat terakhir X"). For listing chats, run `scripts/list_chats.py`. For pinned chats, run `scripts/list_pinned.py`. For unread chats, run `scripts/list_unread.py`. For adding a contact (prompts like "add this number to contacts", "simpan jadi kontak"), ALWAYS ask the user for First Name, Last Name (optional), and whether to sync the contact to the phone before running `scripts/add_contact.py --phone <number> --first-name <first> [--last-name <last>] [--sync]`. For pinning or unpinning a chat (prompts like "pin chat Ezra", "sematkan chat X", "unpin X"), run `scripts/pin_chat.py --to <name-or-number>` or add `--unpin` to unpin. WhatsApp Web allows at most 3 pinned chats — if the pin action becomes a no-op with `already=true`, tell the user the chat is already pinned; if pinning fails due to the 3-pin cap, tell the user they need to unpin something first. For exiting a group without deleting it from the chat list (prompts like "keluar grup X", "leave group X"), ALWAYS ask the user to confirm first ("Keluar dari grup X? Grup tetap ada di chat list sampai kamu hapus manual."), then run `scripts/exit_group.py --name <group-name> --confirm`. For deleting a chat from the sidebar (prompts like "hapus chat Ezra", "delete chat X", "clear chat"), ALWAYS ask the user to confirm first ("Hapus chat X dari sidebar? Ga bisa di-undo."), then run `scripts/delete_chat.py --to <name-or-number> --confirm`. For active groups you want fully gone, prefer `scripts/delete_group.py` (kick-all + exit + delete) over calling exit + delete-chat separately. For deleting a group (prompts like "hapus grup X", "bubarkan grup"), ALWAYS ask the user to confirm first ("This will kick every member, exit the group, and remove it from your chat list. Lanjut?"). Only after the user confirms, run `scripts/delete_group.py --name <group-name> --confirm`. The script refuses to run without `--confirm`. After it returns, report the `status` field back — "deleted" = fully gone; "exited" = you're out but delete didn't finalize; "partial" = something failed mid-way. Also surface the `skipped` list so the user knows which members couldn't be kicked (usually because the caller isn't admin). For creating a new group (prompts like "buat grup baru", "create a group"), ALWAYS ask the user for the group name AND the members. Members can be many — accept comma-separated input and ask again (repeatably) if the user has more to add, stopping when they signal done. Then run `scripts/create_group.py --name <name> --members <a,b,c> [--members ...]`. After the script returns, check the `failed` array — if any member failed to match a contact, tell the user which ones so they can add them manually later. Always keep responses to the user friendly and non-technical (say "Opening WhatsApp Web..." instead of "Starting Chrome with CDP").
license: Proprietary
compatibility: Requires Python 3.10+, Google Chrome, and Playwright. macOS or Linux only.
metadata:
  author: lazuardy-tech
  version: "1.0"
---

# whatsapp-web

WhatsApp Web automation via Playwright + Chrome CDP. Scripts output JSON to stdout.

## Setup

Requires Python 3.10+, Google Chrome, and Playwright.

First-time login — scan QR code once:

```bash
python3 scripts/login.py
```

This opens Chrome, navigates to web.whatsapp.com, reports the current login state, and **exits immediately** so the calling agent stays responsive. If the user still needs to scan the QR code, tell them to scan it from their phone and re-run the task once signed in. Chrome profile persists in `/tmp/whatsapp-web/chrome_profile/`, so no re-scan is needed after the first login.

## Available Scripts

### Check if number(s) are on WhatsApp

```bash
# Single number
python3 scripts/check_number.py --phone 081234567890

# Multiple numbers (comma-separated)
python3 scripts/check_number.py --phones 08111,08222,08333
```

Output: `{"081234567890": true}`

### Add a new contact

```bash
python3 scripts/add_contact.py --phone 081234567890 --first-name Ezra
python3 scripts/add_contact.py --phone 081234567890 --first-name Ezra \
    --last-name Wijaya --sync
```

Output: `{"status": "saved", "first_name": "Ezra", "last_name": "Wijaya", "phone": "081234567890", "sync_to_phone": true}`

**Agent must ask the user for First Name, Last Name (optional), and whether to sync the contact to the phone before invoking this script.** Pass `--sync` only if the user confirms syncing.

### Create a group

```bash
python3 scripts/create_group.py --name "LT Team" --members "Ezra,Adit,Rani"

# Members can be repeated — useful when the user provides them in batches
python3 scripts/create_group.py --name "LT Team" \
    --members "Ezra,081234567890" --members "Adit"
```

Output:

```json
{
  "status": "created",
  "name": "LT Team",
  "requested_members": ["Ezra", "Adit", "Rani"],
  "added": ["Ezra", "Adit"],
  "failed": ["Rani"]
}
```

`failed` lists members whose name/number didn't match a suggestion and were skipped. The group is still created as long as at least one member is added.

**Agent must ask the user for both the group name and the members.** Members can be many — accept comma-separated input and repeat the prompt if the user has more to add. Combine everything into one or multiple `--members` flags.

### Exit (leave) a group

```bash
python3 scripts/exit_group.py --name "LT Team" --confirm
```

Output: `{"status": "exited", "name": "LT Team", "exited": true, "already": false}`

If the menu has no Exit option (already left), returns `{"status": "noop", "exited": false, "already": true}`. The group stays visible in your chat list as read-only — use `delete_chat.py` afterwards to hide it.

**`--confirm` required.** Leaving is reversible only if an admin re-invites you.

### Delete a chat

```bash
python3 scripts/delete_chat.py --to "Ezra" --confirm
python3 scripts/delete_chat.py --to 081234567890 --confirm
```

Output: `{"status": "deleted", "name_or_number": "Ezra", "deleted": true}`

Removes the chat from YOUR sidebar and clears your copy of the history. The other party still sees the conversation. Not reversible.

For active groups WA won't offer "Delete chat" — use `exit_group.py` first, or `delete_group.py` for the full teardown.

**`--confirm` required.**

### Delete a group (kick all → exit → delete)

```bash
python3 scripts/delete_group.py --name "LT Marketing Team" --confirm
```

Output:

```json
{
  "status": "deleted",
  "name": "LT Marketing Team",
  "kicked": ["Adit", "Rani"],
  "skipped": [],
  "exited": true,
  "deleted": true
}
```

`status` values:
- `deleted` — kicked all kickable members, exited the group, removed it from the chat list.
- `exited` — exit succeeded but delete didn't finalize (you can still remove it from the sidebar manually).
- `partial` — something stopped before exit.

`skipped` lists members whose Remove action didn't surface — usually means the caller isn't a group admin, so those members remain in the group.

**DESTRUCTIVE.** The script refuses to run without `--confirm`. Agent must ask the user for explicit confirmation before passing `--confirm`.

### Pin / unpin a chat

```bash
python3 scripts/pin_chat.py --to "Ezra"
python3 scripts/pin_chat.py --to "Ezra" --unpin
python3 scripts/pin_chat.py --to 081234567890
```

Output examples:
- `{"status": "pinned", "action": "pin", "name_or_number": "Ezra", "already": false}`
- `{"status": "noop", "action": "pin", "name_or_number": "Ezra", "already": true}` (already pinned)
- `{"status": "unpinned", "action": "unpin", ...}`

WhatsApp Web allows at most 3 pinned chats. If pinning a 4th, WA shows a modal the script auto-dismisses — the chat stays unpinned and `status` stays `unpinned` (tell the user to unpin something first).

### Send a message

```bash
python3 scripts/send_message.py --to "Ezra" --message "Hello!"
python3 scripts/send_message.py --to 081234567890 --message "Hi there"
```

Output: `{"status": "sent", "to": "Ezra"}`

### Read recent messages from a chat

```bash
python3 scripts/read_messages.py --from "Ezra"
python3 scripts/read_messages.py --from 081234567890 --count 20
```

Output:

```json
{
  "from": "Ezra",
  "count": 10,
  "messages": [
    {"direction": "in", "sender": "Ezra", "time": "08.42", "date": "17/04/2026", "text": "..."},
    {"direction": "out", "sender": "Me", "time": "08.43", "date": "17/04/2026", "text": "..."}
  ]
}
```

`direction` is `"in"` (received) or `"out"` (sent by the logged-in user).

### Last reply from a contact

```bash
# Last incoming message (what the contact said) — maps to "X bales apa"
python3 scripts/last_reply.py --from "Ezra"

# Last message regardless of sender — maps to "apa chat terakhir X"
python3 scripts/last_reply.py --from "Ezra" --any-direction
```

Output:

```json
{
  "from": "Ezra",
  "mode": "incoming",
  "message": {
    "direction": "in",
    "sender": "Ezra",
    "time": "08.42",
    "date": "17/04/2026",
    "text": "oke siap"
  }
}
```

`message` is `null` if no matching message is visible (e.g. asking for an incoming message in a chat the user has only sent to).

### List chats in the sidebar

```bash
python3 scripts/list_chats.py                 # top 50 chats
python3 scripts/list_chats.py --limit 20      # top 20
python3 scripts/list_chats.py --names-only    # drop previews
```

Output: `{"total_in_sidebar": 188, "returned": 50, "chats": [{"name": "...", "preview": "...", "pinned": false}, ...]}`

`total_in_sidebar` is the full chat count WhatsApp reports (all archived + active), `returned` is how many entries the script actually collected.

### List pinned chats

```bash
python3 scripts/list_pinned.py
```

Output: `{"count": 2, "chats": [{"name": "...", "preview": "...", "pinned": true}, ...]}`

WhatsApp Web allows at most 3 pinned chats.

### List unread chats / count unread messages

```bash
python3 scripts/list_unread.py                 # scan top 50 rows
python3 scripts/list_unread.py --limit 100     # scan deeper
python3 scripts/list_unread.py --count-only    # just the totals
```

Output:

```json
{
  "chat_count": 3,
  "message_count": 46,
  "chats": [
    {"name": "LT Marketing Team", "unread_count": 33, "unread": true, "pinned": false, ...}
  ]
}
```

`chat_count` = number of chats with unread messages; `message_count` = sum of per-chat unread counts. Only chats whose rows are scanned are counted — raise `--limit` if you have many chats and want to look deeper.

### Open WhatsApp Web / check login state

```bash
# Default: open WA Web, report state, exit immediately (non-blocking)
python3 scripts/login.py

# Block until the user signs in (only when explicitly requested)
python3 scripts/login.py --wait
python3 scripts/login.py --wait --timeout 120
```

Default mode exits right after opening the window — agents MUST NOT use `--wait` unless the user explicitly asks to wait for login, otherwise the agent will appear to hang while the user scans the QR code.

Output examples:
- `{"state": "logged_in"}`
- `{"state": "qr_code", "action": "Scan the QR code with your phone", "message": "..."}`
- `{"state": "loading", "message": "..."}`
- `{"state": "timeout", "error": "..."}` (only with `--wait`)
- `{"state": "error", "error": "..."}` — Chrome / CDP / navigation failed

`login.py` never crashes with a traceback: Chrome-launch, CDP-connect, and navigation failures are reported as `{"state": "error", ...}` with exit code 1, same as a `--wait` timeout.

## Script conventions

- All scripts output JSON to stdout, diagnostics to stderr
- Exit codes: `0` = success, `1` = login required / login error / wait timeout, `2` = contact not found, `3` = destructive script missing `--confirm`
- Destructive scripts (`delete_group.py`, `exit_group.py`, `delete_chat.py`) refuse to run without `--confirm` (exit code 3). Agent MUST ask the user to confirm first before invoking them
- Run `python3 scripts/<name>.py --help` for usage
- Scripts use PEP 723 inline dependencies — run with `uv run` or install Playwright manually

## Important notes

- Chrome persists across runs — never killed by the skill
- Anti-ban delay (default 3s) between operations
- Phone formatting defaults to Indonesian numbers (+62)
- All interactions are keyboard/text-based (no CSS selectors) for resilience against WA Web DOM changes
- Number verification checks multiple phone format variants for accuracy
