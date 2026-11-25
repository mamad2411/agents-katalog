---
name: structural-explore
description: "Token-saving code exploration: map a codebase's structure (functions, classes, methods, types with line ranges) before reading anything, then read only the symbols that matter. Uses structural search tools when the session has them and the bundled outline script otherwise. Use when exploring an unfamiliar codebase, finding where something is defined or handled, or understanding a large file without reading all of it."
user-invocable: false
---

# Explore: map first, fetch on demand

The question before every file read: do I need all of this, or a structural overview first? Almost always, the overview. A symbol map of a file costs a fraction of the file, and reading one function costs a fraction of the map.

## Three layers

1. **Search**: find the files and symbols related to a topic across a tree.
2. **Outline**: see the skeleton of one file (every symbol with its line range) without the bodies.
3. **Unfold**: read the source of one symbol, and only that.

Stop at the first layer that answers the question.

## Pick the tool

Use the best one the session has:

1. **Structural search tools, if present.** Some MCP servers and plugins expose these three layers directly (a symbol search, a file outline, a symbol's source), usually built on tree-sitter. If tools like these are in your tool list, use them. A configured language server (the LSP tool) also answers "where is this defined" and "who calls this" precisely.
2. **Otherwise, the bundled outline script** (Python standard library only, no install):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/bin/outline.py <dir> --search "<words>" [--max 20]   # layer 1
   python3 ${CLAUDE_PLUGIN_ROOT}/bin/outline.py <file>                                # layer 2
   python3 ${CLAUDE_PLUGIN_ROOT}/bin/outline.py <file> --unfold <name|Class.method>   # layer 3
   python3 ${CLAUDE_PLUGIN_ROOT}/bin/outline.py <dir>                                 # symbol counts per file
   ```

   Python files are parsed with the `ast` module, so their symbols and line ranges are exact. JavaScript, TypeScript, Go, Rust, Java, Kotlin, C#, C, C++, Ruby, PHP, Swift, and shell use line patterns plus brace or `end` matching: reliable for a map, occasionally off for unusual formatting. When a range looks wrong, read that line range directly with the Read tool's offset and limit.

   The walk skips `.git`, `node_modules`, `dist`, `build`, `target`, `vendor`, virtualenvs, and other output folders, and files over 1 MB.

## When the standard tools fit better

- **Grep**: an exact string or regex ("every TODO", "where is `retryPolicy` used").
- **Read**: small files (under about 100 lines), and non-code files (JSON, YAML, markdown, config).
- **Glob**: file name patterns ("all test files").
- **An exploration subagent**: an open question that needs a narrative across many files ("how does a request flow end to end?"). Structural tools answer "where is this" and "show me that"; they do not synthesize a data flow.

For code files longer than about 100 lines, prefer outline plus unfold over reading the whole file.

## Workflows

**How does a feature work?**

```
outline.py src --search "shutdown"         -> ranked symbols across files
outline.py src/server.ts --unfold stop      -> the one method that matters
```

**Navigate a large file**

```
outline.py services/worker.py              -> the class and its 24 methods with line ranges
outline.py services/worker.py --unfold Worker.drain
```

**Write docs about code**

Search the feature, outline the key files, unfold the important functions, and read the small config or markdown files in full.

## Anti-patterns

- Reading a whole large file to find one function.
- Running Glob, then Grep, then Read in sequence when one structural search gives files and symbols together.
- Unfolding every symbol "to be thorough". Unfold what the question needs.
