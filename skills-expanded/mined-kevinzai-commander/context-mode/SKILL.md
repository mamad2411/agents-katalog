---
name: context-mode
description: Tool output sandboxing — 98% context reduction via FTS5
type: optimization
auto-load: false
---

# context-mode

Intercepts tool results (Read, Grep, WebFetch, Bash) and stores them in SQLite with FTS5 full-text search. Instead of dumping full output into context, returns only BM25-ranked relevant snippets.

## License & Attribution

context-mode is by [Murat Kemal Soylu](https://github.com/mksglu), licensed under **Elastic License 2.0 (ELv2)**. CC Commander installs it as an external npm package — we do not bundle, modify, or redistribute its source code. See the [context-mode repo](https://github.com/mksglu/context-mode) for full license terms.

## When to Use
- File-heavy exploration (reading many files)
- Large grep/search results
- Web fetches returning large pages
- Any task where tool output exceeds what's needed

## Tools Available
- `ctx_execute` — run command, result stored in sandbox
- `ctx_batch_execute` — run multiple commands, all indexed
- `ctx_search` — BM25 search over sandboxed results
- `ctx_fetch_and_index` — fetch URL and index content
- `ctx_execute_file` — execute a file, index output
- `ctx_index` — manually index content

## Installation

```bash
npm install -g context-mode
```

Then add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "context-mode": {
      "type": "stdio",
      "command": "context-mode"
    }
  }
}
```

## Verify
The MCP tools should appear in your Claude Code session. Run `ctx_execute` with a simple command to verify sandboxing works.

## Relationship to Other Tools
- **RTK**: Filters CLI output BEFORE context (input side)
- **context-mode**: Filters tool results AFTER execution (output side)
- **Headroom**: Optimizes at API proxy layer (request/response)
- **ClaudeSwap**: Account rotation for rate limits
- These are complementary layers, not competing.

## Token Optimization Stack
| Layer | Tool | Savings |
|-------|------|---------|
| CLI filtering | RTK | 99.5% of shell output |
| Tool sandboxing | context-mode | 98% of tool results |
| API proxy | Headroom | Cache alignment + compression |
| Account rotation | ClaudeSwap | 2 MAX accounts |
| Server cache | Prompt caching + extended TTL | 90% discount, 1hr TTL |
