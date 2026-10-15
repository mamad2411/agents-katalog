---
name: using-codegraph
description: CodeGraph-first code exploration. Use when working in a repository that may be indexed by CodeGraph and you need to understand, locate, trace, or read code before using grep/find/rg or opening files. Check for a .codegraph directory at the repository root, use the codegraph_explore MCP tool when available or the codegraph explore shell command, and skip CodeGraph when no .codegraph directory exists.
---

# Using CodeGraph

Use CodeGraph as the first code lookup path in indexed repositories. It returns relevant source, symbols, and call paths in one query, including relationships that text search can miss.

## Workflow

1. Find the repository root and check for `.codegraph/`.
   Completion criterion: you know whether the current repository is indexed.

2. If `.codegraph/` is missing, skip CodeGraph.
   Completion criterion: continue with normal exploration tools. Do not create, update, or request a CodeGraph index unless the user explicitly asks.

3. If `.codegraph/` exists and the task requires understanding or locating code, query CodeGraph before grep, find, `rg`, or opening files.
   Completion criterion: CodeGraph has returned relevant symbols, source, call paths, or a concrete miss.

4. Prefer the MCP tool when available.
   Completion criterion: use `codegraph_explore` for the query. If the tool is listed but deferred, load it by name through tool discovery before falling back.

5. Fall back to the shell command when the MCP tool is unavailable.
   Completion criterion: run `codegraph explore "<symbol names or question>"` from the indexed repository and inspect the output.

6. Use narrow file reads or text search only after the CodeGraph pass.
   Completion criterion: follow up on specific files, symbols, or gaps found by CodeGraph, or proceed normally after a CodeGraph miss.

## Query Shape

- Name known files, symbols, functions, classes, or APIs directly.
- Ask behavior questions when the symbol name is unknown, such as where a request is authenticated or how a value flows to storage.
- If CodeGraph reports deferred symbols or files, load the exact names it gives before broadening the search.

## Boundaries

- Do not run indexing as part of this skill. Indexing is the user's decision.
- Do not use CodeGraph in repositories without `.codegraph/`.
- Do not treat CodeGraph output as the final answer when the task requires an edit; verify the target files before patching.
