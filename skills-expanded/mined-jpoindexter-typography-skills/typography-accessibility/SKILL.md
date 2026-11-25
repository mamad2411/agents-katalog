---
name: typography-accessibility
description: Use whenever type carries information — always co-load this with body text, UI, and editorial typography work. Specifically for contrast, 200% zoom, user text-spacing overrides, Dynamic Type, dyslexia and low-vision needs, screen-reader compatibility, images of text, and any claim that typography is "accessible".
---

# Typography accessibility

The top of the source hierarchy. A typographic rule that fails an accessibility
criterion is wrong no matter which book it came from.

## 1. When to invoke

- Any body text, UI text, or editorial text that carries meaning.
- Contrast, zoom, spacing overrides, or text resizing questions.
- Claims that a design is accessible.
- Dyslexia, low vision, ageing eyes, or cognitive-load requirements.
- Text rendered as an image, or styled with CSS that may break assistive tech.

**Always co-load with `body-text-and-reading` and `ui-component-typography`.**

## 2. Required context

- Target **conformance level** (AA is the common legal floor; AAA where required).
- **Jurisdiction** — EAA, Section 508, ADA, EN 301 549 all reference WCAG.
- Whether the platform has a **user text-size setting** (iOS/Android Dynamic Type,
  OS-level scaling).
- Whether content is **user-generated** (rules must be systemic).
- Real **foreground/background pairs**, including over imagery and on hover/disabled.

## 3. Invariant principles — the WCAG floor

These are not heuristics. They are pass/fail.

| Criterion | Requirement |
|---|---|
| **1.4.3 Contrast (Minimum)** AA | Normal text ≥ **4.5:1**. Large text ≥ **3:1**. Large = **≥18pt (24px)**, or **≥14pt (18.66px) bold** |
| **1.4.4 Resize Text** AA | Text resizable to **200%** with no loss of content or functionality |
| **1.4.12 Text Spacing** AA | No loss of content or functionality when the user sets line-height **1.5×** font size, paragraph spacing **2×**, letter spacing **0.12em**, word spacing **0.16em** |
| **1.4.5 Images of Text** AA | Use real text unless the presentation is essential (logotypes excepted) |
| **1.4.8 Visual Presentation** AAA | Includes ≤80 characters per line, no justified text, line spacing ≥1.5 within paragraphs |
| **1.4.6 Contrast (Enhanced)** AAA | Normal ≥ 7:1, large ≥ 4.5:1 |

Note **1.4.8 forbids justified text at AAA** — which aligns with Hochuli's craft
objection for independent reasons.

Additional invariants:

- **Never suppress zoom.** `user-scalable=no` or `maximum-scale=1` fails 1.4.4.
- **Text in images is invisible to screen readers, translation, and search**, and
  degrades on zoom.
- **Contrast applies to every state** — placeholder, disabled, hover, and text over
  imagery all carry information and all must pass or be genuinely decorative.
- **Don't remove focus indicators** from interactive text.

## 4. Context-dependent heuristics

- **There is no "dyslexia font" that reliably outperforms a well-set common
  typeface.** Evidence for specialist faces is weak. What demonstrably helps:
  generous line spacing, shorter measures, left-aligned ragged setting, clear
  paragraph separation, and letting users adjust. Offer control rather than
  prescribing a face.
- **Ragged-left (left-aligned) beats justified** for readers with dyslexia and low
  vision: even word spacing, no rivers, predictable line starts.
- **All-caps runs are slower to read** and are announced awkwardly by some screen
  readers. Use `text-transform: uppercase` on normal-case source text rather than
  typing capitals, so assistive tech and translation receive the real string.
- **Light weights at small sizes fail in practice** even when they nominally pass
  contrast — thin strokes on low-DPI screens lose their measured contrast.
- **`rem`/`em` over `px`** so text responds to user preferences.
- **Respect `prefers-reduced-motion`** for any kinetic type.
- **Dynamic Type / OS scaling**: on native platforms, honour the user's setting
  rather than hardcoding sizes.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Text clips or overlaps at 200% zoom | Fixed heights, `overflow: hidden` | Intrinsic sizing |
| Layout breaks under spacing override | Absolute positioning, fixed containers | Let containers grow |
| Placeholder text unreadable | Grey-on-white below 4.5:1 | Raise contrast; don't use placeholder as label |
| Headline over a photo fails contrast | No scrim, variable background | Scrim, overlay, or move the text |
| Marketing copy set as an image | Design-tool export shipped directly | Real text (1.4.5) |
| Zoom disabled | `user-scalable=no` | Remove |
| Screen reader spells out a heading | Literal capitals in source | `text-transform` instead |
| Passes contrast checker, still unreadable | Thin weight at small size | Increase weight or size |
| "We use a dyslexia-friendly font, so it's accessible" | Font substituted for setting | Fix spacing, measure, alignment; offer user control |

## 6. Evaluation procedure

Run all of these. Passing one establishes nothing about the others.

1. **Contrast** — every text/background pair, every state, against 4.5:1 (or 3:1
   if genuinely large by the pt/px definition above). Include text over imagery.
2. **Zoom to 200%** — no loss of content or functionality.
3. **Apply the 1.4.12 override** and confirm nothing clips, overlaps, or vanishes:
   ```css
   * { line-height: 1.5 !important; letter-spacing: .12em !important;
       word-spacing: .16em !important; }
   p { margin-bottom: 2em !important; }
   ```
4. **Images of text** — inventory them; justify each or convert to real text.
5. **Screen reader** — read the page. Are headings sequential? Is any text
   announced as letters?
6. **Viewport meta** — no zoom suppression.
7. **Native platforms** — set the OS text size to its largest and re-check.
8. **Grayscale** — confirm no information is carried by colour alone.

## 7. Output format

```
Conformance target: <AA | AAA>
1.4.3 Contrast:   <pass/fail> — failing pairs: <list with ratios>
1.4.4 Resize 200%: <pass/fail> — <what broke>
1.4.12 Spacing:    <pass/fail> — <what broke>
1.4.5 Images of text: <n found> — <justified/convert>
Zoom suppressed: <yes/no>
Screen reader: <findings>
Not verified: <what was not actually executed>
```

## 8. Examples

**Pricing table failing at 200% zoom.**

> Contrast passes everywhere, but the table's rows use fixed `height` with
> `overflow: hidden`, so at 200% the price row clips its descenders and the
> footnote disappears entirely — a 1.4.4 failure (loss of content). Fix is
> `min-height` instead of `height` and removing the overflow clip. Re-tested at
> 200% and under the 1.4.12 override: no loss. Note the contrast pass told us
> nothing about this; they're independent criteria.

**"Accessible" redesign that shipped a dyslexia-specific typeface.**

> The font swap isn't the lever. Evidence for specialist dyslexia faces is weak,
> and the page still justifies its text (rivers, uneven word spacing), runs ~95
> CPL, and separates paragraphs by indent only. Recommend: left-align ragged,
> cap the measure, add paragraph spacing, raise line-height, and expose a user
> text-size control. Keep whichever face; the setting is what's failing.

## 9. Counterexamples

- ❌ "Contrast passes, so the typography is accessible." — 1.4.3 is one of at least
  four independent criteria.
- ❌ "Large text is 16px bold." — Wrong. Large is ≥18pt/24px, or ≥14pt/18.66px bold.
- ❌ "We tested with browser zoom, that covers 1.4.4." — Also apply the 1.4.12
  spacing override; they fail differently.
- ❌ "Justified text looks more professional." — Fails 1.4.8 at AAA and produces
  rivers that hurt exactly the readers who can least afford them.
- ❌ `<meta name="viewport" content="… user-scalable=no">` — never.
- ❌ "The hero text is an image so the brand font renders everywhere." — 1.4.5
  failure; invisible to AT, translation, and search; degrades on zoom.
- ❌ "It's decorative text so contrast doesn't apply." — Only genuinely decorative
  text is exempt. If it carries meaning, it isn't decorative.

## 10. Source citations

- **WCAG 2.2** §1.4.3, §1.4.4, §1.4.5, §1.4.6, §1.4.8, §1.4.12 —
  [w3.org/TR/WCAG22](https://www.w3.org/TR/WCAG22/). **Top of the source
  hierarchy; outranks every book in this pack.**
- [Section508.gov — fonts and typography](https://www.section508.gov/develop/fonts-typography/).
- Lupton, *Thinking with Type* 3e — legibility, familiarity bias, and the absence
  of evidence that serifs improve reading performance (the same evidential standard
  applies to dyslexia-specific faces).
- Hochuli, *Detail in Typography* — why justified setting at narrow measures
  produces uneven word spacing and rivers; independent craft support for 1.4.8.
- Rutter, *Web Typography* — relative units, user text-size preferences.
