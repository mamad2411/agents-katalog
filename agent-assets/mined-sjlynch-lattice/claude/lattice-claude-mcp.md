# backend/src/mcp

The MCP control plane: the single place a user curates/toggles MCP servers,
injected into the Claude, Codex and Pi sessions Lattice spawns. Policy is
**resolved in the main backend** (`registry.ts`) and **applied** per harness at
spawn. Owned elsewhere: the spawn chokepoint (`../terminalServerClient/`),
Claude's apply mechanism (`../claudeTrust/`), Pi's adapter + cwd files
(`../piMcp/`), Lattice's own server (`../latticeMcp/`), the MCP tab
(`frontend/src/components/settings/mcp/`), config import (`import/`) — each
has a `CLAUDE.md`.

## Per-harness mechanism

Every spawn funnels through `proxyCreateSession` → `resolveHarnessSpawnBody`
(`terminalServerClient/createSession.ts`): harness-neutral `resolveMcpEntries`,
then one shaper per harness.

- **Claude** (`claudeServerConfig.ts` → `mcpServers` map): shipped as data in
  `POST /sessions` (`managedMcpServers`, + `disableClaudeMemory`); the
  terminal-server writes `~/.claude.json` `projects[<cwd>]` just before
  `pty.spawn`.
- **Codex** (`codexServerConfig.ts` → `-c mcp_servers.lattice_<id>={…}` inline
  TOML + secret env): `configureCodexProjectMcp` (`../terminal/codexTrust.ts`)
  passes each as `--config` via an env var, so braces/quotes never enter shell
  source. Never writes `~/.codex/config.toml`; the dotted key MERGES, so the
  user's servers survive. Secrets by NAME (`env_vars=['VAR']`,
  `env_http_headers={Header='VAR'}`). A stdio secret's name is listed **even
  with no stored value**: Codex starts stdio servers from a cleared env, so
  that's the only way an ambient shell key arrives.
- **Pi** (`piServerConfig.ts`): the BACKEND writes `<cwd>/.pi/mcp.json` + the
  loader shim at the chokepoint (cwd files must exist before Pi starts). Never
  the user's global Pi config; see `../piMcp/CLAUDE.md`.

**Coverage: Lattice-created launches only** (sidebar terminals included;
detection is a command-prefix check). A failed pre-creation falls back to
serverless `/ws/terminal`, bypassing Codex/Pi MCP. A harness typed into an open
shell is invisible — deliberately no tracked `.codex/config.toml` or
project-root `.pi/mcp.json`.

## Policies

- **Third-party servers are off by default, three independent switches**:
  Claude `mcpOverrides`, Codex/Pi `mcpHarnessOverrides.{codex,pi}`. Enabling
  for one harness never loads it into another (`McpHarnessSupport` gates which
  can offer it). `harnessToggleOn` = explicit boolean, else `defaultEnabled`.
- **`lattice` is the one `defaultEnabled: true` entry** (own code, no key, no
  telemetry, local only; worktree agents and planners have nobody present to
  configure it). **Never set `defaultEnabled` on a third-party entry.** It is
  dropped when `ctx.projectPath` is absent (no tools beats tools that all
  fail); opt-out is a real per-harness switch (the tab renders
  `overrides[id] ?? !!defaultEnabled`); `settingsValidation.ts` never copies
  `defaultEnabled` off a custom entry or override (nothing else acquires it),
  and overrides can't re-point it. For Pi it also means every session loads
  `pi-mcp-adapter` (`mcpHarnessOverrides.pi.lattice = false` opts out).
- **`lattice` per-spawn env**: `resolveMcpEntries` emits a CLONE (never mutates
  the long-lived catalog), filled identically for every harness by
  `withSpawnContext`: `LATTICE_API_URL`, `LATTICE_PROJECT` (canonicalized, to
  match the server's `canonicalProject` check), and `LATTICE_TASK_ID` only for
  task run/resume and WORKTREE merge resolvers — **omitted, never empty**: it
  is what makes the server add `my_task` and drop board management +
  `opengrep_ignore` (an untrusted worktree brief must not write permanent
  ignores). `shapeLatticeEntry` strips `LATTICE_*` from an override's env.
  `command` is **`process.execPath`**, not bare `node` (no shell; the harness's
  PATH isn't ours); as an absolute `.exe` it stays unwrapped (`cmd /c` breaks a
  path with a space).
- **`lattice-control` (controller mode) → user-launched only**: opt-in, same
  per-spawn env (no task id). `resolveMcpEntries` drops it unless
  `ctx.userLaunched` — set by `userLaunchedScope.ts` (explicit `user`/`startup`
  owner, no task/QA/scope marker, not a Lattice-managed cwd; fail closed) and
  by the root reconcile. Never task agents, resolvers, workflow steps, push/QA.
  Accepted race (Claude): `projects[<root>]` is keyed by cwd, so a root
  resolver could read it just as a sidebar spawn or reconcile re-adds it.
- **Task-worktree scope → lattice-only** (`taskAgentsLatticeMcpOnly`, default
  ON, also when settings are absent/corrupt): task and worktree-resolver spawns
  get ONLY `lattice` (or nothing) — an idle stdio server is a ~100–180 MB
  process tree per agent. `latticeOnlyMcpApplies` needs `mcpScope:
  'task-worktree'` (set in `routes/tasks/harnessFactory.ts`,
  `routes/tasks/mergeResponses.ts`, `mergeRuns/resolverSpawn/spawn.ts`), the
  setting, AND a cwd strictly under `~/.lattice/worktrees/` —
  **load-bearing**: at a project root `projects[<cwd>]` is the user's own set.
  Persisted on `TerminalLaunch.mcpScope` so relaunches keep it.
  - Claude: also `--strict-mcp-config --mcp-config="<file>"`, appended in the
    BACKEND (a stale executor ignores new wire fields); the `=` form matters
    (`--mcp-config` is variadic). File under
    `per-project/<hash>/mcp-config/` (0600, per spawn, 30-day prune; flags
    skipped with a warning if its path can't be quoted portably). The
    registry keeps the ORIGINAL command, so flags never stack on relaunch.
  - Codex: only `lattice`, after `mcp_servers.<name>.enabled=false` for each
    server named in `$CODEX_HOME/config.toml` / `<cwd>/.codex/config.toml`.
    `-c 'mcp_servers={}'` removes nothing (the layer merges), and disabling a
    name Codex doesn't know fails startup — hence names read from the files.
  - Pi: only managed servers are restricted (the adapter merges the user's
    other MCP configs with no off switch).
- **Playwright has two independent toggles** (Claude; Codex/Pi get one).
  The GLOBAL toggle reaches every Lattice session + the project-root reconcile,
  headless unless `mcpPlaywrightHeaded`. `qaPlaywright` applies to QA runs ONLY
  (`ctx.isQaRun`, set by the QA-run spawn alone), its `headless` wins there, and
  **`mcpPlaywrightHeaded` never touches a QA run**. Catalog args always include
  **`--isolated`** (else a second instance dies "Browser is already in use").
- **Secrets live only in `~/.lattice/mcpSecrets.json`** (`0600`, own file, so
  settings endpoints never touch secret bytes; **raw values never reach the
  browser**) and reach a server by env NAME — **never argv, never written into
  harness config**.
- **A built-in override may TUNE a server but never re-point what it runs**
  (`settingsValidation.ts`, `overrideSecurity.ts`).

## Modules

- `catalog.ts` — `BUILTIN_MCP_SERVERS`; package names live in code (churn is a
  code change, not a data migration). The `McpServerEntry` family is declared
  in node-free `types.ts` (the frontend shares it) and re-exported here.
- `retiredServers.ts` — leaf id list; `userSettings` strips their stale toggles
  (else a leftover `context7: true` would enable a custom server reusing it).
- `registry.ts` — resolver facade (import from here) over the pure
  `resolveEntries.ts`, `harnessResolvers.ts` (`shapeOrSkip`),
  `resolverPolicy.ts`; `taskWorktreeScope.ts` for the scope above.
- `claude`/`codex`/`piServerConfig.ts` — pure entry shapers.
- `claudeInject.ts` — IN the terminal-server fingerprint: never import policy
  here. `reconcileMcpServers` (marker `__latticeManagedMcp`; never touches the
  user's entries) + `platformizeCommand` (win32 `cmd /c` wrap of
  `WIN_SHIM_COMMANDS`; the SDK spawns shell-less, so bare `npx` ENOENTs).
  **Every wrapped arg goes through `escapeCmdArgument`** (raw `&`/`|`/`%VAR%`
  was command injection): carets doubled for a `.cmd`/`.bat` target (assumed
  when unresolved); unrepresentable args throw `UnsafeCmdArgumentError` and
  only THAT server is skipped. The line starts
  `set NoDefaultCurrentDirectoryInExePath=1&&` (else a repo-root `npx.cmd`
  runs) — in-line, not `env`, so absent `env` still inherits. Pinned against
  real cmd.exe in `mcp.inject.test.ts`.
- `settingsValidation.ts` — UNTRUSTED `mcpCustomServers`/`mcpBuiltinOverrides`:
  keep only resolver-read fields; overrides re-pin id/command/url, args
  additive-only. `overrideSecurity.ts`: a flag pointing at a binary/config
  (`--executable-path`, `--chrome-arg`, Playwright `--config`, …) rejects the
  whole override; env denylist (`NODE_OPTIONS`, `LD_PRELOAD`, `PATH`,
  installer/interpreter vars, CA/proxy vars that could MITM the fetch).
- `secrets.ts` — I/O + redaction. `__proto__`/`constructor`/`prototype` ids
  and names are refused on write, dropped on read (they reached
  `Object.prototype`).
- `validators.ts` (`POST /api/mcp/validate`), `importConfigs.ts` + `import/`.
- Storage: definitions/overrides in `globalSettings.json`; the per-project
  switches above in `<project>/.lattice/userSettings.json`, read at spawn.

## Injection sites — resolve in the backend, apply in the terminal-server

The detached terminal-server **never imports the resolver**: its files are
fingerprinted, so policy there would make every policy edit force a respawn
that **kills every running agent** (or run stale). `claudeTrust.ts` imports
only `claudeInject.ts` and IS fingerprinted, so mechanism changes still apply.

- **Per-spawn** — `proxyCreateSession` resolves `resolveManagedClaudeServers(
  projectPath, {isQaRun})` + `isClaudeMemoryDisabled` for every spawn (only the
  QA-run spawn passes `isQaRun: true`); ephemeral cwds get throw-away entries.
- **Project-root reconcile** — `POST /api/project-instrumentation`
  (`projectClaude/reconcile.ts`, on project open + settings save) writes
  `projects[<projectRoot>]` with `isQaRun: false` — the one place Lattice
  writes the user's canonical entry, so global servers reach a hand-started
  `claude` at the root (Claude keys by cwd). It snapshots `process.execPath` +
  the server path: a node upgrade or moved checkout leaves a dead `lattice`
  until the next open/save. Accepted — a boot-time reconcile would rewrite
  `~/.claude.json` for hundreds of stale projects.
- `seedClaudeTrust(dir)` is trust-only (`managed: null`), so it never strips
  MCP a later call added.

## Adding a built-in server

Add to `BUILTIN_MCP_SERVERS`; a required key → `requiresSecret` (+ a
`validators.ts` case if testable). **Do not set `defaultEnabled`.**
`runtimeNote` is the only caveat the MCP tab renders: put out-of-band
prerequisites (`blender` needs Blender open with its addon; no headless mode)
and optional keys there. **Switch off phone-home telemetry in `env`**
(unattended parallel agents would report from every spawn): prefer the
server's env kill switch over in-app consent (blender-mcp's fails open) and
set every accepted variable name, so an upstream rename can't resume sending
(pinned in `mcp.harness.test.ts`).

Tests: `backend/src/__tests__/mcp.*.test.ts`, named after the concern.
