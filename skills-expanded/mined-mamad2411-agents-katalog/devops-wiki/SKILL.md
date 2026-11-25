---
name: devops-wiki
description: Azure DevOps wiki management. Use when asked to create, read, update, or search wiki pages in Azure DevOps.
---

# DevOps Wiki

## When to Use

- User asks to create, read, update, or delete wiki pages
- User wants to find documentation in a DevOps wiki
- User says "write this up in the wiki", "update the docs for..."

## Instructions

### Creating Wiki Pages

Use `devops_create_wiki_page` with:
- **path** — full page path (e.g., `/Architecture/Decision Records/ADR-001`)
- **content** — markdown content

Follow wiki formatting standards:
- Start with a level-1 heading matching the page title
- Use `[[_TOC_]]` for table of contents on long pages
- Link to related pages: `[Link text](/path/to/page)`
- Reference work items: `#12345`

### Updating Wiki Pages

1. Use `devops_get_wiki_page` to read current content and get the eTag
2. Make targeted edits — don't rewrite entire pages unless asked
3. Use `devops_update_wiki_page` with updated content and eTag

### Writing Quality

- Be concise — scannable, not essays
- Use headings (H2/H3) to break content into sections
- Include fenced code blocks with language hints
- Use Mermaid syntax for diagrams
- One topic per page, link to related pages

## Tools

- `devops_list_wikis` — List all wikis in a project
- `devops_get_wiki_page` — Read a wiki page by path
- `devops_create_wiki_page` — Create a new wiki page
- `devops_update_wiki_page` — Update an existing wiki page
- `devops_delete_wiki_page` — Delete a wiki page
- `devops_list_wiki_pages` — List pages in a wiki
- `devops_search_wiki` — Search wiki pages by keyword

## See Also

- **devops-boards** — for work items referenced in wiki documentation
