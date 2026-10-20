---
name: follow-lib-gritql
description: Use GritQL in Biome for code search, transformation, and custom linting
argument-hint: "[scope]"
related:
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd
  - run-scan
  - follow-tool-biome
  - use-astgrep
---

## Goal

Use GritQL together with Biome for structural code search, code transformation, and custom lint rules

## Scope

For JavaScript/TypeScript, CSS, and JSON in projects using Biome v2+ — this skill covers GritQL patterns within Biome only (`biome search`, `.grit` lint plugins)

- If the task is general Biome setup/config/lint (not GritQL) → use `/follow-tool-biome`
- For structural search/rewrite outside Biome, or cross-language codemods that GritQL-in-Biome doesn't support → consider `/use-astgrep` (ast-grep)

- Latest: `@biomejs/biome@2.5.14` (GritQL engine) (verified 2026-09-26)
- References: [apis](references/apis.md) 
## Execute

### 1. Understand GritQL Basics

> Goal: understand the GritQL pattern syntax basics

1. Read the GritQL documentation at `https://biomejs.dev/reference/gritql/`
2. Learn the pattern syntax with code snippets in backticks
3. Learn variables with the `$variable` syntax
4. Learn conditions with `where` and operators

### 2. Set Up Language Target

> Goal: specify the target language and engine for patterns

1. Specify the target language with `language js`, `language css`, or `language json`
2. Use flavors such as `typescript`, `jsx` for JavaScript via `language js(typescript,jsx)`
3. Use `engine biome(1.0)` when you want to match Biome syntax nodes such as `JsIfStatement`
4. Check each language's integration status before use

### 3. Write Basic Patterns

> Goal: write code snippet patterns correctly

1. Write code snippet patterns in backticks, e.g. `` `console.log($message)` ``
2. Use variables for flexible matching, e.g. `$method`, `$message`
3. Use spread metavariables `$$$args` to match arguments
4. Use the same variable multiple times for consistency matching
5. Use `as $name` to capture a node span for diagnostics or rewrites

### 4. Add Conditions And Filters

> Goal: add conditions and filters with the `where` clause

1. Use the `where` clause for conditions
2. Use the pattern matching operator `<:` for pattern comparison
3. Use `or` for multiple pattern options
4. Use built-in functions such as `register_diagnostic()` for complex logic

### 5. Create GritQL Analyzer Plugin

> Goal: create a GritQL plugin for the Biome linter

1. Create a `.grit` file for the plugin, e.g. `.grit/no-console-log.grit`
2. Use `register_diagnostic()` for custom lint rules, specifying `span`, `message`, and `severity`
3. Use `fix_kind` (`safe` or `unsafe`) when there is a rewrite with `=>`
4. Register the plugin in `biome.jsonc` or `biome.json` under the `plugins` key

### 6. Use Biome Search Command

> Goal: use `biome search` for structural code search

1. Use `biome search '<pattern>' [path]`, wrapping the pattern in single quotes
2. Use `--language=<lang>` such as `javascript`, `css`, `json` for the target language
3. Specify a path or glob patterns to scope the search
4. Remember `biome search` supports search patterns only, not rewrites

### 7. Apply Rewrites (Optional)

> Goal: modify code with the rewrite operator in plugins

1. Use the rewrite operator `=>` to transform matched code — rewrites in a plugin become fixable diagnostics for JS, CSS, and JSON
2. Set `fix_kind` in `register_diagnostic()` to declare fix safety — the default is `unsafe`
3. Run `biome check --write` or `biome lint --write` to apply safe fixes only — unsafe fixes need the `--unsafe` flag (`biome check --write --unsafe`)
4. Avoid unsafe rewrites if they could change code logic

### 8. Optimize Performance

> Goal: improve pattern performance

1. Use specific node types or snippets instead of full-tree walks
2. Avoid overly broad patterns
3. Use anchors and node matchers appropriately
4. Verify performance by benchmarking on the real codebase

## Rules

### 1. Pattern Syntax

- Use backticks for code snippets: `` `console.log($message)` ``
- Use `$variable` for metavariables
- Use `$$$args` for spread metavariables
- Use the `where` clause for conditions
- Use the `<:` operator for pattern matching

### 2. Language And Engine Support

- `language js` for JavaScript, supporting `typescript` and `jsx` flavors
- `language css` for CSS
- `language json` for JSON
- `engine biome(1.0)` to match Biome AST nodes such as `JsIfStatement`
- Check the integration status before use

### 3. Variable Usage

- Use the same variable name many times for consistency matching
- Use spread metavariables for flexible argument matching
- Use pattern matching in the `where` clause
- Avoid overly generic variables

### 4. Condition Logic

- Use the `where` clause for filtering
- Use the `<:` operator for pattern comparison
- Use `or` for multiple options
- Use built-in functions for complex logic

### 5. Plugin Integration

- Use `register_diagnostic()` for custom rules, specifying `span`, `message`, `severity`
- Set `fix_kind` to `safe` or `unsafe` when using rewrites
- Register the plugin in the Biome configuration
- Verify plugin compatibility with the Biome version

### 6. Search Usage

- Use single quotes around patterns: `biome search '`console.log($message)`' ./src`
- Use `--language=<lang>` for the target language
- Avoid shell conflicts by wrapping the pattern in single quotes
- Never use rewrites (`=>`) with `biome search`

### 7. Rewrite And Fix Safety

- Use the `=>` operator for transformation in GritQL plugins only
- Set `fix_kind` appropriately — the default is `unsafe` and requires `biome check --write --unsafe`
- Run `biome check --write` for safe fixes
- Test rewrites on sample files before applying in production

### 8. Performance Best Practices

- Use specific node types instead of full-tree walks
- Avoid overly broad patterns
- Use anchors for efficient matching
- Verify performance with benchmarking

- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed
- Use `/run-scan` if needed
- Use `/follow-tool-biome` if needed
- Use `/use-astgrep` if needed
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- GritQL patterns written correctly
- Custom Biome lint rules created with GritQL
- `biome search` used for structural code search
- Understanding of the difference between GritQL and `ast-grep`
