---
name: tree-sitter-recipes
description: Answer structural code questions - what a file defines, imports, exports, its function signatures, types, or syntax errors - with shipped Tree-sitter query recipes instead of reading whole files. Use when asked about code structure in TypeScript, JavaScript, or Python.
---

# Tree-sitter Recipes

Resolve the recipe paths below against this skill's directory.

## Workflow

1. Confirm parser availability with `tree_sitter_languages` (add `useManagedConfig=true` if grammars were installed with `tree_sitter_grammar_install`). If a grammar is missing, suggest `npm install -g tree-sitter-<language>` or the managed install path.
2. Pick the recipe matching the question and run `tree_sitter_query` with `captures=true, compact=true` on the narrowest path scope: one file or directory before the repo root.
3. Use `tree_sitter_tags` instead when the goal is definitions/references navigation; use `tree_sitter_parse` with `mode="json-summary"` for parse health.
4. If a recipe misses a construct, inspect the tree with `tree_sitter_parse` and adapt - see the `tree-sitter-query-authoring` skill for writing new queries.
5. Summarize captures for the user; compact output is one-based `file:line:column`.

Example:

```text
tree_sitter_query(
  queryFile="<this skill directory>/../../queries/typescript/function-signatures.scm",
  paths=["src/index.ts"],
  captures=true,
  compact=true
)
```

## Shipped query recipes

| Task | Query file | Notes |
| --- | --- | --- |
| Syntax errors | `../../queries/universal/syntax-errors.scm` | Captures `@syntax.error` and `@syntax.missing`; works across most grammars. |
| TypeScript signatures | `../../queries/typescript/function-signatures.scm` | Captures `@signature.name`, `@signature.params`, `@signature.return`, including arrow functions, function expressions, and class arrow fields. |
| TypeScript imports | `../../queries/typescript/imports.scm` | Captures `@import.statement`, `@import.source`, `@import.default`, `@import.namespace`, `@import.name`, `@import.alias`. |
| TypeScript exports | `../../queries/typescript/exports.scm` | Captures `@export.function`, `@export.class` (incl. abstract), `@export.interface`, `@export.type`, `@export.enum`, `@export.value`, `@export.name`, `@export.alias`, `@export.source`, `@export.namespace`, `@export.default`. |
| TypeScript type declarations | `../../queries/typescript/type-declarations.scm` | Captures `@type.class` (incl. abstract), `@type.interface`, `@type.alias`, `@type.enum`. |
| pi tool registrations | `../../queries/typescript/tool-registrations.scm` | Finds `pi.registerTool({ name: ... })` calls; captures `@tool.name`, `@tool.name_key`, `@tool.registry_object`, `@tool.registry_method`. |
| JavaScript signatures | `../../queries/javascript/function-signatures.scm` | Captures `@signature.name`, `@signature.params`, including arrow functions, function expressions, and class arrow fields. |
| JavaScript imports | `../../queries/javascript/imports.scm` | Captures `@import.statement`, `@import.source`, `@import.default`, `@import.namespace`, `@import.name`, `@import.alias`. |
| JavaScript exports | `../../queries/javascript/exports.scm` | Captures `@export.function`, `@export.class`, `@export.value`, `@export.name`, `@export.alias`, `@export.source`, `@export.namespace`, `@export.default`. |
| Python signatures | `../../queries/python/function-signatures.scm` | Captures `@signature.name`, `@signature.params`, `@signature.return`. |
| Python imports | `../../queries/python/imports.scm` | Captures `@import.source`, `@import.name`, `@import.alias`, `@import.star`. |
| Python exports | `../../queries/python/exports.scm` | Captures `@export.name` (`__all__` entries), `@export.list`, `@export.function`, `@export.class`, `@export.value`. |
| Python type declarations | `../../queries/python/type-declarations.scm` | Captures `@type.class` and `@type.alias` (PEP 695). |

Shared capture names (`@signature.*`, `@import.*`, `@export.*`, `@type.*`) are stable across languages so output can be summarized uniformly.

## Project recipes

For repeated project-specific patterns, prefer `.scm` files over wrapper tools: `.pi/tree-sitter/queries/<language>/<task>.scm` (pi-specific) or `tree-sitter/queries/<language>/<task>.scm` (tool-agnostic). See the `tree-sitter-query-authoring` skill.
