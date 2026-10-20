# backend/src/piSubagents

Auto-installs the `@tintinweb/pi-subagents` Pi extension and makes it active in
exactly the Pi sessions Lattice owns — **never** the user's global Pi config.
`../piSubagents.ts` is the public re-export barrel; every consumer keeps importing
from `'../piSubagents.js'`.

## Scope (the whole point)

- **Shared Lattice install, not global.** `pi install npm:@tintinweb/pi-subagents`
  (no `-l`) writes the GLOBAL `~/.pi/agent/settings.json` `packages` array, so the
  extension would load in *every* pi session on the machine. We instead run
  `pi install … -l` **once** with cwd = `~/.lattice/pi-extensions/` (home-scoped,
  outside any project tree). That writes a project-local
  `<dir>/.pi/settings.json` + `<dir>/.pi/npm/node_modules/…`; the user's global
  config stays `packages: []`.
- **Per-cwd discovery shim, not `-e`.** Pi discovers `<cwd>/.pi/extensions/*.ts`
  **cwd-exact** (it does not walk up). So we drop a tiny re-export shim
  `lattice-subagents.ts` (`export { default } from "<shared entry>"`) in each
  session cwd we want it in — every Lattice-spawned Pi session (worktree task,
  workflow step, post-merge hook) **plus the project root**
  (so a `pi` the user types in the Lattice terminal panel, cwd = project root,
  gets it too). `-e` would only reach command lines Lattice itself builds; the
  discovery shim is what reaches a manually-typed `pi`. The shim coexists with
  `lattice-complete.ts` and is gitignored/excluded via `worktree/managedFiles.ts`.
- **Requires `--approve` on official Pi ≥0.74.** Pi's project-trust gate skips
  cwd-local `.pi/extensions/` in a non-interactive/untrusted spawn, so this shim
  (and `lattice-complete.ts`, and the MCP shim) only load because Lattice spawns
  Pi with `--approve` (`agentCommandBuilder.ts`) — per-run trust of the cwd's
  project-local files. A manually-typed `pi` at the project root without
  `--approve` will prompt for trust interactively (the user can accept).

## Modules

- `paths.ts` — `installDir()` / `packageDir()` / `resolveEntry(pkgDir)` and the
  `PI_SUBAGENTS_SPEC` constant. Resolution prefers the package's declared
  `pi.extensions[0]`, falling back to `dist/index.js` then `src/index.ts`;
  returns a forward-slashed absolute path or null when not yet installed.
- `install.ts` — `runPiInstall(cwd)`: the `pi install … -l` spawn (via
  `../spawnWithTimeout.js`, `shell:true` so Windows resolves `pi`→`pi.cmd`),
  resolve-on-exit-0 / reject-otherwise. Static args = no injection surface.
- `ensure.ts` — single-flight state. `ensurePiSubagentsInstalled()` (boot +
  project open; idempotent, retries after a transient failure, **never throws**)
  resolves the entry once; `getPiSubagentsEntry()` exposes it (or null).
- `render.ts` — pure shim rendering: `renderPiSubagentsShim(entry)` +
  `PI_SUBAGENTS_SHIM_FILENAME`. Unit-tested in `__tests__/piSubagents.test.ts`.
- `shim.ts` — `installPiSubagentsShim({dir})`: writes the shim into
  `<dir>/.pi/extensions/`. A graceful no-op until `ensure` resolves (a shim
  pointing at a missing entry would make Pi error at startup); idempotent —
  skips the write when on-disk contents already match, so a worktree reconcile
  doesn't dirty `git status`.

Always on when `pi` is present — no toggle.
