---
description: Load documentation from their respective websites into local markdown files our agents can use as context.
allowed-tools: Task, WebFetch, Write, Edit, Read, Bash(ls*), Bash(cat package.json*), Glob, mcp__firecrawl-mcp__firecrawl_scrape
---

# Load AI Docs

Load documentation from their respective websites into local markdown files our agents can use as context.

## Variables

DELETE_OLD_AI_DOCS_AFTER_HOURS: 24

## Workflow

1. **Read the README index**
   - Read `ai_docs/README.md`
   - Parse each section's table to extract URLs with their `source_type` and `framework_version` metadata
   - The table format is: `| URL | source_type | framework_version |`
   - Skip sections that are comments only (deployment, backend)

2. **Read current package.json versions**
   - Read the root `package.json` and relevant workspace `package.json` files
   - Extract current dependency versions for version mismatch detection

3. **Check cached docs**
   - For each URL, derive the cached filename (existing convention)
   - If cached file exists, read its YAML frontmatter for `scraped_at` ISO timestamp
   - If no frontmatter exists, fall back to the file's filesystem modification time
   - If scraped within the last `DELETE_OLD_AI_DOCS_AFTER_HOURS` hours, skip it
   - If older, delete it

4. **Scrape in parallel**
   - For each URL that was not skipped, use the Task tool in parallel with the `scrape_loop_prompt`:
   <scrape_loop_prompt>
   Use @agent-docs-scraper agent - pass it the url as the prompt. After saving the file, ensure it has YAML frontmatter with these fields:
   - `scraped_at`: current UTC ISO 8601 timestamp (e.g. `scraped_at: 2026-03-26T08:37:18Z`)
   - `source_type`: {source_type} (passed from README table)
   - `framework_version`: {framework_version} (passed from README table)
   - `source_section`: {section_name} (the README section this URL belongs to)
   If the file already has frontmatter, merge these fields; if not, prepend a `---` delimited block.
   </scrape_loop_prompt>

5. **Freshness flagging**
   - After all scrapes complete, check for freshness ambiguity:
     - Group scraped docs by `source_section`
     - Within each section, if multiple docs cover overlapping topics at different `framework_version` levels, add a `## Freshness Notes` section at the top of the NEWER doc noting:
       - Which other docs in the same section may conflict
       - Their respective `source_type` rankings (official_docs > official_repo > community_repo > blog > npm)
     - Compare `framework_version` from frontmatter against actual `package.json` dependency versions
       - If mismatch detected, add `version_mismatch: true` to the frontmatter and a warning line in Freshness Notes

6. **Report**

```
AI Docs Report:
- <✅ Success or ❌ Failure>: <url> - <markdown file path> [source_type: <type>, version: <version>]
- ...

Freshness Flags:
- <file>: <description of flag>
- ...
```
