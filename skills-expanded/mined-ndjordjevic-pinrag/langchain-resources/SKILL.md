---
name: langchain-resources
description: LangChain/LangGraph docs, MCP server usage, and reference project lookup for pinrag
---

# LangChain/LangGraph Resource Access

MCP servers to use for LangChain/LangGraph docs and code examples:

1. **`user-docs-langchain`** (primary) — `SearchDocsByLangChain` for LangChain-specific queries
2. **`user-context7`** (fallback) — `resolve-library-id` then `query-docs` for other libraries

Check MCP servers **before** assuming any LangChain API. Use specific queries.

## Reference Projects

Read **`notes/workspace-projects-overview.md`** for the canonical list of reference projects, their structure, and "Value for PinRAG" notes. Consult it before searching for example patterns.

## Guidelines

- **Do not commit** until explicitly asked. Keep commit messages to one or two lines.
- **Search priority**: `notes/workspace-projects-overview.md` → MCP docs → internet search
- **Always cite sources** (URLs when available). Say "I don't know" rather than guessing.
