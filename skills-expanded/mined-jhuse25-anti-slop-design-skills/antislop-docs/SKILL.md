---
name: antislop-docs
description: "Use when writing or reviewing any document (docx, Google Docs, PDF, report, proposal, memo) so it does NOT read or look AI-generated. A bias-correction engine for documents: kills the ChatGPT-essay shape with BLUF/pyramid structure, prunes bold-bombing and connector cliches, sets the prose-vs-list discipline, defines real editorial typography, requires one signature element, and generates a DOC.md per project. Pairs with antislop-web for shared visual discipline."
license: MIT
tags: [design, documents, docx, google-docs, writing, anti-slop]
---

# Anti-Slop Docs — so no document reads or looks AI-generated

Double goal: **remove the "AI tells" of a generated document** in its TWO layers. An AI-made
document gives itself away by how it is WRITTEN (an intro that restates the prompt, everything
in **bold**, "Furthermore/Moreover", bullets for everything, an "In conclusion" that summarizes)
and by how it LOOKS (Calibri 11 single-column, headings with no hierarchy, box-bordered tables,
zero air). This skill forces deterministic structure, voice and editorial design BEFORE you
write, and verifies them at the end.

Same philosophy as `antislop-web`: bias correction + signature element, here over the word and
the page. Zero MCP, zero external service.

## When to use it

- At the start of any document (proposal, report, memo, one-pager, whitepaper, case study):
  generate the `DOC.md` (Part A) before writing.
- While writing or refactoring sections: apply the voice directives (Part B1) and the editorial
  design directives (Part B2).
- In your quality gate before delivery: run the pre-flight (Part C).

## When NOT to use it

- It does not replace substance. A well-laid-out document with no real content is still empty.
- It is not for text that is PRESENTED (lots of titles, little prose, projected): that is a
  deck, use `antislop-decks`.
- Legal/regulated documents: the VOICE anti-slop applies, but the structure is governed by the
  norm/legal template; do not impose BLUF on a contract. Coordinate with the relevant legal
  process.

## Engine integration (how it runs)

- **docx from scratch -> docx-js/OOXML** or `python-docx`: build the .docx with real styles.
- **docx over a template / editing someone else's -> redlining/tracked changes.** For
  legal/business documents use the redlining workflow.
- **Google Docs -> a Docs automation/API** when the client collaborates in Workspace.
- **Final PDF -> a PDF engine** for the read-only deliverable.
- **Voice (text layer):** lean on a plain-writing / de-slop / proofreading skill as the "how"
  of the prose; this skill gives the discipline (what to prune, what to force).
- **Base discipline:** inherit from `antislop-web` the palette, the emoji ban, credible data and
  re-tokenization to the client brand.

---

# PART A — DOC.md generator (per-document source of truth)

Generate a `DOC.md` in the project folder. Single source of truth for structure, voice and
design.

## A.1 Dials (translate "make it look professional" into rules)

Set three values 1-10. Suggested baseline: **FORMALITY 6, DENSITY 5, ORNAMENT 2**.

- **FORMALITY** (conversational 1 <-> institutional 10): governs voice. An internal memo lives
  at 4; a regulatory whitepaper at 8. Do not confuse formal with stiff.
- **DENSITY** (airy one-pager 1 <-> dense technical report 10): governs prose per page and
  figure count. >7 forces an executive summary and navigation (table of contents, headers).
- **ORNAMENT** (sober editorial 1 <-> magazine with devices 10): almost always <= 3 in a
  business document. High ornament without justification is a tell (a Canva template).

## A.2 Structure (the document's #1 lever)

The biggest tell is the **model-essay shape**: an intro that reformulates the task, N sections
with a bold lead-in, a "Conclusion" that repeats. Kill it with architecture.

- **BLUF / pyramid (Minto), by default:** the conclusion and recommendation GO FIRST. The busy
  reader gets the what and the "so what" in the first paragraph; the detail supports afterward.
  Do not make the thesis wait until the end.
- **BAN the intro-that-restates-the-prompt:** no "In today's world...", "This document aims
  to...". First sentence = the single most important claim.
- **BAN the conclusion-summary:** the close delivers implication or next action, it does not
  repackage what was said.
- **Titles that inform:** a title states the section's point ("The migration pays back in 7
  months"), not a label ("Cost analysis"). Sentence case, no all-Title-Case, no ALL CAPS.
- **Each section earns its place:** if a section does not change the reader's decision, cut it.

## A.3 Voice (writing anti-slop) — the tell you READ

- **BAN bold-bombing:** bold only for real, sparse signposting (a key term the first time, a
  critical figure). If half the page is bold, nothing is bold.
- **BAN AI connector cliches:** "Furthermore", "Moreover", "Additionally", "It is important to
  note", "In today's fast-paced world", "Delve", "Leverage", "Robust", "Seamless", "Elevate".
  Concrete subject-verb-object sentences.
- **Prose as default, list as exception (A.4).**
- **Concrete over vague:** real names, figures, dates and examples. Zero filler ("several",
  "various benefits", "numerous advantages") without the data behind it.
- **Varied sentence rhythm:** not every sentence the same length and mold. Syntactic monotony is
  a tell.
- **No em-dash as a crutch** (overuse), no emojis, no decorative unicode. Quotes and dashes
  consistent with the document config.

## A.4 Prose vs list (discipline, the structural tell)

- **Prose is the default.** An argument, an explanation or a narrative go in paragraphs, not
  bullets. AI chops everything into lists because it is easy; it reads like notes.
- **A list earns its place** only when items are genuinely parallel and scannable (steps,
  requirements, criteria). 3-7 items; if there are 12, it is a table or two groups.
- **BAN one-line bullets chained as a chopped paragraph.** If the bullets form a running
  sentence, it was a paragraph.
- **Lists parallel in form:** all items the same grammatical structure (all start with a verb,
  or all with a noun). Mixing is a tell.

## A.5 Editorial design (the tell you SEE)

- **Real typography, not default.** A serif/sans pair with character (inherit from the client
  `DESIGN.md` if it exists). BAN Calibri 11 / Times New Roman 12 with no decision. Body with
  generous leading (1.4-1.5), measure 60-75 characters (not full page width).
- **Hierarchy by scale AND weight, consistent.** H1/H2/H3 with clear jumps and more space above
  than below (the heading belongs to the text that follows). No hierarchy by underline or ALL
  CAPS.
- **Margins and air:** generous margins; text glued to the edge is a default-template tell. Line
  spacing and paragraph spacing that breathe.
- **Designed tables and figures:** no box-borders per cell; use horizontal rules (`border-t`)
  and alignment (numbers right, in mono if they are data). Every figure with a number, an
  assertive caption and a source. Never a pixelated screenshot.
- **Cover/header with the client's brand,** not the vendor's default cover. Footer with
  pagination and a discreet metadatum.
- **No emojis, no clipart, no decorative bullet icons** (inherited).

## A.6 Data, citations and credibility (inherited + doc)

- Organic, real figures (no 99.9% filler). Every factual claim with its source; no invented
  quotes or numbers. Contextual names and examples, not "Acme"/"John Doe".

## A.7 Anti-patterns (the document's AI tells — encode as "NEVER" in DOC.md)

No intro that reformulates the task. No "In conclusion" that summarizes. No bold-bombing. No
"Furthermore/Moreover/It is important to note". No bullets for everything. No chopped-paragraph
bullets. No Title Case or ALL CAPS in headers. No Calibri/Times default. No box-bordered tables.
No emojis or clipart. No vague filler without data. No sentences all the same length. No AI copy
cliches. No fake round numbers. No vendor default cover.

## A.8 Signature element (the one AFFIRMATIVE rule — mandatory)

Passing every ban makes a correct but forgettable document. **Each document declares ONE
signature element**: the device it is remembered for. Just one.

Criteria (all three): **memorable**, **owned** (comes from the content/business, not a
template) and **sustained** (coherent across the document). It can live in:

- **Data/structure:** an owned way of opening every document for the client (a key-figures
  panel at the top, a "status in one sentence") that nobody in the sector uses.
- **Typographic system:** a display face with character in the headers, a recurring margin
  note, an owned callout treatment.
- **Voice:** a radical clarity (short sentences, zero jargon) sustained as a house style.
- **Figure:** an owned chart or diagram type that repeats and becomes recognizable.

Guard: declared in `DOC.md` BEFORE writing and verified in the pre-flight. If you cannot name it
in one sentence, it does not exist.

## A.9 Output template (DOC.md)

```markdown
# Doc: [Title] — Client [X] — [type: proposal/report/memo/whitepaper]

## 0. Dials
FORMALITY: n | DENSITY: n | ORNAMENT: n   (baseline 6/5/2)

## 1. Format and engine
Deliverable: docx / Google Docs / PDF | Engine: docx-js / Docs API / PDF
Inherits brand from: [client DESIGN.md | identity declared below]

## 2. Structure (BLUF)
[The thesis/recommendation in one sentence (goes first). Then the section skeleton, each with
its title-that-informs. Mark whether it carries an executive summary and a table of contents.]

## 3. Signature element (mandatory, exactly one)
**[Name in one sentence]** — [what it is, which layer, why it comes from this content.]
Sustained in: [where it recurs].

## 4. Voice
FORMALITY n; prose by default; connector/bold bans; list only for [cases].

## 5. Typography and layout
Display: [font] | Body: [font] serif/sans | Mono: [data]
Measure 60-75ch, leading 1.4-1.5, generous margins, tables with horizontal rules.

## 6. Figures and data
[Figure type, numbering, cited source, palette derived from the accent]

## 7. Anti-patterns (BANNED)
[List from A.7 adapted to this document]
```

---

# PART B — Production directives

## B1. Voice (while writing)

1. First sentence = the most important claim (BLUF). Never a windup.
2. Prose by default; a list only if items are parallel and scannable.
3. Rare, deliberate bold; zero bold-bombing.
4. Prune connector cliches and vague filler; every sentence adds or is deleted.
5. Vary sentence length and mold. Reading aloud catches the monotony.
6. Writing support: a plain-writing / de-slop / proofreading skill as the "how"; this skill
   fixes the "what".

## B2. Layout (while building the file)

1. **docx from scratch -> docx-js/python-docx:** define REAL styles (heading 1/2/3, body,
   caption, quote) once and apply them; do not hand-format each paragraph. Font, leading, measure
   and margins per the `DOC.md`.
2. **docx editing someone else's or legal/business -> redlining:** tracked changes; do not
   rebuild the client's document, propose changes.
3. **Google Docs -> Docs automation/API:** native paragraph styles; font available in Google
   Fonts.
4. **PDF -> a PDF engine** for the final read-only deliverable.
5. **Verify the font is available** before locking it (inherited): if not, it falls back to a
   default and breaks the brand.
6. **Re-tokenization:** if a client `DESIGN.md` exists, inherit its typography, accent and
   signature element in document form. The client must not be able to trace their doc to a
   template.

---

# PART C — Pre-flight (quality gate before delivery)

Any failure = not shippable until fixed.

- [ ] **BLUF:** the thesis/recommendation is in the first paragraph, not at the end (A.2).
- [ ] No intro-that-restates-the-task; no conclusion-summary.
- [ ] Titles that inform, in sentence case (no Title Case/ALL CAPS everywhere).
- [ ] Prose by default; lists only where they earn it and are parallel (A.4).
- [ ] No bold-bombing; bold sparse and deliberate (A.3).
- [ ] No AI connector cliches or vague filler without data.
- [ ] Varied sentence rhythm (read a random paragraph aloud).
- [ ] Real typography (no Calibri/Times default), measure 60-75ch, generous leading (A.5).
- [ ] Consistent header hierarchy; margins and air; tables with horizontal rules, not boxes.
- [ ] Figures numbered with an assertive caption and a source; data organic and cited.
- [ ] **Signature element (A.8) present, single, sustained.** Name it in one sentence.
- [ ] No emojis/clipart; cover with the client's brand, not the vendor default.

## Limitations

- It gives structure, voice and layout; it does not guarantee the argument is correct: substance
  rules.
- In legal/regulated documents the structure is set by the norm; apply only the voice and layout
  layer that does not contradict the legal requirement.
- The defaults (dials, typography) are 2026; check them against the brand and a11y before
  locking them in.
