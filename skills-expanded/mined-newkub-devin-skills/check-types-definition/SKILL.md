---
name: check-types-definition
description: Inspect lib/config types as a CLI table — name, type, options, default, comment — TS/Rust/other
argument-hint: "<package-or-path> [--json]"
related:
  - learn
  - learn-from-web
  - learn-from-cli
  - follow-default-config
  - use-lib-effective
  - report
  - improve
  - follow-lib-tstyche
---

## Goal

View a library's or config type's real type surface as a single table — field name, type, options (union/enum), default, comment — to check what the config/API offers and what its defaults are, without relying on docs

## Scope

Use when you need an authoritative type surface:

- config file before writing → check which options already have a default (use with `/follow-default-config`)
- library API surface from `.d.ts` in `node_modules` — types are the compile-time source of truth
- Supports TypeScript `.d.ts`, Rust (`pub struct`/`enum` + doc comments/`#[serde(default)]`), and other type-def formats (JSON Schema, `.proto`) as present in the project
- Docs stale or incomplete → type definitions are the real contract
- Surface revealed should be guarded → write type tests pinning it with `tstyche` per `/follow-lib-tstyche`

Not for learning from web docs (use `/learn-from-web`) or a CLI binary (use `/learn-from-cli`)

## Execute

### 1. Locate Definitions

> Goal: Find the target's type-definition entry

1. Take a package name or path from the user
2. TS: read `node_modules/<pkg>/package.json` — look at `types`, `typings`, `exports["."].types`; if there are no bundled types → check `@types/<pkg>`
3. Rust: find `pub struct`/`pub enum` in the crate source or `cargo doc` JSON if present
4. Config schema: find the config object's type/interface (e.g. the `defineConfig` param type)

### 2. Extract Members

> Goal: Get complete field-level data

1. Parse the members of interfaces/types/structs: `name`, `type`, optional marker (`?`)
2. union/literal types → the `options` column (e.g. `mode: 'a' | 'b'`)
3. comments/JSDoc/doc comments above a member → the `comment` column; `@default`/`Default` impl/`#[serde(default)]` → the `default` column
4. `@deprecated` → flag it in the comment — don't recommend a deprecated member

### 3. Render Table

> Goal: A single readable CLI table

1. Use the CLI: `bun run scripts/types-def.ts <path-or-package> [--json]` — auto-detect the language from extension/content
2. columns: `Name` | `Type` | `Options` | `Default` | `Comment`
3. `--json` → machine-readable array; nested types expand into sub-tables
4. If the CLI can't parse it → extract manually per step 2 and render the table yourself

### 4. Report

> Goal: Summarize the usable surface

Summarize per `/report`: public fields/options with the defaults that must be overridden, deprecated members to avoid, and gaps the docs don't mention

## Rules

- Type definitions are the source of truth — don't guess options/defaults that aren't declared
- Every row needs evidence from the real definition — `-` when there's no data
- Report-only — don't modify config files or types in this skill (override decisions live in `/follow-default-config`)

## Expected Outcome

- A table covering every member of the inspected type: name/type/options/default/comment
- Clear knowledge of which options have defaults and need no writing, and which must be set manually
- Ready to use as input for `/follow-default-config` and config authoring
