---
name: body-text-and-reading
description: Use when setting or fixing running text meant to be read continuously — article bodies, documentation, long-form pages, onboarding copy, email. Also use when readers report eye strain, losing their place, re-reading lines, or text that "feels dense", and when choosing body size, line-height, or measure.
---

# Body text and reading

Running text is the only place where typography is measured against a physical
process: the eye's saccadic movement. Every rule here derives from that, not from
taste.

## 1. When to invoke

- Setting body copy for anything read in succession (>1 paragraph).
- A reader reports strain, re-reading lines, or losing their place.
- Choosing or changing body size, line-height, or column width.
- Auditing an existing article/doc template.

**Do not** invoke for isolated UI strings, labels, or numeric displays — that is
`ui-component-typography`. Do not invoke for headings alone — that is
`hierarchy-and-scale`.

## 2. Required context

Refuse to give a number until you have, or have explicitly assumed:

- The **typeface** and its x-height (apparent size varies enormously at equal
  nominal size).
- **Target device and reading distance** (phone ~35cm, laptop ~50–70cm, TV ~3m,
  kiosk standing).
- **Content type** — reference/scanned vs. immersive/continuous.
- **Audience** — age, vision, whether Dynamic Type / user zoom is expected.
- **Available column width**, and whether it is fixed or fluid.

If you have none of these, say what you're assuming before you answer.

## 3. Invariant principles

- **Information is absorbed only during fixations, not during motion.** The eye
  moves in saccades of roughly 5–10 letters (~1–2 English words) alternating with
  fixations of 0.2–0.4 seconds. Only 3–4 letters are focused sharply; the rest are
  perceived indistinctly and from context. Unclear text causes *regression
  saccades* — the eye jumps back. (Hochuli)
- **Size, line-height, and measure are one interdependent system.** Change one and
  you must revisit the other two. Latin calls it a triangle that must stay
  equilateral.
- **The line-return must be unambiguous.** If a reader's eye cannot reliably find
  the start of the next line, the setting has failed, whatever its metrics.
- **Serif vs. sans is not a readability decision.** Research has failed to prove
  serifs improve reading speed or comprehension; "bias favors familiarity."
  (Lupton) Choose on tone and rendering.
- **Text must survive user override.** WCAG 1.4.12 requires no loss of content or
  functionality at `line-height: 1.5`, paragraph spacing `2em`, word spacing
  `0.16em`, letter spacing `0.12em`. WCAG 1.4.4 requires 200% resize.

## 4. Context-dependent heuristics

**Measure.** Use **45–75 characters as a diagnostic range, not a target.**

| Situation | Guidance |
|---|---|
| Desktop, single column, continuous reading | 60–75 is comfortable; check visually |
| Phone at default size | ~40 CPL is normal and acceptable — the device floor wins |
| Below ~35 CPL | Real defect: too many line-returns, ragged texture |
| Above ~85 CPL | Real defect regardless of viewport |
| Inside the range | Judge with your eyes; do not tune to hit a count |

The canon genuinely disagrees here (Lupton 55–70, Rutter 45–75, Material 40–60,
Brown rejecting counting altogether). See `../type/references/corpus-conflicts.md`.
Field trick (Walton, via Stocks): put an asterisk before the 45th character and
after the 75th, then see where lines actually break.

**Size.** Start from the browser default (commonly 16px) as a *starting point, not
an optimum*. Then adjust for apparent size: a face with a tall x-height at 16px
reads larger than one with a short x-height at the same value. Match apparent
size, not nominal size, when swapping typefaces.

**Line-height.** 1.3–1.7 unitless for body text is the working range (Latin);
Santa Maria's range is close but wider, 1.2–1.8, and she's explicit that "a true
ideal line-height doesn't exist" — the typeface's design (wide/decorative faces
want more air) and the specific setting (a narrow hanging caption can run tighter
than the article beside it) both move the number, so treat any range as a
starting point to trial against the real typeface, not a value to look up. Push
higher as measure lengthens — a long line needs more vertical separation for
the return sweep to land correctly. Push lower as measure shortens. Tighter than
1.3 for a full paragraph is almost always wrong. Always use a **unitless** value so
it inherits proportionally.

**Don't ship the default leading.** Elam's observation about how designers actually
work: "initially, many designers are satisfied with the computer default values for
leading, about 20% of the text size" — i.e. roughly 1.2 — and the discipline is to
"become sensitive to the texture of the text on the page," then investigate leading
deliberately and "experiment with dense and airy text." A 1.2 line-height in a
paragraph is usually a default nobody chose. See `microtypography` on typographic
colour for reading that texture.

**Reading distance** scales everything. Kiosk and TV need far larger sizes than
their "equivalent" desktop values. To evaluate this honestly rather than guess,
Brown's technique: zoom the rendered composition to simulate the actual viewing
distance (or better, view it on a real device at its real distance — phone in
hand, TV across a room) and re-judge size and measure at that simulated
closeness, not at your editor's default zoom level.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Reader loses their place mid-paragraph | Measure too long for the line-height | Shorten measure or increase line-height |
| Text feels dense and airless | Line-height too tight, or x-height tall with tight spacing | Raise line-height; check letter spacing |
| Lines drift apart, paragraph stops cohering | Line-height too large for the measure | Reduce line-height or lengthen measure |
| Fine on desktop, cramped on phone | Fixed px sizing, no fluid strategy | Route to `responsive-typography` |
| Breaks when the user zooms or applies a spacing override | Fixed heights, `overflow: hidden`, absolute positioning | Route to `typography-accessibility` |
| Swapping the font changed the whole page rhythm | Matched nominal size instead of apparent size | Re-tune size to x-height, then re-check measure |

## 6. Evaluation procedure

Run in order. Stop and fix before continuing.

1. **Render it.** Never evaluate body text from CSS alone.
2. Count characters on 3 representative full lines. Compare against the
   diagnostic range for that viewport.
3. Read one full paragraph at real size and distance. Did your eye return
   cleanly on every line?
4. Set `line-height: 1.5`, `word-spacing: .16em`, `letter-spacing: .12em`,
   paragraph spacing `2em`. Confirm nothing clips, overlaps, or disappears
   (WCAG 1.4.12).
5. Zoom to 200%. Confirm no loss of content or function (WCAG 1.4.4).
6. Check the narrowest and widest supported viewport.
7. Check contrast ≥ 4.5:1 for normal text (WCAG 1.4.3).

## 7. Output format

```
Setting: <typeface> <size> / <line-height> at <measure>
Inputs:  x-height <tall|moderate|short>, device <…>, distance <…>, content <…>
Measure: <N> CPL at <viewport> — <inside|below|above> diagnostic range
Checks:  1.4.12 <pass/fail> · 1.4.4 <pass/fail> · 1.4.3 <ratio>
Conflicts resolved: <which rule won, if any>
Unverified: <anything not checked in a rendered context>
```

## 8. Examples

**Documentation site, desktop-first, Source Sans (moderate x-height).**

> Starting at the 16px browser default. Source Sans has a moderate x-height, so
> apparent size is close to nominal — no compensation needed. At a 68ch column the
> measure lands ~70 CPL, inside range. Line-height 1.6 unitless, toward the upper
> end because the measure is long. Verified at 200% zoom and under a 1.5
> line-height override: no clipping.

**Swapping Georgia → Merriweather in an existing article template.**

> Merriweather has a notably larger x-height, so at the same 18px it reads
> distinctly larger and the existing 66ch measure now runs ~74 CPL. Two options:
> drop to 17px to match apparent size and preserve the measure, or keep 18px and
> narrow the column. Recommending the size drop — it preserves the tuned measure
> and the page rhythm.

## 9. Counterexamples

- ❌ "Body text should be 16px with 1.5 line-height." — A universal constant with
  no inputs. Wrong for a kiosk, a phone, a TV, or any face with an unusual
  x-height.
- ❌ "Use a serif for body text because serifs are more readable." — Unevidenced.
  Lupton is explicit that research has failed to demonstrate this.
- ❌ "Measure is 45–75 characters, so I set it to exactly 60ch." — `ch` is the
  width of the `0` glyph and varies per font; and tuning to hit a count produces
  the stiff layouts Brown warns about.
- ❌ "It passes contrast, so the body text is accessible." — 1.4.3 is one of three
  relevant criteria; 1.4.4 and 1.4.12 are independent.
- ❌ Setting `line-height: 24px`. Fixed units break inheritance and user scaling.

## 10. Source citations

- Hochuli, *Detail in Typography* — the reading process; saccades, fixation
  duration, regression saccades. **Primary source for why any of this matters.**
- Lupton, *Thinking with Type* 3e — measure 55–70; serif readability research is
  inconclusive; familiarity bias.
- Rutter, *Web Typography* — 45–75 range; 42 CPL satisfactory; ~40 CPL on a
  phone at default size; apparent size and x-height compensation.
- Brown, *Flexible Typesetting* — measure as a visual decision; Frere-Jones,
  "we read with our eyes, not with rulers"; zooming a composition to simulate
  real viewing distance/closeness as an evaluation technique, rather than judging
  size at an editor's default zoom.
- Latin, *Better Web Typography* — 1.3–1.7 line-height; the size/line-height/
  measure triangle.
- Santa Maria, *On Web Typography* — 1.2–1.8 line-height as a starting range;
  there's no universal ideal, it's set per typeface and per setting (a narrow
  hanging caption legitimately tighter than the body beside it).
- Lupton (ed.), *Type on Screen* — 45–75 measure on screen.
- Elam, *Typographic Systems of Design* — default leading of about 20% of text size
  as a starting point designers too readily accept; developing sensitivity to the
  texture of the text; experimenting with dense and airy settings.
- Stocks, *Universal Principles of Typography* — Bringhurst's 66; Material's
  40–60; Walton's asterisk trick.
- WCAG 2.2 §1.4.3, §1.4.4, §1.4.12.
