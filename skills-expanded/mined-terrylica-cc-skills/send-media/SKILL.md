---
name: send-media
description: "Use when user wants to send or upload a file, photo, video, voice note, or document on Telegram via their personal account."
allowed-tools: Bash, Read, Grep, Glob
---

# Send Media on Telegram

Send files, photos, videos, voice notes, and documents from your personal Telegram account.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

Check session is **authorized** (not just that the file exists):

```bash
bun "$SCRIPT" check-auth
```

If `EXPIRED`, run `/tlg:setup` first (uses 3-step non-interactive auth pattern).

## Usage: tg-cli.ts (simple cases)

```bash
/usr/bin/env bash << 'EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Send a photo/image (auto-detected)
bun "$SCRIPT" send-file @username /path/to/photo.jpg

# Send with caption (plain text only)
bun "$SCRIPT" send-file -1003958083153 /path/to/image.png -c "Check this out"

# Force send as document (no preview)
bun "$SCRIPT" send-file @username /path/to/image.png --document

# Send voice note
bun "$SCRIPT" send-file -1003958083153 /path/to/audio.ogg --voice

# Send round video
bun "$SCRIPT" send-file @username /path/to/video.mp4 --video-note
EOF
```

**Known limitation**: captions via CLI are plain text only (no HTML). For formatted captions, use the `draft` skill to compose a message in Saved Messages, copy it into the target chat, and manually attach the file there.

## Parameters (tg-cli.ts)

| Parameter      | Type       | Description                            |
| -------------- | ---------- | -------------------------------------- |
| recipient      | string/int | Username, phone, or chat ID            |
| file           | path       | Local file path                        |
| `-c/--caption` | string     | Caption text (plain text only via CLI) |
| `--voice`      | flag       | Send as voice note                     |
| `--video-note` | flag       | Send as round video                    |
| `--document`   | flag       | Force document (no media preview)      |

## Supported Formats

GramJS auto-detects media type by extension. Override with flags.

| Type     | Extensions        | Notes                                |
| -------- | ----------------- | ------------------------------------ |
| Photo    | jpg, png, webp    | Compressed by Telegram               |
| Video    | mp4, mov, avi     | Use `--document` to skip compression |
| Audio    | mp3, m4a, flac    | Sent as audio player                 |
| Voice    | ogg (opus)        | Requires `--voice` flag              |
| Document | pdf, zip, md, any | Sent as file attachment              |

## Anti-Patterns (NEVER DO)

| Anti-Pattern                                        | Why It Fails                                                              |
| --------------------------------------------------- | ------------------------------------------------------------------------- |
| Running `bun "$SCRIPT"` without checking auth first | If session expired, auth will fail                                        |
| Using formatted text in `-c` caption                | CLI caption is plain text only — use `draft` skill for formatted captions |
| Checking only session file existence in preflight   | Session file can exist but be expired — must check with `check-auth`      |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
