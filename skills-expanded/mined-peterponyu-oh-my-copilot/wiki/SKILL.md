---
name: wiki
description: "[OMCP] LLM Wiki — persistent markdown knowledge base that compounds across sessions (Karpathy model)"
triggers: ["wiki", "wiki this", "wiki add", "wiki lint", "wiki query"]
---

# Wiki

Persistent, self-maintained markdown knowledge base for project and session knowledge. Inspired by Karpathy's LLM Wiki concept.

## Operations

All tool calls below match the schemas registered in `mcp-server/server.mjs` and use the `mcp__omcp__` prefix at runtime. The literal MCP invocation form is shown.

### Add
Create or overwrite a wiki entry. Slug is auto-derived from title if not given.

```
mcp__omcp__wiki_add({ title: "Auth Architecture", body: "# ...", tags: ["auth", "architecture"] })
```

### Read
Read an entry by slug. Returns `{exists, slug, title, tags, body, mtime}`.

```
mcp__omcp__wiki_read({ slug: "auth-architecture" })
```

### Query
Substring search across title, tags, and body. Returns top-K matches scored by hit count (title=3pts, tag=2pts, body=N hits capped at 10). Default `k=5`. YOU (the LLM) synthesize answers with citations from the results.

```
mcp__omcp__wiki_query({ q: "authentication", k: 5 })
```

### List
List all entries, optionally filtered by tag. Returns `{entries: [{slug, title, tags, mtime}, ...]}`.

```
mcp__omcp__wiki_list()                          // all entries
mcp__omcp__wiki_list({ tag: "architecture" })   // filter by tag
```

### Delete
Remove an entry by slug (file + index entry).

```
mcp__omcp__wiki_delete({ slug: "outdated-page" })
```

### Ingest
Import an external markdown file as a wiki entry. Title taken from first H1 line, falling back to source path.

```
mcp__omcp__wiki_ingest({ path: "docs/auth-notes.md", tags: ["auth"] })
```

### Lint
Integrity check. Returns `{orphans, untracked}` — index entries missing files, and files missing from index.

```
mcp__omcp__wiki_lint()
```

### Log
Wiki operations append to `.omcp/wiki/log.md` for monthly review (no automated reader).

## Categorization
omcp's wiki has no `category` field; use **tags** to express category-like dimensions. Suggested tag taxonomy: `architecture`, `decision`, `pattern`, `debugging`, `environment`, `session-log`.

## Storage
- Pages: `.omcp/wiki/*.md` (markdown with YAML frontmatter)
- Index: `.omcp/wiki/index.md` (auto-maintained catalog)
- Log: `.omcp/wiki/log.md` (append-only operation chronicle)

## Cross-References
Use `[[page-name]]` wiki-link syntax to create cross-references between pages.

## Auto-Capture
At session end, significant discoveries are automatically captured as session-log pages. Configure via `wiki.autoCapture` in `.omcp/omcp.jsonc` (default: enabled).

## Hard Constraints
- NO vector embeddings — query uses keyword + tag matching only
- Wiki pages are git-ignored by default (`.omcp/wiki/` is project-local)
