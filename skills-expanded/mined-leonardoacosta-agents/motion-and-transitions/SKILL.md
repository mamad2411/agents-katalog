---
name: motion-and-transitions
description: Add production-grade CSS transitions and micro-animations to web UIs — card resizes, menu dropdowns, modals, page slides, icon swaps, text swaps, notification badges, panel reveals, number pop-ins. Ships nine copy-ready CSS snippets with a unified curve language and `prefers-reduced-motion` guards. Do not use for layout, state machines, or React component logic — only motion/timing.
when_to_use:
  - The user asks to "animate", "add a transition", "smooth out" any UI element
  - The user mentions easing/spring/timing, or asks for "Apple-feel"/"polished" interactions
  - The user requests motion for any of the nine canonical patterns
  - The user names a specific pattern without saying "transition" (e.g. "make the menu open nicely", "the modal should pop in")
allowed-tools: Read, Glob, Grep
---


# Motion & Transitions

This skill ships a small library of production CSS transitions adapted from
[transitions.dev](https://transitions.dev) (Jakub Antalik). The point is not
to memorize nine snippets — it is to internalize the **motion language** they
share, so you can apply it correctly and extend it to patterns the library
does not cover.

## When to use this skill

Reach for this skill whenever a UI element changes state visibly: opening,
closing, swapping, sliding, resizing, appearing, disappearing. If a designer
or user asks for any of the nine patterns by name — or describes the
interaction in plain English — paste from `assets/`, then tune.

If the request is about layout, data flow, accessibility semantics that are
not motion-related, or React state, this skill is the wrong tool. Hand off.

## The motion language (read this first)

The library uses two primary curves plus a neutral closer. Internalize them:

| Curve | `cubic-bezier(...)` | When to use | Feel |
|---|---|---|---|
| **Out-quint** (decelerate) | `(0.22, 1, 0.36, 1)` | The workhorse. Ambient transitions: open/close, resize, slide, swap. | Confident arrival, quiet exit |
| **Spring overshoot** | `(0.34, 1.36, 0.64, 1)` | Attention moments: badge pop-in, icon swap, anything that should feel *alive*. | Bouncy, playful |
| **Ease-in-out** (closing) | `(0.4, 0, 0.2, 1)` | Closing/exit transitions when the spring is too loud. | Neutral |

Pair these with **short durations** (150–500ms). Anything longer than 500ms
on a UI transition feels sluggish unless it is intentionally cinematic
(page-level navigation can stretch to 600–700ms). For a **per-element** ceiling
(button press 100–160ms, tooltip/popover 125–200ms, dropdown 150–250ms,
modal/drawer 200–500ms) — a granular table this skill previously lacked, per
the binding canon eval in `evals/canon-eval/REPORT.md` — see
`references/emil-craft-canon.md`. Never `ease-in` on an entrance (starts slow,
delays the moment the user is watching); never `scale(0)` on an entrance
(start from `scale(0.9–0.97)`) — both are review-bar rules this skill also
lacked before that reference. `ease-drawer` (`cubic-bezier(0.32, 0.72, 0, 1)`,
an iOS-like drawer curve) is a genuinely new fourth curve, not a competing
value for out-quint/spring/ease-in-out above — see the reference for when to
reach for it.

The reason out-quint is the workhorse: it *front-loads motion* and settles
gently. The eye registers the change quickly, then the element comes to rest
without jitter. Linear and standard ease-in-out both feel mechanical by
comparison; bounces are too loud for ambient changes.

## Craft canon & review bar

`SKILL.md` teaches HOW to animate. Two references cover the rest:

- **`references/emil-craft-canon.md`** — WHETHER to animate (a 4-question decision gate:
  frequency/purpose/speed/function; reject-by-default), the ten-standard review bar + block
  criteria, the 9-step remedial hierarchy (delete beats reduce beats polish), performance rules,
  and gesture values. Load it before reviewing any animation diff, or before proposing new motion
  in a functional/high-frequency surface.
- **`references/apple-fluid-interfaces.md`** — spring physics (damping/response), momentum
  projection, rubber-banding, materials, and typography for gesture-driven UI (drag, swipe,
  sheets, drawers). Load it when implementing anything the user can grab and interrupt.

## The snippet contract

Every snippet in `assets/` follows the same three-part contract. **Preserve
this contract** when generating new patterns:

1. **`:root` token defaults** — semantic names (`--badge-pop-dur`, not
   `--p1-scale-open-dur`). Override on `:root` or any tighter scope to
   re-skin without touching the rules.
2. **`t-*` namespaced classes** — the class is a *trait* you apply to your
   own components. Do not rename `t-modal` to match your component class;
   compose: `<div class="my-modal t-modal is-open">`.
3. **`@media (prefers-reduced-motion: reduce)` guard** — required, not
   optional. Cuts transitions to zero for users who request it (vestibular
   disorders, focus mode, battery saving). A snippet without this guard is
   a bug.

If you find yourself omitting any of these three, stop and reconsider.

### NEVER: content invisible by default

Never gate content's EXISTENCE on an entrance animation firing. Three mechanisms have all
shipped blank sections when the reveal didn't fire (hydration hiccup, backgrounded tab,
IntersectionObserver never triggering): CSS `animation-timeline: view()`, IntersectionObserver
class toggles, and Framer `initial={{ opacity: 0 }}`. Content is visible by default; animate
`transform`/`opacity` on already-visible elements instead of gating visibility on the animation.
If an entrance reveal is genuinely wanted, it MUST ship with a no-JS fallback that still renders
the content — never a bare `opacity: 0` starting state with nothing to guarantee it flips.

## The nine patterns

| Pattern | File | What it is | Curve |
|---|---|---|---|
| Card resize | `assets/card-resize.css` | Smooth width/height transitions on a container | Out-quint |
| Number pop-in | `assets/number-pop-in.css` | Digit flips with blur + stagger (counters, prices) | Spring + ease-in-out |
| Notification badge | `assets/notification-badge.css` | Diagonal slide-in with spring pop (unread dots) | Spring (pop) + out-quint (slide) |
| Text swap | `assets/text-swap.css` | Y-axis blur swap between two text states | ease-out |
| Menu dropdown | `assets/menu-dropdown.css` | Origin-aware scale/fade open & close | Out-quint |
| Modal open/close | `assets/modal.css` | Scale up to 100% with backdrop fade | Out-quint |
| Panel reveal | `assets/panel-reveal.css` | Slide-out side/bottom panel | Out-quint |
| Page side-by-side | `assets/page-slide.css` | Forward/back page navigation | Out-quint |
| Icon swap | `assets/icon-swap.css` | Scale + blur cross-fade between two icons | Spring |

### Picking a pattern

- "Make X open" with a clear anchor (a button, a corner) → **menu-dropdown**
  or **modal**. Use dropdown when X is anchored to its trigger; use modal
  when X is centered and dims the background.
- "Make X slide in from the side" → **panel-reveal**.
- "Animate counters / number changes" → **number-pop-in**.
- "Toggle between two icons / text strings" → **icon-swap** / **text-swap**.
- "Indicate something is new / unread" → **notification-badge**.
- "Resize a container without snap" → **card-resize**.
- "Animate between two routes / steps" → **page-slide** (CSS-only, same tab) or **View Transition API** (cross-route, browser-native). See below.

If the request does not match a pattern, do not force-fit. Compose from the
motion language above (out-quint, 150–400ms, reduced-motion guard) and write
a fresh rule.

## Workflow

1. **Pick the pattern, read the asset, paste it.** Use the decision table
   above to choose; load with `Read("assets/<pattern>.css")`; paste verbatim
   into the user's stylesheet (the `:root` block can sit anywhere). Compose
   the class alongside the user's existing class — `<div class="filter-modal
   t-modal">` — don't rename `t-modal`.
2. **Tune the tokens, not the rules.** If the modal feels too slow, override
   `--modal-open-dur` on a tighter scope (e.g. `.filter-modal { --modal-open-dur: 180ms; }`).
   Do not edit the transition declarations themselves.
3. **Wire the state.** Most snippets switch on `data-state` / `data-open` /
   `data-page` attributes or `is-open` / `is-closing` classes. Your
   component's open/close handler toggles those — the CSS does the rest.

### Worked example: filter modal

User: *"Build a filter modal that opens when the user clicks 'Filter'.
Should feel polished — the modal should pop out from the button."*

This is `modal` (centered overlay), and "pop out from the button" is the cue
to set `data-origin` based on the trigger's screen position.

```html
<button id="filter-trigger" type="button">Filter</button>

<dialog class="filter-modal t-modal" data-origin="top-left">
  <h2>Filter results</h2>
  <!-- modal contents -->
</dialog>
```

```css
/* paste assets/modal.css verbatim, then tune tokens for this instance */
.filter-modal {
  --modal-open-dur: 220ms; /* default 280 — small modal can be quicker */
}
```

```js
const trigger = document.getElementById('filter-trigger');
const modal = document.querySelector('.filter-modal');

trigger.addEventListener('click', () => {
  // Decide origin from the trigger's screen position so the scale-up
  // grows from the corner closest to the click. Without this the modal
  // scales from its own center — readable but disconnected.
  const r = trigger.getBoundingClientRect();
  modal.dataset.origin =
    r.left < window.innerWidth / 2 ? 'top-left' : 'top-right';
  modal.classList.add('is-open');
});

modal.addEventListener('click', (e) => {
  if (e.target !== modal) return; // backdrop click only
  modal.classList.add('is-closing');
  modal.addEventListener('transitionend', () => {
    modal.classList.remove('is-open', 'is-closing');
  }, { once: true });
});
```

The `data-origin` swap right before the open is the polish line. The CSS
handles every other detail — duration, easing, opacity, the `is-closing`
asymmetry, the reduced-motion guard.

## Origin awareness (the part LLMs usually get wrong)

For `menu-dropdown` and `modal`, the snippet sets `transform-origin` based
on a `data-origin` attribute. **This matters.** A dropdown anchored to a
button in the top-right of the screen should scale-up FROM its top-right
corner, not from its top-left default. The `data-origin` values are:

```html
<ul class="t-dropdown" data-origin="top-right">…</ul>
<ul class="t-dropdown" data-origin="bottom-center">…</ul>
```

When you wire the dropdown, set `data-origin` based on where the trigger
sits relative to the menu. This is the single most common motion mistake in
generated UI code: scaling in from the wrong corner makes the open feel
detached from the click, even when timing and easing are correct.

## Extending the library

When the user asks for a pattern not in the nine, follow the contract:

1. Define semantic CSS variables at `:root` (duration, distance, ease, blur).
2. Use **out-quint** for the open/exit unless the element is calling for
   attention (then spring).
3. Set `transform-origin` if the element appears from a specific anchor.
4. Wrap the rule body in classes prefixed `t-<your-pattern>`.
5. Add a `@media (prefers-reduced-motion: reduce)` guard.

Example — a "drawer slide-up from bottom" not in the library:

```css
:root {
  --drawer-dur: 280ms;
  --drawer-distance: 24px;
  --drawer-ease: cubic-bezier(0.22, 1, 0.36, 1);
}

.t-drawer {
  transform: translateY(var(--drawer-distance));
  opacity: 0;
  pointer-events: none;
  transition:
    transform var(--drawer-dur) var(--drawer-ease),
    opacity   var(--drawer-dur) var(--drawer-ease);
}
.t-drawer.is-open {
  transform: translateY(0);
  opacity: 1;
  pointer-events: auto;
}

@media (prefers-reduced-motion: reduce) {
  .t-drawer { transition: none !important; }
}
```

## Things to avoid

- **Don't compose into existing rules.** The snippets are designed to drop
  in alongside, not merge with, existing component styles. Composability
  comes from the `t-*` namespace, not from rewriting selectors.
- **Don't lengthen durations to "make it smoother".** If a transition feels
  abrupt, the issue is usually the curve (try out-quint), not the duration.
- **Don't drop the reduced-motion guard.** Even on prototypes. It is one
  line and is the difference between accessible and not.
- **Don't apply spring easing to ambient transitions.** Saving overshoot
  for attention moments is what keeps the language coherent. If everything
  bounces, nothing draws the eye.
- **Don't generate Tailwind utility versions inline.** Tailwind's `transition`
  utilities cannot express custom cubic-beziers without `tailwind.config`
  changes. If the user wants Tailwind, paste the `cubic-bezier` value into
  their config's `transitionTimingFunction` and reference it as
  `transition-[curve-name]`. Or just use the snippets as raw CSS — the
  `t-*` classes coexist cleanly with Tailwind classes.
- **Don't write new patterns to `assets/`.** The nine snippets there are the
  canonical reference and stay frozen. When extending the library, return
  the new snippet inline in the user's stylesheet — never add files to
  `assets/`.

## Page-Level Transitions: View Transition API

The nine CSS patterns above handle **component-local** state changes. For **cross-route** animations — where elements persist or content morphs across a full page navigation — use React's `<ViewTransition>` component instead.

### When to use which

| Situation | Tool |
|---|---|
| Modal opens/closes within a page | `t-modal` (CSS, this skill) |
| Dropdown, panel, card resize | CSS patterns (this skill) |
| Element morphs between two routes | `<ViewTransition name="…">` (View Transition API) |
| Skeleton → content on load | `<ViewTransition exit="…">` + `<ViewTransition enter="…">` |
| Forward/back page slide | `<Link transitionTypes={['nav-forward']}>` + `<ViewTransition>` |
| Same-route content crossfade | `<ViewTransition key={slug} share="auto">` |

### Quick reference

Requires `experimental: { viewTransition: true }` in `next.config.ts` and React 19.

```tsx
import { ViewTransition } from 'react'

// Shared element morph — same name on both pages animates position/size
<ViewTransition name={`photo-${id}`}>
  <Image src={src} alt={alt} />
</ViewTransition>

// Directional nav — tag links, map types to CSS classes
<Link href="/photo/1" transitionTypes={['nav-forward']}>…</Link>
<ViewTransition
  enter={{ 'nav-forward': 'slide-in', default: 'none' }}
  exit={{ 'nav-forward': 'slide-out', default: 'none' }}
  default="none"
>
  {children}
</ViewTransition>
```

CSS pseudo-elements: `::view-transition-old(.class)`, `::view-transition-new(.class)`, `::view-transition-group(.class)`.

**Always guard reduced motion** (same rule as CSS patterns):

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(*), ::view-transition-new(*), ::view-transition-group(*) {
    animation-duration: 0s !important;
    animation-delay: 0s !important;
  }
}
```

Full patterns (Suspense reveals, directional slides with CSS, crossfades): load `nextjs-app-router` skill § View Transitions.

## Diagnosing Jank

The nine patterns above are compositor-safe by construction. If a *custom* animation feels
janky — scroll-driven effects, imperative JS loops, animated blur — load
`references/perf-triage.md` for the rendering-steps glossary, the never-patterns
(polled-scroll, unbounded rAF, large blur/backdrop-filter), before/after fixes, and the FLIP
technique for layout-triggering changes that can't be avoided.

## Attribution

Patterns adapted from [transitions.dev](https://transitions.dev) by Jakub
Antalik. The site does not publish a formal license but explicitly markets
each snippet with a copy button — the intent is reuse. When shipping
commercially or in publicly attributed work, credit the source.
