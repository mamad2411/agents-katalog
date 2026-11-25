---
name: notion-importer
description: >
  Import Notion pages into project vault via MCP. Trigger when user wants to import
  or sync Notion content into the vault: "import notion", "notion docs", "sync notion",
  "импортируй notion", "обнови notion", "sync notion pages", "обнови notion docs".
  Uses the claude.ai Notion MCP server (notion-fetch tool) directly from a live
  Claude session. Does NOT spawn subprocesses.
---

# Notion Importer Skill

Import Notion pages into the project vault using the `claude.ai Notion` MCP server.
This skill calls MCP tools directly from a live Claude session — no subprocess needed.

## Trigger Phrases

English: "import notion", "notion docs", "sync notion", "sync notion pages", "import notion pages"
Russian: "импортируй notion", "обнови notion", "обнови notion docs", "синхронизируй notion"

## Required Setup

The project must have `.claude/notion_pages.json` configured.
Run `claude-dev-stack notion add <url>` to add pages.

## Import Steps

1. **Read config**: Load `.claude/notion_pages.json` to get the list of pages.

```bash
cat .claude/notion_pages.json
```

2. **Fetch each page**: For each page in `config.pages`, call the `notion-fetch` MCP tool
   with the `page_id` to retrieve markdown content. Use the MCP tool directly:

```
notion-fetch(page_id: "<page_id>")
```

   Or use `notion-search` MCP tool if you need to locate pages by title.

3. **Determine vault path**: Use the `vault_path` field from the page config
   (default: `docs/notion`). Resolve against the vault project directory:
   `vault/projects/{project-slug}/docs/notion/`

4. **Write with provenance**: Each imported file gets a frontmatter stamp:

```markdown
---
notion_page_id: <page_id>
notion_last_synced: <ISO timestamp>
notion_content_hash: <SHA-256 of content below frontmatter>
---

<page content>
```

5. **3-way hash check** (overwrite protection, per D-06):
   - If file does not exist → create it with stamp (status: created)
   - If `notion_content_hash` in frontmatter matches hash of new content → skip (status: unchanged)
   - If local body hash matches stored `notion_content_hash` (no local edits) → overwrite in place (status: updated)
   - If local body hash differs from stored `notion_content_hash` (local edits detected) → write `{filename}.notion-update.md` sibling and warn (status: conflict)

6. **Filename convention**: Use the page title for the filename, cleaned with the same rules
   as `cleanNotionFilename()` in `lib/docs.mjs` — strip Notion UUID suffixes, lowercase,
   replace spaces with hyphens. Example: `My Page abc123...` → `my-page.md`

7. **Report results**: Print a summary of created/updated/unchanged/conflict counts.

## Important Notes

- **Use MCP tools directly** — call `notion-fetch` or `notion-search` from the Claude session.
  Do NOT spawn `node`, `claude mcp call`, or any subprocess.
- The `notion_pages.json` config is per-project (`.claude/notion_pages.json`).
- After import, existing `notebooklm sync` picks up the new files automatically.
- If the Notion MCP server is not configured, run: `claude mcp add notion`
- Check MCP status: `claude mcp list`

## Example Session

```
User: импортируй notion
Claude: [reads .claude/notion_pages.json]
        [calls notion-fetch(page_id: "abc123...") via MCP]
        [writes vault/projects/myproject/docs/notion/my-page.md with frontmatter]
        Summary: 1 created, 0 updated, 0 unchanged, 0 conflicts
```
