---
name: follow-create-eslint-plugin
description: Create custom ESLint plugins with JavaScript/TypeScript
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - deep-review-codebase
  - follow-tool-eslint
  - ship
  - report
  - run-lint
  - run-format
---
## Goal

Create custom ESLint plugins with JavaScript/TypeScript to add project-specific rules

## Scope

Use for creating custom ESLint plugins with JavaScript/TypeScript, covering the plugin entry, custom rules, metadata, testing, and flat config

- Packages: `eslint` (10.x — flat config only, Node >= 20.19, deprecated `context`/`SourceCode` members removed, fixer text must be a string, stricter RuleTester), `typescript-eslint` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (don't pin in files — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
3. Record the rationale for the chosen stack and libraries for future reference (create eslint plugins)

### 2. Setup

> Goal: prepare the project directory and dependencies for the plugin

1. Create the project directory for the plugin
2. Create `package.json` with the npm package name as `eslint-plugin-*`
3. Install the necessary dependencies

### 3. Create Plugin Entry

> Goal: create the entry file exporting a plugin object with complete properties

1. Create the entry file that exports the plugin object
2. Define the properties: `meta` (`name`, `version`), `configs`, `rules`, `processors`
3. Export ESM (`export default plugin`) or CommonJS (`module.exports = plugin`) — to support both flat config and eslintrc, use a dual export: `plugin.configs["flat/recommended"]` (an array with `plugins: { ns: plugin }`) + `plugin.configs.recommended` (eslintrc object `plugins: ["ns"]`)

### 4. Create Custom Rules

> Goal: create rule files and implement rule logic with meta and create function

1. Create rule files in the rules directory — each rule exports an object with `meta` + `create(context)`
2. `create(context)` returns a visitor object — keys are node types/selectors (called going down), `<type>:exit` (going up), or code path events (`onCodePathStart`/`onCodePathEnd`)
3. Use `context.options` (an array excluding severity), `context.settings` (shared config), `context.sourceCode` (`getText`, `getFirstToken`/`getLastToken`/`getTokenBefore`/`getTokenAfter`, `getAncestors`, `getScope`, `getDeclaredVariables`, `isSpaceBetween`, comments APIs) — report via `context.report()` or `messageId`

### 5. Configure Rule Metadata

> Goal: fully define the rule's type, docs, fixable, and schema

1. Define the type: problem, suggestion, or layout
2. Add docs for documentation
3. Define `fixable` if the rule can auto-fix
4. Define `schema` (a JSON Schema array — validates `context.options` by position) if the rule has options; `fixable`/`hasSuggestions` are mandatory when a rule produces fix/suggestions — ESLint throws an error if undeclared

### 6. Test Plugin

> Goal: verify the rules work correctly via test files

1. Create test files for rules using `RuleTester` from `eslint` (`new RuleTester()`, then `ruleTester.run('rule-name', rule, { valid, invalid })`)
2. Valid cases must not have `errors`/`output` (ESLint 10 is stricter — the test will fail); invalid cases use `messageId` and assertion options `requireMessage`/`requireLocation`/`requireData` as needed
3. Run tests with a test runner (`vitest`, `bun:test`, or the node test runner)
4. Verify that the rules work correctly

### 7. Ship

> Goal: deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Package Name

- Use the `eslint-plugin-*` naming convention
- The namespace in config is the package name with the `eslint-plugin-` prefix removed
- Example: `eslint-plugin-example` → namespace `example`

### 2. Plugin Structure

- Export an object with the properties: meta, configs, rules, processors
- Meta: information about the plugin
- Configs: named configurations
- Rules: custom rule definitions
- Processors: named processors for preprocessing code

### 3. Rule Structure

- A meta object with type, docs (`description`, `dialects`, `url`), messages (referenced by `messageId`, supports `{{ placeholder }}`), fixable, hasSuggestions, schema
- type: problem (error/confusing behavior), suggestion (a better way), layout (whitespace/formatting)
- fixable: "code" or "whitespace" if the rule can auto-fix
- hasSuggestions: true if the rule can provide suggestions
- schema: the options schema if the rule has options

### 4. Rule Implementation

- `create(context)` returns a visitor object — use `context.report()` to report violations
- Use `context.sourceCode` to access source code (ESLint 10 removed the deprecated `context.getSourceCode()` and deprecated `context`/`SourceCode` members)
- fixer: `insertTextBefore/After(node|range)`, `remove(Range)`, `replaceText(Range)` — `fix()` returns a fixing object, an array, or a generator; the smallest fix, one fix per message, doesn't change runtime behavior (ESLint re-runs rules up to 10 times)
- Fixer methods must always pass `text` as a string (ESLint 10)
- Use AST traversal to analyze code

### 5. Configuration

- ESLint 10 supports only flat config (the legacy `.eslintrc` format was removed) and requires Node.js >= 20.19 (v21, v23 unsupported)
- `eslint.config.js`/`mjs`/`cjs` exports an array via `defineConfig` from `eslint/config`; a config object has `name`, `files`, `ignores`, `plugins`, `rules`, `languageOptions`, `settings` (shared with every rule), `extends`
- In flat config, `plugins` is an object mapping namespace → plugin object (not an array like eslintrc) — a plugin can be defined inline in the config
- Import the plugin and assign the namespace; use `extends` with `"ns/recommended"` or `plugin.configs.recommended` (the `plugins` must be declared first)
- Use the `namespace/rule-name` rule format in the rules object

- Use /follow-create-sdk when needed
- Use /follow-tool-eslint when needed
- Use /run-lint when needed
- Use /run-format when needed

## Expected Outcome

- The plugin package is created with the correct naming convention
- Custom rules are created with the correct structure
- The plugin can be configured in the ESLint config
- Rules work when ESLint runs
