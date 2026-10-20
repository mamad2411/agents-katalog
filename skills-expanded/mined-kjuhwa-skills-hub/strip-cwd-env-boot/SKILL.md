---
name: strip-cwd-env-boot
description: Strip Bun's auto-loaded CWD `.env` keys (and nested Claude Code session markers) at entry-point boot before any module reads env at init time.
category: bun
version: 1.0.0
version_origin: extracted
tags: [bun, dotenv, entrypoint, process-env, isolation]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
linked_knowledge: [bun-auto-loads-cwd-env, nested-claude-code-session-deadlock]
---

# Strip CWD `.env` at Entry-Point Boot (Bun)

## When to use

You ship a Bun CLI or server that is intended to be invoked **from inside arbitrary user projects**. Bun auto-loads `.env`, `.env.local`, `.env.development`, `.env.production` from the CWD before any user code runs. If the target project has its own `.env` (e.g. `DATABASE_URL`, `PORT`, `LOG_LEVEL`, `OPENAI_API_KEY`), those keys leak into your process and shadow your own config.

Regular `dotenv.config({ override: true })` does not help: keys that exist only in the target repo's `.env` survive unaffected, because `override` only resolves the intersection.

Use this pattern when:

- Your tool's binary may be invoked with CWD inside any repo.
- You load your own config from `~/.toolname/.env` and expect it to win.
- You also want to detect and scrub "nested session" markers (e.g. `CLAUDECODE=1`) set by parent processes.

## Steps

1. **Create a dedicated boot-time module** that calls your stripper as a side effect of import. Example: `packages/paths/src/strip-cwd-env-boot.ts` just does `import { stripCwdEnv } from './strip-cwd-env'; stripCwdEnv();`.
2. **Make it the very first import in every entry point** (CLI, server, worker). Line 1 of `cli.ts`: `import '@archon/paths/strip-cwd-env-boot';`. This must come before any module that reads `process.env` at module load (logger, config, etc.).
3. **Inside the stripper**, iterate the list of Bun-auto-loaded filenames. For each file, call `dotenv.config({ path, processEnv: {} })` — `processEnv: {}` parses **without** mutating `process.env`. Collect the keys into a Set.
4. **Delete each key from `process.env`** via `Reflect.deleteProperty(process.env, key)`. Treat `ENOENT` as expected (file simply doesn't exist); log other parse errors to stderr.
5. **Afterwards, load your own config with `dotenv.config({ path: '~/.toolname/.env', override: true })`.** Now `override` only needs to beat shell-inherited env vars, which is the intended behavior.
6. **Second pass (optional): scrub nested-session markers.** For each `process.env` key, if it matches a well-known parent-tool pattern (Archon does this for `CLAUDE_CODE_*` and `CLAUDECODE`, keeping auth vars like `CLAUDE_CODE_OAUTH_TOKEN`), delete it — and emit a one-line stderr warning **before** the deletion so downstream code can't see the marker.

```ts
// strip-cwd-env.ts (shape, not full file — see Archon for details)
const BUN_AUTO_LOADED = ['.env', '.env.local', '.env.development', '.env.production'];
for (const f of BUN_AUTO_LOADED) {
  const r = config({ path: resolve(cwd, f), processEnv: {} });
  if (r.parsed) for (const k of Object.keys(r.parsed)) Reflect.deleteProperty(process.env, k);
}
```

## Counter / Caveats

- Don't strip **your own** env keys. Archon keeps `CLAUDE_CODE_OAUTH_TOKEN`, `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX` explicitly.
- `NODE_OPTIONS` / `VSCODE_INSPECTOR_OPTIONS` inherited from a debugger can crash spawned Claude Code subprocesses; Archon unconditionally strips them here too. Decide for your tool whether that scrub is appropriate.
- This is boot-time-only. If a tool you spawn reads `process.env` asynchronously after boot, it will see the stripped view — usually what you want, but audit carefully.
- On Node (no auto-load), the stripper is still safe — it no-ops when no files match.

## Evidence

- `packages/paths/src/strip-cwd-env.ts` (94 lines): two-pass logic, CWD .env strip + CLAUDE_CODE_* scrub + NODE_OPTIONS/VSCODE_INSPECTOR_OPTIONS strip.
- `packages/paths/src/strip-cwd-env-boot.ts` (13 lines): 3-line side-effect boot module.
- `packages/cli/src/cli.ts:12`: literal `import '@archon/paths/strip-cwd-env-boot';` as the first real import.
- Comment in `strip-cwd-env.ts` cites coleam00/Archon#1097 (Agent SDK leaks `process.env` into spawned child regardless of explicit `env` option) and coleam00/Archon#1067 (CLAUDECODE nested-session warning).
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
