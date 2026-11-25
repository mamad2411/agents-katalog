---
name: clipboard-grab
description: "Copies the latest shell command Claude ran, the latest URL it printed, or the full text of its latest reply (a draft, an email, a snippet) from the current session straight to the system clipboard, with options for several items, older items, and stripping prose around a drafted block. Use when the user wants to copy, grab, or paste something from this session elsewhere without selecting it in the terminal."
user-invocable: false
---

# Grab: this session's output to the clipboard

Bare `/grab` is the common case: the command Claude just ran, ready to paste into another shell, a doc, or a message. A source argument grabs a URL or a whole reply instead.

## How to run it

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/bin/grab.py <args> --session-id "${CLAUDE_SESSION_ID}"
```

Pass the user's arguments through verbatim. The script finds this session's transcript, extracts the items, copies them, and prints a one-line confirmation with a short preview. Report that line; do not repeat the whole payload unless it is short.

## Arguments

```
/grab [session | link | message] [--count N | --all] [--scan N] [--skip N] [--hr] [--dry-run]
```

| Source | What it grabs |
|---|---|
| `session` (default) | The latest Bash command Claude ran in this session. `/grab` calls themselves are filtered out, so `/grab` twice in a row still returns the previous real command. |
| `link` (or `url`) | The latest URL from Claude's replies: the text you saw, not URLs inside tool inputs or fetched pages. Placeholder URLs with `...`, `{`, `}`, `<`, or `>` are skipped; trailing punctuation is trimmed. |
| `message` (or `msg`) | The full text of Claude's latest reply turn, with markdown kept verbatim. One turn is every text block between two of your messages. |

| Flag | Meaning |
|---|---|
| `--count N` | The newest N items, joined by blank lines (default 1) |
| `--all` | Every item in the scan window |
| `--scan N` | How far back to look (default 20 items) |
| `--skip N` | Skip the newest N items first: `--skip 2 --count 1` is the third-newest |
| `--hr` | Keep only the text between the first and last `---` line of each item, to strip the framing around a drafted email or brief |
| `--dry-run` | Print instead of touching the clipboard |

## Examples

```
/grab                         latest command
/grab --count 3               last three commands
/grab link                    latest URL Claude printed
/grab link --all --scan 50    every URL in the last 50 found
/grab message                 the latest reply, whole
/grab message --skip 2 --hr   a draft from three replies back, without the framing
/grab --dry-run               show what would be copied
```

## Clipboard

The script uses `GRAB_CLIPBOARD_CMD` when set (for example `GRAB_CLIPBOARD_CMD="xclip -selection primary"`), otherwise the first of `wl-copy` (Wayland), `xclip` or `xsel` (X11), `pbcopy` (macOS), `clip.exe` (WSL) found on PATH. With no clipboard tool, for example over ssh without a display, it prints the payload and exits non-zero; say that the copy did not happen.

## Chat sources

Grabbing a command someone sent in a WhatsApp chat is the LibreWhatsApp pack's `grab` plugin. This one reads only the current Claude Code session.

## Anti-patterns

- Do not run or paste what was grabbed. Grab only fills the clipboard; the user decides what happens next.
- Do not claim a copy that failed. The script's exit status is the truth.
