---
name: cc-usage-check
description: Daily 11:45pm — capture Claude Code's /status TUI via nested tmux, parse weekly usage %, report via Telegram. EXAMPLE — adapt to your own setup.
---

# CC Usage Check (example)

> **EXAMPLE.** Demonstrates the "tmux-in-tmux" pattern: spawn a nested tmux to capture a TUI's alternate-screen output that you can't access via stdout.

If you see `[cron model:X effort:Y]` suffix, spawn a Haiku sub-agent.

## Why nested tmux

`claude --status` opens a TUI in an alternate-screen buffer. Standard stdout capture doesn't see what's on screen. The workaround: spawn a nested tmux session, run claude inside it, send `/status`, capture-pane to get the rendered text.

## Procedure

```bash
# Clean up any leftover session
tmux kill-session -t cc-usage 2>/dev/null

# Spawn a fresh nested tmux
tmux new-session -d -s cc-usage -x 200 -y 50

# Launch claude in it
tmux send-keys -t cc-usage "$HOME/.local/bin/claude --permission-mode bypassPermissions" Enter
sleep 8

# Send /status
tmux send-keys -t cc-usage "/status" Enter
sleep 2

# Navigate to Usage tab (key varies — check your CC version)
tmux send-keys -t cc-usage "u" Enter
sleep 1

# Capture the pane
output=$(tmux capture-pane -t cc-usage -p)
echo "$output" > /tmp/cc-status-capture.txt

# Clean up
sleep 3
tmux kill-session -t cc-usage
```

## Parse

From `output`, extract the line containing `Current week (all models)` and its percentage. Compute:

- `actual_pct` — the parsed % from the capture
- `day_of_week_num` — which day of your usage week you're on (1-7)
- `projected_pct` — what % you'd be at if usage were perfectly linear (day_num / 7 * 100)
- `diff` — actual minus projected

## Send Telegram

`reply` MCP tool with `chat_id` from `USER.md`:

- If diff > 0 (over projected): `"📊 CC Weekly: {actual}% — {diff}% over projected ({day_num}/7 days)"`
- If diff <= 0 (under projected): `"📊 CC Weekly: {actual}% — {abs(diff)}% under projected ({day_num}/7 days)"`

ALWAYS send — there is no silent mode. The whole point is to see drift before it becomes a 100% week.

## Failure handling

If the parse fails or pane capture is empty: `reply` "⚠️ CC usage check failed — couldn't parse /status output. Manual check needed."
