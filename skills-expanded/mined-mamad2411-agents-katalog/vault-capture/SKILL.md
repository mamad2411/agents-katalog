---
name: vault-capture
description: Save web content to the Obsidian vault. Given a URL, extracts clean content via defuddle, creates a formatted note with frontmatter and wikilinks to related vault content, and files it in a new project folder. Use when the user shares a URL to save to their knowledge base.
---

# Vault Capture

Save a URL as a formatted Obsidian note in the vault. Extracts content via defuddle, generates structure and wikilinks, files into a new project folder.

## Workflow

1. **Extract content from the URL:**
   ```bash
   defuddle parse <url> --md
   defuddle parse <url> -p title
   defuddle parse <url> -p description
   defuddle parse <url> -p domain
   ```
   If defuddle is not installed: `npm install -g defuddle`

2. **Determine a folder name** following vault conventions:
   - Format: `snake_case` with source/author suffix when known
   - Examples: `agent_routing_patterns_anthropic`, `obsidian_cli_guide_kepano`, `mcp_servers_overview_ai_labs`
   - Check the URL domain + page title to construct a descriptive slug
   - Ask the user if unclear

3. **Search for related vault projects:**
   ```bash
   obsidian search query="<2-3 key topics from the content>" limit=10
   ```
   Run 1-2 searches. Collect matching folder names for wikilinks.

4. **Compose the note.** For content longer than ~2,000 chars, use the `Write` tool directly rather than the CLI `create` command:

   ```markdown
   ---
   description: <extracted or synthesized one-liner>
   title: <page title>
   date: YYYY-MM-DD
   source: <url>
   ---

   # <Title>

   > <extracted description or brief summary>

   ## Key Takeaways
   - <Claude-generated bullet summary, 3-7 points>

   ## Content

   <cleaned extracted markdown content>

   ## Related
   - [[related_folder/README]]
   - [[another_folder/gemini3_summary]]
   ```

5. **Write the file:**
   - For short content: `obsidian create path="<folder_name>/README.md" content="..." silent`
   - For long content: Use `Write` tool to write to `<vault-root>/<folder_name>/README.md`

6. **Log to daily note** (optional, do by default unless user says not to):
   ```bash
   obsidian daily:append content="### HH:MM — Captured: <title>\nSaved [[<folder_name>/README]] from <domain>.\n**Source:** <url>\n"
   ```

7. **Report** the folder created, the file path, and any related links found.

## Tips

- Always include the `source` frontmatter property with the original URL
- If the content is very long (>5,000 words), summarize rather than include in full — put the summary in `## Content` and note that the full content is at the source URL
- Prefer `## Key Takeaways` as bullet points over dense prose — this vault is a research reference
- If the user provides context ("this is about MCP servers"), use that to improve the folder name and search queries
