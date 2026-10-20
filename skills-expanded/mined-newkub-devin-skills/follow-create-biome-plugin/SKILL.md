---
name: follow-create-biome-plugin
description: Build custom Biome linter plugins with GritQL
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - follow-tool-biome
  - deep-review-codebase
  - follow-tool-formatter
  - ship
  - run-lint
  - run-format
---
## Goal

Build custom Biome linter plugins with GritQL to add project-specific rules

## Scope

Covers creating `.grit` plugin files, writing GritQL patterns, configuring `biome.jsonc`, and verifying plugins

- Packages: `@biomejs/biome` (2.x — config is `biome.jsonc`, adds GritQL plugin support + `engine biome(1.0)` directive), `@biomejs/js-api` — always confirm the latest version via `/deep-research` + `/follow-best-practice` (no pinning in the file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Check the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then `/deep-review-codebase` to summarize the tech stack
3. Record the stack and library choices for the next reference (create biome plugins)

### 2. Setup

> Goal: Check Biome and project prerequisites

1. Verify Biome is installed by running `/follow-tool-biome`
2. Verify a `biome.jsonc` already exists
3. Identify the target language and the rules to enforce

### 3. Create Plugin File

> Goal: Create and write the `.grit` plugin file

1. Create a `.grit` file at the project root
2. Add the `language` directive at the top of the file (e.g. `language css`, `language js`, `language json`)
3. Add the `engine biome(1.0)` directive when using Biome CST node names
4. Write GritQL patterns for the custom rules
5. Use `register_diagnostic()` to report diagnostics
6. Use an `or` block to combine multiple rules in one file
7. Syntax: backtick snippets = structural match (ignores whitespace/quote style); `$var` named, `$_` anonymous, `$...` spread metavariables; `where` conditions separated by comma; `<:` match operator (`$x <: or { \`a\`, \`b\` }`, `<: not \`null\``); modifiers `as`/`contains`/`within`/`after`/`before`/`some`/`every`; `r"..."` regex; `=>` rewrite (`fix_kind` marks safe/unsafe — `--write` applies safe only, `--write --unsafe` includes unsafe)

### 4. Configure Plugin

> Goal: Configure the plugin in `biome.jsonc`

1. Add the plugin path to the `plugins` array in `biome.jsonc`
2. Use a relative path from the project root
3. Use `includes` to limit which files the plugin runs on (optional) — omit = runs on all files, `[]` = runs on none; negated `!pattern` are exceptions only — a positive `**` pattern must come first
4. Verify the plugin loads correctly

### 5. Discover CST Node Names

> Goal: Find CST node names for GritQL patterns

1. Open the [Biome Playground](https://biomejs.dev/playground/)
2. Paste the code snippet you want to match
3. Switch to the Syntax tab to view the syntax tree
4. Use the node name (PascalCase) in the GritQL pattern
5. Check node names in the `.ungram` files in the Biome repository for the complete list

### 6. Verify

> Goal: Test the plugin with Biome

1. Run `bunx biome lint` to test the plugin (`biome check` = lint+format; `lint --write` applies safe rewrites, `--unsafe` includes unsafe)
2. Verify the custom rules behave correctly
3. Test edge cases and false positives
4. Test rewrites (`=>`) for fixable diagnostics

### 7. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Plugin File

- Use the `.grit` extension for plugin files
- Place the file at the project root
- Always put the `language` directive at the top
- Add `engine biome(1.0)` when using Biome CST node names
- Use `//` for comments

### 2. Target Languages

- `language js` for JavaScript (default)
- `language js(typescript)` for TypeScript
- `language js(typescript, jsx)` for TypeScript + JSX
- `language css` for CSS
- `language json` for JSON
- If unspecified, JavaScript is the default

### 3. register_diagnostic()

- `span` (required): the syntax node to attach the diagnostic to
- `message` (required): the message to display
- `severity` (optional): `hint`, `info`, `warn`, `error` (default: `error`)
- `fix_kind` (optional): `safe` or `unsafe` (default: `unsafe`) — used when a rewrite `=>` is present

### 4. GritQL Patterns

- Code snippets: wrap code in backticks `` ` ``
- Metavariables: use the `$` prefix, e.g. `$message`, `$value`
- Regex: use `r"..."` to match a node's text content
- Conditions: `where`, `<:` (match operator), `and`, `or`, `!`
- Pattern modifiers: `contains`, `within`, `after`, `before`, `some`, `every`, `as`
- CST nodes: use PascalCase function calls, e.g. `JsIfStatement()`, `CssDeclarationWithSemicolon()`
- CST fields: use named args, e.g. `JsConditionalExpression(consequent = $cons)`
- Rewrites: use the `=>` operator, e.g. `` `console.log($msg)` => `console.warn($msg)` ``
- Multiple rules: use an `or` block to combine several rules in one file

### 5. Configuration

- Define plugins via the `plugins` array in `biome.jsonc`
- Use relative paths from the project root
- String form: `["./custom-rules.grit"]`
- Object form with `includes`: `[{ "path": "./plugin.grit", "includes": ["src/**/*.css"] }]`
- `includes` uses glob patterns and supports negation (`!`)
- Plugins can be defined in the root `biome.jsonc` and extended by child configs
- Suppress a diagnostic with `// biome-ignore lint/plugin: <reason>`

### 6. Common CST Node Names

- JavaScript: `JsIfStatement`, `JsCallExpression`, `JsArrowFunctionExpression`, `JsVariableDeclaration`, `JsxElement`, `JsxAttribute`
- TypeScript: `TsAnyType`, `TsTypeAlias`, `TsInterfaceDeclaration`
- CSS: `CssDeclarationWithSemicolon`, `CssComplexSelector`, `CssDeclarationImportant`
- JSON: `JsonMember`, `JsonMemberName`, `JsonObjectValue`, `JsonArrayValue`
- Always verify node names in the [Biome Playground](https://biomejs.dev/playground/)

- Use /follow-create-sdk if needed
- Use /follow-tool-formatter if needed
- Use /run-lint if needed
- Use /run-format if needed

## Expected Outcome

- The `.grit` plugin file is created at the root
- `language` and `engine` directives are correct
- GritQL patterns behave as expected
- The plugin is configured correctly in `biome.jsonc`
- Custom rules work when running `bunx biome lint`
- No false positives or missing matches

## Guide

- [Biome Linter Plugins](https://biomejs.dev/linter/plugins/)
- [GritQL Plugin Recipes](https://biomejs.dev/recipes/gritql-plugins/)
- [GritQL Reference](https://biomejs.dev/reference/gritql/)
- [GritQL Language Documentation](https://docs.grit.io/language/overview)
- [Biome Playground](https://biomejs.dev/playground/)
