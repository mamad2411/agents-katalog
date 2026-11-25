---
name: research-portal
description: >-
  Build and manage a local MkDocs Material "research portal" over a folder of
  Typora/markdown research notes (e.g. ~/notes or a Dropbox-synced folder),
  keeping the original .md files untouched. Use this whenever the user wants to collect,
  browse, organize, or curate a folder of dated markdown notes into a searchable
  navigable site; wants a lighter local alternative to Obsidian / Notion / Outline
  / Logseq for their own notes; needs perfect LaTeX/math rendering in a notes
  site; wants notes grouped by project in a sidebar; or wants to tag/rename notes
  by project without breaking image links. Trigger even if they don't say
  "MkDocs" or "portal" but describe wanting to "정리해서 모아 보기", make a personal
  wiki, or render math from their note folder.
---

# Research Portal

Turn a folder of dated markdown notes into a local, searchable MkDocs Material
site with project-grouped navigation and full LaTeX rendering, without ever
modifying the source notes. The site is read/browse oriented; authoring stays in
the user's existing editor (Typora), so the `.md` files remain the canonical
source.

## When this fits (and when it doesn't)

This is the right tool when notes are flat markdown files in a folder (often
Dropbox-synced), named by date like `YYYYMMDD[_PROJECT].md`, with images in
sibling `<stem>.assets/` folders. It deliberately avoids database-backed wikis
(Outline needs Postgres/Redis/SSO; Notion is a SaaS DB) because those divorce
content from the user's files and break the Typora workflow. If the user instead
wants backlink/graph visualization, mention Quartz as a complement; this skill
does not do graphs.

## Design choices (read `references/design.md` for the why)

- `docs_dir` points straight at the notes folder. The site serves `.md`,
  `.assets/` images, and PDFs in place; originals are never touched.
- Only three helper files land in the notes folder, all regenerable/deletable:
  `index.md` (home), `SUMMARY.md` (sidebar nav), `javascripts/mathjax.js`.
- Math: `pymdownx.arithmatex` (generic) protects inline `$...$` from markdown,
  and MathJax 3 also scans raw `$$...$$` as a fallback because arithmatex's block
  processor does not descend into list items (Typora notes often nest display
  math under bullets). This combination renders both reliably.
- Broken symlinks in the source abort an mkdocs build, so the scaffolder
  auto-excludes any first-level subtree that contains dangling links.

## Workflow

All commands run from the portal dir with `uv`. Scripts are bundled in
`scripts/`; the scaffolder copies `gen_index.py` and `tag_note.py` into the
portal dir so the portal is self-contained.

### 1. Scaffold

Ask for the notes folder if not given. Then:

```bash
python <skill>/scripts/scaffold.py \
  --notes-dir ~/notes \
  --portal-dir ~/research-portal \
  --name "Research Portal" --lang ko --port 8123
```

This writes `mkdocs.yml`, copies the helper scripts, writes the MathJax config,
detects broken-symlink subtrees to exclude, then creates the uv venv, installs
`mkdocs-material` + `mkdocs-literate-nav`, and builds the nav. Pass `--no-install`
to only generate files (it then prints the uv commands to run).

### 2. Serve

```bash
cd ~/research-portal && uv run mkdocs serve -a 127.0.0.1:8123
```

Run it in the background so you can keep working; it live-reloads when notes or
config change. After installing a new plugin, restart serve (a running process
won't see newly installed packages). Tell the user the URL and suggest a hard
refresh (Ctrl+Shift+R) after JS/config changes.

### 3. Regenerate nav after adding/removing notes

```bash
cd ~/research-portal && uv run python gen_index.py --title "Research Portal"
```

`gen_index.py` parses `YYYYMMDD[_PROJECT[_extra]].md`, groups by project (most
notes first, untagged "Daily" last), labels each entry by date, and writes
`index.md` + `SUMMARY.md`. It reads the notes dir from `docs_dir` in `mkdocs.yml`.

### 4. Tag / rename notes by project

Untagged date-only notes show up under "Daily". To file them under a project,
first read enough of each note to classify it (section headers `grep -E '^#{2,3} '`
are a fast topic fingerprint). For genuinely multi-project notes, ask the user
rather than guessing. Then:

```bash
cd ~/research-portal
# preview first
uv run python tag_note.py --project ProjectA 20240115 20240116 --dry-run
# apply
uv run python tag_note.py --project ProjectA 20240115 20240116
```

`tag_note.py` renames `<stem>.md`, the `<stem>.assets/` folder, and a matching
`<stem>.pdf`, and rewrites every `<stem>.assets` reference across ALL notes
(image references can be cross-file). It then verifies all `*.assets` references
resolve. Use `--rename OLD NEW` for an explicit single rename (e.g. re-tagging an
already-suffixed note). Always run gen_index.py afterward to refresh the nav.

## Verify before reporting done

- After scaffold/build: `uv run mkdocs build` exits 0 (the red "MkDocs 2.0"
  notice from Material is harmless). Confirm math by grepping the built page for
  `class="arithmatex"` and that `*.assets/` images copied into `site/`.
- After tagging: the script's own link verification must report "all asset refs
  resolve OK"; also confirm no date-only notes remain if the intent was to clear
  "Daily" (`ls <notes> | grep -E '^[0-9]{8}\.md$'`).

## Scripts and references

- `scripts/scaffold.py` — create/refresh the portal project and uv env
- `scripts/gen_index.py` — regenerate `index.md` + `SUMMARY.md`
- `scripts/tag_note.py` — safe project tagging/renaming with link repair
- `references/design.md` — rationale for the math config, file layout, and the
  Outline/Obsidian comparison; read it if the user questions a design decision or
  wants to adapt the setup (different filename scheme, KaTeX, hosting, etc.).
