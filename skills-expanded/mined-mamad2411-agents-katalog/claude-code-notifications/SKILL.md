---
name: claude-code-notifications
description: Use when the user wants to set up sound and custom icon for Claude Code hook notifications on macOS, or when notifications have no sound.
---

# Claude Code Notification Setup

## Overview

Interactively set up sound and custom icon for Claude Code `Notification` hooks on macOS using [growlrrr](https://github.com/moltenbits/growlrrr).

## Prerequisites Check

**Before doing anything else**, verify the environment:

### 1. Must be macOS

```bash
uname -s
```

If the output is NOT `Darwin`, stop immediately and tell the user:
> This skill only works on macOS. growlrrr and the Notification hook are not supported on Linux or Windows.

### 2. Must be Claude Code

Check if running inside Claude Code by verifying the `~/.claude/settings.json` file exists:

```bash
test -f ~/.claude/settings.json && echo "ok" || echo "not found"
```

If not found, stop and tell the user:
> This skill is designed for Claude Code. It does not apply to Codex, Cursor, or other AI tools.

---

## Execution Steps

### Menu — Ask what the user wants to do

First, present this menu and ask the user to choose:

```
What would you like to do?
1. Install (set up notifications from scratch)
2. Change icon
3. Change sound
4. Uninstall
```

Then proceed to the corresponding section below based on their choice.

- **1 → Install**: run Steps 1–8
- **2 → Change icon**: run Steps 4–5 only (skip to Step 4, re-use existing sound from `settings.json`)
- **3 → Change sound**: update the `--sound` value in `~/.claude/settings.json` only
- **4 → Uninstall**: run the Uninstall section

---

### Install

Before starting, show the user this checklist:

```
Installation progress:
- [ ] Detect preferences (icon & sound)
- [ ] Install growlrrr
- [ ] Remove quarantine flag
- [ ] Prepare icon
- [ ] Register virtual app identity with macOS Notification Center (requires clicking Allow on macOS prompt)
- [ ] Test notification
- [ ] Update settings.json
- [ ] Grant notification permission
```

After each step completes, re-print the checklist with that item marked as `[x]`.

---

Follow these steps in order when this skill is invoked:

### Step 1 — Ask the user for preferences

Ask the user two things (can be in one message):

1. **Icon**: Choose one of the following options:
   - Provide an image URL or local file path (PNG recommended)
   - Use the Claude.app icon (if `/Applications/Claude.app` is installed) — Claude will extract it automatically
   - Skip to use the default growlrrr icon
2. **Sound**: Which sound do you want?

| Option | Sound |
|--------|-------|
| `Glass` | Clear, crisp (recommended) |
| `Ping` | Short single tone |
| `Tink` | Soft, subtle |
| `Sosumi` | Classic Mac |
| `Basso` | Low, deep |
| `none` | No sound |

### Step 2 — Install growlrrr

Check if already installed:

```bash
which grrr
```

If not found, install it. **Tell the user this may take a minute:**

```bash
brew tap moltenbits/tap && brew install growlrrr
```

### Step 3 — Remove macOS quarantine flag

growlrrr is not yet signed by an Apple Developer account:

```bash
xattr -cr /Applications/growlrrr.app
```

### Step 4 — Prepare icon

**If the user provided a URL**, download it:

```bash
curl -fsSL "<URL>" -o /tmp/notification-icon.png
```

**If the user wants the Claude.app icon**, first check it's installed:

```bash
test -d /Applications/Claude.app && echo "found" || echo "not found"
```

If found, extract the icon:

```bash
iconutil -c iconset /Applications/Claude.app/Contents/Resources/electron.icns -o /tmp/claude.iconset && cp /tmp/claude.iconset/icon_512x512.png /tmp/notification-icon.png
```

**If the user gave a local path**, use it directly.

**If the user skipped**, omit `--appIcon` in Step 5.

### Step 5 — Register virtual app identity with macOS Notification Center

**Always remove the existing app first** (no-op if it doesn't exist):

```bash
grrr apps remove Claude-Code --force || true
```

Then create fresh:

```bash
grrr apps add --appId Claude-Code --appIcon '/tmp/notification-icon.png'
# or without icon:
grrr apps add --appId Claude-Code
```

> **Important:** If the user set a custom icon, tell them that macOS caches notification icons — a **reboot is required** for the new icon to appear.

> **Note:** If the user just uninstalled and is immediately reinstalling, there may be an app bundle cache. If `grrr apps add` fails or behaves unexpectedly, a reboot is required before retrying.

### Step 6 — Test the notification

> **Before running the next command**, warn the user:
> When the first notification is sent, macOS will show a permission prompt in the top-right corner — **"Claude-Code" Notifications** with an **Options → Allow** button. Watch for it and click **Allow** as soon as it appears.

```bash
grrr --appId Claude-Code --title 'Claude Code' --sound <SOUND> 'Claude Code needs your attention'
```

Ask the user: did the Allow prompt appear? Did they click Allow?

> **Note:** The test notification itself may not play sound yet. Sound will only work after `settings.json` is updated and Claude Code is restarted (Step 7–8).

### Step 7 — Update `~/.claude/settings.json`

Add or replace the `Notification` hook:

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "grrr --appId Claude-Code --title 'Claude Code' --sound <SOUND> 'Claude Code needs your attention'"
          }
        ]
      }
    ]
  }
}
```

### Step 8 — Restart Claude Code and grant notification permission

Tell the user:
1. **Restart Claude Code** — the `settings.json` hook only takes effect after restarting.
2. If notifications still don't appear, open **System Settings → Notifications → Claude-Code** and make sure notifications are allowed.

## Uninstall

Before starting, show the user this checklist:

```
Uninstall progress:
- [ ] Remove Notification hook from settings.json
- [ ] Deregister virtual app identity from macOS Notification Center
- [ ] Uninstall growlrrr
```

After each step completes, re-print the checklist with that item marked as `[x]`.

---

If the user wants to remove everything:

### Step 1 — Remove the Notification hook from `~/.claude/settings.json`

Delete the entire `Notification` entry under `hooks`.

### Step 2 — Deregister virtual app identity from macOS Notification Center

```bash
grrr apps remove Claude-Code --force || true
```

### Step 3 — Uninstall growlrrr

```bash
brew uninstall growlrrr && brew untap moltenbits/tap
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No notification appears | System Settings → Notifications → Claude-Code → enable |
| Command hangs | Run `xattr -cr /Applications/growlrrr.app` again |
| `appId` error | appId must use only letters, numbers, hyphens, underscores |
| Wrong icon showing | macOS caches notification icons — reboot to fully clear the cache |
| Hook has no effect | Restart Claude Code after editing `settings.json` |
