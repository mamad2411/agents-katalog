---
name: forgeax-view-cli
description: >-
  Operate View through its public API and CLI. Use when demonstrating or
  inspecting View, opening assets, controlling Play or cameras, selecting
  scene entities, or checking whether a request affects an open View page.
---

# ForgeaX View API and CLI

> [!IMPORTANT]
> The resident workspace API is authoritative. The browser and CLI are clients
> of the same owner; the CLI does not implement project, asset, scene, or camera
> behavior. Engine owns project and target execution. View owns workspace
> bindings, selection, and presentation requests.

Use public API/CLI operations for supported actions, including demonstrations.
Use browser tools to inspect the resulting UI and pixels, test pointer/keyboard
interaction, or operate presentation controls without a public operation. A
missing capability must be reported explicitly; clicking the UI does not prove
API/CLI coverage.

## Find the live contract

AI authoring, asset previews and captures stay on Engine CLI or the SDK command
client. Their operation receipts and images are visible in View's Operation
history without a second View call. Use `view.workspace.history.list/get/artifact.read`
to inspect that history through an admitted View project, or `engine.history.*`
without View. These reads never replay a command or start a game. Use the
presentation API below when the user actually wants to operate the View UI.

For "what is View showing now?", run
`forgeax view workspace presentation get --root <backend-root> --input '{}' --json`.
It returns actual pages, active page, native panel visibility, appearance and
the exact document's workspace summary. Use returned page/panel IDs with
`presentation.page.open`, `.select`, `.close` and `presentation.panel.reveal`.
These relative IDs have the public `view.workspace.` prefix. With multiple
documents, read `view.workspace.pages.list` and pass `connectionId`; frontend
callers can address only themselves. A failed or timed-out write may have
applied: query current state and never replay it automatically.

Discover the running owner's declarations with
`forgeax help view --root <backend-root> --tree --json`.

| Surface | Example | Naming authority |
|:--|:--|:--|
| Public ToolApi ID | `view.workspace.asset.open` | View owner descriptor |
| Unified CLI | `forgeax view workspace asset open --root <backend-root> --input '<args>' --json` | Dots in the public ID become command segments |
| Workspace client / generic call | `asset.open` | Relative to the already selected View workspace service |
| Engine domain operation | `engine.asset.open` | Engine owner; View delegates execution |

Use the fully qualified ID in public inventories and the unified CLI in normal
examples. Relative IDs are arguments to `view workspace call --operation` or
`connectViewWorkspace(...).call`, not global API names. Owner operations such as
`view.display.bind` retain their descriptor prefix; derive names from live help
rather than adding `workspace` mechanically. The backend discovers descriptors
without mounting new plugins.

Read `@forgeax/view/workspace/contract` for operation names and request shape
(`packages/view-workspace-core/src/contract.ts` in this repository). For
programmatic clients, call
`connectViewWorkspace(...).capabilities()` to see what the connected owner can
execute. The contract's operation list alone does not prove that a provider is
installed and callable. Use `view.workspace.tabs.get` for the current project,
tab, and exact target identities. For domain reads such as
`view.workspace.assets.list`, pass both `projectId` and the returned project
`targetId`: a page-less caller has its own Engine runtime and `projectId` alone
does not select the browser's project. Obtain asset GUIDs from that result. Keep the returned
`projectId`, `targetId`, and `targetGeneration` with subsequent requests instead
of guessing from paths, names, or a previous target.

| Need | Owner and entry |
|:--|:--|
| Backend or optional View lifecycle | `forgeax backend ...` and `forgeax view start\|status\|stop`; use [View startup](../forgeax-view-start/SKILL.md) |
| Allocate a project on the running View | `forgeax view project open --root <backend-root> --project <project-root> --json`; open the returned headed URL |
| Call one resident workspace operation through Engine CLI | `forgeax view workspace call --root <backend-root> --operation <id> --args <json> --json`; requires the selected View host Pack and running View owner |
| Call the resident View workspace API | `forgeax-view workspace --operation <id> --args <json>` with the issued endpoint and token |
| List pages and reveal a Pack | `forgeax view workspace call --operation pages.list --args '{}' --json`, then `--operation pack.reveal --args '{"projectId":"...","sourcePath":"assets/example.pack.ts","revision":"...","connectionId":"..."}' --json` |
| Author assets or control an independent AI run | Engine CLI; use the installed `forgeax-engine-cli` skill when available |

`forgeax help view --tree --json` discovers declarations from the running
backend's selected host Pack. A listed command does not prove its plugin
is mounted or its provider is callable. The `forgeax-view workspace --help`
operation list describes its client grammar; an unavailable operation fails at
the connected owner. The workspace CLI accepts `--endpoint` and `--token`, or
`FORGEAX_VIEW_WORKSPACE_ENDPOINT` and `FORGEAX_VIEW_WORKSPACE_TOKEN`. Treat
these credentials as connection secrets; do not paste them into reports.
The resident View registers `view.workspace.*` on ToolApi; the frontend
transport and both CLI entries reach the same View owner. The Engine CLI
entry uses the backend's existing authentication. Select the package host
with `backend start --host-pack`; a downloaded View package alone
does not make this command discoverable.
`pages.list` exposes a bounded page inventory; `pack.reveal` waits for the
addressed frontend to show the Pack. With multiple pages, select the exact
`connectionId`; a stale page or source revision returns a non-action result.

## Open an asset through the API

With one Scene page connected, read its identities, list its exact target's
assets, then open a returned GUID. Scene, mesh, material and texture opens use
the same operation as Content Browser double click:

```sh
forgeax view workspace tabs get --root <backend-root> --input '{}' --json
forgeax view workspace assets list --root <backend-root> \
  --input '{"projectId":"<project-id>","targetId":"<project-target-id>"}' --json
forgeax view workspace asset open --root <backend-root> \
  --input '{"projectId":"<project-id>","targetId":"<project-target-id>","guid":"<asset-guid>","tabId":"forgeax-user-workspace"}' --json
```

After success, read `tabs.get` again and check its `openRequest` and Scene
target. If an already connected frontend has the scene PageType, it observes
the new request and focuses the Scene page. A frontend that connects later
baselines the retained request; the CLI response alone does not prove a page
is visible or that a rendered frame exists. Verify the browser and target when
the requested outcome is visual. `view.workspace.tabs.select` selects the
Scene or Runtime capture binding; resource-page placement remains frontend
policy. With multiple connected pages, page operations fail with
`view-page-ambiguous`; do not guess a page or reuse another target's identities.

Use `scene.select`, `scene.pick`, or `scene.clear` for View selection; direct
Engine `target.pick` only returns query facts. `presentation.*` reads and operates
the Shell's actual pages independently of runtime bindings. Content Browser
filters remain local UI policy. Keep multi-call camera transactions on one client
connection with `--batch`; a single CLI call closes its connection after the
API response.
