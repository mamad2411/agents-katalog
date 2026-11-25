---
name: responsive-typography
description: Use when type must adapt across viewports, containers, or devices — fluid sizing with clamp(), breakpoint jumps, text that overflows or shrinks illegibly on mobile, headings that wrap badly, or a scale that works on desktop and collapses on phone. Also use when building a type system intended to be resolution-independent.
---

# Responsive typography

The shift Brown argues for: stop designing screens and start designing
*relationships* that hold at any size.

## 1. When to invoke

- Type sizes must change across viewports or container widths.
- Headings wrap badly, overflow, or shrink below legibility on small screens.
- Building a type system meant to work without per-breakpoint overrides.
- Migrating from fixed breakpoint steps to fluid sizing.

**Do not** invoke to choose the base size (`body-text-and-reading`) or the ratio
(`hierarchy-and-scale`). This skill adapts a scale you already have.

## 2. Required context

- The **existing scale** and body anchor.
- **Minimum and maximum viewport** (or container) widths you support.
- Whether sizing should key off the **viewport** or the **container** — a card in a
  sidebar should respond to the sidebar, not the window.
- Whether the component is reused at multiple widths.
- Whether users can zoom, and whether Dynamic Type / user font-size preferences apply.

## 3. Invariant principles

- **Design relationships, not screens.** A fixed size at each breakpoint is a set
  of disconnected designs. Define how size, spacing, and measure move *together*.
- **Everything is interdependent.** Change viewport → measure changes → the size
  and line-height that suited that measure no longer do.
- **Never disable user zoom.** `user-scalable=no` and `maximum-scale=1` violate
  WCAG 1.4.4.
- **Avoid `text-size-adjust` entirely.** `text-size-adjust: none` blocks mobile
  browsers' automatic resizing outright — a real accessibility problem, not a
  theoretical one. `text-size-adjust: 100%` (the common "fix" for iOS
  orientation-change resizing) just suppresses that resize instead of solving
  anything. Browser support and behavior are inconsistent enough that Brown's
  standing recommendation is to leave the property alone rather than reach for it.
  (Don't confuse it with `font-size-adjust`, an unrelated property for matching
  fallback-font apparent size — see `font-loading-and-performance`.)
- **Never size type in raw viewport units alone.** `font-size: 4vw` doesn't respond
  to user zoom at all, because zoom doesn't change viewport units proportionally.
  Always combine with a rem term.
- **Line-height must be unitless** so it scales with the font size it inherits.
- **Larger viewport does not simply mean larger type.** It means a longer available
  measure, which may call for a wider column, more size, or both — decided visually.

## 4. Context-dependent heuristics

**Fluid sizing with `clamp()`.** The correct shape is:

```css
/* min, preferred (must contain a rem term), max */
font-size: clamp(1.5rem, 1rem + 2.5vw, 3rem);
```

The `1rem +` term is not decoration — it's what keeps the text responsive to user
zoom and font-size preferences. `clamp(1.5rem, 4vw, 3rem)` fails WCAG 1.4.4 in the
fluid band.

**Fluid vs. stepped — a real choice, not a default.**

| Use fluid when | Use breakpoint steps when |
|---|---|
| Type should feel continuous across sizes | Sizes must land on exact token values |
| Display/hero type spanning a wide range | Dense UI where an off-token size is a bug |
| Few levels, editorial character | Many levels that must stay distinguishable |
| You can verify the whole band visually | You need discrete, auditable states |

Fluid type is hardest to verify because it has infinite states. Check the two
endpoints *and* several points in between — defects usually live mid-band.

**Container queries over media queries for components.** A component reused in a
main column and a narrow sidebar should key off its container:

```css
.card { container-type: inline-size; }
@container (min-width: 30rem) { .card h2 { font-size: 1.5rem; } }
```

This is the fix for "the card looks right on the page and wrong in the sidebar."

**Scale the ratio, not just the sizes.** A 1.333 ratio that reads well on desktop
is often too dramatic on a phone, where the largest step overwhelms a narrow
column. Compressing the ratio at small sizes usually beats compressing every size
independently.

**Measure is the real constraint.** As the viewport grows, don't let the column
grow with it indefinitely. Cap the measure (`max-width` in `ch` or `rem`) and let
the margins absorb the rest.

**Small screens have a floor.** Roughly 40 CPL is normal on a phone at default
size; don't shrink type to buy characters. Below ~16px body on mobile, tap-target
and legibility problems arrive before typographic ones.

**Derive breakpoints from the type system, not device widths.** Brown's
alternative to picking breakpoints at conventional device sizes (320/768/1024…):
derive them from the typographic decisions you already made.

- **From text-block limits.** If you've set a maximum measure (say 35em) and a
  loosest-case margin (say 5.1em per side at that measure), the point where the
  text block plus margins hits that combined width *is* a defensible breakpoint —
  it's the width where the current setting stops working, not an arbitrary device
  class.
- **From the modular scale.** A number already in your type/spacing scale can
  supply the breakpoint value directly — set measure and margins from separate
  scale steps, or use a larger scale step as the breakpoint itself. There's no
  single correct mapping; treat the scale as a source of candidate values to
  sanity-check a visual decision against, not a formula to solve.

Either way the point is the same: a breakpoint should mark where *pressure* on
the text block (line getting too long, margins going slack) becomes visible, not
where a device category conventionally changes. (Brown)

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Text doesn't grow when the user zooms | `vw`-only sizing | Add a rem term to the `clamp()` preferred value |
| Hero heading is fine at 1440 and 375, broken at 900 | Only endpoints tested | Sweep the middle of the band |
| Card correct on page, wrong in sidebar | Media queries on a reusable component | Container queries |
| Line-height fine large, cramped small | Fixed line-height, or a unit value | Unitless, and consider a larger ratio at small sizes |
| Column keeps widening on ultrawide until unreadable | No measure cap | `max-width` in `ch`/`rem` |
| Body shrunk on mobile to fit more words | Optimizing CPL over legibility | Accept ~40 CPL; keep the size |
| Fluid sizes land off-token | Fluid applied to dense UI | Use stepped sizes for UI, fluid for display |
| Two-word heading becomes 3 ragged lines | No wrap control | `text-wrap: balance` |
| Breakpoints feel arbitrary, chosen at 768/1024 | Picked at device widths, not where the setting fails | Derive from text-block limits or the modular scale |
| iOS text stops resizing on rotation | `text-size-adjust: 100%` used as a "fix" | Remove it; don't reach for `text-size-adjust` at all |

## 6. Evaluation procedure

1. Render at **min supported width, max supported width, and ≥3 points between.**
2. At each, count CPL and confirm the measure is defensible for that width.
3. Zoom to 200% at each. Text must grow. If it doesn't, a `vw` term is unguarded.
4. Test the component in every **container** it's reused in, not just every page.
5. Check the largest heading at the narrowest width for wrapping and overflow.
6. Confirm every `line-height` is unitless.
7. Confirm no `user-scalable=no` / `maximum-scale` in the viewport meta.
8. Re-check hierarchy at the narrowest width — levels often collapse there.

## 7. Output format

```
Strategy: <fluid | stepped | hybrid> — because <reason>
Viewport band: <min> → <max>
Sizing:  <role>: clamp(<min>, <rem term> + <vw term>, <max>)
Query type: <viewport | container> — because <reason>
Measure cap: <value>
Verified at: <list of widths tested>
Zoom 200%: <pass/fail>
Unverified: <what wasn't rendered>
```

## 8. Examples

**Marketing hero, 375→1440.**

> Fluid suits it — one level, wide range, editorial character.
> `clamp(2rem, 1.25rem + 3.5vw, 4rem)`. The `1.25rem` base keeps it zoom-responsive;
> the `3.5vw` term does the travel. Verified at 375/600/900/1200/1440 — at 600 the
> heading was breaking to three lines with a one-word last line, so added
> `text-wrap: balance`. At 200% zoom the text grows correctly.

**Dashboard, same product.**

> Stepped, not fluid. Sizes must stay on token values so an off-scale size is
> detectable as a bug, and the dense scale's steps are small enough that fluid
> interpolation would blur adjacent levels. Two breakpoints, both landing on
> existing tokens.

## 9. Counterexamples

- ❌ `font-size: 4vw` — ignores user zoom entirely. WCAG 1.4.4 failure.
- ❌ `clamp(1rem, 3vw, 2rem)` — same failure inside the fluid band; the preferred
  term needs a rem component.
- ❌ `<meta name="viewport" content="width=device-width, user-scalable=no">` —
  never.
- ❌ "Fluid type means we don't need breakpoints at all." — Layout still changes
  structurally; fluid sizing doesn't reflow a grid.
- ❌ "It works at 375 and 1440, ship it." — The band between is where fluid
  typography breaks.
- ❌ `line-height: 1.5rem` on a fluid size — the ratio inverts as the size grows.

## 10. Source citations

- Brown, *Flexible Typesetting* — **primary source.** Designing systems rather than
  individual screens; typographic relationships across viewport sizes; responsive
  line length; measure as a visual decision; pressure and relief between size,
  spacing, and available space; deriving breakpoints from text-block limits or the
  modular scale instead of device widths; `calc(1em + 2vw)`-style sizing as the
  accessible pattern; warning against `text-size-adjust`.
- Rutter, *Web Typography* — em/rem/ch units; responsive typography; why `ch`
  varies by font and is unreliable for layout.
- Lupton (ed.), *Type on Screen* — mobile and responsive composition; dynamic
  rather than fixed compositions.
- Latin, *Better Web Typography* — responsive web typography; revisiting
  line-height when measure changes.
- WCAG 2.2 §1.4.4 (resize text to 200%).
- MDN — [`clamp()`](https://developer.mozilla.org/en-US/docs/Web/CSS/clamp),
  [container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries),
  [`text-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap).
