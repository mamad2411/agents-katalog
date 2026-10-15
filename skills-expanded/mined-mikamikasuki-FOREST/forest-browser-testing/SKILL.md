---
name: forest-browser-testing
description: "Verify FOREST frontend behavior in a browser using isolated data, targeted Playwright regressions and actual API/worker smoke checks. Use for interaction, route, responsive, draft, freshness or functional-integration changes."
---

# FOREST browser testing

Verify the user-visible result and the underlying saved state. A screenshot, mocked success response
or queued task is insufficient to establish end-to-end operation or scientific validity.
Paths below are relative to the FOREST repository root. Choose checks proportional to the change.

## Read the right reference

Read [references/repository-map.md](references/repository-map.md) when selecting existing tests,
interpreting their mocks or locating test configuration and script side effects.
Read [references/runtime-verification.md](references/runtime-verification.md) before starting a
server, running tests against a backend, preparing browser evidence or reproducing async failures.
These references were source-audited at `ff16c3f656f94d053d1bba65c6b3a07a5feaccde`;
they do not claim that the current browser or environment has been exercised.
Inspect the current test body and installed runtime before executing a copied command.

## Keep test state isolated

Playwright has no `webServer`; start the intended services explicitly and wait for `/api/health`.
Its default URL is `http://127.0.0.1:5173`; override with `FOREST_WEB_URL` for isolated production runs.
Use a fresh disposable `FOREST_DATA_DIR` and explicit `FOREST_DATABASE_URL` together.
`--data-dir` alone does not replace an inherited database URL. API settings also load repository `.env`.
Set `FOREST_MODEL=''` for provider-free local checks; a fresh DB then avoids startup Ollama seeding.
Do not run mutation or cleanup tests against the user's durable server, project directory or providers.
Pass the same `FOREST_DATA_DIR` to the test process for specs that inspect worker-created files.
Ensure the chosen port is available; never terminate an unrelated listener to make it available.
Keep the normal worker for run-lifecycle smoke. API-only or route-mocked checks cannot verify execution.

## Separate evidence levels

- **Source-confirmed:** identified in code, with the relevant source and suspected observable effect.
- **Browser-reproduced:** observed in an actual browser with steps, URL, state and result recorded.
- **Mocked UI regression:** fixture/fault responses prove presentation or interaction handling only.
- **Real API persistence:** verify saved state through ordinary API requests and after browser reload.
- **Real worker smoke:** observe an actual task through running and terminal states, logs and artifacts.
- **Scientific measurement:** independently verified outputs with provenance and appropriate evaluation.

Classify each check honestly; one spec can contain more than one evidence level.
Fixtures may deliberately carry plausible metrics. Never present these as newly measured results.
Past screenshots, filenames, CI workflow declarations and existing assertions are not evidence that
this session passed a check. Record command exit status and actual observed results separately.

## Select meaningful checks

Use `npm --prefix apps/web run build` to check TypeScript/build integration.
Use `npm --prefix apps/web test -- <src/test-file>` for the affected helper/component contract.
Run targeted browser files or `--grep` scenarios for the changed behavior and critical nearby state.
There is no npm `lint` or `typecheck` script. `scripts/test.sh` runs backend, build and Vitest, not e2e.
Do not require every browser case for every small edit; broaden testing when scope, failures or
unresolved integration risk justify it. Use a broader suite for cross-route/state architecture changes.

For real integration, prefer an isolated production build with API and normal worker on one URL.
`progress.spec.ts` includes a genuine local process success/failure and scoped source-navigation smoke.
Its second case delays a fetched real response. `storage-cleanup-retention.spec.ts` uses mocked settings
and checks controls; it never executes cleanup. The CI browser job includes both kinds.
Inspect `workspace.spec.ts` carefully: it mixes real API files/graphs/processes and fabricated responses.

For full redesign acceptance, also follow the provider-free numerical artifact journey in the runtime
reference. The sleep success/failure smoke above checks execution plumbing; it does not produce the
measured artifact, export/reload provenance, or paper evidence needed by that larger journey.

## Observe the behavior, not only the layout

Start from a clean project/context and record complete project, node, branch and run IDs where relevant.
Use accessible names and scoped regions for interactions; CSS selectors are appropriate for graph cards,
editor integration and geometry checks when accessible controls do not expose the needed observable.
Wait for a concrete response/state transition, not an arbitrary delay or a toast alone.
For mutations, inspect response status/body and refetch saved state; reload to confirm persistence.
For runs, distinguish queued acceptance from running/terminal observation, error/exit and artifacts.
For draft protection, type a distinctive unsaved value and verify it survives the triggering refresh,
preview, source inspection or conflict. Verify saved server content separately from the editor text.

Test keyboard focus, modal close/restore, disabled controls during pending requests and repeat clicks
when the change affects them. Exercise real error/retry or a clearly labelled fault-injection case.
For async changes, delay A, switch to B, release A, and confirm B's identity and draft remain current.
Exercise A → B → A for file selection because a path comparison alone does not reject the oldest read.
Collect page errors and unexpected API failures; inspect a legitimate expected error rather than
calling all non-2xx responses a regression. Preserve failure artifacts for diagnosis.

## Responsive and graph navigation

Check desktop, a width around the 820px inspector boundary, and 390px where the changed UI is relevant.
Test initial narrow navigation and resizing from desktop; they exercise different state paths.
Verify required entry points are reachable, text/controls remain usable, focus stays visible and
unintended document overflow is absent. Intended editor/table/canvas scrolling is allowed.
For the narrow inspector, confirm overlay geometry, close-button reachability, dismissal and return
to the selected canvas node. Do not treat a non-overflow screenshot as complete mobile acceptance.
For node search, inspect the requested ID/title, viewport visibility and filtered/collapsed/offscreen
cases as relevant; navigation should leave graph revision and durable positions unchanged.

## Known candidates require fresh confirmation

Source shows Escape clears Workspace selected ID but the auto-selection effect immediately selects
the first node. Source shows Overview reloads project budget/mode into local drafts without a dirty guard.
Source shows branch and run selections are local; no run route or branch/run query synchronization exists.
InterventionPanel emits those unsupported links; materialization's `run_id` field actually carries
a branch ID in backend code. Test link behavior without assuming an ID-type defect from the field name.
At ≤620px node search hides; settings/footer links also hide in the icon sidebar at ≤820px.
Record these as source-confirmed candidates until browser steps demonstrate the actual user impact.
Do not report a candidate as fixed unless the intended behavior is agreed by task scope and verified.

## Close with an auditable result

Report changed behavior, the targeted checks actually run, real versus mocked coverage, and material
untested paths. Include screenshots/trace/log paths when they clarify an observed result or failure.
Stop only the supervisor started for this check; keep its isolated data/logs until diagnosis is complete.
Delete disposable test data only when its identity is certain and no evidence still needs retention.
Do not launch paid/demo/soak qualification or install a background service as an incidental UI check.
