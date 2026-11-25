---
name: heartbeat
description: Nolty's every-30-min self-check during waking hours. Detects Claude Code version drift and self-heals. Scans urgent email + upcoming meetings, alerts via Telegram if something needs attention.
---

# Heartbeat

You are Nolty, running a scheduled heartbeat.

If you see a `[cron model:X effort:Y]` suffix, you were fired by `cron-runner.py`. Spawn a Task sub-agent with the specified model + effort. The sub-agent runs the steps below and has access to your `reply` MCP tool.

cron-runner fires this every 30 minutes, 24/7 — so the **skill itself** gates off-hours. Never send a Telegram outside the user's active hours (see `USER.md`), even if something seems urgent.

---

## STEP 0 — Time gate (do this FIRST, before anything else)

Get the current hour in the user's timezone (look up `Timezone` in `USER.md`; default `America/Chicago`):

```bash
TZ='America/Chicago' date '+%Y-%m-%d %H:%M %Z (hour=%H, dow=%u)'
```

Parse the `hour=HH` value as an integer.

**Decision:**
- If `hour < 7` OR `hour >= 23` → **QUIET HOURS.** Respond with the exact text `QUIET_HOURS <timestamp>` and exit. Make NO further tool calls. No file reads. No email checks. No Telegram. Nothing.
- Otherwise, continue to STEP 0.5.

This rule is absolute. Customize the 7/23 bounds by reading active hours from `USER.md` if set.

---

## STEP 0.5 — Claude Code version-drift self-heal

Claude Code auto-upgrades its binary symlink. When an upgrade lands, the supervisor daemon self-restarts but Nolty's tmux-resident process stays on the OLD binary — the Telegram plugin's bridge breaks (inbound still works, outbound `reply` fails silently). Detect drift and trigger a detached restart.

Run this block:

```bash
PANE_PID=$(tmux list-panes -t CC_running_like_OC -F '#{pane_pid}' 2>/dev/null | head -1)
CLAUDE_PID=$(pgrep -P "$PANE_PID" -f 'claude.*--channels' 2>/dev/null | head -1)
RUNNING=$(lsof -p "$CLAUDE_PID" 2>/dev/null | grep -oE 'versions/[0-9]+\.[0-9]+\.[0-9]+' | head -1 | cut -d/ -f2)
LATEST=$(ls -1 ~/.local/share/claude/versions/ 2>/dev/null | sort -V | tail -1)
echo "claude version: running=$RUNNING latest=$LATEST"

if [ -n "$RUNNING" ] && [ -n "$LATEST" ] && [ "$RUNNING" != "$LATEST" ]; then
  NOLTY_HOME="${NOLTY_HOME:-$HOME/Documents/CodingProjects/nolty}"
  nohup "$NOLTY_HOME/clawd-restart.sh" > /tmp/heartbeat-restart-$(date +%s).log 2>&1 &
  disown 2>/dev/null
  echo "VERSION_DRIFT_RESTART_TRIGGERED running=$RUNNING latest=$LATEST"
  exit 0
fi
```

**Decision:**
- `RUNNING` empty (couldn't detect) → continue. Don't fail just because detection failed.
- `RUNNING == LATEST` → continue.
- `RUNNING != LATEST` → restart triggered. Tmux session (and you) will die within seconds. Do NOT do other steps. Exit with `VERSION_DRIFT_RESTART_TRIGGERED`.

`nohup ... &` is critical — the restart script must survive the kill of its parent.

---

## STEP 0.6 — Bun listener presence check

The Telegram plugin spawns a `bun` child process that long-polls Telegram for inbound messages. It dies silently under several conditions: Mac sleep/wake severs the TCP connection, CC binary swaps leave it zombie, the plugin's "experimental" channel gets unreliable over long uptime. When bun is dead, the main claude process is still alive — but inbound Telegram messages don't reach the agent. No error is surfaced anywhere.

Same self-heal pattern as STEP 0.5, but on a different signal.

Run this block:

```bash
NOLTY_HOME="${NOLTY_HOME:-$HOME/Documents/CodingProjects/nolty}"
BUN_PID=$(pgrep -f 'bun.*telegram' 2>/dev/null | head -1)
if [ -z "$BUN_PID" ]; then
  echo "BUN_LISTENER_MISSING — triggering restart"
  nohup "$NOLTY_HOME/clawd-restart.sh" > /tmp/heartbeat-bun-restart-$(date +%s).log 2>&1 &
  disown 2>/dev/null
  echo "BUN_RESTART_TRIGGERED"
  exit 0
else
  echo "bun listener alive (PID $BUN_PID)"
fi
```

**Decision:**
- bun process found → continue to STEP 1.
- bun process missing → detached restart triggered. Tmux + main claude + your own sub-agent will die within seconds when `clawd-restart.sh` kills the session. Do NOT continue. Exit with sentinel `BUN_RESTART_TRIGGERED`.

Same `nohup ... &` discipline as STEP 0.5 — the restart script must outlive its parent.

This catches the silent-Telegram-death failure mode within 30 min (the heartbeat cadence), the same way STEP 0.5 catches version drift.

---

## STEP 1 — Identity refresh (only during active hours)

Briefly read these to stay grounded:
- `SOUL.md`
- `IDENTITY.md`
- `MEMORY.md`

---

## STEP 2 — Urgent unread email

```bash
/opt/homebrew/bin/gog gmail search "is:unread" --limit 10 --account YOUR_EMAIL@example.com
```

(Replace `YOUR_EMAIL` with the value from `USER.md`. If you don't use `gog`, substitute `mcp__claude_ai_Gmail__search_threads`.)

Flag only:
- Client replies
- Meeting reschedules / confirmations
- Time-sensitive items (invoices due, deadlines, urgent requests from known contacts)

Skip: newsletters, promotions, automated notifications, OOO auto-replies, LinkedIn/Apollo summaries, **LinkedIn InMail messages** (any email from LinkedIn with "InMail" in subject or body).

**Attribution rule:** When reporting a thread, show who sent the **most recent message** — not the thread starter. Parse the `From` header of the newest unread message in the thread.

---

## STEP 3 — Upcoming meeting (next 60 min)

```bash
/opt/homebrew/bin/gog calendar list --today --account YOUR_EMAIL@example.com
```

**Compute time delta in bash — do NOT do mental math.** For each event:

```bash
now_epoch=$(TZ='America/Chicago' date +%s)
meeting_time="HH:MM"  # replace with actual start time from calendar
meeting_epoch=$(TZ='America/Chicago' date -j -f "%Y-%m-%d %H:%M" "$(TZ='America/Chicago' date +%Y-%m-%d) $meeting_time" +%s)
diff_min=$(( (meeting_epoch - now_epoch) / 60 ))
echo "$diff_min minutes until meeting"
```

- Only flag if `diff_min` is between 1 and 60 (inclusive)
- Check `memory/heartbeat-state.json` → `remindedEvents` — if already reminded, skip
- Skip all-day events and events already in progress (`diff_min` <= 0)

---

## STEP 4 — Alert (only if anything from steps 2-3 needs attention)

Combine into ONE concise Telegram (under 300 chars, Markdown supported) and send via the `reply` MCP tool with `chat_id` from `USER.md`. Start with "❗" so the user sees urgency at a glance.

If a meeting was alerted, append it to `memory/heartbeat-state.json` → `remindedEvents` as `"<title> <YYYY-MM-DD>"` to prevent repeat pings.

---

## STEP 5 — Silence

If nothing urgent, respond with `HEARTBEAT_OK <timestamp from STEP 0>` and exit. Do NOT send a silent Telegram.

---

## Hard rules

1. **Quiet hours are absolute.** Outside active hours → `QUIET_HOURS` and exit, no tool calls.
2. **Use the `reply` MCP tool** for Telegram, not `send-telegram.sh`.
3. **Never send a silent "nothing to report" Telegram.** Silence = `HEARTBEAT_OK` response only.
4. **Deduplicate meeting reminders** via `remindedEvents`.
