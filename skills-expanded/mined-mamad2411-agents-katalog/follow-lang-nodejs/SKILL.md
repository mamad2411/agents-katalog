---
name: follow-lang-nodejs
description: Use the Node.js runtime to develop and run JavaScript/TypeScript projects across its ecosystem
argument-hint: "[scope|setup-project|migrate-version]"
related:
  - follow-lang-javascript
  - follow-lang-typescript
  - follow-lang-bun
  - follow-best-practice
  - setup-cicd
  - use-scripts
  - deep-research

---

## Goal

Use the Node.js runtime to develop and run JavaScript/TypeScript projects with the largest, most mature ecosystem

## Scope

For projects needing maximal ecosystem compatibility or a mature runtime. Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/` — dispatch: `setup-project` → `workflows/setup-project/SKILL.md`, `migrate-version` → `workflows/migrate-version/SKILL.md`; verify current Node LTS/release behavior via `/deep-research` at use time (official docs: https://nodejs.org/api/)

## Execute

### 1. Check Version And Setup Project

> Goal: set up the Node.js project with live-checked versions

1. Run `/deep-research` + `/follow-best-practice` to confirm the current LTS, active releases, and current Node practices; pin the project to a supported line via `mise use -g node` (or `.nvmrc`/Volta) — never an EOL version
2. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): scaffold, ESM default, scripts, TypeScript config, verify, git hygiene
3. Tool inventory (runtime, PM, test runner, linter) → `references/toolchain.md`

### 2. Use The Module System Correctly

> Goal: pick and apply one module system consistently

1. Prefer ESM (`import`/`export`); use CommonJS (`require`/`module.exports`) only when interop demands it
2. For interop, use dynamic `import()` from CJS; never dual-maintain two module systems in one package
3. Built-in modules: import with the `node:` prefix (`import fs from "node:fs/promises"`)
4. Key modules by task: `node:fs/promises`, `node:path`, `node:http`/`node:https`, `node:events`, `node:stream`, `node:crypto`, `node:test` (built-in runner), `node:child_process`, `node:worker_threads` (CPU-heavy work), `node:v8`/`node:vm` (specialized)

### 3. Use Globals And Modern Runtime APIs

> Goal: rely on stable runtime globals instead of shims

1. Use `process` (env, argv, exit codes), `console`, `Buffer`, `URL`, `URLSearchParams`, `TextEncoder`
2. Use the global `fetch`, `structuredClone()`, `AbortController`, Web Streams — check support for the pinned version before use
3. Handle errors properly: `process.on("unhandledRejection")`, typed error propagation, graceful shutdown on `SIGTERM`

### 4. Use CLI Efficiently

> Goal: run, watch, and debug with the right command

1. `node --watch file.ts` for dev (type-stripping per pinned version support; otherwise `/follow-lang-bun` or a loader), `node --inspect` for debugging
2. `npm init -y`, `npm install`, `npm run <script>`, `npm test`; `pnpm add -D <pkg>`; `npx <pkg>` for one-off execution
3. Scaffolding via the framework's official creator, not deprecated generators — live-check with `/deep-research`

### 5. Migrate Versions

> Goal: move between Node.js major versions safely

1. Run the workflow `workflows/migrate-version/SKILL.md` (argument `migrate-version`): baseline, per-major changelog review, runtime switch with pins in one commit, verify per bump, ship

## Rules

### 1. Runtime Hygiene

- Pin to a supported (LTS-preferred) major; check the release schedule before upgrades — live-verify, never restate version numbers from memory
- `node:` prefix for built-ins; one module system per package
- async/await over callbacks; proper error handling and graceful shutdown

### 2. Ecosystem

- `npm`/`pnpm`/`yarn` per project choice; `npx`/`pnpm dlx` for one-offs
- Audit dependencies (`npm audit`) and keep them updated via `/improve deps`

### 3. Resources

- Official API docs (https://nodejs.org/api/), ESM guide, security and profiling guides are the primary sources — fetch them with `/learn-from-web` when unsure

- Use /follow-lang-javascript if needed
- Use /follow-lang-typescript if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed

## Expected Outcome

- Projects compatible with the largest JS/TS ecosystem
- Stable development on a supported Node.js release line
- Consistent module system, proper error handling, and clean version migrations
