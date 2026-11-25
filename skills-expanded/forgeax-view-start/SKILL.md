---
name: forgeax-view-start
description: >-
  Open or preview ForgeaX projects and assets in View with a published npm SDK
  or a local Engine checkout. Use for project/asset preview requests, View startup,
  local Engine binding, and failures before the interface opens.
---

# ForgeaX View startup

After startup, use [forgeax-view-cli](../forgeax-view-cli/SKILL.md) for View
actions and demonstrations. It owns API/CLI naming, capability discovery and
exact page/target arguments. Browser tools verify the resulting presentation.

## Select this workflow

A request to preview, inspect, open, or show a ForgeaX project or its assets
selects this skill. The same applies to an unqualified "preview" while working
on a ForgeaX project, including "make the game playable, then preview". Finish
requested development and the game guide's required checks before opening View.
For inspection alone, check project and asset readiness first. Use Engine game
execution when the user explicitly asks to play the running game. Questions
about View itself do not start services.

Project/asset preview is complete when the returned View URL is open in a browser
and the requested project and its assets are visible there. `project preview`,
a game runtime URL, a standalone asset image, and a connected but empty View
Shell do not establish that result. Use [forgeax-view-cli](../forgeax-view-cli/SKILL.md)
for asset and panel actions after startup.

## Published npm SDK

Use this path for an SDK installed from npm, including its expanded source
archive. Use the installed SDK's `bin/forgeax.mjs` for both Engine and View; the
local-checkout helper below needs Git provenance and is not the npm entry.
Keep the game's pinned Engine release and the installed View/SDK release matched.
Read the SDK and game `AGENTS.md` before changing or delivering the game. Published
Engine/View outputs are built already; do not rebuild them to inspect assets.

The Engine backend owns the workspace and loads View's `host.pack.json` at
`backend start`. That selected Host Pack contributes `forgeax view` commands to
the backend's command tree. The View package being installed is insufficient:
`help view` and `view status` may return `tool-command-not-found` before a
compatible backend is ready, or when called with another backend `--root`.
The same `--root` must select the backend for every later View command.

Run the sequence in one **persistent terminal session**, using the same SDK
CLI path, environment and `WORKSPACE_ROOT` throughout. Separate Node invocations
in that terminal are fine. A backend launched through a short-lived command
environment may end with it; keep the owning terminal alive while starting View,
opening the browser and handing it to the user. `GAME_ROOT` is the absolute
project directory. It may equal `WORKSPACE_ROOT`; choose a separate backend
workspace when the game already owns a host root.

1. Resolve View's Host Pack from the SDK CLI runtime, not from the SDK's bare
   `packages/view` directory. Set absolute `SDK_ROOT`, `WORKSPACE_ROOT` and
   `GAME_ROOT` in that persistent terminal.
2. Run `backend status` with `WORKSPACE_ROOT`. Reuse a ready backend only when
   its reported `hostPack` is the resolved View Pack. If stopped, start it with
   that Pack in the same terminal. Inspect ownership before changing an
   incompatible ready backend; do not silently stop another workflow.
3. Once backend status is ready, discover `help view`, check `view status`, then
   run `view start --project` with the absolute `GAME_ROOT`, always using the
   same CLI and `WORKSPACE_ROOT`.
4. Open the returned URL in a browser. Confirm the project name/path, an exact
   project target, and the requested assets in the Content Browser or asset
   pages. A ready service or URL alone is not visual acceptance. Keep the
   terminal alive through this check and handoff.

For POSIX shells, the commands in that one terminal are:

```sh
SDK_CLI="$SDK_ROOT/bin/forgeax.mjs"
VIEW_HOST_PACK="$(node -e '
  const { createRequire } = require("node:module");
  const { join } = require("node:path");
  const sdkRequire = createRequire(join(process.argv[1], ".forgeax/cli-runtime/package.json"));
  console.log(sdkRequire.resolve("@forgeax/view/host.pack.json"));
' "$SDK_ROOT")"

node "$SDK_CLI" backend status --root "$WORKSPACE_ROOT" --json
# Only if no compatible backend is ready:
node "$SDK_CLI" backend start --root "$WORKSPACE_ROOT" --host-pack "$VIEW_HOST_PACK" --json
# Only after backend readiness:
node "$SDK_CLI" help view --root "$WORKSPACE_ROOT" --tree --json
node "$SDK_CLI" view status --root "$WORKSPACE_ROOT" --json
node "$SDK_CLI" view start --root "$WORKSPACE_ROOT" --project "$GAME_ROOT" --json
```

For Windows, keep one interactive PowerShell or CMD session open. If an agent's
command tool creates a fresh shell for each call, open one persistent terminal
and send every subsequent command to that session. This PowerShell sequence
uses the same conditional `backend start` step:

```powershell
$SDK_ROOT = 'C:\absolute\path\to\forgeax-sdk'
$WORKSPACE_ROOT = 'C:\absolute\path\to\backend-workspace'
$GAME_ROOT = 'C:\absolute\path\to\game'
$SDK_CLI = Join-Path $SDK_ROOT 'bin/forgeax.mjs'
$VIEW_HOST_PACK = node -e 'const {createRequire}=require("node:module"); const {join}=require("node:path"); console.log(createRequire(join(process.argv[1], ".forgeax/cli-runtime/package.json")).resolve("@forgeax/view/host.pack.json"))' $SDK_ROOT

node $SDK_CLI backend status --root $WORKSPACE_ROOT --json
# Only if no compatible backend is ready:
node $SDK_CLI backend start --root $WORKSPACE_ROOT --host-pack $VIEW_HOST_PACK --json
# Only after backend readiness:
node $SDK_CLI help view --root $WORKSPACE_ROOT --tree --json
node $SDK_CLI view status --root $WORKSPACE_ROOT --json
node $SDK_CLI view start --root $WORKSPACE_ROOT --project $GAME_ROOT --json
```

On Windows, pass the absolute path as `--project` and use the CLI's returned
URL; do not build or re-encode a URL from the filesystem path. A missing View
command after backend readiness calls for checking that exact root's backend
status, selected `hostPack`, SDK CLI/runtime package resolution and backend logs.
Repair the failing stage and retry it; a game server is not a substitute for
the requested View preview.

## Local Engine checkout: one script

Use the fixed `tools/view` source in the selected Engine checkout. The helper installs from the shared workspace and calls Engine `build:tools`, which supplies the native diagnostic plugins. For a known game project, run:

```sh
node tools/view/skills/forgeax-view-start/scripts/start-view.mjs \
  --project /absolute/path/to/game \
  --engine /absolute/path/to/forgeax-engine
```

The script checks the package link and local Engine binding, builds stale
Engine/View outputs, prepares the shader profile, reuses or starts a managed
backend with View's `host.pack.json`, and calls `view start --project`. It
returns one JSON result on stdout. Read `url` from an `ok: true` result and
open it with the available browser tool. Then verify the requested project
name/content and a live Engine target in the browser. The URL alone proves
only that View is serving the project intent. The script does not launch a
browser, open Play, or control an independent AI run.

Use `--view` to name the selected Engine's `tools/view` directory explicitly, `--root` for a dedicated empty backend
workspace, `--restart` after a compatible host needs replacement, and
`--profile point-ssao` for a project that uses point shadows. `--build auto`
is the default; `--build always` rebuilds, and `--build never` requires fresh
outputs. The script refuses a conflicting package link, foreign backend, or
nonempty unmanaged workspace and reports the failing stage in JSON. Do not
silently replace those owners. Progress and command diagnostics go to stderr.

The manual composition below remains useful for a narrower service-only
request or diagnosis of a failed stage.

This helper uses Git provenance from contributor checkouts. For a public SDK or
its expanded source archive, follow [Published npm SDK](#published-npm-sdk).

Read [Start here](../../README.md#start-here) for the current commands and Pack
PluginAsset root. Check the selected Engine package's public exports and CLI help
before using a command.

## Interpret the requested outcome

Treat "use View to start this project" as a request to open that project in
View for editing. Compose the necessary steps in this skill; do not require the
user to request each service separately. Start Play or an independent AI run
only when the user requests that execution mode. A request for just a service
or URL ends at that narrower outcome.

| Step | Owner and boundary | Completion evidence |
|:--|:--|:--|
| Backend | Explicit Engine backend command; reuse a compatible owner or start a missing one | Backend responds with the requested Engine and host composition |
| View | View plugin command on that backend; never implicitly starts the backend | View returns its interface URL |
| Browser | Agent uses an available browser tool when the request includes opening the project | Returned URL is visited; low-level CLI commands do not launch a browser |
| Project | Existing workspace API, reached through the project-intent URL or explicit project.open | Requested project identity, content and exact Engine target are present |
| Play / AI run | Explicit Engine execution operation for the requested mode | Its own target or run readiness; separate from Scene readiness |

Use a documented convenience command when the installed CLI provides one;
otherwise compose the independent commands here. Check which services it starts,
whether it opens a browser/project, its reuse policy, and its completion result.
Do not assume a `forgeax view open` command exists. Command discovery/help must
not activate services. Follow the installed package's current root and
PluginAsset contract; design proposals are not available commands.

Keep API calls usable independently of CLI workflows. Convenience commands may
compose public APIs, while each underlying CLI command retains its documented
single-operation behavior. Do not duplicate domain validation or state in a
convenience wrapper, or make a low-level API silently perform the full workflow.

For a known project, carry its canonical path through the returned URL or
project.open request. Prefer the URL-intent path for an ordinary browser open;
use explicit project.open when allocation before navigation is required. Do not
issue both as independent allocations. Reuse an existing matching project and
URL; a different open project or incompatible backend requires resolving that
specific conflict, not silently switching or restarting it.

If no suitable browser tool or desktop is available, return the actual URL and
report that browser/project readiness remains unverified. A URL or allocated
target alone is not completion of a request to open the project. Preserve the
last successful stage and original failure; retry only the failed step after
checking current owner state. Do not replay editing, scene-open, or Play actions.

## Resolve the requested Engine

For a local repository request, follow
[Use a local Engine checkout](../../README.md#use-a-local-engine-checkout).
Inspect the current package link and `project engine status` first. Keep a
matching healthy binding; do not replace it with an SDK archive or rebuild it
merely to start View.

The package link selects the local CLI and Node-side Pack imports. The existing
`project engine use-local` binding selects local workspace exports for the
browser host. Verify `mode: "local"`, the requested checkout, the resolved built
entry, and `project engine check` before reporting the binding complete. Use
public built exports; do not redirect package exports or Vite aliases to `src`.
Resolve the actual `node_modules/@forgeax/engine` link from the project and
compare it with the checkout in `.forgeax/engine-binding.json`. Both sides must
select the same Engine revision. `project engine check` proves the browser
binding is healthy, but a different Node-side package link can still cook Pack
assets with stale component fields.

Build missing or changed outputs explicitly. After building a local Engine
checkout, prepare the shader profile used by the target and check both
`packages/vite-plugin-shader/dist/engine-inputs/<profile>/manifest.json` and
`imports.json` before starting a rendering target. The default profile is
`base-ssao`; use the matching point-shadow profile when that feature is enabled.
Recheck after rebuilding the shader package, since its `dist` output can replace
the prepared profile. A missing profile makes each fresh Backend compile Engine
shaders from source and can keep one CPU busy for minutes; a healthy package
build count alone does not establish rendering readiness. Report preparation
separately from backend/View startup. Do not pack a candidate SDK as a
substitute for the requested local repository binding.

## Compose only the requested operations

Inspect `backend status` for the chosen workspace root first; inspect
`view status` only after a compatible backend is ready. Reuse an existing
healthy service with the requested Engine. A binding change does not update
running owners; apply it with an explicit backend restart, and keep
independent runs under their separate lifecycle. Select the installed View
package's `host.pack.json` with `backend start --host-pack <absolute-pack-path>`.
The game needs no View asset or changed `roots.host`. If it already owns a host
root, use a separate backend workspace root and open the game with `--project`.
Perform the operations needed for the user's requested outcome:

| Request | Action and completion evidence |
|:--|:--|
| Start Engine backend | `backend start --host-pack <View package>/host.pack.json`; Engine API and the selected View plugin are ready |
| Start View | Connect to the backend with `view start`; return the actual URL |
| Open the interface | Open that URL in the user's browser; verify Shell connection if browser interaction is requested |
| Edit a project | Return the URL with the known project intent: backend root is the default project if it contains `forge.json`; `--project /absolute/project` overrides it. Verify project identity and Engine target after opening that URL |
| Explicitly allocate a project | `forgeax view project open --root <backend> --project /absolute/project --json`; open `projectTarget.url`, or let an already-open empty Shell adopt it. Command success alone does not prove the headed page is ready |
| Play in Scene | Start Play for the open project; use its exact target for shared tools |
| Observe an AI run | Bind its explicit `{root, runId}`; verify a timestamped image from that run |

For a complete View startup request, start a missing backend first, then enable
View. Stop after the requested outcome. The browser opens the known project from
the returned URL; Play and independent AI runs still require separate intent.
Browser automation setup belongs to an explicitly requested browser workflow,
not to `backend start` or `view start`.

`--root` selects the existing backend workspace. `view start` creates no
project target. Do not ask users to retype a known project path. Verify repeated
refresh carries the confirmed project and old target through the resident View
entry, then opens a fresh Scene only after Engine validates that exact lost
target. Verify no manual reconnect or resource/camera/layout history replay. Never
resend commands to the lost target or restart Play automatically. Report
conflicts with another active page and require an explicit project choice.
During the transfer, verify the resident View entry shows restoration progress
without target-bound panels or stale-target command errors. Measure the time to
the fresh target separately from the time to reach the resident entry.
When startup speed matters, start the Engine backend with
`FORGEAX_WORKSPACE_TIMING=1` and use the Engine checkout's
`node scripts/workspace-timing-report.mjs <backend-root>` after repeated opens or
refreshes. The report groups exact targets and separates Vite config, server
creation/listening, Catalog wait and browser readiness. Record the browser's
time to reach the resident View entry separately; the Engine timer starts when
the replacement target opens. Check the stage distribution before changing
startup behavior.
`view project open` takes the
project directory as `--project` and opens it on the running View; it
never launches a browser, starts Play, or switches away from a different open
project. Its JSON result only proves the headed session was allocated: open
`projectTarget.url`, or confirm the empty shell navigated there, before
treating the project as open in the interface.

When the user supplied a project path and asked to open it, use the project-intent
URL or `view project open` with that path; do not stop at the
connected Shell and do not type into the path dialog. `No project`, an empty path field, or a disabled **Open
project** button means the project-open step is incomplete. The final project
screenshot must contain the requested project target. Treat scene preview and
Play as independent follow-up gates: a scene tree proves scene loading, while a
running Play target plus real pixels proves game execution. During a slow Play
start, retain the pending state until Engine reports readiness; do not infer
failure from temporarily disabled controls.

For WebGPU pixel evidence, use the repository's canonical Playwright launch
configuration or the browser flags required by its real integration script. A
browser that merely exposes `navigator.gpu` can still leave the canvas black on
an unsuitable backend. Wait for the Engine document's submitted-frame marker,
then inspect the screenshot itself; `play.ready`, a mounted iframe, and a black
canvas are not pixel acceptance.

Use [status and stop](../../README.md#check-status-and-stop) for cleanup. Stop
only owned/requested resources; View stop preserves the backend and independent
runs, and borrowed browser resources remain with their caller.

## Preserve the failing boundary

| Evidence | Next action |
|:--|:--|
| Command missing | Check the same CLI and `--root`, confirm a ready backend with View's selected `hostPack`, then inspect installed View exports and package resolution |
| Pack module initialization timeout | Retain the source filename and diagnostic; inspect actual resolved imports before claiming whole-Engine compilation |
| Terminal Pack/catalog failure | Return the producer error; repair and explicitly reopen the project instead of adding another readiness wait |
| Shell ready, rendering failed | Report target failure separately; inspect Engine's original renderer error while keeping View available |
| Missing automation browser | Report that prerequisite only for the browser task; a View URL does not require Playwright |

Return the selected Engine entry, workspace root, service/URL state and the
verification boundary. Keep URL readiness, DOM interaction, real pixels and CI
results distinct. Update this guidance with README startup contract changes.
