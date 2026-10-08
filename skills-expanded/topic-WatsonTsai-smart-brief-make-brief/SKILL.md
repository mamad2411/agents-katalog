---
name: make-brief
description: Produce a local HTML page a human can actually read and decide from - a narrative decision brief, an item-by-item technical review page, or a mechanism explainer that walks through a system and its terminology. Triggers when the user says "write this up as an HTML page for me", "I don't follow, give me the full context", "make me a decision page / review page", "pull the last few days into one document", "brief me on this properly", or "/make-brief". The core moves are: establish motivation before results, explain causal chains with inline SVG, and mark self-corrections and evidence strength honestly.
---

# make-brief - HTML pages built to be understood and decided on

## Why this skill exists

The same piece of work was once delivered twice.

The first version opened with the shortlist: four candidate designs for a data pipeline, a table of
throughput and error-rate metrics, and a ranking. The reader's response was:

> "I don't really follow. Give me fuller context so I understand what we are doing."

The second version opened with the mechanism instead: each nightly run reads from whichever replica
is least loaded, replica lag differs between runs, so the row count you get depends on which replica
answered - which means that without pinning a snapshot, a lag difference gets read as real growth in
orders. Only after that did it reach the method, and only then the four candidates. The response was
"this one is good."

**The data in the two versions was identical. The only difference was whether the reader's
prerequisite knowledge had been built first.**

This skill makes the second version the default.

## The page is written in the reader's language, not in the language of this file

This skill file, `starter.html`, and every example in them are written in English. That is the
language of the instructions. **It is not a decision about the language of the page you produce.**
Write the page in the language the reader will read it in - which in practice means the language the
user has been talking to you in. A page that follows every structural rule here and is written in a
language its reader has to translate has failed at the one thing the skill exists for.

The examples are here to show the **shape** of a sentence, not to supply its words. "Queue time" as
an h2 is demonstrating that a heading names the thing under discussion and stops there; the opening
paragraph beneath it is demonstrating that the argument starts from where the problem came from.
Reproduce those shapes in the target language; do not carry the English across.

Three things get missed in that order, every time the output is not English:

1. **The skeleton strings inside `starter.html`.** Placeholders in `[square brackets]` are obvious,
   but the file also ships default wording that is already valid English - `[Summary]`, `[done]`,
   `[My recommendation:]`, the table headers, the chip labels. Those are bracketed for exactly this
   reason: they are wording to be replaced, not furniture. Copying the file and only filling in the
   blanks yields a page with translated body text sitting inside an English frame. **Grep the
   finished file for `[` - anything still bracketed was missed.**
2. **`<html lang="...">`.** The starter ships `lang="en"` as a working default. It must end up naming
   the language the page is actually in (`zh-Hant`, `ja`, `de`, ...). Screen readers take
   pronunciation from it and browsers take line breaking and font matching from it, so a wrong value
   is not cosmetic. While you are there, check that the font tokens still list a fallback face
   covering the target script; the ones shipped in `starter.html` cover CJK. In a script whose
   glyphs already carry their own advance width - CJK is the common case - also zero the positive
   `letter-spacing` on the small uppercase labels (`.eyebrow`, `.key .kt`, `thead th`, `.chip`,
   `.cand-rank`, `.metrics .k`, `.decide .dn`, and their neighbours). Those values are tuned for
   Latin capitals and read as broken spacing otherwise. Leave the negative values on `h1`/`h2`/`h3`
   alone; they are deliberate and amount to a fraction of a pixel.
3. **The trigger-word lists in section G.** Those lists are English vocabulary. The principle behind
   each rule carries over to any language; the words that let you detect a violation do not. See the
   note at the top of section G.

---

## A. When to use this

**Use it when:**

- The user has to decide something, and the context needed for that decision is scattered across
  several meetings, several scripts, and several files.
- You owe an item-by-item confirmation list where each item needs human judgement (reading an image,
  checking a number, weighing a trade-off).
- A round of research is closing and it needs one document that can be read start to finish - not a
  `report.md` written for another agent to parse.

**Do not use it when:**

- Three paragraphs in the conversation would cover it. Then write those three paragraphs.
  Handing over a file path alone does not count as delivering the work: the claim, the evidence, and
  the decision the reader has to make always go in the conversation itself.
- The material is going to be presented out loud. Build slides instead.
- The output is a durable conclusion for agents or future sessions to read. A plain
  `docs/reports/*.md` is enough; it does not need layout.

> Note: the HTML page never replaces printing the conclusion in the conversation. After the page is
> written, the conversation still has to carry the summary - claim, evidence, what you need decided.
> The HTML is the layer the reader can descend into. It is not the delivery itself.

---

## B. Four questions to answer before writing a single word

1. **Who is the reader?** Usually the person who asked, and they are the person who has to make the
   call. They know their own material and do not know the things you looked up in the last few days.
   They will often carry this page into a conversation with someone else, so **any sentence whose
   reasoning they cannot reproduce from memory is a liability.**
2. **What are they deciding?** Write the decision as one sentence. The whole document exists so that
   this sentence can be answered. Everything else is supporting cast.
3. **What prerequisite knowledge are they missing right now?** List the gaps one by one.
   **Every missing prerequisite becomes an earlier section.** That is the single reason the failed
   first version failed.
4. **Is the reader starting from zero on this topic, or do they already have a base?**
   **Do not ask them. Look.** The reader's own material usually answers it: their existing
   projects and repositories on this subject (written by them, not scaffolded for them today), their
   notes or wiki, any experience they have written down, any conventions they have codified, and
   their git history in this area. If most of those are empty, write for a starter: keep the
   foundation sections, define every term where it first appears, one mechanism per section. If
   most of them have substance, skip the foundations and go straight to the detail - do not spend
   the reader's time explaining what they know better than you do.

   **State the inference in one line of the standfirst**, for example "This page assumes you are
   new to X (basis: no notes on it in your wiki)." The inference will sometimes be wrong - people
   know things they never wrote down. Saying it out loud costs nothing and lets the reader correct
   it at a glance; asking costs them a round of attention every single time.

### The 30-second self-check (run it on the outline, not on the finished draft)

- Take the **first section** on its own. Is it explaining why this thing exists, or is it explaining
  what you did and what came out? If it is the latter, you have rebuilt the failed version. Go back
  and add the motivation section.
- Read straight through. Everywhere you think "the reader has to know X first", **add a section
  before that point.** Do not make the reader supply it.
- Move the decision section to the very front as a thought experiment. If it still reads fine there,
  the context in front of it was filler. If it stops making sense, the ordering is right and the
  decision belongs at the end.

### B-2. Updating an existing page: rewrite it, do not stack patches

**Every update rewrites the whole document and keeps the context intact. Do not keep appending.**

Why: incremental additions turn the section order into a chronology of the author's mistakes instead
of the order the reader needs. A real case: after four rounds of patching, a page had grown to 11
sections and 86 KB. Section 07 was a whole section of superseded results kept only so section 06 had
something to contrast against. Five verification results were spread across three different
chapters. Two self-corrections each sat in "the day it happened" rather than in the topic they
belonged to. The reader had to walk through the author's error history to reach the conclusion.
Rewritten as narrative, the same material was 9 sections and 67 KB - **shorter, and more complete in
context**: the verifications merged into one continuous section, each self-correction folded into
its own topic, the diagram count cut from 20 to 17.

How to do it:

- Before editing an existing page, ask: "with this new part added, is the section order still the
  order the reader needs?" **If it has already been patched twice, rewrite instead of patching a
  third time.**
- The skeleton for the rewrite is D-1: motivation -> why this method -> what happened -> current
  state -> limits -> decision. **Do not** put "old result vs new result" side by side, and **do
  not** order sections by correction date.
- Outdated content gets deleted, not demoted and kept. When a contrast genuinely helps, compress it
  into one line inside a correction box (the "what I originally said" line from F-1). Never keep a
  whole section for it.
- **Keep the old file** - it records how the thinking moved - but put a `.key danger` banner at the
  top pointing at the new file and saying why it was superseded. The new file's footer names what it
  was rewritten from and why. Name the new file with the new date; do not reuse the old date.

---

## C. Pick the document type (and decide whether to split)

| | **Narrative decision brief** | **Item-by-item technical review** | **Mechanism explainer** |
|---|---|---|---|
| Purpose | Get one decision made | Get a list confirmed | Get a system understood |
| How it is read | Once, start to finish | Jumped around, item by item | Once through, then kept as a manual |
| Section logic | Chronological or causal | Principles up front, then one card per item | System overview first, then one term per section |
| Decision format | "What you need to decide" at the end, each item with my recommendation | Each item carries a specific "please confirm" question | **No decision section.** It ends with a lookup table and an evidence-strength table |
| Diagrams | Few, only at the load-bearing causal steps | Many, schematic paired with the actual artifact | One per mechanism that is hard to picture |

**When to write a mechanism explainer:** the reader has to understand a system that was just built,
or a batch of terms they have never met, and they will come back to the page later. The trigger is
"explain this to me" or "draw me a system diagram", not "help me decide".

**When to split into two pages:** would the prerequisite knowledge for one sub-topic blow up the
section count of the main document and drown the decision itself? If yes, split. In the case this
skill was distilled from, the mechanism behind one sub-topic needed six sections of build-up;
folding it into the main brief would have taken it from 8 sections to 14.

**Rules when you split:** the main document keeps a stub - one paragraph of summary plus a link -
so the reader knows the conclusion without opening the second page. Link by relative filename (same
directory), and point at the second page from the standfirst at the very top.

---

## D. Structure templates

### D-1. Narrative decision brief

```
masthead    eyebrow (topic / occasion / date) / h1 (a one-sentence claim) /
            standfirst (how to read this page + link to any companion page)
sticky TOC  plain-language short labels, not jargon        <- only once there are five or more sections (H-7)
Section 1     what this work is and why it exists            <- motivation, must come first
Sections 2..N-3  what happened (chronological or causal)     <- one turn per section, with verbatim quotes
Section N-2   the complete current state (inventory: what is done, what is stuck, stuck on whom)
Section N-1   how to use this at the upcoming occasion (including the answers you must come away with)
Section N     what you need to decide (per item: the question -> why it needs you -> my recommendation + reasoning)
footer        sources, script paths, output directory, date
```

### D-2. Item-by-item technical review page

```
masthead   as above
TLDR       "one-minute version" keybox: motivation -> method -> what is missing -> result ->
           what I need from you (the whole thing in five short paragraphs)
01 Starting point   why this work is being done (with a schematic)
02 Concepts         the prerequisites needed to follow the rest (with a schematic)
03 Why this method  (with a schematic)
04 External requirements (the requester's own words + a clause-by-clause reading)
05 What we did      (step table: step | how | why)
06 How we know it is right (each piece of evidence as its own subsection + self-corrections)
07 The candidates   (cards: metric row -> figure -> why it ranks here -> please confirm)
08 Limits           (aimed at "this changes how you present it", not a disclaimer)
09 What you need to decide
footer
```

### D-3. Mechanism explainer

```
masthead    eyebrow / h1 /
            standfirst: the first sentence says WHAT WAS BUILT; only the second says how to read
                        the page. If you inferred the reader's starting level, say so here in one
                        line, with the evidence, so they can correct you.
TLDR        three-paragraph keybox labelled "what this is / how it was built / the thing that
            matters most" - not "motivation / method / result", which only reads well to someone
            who already knows what the subject is
Terms box   keybox: the three to six words that run through the whole page, defined together.
            Only the framing terms that block reading; per-section jargon stays in its section.
01..03      the system itself: overview diagram, what is shared with what, order of operations
04..0N      one term per section. The h2 is the term (optionally + .h2-en for the technical name).
            Four beats per section: background (where this problem came from) -> what it is ->
            how it works -> why it was designed this way. Close with one line: "remember this about X".
N-1         lookup table: every term on one screen, with a judgement column
            (for example "does it make a noise when it breaks?")
N           evidence strength: mark each claim measured / indirect evidence only / not verified
footer
```

**This type has no decision section.** The reader wants to understand, not to sign off. Forcing a
decision section on it produces a half-hearted brief instead of a usable manual.

### Fixed fields for every section

- **The h2 is a term or a short topic, never a full sentence.**
  Good: "Queue time" / "Job mix" / "Measurement method" / "The three lanes"
  Bad: "Separating the two waits needed three timestamps per job, not one stopwatch."

  This reverses an earlier version of this skill, which required assertion headings. The reason for
  the reversal: a reader who has both versions in front of them cannot scan the assertion one. A
  table of contents made of six full sentences has to be *read*, and by the time you have read it
  you have lost the thing you opened the TOC to find. **A heading's job is to make a section
  findable, not to win the argument.** The argument moves into the opening paragraph, where it has
  room to be made properly.

  Optionally follow the term with a smaller original-language or technical name using `.h2-en`,
  for example `Junction` followed by `NTFS reparse point`.
- **The first paragraph of a section is background, not the conclusion** (`.lede`, a slightly larger
  opening paragraph - there is no separate italic subtitle line any more).
  State where the problem came from before you define anything. The reader needs to know why this
  thing exists in their system before a definition means anything to them.
  - Bad: "A junction is a note holding another path, so two tools can share one directory."
    (opens with the definition and the conclusion at once)
  - Good: "Your skills live in directory A. The second tool only reads directory B. Copying them
    across means the two drift apart. To make both tools genuinely read *one* copy, something has
    to make B point at A - and on Windows that something is called a junction."
  - The test: after the first paragraph the reader should be asking **"so what is it?"**, not
    "so what?".
  - The conclusion moves to the end of the section. In a mechanism explainer make it an explicit
    one-liner ("remember this about X"); in a decision brief it is usually the closing sentence of
    the last paragraph, which reads less mechanically.
- **Explain a term in plain language the first time it appears, in place.** No glossary at the end.
  Mark it with `.term` (dotted underline).
  **Terms that run through the whole page (three to six of them) get one keybox near the top** -
  do not scatter them. Terms used in only one section stay in that section.
- **Name a term before you use a pronoun for it.** Writing "it" or "this mechanism" for something
  the running text has not named yet forces the reader to stop and reconstruct the referent.
  - Bad: "Failures are silent. You might assume that is a bug, but it is a deliberate design choice."
    (the "it" means fail-open, and the paragraph never says fail-open)
  - Good: "Failures are silent. This behaviour has a name - fail-open. You might assume fail-open is
    a bug, but it is a deliberate design choice."
  - **A term appearing in the h2 does not count as naming it.** The reader is following the prose.
- **Run the forward-reference scan before delivering** (see `check_forward_refs.py` in this skill's
  directory). It extracts the plain text, finds where each term first appears, and lists them in
  order so you can check that the definition comes first. Writers cannot catch this by re-reading -
  you already know what the words mean, so your eye skips over them.
- **Quote other people verbatim** (`.quote` + `<cite>`), never paraphrase. In a decision document,
  the precision of "what the other party actually said" is the credibility of the document.
- **Sentence-level writing follows section G.** This section governs the skeleton; whether a single
  sentence has a findable main clause, whether its abstractions are grounded, and whether its
  comparatives have a baseline all live there.

---

## E. Diagrams (this is where the page is won or lost - do not skip it)

### E-1. When to draw

| Situation | What to do |
|---|---|
| Explaining a **spatial or structural relationship** (what sits where, what points at what) | Draw it |
| Explaining a **causal chain** (why A produces B) | Draw it |
| Contrasting **two situations** | Draw it, side by side |
| Pure numbers, comparing magnitudes | **Table.** Do not draw it |
| A real artifact already exists (a rendered image, a screenshot, a plot) | Use `<img>` with an external file. Do not redraw it |

Three to five schematics is enough for one document. **Each one answers a specific "why".** If you
cannot say which "why" a diagram answers, cut it.

### E-2. The most effective composition: side-by-side contrast

In the pages this skill was distilled from, three of the four diagrams were the same pattern: put
"situation A" next to "situation B" and let the reader see the difference themselves - the pipeline
with the snapshot pinned versus without it, a small batch versus a large one, the request path with
the cache warm versus cold. The fourth was a cross-view contrast: a schematic of the mechanism next
to the actual output it produces.

**Decide what you want the reader to compare first, then decide what goes on each side.**

### E-3. Hard rules

- **Inline SVG.** No external dependency, scales freely, follows the theme. Schematics are always
  inline; never an external image file.
- **Every fill and stroke reads from a CSS variable**, and text uses a class (`.svg-label` and
  friends) rather than an inline `fill`, so dark mode recolors automatically. **A diagram with a
  hardcoded `#333` disappears in dark mode.**
- `viewBox="0 0 W H"` plus CSS `width:100%; height:auto`. Never hardcode width/height.
- `role="img"` plus `aria-label="one sentence describing it"`.
- Labels come in three levels: `.svg-title` (per panel), `.svg-label` (main annotation),
  `.svg-label-s` (fine print).
- **Color meaning stays consistent across the whole document.** For example: blue (`--flow`) is
  always the incoming flow, orange (`--accent`) is always the thing under discussion, gray
  (`--muted`) is always what is lost or discarded, red (`--danger`) is always the failure point or
  the bad news. All the diagrams in one page share the same mapping.
- Draw arrows as a `<line>` plus a `<polygon>` triangle by hand. Do not use `<marker>` - fill
  inheritance is awkward and it breaks easily in dark mode.

### E-4. The figcaption states the "so what"

A caption **does not describe what is in the picture.** It states what follows once the picture is
accepted, with the payload sentence wrapped in `<strong>`.

> Bad: "Diagram of batch size versus per-request latency."
>
> Good: "The same total work is sent either way, but a bigger batch means fewer round trips.
> Latency here is measured per request, so a bigger batch shows a lower number without anything
> actually getting faster. **This effect has to be removed before two runs with different batch
> sizes can be compared at all.**"

Four copy-and-adapt SVG patterns (two-panel contrast, three mechanisms side by side, schematic
paired with real output, a quantity changing with a parameter) are in `svg_patterns.md`.

---

## F. Honesty rules

1. **Mark self-corrections explicitly**, and give all three parts together: (a) what I originally
   said, (b) **why it was wrong**, and (c) **what to believe now.** An admission with no replacement
   evidence leaves the reader stranded.
   > Example: "On Tuesday morning I judged that the sample would be too small and recommended
   > dropping the comparison. That was wrong - counted properly, there are five times more usable
   > records than the threshold."
   >
   > Example: "I read the direction of that dependency backwards. The re-check did produce something
   > harder, though: reconstructing the order from 65 runs puts the disagreement at 1.2%."
2. **Mark evidence strength.** Which numbers are measured, which are inferred, and which are
   **unreliable and must not be quoted.**
   > "Only the first of the three timing runs is trustworthy. The other two were taken while the
   > cache was still warming, so those numbers are artifacts. **Do not quote them.**"
3. **Say out loud what should be deleted.** If a sentence in the draft cannot be reproduced, write
   "delete this line, do not say it in the meeting." Keeping the reader from carrying something wrong
   into a room matters more than the document looking clean.
4. **Check the metric before you rank by it.** For any number used to order things, ask first "what
   could this be confounded with", and quantify the confounder when you can.
   > Example: the p95 latency gap between two regions looks like a network effect, but the second
   > region also serves a different query mix. Measuring the share of heavy queries on each side
   > (12% / 13% versus 0% / 37%) reversed the ranking entirely.
5. **A ranking is a claim, so attach a refutable reason.** Put it in the card title directly:
   "why this dropped from first to second".
6. **Every decision item carries "my recommendation" plus the reasoning.** Do not list options and
   make the reader guess what you think. When you genuinely cannot recommend, write "I am not
   confident here, because X" - that is information too.
7. **The limits section points at action**: "this changes how you present it tonight", not a
   disclaimer.

---

## G. Sentence-level rules

These govern the prose you write. They do not apply to material you are quoting from someone else -
quotes stay verbatim, warts included.

> **The principles port to other languages; the word lists do not.** Every rule below is stated as a
> principle and then made checkable with English trigger words. When the page is in another
> language, keep the principle and **rebuild the list from scratch** - do not translate the English
> words and expect them to catch anything.
>
> Where this bites hardest:
> - **Rule 2 (action buried in a noun)** is detected in English by *perform / conduct / make* plus a
>   noun. Other languages bury the action with their own light verbs, and the English list will not
>   match a single one of them. Write out the equivalent construction for the target language before
>   you try to apply the rule.
> - **Rule 4 (references must resolve)** lists *this / that / it / they*. A language that routinely
>   drops the subject altogether carries the same risk in a form the list cannot see: the ambiguous
>   reference is the pronoun that is not there. Check that the subject of each clause is recoverable,
>   whether or not it is written.
> - **Rule 1 (keep the spine visible)** names the English failure - modifiers wedged between subject,
>   verb, and object. A language that puts its modifiers before the head noun instead fails in a
>   different position, so looking in the English place finds nothing.
> - **The mechanical check in G-2** counts `, and` / `, but` / `; `. It only fires on ASCII
>   punctuation. Under a writing system that uses full-width punctuation it returns zero matches on
>   every sentence, including the ones it should have caught. Substitute the target script's
>   punctuation, or check by reading.

**1. The spine must be visible at a glance.** Do not pack modifiers between subject, main verb, and
object. If one sentence carries background, condition, cause, result, exception, and an aside, split
it. Splitting usually reveals that some of those parts did not need saying.

**2. Do not bury the action inside an abstract noun.** "Perform an evaluation of" -> "evaluate".
"Make a determination" -> "determine". "Produce an improvement in" -> "improve". "Have an impact on
the market" -> "affect the market". Trigger words: perform, conduct, carry out, make, produce, cause,
achieve, followed by a noun.

**3. Every sentence has one visible claim.** The reader should not have to reach the end of the
sentence to learn what it was about. Avoid stacked conditions, chained causes, multiple reversals,
and long parentheticals in the middle. When there is a lot to carry, use several sentences and link
them.

**4. References must resolve instantly.** High-risk words: this, that, it, they, them, such, the
former, the latter, the above.
- Bad: "The company told the supplier that they had to adjust their prices." (whose prices?)
- Good: "The company asked the supplier to lower its prices."

**5. Information order equals comprehension order.** Give the premise before the judgement that
depends on it. Never use an unexplained concept and define it two sentences later.
- Bad: "This creates a demand-side economy of scale, meaning the product gets more valuable to each
  user as more users join."
- Good: "The more users join, the more valuable the product becomes to each of them. That effect is
  called a demand-side economy of scale."

**6. Delete.** For every word, sentence, and paragraph: if removing it leaves the reader with the
same information, the same logical relations, and the same tone, remove it. Fixed places to look:
sentences that restate the previous one, announcements that "the next part will discuss X" when the
next sentence is where the discussion actually starts, phrases that only add momentum, simple ideas
dressed as abstractions, and long constructions for something with a shorter existing name.
**The two most common failures in practice are hiding the action inside a noun (rule 2) and
announcing before starting (rule 6).**

**7. Ground the abstract words.** Value, impact, strategy, transformation, differentiation,
innovation, capability, competitiveness, optimization, enablement, resilience - each one obliges you
to check that the reader knows what it refers to here.
- Bad: "The strategy raised brand value."
- Good: "The strategy made the brand more recognizable at the high end, and raised the average
  selling price."

**8. Comparatives need a baseline.** Trigger words: higher, faster, more effective, cheaper, more
successful, substantially, clearly, mainly, leading, significant, outperforms, large numbers, a
minority. Every one of them should stop you to ask "compared with what?".
- Bad: "The company's growth clearly accelerated."
- Good: "Year-on-year revenue growth went from 8% to 17%."

### G-2. Extra rules when the page will be sent to an external reader

Apply these on top of the eight when the reader gets the page without the author next to them - an
external report, a page that will be emailed out, a printed handout. Pages written for the person
you are already talking to do not need them, because they can just ask you.

- **One claim per sentence, parallel openings.** Do not chain several findings with
  "and ... , and only ... , also ...". Mechanical check: if `, and` / `, but` / `; ` / ` also `
  appears twice in one sentence, split it.
- **No abbreviation the document has not defined itself.** A shared domain term is fine; a shorthand
  you invented while working is not, no matter how many times you used it in your notes.
- **No second person and no first person.** The finished piece is not addressed to anyone in
  particular.
- **A phrase with no verb is not a sentence.** Headings may drop the verb; body text may not.
- **When it will be printed or projected, no last line holding a single word.** Height measurements
  cannot see line breaks, so this one needs eyes on the rendered page, not just a character count.
- **Plain language takes more room than jargon** - usually 10 to 20 percent more. When it overflows,
  cut filler words. Do not shrink the type size; that trades away layout consistency, which costs
  more than the words did.

---

## H. Technical checklist for local delivery

1. **Full skeleton.** `<!doctype html>` / `<html lang="...">` with the document's actual language /
   `<meta charset="utf-8">` / viewport / a CSS reset. Hosted artifact platforms inject these for you;
   **a local file has to carry them itself, or any non-ASCII text renders as mojibake.**
2. **Write the file with the Write tool, or with a script that opens it as UTF-8 explicitly**
   (`open(path, "w", encoding="utf-8")`). Do not build it through a shell redirect or a shell
   "write these lines to a file" cmdlet - depending on the shell and the platform, those can apply a
   legacy code page or prepend a BOM, and both wreck non-ASCII content.
3. **Reference images by relative path** into your output directory (`../../output/xxx/chip.png`).
   **Do not base64-inline them** - the file balloons to tens of megabytes. State the cost in the
   footer: **this file cannot be sent on its own; away from the repository the images break.**
4. **Both themes.** `@media (prefers-color-scheme: dark)` plus a `:root[data-theme="dark"|"light"]`
   override, everything through CSS variable tokens. Theme toggle in the bottom right, persisted in
   localStorage (use a different key per document so pages do not overwrite each other).
5. **Semantic colors are independent of the accent.** `--ok` / `--warn` / `--danger` each get their
   own set including a `-soft` background. Do not make the accent moonlight as "good" or "bad".
6. **Text width.** `p { max-width: 68-70ch }`. Wrap tables in `.tw { overflow-x: auto }` so a wide
   table scrolls inside itself; **the body must never scroll horizontally.**
7. **Sticky TOC** once there are five or more sections, plus `section { scroll-margin-top }` -
   otherwise the anchor lands under the TOC.
8. `@media print { nav.toc, #themeToggle { display: none } }`.
9. Landing path: `<project>/docs/reports/<topic>_YYYY-MM-DD.html`.
10. **Open it in a browser when you are done**, and print the absolute path in the conversation:
    - Windows: `Start-Process <absolute path>`
    - macOS: `open <absolute path>`
    - Linux: `xdg-open <absolute path>`

**How to start:** copy `starter.html` wholesale and rewrite its content. **Do not retype the CSS
each time.** It already carries the tokens, reset, both themes, the theme toggle, and every component
listed below.

### Components in starter.html

| class | Purpose |
|---|---|
| `.keybox` / `.key` (`.ok/.warn/.danger`) | Emphasis box: thick left border plus a small label |
| `.callout` (`.ok/.warn/.danger`) | Inline aside, lighter than a keybox |
| `.quote` + `<cite>` | Verbatim quotation |
| `.tw` + `table`, `td.num`, `tr.hi`, `.was` | Table / numeric column / highlighted row / superseded value (struck through) |
| `.chip` (`.ok/.warn/.stop/.idle`) | Status label: done / in progress / not started |
| `figure.dia` | Inline SVG schematic plus figcaption |
| `figure.photo` | External image plus a monospace caption |
| `.cand` (`.best/.good/.caution`) plus `.metrics` / `.verdict` / `.checkq` | Item review card |
| `.decide` + `.rec` | Decision item plus my recommendation |
| `.chain` / `.stage` (`.flag/.cleared`) | Process chain, each stage marked cleared or stuck |
| `.agenda` | Ordered agenda (auto-numbered) |

---

## I. Pre-delivery checklist

- [ ] **The `<title>` has been replaced.** It lives in `<head>`, so nothing on the page itself
      reveals that it is still the placeholder - check the browser tab, not the page. Grep the
      finished file for `[`; anything still bracketed was missed, and the title is the one that
      gets missed.
- [ ] **If updating an existing page: confirm it was rewritten, not appended to** (B-2). No section
      exists only as "outdated but kept for contrast".
- [ ] The first section is about "why", not "results".
- [ ] **Every h2 is a term or a short topic, never a full sentence.** Read the TOC on its own: can
      you tell at a glance what each section covers, without reading whole sentences?
- [ ] **Every section opens with background** (`.lede`) - where the problem came from, not the
      definition and not the conclusion.
- [ ] **The standfirst's first sentence says what was built or what this is**, not how to read the page.
- [ ] **Ran the forward-reference scan** (`check_forward_refs.py`): every term is defined in the
      running text before it is used. A term in an h2 does not count as defined.
- [ ] **After changing the structure, grep for descriptions of the old structure.** Removing the
      italic subtitle line while leaving "the grey line under each heading is the takeaway" in the
      standfirst leaves the page lying about itself.
- [ ] Ran the sentence-level pass from section G: buried actions, unresolvable references, missing
      comparison baselines, ungrounded abstractions, announcement sentences.
- [ ] Every term is explained in place the first time it appears.
- [ ] Every schematic's caption states a "so what".
- [ ] Every SVG reads from CSS variables. Actually switch to dark mode once and look for anything
      that vanished.
- [ ] Self-corrections, untrustworthy evidence, and lines to delete are all marked.
- [ ] Every decision item carries "my recommendation" plus reasoning.
- [ ] The footer has sources, script paths, output directory, and the date.
- [ ] No mojibake in non-ASCII text. Open the file back with the Read tool rather than a shell
      `cat`, so terminal encoding cannot fool you either way.
- [ ] Every relative image path actually exists (list the directory once).
- [ ] **A separate summary is printed in the conversation** - claim, evidence, what needs deciding.
      Never hand over just the path.

---

## Bundled files

- `starter.html` - the full skeleton (tokens, reset, both themes, toggle, all components). Copy and
  use.
- `svg_patterns.md` - four reusable schematic patterns plus the color-meaning table.
- `check_forward_refs.py` - the forward-reference scan. Run it before delivering:

      python check_forward_refs.py your-page.html

  It lists every term by where it first appears, so you can confirm the definition comes first.
  The script finds the positions; deciding whether a spot counts as an explanation is still yours.
