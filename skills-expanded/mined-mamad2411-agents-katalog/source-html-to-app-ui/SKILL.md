---
name: source-html-to-app-ui
description: Rebuild an approved source HTML application as a real, high-fidelity UI in the target repository. Use for source-to-app design tasks requiring interactive source discovery, authored routes and components, local UI behavior, responsive/theme adaptation, and paired Playwright evidence.
---

# Source HTML To App UI

## Objective

Reproduce the approved source HTML as a real target application. The finished experience is the primary measure of success:

- every source page, meaningful state, visible section, and interaction family is represented;
- the target preserves source content, hierarchy, layout, styling, controls, and behavior wherever evidence exists;
- desktop, mobile, short-height, theme, drawer, and overflow behavior remain usable;
- paired Playwright evidence shows the source and target at matching routes, states, themes, viewports, and sections;
- the final audit finds and repairs missing quality work before the exact task-completion command runs.

Use the source HTML for discovery and comparison. Author the target as a normal application with real routes, components, styles, assets, and local UI state. Keep the task UI-only: do not add backend, API, database, persistence, authentication, server, or business logic.

## Strict execution contract

<execution_contract>

This is an end-to-end implementation workflow, not optional advice. A passing phase unlocks the next phase; it is not a successful stopping point. Do not stop after source discovery, Phase 0, target research, implementation, or a partial verification run. If the next phase is locally unblocked, continue into it automatically. The task is not complete until Phase 4 passes and the exact task-completion command has run successfully.

The Agent owns every gate. Browser scripts collect evidence; the Agent reviews the evidence, scores the phase, repairs failures, and promotes the marker. A normal packet failure is a repair loop: inspect the helper-owned failure, fix the same packet, rerun it through the lifecycle helper, and refresh invalidated evidence. A process violation or an unproven gate is a failed run, not permission to continue or sign off.

After compaction, resume, retry, reconnect, or a new session, reread this skill, the current phase reference, the current artifact, `progress.md`, `open-gaps.md`, and the task-owned evidence needed for the next action before doing any work. Never rely on conversation memory or an old `Pass` label as the next-step decision.

</execution_contract>

## First-action lock

<first_action_lock>

The first task turn is source-only. Do not inspect the target repository to orient yourself, confirm its routes, find a logo, check its build, or choose an asset before the source checkpoint below. A target path present in the task message is an input boundary, not permission to read that path. Do not run `ls`, `find`, `tree`, `rg --files`, `git status`, or an equivalent command against the target root; even listing target directory names is target inspection and is forbidden until the unlock. Before orientation, the only allowed skill reads are this `SKILL.md` and the exact Phase 0/lifecycle reference paths named below; never list, glob, search, or inspect the skill root, `references/`, or `assets/` directories to discover files.

Follow this exact order:

1. Read this skill and only the Phase 0 and lifecycle references required for the current marker, using their exact paths from the reference map. Do not list, glob, search, or read any other path under `.agents/skills/source-html-to-app-ui/`, including `references/`, `assets/templates/`, and `assets/scripts/`, before orientation. Use only the exact asset paths named in this skill when copying later; do not enumerate the skill package to discover them. Templates and the helper are copy-only until then, and the helper command contract is already authoritative.
2. Create a fresh `task-workflow/` and set `CURRENT_PHASE.txt` to `phase-0-source-contract`.
3. Copy the approved source HTML and design input byte-for-byte into `task-workflow/`. You may read the design input for setup, but do not open or read the copied/source HTML, inline CSS, or JavaScript yet.
4. Run the first source orientation through the lifecycle helper at desktop and mobile, passing the exact served HTML URL to the packet (for example `--env SOURCE_URL=http://127.0.0.1:5192/approved-mock.html`). The orientation packet produces exactly one desktop image and one mobile image. After the successful helper result, the next two tool calls must be exactly: read the desktop orientation image, then read the mobile orientation image. Record a concrete finding for each. No source/design read, packet write, search, shell command, or other tool call may occur between those two image reads or before them. If either image has not been read, source inspection has not started and reading source/design content is an automatic Phase 0 failure. It must assert a successful response, that the final response URL exactly equals `SOURCE_URL`, and non-directory document content. If task metadata supplies an expected title or identity, assert it; otherwise record the title and reconcile it after the complete HTML read. Helper readiness or a non-empty title alone is not sufficient.
5. Read the approved HTML, inline CSS, and JavaScript completely to EOF.
6. Create and run the complete source inventory through the lifecycle helper. Then perform an image-by-image manifest walk: read the complete manifest, open every referenced full-view, section, state, desktop, and mobile image, and record one concrete finding for each image. Continue until the opened-image count exactly equals the manifest count; a key-image pass, one-image-per-route pass, representative sample, manifest-only review, or one-viewport review is a failed Phase 0 step.
7. Write and reopen `task-workflow/phase-0-source-contract.md`, reconcile `progress.md` and `open-gaps.md`, score at least `48/50`, and pass every critical row.
8. Set `CURRENT_PHASE.txt` to `phase-1-ui-implementation`, reopen the Phase 0 artifact, and only then inspect target architecture, existing assets, routes, packages, configuration, build output, or runtime files.

The target-inspection unlock requires all of step 7, not merely captured screenshots, a completed inventory, a plan, or a claim that the source is understood. If any part of the checkpoint is missing, stay source-only. If you are uncertain whether it passed, treat it as not passed. The first source orientation also has an ordering lock: before step 4 completes and its desktop/mobile images are opened, do not open/read the source HTML or any inline CSS/JavaScript, even to plan the orientation packet. A failed lifecycle invocation does not complete step 4. Treat that failure as a hard pause in Phase 0: the only legal next action is to inspect the helper-owned failure, repair the bounded invocation (for example choose another explicit port), read the repaired packet, and rerun through the lifecycle helper. Do not read source HTML/CSS/JavaScript or design JSON, write the Phase 0 handoff, or treat helper logs/partial screenshots as orientation evidence until a helper-owned rerun succeeds and every successful orientation image has been opened.

The task message may require real brand logos. That requirement still applies, but its “one and only exception” wording is an asset-selection instruction, not an early-inspection exception. Record the requirement in the Phase 0 contract and inspect or copy the real logo only after the source checkpoint unlocks target research. Never open `public/`, `build/`, or another target asset path early to locate it.

Before the first lifecycle orientation, do not run any read, listing, existence check, environment probe, or availability probe in the target repository or in `task-workflow/`. The only permitted pre-orientation actions are direct scaffold/copy writes into `task-workflow/**`, followed by one orientation-packet write, one mandatory orientation-packet readback, and the lifecycle-helper invocation. Setup is write-only: every shell command that creates directories or copies files must end at its last write. `cp <anything> task-workflow/... && ls ...`, `mkdir ... && cp ... && ls ...`, a separate `ls` after setup, a trailing `echo`/`printf` that only announces setup, or any appended `cat`, `test`, `stat`, `git status`, `find`, `rg`, or other verification is a hard process failure. A final `printf 'phase-0-source-contract' > task-workflow/CURRENT_PHASE.txt` is a valid setup write when it is the last write and is immediately followed by the orientation-packet write. Do not use a second shell command to verify or announce setup. After the last setup write, the next tool action must write the orientation packet; after that write, the next tool action must read the complete orientation packet; only that read may be followed by the first lifecycle invocation. You may copy templates and the lifecycle helper for later phases, but do not list, reopen, or read any copied helper, template, source file, ledger, or other task-workflow artifact before the orientation packet readback; **reading the copied `playwright-lifecycle.mjs` to learn its flags or parameters is forbidden because the command contract below is authoritative**. Do not list `task-workflow/`, reopen a template, inspect a ledger, or check an existence/metadata state first. The exact forms `test -d`, `test -e`, `test -f`, `stat`, `file`, `wc`, `du`, `head`, `tail`, `sed`, `grep`, and `rg` are forbidden before the first helper, including when they are used only to check whether cleanup is needed or to learn source-file size. Do not run `ls`, `find`, `tree`, `git status`, `which`, `command -v`, `python --version`, `node --version`, `--help`, or similar commands. Use a known bounded server command directly in the helper; do not test whether Python, Node, Playwright, or a port exists first.

</first_action_lock>

### Pre-orientation read allowlist — hard cutoff

Before the first successful lifecycle orientation, the only files the Agent may read are this `SKILL.md`, `references/phase-0-source-contract.md`, and `references/playwright-lifecycle.md` at their exact mapped paths, plus the task message. Reading any other path is a run-invalidating Phase 0 failure. This explicitly includes `assets/scripts/playwright-lifecycle.mjs`, every file under `assets/templates/`, any copied helper or template, `task-workflow/**`, the source HTML, inline CSS, JavaScript, design JSON, target repository, package files, and runtime files. The helper and templates may be copied as blind byte-for-byte writes, but they must not be opened to learn flags, structure, or content. The command contract in this skill is sufficient; do not read the helper to verify or understand it. If this cutoff is broken, stop, reset the fixture, and restart Phase 0.

Before the first orientation, copy the helper and templates byte-for-byte when setup requires them, using only the exact paths in the Asset Map. Do not list, glob, search, or read `.agents/skills/source-html-to-app-ui/references/`, `.agents/skills/source-html-to-app-ui/assets/scripts/`, `.agents/skills/source-html-to-app-ui/assets/templates/`, or any copied helper/template to discover flags, structure, or parameters. The lifecycle command contract and mapped references are authoritative; copying is allowed, directory enumeration and asset inspection are not.

## Non-negotiable test gates

<hard_stop_rules>

This run is testing whether the workflow is followed. The following actions are not harmless investigation; each one invalidates the current run and requires a reset before continuing:

| Never execute | Correct action |
| --- | --- |
| `ls`, `find`, `cat`, or any equivalent inspection of `/ms-playwright`, `~/Library/Caches/ms-playwright`, `node_modules/playwright-core`, `browsers.json`, browser executable paths, revisions, or process/port state; `which`, `command -v`, `--version`, `--help`, or similar server/runtime availability probes before the first helper run | Write the task-owned packet and invoke the real lifecycle helper; its first packet is the only availability test |
| `node -e`, `node --eval`, a heredoc browser program, `node task-workflow/**/<packet>.mjs`, or any direct `chromium.launch()` process | Run the packet only as the helper's `--run` payload |
| `page.waitForTimeout(`, `waitForTimeout(`, `setTimeout(`, `setInterval(`, shell `sleep`, or timer/arbitrary polling used to settle UI | Wait for visible DOM, URL, response, geometry, or assertion state |
| a manual/background server, `curl`/`wget` readiness probe, `pkill`, `lsof`, or broad process cleanup | Give server startup, readiness, logs, and PID cleanup to the helper |
| a task-message asset/logo exception, required brand-logo path, target-root path, or implementation requirement used to justify early target inspection | Record the requirement and defer every target read until the literal Phase 0 checkpoint passes |
| opening, counting, or reading the approved source HTML, inline CSS, or JavaScript before the first lifecycle orientation has completed and its desktop/mobile images have been opened—including `wc`, `stat`, `file`, `du`, `head`, `tail`, `sed`, `grep`, or `rg` against the source file | Copy the source file only; run the orientation packet through the lifecycle helper immediately, open its images, then read the source to EOF |
| allowing the orientation packet to navigate to a directory listing, wrong route, blank document, or unrelated page; treating the helper readiness URL alone as proof that the approved HTML was opened | Pass the exact HTML URL into the packet, assert the exact final URL and non-directory content, assert task-supplied identity when available, record the title for later source reconciliation, and invalidate/recapture any wrong-page image through the lifecycle helper |
| listing, searching, reading, or inspecting target `app/`, `public/`, `server/`, packages, config, package files, `node_modules`, build/dist, tests, runtime logs, target assets, or the skill's `assets/scripts/` and `assets/templates/` before the Phase 0 source checkpoint—or verifying `task-workflow/` setup before the first helper with `ls`, `find`, `test -d`, `test -e`, `test -f`, `stat`, `file`, `wc`, `du`, `head`, `tail`, `sed`, `grep`, or `rg`, including a trailing `ls` in the scaffold command or reading the copied helper first | Stay source-only: create/copy the task-owned scaffold in a write-only command, write and read only the orientation packet, invoke the lifecycle orientation, open its images, read HTML/CSS/JavaScript to EOF, run/open the complete source inventory, then update and pass the Phase 0 artifact |

After instruction/reference setup, and before the Phase 0 source checkpoint, the only allowed workspace work is direct creation/copying of `task-workflow/**`, reading the approved design metadata, writing the orientation packet, reading that packet for audit, running it through the lifecycle helper, opening its source evidence, and updating the Phase 0 artifact. Do not list or read the target root or probe the target environment to decide what to do; the task prompt already supplies the target boundary, and target research begins only at the literal unlock. The mandatory order is: source orientation at desktop/mobile → open orientation images → complete HTML/CSS/JavaScript read to EOF → complete source inventory and opened evidence → Phase 0 artifact checkpoint → target research. After scaffold/template/source copying, do not read the copied helper or any other task-workflow artifact; write and read only the orientation packet, then invoke the first lifecycle orientation. Before every later packet, read the packet and remove the prohibited constructs above; do not execute a knowingly invalid packet “once” to see what happens. The lifecycle helper does not legalize an invalid payload. If any prohibited action occurs, stop immediately, record the failure in the current task-workflow artifact, reset the fixture, and restart from Phase 0.

</hard_stop_rules>

## Managed verification lock after Phase 0

<managed_verification_lock>

Passing Phase 0 does not relax lifecycle ownership. From Phase 1 through completion, every target browser check, screenshot, layout measurement, scroll test, or runtime inspection must be a lifecycle-owned packet. Do not run `pnpm run dev`, `npm run dev`, `vite`, or `react-router dev` directly; do not background a server; do not use shell `sleep`, `curl`, `wget`, port probes, or manual process cleanup to start, wait for, inspect, or stop it. A successful build or typecheck is not browser verification.

The only legal target-browser flow is the lifecycle helper with the target server, readiness URL, runtime directory, and packet supplied explicitly:

```bash
cd <target-repository>
node task-workflow/scripts/playwright-lifecycle.mjs \
  --server "<target-start-command>" \
  --ready-url "<target-readiness-url>" \
  --runtime-dir "task-workflow/runtime/target" \
  --run "node task-workflow/target-playwright/<packet>.mjs"
```

If this flow fails, repair the task-owned packet or the bounded helper invocation and rerun it through the helper. Never substitute a manual smoke test. A direct target server, shell wait, readiness probe, or browser check is a hard process failure: stop, record it, reset the fixture, and restart from Phase 0.

</managed_verification_lock>

## Operating Contract

<operating_contract>

Treat this file as the canonical five-phase execution protocol. Read it before work, reread it at every phase boundary, and reread it after compaction, resume, retry, reconnect, or a new coding session. Load the reference mapped to the current phase before doing that phase's work.

### Phase 0 write lock — read before any command

Until `task-workflow/phase-0-source-contract.md` has been written, reopened, scored at least `48/50`, all critical rows pass, and `task-workflow/CURRENT_PHASE.txt` is set to `phase-1-ui-implementation`, this is a source-only run. You may write only `task-workflow/**`, including source runtime files, source payloads, manifests, screenshots, and logs. Do not write `app/**`, `public/**`, `server/**`, packages, configuration, package files, build/dist, tests, or any target asset. Do not run `curl` or any download command whose output is a target path. Keep downloaded source assets inside `task-workflow/`; move or copy them to a target path only after the Phase 0 gate. The brand-logo exception changes the Phase 1 asset choice only; it never permits a pre-gate `public/` write. Any pre-gate target write is a hard Phase 0 failure: remove or revert it, record the repair, and restart Phase 0 before implementation.

For every browser, server, readiness, runtime, or evidence command, the lifecycle helper is the only process owner. Before and during the task, never run a browser or Playwright preflight through `node -e`, `node --eval`, a heredoc, a standalone script, cache/executable inspection, or an availability probe; never probe a server runtime with `which`, `command -v`, `--version`, `--help`, or similar; never manually start a server, background a server with `&`, use `nohup`, use shell `sleep`, probe with `curl`/`wget`, or clean up with `pkill`, `lsof`, or broad process hunting. Use the helper's real packet to discover whether the existing browser and server work. A `curl` used only to download the approved brand asset after the Phase 0 gate is the sole exception; it is never a readiness or UI-proof mechanism. Any direct browser/preflight command or manual server/probe/cleanup command is a hard process failure: stop the packet, record the failure, and rerun the packet through `playwright-lifecycle.mjs` before scoring or promoting the phase.

There is no exploratory-browser exception. A selector check, animation diagnosis, screenshot investigation, console probe, layout measurement, or one-off reproduction is still browser evidence work. Do not create `/tmp` diagnostics, shell-generated browser files, inline browser programs, or temporary Playwright scripts outside `task-workflow/`; do not run a task-owned packet directly just because it is short. Add the diagnostic to the appropriate task-workflow packet, keep its outputs under task-workflow, and invoke that packet through the lifecycle command shape below. `chromium.launch()` is permitted only inside a packet that the helper is currently running. Running it any other way is a hard failure even when the packet is read-only or only prints computed styles.

The first lifecycle packet is also the only browser-availability check. Never inspect `/ms-playwright`, `~/Library/Caches/ms-playwright`, `node_modules/playwright-core`, `browsers.json`, executable paths, browser revisions, `.runtime.logs`, or process/port state to decide whether Playwright works. Never use `ls`, `find`, `cat`, `ps`, `lsof`, or a package/runtime probe for that purpose. Invoke the real helper packet; if it fails, inspect only the helper-owned runtime output and repair the packet or bounded invocation. Cache, executable, revision, and availability inspection is a hard process failure.

Before invoking the helper, read back the complete custom packet from line 1 through EOF. After every packet write or edit, the very next tool call must be that complete line-1-through-EOF read; do not run `grep`/`rg`, make another edit, invoke the helper, or use any other tool between the edit and the read. A targeted slice may confirm a local edit only after that mandatory complete read; it never replaces the audit. The write response, diff preview, grep/ripgrep result, or remembered contents is not evidence that the whole packet was audited. Record the complete-read and fixed-wait review in the packet or phase artifact. A packet is invalid and must not be run if it contains `page.waitForTimeout(`, `waitForTimeout(`, `setTimeout(`, `setInterval(`, shell `sleep`, arbitrary polling/timer code used to settle the UI, or a catch/fallback that suppresses a browser wait, navigation, screenshot, console, page-error, or assertion failure. Browser packets must fail loudly: never use `.catch(() => ...)`, broad `try/catch`, ignored promises, or optional fall-through to continue after required browser work fails. Replace timer settling with a visible-state, URL, DOM, response, or geometry condition such as `locator.waitFor`, `waitForSelector`, `waitForURL`, `waitForResponse`, or an assertion. This is a model-owned packet check, not a scoring script; any prohibited construct that reaches the helper is a hard packet failure and the phase cannot be scored or promoted until the packet is rewritten and rerun.

The Agent owns each gate. A phase gate is an evidence-backed self-review: inspect the work, calculate the score honestly, identify weak rows, repair them, refresh invalidated evidence, and rescore. A failed gate is a repair loop, not a report to the user. Process details may vary with the task when coverage, evidence quality, and the required outcome remain intact.

Browser scripts collect evidence; they do not score or promote phases. Do not create phase-check, scoring, closeout, receipt, forced-read, or promotion scripts. The only supplied runtime script is `playwright-lifecycle.mjs`, which owns browser/server lifecycle. Custom Playwright scripts are expected for discovery, interaction, capture, measurement, and comparison, and they run through that helper.

Promote only from the current artifacts, opened evidence, readbacks, and actual target files. A summary claim, green build, screenshot path, or prior `Pass` label is not proof by itself. If later work invalidates a gate, return to the earliest affected phase and repass forward.

</operating_contract>

## Phase Map

<phase_map>

| Phase | Marker | Owns | Gate | Outcome |
| --- | --- | --- | ---: | --- |
| 0 | `phase-0-source-contract` | fresh artifacts, managed source discovery, complete inventory, source/design handoff, reproduction contract | `48/50` | every source page/state/section/interaction is understood and evidenced |
| 1 | `phase-1-ui-implementation` | target research, owner mapping, and ordered target-native implementation in reviewed packets | `48/50` | every contracted route/state/section/interaction has a real target owner and authored target UI |
| 2 | `phase-2-paired-responsive-proof` | code integrity, checks/build, paired source-target Playwright proof | `48/50` | responsive, theme, scroll, sidebar, drawer, and paired evidence pass |
| 3 | `phase-3-fidelity-repair-signoff` | section comparison, mismatch repair, adversarial checks, real-input proof | `49/50`; desktop/mobile `48/50` each | one-to-one visual and behavioral signoff |
| 4 | `phase-4-final-audit-completion` | artifact integrity, current evidence, final diff, completion lock | exactly `50/50` | every gate remains valid and completion is unlocked |

</phase_map>

Keep work in the phase that owns it. Each phase has different work; do not use a later phase to avoid an earlier gate. Continue through Phase 4 whenever local repair is possible. An external blocker is a valid stop only when it is proven, recorded in the current artifact and `task-workflow/open-gaps.md`, and has no local recovery.

## Phase Gate Loop

Run this loop for every phase:

1. Set `task-workflow/CURRENT_PHASE.txt` to the phase marker before phase work begins.
2. Reread this file, the mapped reference, the current phase artifact, `progress.md`, and `open-gaps.md`.
3. Record a small work or evidence packet: scope, intended owners, evidence paths, exclusions, and its review action.
4. Perform only that packet, using the required real inputs and managed Playwright lifecycle.
5. Reopen changed files and generated artifacts; inspect focused diffs and complete the packet's image-by-image manifest walk before scoring it.
6. Reconcile browser findings, source declarations, target code, evidence identity, and gap ownership.
7. Update and read back the phase artifact, `progress.md`, and `open-gaps.md`.
8. Score every rubric row from concrete evidence and evaluate every critical item independently.
9. On failure, keep the marker on the phase, record the earliest repair, fix it, refresh invalidated evidence, and repeat from step 2.
10. On pass, record the promotion lock, reopen the artifact trail, verify arithmetic and evidence, set the next marker, and immediately load the next reference.

The artifact trail must agree: marker, phase artifacts, `progress.md`, `open-gaps.md`, evidence ledgers, and actual files must describe the same current phase and next action. `CURRENT_PHASE.txt` is a resume pointer, not proof. `progress.md` is a compact resume ledger, not a substitute for detailed evidence.

Keep browser work and visual review in bounded packets. A source or target packet should own one route/state family and a coherent viewport/theme set, with a reviewable number of outputs. Do not create one monolithic corpus packet that must be rerun after an unrelated selector or state failure. When a packet passes, preserve its manifest rows; repair and rerun only the failed or invalidated packet, using new revisioned paths when evidence changes.

## Fresh Task Workspace

The first target-repository write creates a clean `task-workflow/` from the supplied assets. Remove stale `task-workflow/` state, then create:

- `CURRENT_PHASE.txt`, `progress.md`, `open-gaps.md`, and `spec.json`;
- one artifact for each of the five phases;
- `source-playwright/`, `source/`, `target-playwright/`, `verification/`;
- `runtime/source/`, `runtime/target/`;
- `scripts/playwright-lifecycle.mjs` copied byte-for-byte from this skill.

Copy the supplied design JSON byte-for-byte to `task-workflow/spec.json`. Keep every generated screenshot, script, manifest, runtime log, note, ledger, and decision under `task-workflow/`. Preserve the supplied templates and their scorecards, critical gates, and promotion locks. Exact wording may be shortened only when the same evidence remains explicit and scorable.

During Phase 0, the opening operating-contract lock above is absolute: keep target implementation, configuration, package, asset, generated, build, and test files read-only and unread. Do not open, list, grep, find, inspect, or research target files, target build output, target runtime logs, target assets, or target dependencies before the source-only evidence sequence has completed. The required order is: (1) create the task-workflow scaffold; (2) run the first source orientation through the lifecycle helper at desktop and mobile; (3) open those orientation images; (4) read the approved HTML, inline CSS, and JavaScript to EOF; (5) run and open the complete source inventory/state/section evidence through the lifecycle helper; (6) record the source/design handoff and score the Phase 0 source contract with all critical rows passing; (7) reopen the artifact, verify the promotion lock, and set `CURRENT_PHASE.txt` to `phase-1-ui-implementation`; only then may target research begin. The Phase 0 handoff names required target roles and adaptations, but it does not invent exact target files before target research. If target files are inspected or written early, Phase 0 has failed; remove or revert only premature writes, record the failure, and repeat the source gate. Never use premature target research or implementation as evidence that Phase 0 passed.

## Evidence Contract

<evidence_contract>

### Source discovery

Follow this source-only order exactly: scaffold task-workflow; start the source through the lifecycle helper; capture exactly one desktop and one mobile orientation image and open both; then read the approved HTML, inline CSS, and JavaScript completely to EOF; then run the complete source inventory through the helper and perform the image-by-image manifest walk; then update and pass the Phase 0 source contract; only after that inspect target architecture and assets. The orientation pair is only a startup check. The later manifest walk means: read the complete manifest, process every image path in manifest order, open each image at a readable scale, and record a concrete observation against that image's identity. The walk is complete only when opened-image count equals manifest-image count. Do not score or promote from key images, one image per route, representative samples, a contact sheet alone, a manifest-only review, or one viewport. Do not inspect target files, build output, runtime logs, or dependencies during the earlier source-only steps. Inventory every page-like surface, route, hidden view, state, section, interaction family, theme, breakpoint, scroll owner, fixed/sticky region, and source-declared item not visible initially.

Use Playwright's user-facing input APIs to reach pages and states: locator/page `click`, `fill`, `selectOption`, `press`, `wheel`, drag, or touch as appropriate. Do not use `evaluate(() => element.click())`, `dispatchEvent(...)`, synthetic routing, direct handler calls, or DOM mutation to stand in for a real interaction. This includes assigning `el.value`, `el.checked`, or classes and then dispatching `input`, `change`, or click events. A browser-evaluated function may observe or measure state, but it may not create the state being evidenced. If a normal action fails, diagnose and repair the page or interaction target; do not bypass the failure with a DOM-dispatched event. Scope selectors to the active route/state and assert the intended control or section is unique before using it. Required section/state captures must fail the packet when their locator, assertion, screenshot, or finding fails; do not catch, log, and continue with partial evidence. Let the inventory determine evidence volume: there is no fixed page, state, section, or screenshot limit. For every inventoried page and meaningful state, capture desktop and mobile full-view evidence plus readable section/state/theme evidence where applicable.

### Paired proof

Capture source and target separately through lifecycle-owned runs. Pair images by route, state, theme, viewport, section, and framing. Give every image a unique stable ID/path, actual dimensions, capture time, lifecycle run, opened time, and concrete findings. Use a new revisioned path after recapture.

Complete the image-by-image visual closure before scoring any phase. Read the complete manifest, then open every manifest image individually or in small readable batches of no more than four related images at a time. This is a context-protection rule for each review batch, not a cap on total pages, states, sections, viewports, or screenshots. After each batch, immediately append the opened result and one concrete finding per image to the owning phase artifact, update `progress.md` and `open-gaps.md`, and read those updates back before opening the next batch. Continue until the opened count exactly matches the manifest count. “Key images,” one image per route, representative samples, a contact sheet without constituent-image review, a manifest-only review, or opening only one viewport is an automatic evidence failure. A screenshot path or manifest row becomes evidence only after that exact image has been opened and its finding is recorded. Compare content/order, geometry, spacing, typography, color, backgrounds, borders, radii, shadows, assets, controls, clipping, overlap, responsive transformation, interaction state, and scroll behavior.

### Responsive and theme safety

Check desktop, tablet when relevant, mobile, omitted-size extrapolation, short-height overflow, source themes, target-required themes, and important interaction states. Derive missing target themes conservatively from the accepted source/design system. Repair objective defects such as overlap, clipping, cutoff, horizontal canvas overflow, unusable controls, accidental document scroll, or blank regions.

When a source entrance animation interferes with a readable capture, reach the state with a real control and wait for the source's own settled DOM, geometry, opacity, or transition condition. Do not inject styles, set opacity/classes, disable animations, or otherwise mutate source DOM/CSS merely to make a screenshot readable. If the source has no stable settled state, record that behavior and its evidence instead of rewriting the source inside the packet.

</evidence_contract>

## Sidebar, Content Scroll, And Drawer Contract

<sidebar_contract>

When a sidebar exists, treat its scroll architecture as a target requirement, not a cosmetic detail. Prove it at a forced-overflow short desktop height with real scroll input and before/after screenshots.

Record two separate contracts:

| Contract | What to record |
| --- | --- |
| Source observation | source document/content scroll values, sidebar bounds, sticky/fixed behavior, and visible result |
| Target requirement | viewport-bounded shell, named sidebar, named content scroller, document scroll unchanged, content scroll increasing, sidebar fixed to the viewport |

The target proof must copy raw values from the target manifest and calculate:

- document scroll delta = `0`;
- content-pane scroll delta `> 0`;
- sidebar top and bottom deltas within `1px`;
- sidebar height and bottom cover the viewport within `1px`;
- the post-scroll image has no blank lower-sidebar region.

Source values describe the reference; they cannot satisfy or relax target predicates. A target that relies on document scrolling, sticky positioning alone, a fixed-height strip, or an unnamed overflow owner returns to Phase 1 for shell repair.

When a mobile drawer exists, prove real-input open/close, overlay interception, full-viewport geometry, body/document scroll lock, and scroll restoration with screenshots and measurements.

</sidebar_contract>

## Managed Playwright Lifecycle

### Lifecycle-only entry rule

Every browser or runtime UI check is lifecycle-owned. A custom Playwright file is a payload for the helper, never a standalone command. Do not run `node task-workflow/source-playwright/<script>.mjs`, `node task-workflow/target-playwright/<script>.mjs`, `node -e`/`node --eval` with Playwright, an inline heredoc browser program, or any equivalent direct browser command. Debug browser behavior by editing a task-owned `.mjs` packet and rerunning that packet through the helper; never write a diagnostic to `/tmp` or another temporary location and never use a shell heredoc or redirection to manufacture a browser script. Do not start a background server for a smoke test, readiness test, or browser run; do not attach Playwright to a manually started server; do not use shell `sleep`, `curl`, or another manual request as a substitute for the helper’s ready URL. After a build, validate the running target by invoking the lifecycle helper with the bounded server command, ready URL, runtime directory, and custom Playwright payload. Do not invoke `playwright install`, `playwright install --dry-run`, or any equivalent browser-install or browser-availability command; use the existing browser cache through the lifecycle helper.

Use this shape for every source and target packet, changing only the owned server, readiness check, and payload:

```bash
node task-workflow/scripts/playwright-lifecycle.mjs \
  --server "<bounded server command>" \
  --ready-url "http://127.0.0.1:<port>/<ready-path>" \
  --run "node task-workflow/<source-or-target-playwright>/<packet>.mjs"
```

The helper must own startup, readiness, browser environment, runtime logs, and PID-scoped cleanup. If the browser or server fails, inspect the helper-owned logs and repair the invocation or packet. Never bypass the helper to test whether the payload works; a direct Playwright command, including a one-off debug command, is a hard process failure even when it produces useful output. A lifecycle failure remains a gate failure until a helper-owned rerun produces usable evidence.

Start the source through the helper, capture and stop it; start the target through the helper, capture and stop it; then compare saved evidence. Keep ports, scripts, screenshots, and runtime logs separate.

Use deterministic readiness and state conditions rather than fixed sleeps. `page.waitForTimeout`, shell `sleep`, arbitrary polling delays, and timer-only settling are hard packet failures; remove them, record the gate failure, and rerun through the helper before scoring. Start readiness and focused script timeouts at `15,000`–`20,000` ms. If a run ends only from a timer with no useful diagnostic, record clean triage before one `60,000` ms retry; keep one targeted script within `120,000` ms by splitting the work. A useful failure is a repair ticket: inspect its logs, DOM/state, console, network, and server output before rerunning.

Keep lifecycle ownership with the helper and its PID-scoped cleanup. Prefer explicit task-owned ports, bounded scripts, and focused reruns. Preserve the helper byte-for-byte; keep process hunting, background-server loops, arbitrary port sweeping, browser downloads, and manual lifecycle outside the normal workflow.

## Adaptation Rules

- Match accepted source evidence one-to-one wherever it exists.
- Preserve source content, hierarchy, spacing, typography, colors, controls, states, routes, interactions, themes, and assets.
- Apply the required target-safe viewport shell/content-scroller architecture while preserving the source's visible result.
- Extrapolate omitted breakpoints conservatively from source evidence, design JSON, and target tokens.
- Use the real repository logo when available.
- Disable unsupported navigation rather than inventing destinations.
- Keep implementation UI-only and source-backed.

## Resume And Reference Loading

After compaction, resume, retry, reconnect, or a new session, read in this order:

1. this `SKILL.md`;
2. `task-workflow/progress.md`;
3. `task-workflow/CURRENT_PHASE.txt`;
4. `task-workflow/open-gaps.md`;
5. the current or earliest failing phase artifact;
6. the reference mapped to that marker;
7. the task input, source HTML, design JSON, and active target files required by that phase.

Reference map:

| Marker | Read |
| --- | --- |
| missing workflow or Phase 0 | `references/phase-0-source-contract.md`, `references/playwright-lifecycle.md` |
| Phase 1 | `references/phase-1-ui-implementation.md` |
| Phase 2 or 3 | `references/phase-2-3-playwright-fidelity.md`, `references/playwright-lifecycle.md` |
| Phase 4 | `references/phase-4-final-audit-completion.md` |

## Completion Lock

Before completion, verify that:

1. `CURRENT_PHASE.txt` is `phase-4-final-audit-completion`;
2. every phase artifact says `Decision: Pass` at its required threshold;
3. every critical row, packet review, promotion lock, and gap row has concrete current evidence;
4. every cited image exists, was opened, and has a matching source-target comparison;
5. final desktop/mobile/section/sidebar/drawer evidence represents final target code;
6. the final diff is UI-only and all required checks/build evidence remains current;
7. the exact completion command from the task instructions is copied, unrun, and the sole remaining action.

Use the exact supplied command, for example:

```bash
node /workspace/builder/task_complete.mjs --projectId "<projectId>" --taskId "<taskId>" --status completed --summary "<brief summary>"
```

After the Phase 4 artifact and `progress.md` are read back, run that exact command as the literal final tool action. Do not run another tool afterward; respond directly from its result.

## Asset Map

| Runtime artifact | Source asset |
| --- | --- |
| `phase-0-source-contract.md` | `assets/templates/phase-0-source-contract.md` |
| `phase-1-ui-implementation.md` | `assets/templates/phase-1-ui-implementation.md` |
| `phase-2-paired-responsive-proof.md` | `assets/templates/phase-2-paired-responsive-proof.md` |
| `phase-3-fidelity-repair-signoff.md` | `assets/templates/phase-3-fidelity-repair-signoff.md` |
| `phase-4-final-audit-completion.md` | `assets/templates/phase-4-final-audit-completion.md` |
| `progress.md` | `assets/templates/progress.md` |
| `open-gaps.md` | `assets/templates/open-gaps.md` |
| `scripts/playwright-lifecycle.mjs` | `assets/scripts/playwright-lifecycle.mjs` |
