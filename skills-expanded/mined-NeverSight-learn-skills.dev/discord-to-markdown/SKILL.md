---
name: discord-to-markdown
description: >
  Convert a Discord message copy (from the clipboard) into clean Markdown, deterministically
  and without an LLM. Discord puts a rich HTML flavor on the clipboard that preserves author
  groups, the poster's own bullet/number lists, links, code, emoji, and image attachments; a
  naive HTML-to-Markdown converter turns Discord's message list (an <ol>) into a numbered list
  and clobbers the real lists. This skill parses that HTML correctly. Use when the user says
  "convert this Discord copy to markdown", "discord to markdown", "/discord-md", "paste this
  Discord thread into Obsidian", "clean up this Discord paste for an LLM", or copies messages
  from Discord and wants readable Markdown. macOS only (reads the clipboard via osascript/pbpaste).
---

# Discord → Markdown

A deterministic clipboard→Markdown converter for Discord. The engine is a zero-dependency
Python script (`discord2md.py`) that lives next to this file. **Prefer the script over doing
the conversion yourself** — it is faster, exact, and free of LLM drift.

## Why it exists

When you copy messages in Discord, the clipboard carries two flavors:

- **plain text** — loses list markers (typed bullets come through as bare lines) and links.
- **HTML** — preserves everything, but wraps the whole thread in `<ol data-list-id="chat-messages">`
  with each message as an `<li>`. A generic html→md converter renders that as a numbered list,
  destroying the genuine lists the poster typed.

`discord2md.py` treats the message list specially (author headers, not list items) and only
renders the *inner* content lists, so the output reads like what the poster actually typed.

## How to run it

The script is bundled in this skill's directory. Invoke it with the system `python3`
(needs 3.9+ for `zoneinfo`):

```bash
python3 "<this-skill-dir>/discord2md.py" [options]
# installed globally this is usually:
python3 ~/.claude/skills/discord-to-markdown/discord2md.py
```

**Default** (no args): reads the clipboard's HTML flavor, writes Markdown back to the
clipboard **and** prints it to stdout. That's the common case — run it, then paste.

Useful options:

| Goal | Command |
| --- | --- |
| Default (clipboard → clipboard + stdout) | `discord2md.py` |
| Just print (for piping) | `discord2md.py --to stdout` |
| Write a file | `discord2md.py --out thread.md` |
| Write an Obsidian note (images → webp in Attachments, `![[…]]`) | `discord2md.py --obsidian` |
| Include images as downloaded webp | `discord2md.py --images webp` |
| Keep system messages (title changes) | `discord2md.py --system` |
| Keep link-preview embeds | `discord2md.py --embeds` |
| Teach it a server (see below) | `discord2md.py --learn "<message-link>"` |

Image modes (`--images`): `remove` (default — leaves `[image: filename]`), `sidecar`
(download originals), `webp` (download + convert via `cwebp`/`sips`), `inline`
(remote URL — **expires in ~24h**, avoid for anything durable).

## Message links need the server (guild) id — first-time setup per channel

Discord links are `https://discord.com/channels/<guild>/<channel>/<message>`, but a copy only
contains the channel and message ids, **not the guild**. So:

- If the guild for a channel is **known**, each group's timestamp becomes a clickable link.
- If **unknown**, timestamps render as plain text and the script prints a one-line note to stderr.

To enable links for a channel the first time, ask the user to **right-click any message in that
Discord channel → Copy Message Link**, then run:

```bash
python3 discord2md.py --learn "https://discord.com/channels/123.../456.../789..."
```

This records `channel → guild` in the config and links work for every future paste from that
channel. The script also auto-harvests guild ids from any real `discord.com/channels/` URLs that
appear inside the copied content (rendered `@user`/`#channel` mentions have no URL, so those don't
help).

## Config (the personal layer)

Defaults live in `~/.config/discord2md/config.json` (override with `--config`). The script is
generic and shareable; this file is where personal settings go, so nothing personal is baked into
the code:

```json
{
  "timezone": "America/Chicago",
  "link_base": "discord.com",
  "default_image_mode": "remove",
  "default_link_style": "md",
  "obsidian_image_mode": "webp",
  "attachments_dir": "/path/to/Vault/Attachments",
  "output_note_dir": "/path/to/Vault/Outputs",
  "channel_guild_map": { "<channel_id>": "<guild_id>" }
}
```

The `channel_guild_map` is maintained automatically by `--learn` and by harvesting; you can also
edit it by hand.

## Caveats to relay to the user

- **Images into Claude**: a Markdown image *reference* does not feed Claude's vision — only
  *attached files* do. The `webp`/`sidecar` modes download the bytes so Obsidian renders them and
  you can attach the files to a Claude chat. There is no Markdown-only trick to get images into Claude.
- **Inline image URLs expire** (~24h). Use `webp`/`sidecar` for anything you keep.
- **Plain-text fallback**: if the clipboard has no HTML flavor (e.g. pasted from clipboard
  history), the script degrades to a best-effort text parse and warns — lists and links can't be
  recovered. Re-copy from Discord live to get full structure.
- **Replies are unrecoverable**: when you copy a message that is a Discord *reply*, Discord does
  **not** include the replied-to preview in the clipboard (verified: nothing sits between the
  message container and its header). Only the reply's own text is copied, so the "replying to X: …"
  context is lost. If it matters, copy the referenced message too.
- **`---` collision**: author-groups are separated by a `---` rule; if someone *typed* `---` in a
  message it renders as a rule too. Both are horizontal dividers, so it reads fine, but they are
  not distinguishable in the output.

## Raycast

The script is headless and clipboard-driven, so a Raycast Script Command is a 3-liner — see
`raycast-discord-to-md.sh` in this directory.
