---
name: llmwiki-ingest
description: Ingest one source document (or a folder of them) into the llmwiki. Use when the user drops a new markdown file, PDF, or URL into the wiki and asks you to process it. The user will typically say "ingest this", "add this to the wiki", "process this file into the wiki", or point at a file under `raw/`.
---

# llmwiki-ingest

## What this skill does

Takes a source file (or a folder) and turns it into wiki pages following the Karpathy LLM Wiki pattern:

1. Writes a `wiki/sources/<slug>.md` summary
2. Creates/updates entity pages for people, companies, projects, tools, libraries mentioned
3. Creates/updates concept pages for ideas, patterns, decisions discussed
4. Cross-links everything with `[[wikilinks]]`
5. Flags contradictions
6. Updates `wiki/index.md`, `wiki/overview.md`, `wiki/log.md`

## When to use

- User says "ingest this file", "add this to the wiki", "process this into the wiki"
- User runs the `/wiki-ingest` slash command
- User says "sync the wiki" — in that case, the `llmwiki-sync` skill runs the converter first, then invokes this skill for each new file

## Workflow

Follow the **Ingest Workflow** from the repo's `CLAUDE.md` exactly:

1. Read the source file(s) with the Read tool
2. Read `wiki/index.md` and `wiki/overview.md` for context
3. Write `wiki/sources/<slug>.md` using the Source Page Format
4. Update `wiki/index.md` — new entry under `## Sources`
5. Update `wiki/overview.md` if substantial new info
6. Create/update entity pages (`wiki/entities/<TitleCase>.md`)
7. Create/update concept pages (`wiki/concepts/<TitleCase>.md`)
8. Cross-link with `[[wikilinks]]` under `## Connections`
9. Flag contradictions under `## Contradictions`
10. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <title>`

## Session-specific rules

When the source is under `raw/sessions/` (a session transcript converted by the converter):

- **Trust the frontmatter** as authoritative (project, started, model, tools_used, etc.)
- **Do not copy the `## Conversation` section verbatim** — use it as raw material to summarise
- **Create a project entity page** at `wiki/entities/<ProjectSlug>.md` with a `## Sessions` list
- **Extract decisions** into `wiki/concepts/` — anything the user explicitly locked
- **Extract tools used** — every entry in `tools_used` is a candidate entity
- **If `is_subagent: true`** — link to the parent session rather than creating a new project entity

## Hard rules

1. `raw/` is immutable. Never modify files there.
2. No silent overwrites. Conflicting claims go under `## Contradictions`.
3. Every page has a `## Connections` section with at least one `[[wikilink]]`.
4. Frontmatter is authoritative. Always populate `title`, `type`, `tags`, `sources`, `last_updated`.
