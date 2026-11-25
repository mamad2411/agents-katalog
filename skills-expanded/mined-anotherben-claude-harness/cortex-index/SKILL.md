---
name: cortex-index
description: Index or reindex the current project with cortex-engine. Use when the user says "index this repo", "reindex", "cortex index", or invokes /cortex-index. Also use when cortex queries return empty or stale results.
---

# Cortex Index

Trigger a cortex-engine index of the current project.

## Steps

1. Call `mcp__cortex-engine__cortex_status()` to check current index state.

2. If the index has files, report the current state and ask if the user wants a full reindex. If the index is empty or the user requested a fresh index, proceed.

3. Call `mcp__cortex-engine__cortex_reindex()` to trigger a full reindex.

4. Call `mcp__cortex-engine__cortex_status()` again and report the result:

```
Cortex index complete: X files, Y symbols indexed.
```

## Arguments

- No args: index/reindex current project
- File path arg (e.g., `/cortex-index src/services/`): reindex just that path via `mcp__cortex-engine__cortex_reindex(file_path="<path>")`
