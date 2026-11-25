---
name: typeface-selection
description: Use when choosing or replacing a typeface — "which font should we use", evaluating candidates, building a type palette, or replacing a face that isn't working. Also use when a font must carry a brand tone, survive small sizes, support extra scripts, or fit a licensing and performance budget.
---

# Typeface selection

Selection is a constraint-satisfaction problem, not a taste contest. Taste
decides between the candidates that survive the constraints.

## 1. When to invoke

- Choosing a typeface for a product, brand, or document.
- Replacing a face that fails at some size, script, or medium.
- Building a type palette for a system.
- Auditing an inherited choice.

**Do not** invoke for combining faces (`typeface-pairing`) or for expressive
critique (`typography-critique`).

## 2. Required context

Do not name a font before you have these:

- **Roles required** — body, UI, display, data, code. Different constraints each.
- **Smallest and largest** sizes it must work at.
- **Scripts and languages** required, now and planned.
- **Weights and styles** genuinely needed (including true italics).
- **Figure requirements** — tabular for data, oldstyle for prose. Confirm the file
  actually ships them (`../type/references/opentype-features.md`).
- **Licence and budget** — web, app, desktop, redistribution.
- **Performance budget** — see `font-loading-and-performance`.
- **Brand tone**, and any existing system constraint.
- **Medium** — screen, print, low-DPI, e-ink, embedded.

## 3. Invariant principles

- **Constraints first, taste last.** Script coverage, licensing, weights, and
  figures eliminate most candidates before aesthetics is consulted.
- **Judge at the size of use**, in the medium of use, with real content.
- **Serif vs. sans is not a legibility decision.** Research has failed to prove
  serifs improve reading speed or comprehension; "bias favors familiarity."
  (Lupton) Choose on tone and rendering behavior.
- **A typeface must be judged in running text**, not from its logotype-friendly
  showcase glyphs. Santa Maria: flourishes that look charming in a specimen "stick
  out in running text."
- **The face must survive its worst case**, not flatter its best — the longest
  German compound, the smallest label, the lowest-DPI screen.
- **Familiar is not a failure.** Familiarity aids reading.

## 4. Context-dependent heuristics

**By role.**

| Role | Prioritise |
|---|---|
| Body / long-form | Low-moderate contrast, open apertures, real italic, comfortable at 15–18px, wide language coverage |
| UI / dense product | Open apertures, distinguishable `1 l I` / `0 O`, tabular figures, tight vertical metrics, several weights |
| Display / brand | Character, distinctive forms, optical sizes if available; small-size behavior irrelevant |
| Data / tables | **Tabular figures mandatory**; unambiguous digits |
| Code | Monospace, disambiguated `0 O l 1 I`, clear punctuation |

**Reading tone from form.** Coles' value is explaining *why* a face reads a
certain way, from evidence:

| Wanted tone | Visible signals to look for |
|---|---|
| Unobtrusive, systematic | Neo-Grotesque; regular proportions, low contrast, closed-ish apertures |
| Technical, precise | Geometric or Grotesque sans; uniform stroke, circular rounds |
| Humanist, warm | Angled axis, calligraphic trace, open apertures |
| Editorial, authoritative | Transitional/Rational serif; vertical axis, higher contrast |
| Contemporary, sturdy | Large x-height, low contrast, chunky serifs, very open apertures |
| Expressive, characterful | Distinctive terminals, unusual proportion |

Say the evidence out loud. "Feels modern" isn't a reason; "geometric construction,
near-uniform stroke weight, circular bowls" is.

**Do not say "neutral."** Rutter: "There's no such thing as a neutral typeface…
You cannot wear neutral clothes. Boring, predictable, unadventurous and inoffensive,
perhaps; but never neutral." Every choice carries a voice, and calling one neutral
hides the decision. When a stakeholder asks for "something neutral," translate it:
they want a face that *gets out of the way and lets the ideas shine through* — which
Rutter notes is a demanding brief, since "any successful boring typeface will have
been carefully designed to be highly readable." Say "unobtrusive" and mean it.

**Classification analyses; genre finds.** There is no universal classification
system, and no vendor lists faces under the descriptive terms designers use — you
won't find "linear dynamic sans serif" as a browsable category. Use classification
(`typeface-anatomy`) to describe and defend a face from evidence; use genre,
description, and specimen browsing to *discover* candidates.

**Make a specimen to reduce the shortlist.** Set the same real content in every
candidate, at the real sizes, and compare them side by side in one document. This is
the step people skip, and it is the one that actually eliminates candidates.

**Building a palette** (Santa Maria). Keep a small personal set you know deeply
rather than searching fresh each time. Knowing how a face behaves at 12px, in
italic, in long German words, and under a fallback swap is worth more than novelty.

**Superfamilies** — a serif and sans sharing skeleton and metrics — solve pairing
and metric-matching at once. Strong default when a project needs both.

**Variable fonts** collapse many weights into one file. See `variable-fonts`.

**How the face renders on screen is part of the choice.** Rasterisation is lossy and
varies by engine, only Windows uses hinting, and handhelds use greyscale smoothing
rather than subpixel anti-aliasing — so **check your type across platforms** rather
than judging on your own machine. Delicate high-contrast faces and hairline weights
are the first casualties on low-DPI displays. Full detail in `typeface-anatomy`
("How letterforms become pixels").

⚠️ One piece of the 2017 advice is stale. Rutter recommends disabling subpixel
anti-aliasing (`-webkit-font-smoothing: antialiased`) *only* for reversed-out text,
because light-on-dark rendered "an entire weight bolder" on low-resolution macOS.
macOS removed subpixel anti-aliasing system-wide in Mojave (2018), so the specific
condition no longer holds; the property is now used for consistency with the OS, not
as a reversed-text fix. Verify current behavior before applying either. The
underlying design point survives: **reversed text reads heavier, so test it.**

**System font stacks** cost zero bytes and render natively. Legitimate for
performance-critical and utility interfaces; they forfeit brand distinctiveness and
render differently per platform.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Beautiful in the specimen, muddy at 14px | Judged at display size | Re-evaluate at the real size |
| Lovely until German/Polish shipped | Coverage unchecked | Verify glyph coverage per language |
| Numbers jitter in the table | Proportional figures | Require tabular figures |
| Faux italic renders | No true italic in family | Check styles, not just weights |
| Licence blocks app embedding | Web-only licence | Confirm every medium up front |
| Face "feels off" in body, fine in headings | Display face used for text | Separate display and text roles |
| Distinctive flourishes distract in paragraphs | Judged on isolated glyphs | Judge in running text |
| Chosen for readability because it's a serif | Folklore | Choose on tone and rendering |
| Nine weights shipped for a 4-weight design | No inventory | Ship only what renders |

## 6. Evaluation procedure

1. Write the constraint list (§2). Eliminate anything failing a hard constraint —
   script coverage, licence, required styles, tabular figures.
2. For survivors, render **real content** — the actual longest string, the actual
   smallest label — at the real sizes in the real medium.
3. Apply the `typeface-anatomy` evaluation procedure to each: x-height, contrast, aperture, counters,
   `1 l I`, `0 O`.
4. Set a full paragraph in each and read it. Do any glyphs distract?
5. Test the worst case: longest locale word, densest table, smallest size, lowest
   DPI, reversed on dark.
6. Check the fallback: how far are its metrics from your candidate?
   (`font-loading-and-performance`)
7. Check the payload for the weights you'll actually ship.
8. Only now compare on tone — and state the visible evidence for the tone claim.

## 7. Output format

```
Roles: <body|ui|display|data|code>
Hard constraints: scripts <…> · styles <…> · figures <…> · licence <…> · budget <…>
Candidates eliminated: <face> — <which constraint>
Recommended: <face>
  Evidence: x-height <…>, contrast <…>, aperture <…>, digits <…>
  Tone claim: <tone> — because <visible signals>
  Worst case tested: <what>
  Payload: <n> files, <n> KB
Runner-up: <face> — <why not>
Unverified: <what wasn't rendered>
```

## 8. Examples

**Fintech dashboard, dense tables, EN + DE + PL, 4 weights, dark mode.**

> Hard constraints eliminate most candidates immediately: Polish requires
> `ą ć ę ł ń ó ś ź ż`, tables require tabular figures, and dark mode means the
> lightest weight must survive reversal. That leaves a Neo-Humanist or Grotesque
> sans with a full Latin Extended set. Recommending Inter: open apertures keep
> `c/e/s` distinct at 13px, `1 l I` and `0 O` are disambiguated, tabular figures
> ship, and one variable file covers all four weights. Verified with the longest
> German compound in the narrowest column and with the 300 weight reversed on the
> dark surface — 300 washed out, so the minimum shipping weight is 400.

## 9. Counterexamples

- ❌ "Use a serif for body text, it's more readable." — Unevidenced (Lupton).
- ❌ "This font is trending, let's use it." — Trend is rule 9, the bottom of the
  hierarchy.
- ❌ "It looked great in the specimen." — Specimens are set to flatter.
- ❌ "We'll add language support later." — Retrofitting script coverage usually
  means changing the face.
- ❌ "Ship all nine weights so we have options." — Every unused weight is pure cost.
- ❌ "Helvetica is neutral, so it's the safe choice." — Neo-Grotesque closed
  apertures actively hurt small-size UI legibility.
- ❌ "The brand deck says 'modern and human', so use a geometric sans." — Geometric
  construction reads *technical*; humanist forms read *human*. Match evidence to
  the claim.

## 10. Source citations

- Coles, *The Anatomy of Type* — selecting type on visible evidence; explaining why
  a face reads technical, humanist, editorial, neutral, or expressive; comparing
  similar typefaces; ~100 analysed faces with designer, foundry, and classification.
- Santa Maria, *On Web Typography* — evaluating typefaces; building a personal type
  palette; matching type to content and tone; flourishes that read fine in isolation
  and "stick out in running text"; balancing aesthetic and technical constraints.
- Lupton, *Thinking with Type* 3e — serif readability research is inconclusive;
  familiarity bias; typeface classification.
- Rutter, *Web Typography* — choosing typefaces for screens; apparent size and
  x-height compensation; OpenType and figure styles; **"there's no such thing as a
  neutral typeface"**; "type genres are more useful than classifications"; make a
  specimen to reduce your shortlist; judge typefaces in context; choose robust faces
  for readability on screens; understand how fonts render on screens and check type
  across platforms; clearly distinguish functional text from body text.
- Latin, *Better Web Typography* — choosing typefaces; language-range considerations.
- Stocks, *Universal Principles of Typography* — classification's uses and limits;
  width as a palette tool; "type should be legible" as a first principle.
