# backend/src/piMcp

Loads the third-party **`pi-mcp-adapter`** into exactly the Pi sessions Lattice
owns so the MCP servers a user enables for Pi (Settings → MCP → the Pi toggle)
are available — **never** the user's global Pi config. `../piMcp.ts` is the
public barrel. Close sibling of `piSubagents/` (same private-install + cwd-exact
shim pattern); read that CLAUDE.md too.

## Why an adapter at all

Pi ships no native MCP client (deliberate — MCP tool defs are token-heavy). The
adapter for official Pi (`@earendil-works/pi-coding-agent` ≥0.74) is
**`pi-mcp-adapter`**; it targets `@earendil-works/pi-*` and supersedes the
earlier `pi-mcp-extension` fallback (which targeted the pre-rename
`@mariozechner/pi-*` and could not do `${VAR}` interpolation). The adapter
auto-discovers standard MCP config files; the one Lattice writes is the
project override `<cwd>/.pi/mcp.json`.

Config precedence (later wins on merge): `~/.config/mcp/mcp.json` → `<Pi agent
dir>/mcp.json` (`~/.pi/agent/mcp.json`) → `.mcp.json` → **`.pi/mcp.json`**.
Lattice only ever writes the last one (project-scoped), so the user's global
Pi config is untouched. (The adapter also parses an explicit `--mcp-config
<path>` argv flag, but Lattice uses the `.pi/mcp.json` discovery path so a `pi`
the user launches at the project root is covered too, not just Lattice-built
command lines.)

## Mechanism (differs from Claude/Codex)

Claude/Codex resolve config in the backend and APPLY it in the terminal-server
(wire data). Pi's config is **cwd-local files** the adapter auto-discovers, so
the **backend writes them at the spawn chokepoint** (`applyPiMcpForSpawn`, called
from `resolvePiSpawn` in `terminalServerClient/spawnPi.ts`, which the chokepoint
`resolveHarnessSpawnBody` in `spawnBody.ts` dispatches a Pi command to) — the files
must exist in the session cwd before Pi starts, and the backend has fs access +
knows the cwd. Two files per Lattice Pi session cwd with ≥1 enabled server:

- `<cwd>/.pi/mcp.json` — the enabled server set, **reconciled** with a
  `__latticeManagedMcp` marker (adds ours, strips ours-now-disabled, leaves the
  user's own servers alone). Each server carries `lifecycle: 'eager'` (connect at
  session start so tool metadata is ready on a cold worktree) and `directTools:
  true` (register each server's tools as individual Pi tools, parity with the
  prior direct-tool exposure, rather than behind the adapter's `mcp()` proxy).
  `config.ts`.
- `<cwd>/.pi/extensions/lattice-mcp.ts` — the loader shim (`export { default }
  from "<shared install entry>"`), Pi discovers it cwd-exactly **but only when
  the project is trusted**. `shim.ts` / `render.ts`.

**Project-trust gate (official Pi ≥0.74).** Pi added a project-trust model:
cwd-local `.pi/extensions/` (this shim) is skipped in a non-interactive spawn
unless trust is granted. Lattice spawns Pi with **`--approve`**
(`../agentCommandBuilder.ts`) to trust the cwd's project-local files for that run
only — the flag that makes this shim load at all (it likewise repairs the
sibling pi-subagents + completion shims). Without `--approve`, everything in this
directory is inert under official Pi.

Secret transport (`../mcp/piServerConfig.ts` `toPiServerConfig`):

- **stdio secret env** → VALUE rides only in the pty env (`managedMcpEnv`) and is
  OMITTED from the JSON file; the adapter's `resolveEnv` copies the child's
  `process.env` before applying per-server `env`, so the MCP child inherits it.
- **HTTP header secret** → the adapter interpolates `${VAR}` / `$env:VAR` in
  `headers` (and `env`/`url`/`bearerToken`/`cwd`), so a secret header is written
  as a `${VAR}` **reference** (value in the pty env, under the same
  `LATTICE_MCP_<id>_<header>` naming as the Codex shaper via the shared
  `secretHeaderEnvVar`). This **lifts the old `pi-mcp-extension` limitation**
  where secret headers had to be dropped.

Resolution is in `../mcp/registry.ts` (`resolvePiServers` /
`resolveManagedPiServers`); shaping in `../mcp/piServerConfig.ts`.

## Modules

- `paths.ts` — `installDir()` (`~/.lattice/pi-mcp-adapter/`, **separate** from
  pi-subagents so two `pi install -l` runs don't prune each other's deps),
  `packageDir()`, `PI_MCP_SPEC` (`npm:pi-mcp-adapter`); re-exports the generic
  `resolveEntry` from `piSubagents/paths.js`. (A lingering `~/.lattice/pi-mcp-ext/`
  from the old `pi-mcp-extension` path is simply orphaned.)
- `install.ts` — `runPiMcpInstall(cwd)`: the `pi install npm:pi-mcp-adapter -l`
  spawn (static args → no injection surface).
- `ensure.ts` — `ensurePiMcpInstalled()` (boot + project open, single-flight,
  never throws) + `getPiMcpEntry()`.
- `render.ts` — pure shim renderer `renderPiMcpShim(entry)` +
  `PI_MCP_SHIM_FILENAME`.
- `shim.ts` — `installPiMcpShim({dir})`: graceful no-op until the install
  resolves; idempotent (skips a matching write).
- `config.ts` — `reconcilePiMcpDocument` (pure marker reconcile, unit-tested) +
  `writePiMcpConfig` (per-cwd-serialized atomic temp→rename).

The managed files are gitignored/excluded via `../worktree/managedFiles.ts`.
Always installs when `pi` is present; the per-server enable is the toggle.
