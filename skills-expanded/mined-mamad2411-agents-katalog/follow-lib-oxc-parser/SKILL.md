---
name: follow-lib-oxc-parser
description: "Use oxc-parser to parse JS/TS into AST — very fast — analysis, tooling, review CLI"
argument-hint: "[files-or-goal]"
related:
  - use-astgrep
  - follow-lang-typescript
  - use-scripts
  - follow-best-practice
---

## Goal

Use `oxc-parser` (the NAPI binding of Oxc — a Rust-based JS/TS parser) to parse source code into an ESTree-compatible AST very fast, for analysis, tooling, and review automation work

## Scope

Use when analyzing JS/TS/JSX/TSX/dts programmatically with AST access, e.g.:

- Extract imports/exports/symbols from many files
- Build specialized analyzers/linters (e.g. a review CLI)
- Find call sites, unused exports, dependency graphs
- Walk the AST with a visitor pattern

Choose `oxc-parser` when you need the full AST + types; choose `/use-astgrep-programmatic` when you want pattern matching with declarative rules; follow `/follow-best-practice` and see `/follow-lang-typescript` or `/use-scripts` per context

- No CLI — used via programmatic API only (thus none); the ecosystem CLI is `oxlint`, a separate package
- Latest: `oxc-parser@0.151.0` (verified 2026-09-24)
- References: [apis](references/apis.md) 
## Execute

### 1. Install

> Goal: install a stable version

1. `bun add -d oxc-parser` — pin a version published at least 7 days ago
2. If you need AST types, add `bun add -d @oxc-project/types`

### 2. Parse Source

> Goal: get a usable ParseResult

1. Use `parseSync(filename, sourceText, options?)` as the default — Oxc recommends sync because AST deserialization happens on the main thread anyway (async `parse` is slower in many cases)
2. Use `parse()` only when genuinely I/O-bound
3. Set `filename` to match the extension — the parser picks the dialect from `.ts`, `.tsx`, `.jsx`, `.mts`, `.cts`, `.d.ts` automatically
4. Read `result.program` (ESTree AST), `result.comments`, `result.errors`, `result.module` (imports/exports/import.meta)

```ts
import { parseSync } from 'oxc-parser';

const result = parseSync('file.tsx', sourceText);
if (result.errors.length) console.warn(result.errors);
const program = result.program; // ESTree Program
```

### 3. Traverse AST

> Goal: walk the AST with a Visitor

1. Use `new Visitor({ NodeType(node) {}, "NodeType:exit"(node) {} })` then `visitor.visit(result.program)`
2. Node types follow the ESTree spec (`VariableDeclaration`, `CallExpression`, `ImportDeclaration`, etc.)
3. If you need a manual walk → recurse through `program.body`

```ts
import { Visitor } from 'oxc-parser';

const visitor = new Visitor({
  ImportDeclaration(node) {
    console.log('import from', node.source.value);
  },
});
visitor.visit(result.program);
```

### 4. Parallel Parsing

> Goal: parse many files concurrently

1. Don't use `parse()` to "parallelize" — thread-spawn overhead outweighs the benefit
2. Use worker threads (`node:worker_threads` or Bun workers) + `parseSync` inside the worker
3. Or parse sequentially — Oxc is fast enough for thousands of files

### 5. Print / Transform (if needed)

> Goal: turn the AST back into code, or transform it

1. Print AST → code: use `esrap` (`import ts from 'esrap/languages/ts'`)
2. Transform (TS→JS, JSX): use `oxc-transform`, a separate package
3. Minify: `oxc-minify`; resolve: `oxc-resolver`

## Rules

### 1. Error Handling

- Always check `result.errors` — the parser is error-tolerant and does not throw
- Set `options.showSemanticErrors` when you need checks deeper than syntax

### 2. Commonly Used Options

- `sourceType: 'module' | 'script' | 'unambiguous'` — default `unambiguous`
- `lang: 'js' | 'jsx' | 'ts' | 'tsx' | 'dts'` — override when the filename doesn't match reality
- `preserveParens`, `allowReturnOutsideFunction` per use case

### 3. When To Use What

- `oxc-parser` → full AST, type info, traversal, module analysis
- `/use-astgrep-programmatic` → pattern rules (`kind`, `pattern`, `has`, `inside`) for lint-style checks
- `oxc-transform` → compile/transpile
- Tree-sitter/Babel → only when you need an API compatible with the existing ecosystem

### 4. Bun Compatibility

- `oxc-parser` uses NAPI `.node` binaries — test on Bun before production; if issues arise, fall back to `bun x tsx` or the Node runtime

- Use `/use-astgrep` if you want declarative pattern matching
- Use `/follow-lang-typescript` if needed
- Use `/use-scripts` if processing many files
- Use `/follow-best-practice` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Parse JS/TS into a correct and fast AST (faster than Babel ~3x, SWC ~2x)
- Walk the AST via Visitor or a manual walk
- Handle parse errors and pick the right dialect from the filename
