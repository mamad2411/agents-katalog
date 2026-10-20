# Daemon Ops Module

This directory owns the `daemon-ops` repo module — the operator-facing CLI and supervisor
surface around the daemon runtime. It also owns the daemon-facing CLI commands.

- Keep this module focused on operator control: daemon status, lifecycle,
  service installation, live event inspection, session inspection, and a
  concise operational snapshot.
- Service integration should stay user-level and directory-scoped. Do not require elevated
  privileges or create global machine state.
- Exact command names, flags, output fields, service-unit contents, and restart constants
  belong in the command implementation and tests, not docs catalogs.
- The daemon runtime itself lives in core; this module wires it into the CLI and supervisor surface.
- Daemon status exposes loaded and canonical runtime revisions and retains failed
  activation targets when the child cannot start. A supervised restart does not
  rebuild an installed binary. Failed activation parks the supervisor, including
  after service relaunch. Changed executable code or an explicit
  `daemon start --retry-activation` after a successful project readiness probe
  permits another attempt. Documentation-only changes and ordinary service
  restarts do not unlock a failed target. Explicit retry retains the prior
  diagnostic until startup establishes readiness.
  The supervisor holds the instance reservation across child replacements and
  parking; children authenticate the parent reservation and publish their own
  control identity. Only the reservation owner expires prior activation readiness
  before spawn and records preflight failures. Rejected duplicate starts leave
  the live owner's activation state intact. Intentional supervisor shutdown
  cancels replacement, releases the reservation after child exit, and does not
  mark the activation failed or prevent retrying the same runtime.
- The `/ui/surfaces` route and `ui` client delegate to one live assembler. This module contributes
  status, scope, inbox, and continuity; capability modules own their sources. Never register demo/fixture surfaces in production.
- Session autonomy mode is part of that operator surface. This module owns the
  `kota session` CLI plus the `sessions` `KotaClient` namespace
  (`client.sessions.list()` / `client.sessions.runOneShot()` /
  `client.sessions.setAutonomyMode()`) end-to-end. Command modules that need a
  short agent judgment use `runOneShot`; they never call the runtime-only
  `ModuleContext.createSession()` capability. Autonomous command judgments
  opt into its scope backoff mode so daemon-side admission, provider failure,
  and successful-empty handling share the selected workflow runtime's authority.
  Both the local-side handler (`sessionsLocalClient`) and the daemon-side
  handler (`buildSessionsDaemonHandler` in `daemon-client-handlers.ts`, contributed through the
  `daemonClient(link)` factory) realize the contract declared in `client.ts`.
  Validate mode values before issuing the HTTP call. Do not embed mode-change
  flow into any other subcommand (e.g. approval resolution) — mode is a
  session-level control.
- Local lifecycle operations authenticate the published control identity and
  confirm its pid before signaling. Both client arms stop the supervised child
  and wait for exit. Resolve an explicit target scope after command parsing,
  before selecting its control file or transport.

## Directory Scopes

Project dependency setup uses `workflow.preparation` in the selected scope's
trusted `.kota/config.json`. Supply `inputs` (manifest, lockfile and setup policy),
`outputs` (ignored, self-contained top-level dependency directories), a
`checkCommand` argv that rejects stale or unusable installations, and a `command`
argv that installs frozen resolutions. Setup runs in the shared sandbox and may
write only those outputs and run scratch. Egress is disabled unless the operator
explicitly configures `allowedEgressHosts`. Lifecycle-script and supply-chain
decisions remain with the project package manager policy.

For a standalone KOTA source checkout, use `["node", "scripts/check-dependencies.mjs"]` as the check and
pnpm install with `--frozen-lockfile --ignore-scripts --store-dir node_modules/.store`
as the command, keeping its writable cache inside the declared output. Include
`package.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml`, and the readiness script
as inputs and
`node_modules` as the output. Add `--offline` when the run package cache is
prepared; otherwise authorize the required registry hosts explicitly. A missing
native binding is a setup failure: copied pnpm installations can be recreated
when store locations change, so copying does not establish native-build readiness.
Prepare the reviewed native build under the
existing pnpm policy. Agents never receive write access to host packages.

Readiness is rechecked after rebase and recovery; only missing readiness invokes
installation. Publication stages validated, relocatable outputs, drains current
blocking workers, and replaces dependencies before exposing the new source
graph. Failed setup retains the same run for ordinary workflow retry. The
existing integration journal owns interrupted output replacement; do not edit
daemon state or discard the retained writer to retry preparation. Source and
installed CLI launchers recover interrupted dependency replacement before loading
the package graph, using the same SQLite integration journal. Source launch uses
Node's native type stripping before registering tsx; use the maintained `pnpm kota`
entrypoint so an early tsx preload cannot strand recovery. Recovery refuses to
change dependency files owned by a live daemon or publisher. Early recovery reads
only the executing installation’s own `.kota` journal and preparation configuration
(with the normal global preparation fallback); command scope selection never
grants authority over the installation. Journals owned by another host remain
with that host’s normal runtime recovery. Output renames require current trusted
preparation permission and ignored, untracked directories.

Scope is the core abstraction. The `kota scope` operator command and
`?scopeId=` selector address directory-backed scopes through the same owner.
Do not reinvent selection per command.

- Reads come through `client.scopes.list()`. The daemon's `/scopes`
  route returns the registry projection plus the operator-selected
  `activeScopeId` (or `null` when no selection is in force) in a single
  round trip. Other CLIs that need to render a scope selector consume
  this same shape; do not call `getScopeRegistryProjection()` and
  `/scopes/active` separately just to splice them client-side.
- Selection writes come through `client.scopes.use(id | null)`. The daemon
  persists the selection in-memory only — restarting the daemon clears
  the selection back to the registry default — and routes that take
  `?scopeId=` use the active selection when the parameter is omitted.
  `kota scope select` is the canonical entry point; `null` clears the
  selection, an unknown id surfaces `not_found`.
- Per-command `--scope <id>` flags override the active selection for
  one call. `daemon-ops` subcommands (`status`, `session`, `events`)
  pass the flag through as `?scopeId=<id>` and otherwise leave the
  query parameter unset so the daemon resolves to the active selection.
  Cross-scope operations are an explicit opt-in (e.g.
  `events tail --all-scopes`) — never the default. New operator
  surfaces should follow the same shape rather than introducing a
  parallel "all scopes" or per-scope flag set.
- External folders enter through the same `client.scopes` onboarding
  operations used by the shared `ui.surface.v1` graph. `kota scope inspect`,
  `configure`, `add`, `status`, `retry`, and `cancel` are terminal renderings
  of that contract. `drain` closes admission before `remove` stops hosting;
  removal never deletes the directory.
- Single-scope setups never render a selector. The presence threshold
  in `daemon-ops` views (e.g. the `Active scope` line in `kota
  status`) is "registry hosts more than one scope," so KOTA-on-itself
  remains a one-line experience.

## Presentation Boundaries

- The dashboard owns visual layout. The daemon core must not draw decorative
  rules, frames, or aligned columns in its log output. Anything emitted via
  `DaemonLogger` shows up inside the dashboard's activity section, so a
  `────` rule from core would render as a second nested frame.
- The daemon core emits a single concise readiness line on startup
  (`Daemon ready (pid …): N workflows, M scheduled items, poll Xs`).
  Static counts already in the dashboard snapshot (workflow count, pid,
  uptime) belong in the snapshot, not in repeated startup log lines.
- Stat grids must compute column widths from the widest entry in each column
  with at least two spaces of gap between value and the next label. Fixed
  `padEnd(N)` is forbidden for stat values, since cost/count growth silently
  collides values with the next label.
- Status block and streaming activity must be visibly separated. The dashboard
  draws a single `Activity ─────` heading rule before the captured log buffer;
  the static block above it has no horizontal rules of its own. The rule uses
  the rendering module's `sectionRule` primitive so it fills the terminal
  width instead of clipping to a fixed column count.
- On a TTY the dashboard refreshes the alternate-screen buffer; non-TTY keeps
  normal output. Task counts use a non-overlapping cached worker projection,
  joining repository intent with canonical runtime ownership through repo-tasks
  work supply. Missing ownership evidence displays unknown availability.
  Stderr bursts schedule at most one pending frame.
- The `Work` section only renders when the task queue carries actionable
  signal. Zero-valued states (`Doing 0`, `Backlog 0`, etc.) are filtered out
  of the counts row and a fully-zero queue suppresses the section entirely,
  so the heading never introduces a row that looks blank.

Color marks state changes; counts and labels stay plain so terminal width
calculation and non-TTY output remain reliable.
