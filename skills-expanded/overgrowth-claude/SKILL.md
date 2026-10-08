# CLAUDE.md

`overgrowth` reclaims disk space from heavy build artifacts (`node_modules` by
default). It is an Nx monorepo with two layers: a **TypeScript orchestrator**
(`packages/cli` + `packages/core`, on Bun) that parses args, runs the terminal
UI, and moves matches to trash, and a **native Rust engine** (`native/`) that
does the filesystem scanning/sizing/deletion and streams JSONL events the
orchestrator reacts to.

**Read [AGENTS.md](./AGENTS.md) first** — it links into `docs/` for the
architecture, the workspace map, the JSONL protocol, and the release flow. This
file is just the quick-start.

## Quick commands

- `bun test` — run every TypeScript suite (`nx run-many -t test`).
- `bun run typecheck` — `tsc --noEmit` across all packages, must stay clean.
- `bun run lint` — `cargo clippy --all-targets -- -D warnings`, must stay clean.
- `bun run dev` — run the app (TUI) against the current directory.
- `bun run build:native` — build the Rust engine (needs `cargo` on PATH); run its
  own tests with `nx test native`.

## Rules that matter most

- **TDD first.** Write the failing test, then the code. The pure core
  (`reduceEvent`, `parseSize`, `validateEngineEvent`) and the fake-engine seam in
  `packages/core/test/spawn.test.ts` exist to make this cheap. `bun test` and
  `bun run typecheck` must both be green before a change is done.
- **Respect the package boundary.** `@overgrowth/core` must not import
  `@opentui/core`; TUI code belongs in `packages/cli`, which imports core through
  its single entry point.
- **YAGNI.** No speculative abstraction — add one only when a second real caller
  needs it (see `docs/contributing.md` for the principles the codebase follows).
- **Honor strict TypeScript.** `strict`, `noUncheckedIndexedAccess`, and
  `exactOptionalPropertyTypes` are on. Model the types; don't reach for `any`/`!`.
- **Never weaken the deletion guards.** Every delete path goes through
  `validateDeletionTarget` in `packages/core/src/delete/trash.ts`, with a test for
  the new case.
