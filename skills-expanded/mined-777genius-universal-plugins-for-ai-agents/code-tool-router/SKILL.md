---
name: code-tool-router
description: Choose the right code intelligence tool before searching, navigating, refactoring, or analyzing a codebase.
execution_mode: docs_only
supported_agents:
  - codex
  - claude
---

# Code Tool Router

## What it does

Routes code work across the right tool:

| Intent | First tool | Verification |
| --- | --- | --- |
| Exact string, config key, env var, error text, symbol spelling | `rg` | Open matching files directly |
| Broad semantic discovery, "where is X implemented?", similar code | Semble | `rg` for exact terms, then file reads |
| Definition, references, rename, signature change, type-aware navigation | Serena | `rg` for generated/dynamic callsites |
| Callers, callees, complexity, dependency graph, architecture report | CGC | Serena or `rg` before edits |
| Project decisions, product facts, user preferences, long-term notes | Existing project memory, when available | Source documents or current code |
| Current library/API usage | Context7 or official docs | Local code examples |

## When to use

Use this skill when a task requires finding code, understanding ownership, tracing behavior, planning a refactor, or comparing implementation patterns. The authored skill contract names Codex and Claude, and plugin targets mirror the same guidance into Cursor, Gemini, and OpenCode outputs.

## How to run

Classify the question before searching, then use the cheapest reliable tool first.

Exact search:

```bash
rg -n "INTERVIEW_MEMORY_MODE" .
rg -n "reset_session\\(" .
rg --files | rg "memory|context"
```

Semantic discovery:

```bash
uvx --from semble==0.2.0 semble search "where interview memory context is assembled" .
uvx --from semble==0.2.0 semble search -k 10 "copy helper browser focus integration" .
uvx --from semble==0.2.0 semble find-related src/path/file.ts 42 .
```

Graph and architecture:

```bash
cgc stats . --context "$(basename "$PWD")"
cgc find name reset_session --context "$(basename "$PWD")"
cgc analyze callers reset_session --context "$(basename "$PWD")"
cgc analyze calls assemble_stream_context_or_fallback --context "$(basename "$PWD")"
cgc analyze complexity --limit 20 --context "$(basename "$PWD")"
cgc report --output /tmp/CGC_REPORT.md --context "$(basename "$PWD")"
```

For Serena, use LSP-backed definitions, references, symbols, diagnostics, rename, and signature tools. If Serena exposes an initial-instructions tool, read it before using Serena in a new session.

## If optional tools are missing

Do not block the task just because a specialized tool is unavailable.

- If `rg` is missing, use the fastest available local text search and mention the fallback.
- If Semble is missing, use `rg` to build a shortlist, then read the most relevant files directly.
- If Serena is missing, use `rg` for definitions/references and avoid automated rename/refactor claims.
- If CGC is missing or not indexed, use `rg --files`, source reads, and language tooling where available.
- If project memory is missing, rely on source documents and current conversation context. Do not invent remembered facts.
- If tool availability is unclear, run the read-only `code-intelligence-doctor` skill when available.

## Constraints

- Use `rg` first for exact text. It is still the fastest and most trustworthy tool for literals.
- Use Semble as a high-quality shortlist, not as complete impact analysis.
- Use Serena for type-aware navigation and safe symbol edits.
- Use CGC for graph questions, but confirm before changing behavior.
- For HackInterview, keep CGC in tree-sitter mode by default. Previous local benchmarking showed SCIP mode missed important TypeScript/Rust caller and callee relationships.
- Use memory for durable facts and decisions. Do not use it as a code index. If memory conflicts with source code, source code wins.
