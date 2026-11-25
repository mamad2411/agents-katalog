---
name: ingest
description: Process raw files from vault/sources/ into linked wiki pages. Actions - all (every unprocessed source), file (one specific source), overview.
---

# Task

Execute the requested action: $ARGUMENTS

Calling rule: `/ingest <action> <arguments>`.

If the requested action is ambiguous or contradictory, do NOT guess: flag it and ask for clarification before executing.

---

## If action is empty

Describe this skill: its purpose and the actions table from "overview". Do not execute anything.

## If action is "overview" (or unknown)

| Argument | Action |
| :--- | :--- |
| `all` | Process every unprocessed file in `vault/sources/` |
| `file <name>` | Process one specific source file |
| `overview` | This table |

If the action was unknown, say so first, then show the table.

---

## If action is "all" or "file"

1. Scope:
   - `all`: list `vault/sources/` and compare against `vault/log.md` ingest entries to find unprocessed files. Large batches: one source at a time, report progress.
   - `file <name>`: match the name in `vault/sources/`; if missing or empty, list the folder and ask.
2. **Read each source fully.** PDFs, images, transcripts, articles alike.
3. **Integrate, don't just summarize**, per source:
   - Update existing pages where the topic exists; create new pages only for genuinely new topics (one topic per page).
   - Add YAML frontmatter (`tags`, `created`, `updated`, `source`) and `[[wiki links]]` to every related page. A single source may touch 10-15 pages.
   - Route by content: user-related → `vault/me/`, project-related → `vault/projects/<name>/`, general knowledge → `vault/knowledge/`.
   - **Flag contradictions** explicitly in the page and in the report; never silently overwrite.
4. **Never modify the source file itself** (CLAUDE.md hard rule).

---

## After any action

- One log entry per source: `## [YYYY-MM-DD HH:MM] /ingest | <source> -> pages touched`.
- Update `vault/index.md` with new pages.
- Report: sources processed, pages created/updated, contradictions flagged.

## Notes

- All pages must pass markdownlint.
