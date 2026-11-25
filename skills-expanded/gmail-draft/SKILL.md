---
name: gmail-draft
description: Use when creating or updating a Gmail draft from the terminal - builds the draft with the gws CLI so paragraphs never hard-wrap (text and HTML parts), threads replies, updates a draft in place, and turns "- " lines into bullets and **text** into bold. Triggers on "draft an email", "gmail draft", "reply to this thread by email", "update that draft", or /gmail-draft.
---

# gmail-draft

Create Gmail drafts that read like ones typed in Gmail's own compose window. The script `gmail-draft` lives next to this file; `install.sh` links it onto PATH, or link it by hand into `~/.local/bin`.

## Usage

```sh
gmail-draft --body FILE --to ADDR [--cc ADDR] [--subject S] [--reply-to MESSAGE_ID] [--update DRAFT_ID] [--force]
```

- `--body FILE`: one paragraph per line, a blank line between paragraphs. Runs of `- ` or `1. ` lines become real Gmail lists; `**text**` becomes bold.
- `--reply-to MESSAGE_ID`: threads the draft under that message (In-Reply-To, References, threadId, "Re:" subject).
- `--update DRAFT_ID`: replaces that draft in place so its id and an open Gmail window stay valid. It refuses to run if the draft was edited in Gmail since this tool last wrote it; merge the hand edits into the body, or pass `--force`.
- Another Google account: set `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` to that account's gws config directory before calling.

## Rules

- Never hard-wrap prose. The tool unwraps lines inside a paragraph, adds the HTML part, and keeps the plain-text part on long lines, so the recipient never sees ragged breaks.
- Drafts only. Sending stays with the user; report the draft id and stop.
- When a draft is superseded, update it in place or delete the old one before creating a replacement; never leave two drafts in one thread.
