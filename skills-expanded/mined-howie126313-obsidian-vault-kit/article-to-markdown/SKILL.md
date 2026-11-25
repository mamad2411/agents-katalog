---
name: article-to-markdown
description: |
  Convert external URLs into structured Markdown and save to the Obsidian vault.
  Use when the user provides an external URL (article, blog post, tweet thread, newsletter) and wants it saved as an Obsidian note.
  Triggers: "save this article", "archive this link to obsidian", "bookmark article", or when user pastes a URL and asks to save/summarize/archive it.
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Bash(open *)
  - Bash(ls *)
  - AskUserQuestion
  - mcp__firecrawl__firecrawl_scrape
---

# Article to Markdown

Convert external article URLs into structured Markdown notes and save them to the Obsidian vault.

## Workflow

### Step 1: Fetch and Detect Environment

**1a. Detect vault root** — follow [../../_shared/common-steps.md](../../_shared/common-steps.md) "Vault Detection" section.

**1b. Fetch article content:**

Use `mcp__firecrawl__firecrawl_scrape` to scrape the URL. This covers most pages including JS-rendered content.

If firecrawl fails, ask the user to paste the article content directly. Do not attempt other fallback tools.

**Special cases:**
- Tweet threads: use `mcp__firecrawl__firecrawl_scrape`, reconstruct thread order
- Paywalled content: ask the user to paste content directly

### Step 2: Restructure and Link

**2a. Understand and restructure** — do NOT simply copy the raw text:

1. Identify the article's core thesis, key arguments, and supporting details
2. Determine author, publication date, and source platform
3. Restructure the content into logical sections with clear headings
4. Generate 3-8 relevant tags and a 1-3 sentence summary

**2b. Search for bidirectional links** — follow the **Bidirectional Link Search** in [../../_shared/common-steps.md](../../_shared/common-steps.md).

**2c. Format as Obsidian Markdown** — follow the template in [references/article-template.md](references/article-template.md) exactly:
- YAML frontmatter with title, date, tags, summary, source
- Blockquote metadata line with original link, author, date
- Sections: Background → content → Key Conclusions → Further Thoughts
- Include `[[wikilink]]` connections from Step 2b
- Code blocks with language identifiers

**2d. (Optional) Mermaid architecture diagram** — if the article has a clear multi-layered architecture or flow worth visualizing, embed a Mermaid diagram after the blockquote metadata and before `## Background`. Skip for simple or short articles. Use:
- `graph TD` / `graph LR` for flows
- `subgraph` for logical grouping
- Concise node labels (keywords, not sentences)
- 3-5 layers, 2-5 nodes per layer

### Step 3: Save and Confirm

**3a. Determine target directory** — follow the **Directory Mapping Rules** in [../../_shared/common-steps.md](../../_shared/common-steps.md). For external URL sources, match against the configured categories; if no rule matches, use the configured default directory.

**3b. Save** — follow the **Save and Open in Obsidian** section in [../../_shared/common-steps.md](../../_shared/common-steps.md).

**3c. Update index.md** — follow the **Index Update** section in [../../_shared/common-steps.md](../../_shared/common-steps.md). Use the article's title, summary (condensed to under 80 chars), and top 2 tags.

**3d. Report to user:**
- Article title and brief summary
- File path where it was saved
- Tag list for review
- Related notes linked (list the `[[wikilink]]` connections made)
