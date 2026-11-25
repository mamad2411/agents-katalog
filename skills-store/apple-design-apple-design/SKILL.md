---
name: apple-design
description: >-
  Build web interfaces (HTML/CSS/JS, React, Vue, Tailwind) that look and feel
  like Apple made them — the real Apple aesthetic, not generic glassmorphism.
  Covers Liquid Glass / iOS-26 materials as rendered CSS+SVG (specular
  highlights, refraction, vibrancy, fallbacks), Apple's fluid-motion physics
  (springs by damping/response, velocity handoff, momentum projection,
  interruptibility, rubber-banding) implemented in BOTH Motion (motion.dev) and
  GSAP (Flip, ScrollTrigger, SplitText, Inertia), SF typography optics, a
  drop-in Apple design-token layer, and complete copy-paste components (glass
  nav, spring bottom sheet, segmented control, toasts, popovers). USE THIS SKILL
  whenever the user wants something to look "Apple-like", "like iOS/macOS",
  "clean and premium", "polished", "Apple-quality"; mentions Liquid Glass,
  frosted/translucent/glass UI, backdrop blur, SF Pro, iOS-style springs or
  sheets/drawers, Apple-style scroll animations, or a bottom sheet; or asks you
  to design/build/restyle/review a landing page, app UI, nav bar, modal, card,
  or animation and premium fit-and-finish matters — even if they don't say the
  word "Apple". Prefer this over generic UI advice for any high-polish web UI.
---

# Apple Design (for the web)

Build interfaces with Apple's fit and finish: fluid, physical motion; translucent
materials with real depth; and the optical typography and restraint that make
software feel considered. This skill is **web-first** (HTML/CSS/JS, React, Vue,
Tailwind) and **build-first** — it exists to help you *make* Apple-grade UI, with
concrete numbers and copy-pasteable code, not just describe principles.

## The one idea that generates everything

Apple UI feels alive because it behaves like a **physical object under glass**:

> Motion starts from the value that's on screen *right now*, inherits the user's
> velocity, projects momentum to where the gesture was going, and can be grabbed
> and reversed at any instant. Surfaces are translucent layers that catch light
> and cast depth. Type is optically tuned so it reads effortlessly. And nothing
> is added that doesn't serve the content.

Every technique below is downstream of that. When a choice is unclear, ask:
*would a physical object behave this way? does this material catch light? does
this detail serve the content or decorate it?*

## What "Apple" actually means (and the traps)

Getting this right is mostly avoiding the things that read as *almost* Apple:

- **It's physics, not durations.** Anything the user can touch uses a **spring**,
  not a CSS `transition` with a fixed time. Springs interrupt and reverse; fixed
  transitions snap and fight the user.
- **Glass is layered light, not just blur.** A real material = translucency +
  saturation boost + a **specular top-edge highlight** + a hairline rim + soft
  depth shadow. Blur alone is 2020 glassmorphism, not Apple 2025.
- **Type is optically tuned, not one font.** Letter-spacing **tightens as size
  grows**; line-height **loosens as size shrinks**; optical sizing is on. A single
  global `letter-spacing` is the #1 non-Apple tell.
- **Restraint is the aesthetic.** Fewer, more meaningful animations. No animation
  on things done 100×/day. Content over chrome. Delight is the *result* of the
  other principles done well, not glitter added on top.
- **Respond instantly.** Feedback on pointer-**down**, never only on release. Kill
  debounces and transition-delays on interactive feedback.

## Do this first, every time

1. **Establish the token layer.** Import `assets/tokens.css` (or the Tailwind v4
   bridge `assets/tailwind.css`). It gives you Apple's real colors, type scale,
   spacing, radii, shadows, materials, and motion easings — with dark mode and
   accessibility fallbacks already wired. Reference tokens (`var(--label)`,
   `var(--accent)`, `--space-5`) instead of hardcoding values. This alone makes a
   UI coherent and theme-able. → details in `references/tokens.md`.
2. **Pick the material and type roles** from the semantic tokens before styling.
3. **Decide motion per surface** using the decision guide below.
4. **Build with the component recipes** rather than reinventing them.
5. **Verify in a browser** (see Verification) — Apple polish is judged by eye.

## Routing — read the reference for the depth you need

Load only what the task needs (progressive disclosure). Each file is dense and
self-contained:

| You're working on… | Read |
|---|---|
| Colors, type scale, spacing, radii, shadows, dark mode, squircles | `references/tokens.md` (+ `assets/tokens.css`) |
| Frosted/translucent/glass surfaces, Liquid Glass, specular, refraction, vibrancy | `references/liquid-glass.md` |
| Any interactive motion — springs, drag, sheets, velocity, momentum, interrupt | `references/motion-physics.md` (the model) |
| Implementing that motion in Motion/motion.dev (gestures, layout, React) | `references/motion-dev.md` |
| Scroll-driven/pinned sequences, shared-element/Flip, headline reveals | `references/gsap.md` |
| Fonts, tracking, leading, optical sizing, hierarchy | `references/typography.md` |
| Ready-made parts: nav, bottom sheet, segmented control, toast, popover, buttons | `references/components.md` |
| Tailwind setup | `assets/tailwind.css` + the Tailwind notes in each file |

## Motion decision guide — which tool, which config

**Should this move at all?** Only if it clarifies cause/effect, shows spatial
relationships, or provides feedback. Skip animation on high-frequency actions.

**Spring or transition?**
- User can grab/drag/reverse it, or it must interrupt → **spring** (Motion).
- Fire-and-forget entrance, hover, simple state → CSS transition with a token
  easing (`--ease-out`, never `ease-in`) is fine and cheap.

**Motion vs GSAP?**
- Gesture-driven, interruptible, per-component, React layout/presence → **Motion**.
- Scroll-pinned hero, shared-element/grid reflow (**Flip**), per-line headline
  (**SplitText**), throwable with **Inertia** → **GSAP**.
- Don't load both for one small job; choose per surface.

**Spring config (defaults):** critically damped `{ type:"spring", bounce:0,
visualDuration:0.3–0.4 }` for most UI; add `bounce:0.15–0.25` only when a gesture
carried momentum. Apple's ship values: reposition 1.0/0.4, rotation 0.8/0.4,
sheet/drawer 0.8/0.3. Full derivation and the velocity/momentum/rubber-band math
are in `references/motion-physics.md`.

## Non-negotiables (accessibility & performance)

These aren't optional polish — Apple ships them, and skipping them breaks real
users. The token layer handles the defaults; honor them per component too:

- **Animate only `transform` and `opacity`.** Never animate layout properties.
- **`prefers-reduced-motion: reduce`** → replace springs/slides with short
  opacity crossfades; keep instant tap feedback. (Gentler, not gone.)
- **`prefers-reduced-transparency`** → drop glass to a solid background.
- **`prefers-contrast: more`** → add real borders to glass/edges.
- **Contrast** ≥ 4.5:1 for body text, including *through* glass. Touch targets
  ≥ 44px. `focus-visible` outlines on every control.
- **`-webkit-` prefix** on `backdrop-filter` for Safari, always.

## Verification — judge by eye, then iterate

Apple quality is visual; don't declare it done from the code alone. If a browser
tool is available (Playwright MCP, or the user's `browser-harness`), **render the
result, screenshot it, and inspect**: Does glass show a lit top edge and float
above content? Do interactions spring and interrupt rather than snap? Is large
text tracked tight, small text tracked open? Check **both light and dark**, a
narrow viewport, and reduced-motion. Fix what looks off and re-screenshot. One
honest look beats ten confident assumptions.

## Tailwind guidance

Use Tailwind (v4) for **structure** — spacing on the 8pt grid, the type scale,
layout, color — via the `@theme` bridge in `assets/tailwind.css`, so utilities
like `bg-material-regular text-label rounded-lg` are backed by the same tokens
that drive dark mode. Keep **Liquid Glass materials** (the `.glass` component
layer) and **interruptible JS springs** in dedicated CSS/JS — layered specular
shadows and SVG refraction don't belong in arbitrary-value utility strings.
Structure in Tailwind, signature material + motion in CSS/JS.

## Provenance & credit

The fluid-motion model draws on Apple's WWDC talks — *Designing Fluid Interfaces*
(2018), *The Details of UI Typography* (2020), *Principles of Great Design*
(2026). The web translation of Apple's springs and easing owes a debt to Emil
Kowalski's `apple-design` / `emil-design-eng` skills, which pioneered quantifying
these for the web. This skill extends that lineage with rendered **Liquid Glass**
materials, first-class **GSAP** coverage, a drop-in **token layer**, and
complete **components** — the parts prior skills left open.
