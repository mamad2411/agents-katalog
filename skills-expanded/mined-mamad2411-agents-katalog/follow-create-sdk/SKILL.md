---
name: follow-create-sdk
description: Ask and route to the follow-create-* skill that best fits the build task
argument-hint: "[skill-name-or-goal]"
related:
  - ask-me
  - search
  - report
  - ship
  - update-references
  - deep-review-codebase
  - run-test
  - update-tests
  - update-devin-global-skills
  - update-devin
  - follow-create-web
  - follow-create-cli
  - follow-create-rust-cli

---
## Goal

Help the user pick the `follow-create-*` skill that best fits the build task, then hand off and proceed immediately

## Scope

Use when the user wants to create a project/plugin/library/extension/CLI/skills/subagents/MCP/web/mobile but isn't sure which `follow-create-*` or suitable skill to use

- If the goal is `sdk`/`library`/`framework-agnostic` → use the `## Framework-Agnostic Pattern` below (Core + Adapters)

- Build toolchain: `typescript` + `tsdown` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Inspect the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
3. Record the reasons for choosing the stack and libraries for later reference (create sdk)

### 2. Parse Argument

> Goal: Check whether the user specified a skill or goal

1. If the user gives a `skill-name` matching an existing `follow-create-<name>` → hand off to that skill immediately
2. If the user gives a goal (e.g. `bun cli`, `mobile app`, `vite plugin`, `skills`, `mcp`, `web`, `mobile`) → use it to sort the options
3. If nothing is given → go to the next step

### 3. Discover Create Skills

> Goal: Find all existing `follow-create-*` skills

1. Use `search-files-patterns` or `exec` to find `follow-create-*/SKILL.md` in `%APPDATA%\devin\skills`
2. Read each skill's frontmatter (`name`, `description`)
3. Build a list: skill name, description, approximate category
   - `skills` → `update-devin-global-skills`
   - `devin skills` → `update-devin-global-skills`
   - `project skills` → `follow-create-devin-project-skills`
   - `update all skills` → `update-devin-global-skills`
   - `subagents` → `update-devin-global-subagents`
   - `mcp`/`plugins` → `follow-create-devin-plugins`, `follow-create-claude-plugin`, `follow-create-codex-plugin`
   - `web` → `follow-create-web` (+ `follow-create-web-nextjs`, `-nuxt`, `-astro`, `-svelte`, `-solidstart` per framework)
   - `cli` → `follow-create-cli`, `follow-create-bun-cli`, `follow-create-rust-cli`
   - `mobile` → `follow-create-ios-android-native-by-kotlin-multiplatform`, `follow-create-mobile-cross-with-capacitor`
   - `extension` → `follow-create-vscode-extensions`, `follow-create-zed-extensions`, `follow-create-raycast-extensions`, `follow-create-obsidian-plugin`, `follow-create-nvim-plugins`
   - `sdk`/`library`/`framework-agnostic` → `## Framework-Agnostic Pattern` below
4. Use `/report` to show a summary table so the user sees the overview before being asked

### 4. Build And Ask Options

> Goal: Ask the user which follow-create- to follow

1. Sort skills by relevance to the goal/argument first; with no goal, sort by category (`skills`, `subagents`, `mcp`, `web`, `mobile`, `cli`, `plugin`) then name
2. Use `/ask-me` with `ask_user_question` in batches of at most 3 skills + a `More...` option per batch
3. Use short skill names as the option `label`, e.g. `follow-create-bun-cli`
4. Use the frontmatter description as the `description`
5. If skills remain → always add `More...` (except the last batch)
6. At the last batch → add `Skip` and `Suggest another` as choices
7. If the user picks `More...` → show the next batch
8. If the user picks `Skip` → stop and report that nothing was selected
9. If the user picks `Suggest another` → let the user type a skill name or goal, then re-match

### 5. Invoke Selected Skill

> Goal: Hand off to the selected skill

1. If the user picks one skill → call the `skill` tool with `skill: <selected-skill-name>`
2. If the user picks several skills → confirm the order with the user via `/ask-me` first, then invoke in order
3. If the user answers free-form (custom text) → use `search-skills` or string match against `follow-create-*`, then invoke if there's a match
4. If the selected skill creates a project/app/CLI that must ship, or the user asks to ship → invoke `/ship` after the selected skill finishes

### 6. Handle Mismatch

> Goal: Handle cases where nothing is found or matched

1. If no skill matches the argument or goal → show the full follow-create-* list
2. If the match is unclear → ask the user to confirm before invoking
3. If the user wants a skill that doesn't exist → report it as unavailable and stop

## Rules

- If the user names a skill exactly, hand off immediately without re-asking
- Ask in batches of no more than 4 options (including `More...` or `Skip`/`Suggest another`)
- Use the description from each skill's `SKILL.md` frontmatter
- Don't invent new `follow-create-*` entries that don't exist
- After the user selects, the skill must be invoked with the `skill` tool
- If multiple skills are selected, confirm the order first
- If the user wants to ship, invoke `/ship` after the selected skill finishes

- Use /follow-create-biome-plugin if needed
- Use /follow-create-bot if needed
- Use /follow-create-browser-extensions-wxt if needed
- Use /follow-create-bun-cli if needed
- Use /follow-create-cli if needed
- Use /follow-create-elysia-plugin if needed
- Use /follow-create-eslint-plugin if needed
- Use /follow-create-github-action if needed
- Use /follow-create-mcp if needed
- Use /follow-create-nitro-plugin if needed
- Use /follow-create-nvim-plugin if needed
- Use /follow-create-obsidian-plugin if needed
- Use /follow-create-oxlint-plugin if needed
- Use /follow-create-powershell-module if needed
- Use /follow-create-product if needed
- Use /follow-create-raycast-extensions if needed
- Use /follow-create-rolldown-plugin if needed
- Use /follow-create-rust-cli if needed
- Use /follow-create-rust-crate if needed
- Use /follow-create-tauri-plugin if needed
- Use /follow-create-tsdown-plugin if needed
- Use /follow-create-vite-plugin if needed (create sdk)
- Use /follow-create-vitest-plugin if needed
- Use /follow-create-vscode-extensions if needed
- Use /follow-create-zed-extensions if needed
- Use /run-test if needed
- Use /update-references if needed
- Use /update-tests if needed

## Framework-Agnostic Pattern

Use when the goal is an `sdk`/`library` that works across frameworks (React, Vue, Svelte, Solid, or vanilla) — the same pattern as TanStack (`*-core` + framework adapters):

- `src/core/` (or the `@scope/name-core` package) = business logic in vanilla TS only — never import framework deps; the API accepts/returns plain data via standard Web APIs (`URL`, `Request`, `Response`, `AbortSignal`, `EventTarget`)
- If validation library interop is needed → implement `StandardSchemaV1` (supports Zod, Valibot, ArkType without binding to any single one)
- Adapters `src/react/`, `src/vue/`, etc. = thin wrappers mapping to framework reactivity/lifecycle only — the API must stay consistent across adapters
- Every framework is a `peerDependency` + `peerDependenciesMeta.optional` — never put them in `dependencies`
- `package.json` uses subpath `exports` (`"."` → core, `"./react"` → adapter) — run `/follow-tool-tsdown` for the multi-entry build
- Keep types in `core/types.ts` — don't bind core to framework lifecycle or global state

## File Structure

Canonical file structure + layer table: [templates/file-structure-sdk.md](templates/file-structure-sdk.md)
- Use /deep-test api and /deep-test contract to verify the SDK surface against the API contract

## Expected Outcome

- The user sees the full list of existing `follow-create-*` skills
- The user picks the desired skill via `/ask-me`
- The selected skill is invoked, with `/ship` if needed

