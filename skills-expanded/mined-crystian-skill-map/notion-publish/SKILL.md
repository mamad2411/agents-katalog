---
name: notion-publish
description: |
  Mirrors the portfolio's pages into Notion after publishing, creating one
  Notion page per site page via the Notion MCP. Use it from /publish, or when
  the user asks to sync the site to Notion.
tools: [mcp__notion__notion-create-pages]
---

# notion-publish

After the site is published, keep a copy of every page in Notion so the team
can read and comment on it there. An OpenCode native skill
(`.opencode/skills/`).

## Steps
1. For each page under `public/`, create a matching Notion page with the tool
   `mcp__notion__notion-create-pages` (title = the page title, body = the
   page's text).
2. Report the created Notion page links.

The `mcp://notion` node is drawn from this skill's `tools` frontmatter (the
`core/mcp-tools` reader materialises it; OpenCode has no project-local MCP
config skill-map can read). Notion needs your own authentication configured in
your MCP client.
