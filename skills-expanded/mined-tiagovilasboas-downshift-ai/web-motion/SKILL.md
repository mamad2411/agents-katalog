---
name: web-motion
description: Smooth, high-impact web motion on the compositor. Use for web animation, scroll effects, "make it smooth", and agent-swarm or cursor build effects.
---

# Web motion

Add motion on top of the page that exists. Never redesign it to make an effect
fit. Inspired by the MIT-licensed `emilkowalski/skills` (animate,
animation-performance) and `mblode/agent-skills` (ui-animation); the text here
is original.

## Hard rules

1. **Compositor only.** Animate `transform`, `translate`, `opacity`,
   `clip-path` and `filter`, on small elements. Never width, height, top, left,
   margin or box-shadow.
2. **Cheapest tool first.** CSS transition, then WAAPI (`el.animate`), then CSS
   keyframes, then per-frame JS. `requestAnimationFrame` only for drags and
   physics, where the value depends on input.
3. **Layout: read once, batch.** Measure once per action, do all reads before
   all writes, and keep the numbers in variables.
4. **Banned in a frame loop:** animated CSS mask gradients, `getClientRects` or
   `getBoundingClientRect` polling, a full-viewport canvas with `shadowBlur`.
5. **`will-change` only on the few nodes moving right now**, removed when done.
6. **Hide until built** with `visibility:hidden`, not `display:none`: the space
   stays, CLS stays 0.
7. **Progressive enhancement.** Content is visible if JS fails. The script adds
   the hidden state, so a crash leaves a readable page.
8. **`prefers-reduced-motion: reduce`** renders the final state at once, with
   no movement and no flicker.
9. **`@media (pointer: fine)`** gates hover and cursor extras. Touch gets none.
10. **Interruptible.** A new action cancels or retargets the running one from
    its current value. Never queue behind a stale animation.
11. **Register every animation** in a per-section list. A skipped or off-screen
    section calls `finish()` on all of them and lands in the final state.
12. **Generation token.** Each replay bumps a counter; every loop and timer
    checks it and exits when it is stale.
13. **CSP-friendly.** External script and style files, no inline handlers or
    inline `<style>`; set styles through CSSOM or classes.

## Easing and duration

- Default curve `cubic-bezier(.55, 0, .15, 1)`; for entrances
  `cubic-bezier(.16, 1, .3, 1)`.
- Duration follows distance:
  `clamp(260, 200 + dist * 0.4, 720)` ms (dist in px). Small UI feedback:
  120-200 ms. Nothing above 720 ms unless it is a showpiece.
- Stagger 30-60 ms per item, capped at about 400 ms total.

## Recipe: the agent swarm builds the page

Keep each stage in its own small module (overlay, agent, build queue, fills).

1. **Overlay layer.** One fixed, `pointer-events:none`, high z-index container.
   Agents, selection boxes and the tour pill live there, never inside content.
2. **Cursor agents.** Each is an inline SVG arrow plus a name pill in the
   agent's colour, moved only with `transform: translate3d`.
3. **Boot.** Agents fly in from the edges, orbit once, then disperse to their
   first sections. About 1.5-2 s total, skippable.
4. **Per-section build, two phases, from one shared queue** (each free agent
   takes the next unclaimed block of the section, staggered 60-70 ms):
   - *Frame:* a selection box with corner handles and a `W x H` tag grows from
     the section's top-left while the agent's cursor rides the bottom-right
     corner. The box then settles into a skeleton.
   - *Fill:* the skeleton fades and the real content appears by type: text
     types in; headings flicker in per letter with a neon glow; photos reveal
     with a `clip-path` wipe; everything else fades.
5. **Nudge-drag.** Once in a while an agent grabs an element, moves it a few
   pixels and drops it on a snap guide line. It is a decoration: it must end
   exactly where the layout puts the element.
6. **Copy-drag ghost** for repeated cards: drag a translucent clone to the next
   slot, then fill it. Build the first card fully, ghost the rest.
7. **Scroll trigger.** Start a section when its top crosses about 62% of the
   viewport. At most one section ahead of the one on screen. Fast scrolling
   speeds the current section up and `finish()`es the ones scrolled past.
8. **Idle conga.** With no work left, a leader follows a Lissajous path and the
   others follow its position history with a fixed lag per agent. Stop on the
   first pointer move or scroll.
9. **Tour pill.** A fixed pill with agent avatars, a section count, a progress
   bar, a status line, a tour button, speed 1x/2x/4x, pause and replay. Speed
   scales every duration through one shared factor. Replay bumps the generation
   token and rebuilds.
10. **Mobile.** At 375 px use about a third of the agents, no conga on touch,
    no nudge-drag, shorter boot.

## UX rules on a product page

A portfolio can make the visitor wait; a product page cannot.

- The LCP element stays painted from first paint. Decorate it, never hide it.
  Measure LCP with and without the effect; it must not regress.
- Primary calls to action are visible and clickable at once. Overlays never
  take pointer events.
- Any click, key or scroll in a section finishes it instantly.
- Full build on the first visit only; later visits get the final page and a
  Replay control. Keep query switches to force or skip it for demos and QA.
- Focus never lands in a hidden block: focusing one finishes its section.
  Announce "building" and "ready" once, not per block.
- Idle motion stops by itself after about 20 s. Nothing moves forever on a page
  people read.
- Let the motion tell the product's story, once, subtly; decoration alone is
  animation debt.

## Verify, do not eyeball

- **Frame pacing:** record rAF deltas for 10 s of scroll and build; report p95
  and the count above 20 ms. Target p95 under 17 ms.
- **Long tasks:** `PerformanceObserver({type:'longtask'})`; none during the
  build is the goal.
- **CLS:** observe `layout-shift`; the total must be 0.
- **Reduced motion:** emulate `prefers-reduced-motion: reduce`; the page must
  be complete and still.
- **Phone:** run at 375 px wide with touch emulation; no horizontal scroll.
- **Production CSP:** inject the real `Content-Security-Policy` header and
  confirm nothing is blocked.
- **Trace A/B:** capture a CDP trace with and without the effect and compare
  ScriptDuration, Layout, RecalcStyle, Paint and Layerize counts and durations.
  Repeat with 4x CPU throttle. Headless vsync hides dropped frames, so compare
  work per frame, not only the worst frame time.
- **JS off:** the content must still read.

## Anti-patterns from a rejected attempt

Measured in headless Chrome over 6 s, overlay running vs the page alone:
script 117 vs 9 ms, layout 113 vs 29 ms, style 167 vs 97 ms, paint 177 vs 95 ms,
893 vs 397 layouts. Each cause below has its fix.

| Cause | Fix |
|---|---|
| Per-frame CSS mask gradients on large text (multi-layer mask per line) | `clip-path: inset()` or a `scaleX` cover per line, driven by WAAPI |
| Re-measuring on a timer (`getBoundingClientRect`, `Range.getClientRects`, `scrollHeight`, canvas resize, read/write/read) | Measure on resize, `document.fonts.ready` and `ResizeObserver` only; read everything, then write once |
| Per-frame `width`/`height` writes on highlight boxes; unguarded `textContent` writes | Size once, animate `transform: scale`; write text only when it changed; cache DOM refs |
| Full-viewport canvas cleared every frame at DPR 1.5 with `shadowBlur` and per-frame gradients | For a few beams use SVG or a transformed pre-rendered glow; else DPR 1, dirty rect, no `shadowBlur` |
| Overlay layer as tall as `scrollHeight` with many promoted children | Per-section layer, or one viewport-fixed layer |
| `filter: drop-shadow` on moving elements; blurred `box-shadow` on resizing boxes | Bake the glow into the asset; put the shadow on a wrapper that does not resize |
| `backdrop-filter` on a fixed pill over animated content | Near-opaque background, no blur |

Also rejected:

- Redesigning the page to suit the effect. Motion is added on top of the
  existing layout and content; remove the script and the page is unchanged.
- No final state for skipped sections, so fast scrollers saw empty blocks.
- Loops that survived a replay and fought the new run.

Downshift by Tiago Vilas Boas · https://github.com/tiagovilasboas/downshift-ai
