---
name: dump-channel
description: user wants to archive, dump, or back up an entire Telegram channel or chat history to NDJSON with all media files downloaded. Full history.
allowed-tools: Bash, Read, Grep, Glob
---

# Dump Telegram Channel History

Archive a complete Telegram channel/group/chat to NDJSON + downloaded media files.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

1. Session must exist: `~/.local/share/gramjs/<profile>.session`
   - If missing, run `/tlg:setup` first
2. User must be subscribed to (or a member of) the target channel/chat

## Usage

```bash
/usr/bin/env bash << 'EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Full dump: NDJSON + all media (photos, videos, documents)
bun "$SCRIPT" dump @ChannelName ./output/ChannelName

# NDJSON only (skip media downloads — much faster)
bun "$SCRIPT" dump @ChannelName ./output/ChannelName --no-media

# Dump by numeric chat ID
bun "$SCRIPT" dump -1001234567890 ./output/MyChannel

# Use a different profile
bun "$SCRIPT" -p missterryli dump @ChannelName ./output/ChannelName
EOF
```

## Parameters

| Parameter    | Type       | Description                                                |
| ------------ | ---------- | ---------------------------------------------------------- |
| chat         | string/int | Channel username (@name) or numeric chat ID                |
| output       | path       | Output directory (messages.ndjson + media/ created inside) |
| `--no-media` | flag       | Skip media downloads, produce NDJSON only                  |

## Output Structure

```
output/ChannelName/
├── messages.ndjson   ← one JSON object per line, chronological (oldest first)
└── media/
    ├── 6.jpg         ← named by message ID for cross-referencing
    ├── 12.png
    ├── 45.mp4
    └── ...
```

## NDJSON Record Schema

Each line is a JSON object with these fields:

| Field             | Type        | Description                                     |
| ----------------- | ----------- | ----------------------------------------------- |
| `id`              | int         | Telegram message ID                             |
| `date`            | string      | ISO 8601 timestamp with timezone                |
| `text`            | string/null | Full message text (no truncation)               |
| `has_media`       | bool        | Whether message contains media                  |
| `media_type`      | string/null | GramJS class name (MessageMediaPhoto, etc.)     |
| `media_file`      | string/null | Filename in media/ dir (e.g., "6.jpg")          |
| `views`           | int/null    | View count (channels only)                      |
| `forwards`        | int/null    | Forward count                                   |
| `reply_to_msg_id` | int/null    | Parent message ID if reply                      |
| `grouped_id`      | int/null    | Album group ID (shared across album messages)   |
| `edit_date`       | string/null | ISO 8601 timestamp of last edit                 |
| `sender.id`       | int         | Sender's Telegram user/channel ID               |
| `sender.name`     | string      | Display name (channel title or user first name) |
| `sender.username` | string/null | @username if set                                |

## Resume Support

Re-running the same command skips already-downloaded media files (checks `dest.exists()`). The NDJSON is fully rewritten each run. This makes it safe to resume interrupted downloads.

## Querying the Output

```bash
# jq: find all GOLD BUY signals with chart screenshots
jq 'select(.text != null and (.text | test("GOLD.*BUY")) and .media_file != null)' messages.ndjson

# DuckDB: aggregate by date
duckdb -c "SELECT date::DATE as day, count(*) FROM read_ndjson('messages.ndjson') GROUP BY day ORDER BY day"

# Python/Polars
import polars as pl
df = pl.read_ndjson("messages.ndjson")
```

## Performance Notes

- ~3000 messages + 1700 media files takes ~3-5 minutes
- Telegram may briefly disconnect mid-download (`Server closed the connection`) — GramJS auto-reconnects
- For very large channels (10k+ messages), expect 10-15 minutes with media

## Recommended Storage Pattern

For git-tracked projects, gitignore the media folder:

```gitignore
# data/telegram/.gitignore
*/media/
```

This keeps the NDJSON (metadata) in version control while keeping large media files local-only.

## Anti-Patterns

- **Don't dump channels you're not subscribed to** — GramJS needs access via your account
- **Don't run multiple dumps concurrently on the same profile** — session file contention

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
