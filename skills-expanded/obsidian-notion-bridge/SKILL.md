---
name: obsidian-notion-bridge
description: Safely bridge Obsidian Markdown notes and Notion pages while preserving source-of-truth, tags, links, page IDs, URLs, and metadata. Use when the user asks to sync, publish, migrate, convert, summarize, or organize knowledge between Obsidian, Notion, local memory, or RAG indexes.
---

# Obsidian Notion Bridge

Use this skill when knowledge should move between local notes and Notion.

## Source Of Truth

- Prefer Obsidian/local Markdown as source of truth for personal knowledge unless the user says Notion is authoritative.
- Keep Notion updates as draft payloads until explicitly applied.
- Preserve source paths, Notion page IDs, Notion URLs, tags, aliases, and wikilinks.

## Workflow

1. Inspect selected scope.
   - Read only selected notes/pages first.
   - Extract title, tags, wikilinks, frontmatter, URLs, and IDs.

2. Plan mapping.
   - Obsidian heading -> Notion page title.
   - Obsidian tags -> Notion multi-select/tag property.
   - Wikilinks -> text references unless a target page map exists.
   - Notion page ID/URL -> Markdown frontmatter.

3. Draft conversion.
   - Use bridge tools to create Notion payload plans or Obsidian Markdown plans.
   - Use RAG tools to chunk/index notes only after source metadata is preserved.

4. Verify.
   - Check frontmatter validity.
   - Check links/tags are not silently dropped.
   - Call out any lossy conversion.

## Safety

- Do not mass rename notes.
- Do not auto-delete old notes/pages.
- Do not auto-sync an entire vault without a reviewed plan.
- Keep private notes private unless the user asks to publish or share.

