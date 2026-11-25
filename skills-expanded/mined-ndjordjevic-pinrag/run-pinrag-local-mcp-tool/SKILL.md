---
name: run-pinrag-local-mcp-tool
description: >-
  Use when the user wants to query, list, add, or remove documents in PinRAG, or
  index PDFs/files/URLs into PinRAG via the local (stdio) PinRAG MCP server. Always
  use PinRAG MCP tools via call_mcp_tool (never Python scripts or one-off CLI unless
  they explicitly ask for code). Discover which PinRAG server is available from the
  workspace mcps folder or ~/.cursor/mcp.json; server id is user- plus the mcp.json key.
---

# Run PinRAG local MCP tools (not Python)

## Non-negotiable

- **Use `call_mcp_tool`** with PinRAG’s MCP tools: `add_document_tool`, `query_tool`, `list_documents_tool`, `remove_document_tool`.
- **Do not** implement indexing or querying with Python (`python -c`, ad-hoc scripts, LangChain/Chroma calls, or `pinrag`/`uv run` in the terminal) unless the user **explicitly** asks for scripts, debugging, or automation outside the editor MCP.
- **Do not** skip MCP because “it’s faster to script”—the user’s editor and `PINRAG_PERSIST_DIR` are wired through the MCP server process.

## How to find which PinRAG MCP is “active”

Cursor exposes **one server id per `mcp.json` entry**. The id you pass to `call_mcp_tool` is:

**`user-` + the exact key** of that entry in `~/.cursor/mcp.json` (hyphens preserved).

Examples:

| Typical `mcp.json` key | `call_mcp_tool` `server` value |
|--------------------------|--------------------------------|
| `pinrag-dev` | `user-pinrag-dev` |
| `io-github-ndjordjevic-pinrag` | `user-io-github-ndjordjevic-pinrag` |
| `pinrag-pypi-from-link` | `user-pinrag-pypi-from-link` |

**Discovery (pick one):**

1. **Workspace MCP descriptors (best):** Under the Cursor project’s MCP folder (see system MCP instructions), look for folders `mcps/user-*/tools/` that contain **`add_document_tool.json`**. The folder name (e.g. `user-io-github-ndjordjevic-pinrag`) **is** the `server` string for `call_mcp_tool`.
2. **`~/.cursor/mcp.json`:** Find entries whose `command`/`args` run PinRAG (`pinrag`, `uvx` with `args` containing `--refresh` and `pinrag`, or `uv run … pinrag`). Each top-level key under `mcpServers` maps to `user-<that-key>`.

**If several PinRAG servers appear:**

- If the user names one (e.g. “use the marketplace / io-github pinrag”), use that key’s `user-…` id.
- Otherwise use **one** server that has the tools (prefer the one they used recently or the least ambiguous name); if unsure, **ask** which MCP entry to use.

**Before the first call:** Read the tool descriptor JSON under `mcps/<server>/tools/<tool>.json` for required parameters (per MCP instructions).

## Tools (stdio PinRAG)

| Tool | When |
|------|------|
| `add_document_tool` | Index local paths (PDF, dirs, Discord export), or pass URLs (YouTube, GitHub). **`paths`**: list of strings (use **absolute paths** for files). Optional **`tags`**: one per path. |
| `query_tool` | Questions over the index. Optional: `tag`, `document_id`, `page_min`/`page_max`, `document_type`, `response_style`. |
| `list_documents_tool` | What’s indexed; optional `tag`. |
| `remove_document_tool` | Remove by `document_id` from listing. |

## Examples

- “Add this PDF to PinRAG `/path/to/book.pdf`” → `add_document_tool` with `{"paths": ["/path/to/book.pdf"]}` (and optional `tags`).
- “What does the Amiga book say about …?” → `query_tool` with `{"query": "…"}` (add `document_id` or `tag` if they want scope).

## Remote PinRAG (HTTP)

If the user uses **PinRAG Cloud** or another **URL-based** MCP, that is a **different** MCP server name and may use the same tool names—still use **`call_mcp_tool`**, not Python; read that server’s folder under `mcps/`.
