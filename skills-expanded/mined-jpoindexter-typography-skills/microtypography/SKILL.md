---
name: microtypography
description: Use when text is technically correct but reads poorly — uneven word spacing, rivers, bad rags, orphans and widows, awkward hyphenation, loose or tight tracking, wrong quote marks and dashes, cramped all-caps. Also use when a design "feels cheap", "looks AI-generated", or "something is off" and the cause is spacing detail rather than font choice.
---

# Microtypography

The layer below font choice. When a page feels amateur despite a good typeface,
the defect is almost always here. Hochuli's subject: *"all the small things that
enhance the legibility of texts."*

## 1. When to invoke

- Text is set correctly by every macro rule and still reads badly.
- Uneven word spacing, visible rivers, ragged edges that clump.
- Orphans, widows, a heading stranded at a column foot.
- Wrong apostrophes, hyphens standing in for dashes, cramped capitals.
- Someone says the work looks "generic", "cheap", or "AI-generated."

**Do not** invoke to pick a typeface (`typeface-selection`) or set a scale
(`hierarchy-and-scale`).

## 2. Required context

- The **rendered** text — microtypography cannot be judged from source.
- Whether setting is **justified or ragged**, and the measure in characters.
- Whether the text is **user-generated** (you cannot hand-fix it — the rules must
  be systemic).
- Language and script — spacing conventions are not universal.
- Whether the typeface carries the needed OpenType features (real small caps,
  oldstyle figures, proper kerning pairs).

## 3. Invariant principles

- **Word spaces should be even and unobtrusive.** They separate words; they should
  not be seen as shapes in their own right.
- **Rivers are defects.** When word spaces in successive lines fall under one
  another they form vertical channels that "disturb the flow of the text"; the
  make-up should be adjusted to remove them. (Hochuli)
- **Justification below ~50 characters per line fails.** Even word spacing becomes
  "difficult, if not impossible" and large holes appear. Below that measure, set
  ragged. (Hochuli)
- **Ragged setting is a legitimate aesthetic choice at any measure**, not merely a
  fallback: even word spacing makes the text regular, while the irregular right
  margin makes it lively. (Hochuli)
- **A paragraph needs exactly one unambiguous separation signal** — indent *or*
  space, never both.
- **Punctuation has correct forms.** `'` and `"` are typewriter marks, not quotes.
  Hyphen, en dash, and em dash are three different characters with three
  different jobs.
- **Turn standard ligatures off wherever you letterspace** — a tracked `fi`
  ligature reads as broken. See `../type/references/opentype-features.md`.
- **Capitals and small caps always need letterspacing.** Set solid, they read as a
  cramped block. Lowercase set for text does not.

## 4. Context-dependent heuristics

**Paragraph separation — a real print/web conflict.** Hochuli, citing Tschichold,
holds that indents are "the only certain indicators of a new paragraph," and that
using blank lines "breaks up the page, requires too much space, and creates
problems when a paragraph ends at the bottom of a page."

That reasoning is about **bound pages**. On the web there is no page bottom, and
WCAG 1.4.12 requires paragraph spacing to survive a `2em` user override. So:

- Continuous prose in a paged/print or ebook context → **indent**, no blank line.
- Web, docs, UI, anything scrolled → **space between paragraphs**, no indent.
- Never both. Never a first-paragraph indent directly under a heading.

Source hierarchy: rule 1 and rule 2 outrank rule 6 here.

**Kerning is not tracking, and people almost always mean tracking.** Stocks:
"Everyone likes to point out bad kerning… most of the time they mean tracking."

- **Kerning** — the space between *two specific glyphs* (the `AV` pair, `To`).
  Handled by the font's kern table; you adjust it only for display-size type where
  one pair is visibly wrong. Never kern body text by hand.
- **Tracking** — the overall letter spacing across *a block* of text. This is the
  control you actually reach for. In CSS it's `letter-spacing`.

If someone reports "bad kerning" in running text, they are describing tracking, a
poorly-spaced font, or a rag problem. Diagnose before adjusting.

**Tracking.**

| Case | Guidance |
|---|---|
| Body text at reading size | Leave at the designer's default — 0 |
| Display sizes (large headings) | Tighten slightly; type spaced for text is loose when scaled up |
| All-caps and small caps | Add positive tracking, always |
| Small sizes / low contrast / dark-on-light inversion | Slightly positive |
| Any text a user can override | Must survive `letter-spacing: .12em` (WCAG 1.4.12) |

Two hard rules on tracking:

- **Never set letter spacing in absolute units.** Tracking, like line-height, must
  be relative to the type itself (`em`) so it scales with the size. `letter-spacing:
  1px` is wrong at every size except the one it was tuned for.
- **Negative tracking works only at large sizes**, and then only slightly. Below
  display size it degrades legibility, and it collides with the 1.4.12 override.

**Typographic colour.** The density of a block of text — its overall grey value,
nothing to do with hue. Stocks: it "refers to the text density on a page… consider
it a squint test." Crucially, colour is set not just by line-height and tracking but
by "all those in-between spaces, too, like counters, serifs, and the very shapes of
the letters."

This is the diagnostic behind most "something feels off" reports. Squint at the
block: if some areas go darker or lighter than others, you have uneven colour —
caused by rivers, inconsistent word spacing, a weight that's too light for the size,
or a heading whose stroke thickness doesn't match the body's apparent weight. Even
colour is what makes a page look professionally set.

**Alternative spaces.** A regular word space around an em or en dash is often too
open. Hair spaces and thin spaces exist for this, and for separating a dash from
adjacent characters without opening a hole. House style decides between a closed-up
em dash, a spaced en dash, and a hair-spaced em dash — but pick one and apply it
consistently, because mixing them is visible.

**Hyphenation and rag.** Hyphenation lets justified text hold even word spacing;
without it, narrow justified columns are unsalvageable. For ragged setting, judge
the rag itself: it should look accidental, not form shapes, stair-steps, or a
near-justified edge that reads as a mistake. Avoid more than two consecutive
hyphenated lines.

**CSS controls for hyphenation, beyond on/off.** `hyphens: auto` is a blunt switch;
CSS Text Level 4 exposes the actual dials Rutter names for controlling a hyphenated
ladder and the rag it produces (support is inconsistent — verify on MDN before
relying on any of these in production, same caveat as `text-wrap`):

| Property | Controls |
|---|---|
| `hyphenate-limit-lines: 2` | Caps consecutive hyphenated lines — enforces the "no more than two" rule in code rather than by eye |
| `hyphenate-limit-chars: 6 3 2` | Word/before/after minimums — don't hyphenate a word under 6 characters, leave ≥3 before the break and ≥2 after |
| `hyphenate-limit-zone: 2em` | The hyphenation zone — how much ragged space is tolerated before the engine hyphenates rather than leave a gap; `0` (default) is minimum rag, a larger value trades even spacing for more ragged edge |
| `hyphenate-limit-last: always` | Forbid hyphenating the last line of a paragraph or column — a targeted fix for one kind of orphan |

**Ampersands vary a lot by design** — some faces keep the historical *et* ligature
shape, others have drifted closer to a treble clef. That range is exactly why an
over-elaborate display ampersand reads as noise in running text (Rutter).

**Orphans and widows.** A single word alone on the last line of a paragraph, or a
single line stranded at the top or bottom of a column. In CSS, `orphans`/`widows`
handle column breaks; `text-wrap: pretty` addresses the last-line orphan and
`text-wrap: balance` evens short blocks like headings. Both are progressive
enhancements — unsupported browsers fall back to normal wrapping with no breakage.

**Hanging punctuation (optical margin alignment).** A quotation mark or hyphen at
the start of a line optically breaks the column's left edge. Lupton: hanging
punctuation "prevents quotation marks from taking a bite out of the crisp left edge
of a text block" — you "create a sharp edge by pushing the quotation marks into the
margin."

CSS `hanging-punctuation: first last;` does this natively but is Safari-only at time
of writing, so treat it as progressive enhancement. For a pull quote or blockquote
where the effect matters, a negative `text-indent` on the first line is the reliable
fallback. Don't hand-hang punctuation in body copy — it won't survive reflow.

**Controlling breaks without polluting content.**

| Need | Use |
|---|---|
| Keep two words together ("12 kg", "Mr Smith") | `&nbsp;` — non-breaking space |
| Offer a break point inside a long word | `&shy;` — soft/discretionary hyphen; shows only if the break is used |
| Offer a break with no hyphen (long URLs) | `<wbr>` |
| Prevent a break in a phrase | `white-space: nowrap` on a span |

Rutter distinguishes the ordinary hyphen (always displayed — `fly-by-wire`, or
disambiguating `twenty-four hour shifts`) from the soft hyphen, which appears only
when the line actually breaks there. And his blunt rule on the pairing: **"to
justify text without hyphenating is to wilfully harm the reading experience."**
Prefer automatic `hyphens: auto` with a correct `lang` attribute; reach for `&shy;`
only for words the dictionary gets wrong.

**Accents and diacritics are not optional.** Rutter: "if a word has an accent, use
it," and "pay particular attention to accented names." Dropping the accent in a
personal name is a correctness error and often a discourtesy — *Bronte* is not
*Brontë*, *Beyonce* is not *Beyoncé*. Verify the shipping font actually carries the
marks (see `typeface-selection`) and that the marks aren't clipped by a tight
line-height (see `international-typography`).

**Prefer UTF-8 characters to HTML entities.** Serve the page as UTF-8 and type the
real character — `—`, `…`, `é`, `×`. Entities (`&mdash;`, `&hellip;`) make source
unreadable, break search-and-replace, and are a legacy workaround. Automate the
substitution at the content pipeline rather than asking authors to remember.

**A few characters people reliably get wrong:**

- Use a real **multiplication sign** `×` and **division sign** `÷`, not `x` and `/`.
- Don't set **brackets and parentheses in italic** just because the enclosed text is
  italic — the upright forms belong to the sentence, not the phrase.
- Don't over-elaborate the **ampersand**. A decorative `&` is a display device; in
  running text it's noise.
- Delete **stray spaces before punctuation and at line ends** — they open holes and
  shift the rag.

**Punctuation quick table.**

| Use | Character |
|---|---|
| Word joining, line-break hyphenation | hyphen `-` |
| Ranges, "1998–2004" | en dash `–` |
| Parenthetical break | em dash `—` (or spaced en dash, house style) |
| Apostrophe, single quote | `'` `'` |
| Double quote | `"` `"` |
| Ellipsis | `…` not `...` |
| Minus sign | `−` not hyphen |

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| "Holes" in justified text | Measure too narrow, hyphenation off | Enable hyphenation, widen measure, or set ragged |
| Vertical rivers | Coincident word spaces across lines | Adjust make-up, re-break, or set ragged |
| Both indent *and* blank line between paragraphs | Two separation signals | Pick one |
| Cramped all-caps heading | No tracking added | Add positive tracking |
| Straight quotes in production copy | No smart-quote transform | Fix at the content pipeline, not by hand |
| Heading tightened globally and body went tight too | Tracking applied to a shared token | Scope tracking to display sizes |
| A single word on a heading's second line | No `text-wrap: balance` | Add it (progressive enhancement) |
| Small caps look like shrunken capitals | Faux small caps | Use a font with real `smcp` |
| "The kerning is bad" in a paragraph | Tracking, font spacing, or rag — not kerning | Diagnose before adjusting; kerning is per-pair |
| Tracking correct at one size, wrong at others | `letter-spacing` in px | Use `em` |
| Block looks patchy/mottled when squinted | Uneven typographic colour | Find the cause: rivers, word spacing, weight mismatch |
| Heading looks weaker than the body it sits above | Stroke thickness lighter than body's apparent weight | Match apparent weight, not nominal |
| Dashes sit in visible holes | Full word spaces around an em dash | Hair/thin space, or close it up — consistently |

## 6. Evaluation procedure

1. **Render at real size, then squint.** This is the typographic-colour test and it
   comes first: rivers, uneven word spacing, and weight mismatches appear as
   blotchy texture before they resolve into detail. An evenly grey block passes.
2. Scan word spacing down the block. Even? Any vertical channels?
3. If justified: count CPL. Under ~50 → change to ragged or widen.
4. If ragged: is the edge accidental, or does it form a shape or stair-step?
5. Check every paragraph boundary for exactly one separation signal.
6. Check the last line of each paragraph for orphans; check column tops/bottoms
   for widows.
7. Grep the copy for `'`, `"`, ` - `, `...` — replace with correct characters.
8. Check all-caps and small-cap runs for tracking.
9. Apply WCAG 1.4.12 overrides (`letter-spacing: .12em`, `word-spacing: .16em`)
   and confirm nothing breaks.

## 7. Output format

```
Defects found (ranked by reading impact):
1. <defect> — <where> — cause: <cause> — fix: <fix>
...
Setting: <justified|ragged> at <N> CPL — <appropriate|not>
Paragraph signal: <indent|space> — <single|doubled ✗>
Punctuation: <n> straight quotes, <n> hyphen-as-dash, <n> ... 
1.4.12 override: <pass|fail>
Unverified: <what was not checked in a rendered context>
```

## 8. Examples

**A marketing page that "looks cheap" despite a good typeface.**

> The typeface is fine. Three microtypographic defects are doing the damage: the
> hero heading is set in all-caps at default tracking, so it reads as a cramped
> block; body paragraphs carry both a first-line indent and a blank line, giving
> two separation signals; and the copy uses straight quotes throughout. Fix the
> tracking on the caps token, drop the indent, and add a smart-quote transform at
> the content layer — the font choice needs no change.

**A 38-CPL justified sidebar with visible holes.**

> Justification is failing because the measure is far below the ~50 CPL floor
> where even word spacing is achievable. Widening isn't available in this layout,
> so set the sidebar ragged. Word spaces become even; the ragged right edge is
> the correct trade and reads as deliberate.

## 9. Counterexamples

- ❌ "Add `letter-spacing: -0.02em` to body text to tighten it up." — Text-size
  type is already spaced correctly by its designer. Tightening body text harms
  legibility and may collide with the WCAG 1.4.12 override.
- ❌ "Justify the text so it looks clean and formal." — At a narrow measure,
  justification produces holes and rivers, which is the opposite of clean.
- ❌ "Use `&nbsp;` before the last word to fix the orphan." — Brittle, breaks at
  other viewports, and pollutes content. Use `text-wrap: pretty`.
- ❌ "Indent the first line of every paragraph, including the one after the
  heading." — The heading already signals the paragraph start; the indent is
  redundant there.
- ❌ "Small caps via `font-variant: small-caps` always looks right." — Without a
  real `smcp` set the browser may synthesize them by scaling capitals, which
  produces visibly too-light strokes.

## 10. Source citations

- Hochuli, *Detail in Typography* — **primary source.** Rivers and page make-up;
  the ~50 CPL floor for justified setting; ragged setting as an aesthetic choice;
  Tschichold on indents as the only certain paragraph indicator; fixation
  behavior around capitals and long words.
- Lupton, *Thinking with Type* 3e — typographic conventions, punctuation forms.
- Stocks, *Universal Principles of Typography* — §22 "a little tracking goes a long
  way"; §53 "typographic color is about density" — the squint test, and colour being
  dictated by counters, serifs, and letterform shapes as well as spacing; §56–57
  dashes and alternative spaces; §58 italicize punctuation and spaces too; §60
  widows and orphans; §61 optical trickery; §76 "kern only if you have to" — the
  kerning/tracking confusion, kerning being the space between two specific glyphs;
  and the rule that letter spacing must never use absolute units. Full index in
  `../type/references/universal-principles-index.md`.
- Rutter, *Web Typography* — hyphenation and justification on the web; the
  `hyphenate-limit-lines`/`hyphenate-limit-chars`/`hyphenate-limit-zone`/
  `hyphenate-limit-last` properties for controlling a hyphenated ladder and rag
  zone in code; ampersand forms varying by design and the case for restraint.
- WCAG 2.2 §1.4.12 (text spacing override).
- MDN — [`text-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap):
  `balance` is supported in Chrome/Edge 114+, Firefox 121+, Safari 17.5+;
  `pretty` in Chrome/Edge 117+ and Safari 26+, not yet Firefox. Chromium applies
  `balance` only to blocks of ≤6 lines. Both degrade silently.
