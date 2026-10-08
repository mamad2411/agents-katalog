# nebu-ctx — Context Engineering Layer

Use only the public nebu-ctx MCP surface when guidance needs nebu-ctx tools:

| PREFER | OVER | Why |
|--------|------|-----|
| `ctx_read(target="file"|"files"|"symbol"|"outline"|"archive", ...)` | Read / cat / head / tail | Public cached read API for files, symbols, outlines, and archives |
| `ctx_search(mode="regex"|"semantic", ...)` | Grep / rg | Compact regex and semantic search results |
| `ctx_tree(path, depth)` | ls / find | Compact directory maps with file counts |
| `ctx(domain="memory"|"context"|"graph"|"analytics"|"agents"|"inspect", action="...")` | private `ctx_*` implementation details | Stable public gateway for advanced operations |

## Public Contract

- `ctx_read` targets: `file`, `files`, `symbol`, `outline`, `archive`
- `ctx_search` modes: `regex`, `semantic`
- `ctx` domains: `memory`, `context`, `graph`, `analytics`, `agents`, `inspect`
- Use native Bash/Shell directly; the nebu-ctx shell hook compresses output automatically. If shell output ever misbehaves, retry once, then use supported raw mode or the repo-built nebu-ctx client and file/update an issue instead of falling back to a public shell wrapper tool.

## File Editing

Use native Edit/StrReplace/Write/Delete tools normally. Public guidance should not recommend private nebu-ctx mutation helpers.

Use `ctx(domain="memory", action="save"|"recall"|"store"|"consolidate")` for persisted memory and `ctx(domain="context", action="overview"|"compress")` for context operations.

## Memory Policy

- Use `ctx(domain="memory", action="save"|"recall")` for task state and working memory.
- Use `ctx(domain="memory", action="store"|"recall"|"wakeup"|"consolidate")` for durable project facts.
- Let the stop/compact hooks consolidate session context into the nebu-ctx server instead of relying on chat history.
- If a public nebu-ctx tool fails reproducibly, retry once if it may be environmental. If it still fails, do not bypass to the native equivalent. Use supported raw mode or the repo-built nebu-ctx client, then create a GitHub issue in `MarkBovee/nebu-ctx` with repro, expected vs actual, shell/platform, and the failing tool call. Prefer `gh issue create --repo MarkBovee/nebu-ctx ...`; fall back to `nebu-ctx report-issue` if needed.
