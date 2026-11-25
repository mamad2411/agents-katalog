---
name: apple-docs
description: Look up Apple's developer documentation, Human Interface Guidelines, App Store Connect Help, sample code and WWDC sessions with the Apple Docs 2.0 MCP server. Use it before writing or fixing Swift or any code that calls an Apple framework, and for Apple design and App Store questions.
---

# Apple Docs

Answer from Apple's own documentation instead of memory, with the Apple Docs 2.0 MCP server (`apple-docs`): API
reference with full signatures and OS availability, articles and tutorials, the Human Interface Guidelines, App Store
Connect Help, sample code, and 1,700 WWDC sessions (2014–2026) with transcripts and code.

## Connect

Installing this skill adds instructions only; it doesn't register the server. If the apple-docs tools aren't
available, add the server to your agent and restart it. In Claude Code:

```bash
claude mcp add apple-docs -- npx -y apple-docs-2.0-mcp
```

Other clients take the same command in their MCP settings: `"command": "npx", "args": ["-y", "apple-docs-2.0-mcp"]`.
No API key or account is needed.

## Use

- Before writing or fixing code that calls an Apple framework, search first with `search_apple_docs` (or
  `search_docs_map` for a name or part of one), then read the page with `get_apple_doc_content`.
- For working code, call `search_wwdc_content` with `view: "examples"` and the type the code uses as `query`, then
  `get_wwdc_video` for the session.
- For design questions, search with type `design` and read the guideline page.
- The server sends its own search instructions when it connects; follow them.
