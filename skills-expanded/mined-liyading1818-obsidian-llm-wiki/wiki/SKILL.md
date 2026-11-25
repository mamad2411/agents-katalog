---
name: wiki
description: Operate on the user's personal Obsidian LLM-Wiki vault (repository root). Use when the user invokes /wiki, asks a question that should be answered using their knowledge base, asks to ingest a new source into the wiki, asks to lint or health-check the wiki, or asks to generate a document (analysis, comparison, summary, slide deck) from wiki content. The wiki follows Karpathy's LLM Wiki pattern documented in AGENTS.md at the repo root.
---

# Wiki Skill

This skill turns the agent into a disciplined maintainer of the user's personal knowledge base at `<VAULT_ROOT>` (the repository root).

## Step 0 — Always read AGENTS.md first

**Before doing anything**, read `AGENTS.md` at the vault root. It defines the directory layout, page conventions, frontmatter schema, log format, and detailed workflows. This SKILL.md is only a dispatcher; AGENTS.md is the source of truth.

## Dispatch: what is the user asking?

Pick exactly one of these intents from the user's message:

| User intent | Workflow |
| --- | --- |
| Asking a question, wants analysis / synthesis | **Query** (below) |
| Dropped a new file or said "ingest this" | **Ingest** (see AGENTS.md §4.1) |
| Said "lint" / "health check" / "find problems" | **Lint** (below) |
| Wants a comparison / slide deck / chart / report | **Generate artifact** (below) |
| Just exploring or unsure | Run `wiki stats` then ask what they want |

If unclear, ask one short clarifying question before proceeding.

## Query workflow

1. Run `wiki search <keyword>` in the repo root to find candidate pages. Use multiple keyword variations if needed.
2. Read `wiki/index.md` to see the catalog.
3. Read the candidate pages found in step 1.
4. If still missing context, fall back to reading the relevant files in `raw/` or `clippings/`.
5. Synthesize an answer with `[[wikilink]]` citations to wiki pages and `[文章](../raw/xxx.md)` citations to raw sources.
6. **If the answer has lasting value** (a comparison, a derived insight, a non-trivial synthesis), write it as a markdown file to **`output/<YYYY-MM-DD>-<short-slug>.md`** with frontmatter:

   ```yaml
   ---
   type: artifact
   kind: answer | comparison | analysis | report | slides
   created: <date>
   question: "<the user's question, verbatim>"
   sources_used: [wiki/concepts/X.md, wiki/sources/Y.md, ...]
   ---
   ```

   Then ask the user: "要不要把这份输出归档为 `wiki/questions/<slug>.md`？"（If yes, copy + update index.md & log.md.）
7. If the answer is trivial (a fact lookup), just answer in chat — no file needed.

## Lint workflow

1. Run `wiki lint` — this writes `lint/<today>.md` automatically.
2. Read that file and **summarize** for the user (which issues are real, which are false positives like literal `[[examples]]` in docs).
3. Propose a prioritized fix plan. **Don't auto-fix** — let the user pick.

## Generate artifact workflow

Same as Query, but the deliverable form is explicit (table / Marp slides / Python chart / canvas). Always save to `output/`. For slide decks, use Marp markdown format. For charts, write a Python script to `output/scripts/` and run it to produce the image alongside.

## Output directory convention

```
output/
├── 2026-06-26-rag-vs-llm-wiki.md          # answer / comparison artifact
├── 2026-06-26-karpathy-summary.slides.md  # Marp slide deck
├── scripts/                                # helper scripts for chart generation
└── assets/                                 # rendered images, exports
```

The `output/` directory is **LLM-owned, append-only** (don't delete prior artifacts without asking). Each file must have the frontmatter shown above so the user can later promote artifacts into the wiki.

## CLI commands available (run from `<VAULT_ROOT>`)

Only four commands, deliberately minimal:

```text
wiki stats              # overview: page counts by type/status
wiki log -n 10          # last N entries from wiki/log.md
wiki search <regex>     # full-text search (--scope wiki|raw|clippings|all)
wiki lint               # write lint/<today>.md with orphans/broken/stubs
```

Everything else (creating pages, editing frontmatter, updating index.md, appending to log.md) is done by **directly reading and writing markdown files**. Don't ask for a CLI to do file edits — that's your job.

## Critical rules (from AGENTS.md)

- **Never modify** files in `raw/` or `clippings/`.
- **Every ingest** must update `wiki/index.md` and prepend an entry to `wiki/log.md` with format `## [YYYY-MM-DD] ingest | <title>`.
- Cross-reference with `[[double-brackets]]` between wiki pages.
- Pages need YAML frontmatter (`type`, `tags`, `created`, `updated`, `sources`, `status`).
- When uncertain, ask the user. Don't do silent large refactors.

## Reporting style

After completing a workflow, give the user a **short** summary:

- What you did (1–3 bullets)
- What artifacts were created or modified (relative paths)
- Any unresolved questions or new gaps you noticed

Keep it tight. The user is browsing Obsidian in parallel and can see file changes.
