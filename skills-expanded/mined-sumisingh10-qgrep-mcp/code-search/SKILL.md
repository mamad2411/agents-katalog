---
name: code-search
description: This skill should be used when the user asks to "search code", "find in files", "grep for", "look for pattern", "search the codebase", "find references to", "find usages of", "search for function", "find where X is defined", or needs to search file contents across a directory tree. Provides guidance on using the search_code MCP tool for fast indexed code search.
version: 0.1.0
---

# Indexed Code Search

This skill provides fast indexed code search via the `search_code` MCP tool, which is up to 300x faster than standard grep on large codebases.

## When to Use search_code

Prefer the `search_code` MCP tool over the built-in Grep tool when searching file contents across a directory tree. The `search_code` tool automatically selects the fastest backend:

- On large repos (15k+ files), it builds and uses a qgrep index. Searches complete in ~10ms instead of ~3-25s
- On small repos (< 5k files), it transparently falls back to ripgrep
- In the gray zone (5k-15k files), it measures ripgrep latency and indexes if beneficial

## Available MCP Tools

### search_code

Primary search tool. Supports regex patterns, glob filters, case-insensitive search, and context lines.

```
search_code(pattern="impl Iterator for", path="/path/to/repo")
search_code(pattern="TODO|FIXME", path="/path/to/repo", case_insensitive=True)
search_code(pattern="class.*Handler", path="/path/to/repo", glob="*.py")
search_code(pattern="fn main", path="/path/to/repo", output_mode="files_with_matches")
```

Parameters:
- `pattern` (required): Regex pattern to search for
- `path` (required): Absolute directory path to search in
- `glob`: Filter files (e.g. `"*.py"`, `"*.{ts,tsx}"`)
- `case_insensitive`: Case-insensitive search (default: false)
- `output_mode`: `"content"` (default), `"files_with_matches"`, or `"count"`
- `context_lines`: Lines of context around matches
- `max_results`: Maximum result lines (default: 200)

### build_search_index

Manage the search index lifecycle. Build an index before searching to get maximum speed.

```
build_search_index(action="build", path="/path/to/repo")
build_search_index(action="status", path="/path/to/repo")
build_search_index(action="rebuild", path="/path/to/repo")
build_search_index(action="delete", path="/path/to/repo")
```

### search_estimate

Analyze a directory and get an indexing recommendation with stats.

```
search_estimate(path="/path/to/repo")
```

Returns file count, current search latency stats, and whether building an index is worthwhile.

## Performance Characteristics

Based on benchmarks against rust-lang/rust (58,534 files):

| Backend | Avg latency | When used |
|---------|-------------|-----------|
| qgrep (indexed) | ~12ms | Index exists or auto-built for large repos |
| ripgrep (fallback) | ~2.9s | Small repos, glob filters, context lines |

Index build is a one-time cost (~7s for 58k files) that pays for itself after ~3 searches.

## Automatic Behavior

The `search_code` tool handles backend selection automatically:

1. If an index exists for the target path, use qgrep
2. If the repo has 15k+ files and no index, build one automatically
3. For glob filters or context lines, use ripgrep (qgrep limitation)
4. For small repos, use ripgrep directly (fast enough)

No manual index management is needed for typical usage. Just call `search_code` and it handles the rest.
