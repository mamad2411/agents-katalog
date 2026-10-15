---
name: hyday-vault-layout
description: Locate, browse, and navigate a Hyday vault — resolve the vault root from the user's `settings.json` (Step 0), list or inventory notes, find where Hyday stores something, decide where to put new files. Use whenever an agent first needs to know where the user's Hyday folder is on disk, or whenever the user asks "where are my notes stored", "list my hyday folders", "整理我的 hyday", "我的 hyday 在哪", or mentions Hyday folder, data path, vault, journal directory, templates, assets, or vault structure. Every other Hyday skill builds on this one's Step 0.
---

# Hyday Vault Layout Skill

A **Hyday vault** is just a folder on your computer. Hyday reads and writes plain `.md` files there — nothing is locked away in a database. This skill describes the folder convention so an agent can place, find, and rename files correctly.

## Step 0 — Locate the vault root (do this FIRST, every time)

Before reading or writing anything, you must know which folder on disk is the user's Hyday vault. **Read it from Hyday's config file** — don't guess and don't ask the user unless steps 1-3 below fail.

### Config file location

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Hyday/settings.json` |
| Windows | `%APPDATA%\Hyday\settings.json` |

The file is JSON. The vault root lives in the `journalPath` field:

```json
{
  "journalPath": "/Users/muki/Documents/MyNotes",
  "...": "other fields"
}
```

### Resolution order (try in sequence)

1. **Explicit override**: if the user typed a path in this conversation, or the env var `HYDAY_DATA_ROOT` is set, use that. Don't override.
2. **Read `settings.json`**: parse the JSON at the path above and read `journalPath`.
3. **Fallback to `~/.hyday-recovery`**: same JSON shape (`{ "journalPath": "..." }`). Hyday writes this as a backup when the user changes the path.
4. **Last resort: ask the user.** Do NOT assume `~/Documents/Hyday` or any default — Hyday has no default location.

### Sanity check after resolving

Verify the resolved path is actually a Hyday vault before any read/write:

- The directory exists.
- At least one of these is true:
  - A `journal/<year>/` subfolder exists (e.g. `journal/2026/`)
  - The root has loose `.md` files with YAML frontmatter (`title:`, `type:`, etc.)
  - A `templates/` or `.hyday/` subfolder exists at the root
- If none match, the resolved path is wrong (or Hyday has never been opened with this path) — bail and ask the user.

### Why this matters

Every other Hyday skill (`hyday-markdown`, `hyday-lifelog`, `hyday-whiteboard`) assumes you already know the vault root. If you skip Step 0 you'll either write files to the wrong directory or fail silently. The whiteboard MCP server uses the exact same resolution chain — keep your behavior consistent with it.

## Folder convention

```
<vault-root>/
├── journal/
│   ├── 2026/
│   │   ├── 2026-05-17.md
│   │   ├── 2026-05-16.md
│   │   └── ...
│   ├── 2025/
│   └── ...
├── templates/
│   ├── meeting.md
│   ├── weekly-review.md
│   └── ...
├── assets/
│   ├── images/
│   └── attachments/
├── reading-notes-atomic-habits.md
├── project-alpha.md
└── ...
```

### Folders explained

| Folder | Purpose | Hyday behavior |
|--------|---------|----------------|
| `journal/<year>/` | Daily journal entries | Files named `YYYY-MM-DD.md` are auto-typed as `journal` (see `hyday-lifelog`). |
| `templates/` | Note templates | Files here are surfaced in Hyday's "新增筆記 → 從範本" menu, not as regular notes. |
| `assets/` | Images and attachments | Not indexed as notes. Linked from notes via standard Markdown image syntax. |
| (root and subfolders) | Regular notes | Any `.md` file outside the above is indexed as a note. |

### Alternate journal layouts (also supported)

Hyday tolerates two older conventions if you inherited them:

- `<vault-root>/<YYYY>/<YYYY-MM-DD>.md` — vault root *is* the journal folder (no `journal/` wrapper).
- `<vault-root>/<YYYY-MM-DD>.md` — journal entries directly at the root (legacy, rare).

For new vaults, prefer `journal/<year>/<date>.md`.

## File naming

### Journal entries

- **Required form**: `YYYY-MM-DD.md` (e.g. `2026-05-17.md`). Hyphen separators.
- **Also accepted**: `YYYY.MM.DD.md` (e.g. `2026.05.17.md`). Dot separators.
- Filenames that look like dates but don't match these patterns are treated as regular notes.

### Regular notes

- Any descriptive filename ending in `.md`, e.g. `project-alpha.md`, `reading-notes-atomic-habits.md`.
- Avoid characters that are illegal in filenames on macOS/Windows: `/ \ : * ? " < > |`.
- Avoid filenames that look like dates (see above) unless you want the file to be a journal entry.
- Lowercase with hyphens is a safe default; Hyday displays the `title` from frontmatter, so the filename is only the on-disk identifier.

## What Hyday writes automatically

When you save a note from inside Hyday, the app maintains some on-disk state alongside your `.md` files. You'll see folders/files like:

| Path | Purpose | Should an agent touch it directly? |
|------|---------|---------------------------|
| `.notes-index/` | Index cache used for fast search and sort | **No** — Hyday regenerates this. |
| `.hyday/whiteboards-v2.json` | Whiteboard data (boards, items, connections) | **Not by hand.** Use the `hyday-whiteboard` MCP server (see `hyday-whiteboard` skill) — it handles backups and schema. |
| `.hyday/...` (other files) | Per-note app sidecars (table layouts, embeddings, etc.) | **No** — created automatically by Hyday. |
| `*.tlayout` | Per-note table layouts (legacy location) | **No**. |

**Rule of thumb**: only read and write the `.md` files (and files inside `assets/`). Sidecars under `.hyday/` are touched by Hyday or by the dedicated MCP servers — not by raw file edits.

## Workflow: Adding a new note from outside Hyday

1. **Decide the kind of file**:
   - Daily log? → `journal/<year>/<YYYY-MM-DD>.md`, use `hyday-lifelog` marks.
   - Regular note? → `<vault-root>/<slug>.md` (or any subfolder under root that isn't reserved).
   - Template? → `templates/<slug>.md`.
2. **Use the right frontmatter** — see `hyday-markdown`. For journal files, frontmatter is usually empty or just `tags:`.
3. **Write the file** with the correct relative path and extension.
4. **Let Hyday pick it up** — usually within seconds when the app is open. The user doesn't need to restart.

## Workflow: Finding an existing note

1. Search by **title** first — Hyday's UI uses `title` from frontmatter as the display name, but the filename rarely matches.
2. If you only have a title, grep frontmatter:
   ```bash
   grep -l 'title: "Project Alpha"' <vault-root>/**/*.md
   ```
3. For journal entries, the filename IS the date — go straight to `journal/<year>/<date>.md`.

## Workflow: Renaming a note

- Renaming the **file** does not break backlinks if you keep the `title` the same — Hyday matches backlinks by title first.
- Renaming the **title in frontmatter** may break `[[title]]` style backlinks elsewhere. If you change a title, scan the vault for `[[old-title]]` and update.

## Validation checklist

After any vault operation:

1. New journal files are under `journal/<year>/` and named `YYYY-MM-DD.md`.
2. New regular notes have a `.md` extension and avoid date-shaped filenames.
3. Frontmatter is valid YAML wrapped in `---` (see `hyday-markdown`).
4. You haven't modified `.notes-index/`, `*.tlayout`, or other dotfiles.
5. Image references in notes point to files inside `assets/` (or external URLs).

## References

- Writing note content: see `hyday-markdown` skill
- Writing journal entries: see `hyday-lifelog` skill
- Hyday whiteboard data (note: not stored in the vault): see `hyday-whiteboard` skill
