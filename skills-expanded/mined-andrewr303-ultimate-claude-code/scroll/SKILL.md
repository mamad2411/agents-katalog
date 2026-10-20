---
name: scroll
description: Build, audit, and repair smooth scroll-driven interfaces: sticky sections, scrollytelling, parallax, scroll-linked animation. Use when asked about scroll jank, pinned sections, ScrollTrigger, Motion useScroll, CSS scroll timelines, IntersectionObserver step activation, or mobile scroll smoothness.
license: MIT
metadata:
  author: ult-performance
  version: "1.0.0"
  category: web-performance
---

# Scroll-driven interfaces without jank

Build scroll-driven interfaces as resilient interaction systems, not animation demos.

The goal is not maximum motion. The goal is intentional motion that remains smooth, accessible, responsive, maintainable, and correct when content, viewport, input method, or browser behavior changes.

Adapted from upstream `zero-jank-scroll` (see `ATTRIBUTION.md`). Compositor, will-change, and GSAP lifecycle detail lives in [interaction](../interaction/SKILL.md) and its [animation-performance.md](../interaction/references/animation-performance.md); this skill owns scroll-UI architecture, implementation, and repair.

## Measure first (plugin rule)

When a URL or running app exists, measure before changing code:

1. Read [execute-snippets.md](../../references/execute-snippets.md).
2. Run the `interaction` snippets per its scroll-jank workflow: `Scroll-Performance.js` (`getScrollSummary()` after scrolling), `Long-Animation-Frames.js` (+ script attribution), `LongTask.js`, and `Layout-Shift-Loading-and-Interaction.js`. See [interaction](../interaction/SKILL.md).
3. Label every number: **field** (CrUX/RUM p75), **lab** (trace/Lighthouse), **snippet** (DevTools snippet return value), or **hypothesis** (source only). Never invent FPS or Core Web Vitals numbers.
4. Findings from the source scanner below are **hypotheses only** — a flagged pattern is a lead, not proof of jank.

Note: `scripts/audit-scroll-source.mjs` is a **Node CLI** — run `node skills/scroll/scripts/audit-scroll-source.mjs <path> [--json]`. It is NOT a browser IIFE, so the snippet protocol does not apply to it.

## Non-negotiable rules

1. Preserve native scrolling by default.
2. Choose the simplest architecture that expresses the interaction.
3. Use real semantic content to create scroll distance.
4. Never hide layout coupling behind arbitrary `300vh`, `400vh`, or percentage ranges when real steps can represent the sequence.
5. Never drive framework state on every scroll frame.
6. Never read layout and write layout repeatedly in the same scroll path.
7. Animate `transform` and `opacity` by default; justify paint-heavy or layout-changing animation.
8. Provide a normal-flow or reduced-motion experience.
9. Do not claim smoothness without runtime evidence.
10. Keep content understandable if animation, sticky positioning, or JavaScript enhancement fails.

## Step 1: Inspect before choosing

Before editing code, inspect:

- the requested visual behavior,
- the current DOM and component boundaries,
- existing animation dependencies,
- existing scroll containers,
- sticky ancestors and their `overflow`, `contain`, and transform properties,
- header behavior and offsets,
- target browsers and devices,
- viewport width and height constraints,
- reduced-motion requirements,
- whether media, canvas, WebGL, or videos run inside the sticky region,
- and whether the task is creation, repair, or audit.

Do not add a new animation library before checking what the project already uses.

## Step 2: Classify the interaction

Choose exactly one primary class.

### A. Discrete activation

Examples:

- four capability steps,
- active chapter changes,
- one panel per section,
- navigation item follows the current section.

Default architecture:

- real step elements,
- CSS `position: sticky` for visual persistence,
- one `IntersectionObserver` for active-step changes,
- one active state update only when the identity changes,
- `scrollIntoView()` for click-to-scroll.

Do not use continuous progress math for a discrete state machine.

### B. Continuous mapping

Examples:

- a progress bar,
- parallax proportional to scroll,
- drawing a path as the user scrolls,
- continuously scrubbing a simple visual property.

Default architecture:

- native CSS scroll/view timelines when the support matrix permits,
- otherwise a library or a single requestAnimationFrame-coalesced controller,
- values carried outside framework render state,
- transform/opacity/custom-property outputs where possible.

Treat CSS scroll-driven animation as progressive enhancement unless all required browsers support the needed behavior.

### C. Cinematic choreography

Examples:

- multi-scene pinned storytelling,
- coordinated scrubbed timelines,
- complex SVG/canvas sequences,
- reversible sequences with precise start/end control.

Default architecture:

- GSAP ScrollTrigger when GSAP is acceptable in the project,
- explicit lifecycle cleanup,
- refresh behavior for fonts, media, and responsive layout,
- simplified fallback for small or short viewports.

Do not use GSAP merely to highlight four steps.

Read [references/architecture-matrix.md](references/architecture-matrix.md) when the choice is ambiguous.

## Step 3: Design the document structure

Prefer this conceptual structure for sticky step stories:

```text
section
├── steps
│   ├── step
│   ├── step
│   └── step
└── stage
    └── sticky-stage
        ├── panel
        ├── panel
        └── panel
```

Requirements:

- Each step is a real element with meaningful content or labeling.
- The rendered number of steps naturally determines section height.
- Adding or removing a step must not require recalculating a track height or percentage boundaries.
- The sticky stage has a stable size or aspect ratio.
- Overlaid panels do not change the stage's layout when activated.
- Hidden interactive panels are not focusable or clickable.
- Sticky offsets derive from shared layout variables, not duplicated magic numbers.
- Step targets use `scroll-margin-block-start` when a fixed header exists.

Use `svh` for stable viewport-sized layout. Use `dvh` only where live browser-chrome resizing is intentionally desired.

## Step 4: Implement activation without scroll churn

For discrete steps:

- Create one observer, not one global listener per component.
- Observe step elements.
- Align the activation line with the intended sticky top offset through `rootMargin` or explicit sentinels. Use a center activation band only when the design explicitly calls for center-based switching.
- Update active state only when the active step actually changes.
- Disconnect the observer during cleanup.
- Preserve DOM order and content without JavaScript.

Click behavior:

- Use real buttons or links.
- Call the matching real control or trigger element's `scrollIntoView()` so it aligns with the same activation line.
- Respect reduced motion by switching smooth behavior to instant/auto.
- Do not calculate absolute document coordinates unless a proven requirement prevents element-based scrolling.
- Do not move keyboard focus merely because scrolling changed the active step.

If a scroll listener is genuinely required:

- coalesce work with one requestAnimationFrame,
- avoid repeated layout reads,
- cache stable references,
- use passive listeners when the handler never calls `preventDefault()`,
- write values directly to animation primitives rather than framework state,
- and remove the listener during cleanup.

## Step 5: Keep animation compositing-friendly

Default animated properties:

- `opacity`,
- `transform`.

Use caution with:

- filters,
- backdrop filters,
- masks,
- clip paths,
- large blurred shadows,
- gradients that repaint large regions,
- fixed backgrounds,
- canvas or WebGL rendering,
- and many independently promoted layers.

Avoid scroll-linked animation of:

- width,
- height,
- top,
- left,
- margins,
- grid tracks,
- or properties that repeatedly trigger layout.

Do not add `will-change` globally. Apply it narrowly only after profiling demonstrates a benefit, and remove it when it is no longer needed.

Pause inactive videos, canvas loops, WebGL renders, Lottie animations, and timers.

Read [references/performance.md](references/performance.md) before optimizing or diagnosing jank.

## Step 6: Build responsive and accessibility fallbacks

Enable sticky choreography only when the viewport has enough width and height. Width-only breakpoints are insufficient.

For narrow or short viewports:

- use normal document flow,
- place the relevant visual near its content,
- shorten or remove non-essential movement,
- preserve every piece of information,
- and avoid empty artificial scroll distance.

For reduced motion:

- remove smooth programmatic scrolling,
- remove or substantially reduce parallax and scrubbing,
- use immediate panel changes or gentle opacity-only transitions,
- never remove content.

Accessibility requirements:

- Use native buttons and links.
- Keep visible focus styles.
- Use `aria-current="step"` for step navigation when appropriate.
- Use full ARIA tab semantics only when implementing the complete tab keyboard pattern.
- Mark inactive hidden panels `aria-hidden="true"`.
- Use `inert` for inactive panels containing interactive descendants when supported by the project.
- Do not use color alone to communicate the active state.
- Do not trap the user's scroll or keyboard.

Read [references/accessibility.md](references/accessibility.md) for the complete review.

## Step 7: Handle framework lifecycle correctly

Framework-independent rule: continuous animation values must not cause component-tree rerenders per frame.

For React:

- create observers and animation controllers in effects,
- clean them up,
- store DOM refs and mutable continuous values outside React state,
- use state only for discrete identity changes,
- account for development-mode effect re-execution,
- do not combine Motion and GSAP control of the same property.

For Vue and Svelte:

- keep continuous progress outside broad reactive state,
- dispose observers/listeners/actions on unmount,
- avoid reactive writes on every native scroll event.

For SSR frameworks:

- isolate browser APIs to client-only lifecycle boundaries,
- render meaningful server HTML,
- avoid hydration-dependent layout shifts.

Read [references/frameworks.md](references/frameworks.md) for framework-specific checks.

## Step 8: Diagnose existing jank

When repairing an implementation, investigate in this order:

1. Confirm the jank with the same input method and viewport where it occurs.
2. Check layout shifts and sticky containment failures.
3. Check long main-thread tasks during scrolling.
4. Check repeated component renders.
5. Check scroll handlers for layout reads and synchronous work.
6. Check large paint areas, filters, shadows, and layer count.
7. Check active media/canvas/WebGL loops.
8. Check asset loading, font swaps, and image dimensions.
9. Check mobile viewport-unit behavior and browser chrome.
10. Check library refresh/cleanup behavior.
11. Change one cause at a time and remeasure.

Run the bundled source heuristic when useful:

```bash
node skills/scroll/scripts/audit-scroll-source.mjs <project-path> [--json]
```

Static findings are leads, not proof.

## Step 9: Verify with evidence

When browser tooling is available, test:

- slow wheel scrolling,
- rapid wheel scrolling,
- trackpad flicks,
- keyboard Page Up/Page Down,
- Home/End where applicable,
- scrolling upward across every boundary,
- clicking controls during and after smooth scrolling,
- resize and orientation changes,
- 125% and 200% zoom,
- reduced-motion mode,
- small width,
- short height,
- and at least one lower-performance emulation.

Collect:

- a performance trace around the problematic section,
- long-task evidence,
- layout-shift evidence,
- render-count evidence for framework components,
- console errors,
- and screenshots or recordings at boundary states.

Do not invent FPS, Core Web Vitals, or trace results. If runtime tools are unavailable, state exactly what was not measured.

## Step 10: Report using this contract

Return:

### Architecture

- Interaction class
- Selected approach
- Why it fits
- Rejected alternatives and why

### Implementation

- Files changed
- State model
- Responsive behavior
- Reduced-motion behavior
- Cleanup and lifecycle behavior

### Verification

- Tests performed
- Evidence collected
- Before/after observations
- Remaining unverified risks

### Red flags remaining

List any known:

- arbitrary scroll tracks,
- per-frame state updates,
- layout-linked animations,
- heavy paint effects,
- sticky containment hazards,
- inactive rendering loops,
- missing fallbacks,
- or unsupported-browser assumptions.

## Completion gate

Do not mark the work complete unless:

- [ ] Native scrolling remains usable.
- [ ] The architecture matches the interaction class.
- [ ] Content creates the scroll structure naturally.
- [ ] Adding a step does not require percentage arithmetic.
- [ ] No framework state updates occur per scroll frame.
- [ ] Scroll work avoids repeated forced layout.
- [ ] Sticky offsets and viewport units are resilient.
- [ ] Narrow, short, zoomed, and reduced-motion layouts remain usable.
- [ ] Hidden interactive content cannot receive accidental input.
- [ ] Observers, listeners, timelines, and media are cleaned up.
- [ ] Runtime evidence is reported, or missing evidence is explicitly disclosed.
