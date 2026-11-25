# /notify — Multi-Channel Notification

Send notifications via Telegram, macOS, and sound.

## Triggers

- `/notify` — send notification
- `notify me`, `send notification`, `bildirim gönder`

## Usage

```bash
bash ~/.claude/skills/notifications/notify.sh --message "text" [--channel telegram|macos|sound|all] [--event build-error|ai-question|task-done]
```

## Examples

```bash
# Notify all channels
bash notify.sh --message "Sprint tamamlandı" --channel all

# Only Telegram
bash notify.sh --channel telegram --message "Backup done" --emoji "💾"

# DevFocus event
bash notify.sh --event build-error --message "flutter analyze failed"
bash notify.sh --event ai-question --message "Approve DB migration?"
bash notify.sh --event task-done --message "Feature X deployed"
```

## Channels

| Channel | What it does |
|---------|-------------|
| `telegram` | Sends Telegram message (requires TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID) |
| `macos` | macOS native notification popup |
| `sound` | Plays alert sound (afplay Glass.aiff) |
| `all` | sound + macos + telegram (if configured) |

## Events (DevFocus)

| Event | What happens |
|-------|-------------|
| `build-error` | Pause music + alert + notify |
| `ai-question` | Pause music + bring terminal to front + notify |
| `task-done` | Resume music + success notification |
