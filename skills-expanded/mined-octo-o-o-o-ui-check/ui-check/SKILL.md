---
name: ui-check
description: Evidence-first UI alignment audit for web, desktop, and mobile projects. Inventories screens, user-visible states, and environment variants, captures real rendered screenshots via browser, computer-use, or simulator tools, discovers the project's own UI standard, classifies findings as spec violations, polish gaps, edge defects, or improvements, builds isolated mock-data A/B demos, and generates an interactive HTML acceptance packet that records user decisions and a continuation prompt without changing product code. Use when the user asks for a UI audit, UI review, UI walkthrough, UI consistency check, design QA, design-system compliance check, or a pre-release visual review.
license: MIT
compatibility: Requires Python 3.8+ (python3 on macOS/Linux, python on Windows) and a browser, computer-use, or mobile-simulator tool for rendered evidence
---

# UI Alignment Audit

Run a complete, evidence-first UI audit and stop before production changes. Treat the project itself as the primary design authority: discover its standard before judging alignment, separate explicit rules from inferred conventions, and never import a new visual language just because it is fashionable.

## Operating contract

- Preserve product code, configuration, data, dependencies, and user changes. Write only audit artifacts and isolated demos unless the user explicitly starts a later implementation task.
- Use real rendered evidence. Operate the product with a browser tool, computer-use tool, or mobile simulator and capture complete screenshots. Code inspection supplements screenshots; it does not replace them. Scripted batch capture that you write into the audit workspace (for example a Playwright script) counts as real rendered evidence; keep the script beside its output.
- Verify visual suspicions with measurements (DOM geometry, computed styles) before recording a finding. A screenshot that merely looks wrong is a hypothesis, not evidence.
- Determine platform scope from the user request and project. Cover all supported surfaces when scope is broad; cover only the requested surface when the user narrows it.
- Do not make a finding from taste alone. Tie it to an explicit standard, a repeated project convention, a mature reference surface, a reproducible user impact, or a clearly labelled opportunity.
- Do not implement a proposed fix. Build A/B evidence in an isolated workspace, let the user decide, and stop.
- Treat user decisions as authoritative. `ACCEPTED` items may be handed to a later implementation task; rejected or deferred items must not be implemented.
- Never invent counts, screenshots, tool output, or user approvals. Run `python3 scripts/validate_audit_manifest.py` before claiming the manifest is consistent.

## Select mode and effort tier

1. Parse the user's scope: all UI, a module, a platform, a route set, a theme, or a specific regression.
2. Pick an effort tier from the request (confirm with the user when ambiguous) and record it in `scope.tier`:
   - `QUICK`: default environment only, a lightweight baseline (record the mode and only the rules your findings actually cite), findings list with screenshots in the report, no demos, no acceptance HTML, no independent review. Completion gates 1, 4, 5, 9, 10, and 11 apply.
   - `STANDARD` (default): declared coverage plan, screenshot-pair demos, full acceptance packet. All gates apply.
   - `EXHAUSTIVE`: full environment matrix. Only on explicit user request with a stated time budget.
   Tell the user the expected effort before starting a `STANDARD` or `EXHAUSTIVE` audit; on a mid-sized app, `STANDARD` runs for hours and may span sessions.
3. Discover the project type and supported surfaces, then choose evidence tools per surface using [references/platform-matrix.md](references/platform-matrix.md).
4. Determine the UI-standard mode: `EXPLICIT` (documented design system with coherent enforcement), `HYBRID` (partial rules plus stable repeated patterns), `INFERRED` (baseline inferred from mature, repeated surfaces), or `ABSENT` (no coherent baseline; report quality separately from compliance). Never invent a missing standard; label `INFERRED` and `ABSENT` conclusions as provisional and keep recommendations conservative.

## Phase 0: protect the workspace and create the audit ledger

Read the applicable `AGENTS.md`, project docs, UI/design docs, and startup and test instructions. Record repository, branch, base commit, dirty state, supported platforms, and available credentials or test data. Preserve all existing user changes.

Run `python3 scripts/init_audit.py --output-dir <dir> --audit-id <id> --scope "<scope>" --tier <tier>` to scaffold the isolated workspace and a minimal manifest. Place it under the project's established audit convention, or `work/ui-check/<audit-id>/` when none exists, and keep it out of version control — prefer a repo-local exclude (`.git/info/exclude`) over editing the product's tracked ignore file. If a manifest for this audit already exists, do not re-initialize: validate it against on-disk artifacts, mark unverifiable rows `NOT_RUN`, and resume from the first incomplete phase.

First-class artifacts (schemas in [references/audit-schema.md](references/audit-schema.md)):

- `audit-manifest.json` — scope, tier, baseline, coverage plan, inventory, evidence, findings, demos, reviews, decisions.
- `reports/ui-standard.md` — explicit or inferred baseline with source evidence.
- `reports/audit-report.md` — coverage against the plan, findings, unknowns, risks.
- `demos/` — isolated A/B evidence and mock fixtures.
- `acceptance/ui-acceptance.html`, `acceptance/decisions.json`, `acceptance/continuation-prompt.md` — the decision packet.

Save long artifacts incrementally and verify writes.

## Phase 1: build the UI baseline before judging alignment

Extract the project's UI language in this order: explicit design-system documentation; tokens and primitives; shared components; mature reference screens; repeated patterns; product copy and interaction rules; and only then general usability principles. If the project has Storybook stories, visual-regression snapshots, or component galleries, use them as baseline and inventory seeds instead of re-deriving everything by hand.

Record tokens, typography, spacing, density, controls, navigation, overlays, loading/empty/error states, motion, copy, focus, contrast, responsive and theme behavior, and permitted exceptions — each with screenshot and `file:line` evidence. An inferred convention needs at least two independent surfaces repeating it; record the source screens of every inferred rule, and do not judge a screen only against a rule whose sole source is that same screen. Before asserting any usage census ("class X is unused", "this is the first production use", "all call sites do Y"), search beyond the literal class or token name: wrapper components, factory helpers, and template-literal class strings hide consumers from a literal grep — find the wrapper (e.g. a component whose implementation emits the class) and count its call sites too, or the census claim inverts on review. If all mature surfaces share the same defect, report it under the external floor in [references/visual-review.md](references/visual-review.md) instead of enshrining it as the standard. Resolve conflicts explicitly; do not silently pick a favorite screen. Treat the baseline as provisional until the Phase 2 inventory completes, then revisit it and record changes.

## Phase 2: inventory screens, states, and environments; declare the coverage plan

Enumerate routes and hidden entries, pages, dialogs, drawers, menus, tooltips, forms, lists, errors, and permission states. Derive every user-visible state and transition per screen from code and runtime behavior; mark truly inapplicable states `N/A` with a reason. For open-ended editors or canvases, inventory representative states per component family and interaction class instead of exhaustive combinations, and record the sampling rule in the plan.

Build the environment matrix from project support and user scope (dimensions and rules in [references/platform-matrix.md](references/platform-matrix.md)), then declare a coverage plan in the manifest:

- Critical screens (entry routes, top navigation targets, screens named in the request, screens with open P0/P1 findings) × the full applicable matrix.
- All other screens × one default environment plus one contrast environment (for example dark theme or the narrowest supported width) per state.
- Collapsing further requires an equivalence argument: code evidence plus rendered evidence from at least one representative screen, generalized explicitly in the manifest with the collapsed cells listed.

Cells outside the declared plan are `NOT_RUN` with the plan cited as the reason — a single plan-level statement suffices; do not create one manifest row per skipped cell. Record unsupported values as `NOT_SUPPORTED` with source evidence. Use stable IDs such as `SCREEN-001`, `STATE-001`, `ENV-001`, and `EVIDENCE-001`.

## Phase 3: perform the real walkthrough

For each cell in the coverage plan:

1. Prepare safe fixture data and record preconditions. Anchor fixture clocks to real time (or tick them) so the product's own freshness/staleness detectors do not fire as harness artifacts; when a staleness signal is provoked by the harness rather than the product, attribute it as such instead of filing it. The same trap applies to environment forcing: an init script that re-injects theme/locale storage on every navigation masks or fakes the product's own persistence — test persistence and lifecycle states in a clean context without the injection.
2. Drive the product with the selected tool; do not rely on DOM/CSS reading alone.
3. Capture a complete screenshot: full-page or contiguous scroll captures for tall pages, plus a viewport capture when sticky or overlay behavior matters; capture transient hover/focus/pressed states while active. Two known full-page capture artifacts — record them as artifacts, do not file them as defects: (a) `position: fixed` layers (scroll-edge fades, sticky bars) stretch into mid-page bands; pair with a viewport capture. (b) Scroll-triggered reveal animations (IntersectionObserver, framer-motion `whileInView`, AOS) leave below-fold content invisible (opacity 0) in a full-page capture taken without scrolling — the page renders as a large blank band that is easy to misfile as a rendering defect; script a scroll-through to the bottom first (reveal-once animations then stay revealed), return to top, then capture. For timed transients (n-second receipts, toasts), trigger and capture in a single scripted evaluation — on MCP-style browser tools that means one run-code call doing interact→wait→screenshot, since consecutive tool calls cannot beat a short reversion window; when the window is still missed, record the observed text and mark the visual capture `NOT_RUN` honestly.
4. Record viewport, zoom, scale, DPR, theme, locale, fixture, tool, timestamp, and screenshot path.
5. Inspect the relevant component, style, token, and state code and record exact `file:line` evidence. When the working tree is dirty, note it and give a base-commit anchor for load-bearing refs — dirty-tree line numbers can drift from the base commit (schema detail in [references/audit-schema.md](references/audit-schema.md)).
6. Record the expected result before comparing the actual result. Use `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, or `NOT_SUPPORTED` honestly.
7. Repeat failures enough to separate deterministic defects from intermittent or environment failures.

Keep a console/network error attribution ledger: errors induced by the audit harness itself (injected control calls, forced-expiry or forced-failure states, cross-origin probe requests) must be attributed to the harness and excluded from product findings — "zero console errors on normal paths" is only claimable with that ledger. Do not substitute generated imagery for a real capture. If a planned cell cannot be reached or captured, mark it `BLOCKED` and preserve the attempted path.

Scripted batch-capture hygiene (learned on MCP-style browser tools, where each tool call has a hard request timeout):

- Size each batch to the tool-call budget and set a short per-action default timeout (a few seconds) inside the script — the driver's default is often 30s, so one failing locator otherwise eats the whole call; a timed-out call may also leave the product mid-interaction with work half-done, so re-verify what was actually captured before moving on.
- Before every batch, check for leftover modal overlays from the previous batch (count `[role="dialog"]` and close them) — a focus-trapped dialog silently blocks all later pointer actions and the batch dies as serial timeouts. Escape only works with focus inside the trap: focus an element inside the dialog first, then Escape. A dialog wrapper styled `display: contents` reports a zero-size bounding rect — measure its child panel when you need clip geometry.
- A shared or persistent browser profile leaks localStorage/IndexedDB/service workers from earlier sessions on the same origin (including unrelated prior tasks). Snapshot and clear origin storage once at the start of the walkthrough and record that in the harness ledger, instead of trusting the tool's default page to be a fresh profile; use isolated contexts for cells that need a genuinely clean first-run.
- When mocked data hides a surface (a flag the mock layer does not know, a data set it does not carry), a fidelity-restoring injection that matches the product's real shipped default is acceptable harness practice — record it in the ledger with the shipped-default evidence; an injection that diverges from shipped behavior is fabrication.

## Phase 4: classify findings

Evaluate every covered cell against all four questions — a non-compliant screen still gets polish, edge, and opportunity review:

1. `SPEC` — does it violate the project's explicit or inferred standard?
2. `POLISH` — is its hierarchy, rhythm, restraint, finish, or cross-surface parity below the project's mature work?
3. `EDGE` — do boundary inputs, transitions, errors, permissions, resizing, themes, or accessibility settings create a visual or interaction defect?
4. `OPT` — is there a high-value, low-regret improvement inside the current standard?

A reproducible defect is `EDGE` even when a spec violation is its root cause; record the violation in the finding's code refs. A proposal that needs a new token, a change to an existing token's defined value, or a visual pattern that exists nowhere in the project is `SPEC_CHANGE_REQUIRED` and never enters the ordinary acceptance queue silently; recombining existing tokens and existing patterns stays `OPT`. Check the external accessibility floor in [references/visual-review.md](references/visual-review.md) regardless of baseline mode. Every finding references its screen, state, environment, screenshot evidence, code evidence, baseline rule or mature reference, user impact, confidence, and severity (schema in [references/audit-schema.md](references/audit-schema.md)).

## Phase 5: independent review

Create review assignments dynamically from the inventory — product value, visual-system fidelity, responsive/theme/accessibility behavior, root cause, edge cases, overdesign, and A/B evidence fidelity (A faithful in both directions, B claims checked against real value domains — see [references/visual-review.md](references/visual-review.md)), as relevant. Use fresh-context sub-agents when available; when they are not, run a self-review pass against [references/visual-review.md](references/visual-review.md) and record it with `fresh_context: false`. Give each reviewer only the manifest rows and screenshots relevant to its dimension. Reviewers file structured objections with evidence before seeing other reviews. Resolve each item as `ACCEPT`, `PARTIAL`, `REJECT`, or `DEFER` with a reason, and re-verify factual disputes.

## Phase 6: build A/B evidence and the acceptance packet

Create A/B evidence for every actionable finding, grouping only findings with the same cause, change, and user impact. When grouped findings sit at different decision levels (for example one of them requires a spec change), split them into separate demo records — they may share the same entry page and composite screenshots — so each level gets its own decision unit instead of riding along under one approval. Choose the cheapest sufficient form:

1. Annotated A/B screenshot pair (default): A reuses or reproduces the Phase 3 capture; B is a mocked-after image or isolated static mock. A must not exaggerate the defect, a single side-by-side A|B composite image is acceptable, and a static mock that only approximates token/pixel values must be labelled direction-only — see the demo fidelity rules in [references/audit-schema.md](references/audit-schema.md) and [references/visual-review.md](references/visual-review.md).
2. Static HTML mock in `demos/` copying the project's real token values, when layout or token changes need direct manipulation.
3. Interactive demo only when the finding concerns interaction behavior or the user asks for one.

Verify every B claim against the product's real value domains before presenting it: enum values, state names, and copy must come from the actual type definitions and canonical copy sources, not from what sounds plausible (an invented enum value in a B mock survives every visual review). Privacy, legal, and consent disclosure copy must be preserved verbatim in B; any reduction is a separate decision item, never a silent "merge of duplicates".

A screenshots-only demo (no `entry`) is valid. Anchor every A variant to the Phase 3 evidence it reproduces (`a.anchor_evidence_id`) and record its fidelity level; when the project builds safely, an ephemeral git worktree with the change applied is the preferred high-fidelity source for B captures — changes inside it do not count as product modifications provided nothing is committed or pushed and the worktree is recorded in the ledger and deleted afterwards. Capture the most affected environment plus one default environment and list other affected environments by ID. Never modify product source, routes, tokens, dependencies, lockfiles, data, or configuration.

Then generate and verify the packet:

1. Run `python3 scripts/validate_audit_manifest.py <manifest>` until it prints `VALID`.
2. Run `python3 scripts/build_acceptance_demo.py --input <manifest> --output acceptance/ui-acceptance.html`. The packet's required behavior is specified in [references/acceptance-protocol.md](references/acceptance-protocol.md) and already implemented by the bundled template — do not hand-write the HTML.
3. Test the packet against a copy of the manifest with a scratch audit ID, saved **beside the original manifest** — artifact paths are relative to the manifest's directory, so a scratch copy placed elsewhere (for example inside `acceptance/`) rewrites every screenshot link wrong and fails the test spuriously. The scratch ID goes in the **top-level `audit_id`** field — that is what keys the packet's browser storage, so a wrong field silently shares storage with the real packet (manifests scaffolded by older versions may also carry a `title` that embeds the original ID; that is cosmetic only). Open it in the browser tool — if the tool blocks `file://` URLs, serve the audit root over a local static server (for example `python3 -m http.server`) and open it via `http://localhost`. Verify findings render, screenshot paths resolve — images lazy-load, so scroll each into view (or sweep the whole page) before asserting none are broken — decision buttons toggle, save is blocked while items are pending (the block surfaces as a transient toast, not a dialog), and after deciding all scratch items the export panel shows the continuation prompt in the preview textarea. The defer-remaining action confirms through a native `confirm()` dialog — headless drivers dismiss native dialogs by default, which silently no-ops the action and leaves items pending; attach a dialog-accepting handler before exercising it. Do not try to verify file downloads or clipboard in headless environments — the preview textarea is the verification surface. Delete the scratch copy and its browser storage afterwards, and stop any helper server you started.

After Phase 5 reviews are resolved, re-verify each demo lightly — A matches its anchor evidence, B's claims hold, links resolve — and mark it `REVIEWED`.

## Degraded modes

- Product cannot be built or run (including builds too slow or flaky to rely on): stop after Phase 1, deliver a code-only provisional report labelled `STATIC_ONLY`, list the startup blockers, and ask the user how to proceed.
- No browser, computer-use, or simulator tool available: same as above; never fabricate rendered evidence. When only one surface's tool is missing, degrade that surface only and continue the rest.
- Screens behind authentication, or states needing data you cannot safely provision: mark the affected cells `BLOCKED` with the attempted path, continue with reachable cells, and list the blockers for user waiver.
- Sub-agents unavailable: use the self-review fallback in Phase 5.
- An external or third-party reviewer tool was requested but is unreachable in this environment (network, TLS, proxy, or auth failure, or it hangs without producing a verdict): record it as unavailable with the observed failure, never fabricate or infer its conclusion, and rely on the remaining reviewers or the self-review fallback. A blocked reviewer is a recorded gap, not a silent pass.
- Interrupted audit: reconcile the existing manifest instead of re-initializing (Phase 0).

## Completion gates

Tier `QUICK` applies gates 1, 4, 5, 9, 10, and 11 only. Do not declare completion until:

1. the UI-standard mode and baseline are documented;
2. every cell in the declared coverage plan has a status;
3. every planned cell has real screenshot evidence or a documented blocker — screenshot paths are machine-checked by the validator; a `BLOCKED` cell keeps the audit open until the user waives it, recorded in the manifest as `waived: {by, reason, at}` on the evidence row;
4. material conclusions link both screenshots and code;
5. findings are classified into the fixed categories;
6. independent review, or the documented self-review fallback, is resolved and recorded;
7. every actionable proposal has A/B evidence or a recorded reason it cannot have any;
8. the acceptance packet passed the scratch-copy test in Phase 6;
9. the manifest passed `scripts/validate_audit_manifest.py` (machine-checked);
10. product source, configuration, data, and user changes remain untouched;
11. the user has the deliverable paths — the report, plus the acceptance packet when the tier produces one — and the task stops before implementation.

## Final handoff

Report the exact paths to the manifest, baseline, report, screenshots, demos, acceptance HTML, and validation output. Summarize coverage against the declared plan, finding counts, and review status, and list any `BLOCKED` cells that need a user waiver. Tell the user to open the acceptance HTML, decide each item, use the save action ("Save & Generate Next-Step Prompt"), and move the two downloads into the audit's `acceptance/` directory as `decisions.json` and `continuation-prompt.md` so the next task can find them. State plainly that no production implementation was applied.

## Resources

- Read [references/audit-schema.md](references/audit-schema.md) when creating or validating the manifest, evidence, findings, demos, reviews, decisions, or continuation packet.
- Read [references/platform-matrix.md](references/platform-matrix.md) when selecting tools and declaring the coverage plan.
- Read [references/visual-review.md](references/visual-review.md) when judging alignment, polish, classification boundaries, and the external accessibility floor.
- Read [references/acceptance-protocol.md](references/acceptance-protocol.md) when building or verifying the interactive acceptance flow.
- Run `python3 scripts/init_audit.py --output-dir <dir> --audit-id <id> --tier <tier>` to scaffold the audit workspace.
- Run `python3 scripts/validate_audit_manifest.py <manifest>` before handoff.
- Run `python3 scripts/build_acceptance_demo.py --input <manifest> --output <acceptance.html>` to generate or refresh the acceptance packet.
