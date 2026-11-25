---
name: ui-component-typography
description: Use when setting type inside interface components — buttons, labels, inputs, form errors, navigation, badges, tooltips, tables, dense dashboards. Also use when numbers jitter in a table, labels wrap unpredictably, UI text is illegible at small sizes, or a component's text breaks in another language.
---

# UI component typography

Interface text is scanned and acted on, not read continuously. Different failure
modes from body copy, and different rules.

## 1. When to invoke

- Typography inside buttons, labels, inputs, nav, tables, badges, tooltips.
- Numbers misaligning or jittering in tables or dashboards.
- Labels wrapping, truncating, or overflowing.
- Dense product UI where vertical space is contested.

**Do not** invoke for running prose (`body-text-and-reading`) or editorial layout
(`editorial-web-typography`).

## 2. Required context

- The **densest** screen the component appears on.
- **Longest realistic string** for every label — in every supported language.
- Whether text is **user-generated** (unbounded length).
- Whether numbers are **compared vertically** (tables, ledgers) or read singly.
- Touch vs. pointer, and the minimum touch target.
- Whether the platform provides **Dynamic Type / OS text scaling**.

## 3. Invariant principles

- **UI text is scanned, not read.** Optimise for recognition speed and
  unambiguity, not reading comfort over long passages.
- **Tabular figures are mandatory wherever numbers align vertically.** Proportional
  figures have varying widths, so digits won't form columns. Lining + tabular is
  the combination for tables. (Lupton, Hochuli, Santa Maria)
- **`1 l I` and `0 O` must be distinguishable** in any interface showing codes,
  IDs, quantities, or currency.
- **Every label must survive its longest translation.** German and Finnish
  routinely run 30–40% longer than English.
- **A label is not a placeholder.** Placeholder-as-label disappears on focus and
  usually fails contrast.
- **Text must survive the WCAG 1.4.12 spacing override** — dense components are
  where this breaks first.
- **Truncation is a last resort and must be recoverable** — never truncate the only
  copy of information without a way to see it.

## 4. Context-dependent heuristics

**Sizing.** UI text usually runs smaller than body copy because it's scanned, not
read — but small type raises the cost of a poor typeface. At 12–14px, aperture and
counter behavior matter more than at 16px. Prefer a face with open apertures and a
generous x-height for UI (see `typeface-anatomy`). Don't drop below ~12px for
anything carrying meaning; never for anything a user must act on.

**Line-height in components.** Tighter than body text — a single-line label doesn't
need 1.5. Around 1.2–1.35 for single-line UI strings, but note this is *component*
line-height, not the paragraph rule. Any multi-line text inside a component reverts
to body-text logic. WCAG 1.4.12 still requires the layout to survive a 1.5 override.

**Figure styles — the four combinations.**

| | Tabular (uniform width) | Proportional (varying width) |
|---|---|---|
| **Lining** (cap height, uniform) | Tables, dashboards, prices, data | Buttons, single values in UI |
| **Oldstyle** (ascenders/descenders) | Rare | Running prose, editorial text |

```css
.table-numeric { font-variant-numeric: tabular-nums lining-nums; }
.prose         { font-variant-numeric: oldstyle-nums proportional-nums; }
```

Full tag/property lookup in `../type/references/opentype-features.md`.

Lining figures are usually cap height or slightly less and are normally set on a
constant (en) body, which is what makes them tabular-capable (Hochuli).

**Multiplexed typefaces solve the hover-reflow problem.** In most families a heavier
weight is also wider, so bolding a nav item or a tab on hover shifts everything
after it. A **multiplexed** face is designed so every weight occupies exactly the
same horizontal space — "a word set in a light weight will take up the exact same
horizontal space as a word set in a heavy weight" (Stocks §31). Nothing moves.

Where a multiplexed face isn't available, the alternatives in order:

1. A variable font's **`GRAD` (grade)** axis — changes apparent weight without
   changing width. See `variable-fonts`.
2. Reserve the bold width up front (render the bold string invisibly to size the
   container, or set `min-width`).
3. Signal the state with something other than weight — colour, an underline, a
   background.

Never let a hover state reflow a navigation bar.

**Labels and truncation.** Design for the longest string first. Options, in order of
preference: allow wrapping; allow the container to grow; shorten the copy; truncate
with the full value available on hover/focus/detail. Truncating by default because
the design assumed English is a localisation bug.

**Alignment in tables.** Numbers right-aligned (or decimal-aligned) so magnitudes
compare; text left-aligned for a familiar entry point into reading; a column of
icons or single glyphs centered, to avoid the lopsided look a left or right rag
gives a symbol column. Headers match their column's data alignment. (Lupton,
*Type on Screen*)

**Case.** Use `text-transform: uppercase` rather than typing capitals, so screen
readers, search, and translation receive the real string. Add tracking whenever you
do — see `microtypography`.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Numbers jitter/shift between rows | Proportional figures | `font-variant-numeric: tabular-nums` |
| Prices don't line up | Not decimal-aligned | Right- or decimal-align |
| Button text wraps in German | Sized to English | Test longest locale; allow growth |
| Label vanishes when typing | Placeholder-as-label | Real `<label>` |
| `0` vs `O` confusion in codes | Ambiguous digits | Face with disambiguated digits |
| Dense table unreadable at 200% zoom | Fixed row heights | `min-height`, intrinsic sizing |
| Layout collapses under 1.4.12 override | Fixed heights in dense components | Let containers grow |
| Screen reader spells out a nav item | Literal capitals typed in source | `text-transform` |
| Error message truncated | Fixed-height container | Let it grow; errors are critical |
| Text illegible at 11px | Too small, closed apertures | Raise size; choose an open-aperture face |

## 6. Evaluation procedure

1. Render each component with its **longest realistic string** in the **longest
   supported locale**.
2. Render with the **shortest** string too — components often break empty.
3. In any table: confirm `tabular-nums`, and confirm numeric columns align.
4. Check `1 l I` / `0 O` in the shipping face at the shipping size.
5. Apply the WCAG 1.4.12 override; confirm nothing clips or overlaps.
6. Zoom to 200%; confirm no loss of content or function.
7. Check contrast for *every* state — placeholder, disabled, hover, error.
8. Confirm touch targets meet minimum size independent of text size.
9. Check any truncation has a recovery path.

## 7. Output format

```
Component: <name>
Size/line-height: <n>/<n> — rationale: <scan vs read, density>
Figures: <lining|oldstyle> + <tabular|proportional> — because <alignment need>
Longest string tested: "<string>" (<locale>) — <fits|wraps|truncates>
Digit disambiguation: <1lI ok?> <0O ok?>
1.4.12 override: <pass/fail> · 200% zoom: <pass/fail>
Contrast by state: default <n> · placeholder <n> · disabled <n> · error <n>
Truncation: <none|recoverable via …>
```

## 8. Examples

**Dashboard table where "the numbers look wobbly".**

> The face defaults to proportional figures, so `1` is narrower than `8` and the
> digits don't form columns — the wobble is real, not perceptual. Fix is
> `font-variant-numeric: tabular-nums lining-nums` on numeric cells plus
> right-alignment so magnitudes compare down the column. Verified the face actually
> ships a `tnum` set (some don't, in which case the fallback is a monospace numeric
> face for those cells).

**Primary button breaking in German.**

> "Save changes" → "Änderungen speichern" is 22 characters vs 12. The button has a
> fixed width sized to English, so the German string truncates. Fix in order:
> remove the fixed width and let the button size to content with a `min-width`;
> allow two-line wrapping with a tighter component line-height; only then consider
> shorter copy. Verified at 200% zoom and under the 1.4.12 override — with the
> fixed width removed, both pass.

## 9. Counterexamples

- ❌ "Use the placeholder as the label to save space." — Disappears on input, usually
  fails contrast, and breaks screen-reader association.
- ❌ "Set the button width so the layout stays consistent." — Guarantees a
  localisation failure.
- ❌ "Body line-height is 1.5, so use 1.5 everywhere." — Single-line UI labels don't
  need paragraph leading; but the layout must still *survive* a 1.5 override.
- ❌ "Numbers are fine, the font looks aligned." — Verify `tabular-nums` explicitly;
  proportional figures can look aligned in one sample and drift in another.
- ❌ "Truncate with an ellipsis, users can guess." — Truncation without recovery
  destroys information.
- ❌ Typing `SUBMIT` in the source to get uppercase. — Use `text-transform`.
- ❌ "10px is fine for secondary labels." — If it carries meaning, it must be legible.

## 10. Source citations

- Lupton, *Thinking with Type* 3e — the four figure styles: lining numerals uniform
  in height and resembling capitals; oldstyle/nonlining resembling lowercase with
  ascenders and descenders; tabular with uniform widths "ideal for tables and
  charts"; proportional with varying widths; lining and nonlining can each be
  tabular or proportional.
- Hochuli, *Detail in Typography* — lining figures usually cap height or slightly
  less, normally set on a constant (en) body so they can serve as tabular figures.
- Santa Maria, *On Web Typography* — tabular figures keep numbers lined up in
  vertical columns, making tables and spreadsheets easier to scan.
- Rutter, *Web Typography* — OpenType figure features; numerals and data tables.
- Lupton (ed.), *Type on Screen* — typography and data display; designing data
  tables; typography in interfaces.
- Brown, *Flexible Typesetting* — calibrated type for scanning complex information:
  tabular data, navigation, infographics, code.
- WCAG 2.2 §1.4.3, §1.4.4, §1.4.12.
- MDN — [`font-variant-numeric`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric).
