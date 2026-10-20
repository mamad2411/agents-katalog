# E2E navigation

- [workflow-editor-drag.spec.ts](./workflow-editor-drag.spec.ts) intercepts all
  API and WebSocket traffic. Exercises click-to-append, real chip drags before,
  between and after steps, empty workflows, existing row reordering, rejected
  drops, and frost styling/editing/save/reload for all step kinds.

- [workflow-parallel.spec.ts](./workflow-parallel.spec.ts) creates a disposable
  workflow definition without launching harnesses. Checks toggle accessibility,
  action barriers, matching connector/icon color, frozen members, and save/reload.
  Its project cleanup is bounded to a direct child of `os.tmpdir()`.

- [workflow-queue.spec.ts](./workflow-queue.spec.ts) uses the **real backend**:
  it creates task/workflow records for a disposable, committed Git project in
  `<tmp>/lattice-playwright-queue-*` and selects it with sessionStorage's
  `lattice.activeFolder`. A task patched to `in_progress` holds a Merge-only
  workflow open without launching a coding harness. Patching it to `qa`
  releases the gate so the queued workflow can start; preserve this fixture
  when testing sequencing and the backend's `409 active-run-exists` guard.
  Never seed these fixtures into the user's active project.
- Queue teardown order matters: cancel active runs, delete the held task,
  delete workflow definitions, then allow the debounced stores to flush
  (currently 300 ms) before removing disk state. Cleanup removes only the
  project's hash directory directly under
  `<LATTICE_E2E_HOME>/.lattice/per-project/` and the fixture project directly
  under `os.tmpdir()`; preserve both parent-path guards. Finally,
  `GET /api/projects` prunes the missing project from the index. Do not wipe
  the whole E2E home: it persists across runs to retain the terminal-server
  auth token while an earlier executor may still be draining.
- [graph-stability.spec.ts](./graph-stability.spec.ts) intercepts all API and
  WebSocket traffic before navigation; its fixture graph never reaches a real
  backend. Keep response shapes complete (notably terminal restore's summary).
  Graph refs come from the mounted React hook tree, with `__testGraph` and
  counters injected by the test; do not add production debug globals to make
  them accessible. Measurements start after the idle gate settles, with faster
  fixture alpha decay for software WebGL. Preserve the structural-addition
  positive control alongside checks that metric bursts, identical rescans and
  overlay toggles leave the layout stable.

[../playwright.config.ts](../playwright.config.ts) owns one-worker Chromium
execution (`fullyParallel: false`) and the default isolated servers, even for
the mocked graph suite. It requires a current, prebuilt `backend/dist/index.js`;
it does not build the backend. Backend/frontend/executor use distinct ports
`5384`/`5383`/`5385`; child `HOME` and `USERPROFILE` point at
`<tmp>/lattice-e2e-home`, with `default-project` inside it so first-open hooks
cannot instrument the checkout. Vite uses `frontend/node_modules/.vite-e2e`.
`reuseExistingServer: false` deliberately makes port collisions fail. Never
start, stop or restart the user's dev server to resolve them.

See the [root README](../README.md#tests) for environment-override guidance and
the config for the complete port/env wiring. `LATTICE_E2E_BASE_URL` skips the
managed servers **and their isolation setup**. The graph and editor-drag specs
intercept all API traffic and can target an isolated Vite instance; the queue
spec (tasks and workflows) and the parallel spec (a workflow definition, POSTed
then DELETEd) still write real backend records. Queue cleanup uses
`LATTICE_E2E_HOME`, falling back to `os.homedir()` when unset, so an external
target's state home must match. Live ports `5183`/`5184` require
`LATTICE_E2E_ALLOW_LIVE=1`; that opt-in does not provide isolation.

Reference commands from the repo root (task agents leave execution to the
workflow's Run tests step):

```sh
npm --prefix backend run build
npm run test:e2e
npm run test:e2e -- e2e/<spec>.spec.ts
```

Replace `<spec>` with `graph-stability`, `workflow-editor-drag`,
`workflow-parallel` or `workflow-queue`. For unit tests and package validation,
use the [backend](../backend/CLAUDE.md#validation) and
[frontend](../frontend/CLAUDE.md#validation) command guides. Their type-check
forms, each starting from the repo root, are `cd backend && npx tsc --noEmit`
and `cd frontend && npx tsc -b`.
