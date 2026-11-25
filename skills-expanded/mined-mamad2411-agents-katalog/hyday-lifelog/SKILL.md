---
name: hyday-lifelog
description: Write, read, and summarize Hyday journal entries with Life Log marks for time-stamped events, thoughts, and highlights. Use whenever the user writes, reads, summarizes, lists, or extracts data from journal `.md` files (filename matches `YYYY-MM-DD.md` or `YYYY.MM.DD.md`) — e.g. "今天做了什麼", "幫我寫今天的日誌", "撈出這週的待辦/想法", "我這個月寫了什麼", "yesterday's journal", "summarize this week" — or mentions journal, daily entry, life log, task start/end, or the special marks `>()`, `<()`, `-()`, `%()`, `!()`.
---

# Hyday Life Log Skill

> **First time in this conversation? Run Step 0 from `hyday-vault-layout` to find the vault root.** This skill assumes you already know where the user's Hyday folder lives on disk. Resolve it from `~/Library/Application Support/Hyday/settings.json` (macOS) or `%APPDATA%\Hyday\settings.json` (Windows) — `journalPath` field. Don't guess, and don't ask the user unless the config lookup fails.

Hyday's journal is a per-day Markdown file decorated with five **Life Log marks** — short inline annotations that turn a free-form daily log into something Hyday can parse for task ranges, thoughts, and highlights.

## When this skill applies

A journal entry is a `.md` file whose filename is a date:

- `2026-05-17.md` ← preferred form
- `2026.05.17.md` ← also accepted (dot-separated)

Files matching this pattern are auto-typed as `journal`. Do **not** set `type: "journal"` in frontmatter — the filename does it.

Journal files normally live under `journal/<year>/<date>.md`. See `hyday-vault-layout` for placement details.

## Workflow: Writing a Journal Entry

1. **Use the correct filename** — `YYYY-MM-DD.md`, placed under `journal/<year>/`.
2. **Optional frontmatter** — usually omitted for journals. If used, `tags` is the most common field.
3. **Write the body** in plain Markdown.
4. **Sprinkle Life Log marks** where appropriate (see below). Use them inline within sentences, not as bullet prefixes.
5. **Save** — Hyday picks up the change. The marks render as styled chips and feed task tracking, lifelog insights, and tag exploration.

## The five Life Log marks

Marks split into two categories by what goes inside the parentheses.

### Time marks — content is `HH:mm`

The mark itself only carries the time. Write the event description as **plain text on the same line**, next to the mark.

| Mark | Type | Meaning |
|------|------|---------|
| `>(HH:mm)` | `taskStart` | Started a task / event |
| `<(HH:mm)` | `taskEnd` | Finished a task / event |
| `-(HH:mm)` | `current` | Snapshot of "what's happening right now" |

```markdown
>(09:00) Inbox triage and morning planning
<(09:45) Done with inbox — 12 emails left for tomorrow
-(10:30) Stuck on the migration script, taking a walk
```

### Content marks — content is free text

The text inside the parentheses **is** the content; nothing else needs to be written.

| Mark | Type | Meaning |
|------|------|---------|
| `%(text)` | `thought` | A passing thought, a hunch, a "note to self" |
| `!(text)` | `important` | Something to flag — decision, surprise, takeaway |

```markdown
%(maybe the bug is in the migration, not the API)
!(decided to ship v2 without the dashboard rewrite)
```

## Mark placement rules

- **Inline**, not as block prefixes. `>(09:00) Did X` ✓ —  `- >(09:00) Did X` puts the mark inside a list item, which still works but is less common.
- **One mark per occurrence**. `>(09:00) <(10:00) ...` (two marks on one line) is technically valid but harder to read; usually you write `<(10:00)` on its own line later.
- **No nesting**. Marks cannot contain other marks. `%(>(09:00) thought)` is treated as literal text.
- **Code-block safe**. Marks inside fenced code blocks (` ``` `) or inline code (`` ` ``) are not parsed — useful when documenting the syntax itself.
- **Time format is 24-hour `HH:mm`** for time marks. `>(9:00)` works (single-digit hour); seconds are not parsed.

## When to use which mark

| Situation | Mark |
|-----------|------|
| About to start something — meeting, deep-work block, errand | `>(HH:mm) <description>` |
| Just finished something | `<(HH:mm) <description>` |
| Pausing mid-task to capture state | `-(HH:mm) <description>` |
| Random idea you don't want to lose | `%(<idea>)` |
| Worth remembering — decision, insight, surprise | `!(<thing>)` |

A common pattern: `>(...)` and `<(...)` bracket a focused block of work, the body in between describes what happened, with `%(...)` and `!(...)` scattered throughout for thoughts and highlights.

## Hyday-specific inline content

Inside a journal body you can also use everything from `hyday-markdown`:

- `#tag` — inline tags
- `@(Label)` — entities (people, projects, places)
- `[[note-id]]` — links to other notes or other journal dates
- Standard Markdown — headings, lists, tables, code blocks, callouts, math

## Complete example

`journal/2026/2026-05-17.md`:

```markdown
---
tags:
  - "monday"
---

# 2026-05-17

>(08:30) Morning routine — coffee, glanced at #news
<(09:00) Done — feeling alert

>(09:00) Inbox triage and replies to @(Aaron) about the launch
%(Aaron's last reply suggests we should rethink the onboarding copy)
<(09:45) Done — 12 emails left for tomorrow

-(10:30) Working on the migration script for [[Project Alpha]]
!(Realized the old script assumes UTC; new one needs to honour user timezone)

>(11:00) Standup
<(11:15) Done — decided to defer the dashboard work to next sprint

## Afternoon

>(13:00) Deep work on [[Atomic Habits — Chapter 3 notes]] writeup
%(I should batch this kind of synthesis work into one slot, not three)
<(15:00) Wrapped — draft is ready for review

!(Big takeaway today: the migration timezone bug would have shipped if I hadn't run the seed script manually)
```

## Validation checklist

After writing a journal entry, verify:

1. Filename matches `YYYY-MM-DD.md` (or `YYYY.MM.DD.md`).
2. Frontmatter (if present) does **not** set `type: "journal"`.
3. Time marks use `HH:mm` inside parentheses, with description as plain text next to the mark — not inside the parens.
4. Content marks (`%()`, `!()`) have the meaningful text **inside** the parens.
5. No mark is nested inside another.
6. Marks you intend to be parsed are not inside fenced code blocks (unless that's intentional).

## References

- Hyday Markdown basics (frontmatter, tags, entities, backlinks): see `hyday-markdown` skill
- Where journal files live: see `hyday-vault-layout` skill
