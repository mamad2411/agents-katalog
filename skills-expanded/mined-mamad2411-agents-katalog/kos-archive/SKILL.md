---
name: kos-archive
description: Use this skill when the user wants to archive a completed Field Notes memo book — typically when the physical book is full and being placed in a Layer 3 archive envelope. Triggers include "archive FL-vol-001", "kos archive", "I'm done with this book", "put this book in envelope 7", or any explicit request to mark a book as archived. The skill validates the book's wiki representation is complete, updates the book page's frontmatter (status, archived-on, envelope-number), optionally moves the page to wiki/books/_archived/, updates wiki/index.md, and logs the operation. Never modifies raw/ — archived books retain their immutable raw transcriptions. Do not use this skill to ingest new sources (use kos-ingest), to query (use kos-query), or to validate the entire wiki (use kos-lint).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# KOS — Archive

Mark a completed memo book as archived, tying the digital wiki to the physical Layer 3 archive envelope.

## Before You Begin: Read the Contract

**Always read `<vault-root>/SCHEMA.md` first.** SCHEMA.md Section 3.3 defines the archiving workflow this skill implements. The user may have customized it. If anything in this skill conflicts with SCHEMA.md, **SCHEMA.md wins**.

If `SCHEMA.md` does not exist at the vault root, stop and tell the user the vault is not initialized. Suggest they run `/kos`.

---

## What This Skill Does (and Doesn't)

This skill makes one specific transition: a book moves from `status: active` to `status: archived`, with metadata recording when and where (which envelope) it was placed.

**MUST:**
- Validate the book is in a state where archiving makes sense
- Run lint scoped to the book before archiving
- Update the book page's frontmatter atomically — all fields together, or none
- Optionally move the book page into `wiki/books/_archived/`
- Update `wiki/index.md` to move the entry from `## Books` to `## Archived Books`
- Log the operation

**MUST NOT:**
- Touch `raw/` in any way — raw transcriptions remain immutable per SCHEMA.md Section 6.1 rule 1
- Modify `wiki/sources/` pages — their `raw-path:` pointers must remain valid
- Auto-fix lint findings — surface problems, let the user decide
- Unarchive a book — that's a deliberate separate action, not a flag on this skill

---

## Identify the Book

1. **If the user specifies a volume** ("archive FL-vol-001"), use it. Validate format matches `^F[LRS]-vol-\d{3}$`.

2. **If the user is ambiguous**, list active books from `wiki/books/` (top level only — `_archived/` books are not candidates):

```bash
find wiki/books -maxdepth 1 -type f -name 'F[LRS]-vol-*.md'
```

Read frontmatter for each: show `volume`, `book-type`, `date-start`, `date-end`. Ask the user which one.

3. **Validate the book exists at `wiki/books/<volume>.md`:**
- Exists at `wiki/books/_archived/<volume>.md` only → already archived. Show `archived-on` and `envelope-number` and stop.
- Doesn't exist anywhere → no wiki page yet. Suggest running `/kos-ingest` on a page from the book first.
- Exists in both locations → vault corruption (lint Check 2 should also flag this). Stop and tell the user; manual cleanup needed before archiving.

---

## Pre-Archive Validation

This is the most important part of the skill. Archiving signals "this book is done." An incomplete wiki representation is cheapest to fix right now.

### 1. Read the book page

Read `wiki/books/<volume>.md`. Confirm:
- `status:` is `active` — if not, stop and tell the user
- At least one source page in `wiki/sources/` is linked from it — if zero, archiving is almost certainly a mistake. Ask the user to confirm before proceeding.

### 2. Run lint scoped to this book

Check the following in order:

**Sources sync (Error if found):**
Every file in `raw/Field-Logs/<volume>/`, `raw/Field-Research/<volume>/`, or `raw/Field-Studies/<volume>/` must have a corresponding `wiki/sources/<volume>-<page>.md`.

**Broken wikilinks within this book's pages (Error if found):**
Read the book page and every source page from this volume. Extract all `[[wikilink]]` references. Verify each target exists.

**Unresolved bit.ly slugs in this book's source pages (Warning if found):**
```bash
grep 'unresolved-slug:' wiki/log.md | grep '<volume>'
```

**Frontmatter validity on the book page (Error if found):**
Verify `type: book`, `volume`, `book-type`, `date-start`, `date-end`, `status: active`. Plus `subject` if `book-type: field-study`.

### 3. Report findings before proceeding

**Clean (no findings):** proceed to "Collect Archive Metadata."

**Warnings only:** ask the user:
> "Found N warnings. None block archiving — these slugs may be permanently unresolved. Archive anyway, or fix first?"

If "fix first" → stop. Tell the user to address the slugs then re-run `/kos-archive`.

**Errors found:** stop. Do NOT proceed. Tell the user:
> "Found N errors that should be resolved before archiving: [list]. Run `/kos-ingest` for unprocessed sources, or fix the wiki manually. Then re-run `/kos-archive <volume>`."

The user CAN override errors with an explicit instruction ("archive anyway"), but require an explicit override — don't make it accidental.

---

## Collect Archive Metadata

### 1. Envelope number

Ask:
> "Which Layer 3 archive envelope is this book going into?"

Default: read the highest existing `envelope-number:` from archived book pages and add 1. Suggest 1 if none exist.

```bash
grep -rh '^envelope-number:' wiki/books/_archived/ 2>/dev/null \
  | awk '{print $2}' | sort -n | tail -1
```

Accept any number the user provides — envelope numbering is the user's prerogative.

### 2. Archive date

Ask:
> "When was the book physically archived? (default: today)"

Default: today in `YYYY-MM-DD` format. Validate: not in the future. If more than 30 days in the past, confirm: "That's [N] days ago — is that right?"

---

## Apply the Archive

**Do all steps in this order. If any step fails, stop immediately — do NOT continue with a partially-archived book.**

### 1. Update the book page's frontmatter

In `wiki/books/<volume>.md`, set:
- `status: archived`
- `archived-on: <date>`
- `envelope-number: <N>`
- `updated: <current ISO 8601 timestamp>`

Preserve all other fields exactly: `created`, `volume`, `book-type`, `subject`, `date-start`, `date-end`, `tags`. Do not modify them.

### 2. Move the book page (default: yes)

Ask the user (unless already specified):
> "Move the book page to `wiki/books/_archived/`? (recommended for visual organization; wikilinks resolve either way)"

If yes:
```bash
mkdir -p wiki/books/_archived
mv wiki/books/<volume>.md wiki/books/_archived/<volume>.md
```

If no: leave at `wiki/books/<volume>.md`. The `status` field still drives behavior — location is cosmetic.

Note: `[[<volume>]]` wikilinks resolve either way because Obsidian matches by filename, not path.

### 3. Update `wiki/index.md`

- **Remove** the `[[<volume>]]` entry from `## Books`
- **Add** under `## Archived Books`: `- [[<volume>]] — <description> (envelope <N>)`
- Create `## Archived Books` section after `## Books` if it doesn't exist
- Update the `_Last updated:_` timestamp

### 4. Append to `wiki/log.md`

Append only — never rewrite.

> Read `./references/ingest-log-examples.md` for the archive log entry format.

---

## Report Results

Tell the user:

1. **What was done:** volume, envelope number, archive date, page location, index and log updated
2. **Physical reminder:**
   > "Don't forget: write '<N>' on the envelope, place <volume> inside, and store in your archive box."
3. **What changed:** book hidden from `## Books`; still searchable via `## Archived Books` and `wiki/books/_archived/`; all `wiki/sources/` pages and `raw-path:` pointers unchanged
4. **What's next:** typically nothing — go back to capturing in the next active book

---

## Edge Cases

**User wants to extend an archived book:**
If `/kos-ingest` adds pages to an archived volume, it will warn the user. If they confirm and extend the book, they should re-run `/kos-archive` on completion — the existing envelope number stays, only `date-end` and `archived-on` update.

**Correcting archive metadata after the fact:**
Manual edit to the book page's frontmatter. This skill handles the initial archive transition only.

**Multiple books in one session:**
One book per invocation — archiving is deliberate, not a batch operation.

---

## Conventions

- **Read SCHEMA.md first.**
- **Pre-archive lint is mandatory.** Don't seal away a book with broken wiki representation.
- **`raw/` is never touched.** Archive operations are wiki-only.
- **Frontmatter updates are atomic.** All four fields change together, or none change.
- **Move is optional, status is mandatory.** `_archived/` is visual organization. `status: archived` is what matters operationally.
- **One book per invocation.**
- **Errors block archiving by default.** Warnings prompt for confirmation. Override requires explicit user instruction.

---

## When to Archive

- Physical book is full (most common)
- Switching purposes mid-book
- End of year / calendar boundary
- Bulk-archiving an existing physical collection when first setting up KOS

---

## Related Skills

- `/kos-ingest` — run before archiving to ensure raw/wiki sync
- `/kos-query` — archived books are still fully searchable
- `/kos-lint` — full vault health check (this skill runs lint scoped to one book only)
