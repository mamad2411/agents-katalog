---
name: nightly-obsidian-index
description: Nightly vault index + morning briefing of what changed in your markdown vault.
---

Scan the vault for new or modified notes and update ALL index files to keep them
current. Ensure 100% wiki coverage and maintain the hot cache as a running
modification log.

> Placeholders: replace `{{VAULT_PATH}}` with your vault path (the `VAULT_PATH`
> env var). Scripts live in the Eidetic OS `scripts/` directory referenced as
> `{{EIDETIC_OS}}/scripts`.

**Objective:** Detect new or modified notes since the last index run, update all
index files, ensure wiki completeness, append to the hot cache, and produce a
morning briefing.

**Steps:**

1. Request access to `{{VAULT_PATH}}`
2. Read the existing `.claude-index.md` and `wiki/index.md`
3. Find all `.md` files modified since the last index (check timestamps)
4. For each new or modified note:
   - Read the note contents
   - Extract key topics, tags, and a brief summary
5. Update `.claude-index.md`:
   - Add entries for new notes in the appropriate section
   - Update summaries for modified notes
   - Update the "last indexed" timestamp
   - Update aggregate stats (total note count, notes per folder)
6. **FULL WIKI SYNC** — Check ALL `.md` files in the vault (not just new ones) against `wiki/index.md`:
   - Find every `.md` file in the vault (excluding `.git/`, `.rag/`, `.claude/`, `node_modules/`, `.obsidian/`)
   - Compare against `wiki/index.md` entries
   - Add wikilinks and one-line descriptions for ANY missing files
   - Create new sections if needed
   - Remove dead links (files referenced in index that no longer exist)
   - Update the file count in the index header
   - Target: 100% coverage — every `.md` file should be in the wiki index
7. **APPEND TO HOT CACHE** — Update `wiki/hot.md` as a RUNNING LOG (append-only, never truncate):
   - Find all `.md` files modified since the last index run
   - PREPEND a new dated section at the top of `wiki/hot.md`:
     ```
     ## YYYY-MM-DD HH:MM — Nightly Index Run
     X files modified since last run:
     - [[filename]] — one-line description (modified/created)
     ```
   - Do NOT delete or overwrite existing entries — the hot cache is a permanent history
   - If no files were modified, prepend: "## YYYY-MM-DD — No changes detected"
   - Keep the frontmatter and header intact at the very top of the file
8. Update `wiki/log.md` with a sync entry
9. Commit vault changes to git:
   - Run `EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} eidetic commit --json`
   - Capture the JSON output (commit hash, counts of new/modified/deleted files)
   - If it returns `"status": "clean"`, note "no changes committed" for the briefing
10. Produce a morning briefing and save to `.claude-morning-briefing.md`:
    - How many notes were added or changed
    - What topics they cover
    - Wiki coverage percentage (X of Y files indexed)
    - Hot cache: confirm updated, list files added this run
    - Flag anything relevant to active projects
    - Flag any changes to system files as high-priority
    - Include the git changelog: run `EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} eidetic changelog --since "24 hours ago" --markdown` and append the output
    - Include the commit hash from step 9 so the briefing is traceable
    - If nothing changed, just say "No changes since last index"
    - Make it scannable in 30 seconds

**Constraints:**
- Do NOT modify any existing notes — only update `.claude-index.md`, `wiki/index.md`, `wiki/hot.md`, `wiki/log.md`, and `.claude-morning-briefing.md`
- NEVER truncate `wiki/hot.md` — it is an append-only running log
- Keep the index files well-organized
- Be thorough but concise
