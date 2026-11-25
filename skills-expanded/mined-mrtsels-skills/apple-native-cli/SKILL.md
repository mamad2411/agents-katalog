---
name: apple-native-cli
description: CLI wrappers for native macOS Apple apps — Notes, Reminders, FindMy, iMessage, Calendar. All require brew-installed CLIs and macOS system permissions.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, findmy, imessage, cli]
    category: apple
---

# Apple Native CLI Tools (macOS)

> Umbrella skill for macOS-native CLI tools that wrap Apple's built-in apps.
> Each tool requires `brew install` + System Settings permission grants.

All four tools share the same setup pattern:
1. `brew install <tap>/<tool>` — install the CLI
2. Grant system permissions when prompted (Automation, Accessibility, Full Disk Access)
3. Tools sync via iCloud — changes appear on all Apple devices

---

## 📝 Apple Notes (`memo`)

**Install:** `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`

**References:** See `references/apple-notes.md` for full command reference.

### Quick commands
```bash
memo notes              # List all notes
memo notes -f "Folder"  # Filter by folder
memo notes -s "query"   # Fuzzy search
memo notes -a "Title"   # Create note
memo notes -e           # Interactive edit
memo notes -d           # Delete (interactive)
memo notes -m           # Move to folder
```

### Rules
- Use Apple Notes for cross-device sync (iPhone/iPad/Mac)
- Use the `memory` tool for agent-internal notes
- Use the `obsidian` skill for Markdown-native knowledge management

---

## ✅ Apple Reminders (`remindctl`)

**Install:** `brew install steipete/tap/remindctl`

**References:** See `references/apple-reminders.md` for full command reference.

### Quick commands
```bash
remindctl               # Today's reminders
remindctl today         # Today
remindctl overdue       # Past due
remindctl all           # Everything
remindctl list          # List all lists
remindctl add "Buy milk" --due tomorrow
remindctl add --title "Call mom" --list Personal --due "2026-02-15 09:00"
remindctl complete 1 2  # Complete by ID
remindctl today --json  # JSON output
```

### Rules
- Clarify: Apple Reminders (synced to phone) vs agent cronjob alert
- `--due` vs `--alarm` are different fields for due time vs notification trigger

---

## 📍 FindMy (`AppleScript + screenshot`)

**Install:** No CLI — uses `osascript` + `screencapture` + optional `peekaboo`

**References:** See `references/findmy.md` for full command reference.

### Quick commands
```bash
# Open FindMy
osascript -e 'tell application "FindMy" to activate'
sleep 3

# Screenshot the FindMy window
screencapture -w -o /tmp/findmy.png

# Switch tabs
osascript -e 'tell application "System Events"
    tell process "FindMy" to click button "Devices" of toolbar 1 of window 1
end tell'
```

### Rules
- Keep FindMy app in foreground for AirTag tracking (updates stop when minimized)
- Use `vision_analyze` to read screenshot content
- Respect privacy — only track devices/items the user owns

---

## 💬 iMessage (`imsg`)

**Install:** `brew install steipete/tap/imsg`

**References:** See `references/imessage.md` for full command reference.

### Quick commands
```bash
imsg chats --limit 10 --json                           # List chats
imsg history --chat-id 1 --limit 20 --json              # View history
imsg send --to "+14155551212" --text "Hello!"           # Send message
imsg send --to "+14155551212" --text "Hi" --file /tmp/img.jpg  # With attachment
imsg send --to "+14155551212" --text "Hi" --service imessage  # Force iMessage
imsg watch --chat-id 1 --attachments                    # Watch for new
```

### Rules
- Always confirm recipient and message content before sending
- Never send to unknown numbers without explicit approval
- Verify file paths exist before attaching
- Don't spam — rate-limit yourself

---

## 📅 Apple Calendar (`sqlite3`)

**No CLI needed** — query Calendar.sqlitedb directly. macOS stores calendar data in SQLite, using **Mac Absolute Time** (seconds since 2001-01-01). Convert to Unix epoch by adding `+ 978307200`.

**References:** See `references/apple-calendar.md` for full command reference and schema.

### Quick queries

```bash
# Upcoming events (excluding holidays/birthdays):
sqlite3 "$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb" "
SELECT datetime(ci.start_date + 978307200, 'unixepoch', 'localtime'),
       ci.summary,
       c.title
FROM CalendarItem ci
JOIN Calendar c ON ci.calendar_id = c.rowid
WHERE ci.start_date + 978307200 >= strftime('%s','now')
  AND ci.hidden = 0
  AND c.title NOT IN ('中國節日','台灣節日','Facebook Birthdays','生日')
ORDER BY ci.start_date
LIMIT 30;"

# List all calendars with event counts:
sqlite3 "$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb" "
SELECT c.title, count(ci.rowid) as events
FROM Calendar c
LEFT JOIN CalendarItem ci ON ci.calendar_id = c.rowid AND ci.hidden = 0
GROUP BY c.rowid ORDER BY c.title;"
```

### Rules
- Database path is `~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb`
- Mac Absolute Time = seconds since 2001-01-01; add 978307200 to get Unix epoch
- Filter out system calendars (holidays, birthdays) when looking for personal events
- Respect privacy — only query when the user explicitly asks about their calendar
