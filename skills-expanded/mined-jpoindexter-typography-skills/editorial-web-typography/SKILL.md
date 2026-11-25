---
name: editorial-web-typography
description: Use when designing article, long-form, marketing, or art-directed pages — pull quotes, drop caps, captions, bylines, subheads, figures, footnotes, hero compositions. Also use when an article template feels flat and undifferentiated, or when a page needs expressive typographic voice without sacrificing readability.
---

# Editorial web typography

Where typography stops receding. Editorial pages carry voice, and voice is carried
by the parts around the body text as much as by the body text itself.

## 1. When to invoke

- Article, essay, documentation, or long-form templates.
- Marketing and landing pages with substantial copy.
- Pull quotes, drop caps, captions, bylines, footnotes, figure treatment.
- Art-directed or per-story layouts.
- An article template that "feels flat".

**Do not** invoke for dense product UI (`ui-component-typography`) or for the body
setting itself (`body-text-and-reading`).

## 2. Required context

- The **real content inventory** — does every story have a pull quote, a hero
  image, a subtitle? Templates fail on the story that lacks them.
- **Story length range**, shortest to longest.
- Whether layouts are **templated** or **art-directed per story**.
- Whether content is authored in **Markdown/CMS** (constrains what's expressible).
- Brand voice, and how far type may carry it.

## 3. Invariant principles

- **The body text is the product.** Every editorial device exists to serve reading,
  not to decorate around it. If a device interrupts reading without repaying it,
  remove it.
- **Secondary elements need a distinct, consistent voice.** Captions, bylines, and
  footnotes should be recognisable as a class at a glance, and consistent across
  every story.
- **A device must degrade.** A drop cap must work when the paragraph is two lines;
  a pull quote must work when there's no quote; a hero must work with no image.
- **Vertical rhythm is felt, not measured.** Consistent spacing between elements
  reads as competence; the reader never counts it.
- **Space above binds, space below separates.** A subhead belongs to the section
  that follows it, so its space above must exceed its space below.
- **Expressiveness is bounded by readability**, and readability is bounded by
  accessibility (rule 1).

## 4. Context-dependent heuristics

**Measure.** Editorial is where the measure guidance in `body-text-and-reading`
matters most — this is genuine continuous reading. Cap the column; let margins
absorb extra viewport width. Full-bleed images may break the column; text should
not.

**Vertical rhythm, concretely.** "Space above binds, space below separates" is the
principle; this is the arithmetic that makes it real (Rutter). Set the page's
rhythm unit from the body text's line-height in pixels — 16px text at 1.3125
line-height gives a 21px unit. Every other vertical measurement on the page —
paragraph spacing, heading margins, caption line-height — should be a multiple or
clean fraction of that unit:

- **Paragraph spacing** = the line-height itself (or half, if tighter spacing is
  wanted), not the browser's default `1em` margin, which is a different, unrelated
  number and will visibly throw off the beat.
- **Headings and asides at a different size** must recompute their own
  `line-height` to still land on a multiple of the unit — an 18px subhead over a
  21px rhythm needs `line-height: 21÷18 = 1.167`, and its margins should equal that
  same value (or an asymmetric split, e.g. 1.5× above / 0.5× below, that still sums
  to a whole multiple). Don't reach for `line-height` alone to add air around a
  heading — if it wraps to two lines, oversized `line-height` reads as two stacked
  headings instead of one.
- **Non-text elements (images, embeds, forms) may break the rhythm.** Don't crop
  content images just to preserve the beat — restart the rhythm when running text
  resumes after the interruption; the tail shouldn't wag the dog.
- **Don't force a print baseline grid onto the web.** Browsers lay out block-by-
  block from the top, not text-outward from a baseline, so chasing true
  baseline-to-baseline alignment (the print definition of vertical rhythm) fights
  the platform. A consistent multiple-of-the-unit rhythm gets the same reader
  benefit without it.

**Subheads.** Give them clear separation from the preceding paragraph and tight
proximity to the following one. Two levels is usually enough. Keep the semantic
heading level correct independently of size. Style them as visibly *part of* the
same hierarchical system as the headline (a scaled-down echo of its treatment, not
an unrelated style) while staying clearly smaller — that visual tie-in is what
tells a scanning reader "this belongs to that headline, and is one level down"
(Santa Maria).

**Pull quotes.** They exist to pull a scanner into the text. Rules:
- Use text that already appears in the article; don't introduce new content.
- Never let it disrupt the measure of the body text around it awkwardly — either
  break the column fully or sit clearly outside it.
- It must be skippable. A reader reading straight through should not stumble.
- If the CMS can't guarantee one exists, the template must look complete without it.

**Drop caps.** Genuinely hard on the web. Requirements:
- Align the cap's top to the first line's cap height and its baseline to a body
  baseline — `initial-letter` does this properly where supported; float hacks
  approximate it badly.
- Never apply to a paragraph shorter than the cap is tall.
- Skip when the paragraph starts with a quotation mark or a number.
- Ensure the first word is still readable as a word by screen readers — a drop cap
  built by splitting the letter into its own element can be announced separately.

**Paragraph demarcation, with numbers.** Rutter's concrete limits: indent by **at
least 1em** if you indent, and separate by **no more than 1em** if you space. Below
1em an indent doesn't read as intentional; above 1em the paragraphs stop cohering
into a text block. And don't use stylised paragraph breaks (dinkuses, ornaments)
without a reason — they interrupt.

**A standfirst should stand first.** The intro paragraph that summarises the piece
needs to be visibly distinct from body copy — larger, or a different weight — and it
needs to come before the body, not float beside it. If it looks like the first
paragraph, it isn't doing its job.

**Block quotes are not pull quotes.** A block quote is *quoted source material* the
reader should read in sequence. A pull quote is *repeated text* used to bait a
scanner. They need different treatments, and styling every block quote as a giant
centred pull quote is a common and confusing default.

**Links, lists, and emphasis.**

- **Make links clear but unobtrusive.** They must be identifiable without scanning
  the page for colour, and identifiable by something other than colour alone.
- **Don't underline for emphasis.** On the web an underline means "link." Use
  italics for emphasis, weight for strong emphasis.
- **Avoid faux bold and italic** — if the family lacks the style, don't synthesize it.
- **Treat lists as text to be read**, not as data dumps: they need the same measure
  discipline, leading, and spacing care as paragraphs.

**Semantics come first, styling second.** Rutter: "establish the semantics up front."
Decide what a piece of text *is* — `<em>`, `<strong>`, `<cite>`, `<q>`, `<abbr>`,
`<figure>`/`<figcaption>`, `<blockquote>` — before deciding how it looks. Semantic
markup drives assistive technology, translation, search, and reader modes; visual
styling that floats free of it is decoration that only sighted users receive. A
`<span class="bold">` communicates nothing to a screen reader.

**Captions.** Small, clearly subordinate, consistently placed, and **still meeting
contrast**. Grey captions are the most common contrast failure on editorial sites.
Print captions can run 6–8pt; that size is illegible on screen — Santa Maria's
floor is **around 12px** on the web, higher on lower-DPI displays, as a starting
point rather than a rule to hit exactly. In a narrow hanging caption (a margin
note beside the article column), set the line-height tighter than the body text's
— the narrow measure both permits and needs it, and it helps the caption read as
its own block rather than a continuation of the adjacent body copy.

**Figures and footnotes.** Use `<figure>`/`<figcaption>` for semantics. Footnotes
need a return path; a link that leaves the reader stranded is a defect.

**Art direction vs. template.** Per-story art direction produces the best pages and
does not scale. Be explicit about which you're building. A common resolution: a
strong template plus a small set of sanctioned variations (full-bleed, wide,
column) that authors select.

**Layering.** Type on Screen's term for building a composition in depth rather than
in sequence — type over imagery, type behind or in front of a scrim, and *additive
layering*, where separate styles within a family act as distinct structural or
decorative elements (Carter's Walker uses five "snap-on" serif styles this way).
Two rules: every layer that carries text must independently meet contrast, and the
stacking must survive the layer beneath changing — a CMS-driven hero image will not
always be the dark, calm photo the design was made against. Use a scrim or a
contrast-guaranteed band rather than hoping.

**Navigation and wayfinding type.** Nav labels are the shortest, most-scanned text
in the product and the first to break in translation. Keep them one line, keep
their voice distinct from body text (usually size and weight, not a second face),
and mark the current location with something other than colour alone. In long-form
editorial, wayfinding also means in-page structure: subheads a reader can scan, and
a visible sense of where they are in a long piece.

**Wrap control.** `text-wrap: balance` on headings and pull quotes prevents the
one-word last line; `text-wrap: pretty` on body paragraphs handles orphans. Both
degrade silently. See `microtypography`.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Every article looks the same and flat | Only body + h2 styled | Give captions, bylines, quotes a real voice |
| Drop cap overlaps the second line | Float hack without baseline alignment | `initial-letter`, or drop the device |
| Pull quote breaks reading flow | Placed inside the measure, mid-sentence | Move outside the column or to a paragraph break |
| Template collapses without a hero image | Device assumed present | Design the absent case |
| Captions unreadable | Grey-on-white below 4.5:1 | Raise contrast |
| Subhead looks attached to the paragraph above | Symmetric margins | More space above than below |
| Spacing inconsistent between stories | Ad-hoc margins, no rhythm | Systematise spacing |
| Long article has no wayfinding | No subheads or progress cue | Add structural subheads |
| Heading breaks to a one-word line | No wrap control | `text-wrap: balance` |
| Paragraph spacing feels arbitrary next to heading spacing | Browser default `1em` margin, unrelated to the line-height unit | Set spacing as a multiple of the rhythm unit |
| Wrapped subhead reads as two stacked headings | Oversized `line-height` used for air instead of margin | Recompute `line-height` to the rhythm unit; add air via margin |
| Caption legible in the design file, not on screen | Sized to a print convention (6–8pt) | ~12px floor on screen, verified at real DPI |

## 6. Evaluation procedure

1. Render the **shortest** and **longest** real story in the template.
2. Render a story **missing** each optional device — no hero, no pull quote, no
   subtitle, no author image.
3. Read one full story at real size. Did any device interrupt without repaying?
4. Check subhead spacing: above > below, on every level.
5. Check the measure through the whole article, including around floated elements.
6. Contrast-check captions, bylines, footnotes, and any grey text.
7. Verify semantic structure: sequential headings, `<figure>`/`<figcaption>`,
   footnote return links.
8. Apply the WCAG 1.4.12 override and zoom to 200%.
9. Check heading and pull-quote wrapping at the narrowest breakpoint.

## 7. Output format

```
Template: <name> — <templated | art-directed | template + variants>
Body setting: <deferred to body-text-and-reading>
Voice elements: caption <spec> · byline <spec> · pull quote <spec> · footnote <spec>
Devices used: <drop cap | pull quote | full-bleed | …>
  Degradation: <device> without <precondition> → <behaviour>
Rhythm: space-above/below per element — subhead binding correct: <yes/no>
Contrast: captions <n> · bylines <n> · footnotes <n>
Tested: shortest <pass/fail> · longest <pass/fail> · missing-devices <pass/fail>
```

## 8. Examples

**Blog template that "feels flat" despite good body type.**

> The body setting is fine — the flatness is that nothing except `h2` has a voice.
> Captions, byline, and reading time are all body-size grey text, so the page reads
> as one undifferentiated block. Give the secondary class a real identity: smaller,
> one weight up, a slight tracking increase, and a consistent placement — but raise
> the grey to pass 4.5:1, which it currently fails. Add one structural device (a
> pull quote at a paragraph break, not mid-sentence) and design the no-quote case
> so short posts don't look broken.

**Drop cap request on a docs site.**

> Recommending against it. Docs paragraphs are frequently two lines, often start
> with a code term or a number, and are re-ordered by authors — three conditions
> where a drop cap fails. If the goal is signalling article start, a larger,
> tracked lead-in phrase gives the same signal, degrades to nothing, and doesn't
> risk the screen-reader split that letter-in-its-own-element drop caps cause.

## 9. Counterexamples

- ❌ "Add a drop cap, it looks editorial." — Fails on short paragraphs, on
  quote/number openings, and often for screen readers.
- ❌ Pull-quote text that appears nowhere in the article. — It's a pull quote, not
  a subtitle.
- ❌ "The template looks great." — with the one story that has every optional
  element populated.
- ❌ Grey captions at #999 on white. — 2.8:1; fails 1.4.3.
- ❌ Symmetric margins on subheads. — Visually attaches them to the wrong section.
- ❌ Letting the column widen with the viewport indefinitely on an article page.
- ❌ "Art-direct every story." — Unless there's a designer per story, this is a
  promise the system can't keep.

## 10. Source citations

- Lupton (ed.), *Type on Screen* — typography in interfaces, screen hierarchy,
  layering, type and imagery, dynamic vs. fixed compositions.
- Lupton, *Thinking with Type* 3e — paragraph composition, hierarchy and contrast,
  typographic conventions, and when breaking a rule is appropriate.
- Latin, *Better Web Typography* — page composition, vertical rhythm, heading
  relationships, drop caps.
- Santa Maria, *On Web Typography* — matching type to content and tone;
  understanding reading behavior; art direction; captions illegible on screen at
  print sizes (6–8pt), ~12px as the web floor; subheads and bylines tying into the
  headline's system at a smaller size to signal "part of, but subordinate to."
- Rutter, *Web Typography* — "establish the semantics up front"; mark the opening of
  each passage; a standfirst should stand first; demarcate paragraphs appropriately
  (indent at least 1em, separate by no more than 1em); don't use stylised paragraph
  breaks without good reason; not all block quotes need to look like pull-quotes;
  treat lists as text to be read; make links clear but unobtrusive; avoid underlines
  for emphasis; avoid faux bolds and italics; implement drop caps accurately or not
  at all; **applying vertical rhythm** — setting a base rhythm unit from the body
  line-height in pixels, spacing paragraphs by that unit rather than the browser
  default, recomputing `line-height` for off-size elements (headings, asides) to
  still land on a multiple of the unit, letting embedded media break the rhythm
  deliberately, and not forcing a print baseline grid onto a browser's top-down
  block layout.
- Hochuli, *Detail in Typography* — paragraph texture, indentation, and the reading
  process that editorial devices must not disrupt.
- Elam, *Typographic Systems of Design* — structural systems for composition; see
  `typography-layout-systems`.
- WCAG 2.2 §1.4.3, §1.4.4, §1.4.12.
- MDN — [`initial-letter`](https://developer.mozilla.org/en-US/docs/Web/CSS/initial-letter),
  [`text-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap).
