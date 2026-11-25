---
name: ai-context-workflow
description: >
  Use for code context, file locations, or an architecture overview on the
  ai-context repository before writing or modifying code. Drives
  repo_structure, semantic_search, get_file, analyze_impact, and (when
  configured) resolve_symbol against the project-specific
  {project_key}-context MCP server that matches the user's question.
mcp_server: any registered *-context MCP server (see workflow below)
tools: [repo_structure, semantic_search, get_file, analyze_impact, resolve_symbol]
---

# ai-context — Codebase Context Workflow

This skill covers every project indexed by ai-context in this repository.
Each project is served by a separate MCP server named `{project_key}-context`.

1. **Pick the project.** Choose the MCP server whose project best matches the
   user's question. Registered projects:

   | MCP server | Project | URL |
   |------------|---------|-----|
   | `ai-context-context` | AI Context | http://localhost:7111/mcp |
   If the question is repo-wide or you are unsure, start with the project that
   owns the file path or module mentioned in the question.

2. `repo_structure` — call first on the chosen project for orientation
   (module map, directory tree). Per-file entries may show
   `[hub]`/`[bridge]` structural-role tags (derived from the import/call
   graph) — hubs warrant extra care before changing.

3. `semantic_search(query)` — use technical identifiers, not prose
   (e.g. `UserRepository authenticate`, not "how do users log in").
   Read the returned summaries before requesting full files. Each hit
   includes a `why` note (identifier match, vector similarity, keyword
   boost, or rerank) — use it to judge trustworthiness, not just the score.

4. `get_file` — only if step 3 wasn't enough. Max 2 calls per query,
   max 3 files per call. Works for code and docs automatically.

5. `analyze_impact(symbol_name, direction, [file_path], [depth],
   [include_tests])` — before editing or removing a symbol, to see its
   callers/callees (blast radius) and which test files likely cover it.
   `direction` is `callers`, `callees`, or `both`. Pass `file_path` to
   disambiguate if the symbol name is not unique in the project.

6. `resolve_symbol(file_path, line, character, kind)` — only if the project
   has `lsp` enabled for that language (not every project/language has
   this). Use for compiler-grade precision (`kind=definition`,
   `references`, or `hover`) when the heuristic call graph from
   `analyze_impact` or the results from `semantic_search`/`get_file` leave
   the exact declaration or call sites ambiguous. Higher cost than steps 2
   to 5 — reach for it only when those are not enough, and skip it if the
   tool reports the language or project is not configured for it.

Some projects declare `sources` in ai-context config; if the answer likely
lives in a related module (e.g. a frontend asking about a backend API),
repeat the workflow against the source project.

Stop as soon as you have enough context — don't call every tool by default.
If `semantic_search` finds nothing after one rephrase, say so instead of
guessing.
