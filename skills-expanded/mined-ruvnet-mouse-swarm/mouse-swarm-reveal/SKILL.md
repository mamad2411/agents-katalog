---
name: mouse-swarm-reveal
description: Build a sequential website reveal with simulated cursor swarms, or add a local Ruflo agent status view. Use for a swarm-built landing page, cursor choreography, agent-themed product demo, reveal controls, or verified read-only Ruflo status integration.
---

# Mouse Swarm Reveal

Create the complete, usable page first. Choose the mode explicitly:

- **Reveal:** simulated cursors choreograph a sequential presentation. They are not agents, computer input, or telemetry.
- **Ruflo observation:** the local bridge reports agent registrations and statuses from the CLI. It does not start agents, prove task execution, or supply cursor coordinates.
- **Both:** keep the visual reveal and observed status clearly labeled and separate. Only show a live marker when the trusted source actually supplies its coordinates.

Use `assets/demo.html` for the existing working reference. The bundled browser modules are self-contained and have no runtime dependencies.

## Workflow

1. Inspect the project instructions, framework, entry point, existing styles, and available assets. Identify the content, brand, links, and intended reveal sequence. Reuse assets only when authorized. If given a URL, work from authorized content and available source; do not assume the site permits cross-origin fetching or reproduce third-party assets without permission.
2. Add `data-swarm-item` to meaningful elements in document order. Keep targets at one hierarchy level: marking a parent and its descendants can hide content unexpectedly. Add `data-swarm-type` only to leaf elements with plain text; the module replaces their text temporarily during the animation.
3. Integrate the bundled `assets/mouse-swarm.js`. For a static site, copy it into a public assets directory and import it as a browser ES module. For a bundled app, install the repository package with `npm install github:ruvnet/mouse-swarm` and import from `@ruvector/mouse-swarm`.
4. Initialize after the target DOM exists. The module captures targets at initialization, so recreate the instance after a material target list change. Configure cursor count, colors, labels, size, motion speed, bot frequency, selection outline, typing cadence, and optional scrolling to suit the project. Expose keyboard-accessible replay, pause, resume, and skip controls that stay visible throughout the reveal. In component frameworks, call `destroy()` on unmount.

```js
import { createSwarmReveal } from '@ruvector/mouse-swarm';

const reveal = createSwarmReveal({
  root: document, cursors: 24, interval: 200,
  colors: ['#c8f578', '#70c9f9', '#c9acff'],
  labels: ['Scout', 'Builder', 'Reviewer'], botEvery: 4,
  cursorSize: 18, cursorSpeed: 600, selection: true,
  typeText: true, typeWords: 2, autoScroll: false,
  onStep: ({ current, total }) => { /* update progress */ },
  onError: (error) => { /* report the failure */ }
});
reveal.start();
// Connect controls to reveal.replay(), reveal.pause(), reveal.resume(), and reveal.skip().
// Read reveal.getState() for status and progress.
// Call reveal.destroy() during cleanup.
```

For static sites, copy `assets/mouse-swarm.js` into a served project directory and replace the import path with that served module path. Serve the site over HTTP; browsers do not resolve bare package names without a bundler or import map. `assets/demo.html` is an interactive configuration reference; use the project's own content and design. Targets cannot be shared by simultaneous instances from the same module. An animation or callback error restores content and reports through `onError`.

## Capture a local page

When the user wants a visual reconstruction, use the optional `mouse-swarm-capture` command on trusted, authorized local HTML. Choose viewport dimensions and verify the resulting sequence editor and output before video export. The result uses static screenshots for one viewport: do not claim that original links or controls work, that the full page was captured, or that external resources were preserved. Scripts are disabled by default; allow them only for explicitly trusted content. See `docs/page-capture.md` in the repository for prerequisites and limitations.

## Sequencing and interaction

- Mark individual visual units rather than an entire section. Use DOM order for header, headline, supporting copy, cards, and final action; use short leaf text for typed steps. Do not mark nested targets. Set `data-swarm-order` (0 to 100000) to change reveal order without changing DOM semantics, `data-swarm-delay` (0 to 10000 ms) for a per-element delay, and `data-swarm-role` for an illustrative label. Use `data-swarm-group` on adjacent targets for a simultaneous reveal and `data-swarm-effect="drag"` for an illustrative drag ghost. Grouped text typing proceeds sequentially after items appear.
- Keep replay, pause, resume, and skip outside the selected content. Do not cover interactive elements or hijack scrolling. Use `onStep` for progress and `onComplete` to restore UI state; inspect `getState()` for status and counts.
- Use `destroy()` before recreating an instance or unmounting a component. Preserve the page's semantics and no-JavaScript content. Respect reduced motion and let the module restore content on errors.
- For MP4 capture, use the optional local `mouse-swarm-video` command with trusted HTML, or `mouse-swarm-activity-video` with a saved observation recording. Both require Playwright, Chromium, and FFmpeg; a video from observations shows source labels and rescales timing. Specify dimensions and duration; verify the resulting file. Do not present a prerecorded demonstration as a live swarm.

## Ruflo integration

For observed state, prefer the opt in loopback example: run `npx --yes --package=github:ruvnet/mouse-swarm mouse-swarm observe` from the intended Ruflo project and open the printed local URL. It reads agent registrations and status using the local Ruflo CLI; it does not start agents, control a computer, or report cursor positions. Do not expose that server publicly.

For a custom host, use `@ruvector/mouse-swarm/ruflo` and `@ruvector/mouse-swarm/ruflo-view`, or copy the corresponding bundled assets into the project. The host must authenticate, authorize, minimize, and normalize events. Supply coordinates only when they were actually observed. Do not put secrets, raw task descriptions, or private agent data into a public landing page. Display status provenance and stale or error state; do not infer execution from registration. The adapter does not perform network calls or execute tasks. For opt-in snapshot capture and replay, install the package and use `@ruvector/mouse-swarm/activity`; source timestamps are observation times, and changes between snapshots are not proof of execution. The `@ruvector/mouse-swarm/metaharness` adapter requires an explicit host mapping of MetaHarness session envelopes and does not discover or authenticate sessions. In Node, `@ruvector/mouse-swarm/metaharness-file` can import a bounded, explicitly selected complete session JSONL file; it validates structure but not state hashes or authenticity.

For a complete authenticated snapshot, validate and map source records to `agent.upsert` events and use `adapter.replaceAgents(events)` once per successful poll. For incremental updates use `adapter.ingest(event)` with monotonically increasing per-agent revisions when the source supports them. The view supports `unverified`, `connected`, `stale`, `error`, and `disconnected`: report connected only after the source succeeds, and mark a failed poll stale or error. Equal snapshot revisions retain prior data. Removal revision history is bounded to twice `maxAgents`, so the source must also prevent delayed events after eviction. Destroy the view and dispose the adapter during teardown.

The local bridge polls only the agent list and excludes task bodies, prompts, and credentials. Custom adapters may accept `task.update` events, but task titles are hidden by default and must not be published without authorization. Do not label illustrative events as native Ruflo wire events.

## Playwright verification

For browser checks, install Playwright and a matching browser in the target project and use `@ruvector/mouse-swarm/playwright` with a host-owned Page. Configure selectors for actual controls and test pause, resume, skip, reduced motion, and pointer transparency. A target with no hidden marker is not proof that text typing or callbacks have completed; check the application completion indicator as well. See the repository `examples/playwright-check.mjs` for a runnable offline example. Choose the browser and video settings according to the request, then validate actual output on the available platform.

## Validation

- Check the initial sequence, final page, replay, pause, resume, skip, and teardown. Confirm the controls remain usable during the reveal and no target is owned by a second active instance. Validate custom values and progress callbacks. Confirm that links and controls remain usable and the overlay does not intercept clicks.
- Check narrow and wide viewports, reduced motion changes during playback, callback failures, and keyboard focus while targets are hidden. Keep content readable without JavaScript and avoid forcing the user's scroll position.
- Preserve the original text, HTML semantics, and destination links. Never collect visitor data or send content elsewhere as part of the effect.
- For observation, verify the CLI responds in the intended project, source failure is visible, and an empty list is shown honestly. Test with actual events when available; never claim a live swarm was verified using a fabricated fixture.
- If video is requested, use the optional MP4 exporter or another recording workflow and verify the requested format and dimensions. The reveal browser module itself does not create MP4 files.

Do not copy third-party websites or assets without permission. Describe animated cursors as simulated unless they are backed by verified live agent events.
