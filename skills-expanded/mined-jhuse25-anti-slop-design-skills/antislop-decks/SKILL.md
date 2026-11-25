---
name: antislop-decks
description: "Use when designing or reviewing any presentation (pptx, Google Slides, HTML/reveal) so it does NOT look AI-generated. A bias-correction engine for decks: kills bullet soup with an assertion-evidence structure, sets DENSITY/MOTION/VARIANCE dials, bans the tells of a generated deck, requires one signature element, and generates a DECK.md per project. Pairs with antislop-web for shared visual discipline."
license: MIT
tags: [design, presentations, decks, pptx, google-slides, anti-slop]
---

# Anti-Slop Decks — so no presentation looks AI-generated

Single goal: **remove the "AI tells" of a generated deck**. An AI-made presentation gives
itself away: every slide is a title + four bullets, a cover with a blue gradient and a giant
centered title, the same layout twenty times, emoji bullets, charts in Excel's rainbow
palette, an empty "Thank you / Questions?" slide. It works, but it screams "template". This
skill forces deterministic, premium decisions BEFORE you generate, and verifies them at the
end.

Same philosophy as `antislop-web`, translated to the language of the slide. Zero MCP, zero
external service.

## When to use it

- At the start of any deck (pitch, proposal, report, keynote, onboarding): generate the
  `DECK.md` (Part A) before touching a slide.
- While building or refactoring slides: apply the directives (Part B) as generation rules,
  whether the engine is pptx, Google Slides or HTML.
- In your quality gate before delivery: run the pre-flight (Part C).

## When NOT to use it

- It does not replace the client's brand. The `DECK.md` is re-tokenized to the client's
  palette/typography (if a web `DESIGN.md` exists, INHERIT from it: the deck is the same
  brand in another medium, not a new identity).
- It does not replace content. A deck with impeccable structure and no substance is still
  bad. This skill gives the FORM that does not get in the message's way, not the message.
- A "document read aloud" deck (lots of text per slide, made to be sent and not presented) is
  a separate anti-pattern: if the deliverable is to be READ, it is a document; use
  `antislop-docs`.

## Engine integration (how it runs)

- **pptx (default for a .pptx deliverable):** an html2pptx workflow for exact positioning
  (e.g. a `pptx` skill), or `python-pptx`, or OOXML/unpack when editing a client template.
- **Google Slides:** a Slides automation/API when the client lives in Google Workspace and
  wants to edit/collaborate.
- **HTML/scrollytelling (deck as a page, not a file):** reveal.js, or your web stack if it is
  a deck-as-page. Also apply `antislop-web` and, for a cinematic hero, your scroll techniques.
- **Base discipline:** inherit ALL of `antislop-web` for palette, typography, color, motion
  and credible data. What follows are only the deck-SPECIFIC rules.

---

# PART A — DECK.md generator (per-presentation source of truth)

Generate a `DECK.md` in the project folder. Single source of truth for the deck's identity
and bans. Every slide is generated against this file.

## A.1 Dials (translate "make it nice" into rules)

Set three values 1-10. Suggested deck baseline: **DENSITY 3, MOTION 4, VARIANCE 6**. A deck
is AIRIER than the web (one idea per slide), with less motion (the transition must not compete
with the speaker) and medium-high variance (break the single template).

- **DENSITY** (one idea per slide 1 <-> data cockpit 10): in a presented deck, almost always
  <= 4. >6 only in a read-along deck (and there, question whether it is a document). Governs
  the word ceiling (A.4).
- **MOTION** (static 1 <-> cinematic build 10): >5 enables per-fragment builds (revealing
  point by point) and continuity transitions. Never vendor transitions (cube, free morph,
  page-curl). Always respects `prefers-reduced-motion` in HTML.
- **VARIANCE** (one template 1 <-> every slide different 10): >4 BANS the single repeated
  layout; forces rotating through the A.5 archetypes. >7 starts to cost coherence: raise only
  in editorial/keynote decks.

## A.2 Narrative structure (the deck's #1 lever, the one the web does not have)

The biggest tell is NOT visual, it is structural: **generic title + bullet list**. Kill it
with an architecture decision, not a color one.

- **Assertion-evidence (Alley), mandatory:** the slide title is a COMPLETE SENTENCE that
  states the point ("Sales fell 18% after the inventory outage"), not a label ("Sales"). The
  body is the VISUAL EVIDENCE of that sentence (a chart, an image, a big number), not the same
  sentence chopped into bullets.
- **One idea per slide.** If a slide has two assertions, it is two slides.
- **Arc, not stack:** the deck tells something (situation -> tension -> resolution / question
  -> answer -> implication). It is not a dump of sections. The sequence of titles, read alone,
  should already tell the story (the "titles-only" test).
- **BAN bullet soup:** bullet lists as the primary content of a slide. A bullet is allowed
  only when items are GENUINELY parallel and scannable (3-5 max), never as a chopped paragraph
  or filler.
- **BAN shell slides:** an "Agenda" that only lists what is coming, an empty
  "Thank you/Questions?", an "Introduction" that asserts nothing. The close carries ONE
  concrete action (A.5).

## A.3 Color, typography, materiality (inherited, with deck nuances)

- **Inherits `antislop-web`:** one accent (sat < 80%), neutral bases, no purple/neon, never
  pure `#000`, no emojis, no `Inter` in premium contexts, hierarchy by weight and color. If a
  client `DESIGN.md` exists, the deck uses THAT palette and typography.
- **Deck scale:** text is read from 3 meters. Slide title genuinely large; body minimum
  generous (never 12pt filler). Hierarchy by SIZE is legitimate here (unlike the web): title
  >> subtitle >> note.
- **AA contrast over the real projection background.** Text over a full-bleed photo only with
  a solid scrim/veil that guarantees contrast; never light text floating over an image with
  light areas.
- **Icons:** one consistent stroke set, or none. Never emojis as bullets. Never clipart or the
  vendor's default icon set.

## A.4 Content ceiling per slide (hard rule)

- DENSITY <= 4: at most ~1 assertion (title) + 1 evidence element. If the title runs past ~15
  words, it is two ideas.
- No paragraphs on the presented slide. Detail goes to the SPEAKER NOTES, not the slide.
  Engines support notes: use them.
- Numbers as the protagonist: one big number (`mono`, high contrast) beats a sentence that
  describes it. Organic, real figures (inherited: no 99.9%).

## A.5 Slide archetypes (break the single template)

Define a system of 5-8 archetypes and ROTATE through them. A single-mold deck is the tell of
VARIANCE 1. Base archetypes:

- **Cover:** assertive title + one real sub-line (not a generic "Presented by"), one owned
  visual anchor. No vendor gradient.
- **Section divider:** a color/slide change that marks a chapter; short, it breathes.
- **Assertion-evidence:** title-sentence + 1 chart/image/diagram. The workhorse.
- **Big number / stat:** one dominant number full-screen, with its source in a small footer.
- **Quote / testimonial:** a real quote attributed to a real person. No giant decorative quotes.
- **Comparison:** before/after, A vs B, in two clean zones (not "three identical cards").
- **Diagram / flow:** hand-built with owned boxes and connectors; NEVER SmartArt.
- **Close with action:** ONE concrete next action (what the audience does now), not "Thanks".
  Real contact details if relevant.

## A.6 Charts and tables (data-ink, the deck's technical tell)

- **No chartjunk:** no 3D, shadows, 3D pie, bar gradients, thick gridlines, legends when you
  can label the series directly.
- **Data palette = the deck's** (sequential/categorical derived from the accent), NOT the
  default Excel/Sheets/Chart.js rainbow.
- **Direct labeling** on the series/bar; the eye should not jump to a legend.
- **One chart says one thing:** the slide title already says WHAT to see in the chart.
- **Tables:** no box-borders per cell; use `border-t`/dividers, right-align numbers in mono,
  highlight only the row/cell that matters.

## A.7 Motion (under the right tier)

- Default transition: cut or short fade. Per-fragment builds only to reveal in the order of
  the speech (the point appears when the speaker says it), never as decoration.
- No vendor transitions (cube, automatic morph, page-curl, "sparkle").
- In an HTML deck: inherit A.7 from `antislop-web` (only `transform`/`opacity`,
  `prefers-reduced-motion`, lightest tier).

## A.8 Anti-patterns (the deck's AI tells — encode as "NEVER" in DECK.md)

No title + four bullets as a mold. No bullet soup. No same slide repeated. No blue-gradient
cover with a giant centered title. No empty "Agenda"/"Thanks"/"Questions?". No emoji bullets.
No SmartArt or clipart. No 3D charts or rainbow palette. No generic stock photo with unreadable
text on top. No paragraphs on the slide (they go to notes). No `Inter`/Calibri/Arial default.
No fake round numbers. No AI copy cliches ("Elevate", "Seamless", "Unlock", "Next-Gen", "In
today's world"). No untouched vendor template. No "Team" slide with stock avatars and "John Doe".

## A.9 Signature element (the one AFFIRMATIVE rule — mandatory)

As on the web: passing every ban stops the deck from looking generated, but does not make it
memorable. **Each deck declares ONE signature element**: the device it is remembered for. Just
one. Two signatures = none.

Criteria (all three): **memorable** (describable from memory a week later), **owned** (comes
from the content/business, not a catalog of effects) and **sustained** (coherent across the
deck, not one firework on the cover).

It can live in any layer:
- **Data:** one real business figure presented as nobody in the sector presents it (the best
  kind: it cannot be copied without the business).
- **Visual system:** a slide treatment, a graphic motif or an owned grid that threads the deck.
- **Typography:** a display face with character used structurally on every divider.
- **Sequence:** a narrative device that returns (a counter, a map that completes, a "before"
  that resolves slide by slide).

Guard: declared in `DECK.md` BEFORE building and verified in the pre-flight. If you cannot name
it in one sentence, it does not exist.

## A.10 Output template (DECK.md)

```markdown
# Deck: [Title] — Client [X] — [purpose: pitch/proposal/report]

## 0. Dials
DENSITY: n | MOTION: n | VARIANCE: n   (deck baseline 3/4/6)

## 1. Format and engine
Aspect: 16:9 | Engine: pptx (html2pptx) / Google Slides / HTML(reveal)
Inherits brand from: [client DESIGN.md | new identity declared below]

## 2. Narrative arc (titles-only test)
[The sequence of title-sentences, read alone, tells the story. List the titles.]

## 3. Signature element (mandatory, exactly one)
**[Name in one sentence]** — [what it is, which layer, why it comes from this content.]
Sustained in: [where it recurs across the deck].

## 4. Palette and typography
- Accent (#XXXXXX) + neutrals | Display: [font] | Body: [font] | Mono: [font]
- Data palette derived from the accent (not rainbow)

## 5. Archetype system
[The 5-8 archetypes to use and when; rotation rule]

## 6. Charts
[Type per data, direct labeling, no chartjunk, data palette]

## 7. Anti-patterns (BANNED)
[List from A.8 adapted to this deck]
```

---

# PART B — Production directives (by engine)

Rules for generating the real deck. Pick the engine by the requested deliverable.

1. **pptx from scratch -> html2pptx.** Lay out each slide in HTML with exact positioning and
   convert. State the design approach BEFORE coding. 16:9, safe margins, content inside the
   usable area.
2. **pptx over a client template -> OOXML/unpack.** Read the theme (colors/fonts) and respect
   the brand; never a foreign theme on top. Edit the XML, do not rebuild.
3. **Google Slides -> Slides automation/API.** When the client collaborates in Workspace. Same
   A.2-A.9 rules; make sure the font exists in Google Fonts.
4. **HTML/reveal -> reveal.js + antislop-web.** Deck-as-page or to project from a browser. Only
   `transform`/`opacity`, `prefers-reduced-motion`.
5. **Speaker notes ALWAYS:** detail that does not fit on the slide goes to speaker notes, not
   the slide. All three engines support it.
6. **Verify fonts/deps before use:** if the font is not embedded or available in the engine, it
   falls back to a system font and breaks the brand. Confirm availability.
7. **Credible data:** organic figures, real names, sources cited in the footer.
8. **Re-tokenization:** if a client `DESIGN.md` exists, the deck uses that palette, typography
   and signature element in deck form. The client must not be able to trace the deck to a
   template or a recognizable vendor default.

---

# PART C — Pre-flight (quality gate before delivery)

Any failure = not shippable until fixed.

- [ ] **Titles-only test:** read in a row, the title-sentences tell the story (A.2).
- [ ] No title + bullets as a mold; no bullet soup; one idea per slide.
- [ ] No shell slides (empty Agenda, Thanks/Questions, Intro that asserts nothing).
- [ ] **Signature element (A.9) present, single, sustained.** Name it in one sentence.
- [ ] VARIANCE met: archetypes rotate, no single repeated template.
- [ ] Per-slide content ceiling respected; detail is in speaker notes.
- [ ] Charts without chartjunk, with the deck's data palette and direct labeling (A.6).
- [ ] AA contrast over the real background; text over a photo with a scrim; never unreadable.
- [ ] Zero A.8 AI tells (cover, icons, SmartArt, copy, stock, numbers).
- [ ] Close with ONE concrete action, not "Thanks".
- [ ] Everything re-tokenized to the client brand (no vendor default).

## Limitations

- It gives form discipline, not a guarantee the argument convinces: content rules.
- One idea per slide can raise the slide count; that is fine, a deck that is dense to read is
  not a good deck to present. If the deliverable is to be READ, it is a document.
- The defaults (archetypes, tiers) are 2026; check them against the brand and a11y before
  locking them in.
