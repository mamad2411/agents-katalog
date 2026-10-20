# src/lib/
> L2 | parent: src/CLAUDE.md

Content pipeline utilities — read markdown from `content/`, parse frontmatter, render to HTML.

## Members

- `og.ts`: Build-time OG metadata fetcher with filesystem cache (`.cache/og/`). Exports `fetchOgData()`, `OgData`.
- `markdown.ts`: Async GFM markdown renderer wrapping `marked` + OG link previews. Bare URLs on own lines become glass-panel preview cards. Exports `renderMarkdown()`.
- `content.ts`: Content abstraction layer. Reads `.md` files from `content/{type}/`, parses YAML frontmatter, returns typed `Entry` objects with rendered HTML and link previews. Exports `getEntries()`, `getEntry()`, `getSlugs()`.

[PROTOCOL]: update this file on member changes, then check parent CLAUDE.md
