# CLAUDE.md

Consumer-facing context (what the tool checks, monorepo support, Node LTS reference) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./bin
npm run dev   # Build and run locally
npm test      # from the repo root — no per-package test script
```

## Internal architecture

Helpers in `src/helpers/`:

- **`checkEngine(path, { include, lts })`** — pure: reads one `package.json`, collects `engines.node` from every dependency (or devDependency if dependencies is empty, plus the `include`d groups), and returns a `WorkspaceResult`, with an LTS advisory when `lts` is given. It never exits or writes.
- **`findWorkspaces(cwd, workspaces)`** — expands workspace globs with `node:fs` `globSync`; root first, then sorted.
- **`fetchNodeInfo(path)`** — current and maintained LTS from nodejs.org (3s timeout), falling back to `./node.json`; throws with instructions if both fail.
- **`formatHuman(results, { quiet })`** — pure: renders the results as one line per workspace, plus warning and advisory lines; `quiet` returns `''` when every workspace passes.
- **`buildReport(results, lts)`** — pure: the `--json` document (`{ ok, lts, workspaces }`, workspaces sorted by path).

`src/index.ts` fetches the LTS info once (skipped by `--no-lts`), resolves the `package.json` files via `findWorkspaces`, and runs `checkEngine` once per path. The human report goes to stderr (`--json` also writes the document to stdout; `--quiet` hides the human text on success), and `process.exitCode` is set to `1` once if any result failed (`process.exit` is never called). A `fetchNodeInfo` error propagates.
