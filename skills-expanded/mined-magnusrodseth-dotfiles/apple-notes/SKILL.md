---
name: apple-notes
description: Create, read, search and update notes in the macOS Apple Notes app from the command line, including notes that sync to iPhone and iPad via iCloud. Use when the user wants something in Apple Notes, a note on their phone, an agenda or checklist to carry into a meeting, or mentions Notes.app, iCloud notes, or "on my phone". Not for the Obsidian vault.
---

# Apple Notes

Drive Notes.app from the shell via `osascript`. A note written to the iCloud account is on the user's phone within seconds, which is the usual reason to reach for this: something they need to carry off the Mac.

**This is not the Obsidian vault.** The vault is the durable second brain and has its own skills (`vault`, `note`, `inbox`). Apple Notes is the portable, disposable surface. When a topic deserves both, write the lasting version to the vault and a stripped, phone-readable version here, and do not treat the Apple Note as the source of truth.

## The CLI

`scripts/notes.sh` wraps every operation. Content goes in on **stdin as HTML**; the script routes all strings through temp files read as `«class utf8»`, so quotes, backslashes, newlines and æøå survive untouched. Never hand-build an `osascript -e` string with user text in it.

```
notes.sh accounts                    name <TAB> note count
notes.sh folders                     name <TAB> note count
notes.sh list                        id <TAB> ISO-modified <TAB> name, newest first
notes.sh search <query>              body substring, case-insensitive, all accounts
notes.sh get <id|title>              plaintext
notes.sh html <id|title>             raw HTML body
notes.sh create < body.html          prints the new note id
notes.sh append <id|title> < f.html
notes.sh replace <id|title> < f.html
notes.sh delete <id|title>           moves to Recently Deleted
notes.sh show <id|title>             opens in the Notes UI, steals focus
notes.sh attach <id|title> <file>
```

Flags: `--account NAME`, `--folder NAME`, `--limit N`. Default account and folder come from Notes itself (`default account` / `default folder`), which is normally iCloud → "Notes".

**Write the HTML to a file first, then pipe it.** Composing a long note inline in a heredoc invites shell-escaping bugs that the script otherwise prevents:

```bash
# build with the Write tool, then:
notes.sh create < /tmp/agenda.html
```

## The title is the first line

Notes derives a note's title from the first line of its body. Passing a `name` property *and* a leading `<h1>` renders the title twice. Let the first line be the title and never set `name` on create.

## HTML that actually survives

Notes rewrites the body on save. Verified behavior:

| Written | Stored as | Verdict |
|---|---|---|
| `<h1>` / `<h2>` | bold span, 24px / 18px | works as headings |
| `<b>` `<i>` `<u>` | unchanged | works |
| `<s>` | `<strike>` | works |
| `<code>` | Courier span | works |
| `<ul>` `<ol>` `<li>` | unchanged | works |
| `<div>` `<br>` | unchanged | works |
| `<table>` | Notes table object | works |
| `<a href="...">` | `<u>text</u>`, **URL destroyed** | write the bare URL as text instead, Notes auto-links it |
| `<blockquote>` | plain `<div>` | styling lost, text kept |
| `<ul class="Checklist">` | ordinary list | checklists cannot be created this way |

**Adjacent lists merge.** Two `<ul>`/`<ol>` blocks with nothing between them collapse into one list, silently reassigning items to the wrong section. Separate every list with a heading or a `<div>`.

## Rules that bite

- **Titles are not unique.** Notes happily holds three notes with the same name. `get`/`delete` by title resolve to an arbitrary first match, so use the id (`x-coredata://...`) for anything destructive or when a name looks generic.
- **`plaintext` is read-only.** `body` is the writable HTML property. There is no append command in the dictionary; the script does read-modify-write for you.
- **Delete is recoverable.** It moves the note to Recently Deleted, where it sits for about 30 days. Purging for real means deleting it again from that folder.
- **First run prompts for automation permission.** macOS shows a TCC dialog the first time a given terminal drives Notes. It cannot be granted from the shell; the user has to click it.

Bulk operations, folder manipulation and anything the CLI does not cover: read `REFERENCE.md` before hand-rolling AppleScript, because iterating and mutating a note collection has a trap that costs a debugging cycle every time.
