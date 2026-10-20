# Commands Module

This module owns the user-facing slash-command catalog that chat clients render
as an autocomplete palette.

## Source Of Truth

The catalog is derived, not registered. There is no per-command registration
surface.

- A workflow appears in the catalog when its definition includes the tag
  `command`. Any workflow without the tag stays internal — it remains
  triggerable through `/api/workflow/trigger`, but it does not surface in the
  palette.
- Every contributed skill is exposed as a `skill:<name>` command without
  additional opt-in. Skills are user-facing by construction.

The module builds the catalog from `ctx.getContributedWorkflows()` and
`ctx.getModuleSummaries()` so a single function feeds both the web server and
the daemon control server.

## Invocation Contract

A command invocation resolves to one of two actions:

- `workflow`: submits through the daemon's `workflow-dispatcher` provider.
  Definition validation, idempotent admission, logical resource ownership,
  project pause, and shared coordinator capacity apply exactly as they do for
  `/api/workflow/trigger`.
- `skill`: returns the skill's raw prompt body. The client pastes it into the
  chat composer; the user reviews and sends via the normal chat path. Skill
  commands do not bypass the session loop — they are preset messages.

Clients call:

- `GET /api/commands` or `GET /commands` to list the catalog.
- `POST /api/commands/invoke` or `POST /commands/invoke` with `{ name }` to
  resolve a command. The response either confirms a queued workflow or
  delivers the skill prompt.

## Surfaces

The module owns two parallel HTTP surfaces backed by the same catalog:

- Web routes (`KotaModule.routes`) under `/api/commands` and
  `/api/commands/invoke` for in-process clients.
- Daemon-control routes (`KotaModule.controlRoutes`) under `/commands` and
  `/commands/invoke` for the daemon control plane.

Both surfaces resolve through the `slash-command-catalog` provider the
module registers in `onLoad`. Route factories are side-effect-free and look up
the catalog through their owning context on each request; an unavailable or
withdrawn provider returns 503. No process-global catalog or reset lifecycle
competes with the host registry. Daemon-control invocation triggers workflow
runs through the `workflow-dispatcher` provider seam
(`#core/workflow/workflow-dispatcher-provider`), which the daemon registers
at startup. The handler looks the dispatcher up per request and returns 503
when the seam is unregistered, mirroring the catalog-unavailable path.

## Boundaries

- Keep the command shape small: name, label, optional description, source, and
  contributing module. No per-command UI DSL.
- Do not invent a parallel registry for user-invokable capabilities. If a
  capability needs to be reachable from the palette, the right move is to add
  the `command` tag to an existing workflow or contribute a skill.
- Clients query the daemon for the catalog; they do not read repo files.
- The daemon-control route handler must not import the `DaemonControlHandle`
  type; the workflow-dispatcher seam is the only authorized way to enqueue a
  workflow run from a module-contributed control route.
