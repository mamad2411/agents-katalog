---
name: context-scoper
description: Use this before reading whole files to answer any "where is X handled", "how does Y work", "which file defines Z", "what calls this function", "who uses this", or "is it safe to change this" question about the current {{PROJECT}} project — and before making a change to code you haven't already read in this conversation. Calls the search_codebase MCP tool (deterministic, no LLM, no network) to find the exact symbol, method, or file first, instead of grepping blind or opening whole files to hunt for the right spot. It resolves class methods, interface members, and object-literal methods, not just top-level declarations. Also use before renaming, removing, or changing the signature of an existing function, class, or export, to see what else references it first. Read the backend field on every result — "typescript" means the type checker resolved it and each reference names the declaration it belongs to; "tree-sitter" means it is a name match that cannot separate two same-named symbols in different scopes.
---

# Context Scoper

Reading whole files to find one function, or grepping for a name and hoping the matches are the real ones, both cost tokens and cost accuracy — a grep match inside a comment, a string, or a same-named variable in an unrelated scope looks identical to a real hit until you've read enough surrounding code to tell the difference. This skill exists so that step happens once, cheaply, via `search_codebase` instead of being repeated by hand on every request.

## What to do

1. **Before opening a file to find where something is implemented**, call the `search_codebase` MCP tool (served by `@vovy-ai/mcp-server`, already registered if Vovy is installed) instead of guessing a filename or grepping across the repo:
   - `action: "find_symbol"` with the name you're looking for — returns every declaration site (file, line, kind: function/class/interface/type/variable) across the project.
   - `action: "overview"` with a specific `filePath` — returns just that file's top-level functions/classes/exports with line ranges, when you already know the file but not where in it.
   - `action: "find_references"` with a name — returns identifier-boundary-aware usage sites across the project. Use this **before** renaming, removing, or changing the signature of anything that already exists, so you know what else depends on it before you touch it.
   - `action: "pattern"` — a plain regex/text search fallback for prose, config, or any file type the tree-sitter layer doesn't parse (it only understands `.js/.jsx/.mjs/.cjs/.ts/.mts/.cts/.tsx`).
2. **Read only the file(s) and line range(s) the search actually returned**, not the whole file, unless you need the surrounding context to understand how a symbol is used — this is the actual token saving, not a side effect.
3. **If `search_codebase` isn't available** (Vovy's MCP server isn't registered in this host), fall back to the tools you'd normally use — Grep/Glob/reading files directly — rather than blocking on it.

## What this doesn't claim

`search_codebase` is identifier-boundary-aware (it matches real tokens tree-sitter parsed, never a substring inside a string or comment) — that's a real, meaningful improvement over grep. It is **not** scope- or type-aware like a real language server: two unrelated symbols that happen to share a name in different scopes will both show up in `find_symbol`/`find_references` results. Use judgment on which result is the real one the same way you would with any search tool — don't treat every hit as guaranteed-correct just because it came from a structured tool instead of grep.

## Why this matters

This is the concrete "better tool-calling via semantic search" half of Vovy's cost story: fewer, more targeted file reads mean fewer tokens spent per request and a lower chance of editing the wrong same-named thing. Nothing here is a hosted service or a model call — `search_codebase` resolves symbols deterministically through the project's own TypeScript or a bundled tree-sitter parser, same free-forever ethos as `analyze_project`.
