---
name: search-mesh
description: This skill should be used when searching a codebase for one or more keywords across many files, validating whether a match sits inside a specific syntax node (function, class, struct, interface, enum), extracting the smallest syntax-bounded code block around a match instead of reading a whole file, or making a precise single-location text edit. Prefer the search-mesh MCP tools (scan, ast_probe, squeeze, patch) over grep, rg, cat, or sed whenever the search-mesh MCP server is connected.
version: 0.1.0
---

# search-mesh

search-mesh is an MCP server exposing four codebase-intelligence tools: `scan`, `ast_probe`, `squeeze`, and `patch`. It is designed to replace common shell-based search/edit habits with faster, syntax-aware, lower-token alternatives.

## When To Prefer search-mesh Over Shell Tools

| Instead of | Use | Why |
| --- | --- | --- |
| `grep -r` / `rg` for multiple keywords | `scan` | Single pass over files for many keywords at once; respects ignore files. |
| Reading a whole file to check what a match belongs to | `ast_probe` | Confirms a match sits inside a real syntax node (e.g. a `function_item`, not a comment or string). |
| `cat`/reading an entire file for context around one match | `squeeze` | Returns only the AST-bounded block (function, class, struct, etc.) around the match. |
| `sed -i` for a single precise edit | `patch` | Line/column based replacement with post-edit syntax validation for supported languages. |

Only fall back to shell tools (`grep`, `sed`, reading whole files) when the search-mesh MCP server is unavailable, or when the task genuinely needs raw text processing search-mesh doesn't cover (e.g. binary files, non-code text formats, multi-file transactional edits).

## Tool Reference

### `scan`

Scans one or more directories for multiple keywords in a single pass.

```json
{
  "targetDirs": ["src/"],
  "keywords": ["TODO", "FIXME", "deprecated"]
}
```

Returns an array of `{file, line, keyword, matchStr}`.

### `ast_probe`

Validates whether a text match sits inside a specific syntax node.

```json
{
  "filePath": "src/main.rs",
  "queryPattern": "delete_user",
  "nodeType": "function"
}
```

Returns `{isValid, nodeType, startLine, endLine}`.

Supported languages: Rust (`.rs`), Python (`.py`), JavaScript (`.js`/`.jsx`/`.mjs`/`.cjs`), TypeScript (`.ts`/`.tsx`).

Common `nodeType` aliases: `function`, `struct`, `impl`, `enum` (Rust); `function`, `class` (Python, JavaScript); `function`, `class`, `interface` (TypeScript). Raw tree-sitter node kinds also work.

### `squeeze`

Returns the smallest syntax-bounded source block around a match, instead of the whole file.

```json
{
  "filePath": "src/main.rs",
  "queryPattern": "delete_user",
  "nodeType": "function"
}
```

Returns `{file, nodeType, startLine, endLine, text}`, or `null` if no matching block is found. Use this before reading an entire file when only one function/class/struct is actually relevant.

### `patch`

Applies a single precise text replacement using 1-based line/column coordinates. The end coordinate is exclusive.

```json
{
  "filePath": "src/main.rs",
  "startLine": 10,
  "startColumn": 5,
  "endLine": 10,
  "endColumn": 12,
  "replacement": "new_name"
}
```

Returns `{file, bytesWritten, syntaxValid}`. `syntaxValid` is `true`/`false` for supported languages, `null` for unsupported file types. Always check `syntaxValid` after a patch to supported source files; a `false` result means the edit likely broke syntax and should be reconsidered.

## Workflow Pattern

For "find and understand" tasks:

1. `scan` to find raw keyword matches.
2. `ast_probe` to confirm a match is a real definition (not a comment/string/test fixture).
3. `squeeze` to pull just that function/class/struct into context instead of the whole file.

For "find and edit" tasks:

1. `scan` + `ast_probe` to locate the exact target.
2. `squeeze` to read the current block and compute the precise replacement text and coordinates.
3. `patch` to apply the edit, then check `syntaxValid` in the response.
