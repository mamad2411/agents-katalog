# Telegram Desktop → CLI Conversion Prompt

Use this prompt with `[skill:electron-to-cli]` (adapted for native apps), `[skill:agent-browser]`,
and `[skill:electron]`. Reference `[skill:discord]` as the working CLI example built with this methodology.

**Key difference:** Telegram Desktop is a **native macOS app** (Qt/C++), NOT Electron. This means
no CDP access, no `--remote-debugging-port`, no webpack modules. The methodology adapts by using
alternative recon paths: Bot API, tdlib, AppleScript, and filesystem inspection.

---

## The Prompt

```
I need you to convert Telegram Desktop into a full CLI tool.

IMPORTANT SKILLS TO USE:
- [skill:electron-to-cli] — the general methodology (adapted for native apps)
- [skill:agent-browser] — for any browser-based testing of the Bot API
- [skill:discord] — reference implementation of a working CLI built with this methodology
- macos-automator source — for AppleScript/Accessibility automation as a fallback

### Phase 1: Reconnaissance (Native App — No CDP)

Since Telegram is native macOS (NOT Electron), we cannot use CDP. Alternative recon:

1. **Check for existing integrations:**
   - Environment: `env | grep -i telegram`
   - Keychain: `security find-generic-password -s "telegram" 2>/dev/null`
   - Phone workspace: `ls ~/.craft-agent-phone/ 2>/dev/null`
   - Existing configs: `find ~/.craft-agent* -name "*telegram*" 2>/dev/null`
   - Python libs: `pip3 list 2>/dev/null | grep -i tele`

2. **Inspect Telegram's local data:**
   - `~/Library/Group Containers/*.Telegram/` (sandboxed data)
   - `~/Library/Application Support/Telegram Desktop/` (if exists)
   - Look for: session files, tdata/ directory, database files, exported data
   - `find ~/Library -maxdepth 4 -name "*telegram*" -o -name "*tdata*" 2>/dev/null`

3. **Test AppleScript support:**
   - `osascript -e 'tell application "Telegram" to get name'`
   - Check Accessibility API access via System Events
   - Test if we can read window contents or send keystrokes

4. **Probe the Telegram Bot API** (if bot token found):
   - `curl -s "https://api.telegram.org/bot<TOKEN>/getMe"`
   - `curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates?limit=5"`

5. **Check for tdlib/telethon availability:**
   - `pip3 show telethon 2>/dev/null`
   - `pip3 show pyrogram 2>/dev/null`
   - `brew list | grep tdlib`

### Phase 2: Architecture Decision

Determine the best approach based on what's available:

**Path A — Bot API (recommended if bot token exists):**
- Bash+curl CLI, same pattern as the Discord CLI
- REST API, fast, reliable, well-documented
- Limited to bot-visible chats (groups where bot is added, direct messages to bot)
- Token in macOS Keychain

**Path B — Telethon/Pyrogram (full user account access):**
- Python wrapper called from a Bash CLI
- Full access to all chats, contacts, media, channels
- Requires initial phone number + 2FA verification
- Session stored in ~/.telegram-cli/

**Path C — AppleScript/Accessibility (fallback, no setup):**
- Use macos-automator source for UI automation
- Can read visible text, click buttons, send messages
- Most fragile, slowest, but works without any API setup

**Path D — Hybrid (ideal):**
- Bot API for reading/sending in bot-accessible chats
- Telethon for full account operations
- AppleScript for app control (open chats, navigate, screenshot)

### Phase 3: Build the CLI

Follow the Discord CLI pattern (see [skill:discord] for reference):

```bash
telegram chats                     # List all chats
telegram messages <chat> [--limit] # Read messages from a chat
telegram send <chat> "text"        # Send a message
telegram search "query"            # Search messages globally
telegram contacts                  # List contacts
telegram unread                    # Show unread messages/counts
telegram me                       # Current user info
telegram media <chat>              # List media in a chat
telegram forward <msg_id> <chat>   # Forward a message
telegram stickers                  # List sticker packs
telegram channels                  # List channels/groups
telegram pin <chat> <msg_id>       # Pin a message
telegram navigate <chat>           # Open chat in Telegram app
telegram screenshot [file]         # Screenshot via screencapture
```

Support --json, --no-input, --limit flags (matching discord/bird/gog patterns).
Token in macOS Keychain (service: telegram-cli-token).
Install to /opt/homebrew/bin/telegram.

### Phase 4: Create Craft Agent Integration

1. Source: ~/.craft-agent/workspaces/my-workspace/sources/telegram/
   - config.json (type: "local", path to source directory)
   - guide.md (CLI reference, command table, user context)
   - permissions.json (read-only commands in Explore mode)

2. Skill: ~/.craft-agent/workspaces/my-workspace/skills/telegram/
   - SKILL.md with command reference and examples
   - requiredSources: [telegram]
   - Include the user's specific context (accounts, groups, channels)

3. Validate:
   - skill_validate({ skillSlug: "telegram" })
   - source_test({ sourceSlug: "telegram" })

### Important Context

- The user's phone workspace at ~/.craft-agent-phone/ may have existing Telegram
  integration — check it and build on it if possible
- The user's pattern for CLIs: discord, bird (Twitter), gog (Google) — match these
- Telegram Desktop is at /Applications/Telegram.app
- For screenshots without CDP: use `screencapture -l $(osascript -e 'tell app "Telegram" to get id of window 1')` or the macos-automator source
```

---

## Telegram vs Discord: Key Differences

| Aspect | Discord (Electron) | Telegram (Native) |
|--------|-------------------|-------------------|
| CDP access | Yes (--remote-debugging-port) | No |
| Token extraction | Fetch interceptor via eval | Bot token or Telethon session |
| REST API | Full user API (unofficial) | Bot API (official) or MTProto |
| Local IPC | discord-ipc-0 socket | None |
| UI automation | agent-browser via CDP | AppleScript/Accessibility |
| Screenshots | agent-browser screenshot | screencapture CLI |
| Auth complexity | Extract from app | Bot token (easy) or phone verify (complex) |

## Skills Referenced

- `[skill:electron-to-cli]` — General methodology (Phase 1-4 pipeline)
- `[skill:agent-browser]` — Browser/CDP automation commands
- `[skill:electron]` — Electron app CDP connection patterns
- `[skill:discord]` — Working reference implementation
- `[skill:claude-prompt-architect]` — For calibrating the skill's SKILL.md description
- `macos-automator` source — For AppleScript/Accessibility fallback
