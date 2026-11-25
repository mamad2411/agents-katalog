---
name: execute-install
description: Use this skill to understand how to install, setup, run or deploy project in local or production environments.
---

# Local Installation

## [Prerequisites]

1. Install Bun first; repo uses `bun.lock` and Bun scripts.
    - Expected: Bun can run `bun --version`.
2. Install OpenCode too; plugin loads in OpenCode and writes shim to `~/.config/opencode/plugins/autocode.js`.
    - Expected: OpenCode config dir exists or can be created.
3. Install Node.js too; `bun run verify:sandbox-online` uses `node scripts/verify-sandbox-online.mjs`.
4. Use bubblewrap (`bwrap`) if sandbox tools will run.
    - Evidence: sandbox code rejects `proot`/`proot-distro` and requires `bwrap`.

## [Local Setup Steps]

1. Install deps with `bun install`.
    - Expected: `node_modules/` and Bun lockfile.
2. Keep config in `~/.config/opencode/autocode.jsonc` or `.opencode/autocode.jsonc`.
    - Why: global config loads first, then worktree, then active directory overrides.
3. Use JSONC keys `autocode.tier`, `autocode.tiers`, `autocode.sandbox`, and `permission.external_directory`.
    - Example: `{"autocode":{"tier":"fast","sandbox":{"sync_method":"auto"}}}`
4. Put generated skill sources in `src/skills/**/SKILL.md`.
    - Why: build copies them into `dist/skills/**/SKILL.md`.

## [Startup Steps]

1. Build once with `bun run build`.
    - Why: it preserves the live `dist` entrypoint, bundles `src/plugin.ts`, emits declarations, and copies skills.
    - Expected: `dist/plugin.js`, `dist/plugin.d.ts`, `dist/skills/**/SKILL.md`.
2. Install the local shim with `bun run install:shim`.
    - Why: build does not install the shim.
    - Expected: `~/.config/opencode/plugins/autocode.js`.
3. Run watch mode with `bun run watch` for live edits.
    - Why: it watches Bun bundle plus TypeScript declarations.
4. Load plugin in OpenCode using the generated shim path.
    - Example path: `~/.config/opencode/plugins/autocode.js`.
    - Do not add a repository-local shim for AutoCode: it duplicates the global plugin ID.

## [Common Project Commands/URLs]

1. `bun run build` — production build.
2. `bun run watch` — rebuild on file changes.
3. `bun test` — Bun test suite under `src/**/*.test.ts`.
4. `bun run typecheck` — TypeScript no-emit check.
5. `bun run copy:skills` — refresh `dist/skills` only.
6. `bun run verify:sandbox-online` — verify sandbox connectivity script.
7. No app URL or local port found in repo; plugin/library only.

# Production Deployment

## [Packaging Steps]

1. Run `bun run build` before publish or install.
    - Why: package exports `dist/plugin.js` and `dist/plugin.d.ts`.
2. Confirm npm files include only `dist` and `scripts`.
    - Evidence: `package.json` `files` array.

## [Deployment Steps]

1. Install or copy package into OpenCode plugin path.
    - Why: OpenCode loads the built plugin from the installed package or local shim.
2. Restart OpenCode after update.
    - Why: host must reload plugin entrypoint and generated skills.
