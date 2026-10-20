---
name: ui-css-primitives
description: Specifies CSS-level implementation primitives for UI work — OKLCH palette construction, motion duration and easing tokens, interactive and input state coverage, text-on-fill contrast pairing, and framework-agnostic responsive-correctness bugs. Use when writing or reviewing CSS tokens, building a colour palette, implementing interactive or input states, debugging a UI that looks "almost right", or fixing layout that breaks at narrow viewports.
---

# UI CSS Primitives

> [!note] Vault placement
> This is the **implementation layer** under the design cluster. For choosing an
> aesthetic direction use `design-taste-frontend` (build-new, brief inference),
> `high-end-visual-design` / `gpt-taste` (fixed named presets),
> `redesign-existing-projects` (redesign audit), or `improve-ui` (read-only audit
> of an existing surface). For a fast cleanup pass use `baseline-ui`. For live
> Web Interface Guidelines compliance use `web-design-guidelines`.
> Distinguishing axis: **those pick what to build; this specifies how to implement it.**

## What this is

Five things the taste-level skills leave unspecified, because they operate above
the CSS-property level:

| Area | What's specified here |
|---|---|
| **Colour** | Constructing a palette in a perceptual space; pairing text with fills |
| **Motion** | A named duration + easing token system, not raw `cubic-bezier` values |
| **States** | All eight interactive states; the five input-state failures |
| **Responsive** | The correctness bugs no framework fixes for you |
| **Type** | The family ceiling, ratio scale, and headline-size-by-length rule |

## What this is not

Not a style. It contains no opinion about whether a page should be editorial or
brutalist, which fonts express which mood, or how a hero should be composed.
Those choices belong to the taste skills. Everything here is checkable — a
reviewer can point at a line of CSS and say pass or fail.

## Provenance

Distilled from [Nutlope/hallmark](https://github.com/Nutlope/hallmark) (MIT),
which packages these primitives alongside a large amount of house-style opinion.
Only the framework-agnostic, verifiable rules are carried over. Deliberately
**not** imported: its bans on section eyebrows, italic headings, and
hanging/tag-left section heads — those are aesthetic positions, and the vault's
taste skills already own that layer.

Where the upstream overstated a claim, the reference files here say so inline
(APCA's standards status, `grid-template-rows` interpolation support, and the
difference between WCAG 2.5.5 AAA and 2.5.8 AA target sizes are all corrected).

## The non-negotiables

A quick pass. Each line links to the reference that explains it.

**Colour** — [`references/oklch-palette.md`](references/oklch-palette.md)
1. Palette declared in OKLCH, four layers: paper · ink · neutrals · one accent.
2. No pure `#000` / `#fff`; no zero-chroma neutrals. Every neutral carries ≥0.005 chroma toward the anchor hue.
3. Any fill that carries text has a paired ink token, verified against that fill — not against the page background.
4. A section that sets a dark `background-color` sets its `color` in the same rule.

**Motion** — [`references/motion-tokens.md`](references/motion-tokens.md)
5. Animate `transform` and `opacity` only. Never `width`/`height`/`top`/`left`/`margin`/`padding`.
6. Durations and easings come from named tokens, not inline values. Exits ≈75% of enters.
7. Every keyframe and transition has a `prefers-reduced-motion: reduce` path.
8. Focus rings never transition into existence.

**States** — [`references/interactive-states.md`](references/interactive-states.md)
9. Universal states — default · hover · `:focus-visible` · `:active` — exist on every interactive element. Conditional states — disabled · loading · error · success — exist wherever the control can actually enter them. A nav link needs the first four; a submit button needs all eight.
10. Inputs never change `border-width` between states; focus is `outline`, not `border`.

**Responsive** — [`references/responsive-correctness.md`](references/responsive-correctness.md)
11. Overflow is clipped on the specific container that overflows. A global `overflow-x: clip` on `html`/`body` is a last resort, never a substitute for fixing the overflow.
12. Grid tracks holding images use `minmax(0, 1fr)`, never bare `1fr`.
13. Single-line controls (buttons, primary nav) don't wrap. Ordinary links and flexible controls may — the requirement is that nothing overflows or clips, not that nothing wraps.

**Type** — [`references/type-ceiling.md`](references/type-ceiling.md)
14. At most three font families: display + body + one outlier used in ≤2 slots.
15. Heading weight contrasts body weight by ≥300 units.
16. Numeric columns use `font-variant-numeric: tabular-nums`.

## Which reference to load

Load only what the task touches — these are independent.

- Building or reviewing a palette, or fixing a contrast bug → `oklch-palette.md`
- Writing transitions, keyframes, or scroll reveals → `motion-tokens.md`
- Building a button, input, or any interactive component → `interactive-states.md`
- The layout breaks at some viewport, or before shipping any page → `responsive-correctness.md`
- Setting up a type scale, or the headline looks wrong → `type-ceiling.md`

## Framework interaction

Several of these are handled for you depending on the stack. Check before
hand-rolling:

- **Tailwind** ships a 4pt spacing scale and a type scale by default, but both are
  theme variables a project can replace. Read the project's config and reuse
  whatever scale it actually declares rather than adding a parallel set of tokens
  — and don't assume the defaults are still in place.
- **Radix / Base UI / React Aria** own keyboard interaction, focus *behaviour*,
  and focus *state* (the `data-focus-visible`-style hooks). Per `baseline-ui`:
  never rebuild that by hand. They do **not** ship focus *styles* — you still
  write the visible indicator yourself, against the primitive's state hook rather
  than a raw `:focus-visible` selector. Nor do they give you `loading`, `error`,
  or `success` appearances.
- **Nothing** handles the colour construction, the contrast pairing, or the
  responsive bugs in `responsive-correctness.md`. Those are yours regardless of
  stack.

The rules here are written for vanilla CSS because that is the lowest common
denominator. Translate freely into Tailwind's `@theme`, CSS-in-JS, or a
design-token pipeline — the constraint is the output, not the syntax.
