---
name: toutour
version: 1.2.0
description: Add a spotlight onboarding tour to any website. Analyzes the site's layout, tabs and UI components, interviews the developer (step granularity, mask, languages, theming, trigger mode, library), then generates and Playwright-verifies a guided tour. Use when the user asks for an onboarding tour, product tour, guided walkthrough, coach marks, feature introduction overlay, or says users can't figure out their site.
---

# Toutour — generate a verified spotlight onboarding tour

You are adding a step-by-step guided tour (dark mask + spotlight + tooltip) to the user's website. Follow all five phases in order. Do not skip the interview and do not skip verification — an unverified tour that covers its own target is worse than no tour.

## Phase 1 — Analyze the site (before proposing anything)

Read the code and, if a browser tool (Playwright/Chromium) is available, load the real page. Build an inventory:

1. **Stack & render model**: static HTML / SPA framework / SSR+hydration. For SPAs note route changes and lazy-mounted components — targets may not exist at tour-start time; steps need `waitFor` logic or route navigation hooks.
2. **Layout regions**: header/nav, panels, canvas/content area, footer. Note `position: sticky/fixed` elements and every explicit `z-index` in the codebase (you must render above ALL of them — pick tour z-indexes above the max found, and record the max in a comment).
3. **Tab systems & disclosure**: every tab bar, accordion, drawer, modal. Record: the trigger element selector, the panel shown, and HOW switching works (click handler? URL hash? framework state?). The tour must programmatically reveal a target's container before spotlighting it — prefer dispatching a real `click()` on the existing trigger over re-implementing state changes.
4. **Interactive controls per region**: buttons, sliders, checkboxes, selects, color pickers, canvases. For each: selector, what it does, and its *grouping* — controls that share a card/fieldset/label-row should be introduced **together as one step** (spotlight the wrapper, not each 13px checkbox). Related callbacks that form one mental action (e.g. "pick a value + see the preview update") belong in the same step's copy.
5. **Conditional/hidden elements**: anything shown only for certain modes/settings (`display:none` toggles). These need `when:` predicates so steps skip cleanly, with the step counter computed from the filtered list.
6. **Responsive differences**: breakpoints where the chrome changes (bottom sheets, hamburger menus, relocated DOM). If mobile is a *different UI* (not just reflow), plan **two step maps sharing one engine**, selected via `matchMedia`. Check whether elements are physically moved (`appendChild`) at a breakpoint — a tour running across that boundary must end cleanly, not survive it.
7. **Existing conventions**: i18n mechanism, theme system (CSS custom properties?), localStorage key prefix, analytics helper. The tour must reuse ALL of these, not invent parallel ones.
8. **Honest assessment — a tour is not a bandage**: if the analysis reveals UX that no tour can fix (mislabeled or invisible primary actions, contradictory navigation, dead ends), say so and recommend fixing the UI first. Adding a tour on top of confusing UX increases frustration; the step map you propose should note any such findings separately.
9. **Anti-pattern audit**: check the site against `references/anti-patterns.md` (install interstitials, pre-checkout auth walls, instant popups, fake urgency, confirmshaming, missing `prefers-reduced-motion`, zero-results dead ends, 100vh false-bottom heroes). Report every hit as a friction finding WITH its published number — these findings routinely matter more than the tour itself.

Deliverable of this phase: a written step-map proposal (region → steps → grouped controls → nav metadata per step) shown to the user.

## Phase 2 — Interview the developer

Ask (use your environment's structured-question tool if available; otherwise ask in chat). Never assume defaults silently:

1. **Granularity**: (a) condensed main tour ~10–14 steps (recommend: highest completion rate), (b) exhaustive every-control tour, (c) two-tier — condensed main tour + a small "?" button per panel launching an exhaustive mini-tour of that panel. Two-tier is the best answer for dense tool UIs.
2. **Mask & emphasis**: dark semi-transparent mask on/off (recommend on, `rgba(0,0,0,.55–.65)`); accent-colored spotlight ring on/off (recommend on — the ring keeps the spotlight visible against dark page themes).
3. **Languages**: which locales. If the site is already multilingual, reuse its exact mechanism (CSS-class-scoped spans, i18n framework, dictionaries). Tour copy must switch live if the site switches live.
4. **Theming**: follow site day/night mode (recommend: style everything with the site's existing CSS custom properties so it's automatic) or fixed look.
5. **Trigger**: auto-show for first-time visitors (persist dismissal in localStorage using the site's key prefix; suppress for deep links / shared URLs / embedded modes) and/or a persistent "?" help button. Recommend BOTH. Verify the "?" button is actually visible on every breakpoint — mobile headers often hide or cover desktop nav.
6. **Interaction during tour**: block page interaction (navigation only via Next/Prev/Skip/Esc/arrows — recommended, prevents state drift) or allow interacting with the spotlighted element.
7. **Analytics**: which tracking helper to wire `tour_start` / `tour_step` / `tour_done` / `tour_skip` into. Per-step events are what make the completion funnel visible — developers learn exactly which step users abandon on. If the site has no analytics, note it and move on; never add a tracking vendor uninvited.

## Phase 3 — Choose the rendering approach

Decision order:

1. **Site has zero JS dependencies / wants full control** → use the Toutour reference engine (`engine/toutour.js` + `toutour.css`, MIT, ~9 KB, no deps). Inline it or vendor it.
2. **Site already uses npm and wants a maintained lib** → **Driver.js (MIT)** is the default safe choice.
3. **⚠️ License gate — check before suggesting anything else**: Intro.js is **AGPL + paid commercial license**; Shepherd.js moved to **AGPL + paid commercial** in recent major versions. Never add these to a commercial/proprietary site without telling the user about the license cost. React-only sites: React Joyride (MIT) or Onborda (MIT, Next.js).
4. Consult `references/libraries.md` for the full catalog and integration notes.

## Phase 4 — Implementation rules (hard-won; follow them)

- **Spotlight**: one fixed-position div with `box-shadow: 0 0 0 200vmax rgba(0,0,0,.6)` punches a true hole — the target keeps its exact colors. Round corners from the target's computed `border-radius`, plus ~6px padding. CSS transition on top/left/width/height gives the glide between steps; disable it for the first placement (no fly-in from origin) and entirely under `prefers-reduced-motion`.
- **Tracking**: a `requestAnimationFrame` loop reading `getBoundingClientRect()` each frame (update only on >0.5px delta). One mechanism covers scroll, resize, sheet/drawer animations, and i18n reflow. Cancel it on tour end.
- **Tooltip**: never overlaps the spotlight rect — pick the side with room (desktop: right→left→bottom→top; mobile: bottom→top), clamp into viewport, aim a rotated-square arrow at the target center (clamped off the card corners). Step icon + "3/13" counter live on the card, which by construction sits outside the lit area. Full-screen targets: pin the card to the freer screen edge and hide the arrow.
- **Target widening**: if a step targets a bare `<input>` (checkbox/radio/range), widen to `closest('label')` or the labeled wrapper — a 25×25px spotlight that excludes its own label reads as broken.
- **Navigation metadata per step**: which tab/sub-tab/drawer state reveals the target, expressed by clicking the site's real triggers. Steps whose target is missing or hidden at start are filtered out BEFORE computing the "n/total" counter.
- **Blocking**: full-viewport transparent blocker div under the spotlight layer; spotlight div itself gets `pointer-events:auto` so the target can't be clicked mid-tour (unless the developer chose interactive mode).
- **Keyboard**: Esc ends, ArrowRight/Enter next, ArrowLeft prev — as a capturing listener, with `preventDefault` so a focused button doesn't double-fire.
- **State**: one localStorage key (site's prefix + `tour_seen`), set on dismiss AND completion, wrapped in try/catch (private mode). Suppress auto-show when the URL carries share/deep-link params.
- **Accessibility (non-negotiable)**: tooltip is `role="dialog"` with `aria-live="polite"` so step copy is announced; focus moves to the Next button each step; full keyboard operation (Esc/arrows/Enter); spotlight ring must be readable by **luminance**, not hue — pair the accent ring with a light hairline halo so color-blind and low-color-vision users see the edge regardless of the accent color (never rely on red/green alone anywhere in the tour); the step counter is text ("3/13"), never a color-only progress dot row; honor `prefers-reduced-motion` end to end.
- **Analytics**: if the site has a tracking helper, fire `tour_start`, `tour_step {step}`, `tour_done`, `tour_skip {step}`, and per-mini-tour open events. The per-step funnel (where users bail) is the single most useful signal for iterating the tour.
- **Isolation**: ship as one banner-commented CSS block + one HTML block + one IIFE, touching at most one line of existing code. The feature must be inert until triggered.
- **Deep links & resume (engine, MIT)**: `Toutour.start(steps, {startAt: 3})`
  opens mid-tour — read `?tour`/`?step` from the URL so support can send a
  link that lands the user exactly where help is needed. `Toutour.resume(steps,
  opts)` is `start()` plus continuity: position persists per step under
  `<storageKey>:pos`, a reload within `resumeMaxMin` (default 30) returns to
  the same step, and finishing or skipping clears it so a completed tour never
  comes back. `startAt` is clamped to the FILTERED step list, so a stale deep
  link cannot land on a step whose target no longer exists. Prefer `resume()`
  over `start()` for the auto-show path — losing your place on a refresh is a
  real defect, not a premium feature.
- **False-bottom repair**: when Phase 1 found a first section ≥ ~90vh with no visible continuation, offer `engine/scroll-hint.js` (MIT, bundled) before offering any tour step that says "scroll down": `Toutour.scrollHint({ target: '#hero' })`, loaded after `toutour.js`. It skips mounting when the page is already scrolled, dismisses on first scroll/keys/next-section-visible, never intercepts clicks, and keeps the cue (minus motion) under reduced-motion.

## Phase 5 — Verify (non-negotiable)

Serve the site locally and drive it with Playwright (or the available browser tool) at a desktop viewport AND a mobile viewport:

1. Fresh profile → welcome/trigger behaves per spec; dismiss persists across reload; deep-link visit does NOT auto-show.
2. Step through the ENTIRE tour clicking Next. At every step assert: spotlight rect intersects the target rect; tooltip rect does NOT intersect the spotlight rect; the correct tab/panel became active; spotlight is not degenerate (>4px each dimension).
3. Keyboard: Esc exits, arrows navigate.
4. Every mini-tour, on both viewports, including gated/locked panels in both states.
5. Theme toggle and every language, including switching MID-tour.
6. `prefers-reduced-motion: reduce` → no transitions.
7. **Regression**: with the tour never opened, exercise the site's core flows and assert zero console errors and unchanged behavior.
8. Screenshot key steps (both themes) — attach them to the PR/report. Fix every finding and re-run; report honestly what passed and what you saw.

## Phase 6 — Maintenance (tour health check)

Tours rot: UI refactors silently break selectors and step order ("step drift"). Ship the tour with its own guardrails:

- Commit the step map AND the Phase 5 verification script into the repo (e.g. `tests/tour-verify.*`) so it can run in CI or on demand.
- When asked to "check the tour" (or after any UI change), re-run the verification script. Treat as failures: a selector matching nothing, a 0×0 target, a step whose tab/panel no longer activates, or a step-count change the developer didn't intend.
- When copy or UI changes, update the step map in the same PR as the UI change — a stale tour teaches the previous version of the product.

## Common traps (check each one explicitly)

- A fixed overlay (subnav, cookie bar, FAB) covering the element you spotlight or the "?" entry point on mobile.
- Bottom sheets whose "collapsed" state leaves the target below the fold — snap the sheet per step.
- `element.textContent` lies about visible text when locale spans are CSS-hidden — assert with `innerText`.
- Lazy/conditional targets measured as 0×0 — skip, don't point at nothing.
- Crossing the responsive breakpoint mid-tour when the site relocates DOM — end the tour cleanly on `matchMedia` change.
- Shadow DOM / iframes: `querySelector` won't reach inside; either expose hosts or scope the tour to the light DOM.
