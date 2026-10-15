---
name: refactor-web-05-naming
description: Use this skill when the user wants to check or fix front-end naming conventions against the Alibaba front-end standard and the integrated-system UI standard — for example when they mention "naming convention", "component naming", "file naming", "variable naming", "CSS class name", "naming check", "naming review", "naming fix", or "rename". It is step 5 of 5 of the frontend governance lane in the refactor-chain bundle. The ruleset is selected adaptively from the project's `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`).
---

# Front-End Naming Convention Check & Repair — refactor-chain · Web lane · step 05/05

**Bundle:** refactor-chain (orchestrated, self-healing refactor chain-of-skills).
**Lane:** Frontend project governance (versioned) · **Position:** step 05 of 05 · **Prerequisite:** refactor-web-04-layout · **Next:** refactor-code-solid (default final pass).
**Adaptivity:** Selects the versioned ruleset from `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`).

## Purpose
This skill is the multi-version-adaptive checker and fixer for front-end naming. Grounded in the Alibaba front-end development standard and the *Integrated System UI Standard*, it enforces standardized constraints on component naming, file naming, variable naming, CSS class names, event-handler naming, tab naming, workflow-node naming, and Props-type naming. Because naming rules can differ between releases, it selects the matching version's rules automatically from the project `package.json` `version`.

## When to use
- Verify that naming complies — triggers: "naming convention", "naming check", "naming review".
- Fix naming violations — triggers: "naming fix", "rename", "naming remediation".
- Check a specific category — triggers: "component naming", "file naming", "variable naming", "CSS class name".

## Rules enforced
Version detection runs first and is mandatory: read the project root `package.json`, extract `version`, and route as follows — exact match to `3.6.0-SNAPSHOT` / `3.6.1-SNAPSHOT` / `3.7.0-SNAPSHOT`; fuzzy `3.6.x-SNAPSHOT` → `3.6.1-SNAPSHOT` (latest of the 3.6 series); fuzzy `3.7.x-SNAPSHOT` → `3.7.0-SNAPSHOT`; anything else or unreadable → default `3.6.0-SNAPSHOT` (baseline). Then load that version's `REFERENCE.md` for the full ruleset.

**S8 — Naming checks (8 categories):**

| ID | Check | Level | Summary |
|------|--------|---------|------|
| `S8-01` | Component naming | ERROR | Components use `PascalCase`; a single-file component's file name matches its `name`; multi-word names (avoid clashing with HTML elements); base components start with `Base`/`App`/`V`. |
| `S8-02` | File naming | ERROR | TypeScript files use `kebab-case`; Vue component files use `PascalCase`; directories use `kebab-case`; test files are `*.spec.ts` / `*.test.ts`. |
| `S8-03` | Variable naming | WARNING | Variables/functions use `camelCase`; constants use `UPPER_SNAKE_CASE`; interfaces/types use `PascalCase`; enum values use `UPPER_SNAKE_CASE`; booleans take an `is`/`has`/`can`/`should` prefix. |
| `S8-04` | CSS class names | WARNING | Use BEM or CSS Modules — block `kebab-case`, element with a double-underscore (`query-panel__item`), modifier with a double-hyphen (`query-panel--expanded`); avoid inline styles; colors via CSS variables. |
| `S8-05` | Event-handler naming | WARNING | Handlers use a `handle` prefix (`handleSubmit`); custom events use an `on` prefix (`onUpdate`); emitted event names use `kebab-case` (`update:model-value`); computed properties are nouns/adjectives. |
| `S8-06` | Tab naming | WARNING | Tab labels are concise — no more than 6 Chinese characters. |
| `S8-07` | Workflow-node naming | WARNING | Workflow nodes use a verb-object structure. |
| `S8-08` | Props-type naming | ERROR | Props interfaces are named as the component name plus a `Props` suffix. |

Category detail — component naming (`S8-01`): scan every `.vue` file name, verify `PascalCase`, verify the component `name` attribute matches the file name, and verify the name is multi-word (two or more words); e.g. `DataTable.vue → name: 'DataTable'` is compliant, while `dataTable.vue`, `data-table.vue`, and the single-word `Table.vue` (clashes with HTML `<table>`) are violations. File naming (`S8-02`): scan `.ts` names for `kebab-case`, `.vue` names for `PascalCase`, and directory names for `kebab-case`, excluding build directories such as `node_modules/` and `dist/`; e.g. `composables/use-table-data.ts` and `components/DataTable.vue` are compliant, while `composables/tableData.ts` and `types/BaseData.ts` are violations.

## Procedure
1. Detect the project version from `package.json` and resolve the version directory using the routing table above.
2. Load that version's `REFERENCE.md` to obtain the full check rules.
3. Run the naming check across the selected scope — all categories, or only the requested category (component / file / variable / CSS) — consulting the rule scripts under `scripts/` (and the exhaustive per-version rules under `references/original/versions/<version>/`).
4. Emit a report of compliant items and violations, each violation carrying its ID, level, and the compliant form.
5. For a fix task, apply or propose the corrected names (rename files, update `name` attributes, adjust identifiers/class names) consistently across references.

## Guardrails
- Do not change business logic/behavior; structural + standards refactoring only.
- Renames must be applied consistently everywhere a symbol, file, or class is referenced; never leave dangling imports, stale `name` attributes, or broken selectors. Do not rename anything inside build/vendor directories.

## Verify
Confirm the resolved version matches `package.json` (or documents the fallback). Every applicable S8 category is checked with each violation carrying an ID, level, and compliant form. After any fix, the project still resolves — no dangling imports, mismatched component `name`s, or orphaned CSS selectors remain.

## References
The exhaustive original rules, versioned rule sets, and templates are bundled verbatim under `references/original/` (source of truth).

## Chain position
Runs after refactor-web-04-layout. On success the orchestrator advances to refactor-code-solid (default final pass). `refactor-code-solid` runs by default as the final step of the lane.
