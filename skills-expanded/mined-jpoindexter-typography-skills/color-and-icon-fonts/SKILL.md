---
name: color-and-icon-fonts
description: Use when type needs to be more than one flat colour, or when glyphs carry non-letter meaning — layer fonts, colour fonts (COLRv1, OT-SVG, bitmap), CSS font-palette, icon fonts, emoji. Also use when deciding between an icon font and SVG, when a colour font renders as flat black, or when emoji or icons break in a screen reader.
---

# Colour and icon fonts

Two capabilities the rest of the pack assumes away: type that carries **more than
one colour**, and glyphs that carry **non-letter meaning**. Both are font
technology, both have sharp accessibility edges, and both are chosen far more often
than they should be.

## 1. When to invoke

- Type must render in more than one colour, with gradients, or as a 3D/layered effect.
- Choosing between an icon font and inline SVG.
- Emoji rendering, sizing, or weighting.
- A colour font renders as flat black in some browsers.
- Icons or emoji are announced wrongly by a screen reader.

**Do not** invoke for ordinary text colour (that's CSS `color`) or for choosing a
text face (`typeface-selection`).

## 2. Required context

- **What the colour is doing** — brand expression, information, or decoration.
  Only the first two usually justify the cost.
- **Which browsers must render it correctly**, and what the acceptable degradation is.
- Whether the glyphs are **decorative or meaningful** (drives the a11y treatment).
- Whether the text must remain **selectable, searchable, and translatable**.
- Icon count, and whether icons change at runtime.

## 3. Invariant principles

- **Colour fonts degrade, they don't fail — but the degradation is the design
  decision.** Plan what the flat-colour fallback looks like, because some readers
  will only ever see that.
- **Never let colour carry meaning alone.** Same rule as everywhere else; a colour
  font doesn't exempt you from WCAG 1.4.1.
- **Icons that carry meaning need an accessible name**; icons that are decorative
  must be hidden from assistive technology. There is no third option.
- **A glyph is not a picture to a screen reader.** An icon-font character is
  usually announced as a meaningless codepoint from the Private Use Area, or as
  nothing at all.
- **Layered type must stay legible in one colour.** If the layers only resolve into
  readable letters when all colours are present, the fallback is illegible.

## 4. Context-dependent heuristics

### Layer fonts vs. colour fonts

Stocks: they are different but "effectively work towards the same goal: to move
beyond 'flat' colors when setting type."

**Layer fonts** are ordinary font files that "break out different layers into
styles." You duplicate the text, set each copy in a different style, and overlay
them — each layer in its own colour. Chouquet's *Lustik* uses a Back style of
hand-drawn squares and a Front style of abstract shapes that only read as letters
once combined. Clarke's *Rig Shaded* ships Face, Extrude, Shadow, and two Shading
styles that build a three-dimensional object. Blend modes on the layers extend this
further.

- **Pros:** total control per layer; works anywhere; each layer is a normal font.
- **Cons:** duplicated text nodes (an accessibility and DOM problem on the web),
  brittle alignment, and the text is repeated for screen readers unless hidden.
- **On the web:** acceptable for a one-off display headline; not for body or UI. Mark
  all but one layer `aria-hidden="true"`.

**Colour fonts** keep everything in one file — no duplicated text — at the cost of
per-layer control.

| Format | State in 2026 |
|---|---|
| **COLRv1** | The one to use. Paint graph with linear/radial/sweep gradients, transforms, compositing, blending, and **variation data for the colour construction itself** — so variable colour fonts are real. Renders in Chromium, Firefox, Samsung Internet. **Safari falls back to a single solid colour.** |
| **OT-SVG** | Avoid for new work. **Chromium has stated it will never support it**, and Firefox has signalled it may drop it. |
| **sbix / CBDT (bitmap strikes)** | Raster; resolution-bound. Mostly emoji legacy. |

**`font-palette` is the reason COLR matters.** It lets a page select a palette from
a colour font, and `@font-palette-values` lets you override individual entries or
define your own:

```css
@font-palette-values --brand {
  font-family: "Nabla";
  override-colors: 0 #1a1a1a, 1 #e63946;
}
.headline { font-family: "Nabla"; font-palette: --brand; }
```

This is COLR-only. It means one font file can be re-themed per brand or per dark
mode without shipping another file.

### Icon fonts vs. SVG

**Default to SVG.** Icon fonts were a workaround for an era without good SVG
support, and they carry real defects:

| Icon font problem | Consequence |
|---|---|
| Glyphs live in the Private Use Area | Screen readers announce garbage or nothing |
| Fails as a font failure | Font blocked/slow → missing or tofu icons, not degraded ones |
| Single colour only (unless COLR) | No multi-tone icons |
| Anti-aliased as text | Icons shift with font smoothing, not pixel-tuned |
| Whole set ships as one file | Pay for 300 icons to use 12 |

Choose an icon font only when you genuinely need glyph behaviour — icons inline in
text that must inherit `font-size`, `color`, and baseline alignment automatically,
across a very large icon set. Then:

- `aria-hidden="true"` on the glyph, with a real text label adjacent, **or**
  `role="img"` plus `aria-label`.
- Never put meaning only in the glyph.
- Provide a fallback so a failed font load doesn't erase the UI.

**Emoji.** Stocks' point in §89 is that icons and symbols "are like type — and often
are fonts," and they behave like type: Noto Emoji ships weights whose stroke
thickness changes to suit context. Practical notes: emoji render per-platform and you
do not control the artwork; they carry a screen-reader name that is often verbose
(🎉 → "party popper"); and they should never be the sole carrier of meaning or state.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Colour font renders flat black in Safari | COLRv1 unsupported there | Design the single-colour fallback deliberately |
| Colour font renders flat everywhere | OT-SVG in Chromium | Use COLRv1 |
| Layered headline is illegible without colour | Layers only resolve when combined | Ensure one layer carries the letterform |
| Screen reader reads the headline three times | Duplicated layer text nodes | `aria-hidden` on all but one |
| Icons vanish on slow connections | Icon font failed to load | SVG, or a fallback |
| Screen reader says "private use area 61489" | Icon glyph with no accessible name | `aria-hidden` + text label, or `role="img"` + `aria-label` |
| Icon-only button unusable by keyboard/AT | No accessible name | Add one |
| 400 KB icon font for 12 icons | Whole set shipped | SVG sprite or subset |
| Emoji means "done" and nothing else does | Meaning carried by glyph alone | Add text |
| Colour font can't be re-themed for dark mode | Palette baked in | `font-palette` / `@font-palette-values` |

## 6. Evaluation procedure

1. State what the colour or icon is **for**. Decorative → hide it from AT.
   Meaningful → it needs a text equivalent.
2. Render in a browser **without** COLRv1 support (Safari) and confirm the flat
   fallback is acceptable, not broken.
3. Render with **fonts blocked entirely.** Icons and layered type must not take the
   interface with them.
4. Run a screen reader over it. Nothing should be announced as a codepoint, and
   nothing meaningful should be silent.
5. Check contrast of the rendered result — gradients mean the ratio varies across
   the glyph; test the worst point.
6. Grayscale it. Does anything stop making sense?
7. Weigh the payload against the number of glyphs actually used.
8. If re-theming is needed, confirm `font-palette` works rather than shipping a
   second file.

## 7. Output format

```
Purpose: <brand expression | information | decoration>
Technique: <layer font | COLRv1 | OT-SVG ✗ | bitmap | SVG | icon font>
  because <reason>
Fallback (no COLR support): <what renders> — acceptable: <yes/no>
Fonts-blocked behaviour: <what renders>
A11y: decorative → aria-hidden | meaningful → <accessible name>
Contrast at worst point: <ratio>
Palette themable: <font-palette | baked in>
Payload: <n> KB for <n> glyphs used
```

## 8. Examples

**Brand wants a gradient, dimensional headline face.**

> Two routes. A **layer font** like Rig Shaded gives per-layer control — Face,
> Extrude, Shadow — but on the web it means duplicated text nodes, so all but one
> copy needs `aria-hidden` and the alignment is brittle at fluid sizes. A **COLRv1**
> colour font keeps it to one text node with real gradients, and `font-palette` lets
> dark mode re-theme it without a second file. Recommending COLRv1 — but the
> deciding question is Safari, which falls back to a single solid colour. Design that
> flat state first and confirm the brand still holds; if it doesn't, the effect is
> wrong for this surface regardless of technique.

**"Should we use an icon font or SVG for our 40 product icons?"**

> SVG. Forty icons doesn't justify the icon-font tradeoffs: PUA codepoints that
> screen readers mangle, icons disappearing entirely if the font fails, single-colour
> only, and shipping the whole set to use a subset. The one case that would flip this
> is icons inlined mid-sentence that must inherit size, colour, and baseline
> automatically — that's genuine glyph behaviour and SVG handles it worse. Not the
> case here.

## 9. Counterexamples

- ❌ "Use an OT-SVG colour font for the hero." — Chromium has said it will never
  support OT-SVG. Most of your traffic gets flat colour.
- ❌ "Colour fonts degrade gracefully, so no fallback design is needed." — The
  fallback *is* a design state; Safari users only see it.
- ❌ "The icon is obvious, it doesn't need a label." — Obvious to sighted users
  looking at it. A screen reader gets a codepoint.
- ❌ `aria-hidden="true"` on an icon that is the button's only content. — Now the
  button has no accessible name at all.
- ❌ "We'll ship two font files for light and dark palettes." — `font-palette` and
  `@font-palette-values` re-theme one COLR file.
- ❌ Layering four copies of a headline in the DOM with no `aria-hidden`. — The
  headline is read four times.
- ❌ "✅ means the step is complete." — with no text saying so.

## 10. Source citations

- Stocks, *Universal Principles of Typography* — §89 "icons & symbols are like type
  — and often are fonts" (Noto Emoji's weights changing stroke thickness to suit
  context); §90 "expand your palette with layer fonts & color fonts" — layer fonts
  and colour fonts "effectively work towards the same goal: to move beyond 'flat'
  colors when setting type"; layer fonts "break out different layers into styles" so
  you "duplicate our text box and select a different style for each one"; Chouquet's
  *Lustik* (Back/Front styles resolving into legible characters) and Clarke's *Rig
  Shaded* (Face, Extrude, Shadow, Shading building a three-dimensional object);
  blend modes; colour fonts keeping all options in one file.
- **Current standards take precedence on support.** COLRv1 renders in Chromium,
  Firefox, and Samsung Internet; **Safari falls back to a single solid colour**.
  Chromium has stated it will not support OpenType-SVG; Firefox has signalled it may
  drop it. COLRv1 carries a paint graph (linear/radial/sweep gradients, transforms,
  compositing, blending) plus variation data for the colour construction itself.
  MDN — [`font-palette`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-palette),
  [`@font-palette-values`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-palette-values).
- WCAG 2.2 §1.1.1 (non-text content), §1.4.1 (use of colour), §1.4.3 (contrast).
