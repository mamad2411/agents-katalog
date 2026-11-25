---
name: type-foundations
description: Use when typographic vocabulary or first principles are needed — what an em actually is, font vs typeface, leading vs line-height, points vs pixels, how CSS units relate, what the em square means. Also use when someone is confidently using a term incorrectly, or when an explanation needs grounding before a decision is made.
---

# Type foundations

The vocabulary and measurement system everything else depends on. Most
typographic mistakes at the decision level trace back to a wrong model here.

## 1. When to invoke

- A term needs defining before a decision can be made.
- Someone conflates font/typeface, leading/line-height, or point/pixel.
- Choosing CSS units for type.
- Explaining a typographic decision to a developer or client.

**Do not** invoke when the decision is already scoped — go to the specific skill.

## 2. Required context

- The **medium** — print units and screen units are related but not equivalent.
- The audience's **existing vocabulary**, so you correct only what matters.

## 3. Invariant principles

**Typeface vs. font.** A *typeface* is the design (Helvetica). A *font* is a
specific instance of it that you use (Helvetica Bold 12pt; a `.woff2` file).
Historically a font was one size of metal type. The distinction matters in
licensing and in file inventories.

**Glyph vs. character.** A *character* is the abstract unit (the letter "a"); a
*glyph* is a drawn form. One character may have many glyphs (small cap, oldstyle,
alternate); one glyph may represent several characters (the `fi` ligature).

**The em square is the design space.** An em is not the width of "M" — it's the
full body of the type, historically the metal block. Glyphs are drawn within it and
may fill it generously or sparsely, which is why **two typefaces at the same point
size render at visibly different apparent sizes.**

**Point size measures the body, not the letters.** Nothing in a font is guaranteed
to be exactly the point size. This is why apparent size must be judged visually.

**Leading vs. line-height.** *Leading* is historically the extra metal strip added
*between* lines. CSS `line-height` is the **total** line box — the font size plus
the space distributed above and below. So `font-size: 16px; line-height: 24px`
means 8px of added space, not 24px. Don't use the terms interchangeably when
precision matters.

**Half-leading.** CSS splits the difference between line-height and font size
equally above and below the text. This is why text sits with extra space above the
cap-height and below the baseline — and why `text-box-trim` exists.

**Legibility vs. readability.** *Legibility* is glyph-level: can a reader tell
characters apart at all — `1 l I`, `0 O o`, `q p`, `d b`. *Readability* is text-level:
whether the whole passage is comfortable to get through, which legibility feeds but
doesn't determine — tracking, leading, measure, and plain boring content all affect
readability independent of the typeface. A legible face can still be unreadable if
poorly set; the two questions get asked and fixed differently. (Stocks)

## 4. CSS units for type

| Unit | Relative to | Use for |
|---|---|---|
| `rem` | Root font size | **Default for type sizes.** Respects user preference, predictable |
| `em` | The element's own font size | Spacing that must scale with local text (margins on a heading) |
| `px` | Device pixel (CSS px) | Borders, hairlines. **Avoid for type sizes** — historically blocked user text scaling and remains less preference-responsive |
| `ch` | Width of the `0` glyph | Rough measure caps only — **varies per font**, so unreliable for layout (Rutter) |
| `ex` | The font's x-height | Rare; occasionally useful for optical alignment |
| `%` | Parent | Compounding; use with care |
| `vw`/`vh` | Viewport | **Never alone for type** — ignores user zoom. Only inside `clamp()` with a `rem` term |
| unitless | Font size, at compute time | **Always for `line-height`** — inherits proportionally |

**Why unitless line-height.** A unitless value is inherited as a *ratio* and
recomputed against each element's own font size. A `px` or `em` line-height is
computed once and inherited as a fixed length, so a larger child gets a line box
too small for it.

## 5. Context-dependent heuristics

- **Root font size is the user's setting.** The common default is 16px, but users
  change it. Sizing in `rem` honours that; sizing in `px` doesn't.
- **Points for print, pixels/rem for screen.** 1pt = 1/72in. CSS px is a
  reference pixel, not a hardware pixel — on high-DPI screens one CSS px covers
  several device pixels.
- **`text-box-trim` / `text-box-edge`** remove the half-leading so text can be
  aligned by cap-height or x-height rather than by line box — the long-standing
  "why is there mystery space above my heading" fix. Chrome/Edge 133+, Safari
  18.2+, not Firefox as of mid-2026; ~80% availability, not Baseline. Degrades
  silently to today's behavior, so it's safe progressive enhancement.

## 6. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| "Set leading to 24px" | Leading/line-height conflated | State which; prefer unitless line-height |
| Child text has a cramped line box | `line-height` in px or em | Unitless |
| User's larger text setting ignored | `px` type sizes | `rem` |
| Measure cap drifts when the font changes | `ch` treated as stable | `ch` varies per font; verify or use `rem` |
| Same pt size, different apparent size | Point size measures the body | Compare x-heights |
| Unexplained space above a heading | Half-leading | `text-box-trim`, or negative margin as fallback |
| "Font" and "typeface" used interchangeably in a licence discussion | Terms conflated | Be precise; licensing depends on it |

## 7. Evaluation procedure

1. Identify which term is actually meant, and restate it precisely.
2. Check every `line-height` is unitless.
3. Check type sizes are in `rem` (or `clamp()` containing a `rem` term).
4. Check no `vw`-only type sizing.
5. If `ch` is used for measure, confirm it was verified with the shipping font.
6. Confirm the root font size isn't hardcoded in a way that defeats user
   preference.

## 8. Output format

```
Term clarified: <term> = <precise definition>
Units: sizes in <unit> · line-height <unitless?> · measure in <unit>
Issues: <list>
Implication: <what changes as a result>
```

## 9. Examples

**Developer asks: "the designer said 16/24 — do I set `line-height: 24px`?"**

> The intent is a 1.5 ratio, so set `line-height: 1.5` unitless, not `24px`. Two
> reasons. First, a px line-height is inherited as a fixed length: a child at 32px
> would get a 24px line box, which is smaller than its own text. Second, unitless
> recomputes per element, so the ratio survives every size in the scale. Also worth
> naming: "16/24" is *line-height*, not leading — leading is the 8px added between
> lines, and the distinction matters if you're ever translating a print spec.

## 10. Counterexamples

- ❌ "An em is the width of the capital M." — It's the full type body; the M
  connection is historical coincidence.
- ❌ "Set line-height in px for precise control." — Breaks inheritance.
- ❌ "Use `px` so text renders consistently." — Consistency at the cost of ignoring
  the user's text-size preference.
- ❌ "`ch` is the character width, so `65ch` is 65 characters." — `ch` is the `0`
  glyph's advance width and varies per font; the rendered count will differ.
- ❌ "16px is the standard body size." — It's the common browser *default*, which
  the user may change, and apparent size varies by typeface.
- ❌ "Leading and line-height are the same thing." — Related, offset by the font
  size, and the difference matters when translating print specs.
- ❌ "It's legible, so it's readable." — Legibility is glyph-level distinction;
  readability also depends on tracking, leading, measure, and content. (Stocks)

## 11. Source citations

- Lupton, *Thinking with Type* 3e — typeface vs. font; anatomy and alignment;
  typographic conventions and their history.
- Rutter, *Web Typography* — em, rem, and ch as the primary tools for adaptive web
  type; the caution that `ch` "varies from font to font so it's not usually
  suitable for layout purposes"; "a pixel is not a pixel" and subpixel rendering.
- Stocks, *Universal Principles of Typography* — the em square "at the heart of it
  all"; font metrics; characters vs. glyphs; legibility (glyph-level distinction,
  tested via `1lI`/`0Oo`/`qp`/`db`) vs. readability (text-level, also driven by
  tracking, leading, measure, and content) as related but distinct questions.
- Latin, *Better Web Typography* — anatomy vocabulary; practical unit use.
- Hochuli, *Detail in Typography* — the line and linespacing as craft terms.
- MDN — [`line-height`](https://developer.mozilla.org/en-US/docs/Web/CSS/line-height),
  [`text-box-trim`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-box-trim)
  (Chrome/Edge 133+, Safari 18.2+, not Firefox as of mid-2026).
