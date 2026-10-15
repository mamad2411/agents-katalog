---
name: color
description: "Use when picking, converting, or repairing color values: OKLCH ramps, hue and chroma tuning, contrast ratios, P3 gamut, and semantic palette assignment."
---


# Choosing and Repairing Color

Write every new color as `oklch()`, and repair every broken one by moving exactly one channel. Lightness alone carries contrast, hue alone carries identity, chroma alone falls out of gamut — so a fix that moves two at once is a guess wearing the costume of a decision. The default palette posture is austere: one hue per ramp, one saturated accent in the entire chrome, a grey ladder instead of a second hue for secondary text, and a warm off-white canvas rather than `#fff`. This skill decides what a color *is*; `design-tokens` decides what the variable holding it is called and which tier it sits in; `dark-mode` maps a finished light set onto dark surfaces and never picks a brand hue. Contrast ratios have one owner and it is this skill — `a11y` deliberately carries none.

**Read the project's color plumbing before touching a value.** Find where colors are declared — `:root` custom properties, a Tailwind v4 `@theme` block, a CSS-in-JS theme object, a generated token pipeline — and make the change in that mechanism, at that layer. If a ramp exists, extend it rather than starting a second. A color fix is never a reason to bolt on a parallel theming layer, and a hex literal typed into a component is a bug even when the hex is right.

## Quick Reference

| Open this | When |
| --- | --- |
| [converting-colors.md](references/converting-colors.md) | Migrating hex / `rgb()` / `hsl()` literals, and you need what must *not* be converted. |
| [building-scales.md](references/building-scales.md) | Generating a ramp, equalizing hues into one family, or auditing a scale for drift. |
| [contrast.md](references/contrast.md) | A specific foreground/background pair fails, or a compliance target is named. |
| [gamut-p3-tailwind.md](references/gamut-p3-tailwind.md) | A chroma looks clipped, a color must survive both gamuts, or you are authoring a Tailwind v4 `@theme` palette. |

## Core Principles

1. **Write new color as `oklch()`; convert old color value-for-value.** The channels track perception, so palette math and contrast repair become arithmetic rather than eyeballing. Three decimals per channel is enough, and alpha goes after a slash — `oklch(0.586 0.222 17.585 / 0.9)`, never a fourth comma-separated argument. *Exception:* third-party config that parses hex (charting libraries, `manifest.json`, email templates) keeps hex; converting it breaks the consumer.

2. **Repair contrast by moving `L` and nothing else.** Chroma and hue contribute almost nothing to perceived contrast, so raising saturation to "make it pop" is the classic dead end. Push the foreground's lightness away from the background's, leaving `C` and `H` alone. *Exception:* a mid-tone background (`L` between `0.3` and `0.6`) leaves no foreground enough room — move the background instead.

3. **Clear `|Lc| 60` (APCA) or `4.5:1` (WCAG 2 AA) for body text.** APCA models perceived lightness difference and reports a signed `Lc`; judge the magnitude. Floors: body `|Lc| 60` (`75` comfortable), large or heavy text `|Lc| 45`, non-text essentials such as borders and focus rings `|Lc| 30`; WCAG 2 equivalents are `4.5:1`, `3:1`, `3:1`. *Exception:* when a contract or audit names WCAG 2.x, its ratio math is what you must satisfy whatever APCA says.

4. **Hold one hue for every step of a ramp.** A ramp whose ends resolve to different perceptual hues visibly "goes purple" at the light end — the defect that makes HSL unusable for scale generation. Measure the `H` spread across the steps; over `10°` means rebuild on the mid-tone's hue. *Exception:* neutrals may lean up to `4°` toward the brand hue so the greys agree with it — a fixed amount at every step, never a drifting one.

5. **Express chroma as a fraction of each step's own ceiling, never one shared absolute.** The sRGB ceiling swings roughly `3×` between the roomiest and tightest hues at one lightness, so "all our 500s use `C 0.19`" over-saturates violets and flattens cyans. Give sibling hues the same *percentage* of their own ceiling at a shared `L`. *Exception:* a single-hue system has no siblings to equalize — pick absolute chroma per step.

6. **Ship one saturated accent in the whole chrome.** Benji Taylor's site holds to exactly one and keeps everything else achromatic; the restraint is what makes the accent read as a decision. A second saturated hue does not add hierarchy, it removes the first one's meaning. *Exception:* status colors are meaning, not decoration — but if the brand accent is green, success must take a different hue or nobody can distinguish "primary action" from "it worked."

7. **Make the canvas a warm off-white, not `#fff`.** Benji Taylor's site paints `#fdfdfc`; the fractional warmth stops the page reading as a raw browser default and gives white cards somewhere to sit above. Reserve `#fff` for raised surfaces. *Exception:* products rendering photography or color-critical work need a strictly neutral canvas, so content is not judged against a tint.

8. **Build the text ladder from one grey, not a second hue.** Primary, secondary, and tertiary text are three lightnesses of one neutral — Benji Taylor's workhorse secondary is `rgba(0,0,0,.4)` over his off-white canvas. A blue-grey invented for "muted" is a hue the reader must decode. *Exception:* links, which may carry the accent hue, because there the hue *is* the affordance.

9. **Build tints by lowering chroma, not opacity.** An opacity tint composites with whatever sits behind it and goes grey the moment the surface changes; a chroma-reduced tint works anywhere. Derive hovers with `color-mix(in oklch, var(--accent) 85%, black)`, not a hand-picked darker hex. *Exception:* scrims and overlays, where compositing with unknown content is the point.

10. **Clamp chroma to the sRGB ceiling and layer wide-gamut punch behind `@media (color-gamut: p3)`.** An out-of-gamut value is mapped by the browser with results you did not choose. Ship the clamped value unconditionally, then re-declare the accent in `display-p3` inside the capability query — the pattern Benji Taylor's site uses. *Exception:* a decorative gradient carrying no text or control can be left to browser mapping.

11. **Bind roles to steps once, then never name a step in a component.** Canvas, raised surface, hairline, ink, muted ink, accent, accent-ink, and each status color point at one step of one ramp; components ask for the role. *Exception:* none in product code — a raw step reference is always a finding. Naming and tiering those variables belongs to `design-tokens`.

12. **Style `::selection` grey rather than leaving the OS blue.** Benji Taylor's site sets `#111` on `#ededed`. The default belongs to no palette and collides with any accent that is not itself blue. *Exception:* tint the selection with a low-chroma accent, if that accent already reads as a highlight.

## Smells and Fixes

| Smell | Fix |
| --- | --- |
| A fresh hex or `hsl()` literal in new code | Express it as `oklch()` in the token layer |
| Low contrast "fixed" by raising saturation | Vividness is not contrast — widen the `L` gap |
| Ramp ends more than `10°` apart in `H` | Rebuild on the mid-tone's `H` |
| One `C` value copied across hues | Re-derive per hue as a percentage of its own ceiling |
| Chroma past the sRGB ceiling, no fallback | Clamp `C`, add the `@media (color-gamut: p3)` layer |
| Two saturated accents in one chrome | Demote one to the grey ladder |
| `#fff` page background | Warm it; keep `#fff` for raised surfaces |
| A blue-grey invented for "muted" text | Use a lighter step of the existing neutral |
| `opacity: 0.4` standing in for disabled | A muted token — opacity passes on one background, fails elsewhere |
| `oklch(0.5, 0.1, 200, 0.5)` | Invalid; alpha after `/`, channels space-separated |
| A component naming `--berry-600` | Point it at the role token |

## Reporting Changed Colors

Report modified colors grouped by file: each declaration's previous value beside its replacement, plus a clause naming the rule it broke — drifting hue, insufficient `L` gap, out-of-gamut chroma, second accent, raw step reference. Cover every declaration you touched, so the diff can be audited without re-deriving it.

## Checklist

- [ ] Every new value `oklch()`, alpha behind a slash, three decimals max
- [ ] Every contrast repair moved `L` only, and the pair was re-measured
- [ ] Body text clears `|Lc| 60` / `4.5:1` against the surface it truly paints on
- [ ] Every ramp holds one `H`; measured spread under `10°`
- [ ] Sibling hues share a lightness and a percentage of their own ceiling
- [ ] Exactly one saturated accent; status hues distinct from it
- [ ] Canvas warm off-white; `#fff` reserved for raised surfaces
- [ ] Secondary and tertiary text are steps of one neutral
- [ ] High-chroma values clamped to sRGB with a P3 layer above
- [ ] Roles bound to steps; no component names a step
- [ ] `::selection` styled, not left as the OS blue
