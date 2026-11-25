---
name: forest-frontend-architecture
description: "Implement or redesign FOREST's React frontend against its existing projects, research graph, run, file, evidence and manuscript APIs. Use for route, component, state or API integration changes in this repository."
---

# FOREST frontend architecture

Make the requested interface work with the existing research product. Preserve durable identities,
revision guards and user drafts while improving the screen or interaction the user requested.
Paths below are relative to the FOREST repository root; verify the current source before editing.

## Read only the relevant implementation

Read [references/repository-map.md](references/repository-map.md) when locating an unfamiliar
route, state owner, adapter or refresh mechanism. It records a source audit at commit
`ff16c3f656f94d053d1bba65c6b3a07a5feaccde`, not a browser acceptance result.
For an API-facing feature, also read the applicable section of `docs/FRONTEND_API_GUIDE.md`
and the operation in `packages/contracts/api.generated.ts` or `packages/contracts/openapi.json`.
Check the corresponding `services/api/` handler when semantics are unclear or differ from copy.
Read the relevant component and its callers instead of loading every page and contract at once.

## Choose the existing owner

- `App.tsx` owns application preferences, navigation, the project shell and overview/controller UI.
- `Workspace.tsx` owns React Flow, graph commands, node editing, branch filtering and the run dock.
- `pages.tsx` owns library, ideas, theory, experiments, analysis, figures, paper, files and settings.
- `ui.tsx` supplies `UIContext`, `useLoad`, controls, modal focus behavior and error presentation.
- Evidence, interventions and progress have separate components; reuse their server interpretation.

Extract a focused module when it improves a substantial change. Avoid a parallel shell or duplicate
API cache that leaves original screens with conflicting project/run/graph state.
Keep `t(zh, en)`, accessible names and existing light/dark tokens consistent across new controls.
Reuse Monaco, the existing PDF viewer, terminal adapter and React Flow integration where applicable.

## Routes and identity

The current routes include `/projects`, `/settings`, `/share/:token` and
`/projects/:id/{overview,workspace,library,ideas,theory,experiments,data,figures,paper,files}`.
`/projects/:id` redirects to overview; unknown paths redirect to projects.
There is currently no dedicated `/runs/:runId` or project run-detail frontend route.
Workspace branch selection starts at `all`; the run dock selects locally and falls back to `runs[0]`.
Do not claim `?branch=...` or `?run=...` deep links work without implementing and verifying them.
InterventionPanel already emits `/projects/:id/runs?run=...` and Workspace branch-query links;
these do not match the current route/query consumers. Inspect effect action semantics before fixing IDs.
Use the complete run ID for operations; shortened IDs are display labels only.
`Files` source links use `?source=<encoded JSON>` with the scoped source identity, including
`segment_id` when needed; retain project/run/branch and file generation distinctions.
Preserve `demo=1` through `demoLink` when extending guided-demo navigation.

## API and mutation semantics

Prefer `requestApi()` in `apiClient.ts` for new JSON operations. It delegates to `api.ts`,
which prefixes `/api`, handles JSON/FormData, returns direct response bodies and raises `ApiError`.
Do not add an assumed `{ data: ... }` envelope, automatic mutation retries or another auth store.
HTTP 204 produces `undefined`; nullable run fields and extensible JSON configuration are real.
Keep download blobs, EventSource and terminal WebSockets on their existing separate transports.
Handle structured errors and authentication events in the existing UI flow.

For graph writes, send the actual `expected_revision`, command scope and a `request_id`.
Keep one request identity for the same pending operation; a new identity means a new action.
Use the server's returned graph/revision after acceptance. Do not manufacture revisions or infer
successful execution from a queued response, a toast, a model connection or an optimistic badge.
Use preview/impact/intervention flows for changes whose effects need review in the product.
Resolve conflicts against current content while retaining the user's draft; silently refreshing
the expected revision and resubmitting can overwrite another editor's change.
Maintain the Workspace mutation queue and pending position flush behavior across project switches.
Preserve unknown config fields when changing execution, resource, budget or provider settings.

## Refresh and draft ownership

`subscribeProject()` shares one SSE stream per project and coalesces updates; `ProjectShell`
refreshes project/runs and dispatches `forest-refresh`. Use these existing refresh points.
`useLoad` checks path and request generation, coalesces overlapping reloads and ignores old replies.
Keep equivalent identity/generation checks in custom reads: project switch, run switch, file switch,
preview toggle, and returning A → B → A can each make an earlier response stale.
`RunPanel`, `RunEvidence`, `SourceExplorer` and `useProgress` have their own cleanup/live guards.
Progress additionally rejects older generations within one epoch and checks snapshot project ID.

Treat server snapshots and editable drafts as distinct state. An SSE reload must not erase
unsaved instructions, CSV/text, figure, manuscript, budget or provider edits.
For manuscript side-panel/full-page transitions, preserve the complete editing session through
hide/expand/unmount: source, BibTeX, template/layout, revision instruction, base revision and dirty
flags. Current paper sessionStorage covers source/BibTeX/revision, not every draft field; sharing
only the server document or restoring those three fields does not protect layout/instruction edits.
Node instruction drafts and file drafts already have scoped sessionStorage keys; retain them.
Files use both selection generations and read/draft guards; a matching path alone is insufficient.
Preserve saved revision and conflict handling on deletion, rename and recreation of files.
Use stable selected IDs for figure/run lists; reordering must not replace a dirty editor.

## Navigation, keyboard and responsive work

Account for React Flow virtualization: an offscreen node may have no measured DOM card.
Search currently reveals hidden nodes, expands ancestors, opens the inspector and centers by stored
position. Keep filtering/selection separate from durable graph edits; navigation must not change revision.
At widths ≤820px the inspector initially closes and opens as a dismissible overlay.
Verify both initial narrow load and resizing an already-open desktop session; initial matchMedia state
does not by itself subscribe to viewport changes. Check actual CSS cascade for the requested width.
At ≤620px the sidebar is an icon rail and some search/settings entry points are hidden.
Provide a usable route to required actions when changing these layouts; overflow checks alone are insufficient.
Preserve modal focus trapping/restoration, tab keyboard behavior and editor shortcut exclusions.

## Source-confirmed candidates, not established runtime failures

At the audited revision, Escape clears Workspace selection, while an effect selects the first node
whenever selection is empty. Verify the intended dismissal behavior in the browser before fixing it.
Overview unconditionally resets budget/mode drafts whenever the loaded project object changes;
test an unsaved edit during SSE refresh before reporting draft loss as a browser reproduction.
Missing run/branch URL synchronization and narrow hidden entry points are product candidates,
not automatically authorized feature requirements. Choose scope from the user's actual request.

## Verify the changed behavior

Run `npm --prefix apps/web run build` for TypeScript/build integration and relevant Vitest tests
with `npm --prefix apps/web test -- <src/test-file>`. There is no `lint` or `typecheck` npm script.
For route, interaction, async or responsive changes, use `forest-browser-testing` when available
and select browser scenarios that observe the changed behavior and its critical neighboring state.
For API contract changes, update schema/handler together and use the repository contract exporter/check.
Report only checks actually run, observable outcomes, and remaining material integration limits.
