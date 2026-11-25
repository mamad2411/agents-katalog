---
name: symbolpeek
description: Token-efficient code, JSON, and Markdown navigation; use before whole-file reads.
---

# SymbolPeek

Use SymbolPeek before whole-file reads.
Use only tools advertised by the current server; tools may be disabled locally.

- Known file: `get_document_outline`/`list_symbols`; unknown: `search_symbols`.
- Fetch: `read_symbol`; batch: `read_symbols`; local context: `read_symbol_context`.
- TS/JS: `find_references`, `find_calls`, `find_implementations`, definition/type/diagnostics.
- Refactor with `rename_symbol`/deletion checks; use `get_capabilities` when unsure.
