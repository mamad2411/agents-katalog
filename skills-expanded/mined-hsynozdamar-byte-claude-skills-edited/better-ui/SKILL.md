---
name: better-ui
description: "Visual polish for UI code: radii, optical alignment, shadows, icons, press feedback, small motion. Use when building or polishing components, or when something looks slightly off."
---

# UI polish

Polish is many small details that compound. Keep the project's components, tokens, density and motion language. The values here are tested defaults, so use them as written when the project has nothing of its own, rather than a familiar-looking substitute.

When reviewing motion, slow it down (10% in the browser's Animations panel). What feels off slowly is subtly wrong at full speed.

Text rendering belongs to `better-typography`, hit areas and reduced motion to `better-accessibility`, grouping and spacing to `better-layout`.

## Surfaces

- **Concentric radius.** Outer radius = inner radius + padding (card `rounded-2xl p-2` holds `rounded-lg`). Same radius on both is the most common "feels off" cause. Past about `24px` of padding the layers read as separate surfaces; pick radii independently.
- **Optical alignment.** Icon-side padding = text-side padding minus `2px` (`ps-4 pe-3.5` for a trailing icon). Play triangles shift right about `2px`. Fix asymmetric icons (stars, carets) in the SVG first, a `translate-x-px` wrapper second.
- **Shadows for depth, borders for structure.** Where a border only creates elevation on cards, buttons or popovers, a layered transparent shadow adapts to any background. Keep borders for dividers, table cells, inputs and selected or focus states.
- **Image outlines.** `1px` outline, `-1px` offset: `oklch(0 0 0 / 0.1)` light, `oklch(1 0 0 / 0.1)` dark (`outline-black/10 dark:outline-white/10`). Use pure black or white, not slate or zinc: a tinted outline picks up the surface and reads as dirt on the edge.

Shadow tokens and recipes: [references/surfaces.md](references/surfaces.md).

## Icons

- Stroke follows adjacent text weight: `1.5px` beside 400, `2px` beside 500 to 600, `2.5px` beside bold. One library and one stroke convention per surface.
- One SVG with `currentColor`; hover, selected and disabled come from CSS color and opacity. Strip hardcoded fills on import.
- Outline is the default state, fill the active state. Don't use them interchangeably.
- Size inline icons at `1em` to `1.25em`, on the set's native grid (16, 20, 24), and check them at the smallest render size.

Load [references/icons.md](references/icons.md) for RTL flipping rules and the icon cross-fade code.

## Motion

- **Interruptible.** CSS transitions (or springs) for interactive state, because they retarget mid-flight. Keyframes only for one-shot sequences.
- **Restraint.** High-frequency interactions (typing, row hover, tab switches) get instant feedback or at most `150ms` on opacity and color. Save expressive motion for rare moments. Every animated change also leaves a static cue (color, icon, label).
- **Press.** `scale(0.96)` on `:active`, `150ms ease-out`. Below `0.95` feels exaggerated. Offer a `static` prop to turn it off.
- **Contextual icon swap.** Scale `0.25` to `1`, opacity `0` to `1`, blur `4px` to `0`. With `motion`/`framer-motion` (match the import already used): `{ type: "spring", duration: 0.3, bounce: 0 }`. Without one, keep both icons in the DOM and cross-fade with `cubic-bezier(0.2, 0, 0, 1)` over `300ms`; don't add a dependency for this.
- **Enter.** Only for infrequent staged entrances: split into semantic chunks (title, text, actions), stagger about `100ms` (words in a title about `80ms`), combine opacity, `translateY(12px)` and `blur(4px)`.
- **Exit.** Softer and shorter than enter: small fixed `translateY(-12px)`, about `150ms ease-out`. Remove instantly when motion adds no information.
- **First render.** `initial={false}` on `AnimatePresence` stops toggles animating on load. Don't use it where the entrance itself is the point (hero stagger).
- **Theme switch.** Disable all transitions during the swap, force a reflow, remove on the next frame, or the page smears. `next-themes` has `disableTransitionOnChange`.
- **Performance.** Name transitioned properties (`transition-[scale,opacity]`), never `transition: all`. `will-change` only on `transform`, `opacity` or `filter`, and only after you see first-frame stutter.

Code for each: [references/motion.md](references/motion.md).

## Reporting (standalone)

`HIGH`: breaks an interaction or leaves a state visible only during animation. `MEDIUM`: visible inconsistency in surfaces, icons or motion. `LOW`: isolated polish. One row per root cause: Severity, Location (`path:line`), Before, After, Why. Check every defined state (hover, focus, active, loading, empty); mark what you couldn't run `Not verified`. End with `Block` if any `HIGH`, else `Approve`.
