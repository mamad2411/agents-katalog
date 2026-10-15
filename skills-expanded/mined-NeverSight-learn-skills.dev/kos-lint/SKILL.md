---
name: kos-lint
description: Use this skill when the user wants to health-check their Kodex OS Layer 1 LLM Wiki for structural issues. Triggers include "lint kos", "check my wiki", "audit the wiki", "find broken links", or any explicit request for a wiki integrity report. The skill verifies that the vault conforms to its SCHEMA.md, that every raw/ source has a corresponding wiki/sources/ entry, that every memo book folder has a wiki/books/ entry, that wikilinks resolve, that frontmatter is valid, and that bit.ly slugs are resolved. Reports findings grouped by severity. Does not make changes unless the user explicitly approves each fix. Do not use this skill for routine ingest (use kos-ingest) or content questions (use kos-query).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# KOS — Lint

Health-check the wiki against SCHEMA.md and report issues with actionable fixes.

## Before You Begin: Read the Contract

**Always read `<vault-root>/SCHEMA.md` first.** It defines what valid structure looks like for this vault. The user may have customized it. SCHEMA.md Section 6.4 lists the checks lint MUST perform. If anything in this skill conflicts with SCHEMA.md, **SCHEMA.md wins**.

If `SCHEMA.md` does not exist at the vault root, stop and tell the user the vault is not initialized. Suggest they run `/kos`.

Note the `schema-version` from SCHEMA.md's YAML header — you'll use it in Check 7.

---

## Determine Scope

Ask the user, unless already specified:

- **Full audit** — all checks against the entire vault
- **Quick audit** (default) — Checks 1, 2, 3, 7 only (structural integrity; skips slow checks - excludes check 2b and check 8)
- **Scoped audit** — limited to a directory, time window, or specific book
- **Deep audit** — full audit plus Checks 9 and 10 (contradiction and stale-claim checks — slow, produces false positives; only run on explicit request)

Default to **quick audit** if the user just says "lint." Reserve full audit for explicit requests ("full lint", "audit everything").

---

## Audit Checks

Run checks in this order. Every finding gets a severity:

- **Error** — violates a SCHEMA.md MUST rule. Must be fixed.
- **Warning** — likely a problem but may be intentional.
- **Info** — suggestion, not a defect.

For every finding, capture: `severity`, `check`, `path`, `line` (if applicable), `message`, `suggested-fix`.

### Check 1: Raw → wiki/sources/ sync (Error)

Every file under `raw/` (excluding `raw/assets/` and binary files) must have a corresponding `wiki/sources/` page per SCHEMA.md Section 3.2's filename derivation rule.

```bash
find raw -type f -name '*.md' ! -path 'raw/assets/*'
find raw/Field-Logs raw/Field-Research raw/Field-Studies -type f -name '*.pdf'
```

**Derivation rules:**
- `.md`: `raw/<path>/<file>.md` → `wiki/sources/<path>-<file>.md`
- `.pdf`: strip capture suffix (`-sticky`, `-under`, `-flip`) to get base name → `wiki/sources/<path>-<base>.md`
- Companion scans (`-under`, `-flip`) share a derived path with their `-sticky` — they are NOT evaluated individually
- **Field Study exception:** all pages from one `FS-vol-XXX` accumulate into one source page. Only flag if no source page exists at all for that volume.

Finding: **Error** — `Unprocessed source: <raw-path> has no wiki/sources/ page` — Fix: run `/kos-ingest`

### Check 2: Memo book → wiki/books/ sync (Error)

Every folder matching `^F[LRS]-vol-\d{3}$` under `raw/Field-Logs/`, `raw/Field-Research/`, or `raw/Field-Studies/` must have a book page at EITHER `wiki/books/<volume>.md` OR `wiki/books/_archived/<volume>.md`. The `book-type` in frontmatter MUST match the volume prefix.

```bash
find raw/Field-Logs raw/Field-Research raw/Field-Studies -maxdepth 1 -type d -regex '.*F[LRS]-vol-[0-9][0-9][0-9]'
find wiki/books -type f -name '<volume>.md'
```

For each memo book folder:
- Neither location has a book page → **Error**, fix: run `/kos-ingest` on a page from this book
- Book page exists but `book-type` doesn't match prefix → **Error**, fix: correct the frontmatter
- Book page exists in BOTH locations → **Error**, fix: delete the duplicate

> Read `./templates/frontmatter-templates.md` for the prefix → `book-type` mapping.

**Cross-check archived book metadata.** For pages under `wiki/books/_archived/`:
- `status: archived` missing → **Error**
- `archived-on:` missing or malformed → **Error**
- `envelope-number:` missing → **Warning**

For pages under `wiki/books/` (top level):
- `status: archived` is set → **Error**: archived books belong in `_archived/`. Fix: move the file OR revert `status:` to `active`.

### Check 2b (full and deep audit only): Orphaned companion scans (Warning)

```bash
find raw/Field-Logs raw/Field-Research raw/Field-Studies \
  -type f \( -name '*-under.pdf' -o -name '*-flip.pdf' \)
```

For each `-under` or `-flip` found, check for a corresponding `-sticky` in the same folder:
- No `-sticky` → **Warning**: `Orphaned companion scan: <path> has no corresponding -sticky scan` — Fix: upload missing `-sticky`, or rename if misnamed

Also check: a `-sticky` with no `-under` companion where the vault's last-modified timestamp is more than 24 hours old:
- **Warning**: `Incomplete capture: <path>-sticky.pdf has no -under companion` — Fix: scan the page without the sticky and upload as `<path>-under.pdf`, or ingest now if sticky content is sufficient

### Check 3: Broken wikilinks (Error)

```bash
grep -rn '\[\[[^]]*\]\]' wiki/
```

For each match:
- Extract the page name (in `[[page-name|display text]]`, take the part before `|`)
- Search `wiki/**/*.md` for `<page-name>.md`
- No match → **Error**: `Broken wikilink: [[<page-name>]] in <file>:<line>` — Fix: create the target page or correct the link

### Check 4: Index consistency (Error / Warning)

Verify `wiki/index.md` reflects reality:
- Every page in `wiki/{sources,entities,concepts,synthesis,questions}/` must have an entry under the matching section header → **Error** if missing
- Every active book (`wiki/books/<volume>.md`) must appear under `## Books` → **Error** if missing
- Every archived book (`wiki/books/_archived/<volume>.md`) must appear under `## Archived Books` → **Error** if missing
- Any index entry pointing to a non-existent page → **Error**
- A book listed under the wrong section (`## Books` vs `## Archived Books`) → **Error**, fix: move the entry
- Entries not alphabetized within a section → **Warning** (cosmetic)

```bash
find wiki/books -type f -name '*.md'
```

### Check 5: Frontmatter validation (Error)

For each wiki page, verify frontmatter against SCHEMA.md Section 4 and type-specific fields.

> Read `./templates/frontmatter-templates.md` for the complete required field list per page type before running this check.

**Key validation rules (apply without re-reading the template):**
- `created` and `updated` must be valid ISO 8601 timestamps (`YYYY-MM-DDTHH:MM:SSZ`)
- `type:` must match the directory the page lives in (pages in `_archived/` still use `type: book`)
- `book-type:` must match the volume prefix per the prefix mapping
- `status:` for book pages must be `active` or `archived` — anything else is an **Error**
- For archived book pages, `archived-on:` must be a valid `YYYY-MM-DD` date
- For `field-study-page` sources, `created` must not be newer than `updated` — `created` is set once on first ingest and never changes
- For `field-log-page` sources, `entries:` must be present with at least one item
- For `field-study-page` sources, `subject:` must be present

Each violation: **Error**, naming the specific missing or malformed field.

### Check 6: Unresolved bit.ly slugs (Warning)

Grep `wiki/log.md` for `unresolved-slug:` entries — never read the full file:

```bash
grep 'unresolved-slug:' wiki/log.md
```

- **Warning**: `Unresolved bit.ly slug: <slug> in <source-page>` — Fix: visit `https://bit.ly/<slug>` to determine target, add description in source page, then re-ingest

Cross-vault consistency per SCHEMA.md Section 5.4: if the same slug appears across multiple `wiki/sources/` pages with different descriptions or URLs:
- **Warning**: `Inconsistent slug usage: <slug> linked differently across <pages>`

### Check 7: Schema version (Error / Info)

Compare `schema-version` in the vault's SCHEMA.md against the canonical version in `./references/schema-changelog.md`:

- Vault version < canonical → **Error**: `Schema out of date: vault is on v<X>, KOS ships v<Y>` — Fix: review the diff in `templates/SCHEMA.md` upstream and update the vault manually. Do NOT auto-migrate.
- Vault version > canonical → **Info**: vault is ahead of the install (user may have edited locally)
- Versions match → no finding

### Check 8 (full and deep audit only): Orphan pages (Warning)

A page is an orphan if no other page links to it via `[[wikilink]]`.

**Exclude from orphan checks:**
- `wiki/sources/` (leaf nodes; many have no inbound links)
- `wiki/books/` and `wiki/books/_archived/` recursively
- `wiki/index.md` and `wiki/log.md`

For each remaining page (entities, concepts, synthesis, questions):
- Search all wiki pages for `[[<page-name>]]`
- No match → **Warning**: `Orphan page: <path> has no incoming wikilinks` — Fix: link from a relevant page, or delete if no longer relevant

### Check 9 (deep audit only): Duplicate entities (Warning)

Scan `wiki/entities/` for pages referring to the same thing:
- Compare `aliases:` lists across entity pages
- Compare titles for case-insensitive or whitespace-only differences
- Use LLM judgment to identify obvious duplicates (e.g., `anthropic.md` and `anthropic-pbc.md`)

Finding: **Warning** — Fix: merge pages, consolidate aliases, redirect wikilinks.

### Check 10 (deep audit only): Stale claims & contradictions (Info)

These checks are slow and produce false positives — only run during deep audit.

- **Stale claims:** entity or concept page cites only sources older than N days when newer sources mention the same entity/concept
- **Contradictions:** two source summaries make opposing claims about the same entity or concept

Finding: **Info** — Fix: review and update the wiki page.

If the wiki has more than 100 pages, ask the user to scope this check (e.g., "check entities mentioned in sources from the last 30 days") rather than scanning everything.

---

## Report

> Read `./references/lint-report-example.md` for the exact report format before writing the findings.

Present findings grouped by severity, then by check. Include pages scanned counts, schema version status, and a summary line at the end.

---

## After the Report

Ask the user per finding — **NOT in batch**:

> "Want to fix [Check 1: 2 unprocessed sources]? I'll run /kos-ingest on each. (yes / no / skip all errors)"

The user may respond:
- **yes** — apply this specific fix
- **no** — skip this finding, move to the next
- **skip all errors** — stop offering fixes; finish the report

For findings with ambiguous fixes (orphan pages: link or delete? duplicate entities: which page survives?), present the options and let the user choose. **Never auto-fix ambiguous findings.**

---

## Log the Lint Pass

Append to `wiki/log.md` — append-only, never rewrite.

> Read `./references/ingest-log-examples.md` for the lint log entry format.

---

## Conventions

- **Read SCHEMA.md first.** It is the source of truth.
- **Report by severity, fix per finding.** Never batch-apply fixes without per-item confirmation.
- **Errors map to SCHEMA.md MUST violations.** Warnings are likely problems. Info is advisory.
- **Don't auto-migrate schemas.** Report out-of-date schemas; let the user review the diff manually.
- **Bash paths are relative to vault root.** `cd` there before running grep/find commands.
- **Grep before read.** Never read a file to check if it's relevant. Use grep/find to identify candidates first, then read only confirmed matches. Never load `wiki/log.md` in full — always grep it.
- **Start a fresh session for each operation.** Resumed sessions carry prior context that bloats the window before the operation begins.

---

## When to Lint

- After every ~10 ingests
- Monthly minimum
- Before major queries
- Before archiving to Layer 3

---

## Related Skills

- `/kos-ingest` — process new sources into wiki pages
- `/kos-query` — ask questions against the wiki
