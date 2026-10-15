---
name: httrack-cloner-skill
description: Use when an authorized website URL or HTTrack mirror must become an editable local React and TanStack Router project without automatic external runtime dependencies.
---

# HTTrack Cloner Skill

## Invocation Contract

When this Skill is supplied with a target URL, that is the complete command. Begin the URL-to-delivery workflow immediately. Do not ask what the user wants done with the URL, offer alternative tasks, request a work directory, or wait for additional implementation guidance.

Existing captures, invalid runs, experiments, or related projects do not make a bare-URL invocation ambiguous. Never ask whether to clone, review, fix, summarize, or reuse them. Ignore every sibling artifact and execute a fresh clone immediately.

### First Tool Calls

For a new URL, do not list, search, sort, inspect, or modify `clone-runs` first. No valid `RUN` exists yet. Install the bundled tools, then execute the Primary Command with the supplied URL. Assign `RUN` only from that command's `Fresh run:` stdout. Never infer it from a timestamp, directory name, latest sibling, or existing state file.

If any directory reports `stale-run-reuse-forbidden` or lacks schema-2 invocation provenance, abandon it without editing and immediately execute the new-URL Primary Command. Saying "the practical next step is to allocate a fresh run" is forbidden; allocate it now.

## Finish The Project

Do not stop at analysis or a repair report. Continue until the generated React project installs, builds, serves over local HTTP, and its preview is opened. `REPAIR_LOOP` means perform the listed repair and resume the same run.

### Mandatory Continuation

At every `REPAIR_LOOP`:

1. Read `.cloner/next-actions.json` and execute the first useful procedure now.
2. Fix the generated project, run a focused check, and resume the launcher.
3. Run `npm ci --prefix "$RUN/react"` when local test tools are absent; missing `tsc` or `node_modules` is setup work, not a blocker.
4. Never inspect, copy, compare, or cite a sibling run. Prior output is neither implementation input nor evidence.
5. Resume the exact launcher after every source change so artifact tracing and authoritative reports are refreshed.
6. Repeat until the project is delivered. Reports are guidance, not the product.

If `apply_patch` repeatedly fails on a large source replacement, do not stop. Prepare the complete candidate in a temporary file, then use the bundled restricted atomic writer:

```bash
node "$SKILL_DIR/scripts/atomic-replace.mjs" --run "$RUN" \
  --target "$RUN/react/src/pages/HomePage.tsx" --input /tmp/HomePage.tsx
```

The writer only permits `react/src/**` and selected React config files, rejects symlink targets and empty inputs, and replaces atomically. Run the focused test immediately afterward.

Before `COMPONENT_RECONSTRUCTION` can return a repair loop, the orchestrator generates `reports/bootstrap-contract.json` and, when a bootstrap candidate exists, `.cloner/decompiled/main.js`. A missing decompiled artifact is an orchestrator defect to repair and rerun immediately, never a reason to hand off the reconstruction.

## Objective

Run one continuous Agent workflow from URL to an editable React + TypeScript + TanStack Router project, a running local preview opened in the user's browser, and machine-readable parity evidence.

Keep the implementation path simple: capture the deployed files, locate and decompile the application bundle, move visible DOM and state into React, isolate only unavoidable canvas/WebGL internals, localize runtime dependencies, build, then repair from browser proof. Reports exist to point at work; they must not become a substitute for producing the project.

Prefer React ownership of visible DOM, state, forms, and page lifecycle. For a large production canvas/WebGL bundle, the first valid delivery may retain the sanitized captured runtime behind a local React adapter so the site remains functional and fully offline. Report that result as `React adapter`, not `React rewrite`; continue modular migration when deeper source ownership is required.

## Production-First Core Loop

Keep the execution model simple and continue until a runnable project exists:

1. HTTrack the deployed source and assets.
2. Unpack/decompile enough of the captured output to understand routes, bootstraps, and runtime assets.
3. Generate a React project with TanStack Router and preserve the captured UI/runtime locally.
4. Remove automatic source-site and third-party network dependencies.
5. Build, open the local preview, exercise the real page, and repair observed failures.

Static analysis is supporting evidence, not the product. Only missing TanStack routing, direct HTML/CSS assets, automatic external runtime requests, build failure, or an observed browser failure may stop delivery. Bundle-only asset guesses, provenance differences, architecture debt, and parser uncertainty are diagnostics and must not prevent a working preview.

Source/local parity differences and proof-tool failures block delivery until repaired. A buildable project is not a successful clone when the rendered structure, page height, visible media, navigation, or required interactions differ materially from the source.

When the browser requests a local JS, JSON, shader, worker, model, audio, or video path and receives the SPA HTML fallback, treat that as a real missing runtime asset. Recover the source bytes or remove the reachable request, then retry. Do not hide the failure with longer waits or fabricated empty files.

Dynamic asset discovery is best-effort during capture. Keep every successful download, record failed guesses in `dynamic-assets-report.json`, and continue reconstruction. Only browser-reachable missing assets become repair work; use strict dynamic capture only for an explicit audit.

Bound every dynamic fetch and proof wait. Video, event streams, and long-lived requests may prevent browser `networkidle` forever; after the bounded wait, continue with a short deterministic settle delay and inspect the rendered page.

HTTrack may save a 404 asset response under an `.html` filename. If that document identifies itself as Error/404 and its canonical route differs from the captured path, exclude it from React routes and remove references to it from generated HTML/CSS.

Remote literals, outbound links, and manifest-only unresolved references are diagnostics by default. Explicit automatic request sinks remain blocking. Use verifier `--strict` only when the user requests a static URL audit in addition to the runtime-offline guarantee.

Captured HTML files are route inputs, not public runtime assets. Do not copy secondary `.html` files into `public/`, because hard navigation would bypass React and execute the captured bootstrap again. Preserve their content in React routes and route aliases instead.

The generated project includes a lockfile, Vitest, jsdom, and Testing Library. Do not spend a repair cycle inventing a test toolchain or changing package versions unless clean reproduction proves the generated lockfile is invalid.

## Completion Contract

Delivery requires:

- TanStack Router owns the routes and React mounts every page.
- Captured UI, styles, media, fonts, scripts, shaders, workers, models, and other reachable assets resolve locally.
- Automatic source-site and third-party runtime requests are removed or replaced with local behavior.
- The project installs from its lockfile, typechecks, and builds.
- The important routes and interactions work in a local browser preview.
- The preview URL is opened for the user.

Proof, provenance, architecture, and migration reports are delivery evidence. Any failed authoritative proof, empty screenshot set, unexpected top-level navigation, or material source/local mismatch must enter `REPAIR_LOOP`. Do not claim a pure React rewrite when a captured runtime remains; call it a `React adapter` and keep the runtime local and sanitized.

## Self-Contained Rule

Execute this Skill directly. Do not invoke or depend on another Skill. Do not delegate capture, reconstruction, review, or proof to separate agents. Treat the sections below as SOP stages performed by the same Agent.

The bundled scripts and references are the complete execution surface. Direct command-line tools and locked package dependencies are allowed.

## Prerequisites

- Node.js 20 or newer
- npm
- HTTrack on `PATH`
- HTTP access to the source URL
- enough disk space for captured media, models, textures, and proof artifacts

Install the Skill's locked tools:

```bash
npm ci --prefix "$SKILL_DIR/scripts"
```

Set `SKILL_DIR` to this Skill directory.

## Run Layout

Use a dedicated run directory:

```text
RUN/
  mirror/
  react/
  proof/
  .cloner/
    state.json
    preview.json
    repair-history.json
    artifact-trace.json
    artifact-snapshot.json
    style-baseline.json
```

Never overlap input, output, Skill, home, repository root, or current working directory. Captured input containing symbolic links is rejected.

For a URL-only invocation, create a fresh `clone-runs/<host>-<timestamp>/` directory. Do not search for, inspect, or reuse sibling experiments, earlier generated projects, screenshots, hints, proof profiles, or repair history.

URL-only runs must be allocated by `scripts/run-url.mjs`. Its `.cloner/invocation.json` is mandatory provenance. Never pass an existing work directory to the first invocation, and never resume a directory without that file.

The invocation contains an integrity fingerprint over URL, paths, source preview, and options. Never edit it. A changed URL, loopback source substitution, path change, or recomputed ad hoc invocation is `stale-run-reuse-forbidden`.

## Primary Command

For a new URL:

```bash
node "$SKILL_DIR/scripts/run-url.mjs" \
  --url "https://example.com/" \
  --authorized \
  --depth 3
```

Read the printed `Fresh run:` path and assign it to `RUN`. The launcher intentionally writes no `current-<host>.json` or other sibling-run pointer. If the run enters `REPAIR_LOOP`, repair that exact run and resume only with:

```bash
node "$SKILL_DIR/scripts/run-url.mjs" --resume "$RUN"
```

For an existing HTTrack mirror:

```bash
node "$SKILL_DIR/scripts/orchestrate.mjs" \
  --url "https://example.com/" \
  --input "$RUN/mirror" \
  --work "$RUN" \
  --output "$RUN/react" \
  --authorized \
  --source-preview "https://example.com/"
```

Optional inputs:

- `--allow-host` for capture-time sibling asset hosts
- `--hints` for runtime-assembled asset paths
- `--offline-rules` for deterministic local service behavior
- `--base-path` for subpath deployment
- `--port` for a fixed local preview port

`--no-open` exists only for automated or headless tests. Do not use it for a normal user delivery.

Rerun the launcher resume command after repairs. `.cloner/state.json` resumes from the first incomplete gate. A directory without launcher provenance is stale and must be abandoned, not repaired.

## Autonomous State Machine

The orchestrator advances through:

```text
CAPTURE
INVENTORY
AUTHORIZATION_INVENTORY
ROUTE_RECONSTRUCTION
COMPONENT_RECONSTRUCTION
BEHAVIOR_EXTRACTION
ENGINE_ISOLATION
OFFLINE_SERVICES
LEGACY_ELIMINATION
BUILD
LOCAL_PREVIEW
PARITY_PROOF
REPRODUCIBILITY
DELIVERY_MANIFEST
OPEN_PREVIEW
DELIVERED
```

A recoverable failure enters `REPAIR_LOOP`. Read `.cloner/next-actions.json`, fix the first issue that prevents capture, React generation, local assets, build, browser operation, or preview opening, then resume the same command. Do not hand-edit reports to fake success. Trace and repair-history files are optional debugging aids unless the same failure repeats.

Only unavailable source bytes, inaccessible authenticated content, CAPTCHA, DRM, or another external impossibility may leave the run in `SUSPENDED`. `SUSPENDED` is not delivery.

## Stage 1: Capture And Asset Closure

Capture requires `--authorized` user attestation. HTTrack output is evidence, not maintainable source.

The capture scripts:

- restrict host scope
- parse HTML, CSS, JS, JSON, SVG, and manifests
- recover dynamic chunks, fonts, media, models, KTX2, WASM, workers, and decoders
- retry transient failures
- hash every captured file
- write capture and dynamic-asset reports

Before AST analysis, classify every `.js`, `.mjs`, `.cjs`, `.json`, `.css`, worker, manifest, and dynamically fetched text asset by actual bytes. HTML returned for a JavaScript path is a capture mismatch: reject it during dynamic fetch or quarantine it under `reports/quarantine/`; never report it as a JavaScript parse error. Pure JSON under a misleading extension is inert data and must not be executed.

If a `.js` path parses as raw JSON or another inert payload, treat it as a content-signature failure and quarantine or relabel it before behavior analysis. The `santionispirits.com` evidence included `public/assets/data/uil.1782836328290.js` as non-JavaScript bytes; that is not executable runtime evidence and must not remain as a parser finding in a supposedly repaired run.

Use an asset hints file for paths assembled from arrays, template strings, prefixes, decoder configuration, or stage manifests. Missing required runtime assets are never accepted in final mode.

Dynamic extraction must match longer extensions before shorter prefixes: `.json` is not `.js` plus trailing text. JavaScript asset closure is sink-based. Count imports, `fetch`, Worker, media/DOM load attributes, loader calls, manifests, and resolved constant paths; ignore unused literals and bundled CommonJS/webpack module-table keys. Preserve Emscripten `locateFile` script-relative WASM resolution.

Read [references/pitfalls.md](references/pitfalls.md) for dynamic imports, WebGL, media ranges, source maps, and root-path traps.

## Stage 2: Automatic Authorization Inventory

The Agent generates `reports/authorization-manifest.json`; the user does not prepare a per-asset list.

The report inventories:

- source and captured host scope
- every redistributed file and SHA-256
- license files and source notices
- brand, logo, font, media, model, and third-party paths
- available domain, repository, terms, and attestation evidence
- per-item status: `covered`, `restricted`, or `unverified`

This is an evidence inventory, not a license grant or legal conclusion. Never fabricate rights evidence. No manual-review queue is produced.

## Stage 3: TanStack Route Reconstruction

The deterministic generator emits TypeScript, TanStack file routes, strict TypeScript configuration, and Vite integration.

Required route rules:

- use `src/routes/__root.tsx` for global layout and boundaries
- preserve pathname, search, and hash separately
- convert only known same-origin routes to `Link`
- preserve targets, downloads, modified clicks, and ordinary external anchors
- render unknown paths through the not-found boundary, never the home page
- create loaders only when a real local data contract is known
- keep `routeTree.gen.ts` generated and all other source editable
- support configurable Vite `base`

Read [references/tanstack-router.md](references/tanstack-router.md) before repairing route generation.

## Stage 4: Component Reconstruction

Use captured DOM and style evidence to create named TSX modules. Apply [references/reconstruction-rules.md](references/reconstruction-rules.md).

`src/styles/source.css` and `.cloner/style-baseline.json` are the starting fidelity evidence. Reuse original selectors, class names, font faces, breakpoints, dimensions, and declarations before adding migration-specific styles. Do not append a generic landing-page design or replace a fixed interactive story with a normal document flow.

Create boundaries for:

- global layouts
- semantic page sections
- repeated structural subtrees
- independently stateful regions
- forms, dialogs, menus, HUD, and overlays
- canvas mount surfaces

Do not create arbitrary components based only on size. Reuse requires structural evidence. Preserve exact text, attributes, order, and local assets.

This stage passes when each captured route has a visible React-owned surface. Missing canvas/worker integration does not send the Agent back to component reconstruction; `ENGINE_ISOLATION` owns that repair so each loop has one clear responsibility.

The generated HTML-to-TSX scaffold is a starting point. It is not completion when captured runtime scripts still own behavior.

## Stage 5: Behavior Extraction And Migration

Inspect:

- `reports/site-inspection.json`
- `reports/behavior-contracts.json`
- `reports/conversion-manifest.json`
- captured JavaScript and source maps when present

Generate the machine-readable ownership inputs before deciding how to repair a legacy route:

```bash
node "$SKILL_DIR/scripts/extract-bootstrap-contract.mjs" --project "$RUN/react"
node "$SKILL_DIR/scripts/extract-react-owned-ui.mjs" --project "$RUN/react"
```

Read `reports/legacy-classification.json`, `reports/bootstrap-contract.json`, and `reports/react-owned-ui.json`. A route with a legacy loader and zero reachable visible React elements is `bootstrap-owned-shell`. Runtime canvas or worker evidence without an engine contract is `runtime-engine-present-but-unisolated`.

When a business bundle has no usable source map, create readable analysis source before migration:

```bash
node "$SKILL_DIR/scripts/decompile-bundle.mjs" \
  --input "$RUN/react/public/assets/main-HASH.js" \
  --output "$RUN/.cloner/decompiled/main.js" \
  --report "$RUN/.cloner/decompiled/report.json"
```

Preserve the decompiled file hashes and tool version, then use it to extract React-owned UI, typed services, lifecycle scope, and engine boundaries. A sanitized local runtime adapter may remain for fidelity-first delivery, but it must be clearly isolated and reported as migration debt rather than described as a pure rewrite.

An empty or nearly empty generated TSX page combined with an inline loader is a bootstrap-owned application, not a static empty page. Resolve the loader's constructed asset path, ensure the real application bundle was captured, decompile that bundle, and reconstruct its UI. Deleting the loader, removing its `<script>` node, or claiming the page no longer depends on it leaves the application blank and must not clear `captured-legacy-script-not-reconstructed`.

Migrate captured behavior according to [references/behavior-extraction.md](references/behavior-extraction.md).

For every behavior area:

1. Write a failing interaction or state regression test.
2. Name the trigger, precondition, transition, effect, network outcome, and cleanup.
3. Implement React state, a typed service, or an engine event.
4. Remove the captured DOM/event ownership.
5. Run the focused test, build, and relevant browser scenario.
6. Remove the captured script from the manifest only after its behavior is replaced.

Build an engine-to-React bridge inventory from actual runtime property and method usage. Every used bridge member must have a mounted implementation. `null`, constant `undefined`, empty callbacks, hidden resource mounts, and placeholder geometry methods fail migration when the runtime depends on them. If captured CSS defaults a control to hidden, visible React state must explicitly override that default. Test bridge members and blocking controls before proof.

Inventory top-level bootstrap calls as well as class methods. Bundle extraction often preserves helper definitions but drops the original calls that activated custom cursors, glass/decorator layers, click audio, observers, responsive mounts, or global event wiring. A defined-but-never-invoked helper is missing behavior. Recreate visible global decorators as React components with cleanup; do not restore untracked `document.body.appendChild` ownership merely to satisfy screenshots.

For deep interactive sites, move completion-critical UI into React before claiming convergence. In `why.zero.university`, proof only became meaningful after React owned the visible `DRAW A ZERO` status, `SCROLL` prompt, XP/BZ counters, next-stage hold trigger, and waitlist completion flow while the isolated engine consumed typed events behind the adapter.

Responsive ownership is part of behavior reconstruction, not a styling choice. When desktop and mobile mount different control trees, React must conditionally mount the correct controls and keep them state-synchronized. The `why.zero.university` evidence required a desktop `scroll-ruler` and a separate mobile `mobile-timeline`; hidden duplicate trees or one-size-fits-all placeholders are not sufficient.

Do not silence findings by deleting manifest entries or renaming bundles. Keeping the original sanitized local adapter is allowed; hiding it is not.

Do not replace an application bootstrap with a brochure, static marketing copy, arbitrary cards, or a shortened page. That is functional deletion, not reconstruction. User-facing text should come from captured HTML, JSON, bundle, SVG, or decompiled evidence; canvas/worker evidence must still produce a mounted engine and visible canvas surface. A project with fewer captured interaction families, media surfaces, forms, stages, or blocking gates is incomplete even when it builds.

Reports are outputs, never repair inputs. Do not hand-edit `conversion-manifest.json`, `behavior-contracts.json`, architecture/provenance reports, proof summaries, or delivery manifests to clear findings. Change source, assets, or typed ownership, then rerun the bundled verifier that owns the report.

For `captured-legacy-script-not-reconstructed`, use this repair sequence and continue in the same run:

1. Generate the legacy classification, bootstrap contract, and React-owned UI inventory.
2. Read the legacy script classification: tracker, inert data, configuration loader, application bootstrap, or engine.
3. If it constructs another script URL, verify that target exists locally; rerun capture after automatic constant-path discovery or add a machine-readable asset hint only when static evaluation cannot prove the path.
4. Decompile and inventory the target application bundle, including top-level activation calls and global side effects.
5. Reconstruct visible DOM/state in React and isolate only eligible renderer internals.
6. Add interaction and lifecycle regressions.
7. Remove the legacy manifest entry only after the replacement is mounted and architecture verification passes.

`REPAIR_LOOP` is an instruction to execute this sequence, not a valid stopping point or handoff result.

## Stage 6: WebGL Engine Isolation

An engine may own renderer internals, scenes, materials, shaders, post-processing, GPU resources, animation mixers, and engine-specific audio.

It may not own page navigation, forms, overlays, remote services, or page DOM outside its mount.

React mounts it with an effect and always calls `destroy()` on unmount. `destroy()` must cancel RAF, remove listeners, disconnect observers, stop workers and timers, release audio, dispose GPU resources, and restore modified globals.

If the retained runtime still mutates `document.body` classes or theme markers, React must own the source of truth and synchronize those globals deliberately. Proof artifacts for `why.zero.university` depended on body-class and theme progression such as `frame-open` and dark/light HUD variants; leaving those mutations as incidental legacy side effects makes proof and cleanup non-deterministic.

When the captured runtime has already been removed, the architecture verifier fails missing or incomplete engine contracts. When a sanitized local captured runtime adapter remains, engine findings are migration diagnostics and browser proof decides whether the delivered behavior is faithful.

A method-shaped adapter is not an engine. `getContext()` plus RAF counters, dataset mutations, an echo Blob worker, or empty lifecycle methods fails. Captured canvas/WebGL evidence requires source-derived render output and behavior ownership before bootstrap replacement is proven.

## Stage 7: Offline Services And Network Boundary

Assign every removed remote service one local behavior:

- persistent local implementation
- deterministic demo response
- explicit validation failure
- explicit unavailable response

Read [references/offline-network.md](references/offline-network.md) for request semantics.

The final runtime boundary must cover fetch, Request methods, XHR, beacon, WebSocket, EventSource, Worker URLs, dynamic scripts, and other automatic loading surfaces. Loopback origins are local; every non-loopback automatic HTTP(S) origin is external. User-triggered external navigation is classified separately.

## Stage 8: Legacy Elimination Gate

Run:

```bash
node "$SKILL_DIR/scripts/extract-bootstrap-contract.mjs" --project "$RUN/react"
node "$SKILL_DIR/scripts/extract-react-owned-ui.mjs" --project "$RUN/react"
node "$SKILL_DIR/scripts/verify-architecture.mjs" --project "$RUN/react"
node "$SKILL_DIR/scripts/verify-local-assets.mjs" --project "$RUN/react" --hints "$RUN/asset-hints.txt"
node "$SKILL_DIR/scripts/verify-content-provenance.mjs" --project "$RUN/react" --mirror "$RUN/mirror"
node "$SKILL_DIR/scripts/verify-public-asset-provenance.mjs" --project "$RUN/react" --mirror "$RUN/mirror"
node "$SKILL_DIR/scripts/verify-style-provenance.mjs" --project "$RUN/react" --work "$RUN"
node "$SKILL_DIR/scripts/verify-no-external.mjs" --project "$RUN/react"
```

The gate blocks progression only when:

- TanStack Router ownership is missing
- direct HTML/CSS assets are absent
- unknown automatic external requests remain

JavaScript bundle asset sinks are over-approximations and therefore diagnostic by default; use `--strict-runtime` only for an explicit audit. Architecture migration, content, public-asset, style, bundle-asset, and parser diagnostics still write reports. Treat them as a refactoring queue, not as a reason to stop producing or previewing the React project. Browser proof remains authoritative for reachable assets and visible fidelity.

Do not proceed to parity proof until the blocking conditions pass.

`conversion-manifest.json`, `bootstrap-contract.json`, and architecture reports are outputs, not ownership truth. The verifier re-derives bootstrap and runtime evidence from the run's mirror. Renaming public bundles or editing report JSON cannot satisfy this gate.

## Stage 9: Build And Preview

The orchestrator installs from the lockfile, builds once so TanStack refreshes `routeTree.gen.ts`, then typechecks, starts Vite preview, waits for HTTP 200, and records the URL in `.cloner/preview.json`.

Direct `file://` opening is not a valid verification environment. The final project may use root or configured subpath HTTP hosting.

## Stage 10: Source-Local Proof

Proof starts only after source code exists and the legacy-elimination gate passes. The original site is a read-only test oracle, never a code-generation source.

The state machine fingerprints `react/src`, package/config files, and the public delivery surface. Any source or public mutation after a completed gate invalidates `COMPONENT_RECONSTRUCTION` and every downstream stage. A proof-profile-only change invalidates `PARITY_PROOF` and delivery stages. Never add hidden, transparent, offscreen, or proof-only controls after legacy elimination; the next resume sends them back through content, architecture, build, and proof gates.

The proof runner enables WebGL2 through SwiftShader and normalizes only the reported GPU vendor/renderer for both source and local contexts. This prevents source-side `swiftshader` blocklists from redirecting an otherwise capable browser while preserving identical proof conditions. Do not patch source code, bypass application gates, or treat an `/unsupported` redirect as source unavailability until this runner has been used.

If the live source is genuinely unavailable during proof, create a proof-only local source oracle under `$RUN/.cloner/oracle/site` from untouched captured source bytes, hash it, and serve it only on loopback. Register it without editing invocation provenance:

```bash
node "$SKILL_DIR/scripts/register-source-oracle.mjs" \
  --work "$RUN" \
  --source "https://example.com/" \
  --preview "http://127.0.0.1:ORACLE_PORT/" \
  --root "$RUN/.cloner/oracle/site"
```

Registration fails unless every oracle file is byte-identical to some captured file and the preview is loopback. Keep the captured bootstrap inside the oracle only; never copy the oracle into `$RUN/react`, use it for reconstruction decisions, or make delivery depend on its server.

The internal Playwright runner executes each scenario in locked desktop and mobile environments and compares:

- route and title
- normalized visible text
- landmarks and accessible structure
- geometry and computed style checkpoints
- network and console errors
- screenshots and fixed visual thresholds
- canvas presence and nonblank pixels
- interaction state snapshots

Read [references/proof-protocol.md](references/proof-protocol.md).

For a dynamic page, never capture an arbitrary animation frame. `reports/behavior-contracts.json.summary.interactionFamilies` is the minimum proof coverage list. When that list is nonempty, the orchestrator synthesizes `reports/proof-profile.json` from behavior evidence and `react-owned-ui.json`. Treat the generated profile as an executable draft: run it, inspect exact selector/state failures, and make only evidence-backed selector, ordering, duration, repetition, and checkpoint corrections. Do not delete interaction families, routes, stages, desktop, or mobile coverage. Supported actions include `wait-for-selector`, `wait-for-time`, `click`, `tap`, `fill`, `press`, `media-play`, repeated `wheel`, `pointer-circle`, `pointer-hold`, and `checkpoint`. A profile cannot change thresholds.

Exercise every distinct family present: scroll/wheel, click/tap, pointer drag, press-and-hold, forms, keyboard, navigation/stage transitions, media, and touch/mobile variants. Every `wheel` action and `pointer-hold` action must have a checkpoint immediately before it. The after checkpoint must observe the same selector and declare `requireChangeFrom`; deterministic stabilization actions such as `wait-for-selector`, `wait-for-time`, or network idle may occur before that checkpoint. Scroll checkpoints record `scrollX`, `scrollY`, maximum depth, and effective HTML/body overflow, so a local scroll lock cannot hide behind a matching final screenshot. Capture checkpoints before, at, and after every blocking gate. Final screenshots without state progression do not pass.

For multi-gate deep-scroll flows, encode each gate explicitly in the proof profile. The `why.zero.university` deep proof required a pointer-circle loader-clear action, repeated wheel segments, two separate `pointer-hold` gates with before/after checkpoints, and a final checkpoint proving stage-5 progression. A single end-state screenshot or one generic wheel action is not acceptable evidence for staged experiences.

The proof runner compares rendered, unclipped, nonzero-opacity text and landmarks. Hidden implementation DOM, offscreen digit stacks, collapsed menus, and clipped controls are not visible evidence. Checkpoints are compared by named fields such as route, body class, normalized visible text, target visibility, and geometry; raw object serialization and hidden `body.textContent` are not gate signals. Geometry uses stable tag/role occurrence keys rather than global DOM indexes.

Source and local captures share a deterministic random seed and run in parallel. Canvas/video/continuous-animation scenarios capture a bounded frame sequence. The runner records both the best phase-aligned frame ratio and temporal-mean ratio, then applies the lower measured ratio to the unchanged locked threshold and records the selected comparison mode. Keep the matched real frames and aggregate diff artifacts. This handles source self-variance without hiding persistent layout, content, or control differences.

Do not weaken thresholds to make a run pass. Diagnose the finding, add a regression test, repair code, record the repair, and rerun.

## Stage 11: Reproducibility And Direct Delivery

The final verifier copies the project to a clean temporary directory, runs `npm ci`, builds, starts preview, and requests every known route.

The delivery stages keep the verified project directory in place, write:

- `reports/delivery-manifest.json`
- `reports/reproducibility.json`

Then `OPEN_PREVIEW` launches the recorded loopback URL with the platform browser opener. Delivery fails if the browser cannot be opened, except when an automated/headless test explicitly uses `--no-open`.

`DELIVERY_MANIFEST` is a pre-open gate for authoritative proof, reproducibility, and required repair evidence. It rejects missing proof contracts, unlocked or mismatched threshold fingerprints, incomplete desktop/mobile scenario coverage, missing source/local screenshots, missing action traces, missing image evidence, fake clean-build reports, and absent HTTP 200 route probes. `OPEN_PREVIEW` is the final browser gate. `DELIVERED` must read the final manifest and require `passed && delivered`. If nested proof reruns exist, the deepest proof depth is authoritative and the newest result at that depth wins; a newer shallow pass never overrides a deeper failure. After repeated parity failures or interruptions, both `.cloner/trace-summary.json` and `.cloner/repair-history.json` are mandatory.

## Review SOP

The same Agent performs all reviews. A review passes only through script evidence:

1. specification coverage
2. route and component architecture
3. legacy elimination
4. local asset closure
5. network isolation
6. behavior contracts and cleanup
7. bridge implementation completeness and interaction-depth coverage
8. bootstrap classification, React-owned UI inventory, and source-local parity with blocking-gate progression
9. trace/repair convergence
10. clean reproduction
11. direct-project delivery manifest and opened preview

Do not substitute prose confidence for a passing JSON report.

## Final Report

Return:

- generated project path
- local preview URL
- browser-open result
- test count
- architecture report
- asset and network reports
- proof summary
- trace summary and repair-history convergence
- reproducibility report
- authorization evidence decision

Use the phrase "React reconstruction with isolated engine" when a typed imperative engine remains. Use "React rewrite" only when no captured bootstrap owns behavior.

## Black-Box Skill Evaluation

To evaluate this Skill, give one fresh Agent only the target URL and this Skill path. Do not provide a working directory, prior output, hints, repair history, or expected implementation. The evaluator must create a fresh run, complete the SOP, leave the preview running, open it in the browser, and return evidence paths. Independently rerun every gate before accepting its claim.
