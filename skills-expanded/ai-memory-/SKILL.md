# Cursor Rules — ai-memory

## AI-Memory Loop

Use `memory.*` MCP tools as a persistent memory loop when available.

**Namespace for all operations in this repo:**
```json
{ "repo_url": "https://github.com/matt-antone/ai-memory" }
```
Do not pass `agent` or `repo_name` — set automatically. Global items (no `repo_url`) are always included in repo-scoped searches.

**Task start:** Call `memory.search` with a relevant query before starting work. If no hits, follow with `memory.list_recent` in the same namespace.

**During work:** Persist with `memory.write`:
- Decisions and their rationale
- Gotchas hit during development
- Deployment warnings
- Anything NOT already derivable from reading the code or docs

**Do NOT write:**
- Reference docs, architecture summaries, or anything already in the codebase
- Do NOT use `memory.ingest_document` for repo files (CLAUDE.md, README, etc.) — these inflate token costs and lose to grep on code questions
- Use `memory.ingest_document` only for external content with no home in the repo (postmortems, meeting notes, external specs)

**Task end:** Write a concise outcome summary. Link related items with `memory.link`.

**kind values:** `fact`, `summary`, `memory`, `document`, `chunk` — do not guess other values.

**If `memory.*` tools are unavailable:** say so briefly and continue. **Fallback:** use the `ai-memory` CLI from the integrated terminal when installed (`ai-memory self-install` puts it on PATH). Cursor’s managed install uses **stdio** (`ai-memory mcp`); if the MCP panel shows errors, run `ai-memory doctor` and ensure `.env` includes `MEMORY_MCP_ACCESS_KEY`, `SUPABASE_URL`, and `SUPABASE_SERVICE_ROLE_KEY`.
