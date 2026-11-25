---
name: threejs-dreamy-glass-hud
description: Turns a three.js scene's DOM overlay into one coherent, dreamlike HUD — a single frosted-glass material shared by every pill, badge and popover whose colours are registered CSS properties so the whole HUD cross-fades from pearl to deep indigo as the scene turns to night; an inline-SVG icon dock whose lit toggles glow gold instead of shouting; a glass popover in place of a native select; first-visit hints "whispered" in handwriting that step aside the moment the visitor understands; a HUD that drifts away after half a minute of stillness; a mote of light under each tap; a staggered arrival after the loading gate; and letterbox bars during a camera tour. Use when the overlay UI looks like a dev panel on top of a beautiful scene, when asked for a dreamy, cinematic, premium or 梦幻 / 绝美 UI, glassmorphism, a day/night-aware HUD, onboarding hints, auto-hiding UI, tap feedback, or to restyle lil-gui to match.
---

# A dreamlike glass HUD for a WebGL scene

A hand-painted scene is easily let down by its overlay: a native `<select>`, unicode glyphs for icons, five pill
styles that grew one feature at a time. This skill replaces all of that with **one material and a few manners**:

- **One glass.** Every pill, badge, popover and prompt reads the same tokens. Night swaps the tokens, not the rules.
- **It follows the sky.** The tokens are registered colours, so `body` can transition them: the HUD crosses from
  pearl to indigo over the same seconds the scene does.
- **Quiet by default.** Lit toggles glow; nothing is a filled disc. After 28 s of stillness the HUD drifts away.
- **It speaks in the scene's voice.** Hints, toasts and view names arrive in handwriting out of a soft blur.

Stack: plain CSS + ~40 lines of DOM JS over a three.js canvas. No framework. In R3F keep the HUD outside `<Canvas>`
and call `ui.step()` from `useFrame`.

## When to use

- The 3D looks finished and the UI does not.
- The scene has a day/night or weather state the UI ignores (pearl pills over a midnight river).
- Visitors don't discover what they can do, or the UI never gets out of the way.

## Paste-ready prompt

> Restyle the DOM overlay of `{{entry file}}` as one dreamlike glass HUD, without changing what any control does:
> - Define glass tokens (`--glass`, `--glass-hi`, `--edge`, `--text`, `--text-soft`, `--gold`, `--glow`, `--shade`)
>   with `@property` so they can transition; `body.night` overrides them; toggle that class when the scene's night
>   blend crosses .5. Every pill, badge, popover and prompt uses the tokens — no literal colours left in the HUD.
> - Replace glyph icons with inline SVG (24 px viewBox, `stroke:currentColor`, 1.6 px round strokes). A lit toggle
>   takes the gold and a small glowing dot under it; group the dock with thin separators.
> - Replace `{{native select / settings control}}` with a glass popover opened from a dock button; keep the
>   original control hidden as the state holder.
> - First visit only: whisper `{{2–3 hints}}` one at a time in the handwriting font, each leaving when the
>   visitor does the thing it describes. Never during reading, touring or steering.
> - After 28 s without input, fade the whole HUD out; any pointer, key, wheel or touch brings it back.
> - A tap (not a drag) on the canvas leaves a small ring and a few sparks at the pointer.
> - After the loading gate lifts, bring the HUD in piece by piece over ~2 s.
> - During the camera tour, slide in two soft letterbox bars.
> - Respect `prefers-reduced-motion`, safe-area insets, and 36–38 px touch targets. Verify at 1440×900 and 390×844,
>   by day and by night, in every language the page ships.

## Implementation

### One glass, registered (`references/glass-tokens.css`)
- Register each colour: `@property --glass { syntax:'<color>'; inherits:true; initial-value:… }`. An unregistered
  custom property cannot be interpolated; a registered one can, so
  `body { transition: --glass 1.8s, --text 1.8s, … }` animates every element that reads it — with no per-element
  transition rules, and without fighting the opacity/transform transitions those elements already have.
- Numbers that worked over a bright, busy scene: day `--glass rgba(255,250,240,.52)`, `--glass-hi …,.86` (popovers,
  hover, anything with body text); night `rgba(14,24,52,.46)` / `rgba(20,32,66,.84)`; text `#22302a` → `#f4ecd8`;
  gold `#c8743a` → `#ffd28a`. `backdrop-filter: blur(14px) saturate(1.35)`; a popover over flowers needs
  `blur(22px) saturate(1.1)` or the petals show through the words.
- One shadow for everything: `0 10px 34px var(--shade), inset 0 0 0 1px var(--edge), inset 0 1px 0 var(--edge)`.
- Drive it from the render loop, on change only:
  `const n = night.k > .5; if (n !== isNight) body.classList.toggle('night', isNight = n)`. Also set
  `<meta name="theme-color">` so a phone's browser chrome follows.

### The dock
- Inline SVG inside each button plus an empty `<i>` for the light: `fill:none; stroke:currentColor;
  stroke-width:1.6; stroke-linecap:round`. Glyph characters (☀ ☾ ♪ ⚙) come from whatever font the OS has: two of
  them looked identical and none matched the scene.
- **On** = `color: var(--gold)` + `drop-shadow(0 0 5px var(--glow))` on the icon + the dot scaling in. With three
  toggles lit by default, filled orange discs were the loudest thing on screen.
- Separators are `<hr>` (1 px × 16 px, `currentColor` at .16). Tooltip from `::before { content: attr(data-label) }`;
  left-align the first button's tooltip so it cannot leave the screen; hide tooltips on coarse pointers.
- A button whose icon changes with state (weather) swaps `button.firstElementChild.innerHTML`, never `textContent`
  (that would delete the dot).

### A popover instead of a native select
- Keep the `<select hidden>` and its `onchange`: the popover's radio buttons set `select.value` and call it. Nothing
  downstream changes.
- Open state on a class; `transform-origin` at the button; close on outside `pointerdown` and Escape; stop
  `pointerdown` inside it from reaching the canvas.
- Each choice gets one plain line of what it means ("the sharpest picture"), and a note if choosing has a cost
  ("switching reloads the scene").

### Whispers (`references/hud-manners.js`)
- One element, one line at a time: opacity 0 → .96, `blur(8px)` → none, `letter-spacing .12em → .03em`, 1.1 s.
- A queue of `[text, ms]`. Wait 1.3 s between lines; if the HUD is busy (reading, tour, steering, a popover open)
  the line is skipped, not delayed into an unrelated moment.
- The first hint leaves early on the controls' `start` event — the visitor has dragged, so they know.
- `localStorage` marks them seen. Capture runs (`?silent`) get none, with a `?whisper` override for testing.
- Reuse the same blur-in for toasts and for the view name when a number key switches views.

### Stillness
- One `last = performance.now()` updated by capture-phase, passive `pointermove / pointerdown / keydown / wheel /
  touchstart` listeners. In the frame loop: after 28 s and not busy, add `body.admire`.
- `body.admire` sets `opacity:0 !important; pointer-events:none !important; transition:opacity 2.6s` on the HUD
  roots and `cursor:none` on the canvas. `pointer-events:none` matters on touch: the tap that wakes the HUD must
  not also press an invisible button.

### Tap sparkle
- `pointerdown` stores position and time; `pointerup` within 6 px and 450 ms appends `<i class="spark">` at the
  pointer and removes it after 850 ms. The ring is a scaled box-shadow; the five sparks are one pseudo-element
  whose `box-shadow` list animates outward. Skip under pointer lock and reduced motion.

### Arrival and the tour
- On enter: add `body.entering` for 3.2 s. Under it only `transition-delay` differs (counters 1.1 s, language
  1.3 s, dock 1.5 s, wordmark 1.8 s), so the same fade rules stagger once and never again.
- Letterbox: two fixed pseudo-elements, 8.5 vh (6 vh in portrait), a gradient that is solid for 55 % and then
  fades, `translateY(∓101%)` → none over 1.6 s under `body.touring`. The tour caption sits just above the lower bar
  and the "tap to explore" hint inside it.

### The tuning panel
- lil-gui reads CSS variables: set `--background-color`, `--title-background-color`, `--widget-color`,
  `--number-color`, `--text-color`, `--font-family` on `.lil-gui.root`, add the same `backdrop-filter` and a 14 px
  radius, and it stops looking like a different app.

## Pitfalls

- **Descendant selectors leak into the popover.** `#toggles button { width:36px; border-radius:50% }` also styled
  the popover's buttons (it lives inside the dock so it can anchor to it) and gave each a tooltip. Use
  `#toggles > button` for the dock's own buttons.
- **A centred box is not centred text.** A block placed with `left:50%; transform:translateX(-50%)` holds
  left-aligned lines: a short headline sat visibly left of the longer small print under it. Give it
  `text-align:center; width:max-content; max-width:88vw`, and `text-wrap:balance` for anything that may wrap.
- **Transitions on a class lose to ID rules.** Putting `transition: background 1s` on a shared `.glass` class is
  overridden by each element's own `transition:` shorthand. Animating the registered properties on `body` avoids
  the conflict entirely.
- **Glass that is right at night is too thin by day.** `.36` alpha over sunlit flowers left dark icons unreadable;
  `.52` with icons at .8 opacity held. Check the dock over the brightest and busiest part of the frame.
- **Mobile width is a budget.** Eight 38 px buttons, three separators and padding are ~355 px of a 390 px screen
  with 12 px gutters. Count before adding a ninth; drop the separators under 380 px.
- **Two top-row pills collide on a phone** once their padding grows. Pin one to each side below 640 px.
- **A whisper behind a translucent popover is still legible.** Hide it with
  `body:has(#popover.open) #whisper { opacity:0 }`.
- **Local static servers may drop the query string.** `npx serve` redirects `/index.html?lang=zh` to `/`, so a
  translated or flagged page silently tests as the default. Navigate to `/?lang=zh` and assert `location.search`.

## Verify

- Screenshot (DOM included, so `page.screenshot`, not `canvas.toDataURL`) at 1440×900 and 390×844: gate, entered,
  popover open, night, tour, reading, each language.
- Night: `body.night` flips once as the blend crosses .5 and every glass element changes together.
- Wait 28 s untouched: HUD gone; move the pointer: back. On touch, the waking tap presses nothing.
- Tap leaves one `.spark`; a drag leaves none.
- Second visit: no whispers. `prefers-reduced-motion`: no blur-ins, no sparks, no pulsing.
- Frame time unchanged (this is all DOM/CSS; `backdrop-filter` on a handful of small elements was free here).

## References

- `references/glass-tokens.css` — tokens, night override, dock, popover, whisper, stillness, spark, letterbox.
- `references/hud-manners.js` — night class, whisper queue, stillness timer, tap sparkle, popover wiring.

## Related skills

threejs-hud-objective-markers (the badges and fly-to this dresses) · threejs-cinematic-loading-screen ·
threejs-camera-guided-tour · threejs-ghibli-night-mode · threejs-headless-visual-verification
