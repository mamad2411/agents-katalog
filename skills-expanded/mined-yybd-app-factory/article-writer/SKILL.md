---
name: article-writer
description: >-
  Write a page's words from an approved brief — an article, a case study or guide, and
  the pages for people who are choosing: an alternatives page, a comparison, a landing
  page for one use case, a concept page. The answer first, every claim traced to
  first-hand material or a dated source, honest about any competitor named, in every
  language the site ships — each written as that language. It follows the brief
  `seo-strategist` produced, and returns a claims ledger and the open TODOs. Use when the user asks to write or draft an article, a blog entry, a case study, an
  alternatives or comparison page, a landing page, or to write up a brief ("write the
  article", "כתוב את המאמר", "תכתוב מאמר לבלוג", "כתוב דף השוואה", "נסח את הדף
  מהשרטוט"). It does NOT choose the topic or the angle
  (`seo-strategist`), does NOT decide a page's structure (`page-builder`) or write the
  product's own page or store listing, does NOT polish existing text (`copy-edit`) or
  write announcements (`announce`), and never publishes.
---

# article-writer — from a brief to a page worth quoting

It writes two kinds of page from a brief: **articles** (an argument, a guide, a case
study, original numbers) and **pages for people who are choosing** (an alternatives page,
a comparison, a landing page for one use case, a concept page). The name stayed when the
second kind was added; everything below applies to both, and §2a adds what the second
kind needs.

A page earns its place when it says something the current results and an AI answer
do not, and can show why it is true. Everything else about writing for search in 2026
follows from that: the pages that rank, and the pages answer engines quote, are the ones
with real evidence stated early and plainly. Formatting is second-order; length is no
order at all.

So this skill writes **only from material that exists** — the brief's evidence inventory
and its listed sources. Where a fact is missing it stops and leaves a TODO. It never
fills a gap with a plausible number.

## Prerequisites

- **Tools:** none beyond Claude Code; the site's own build command where it has one (the descriptor's `articles.build_command`).
- **Credentials:** none.
- **Hub (`$APP_HUB`):** optional — a brief or the product's facts may live there when the site's descriptor points to it; without one, both are in the site's repo.
- **Other tracks:** `copy-edit` (shared-track) is the pass every draft goes through before it is handed over; `announce` (announce-track) writes the posts once the page is live.

## 0. What it needs before a word is written

1. **An approved brief** — `briefs/<date>-<slug>.md` in the site's state directory, in
   the shape of `seo-strategist`'s
   [brief template](../seo-strategist/references/brief-template.md), with its gates filled
   and `Approved by the owner on:` dated.
   - **A gate is empty** (demand evidence, inventory check, thesis, what the piece adds,
     evidence inventory, inbound links) → stop and send it back to `seo-strategist`. A
     brief with no evidence inventory produces exactly the page nobody needed.
   - **No brief at all**, and the user wants an article anyway → say that the search
     half (query, inventory check, links, success metric) is `seo-strategist`'s, and
     offer the two honest routes: have it briefed first, or write from a **minimum** the
     user supplies now — thesis, reader, and the first-hand material — and record in the
     hand-over that the piece was written without a search brief.
2. **Where the page lives on this site.** For an article: the descriptor's `articles`
   entry (source path pattern, languages, front matter, build command); without it,
   read how the existing articles are stored and follow that; with neither, ask. For any
   other page: the structure `page-builder` decided (sections, order, call to action) —
   write into that structure, and do not invent one. Where the page's files belong to
   another skill (the site's own page or product-site skill, or a repo's ownership
   file says so), this skill writes the **copy** and hands it to that skill to place.
3. **How this site writes** — the descriptor's `voice` document, else the site's own
   product or voice document, else two of its published articles. The voice is the
   site's, not this skill's.

## 1. Open the evidence, then build the ledger

Before drafting, **open every item in the evidence inventory** — the measurement, the
code, the log, the screenshot, the commit — and every listed source. Then write the
**claims ledger**: one line per factual claim the article will make.

```
claim | supported by (file, command output, or URL + date) | where it appears
```

- A claim with nothing in the middle column is not written. It becomes a TODO for the
  owner, or it is cut.
- An external source is read at the source — the primary page, not a summary of it —
  and its date is recorded. If it no longer says what the brief says it says, the brief
  is wrong: say so.
- The ledger is returned with the draft. It is what lets the owner check the piece in
  minutes, and what lets a refresh a year later find which claims to re-verify.

## 2. Write it — the rules

**Substance**

1. Write only from the ledger. Never invent a number, a quote, a benchmark, a
   testimonial or a date.
2. Every statistic or outside claim carries its named source, a link and a date, in the
   sentence or right after it.
3. First-hand material is **shown, not described**: the real number, the real code, the
   real command and its output, the real screenshot.
4. Concrete specifics — versions, limits, prices, sizes, dates — are stated in plain
   text, never only inside an image.
5. Assert what the evidence supports, plainly. Hedge only where the uncertainty is real,
   and say why.
6. No contradictions: a number agrees with itself across the body, the table, the title
   and the meta description.
7. Neutral about competitors; no promotional adjectives about the site's own product.
   The article is not the product page.

**Structure**

8. **The first ~150 words give the answer or the result, and say for whom.** No
   scene-setting. The ~200 characters after the `h1` state what the page is and what it
   concludes — that string is often all an answer engine sees.
9. **Each section opens with its own answer** — one to three sentences, taken from the
   brief's outline, that can be understood without the rest of the page: name the
   subject instead of "it" or "this", repeat the key term.
10. Headings say what the section answers. Question form only where the brief marks a
    real query. In order, roughly four to ten in an article.
11. Define each key term once, on first use, as "X is …".
12. A table for a comparison or a spec, numbered steps for a procedure, a code block
    with its language for code. Never turn prose into bullets for the sake of
    "structure".
13. **One coherent article.** Do not fragment into micro-sections, and do not pad to a
    length: stop when the brief's questions are answered.
14. End with the result in two sentences and the single call to action the brief names.
    No new claims in the closing.
15. No FAQ block unless the brief lists real questions the body has not answered.

**The page**

16. Title, `h1`, opening statement, meta description and slug as the brief specifies;
    the meta description states the answer, not a teaser.
17. A named author who has the experience; visible published and updated dates. The
    updated date changes only when the substance does.
18. Place every internal link the brief lists, with its anchor text; the link to the hub
    sits on the first screen.
19. Alt text on every image that says what it shows; a real transcript for any video.
20. Structured data, where the site's templates add it, matches the visible content
    exactly.

**Integrity**

21. Quote no more than a short phrase from any source; say it in your own words.
22. Nothing aimed at manipulating a model's answer: no hidden text, no instructions to
    models, no "best X" list with the site's own product first.

## 2a. Pages for people who are choosing

Everything in §2 holds. These pages are read by someone deciding between options, and
quoted by answer engines for "what should I use" questions — which is why they are worth
making, and why they fail the moment a reader, or a model, catches them being unfair.

**Alternatives page** ("an alternative to X", "X for <platform>") — the reader knows X.

1. Say plainly what X is and what it does well, in the first screen. Name it exactly; a
   page that is coy about the product it is an alternative to is not believed.
2. Say who should **stay** with X. A page with no case for the other side reads as an
   advert and is quoted as one.
3. The differences are facts from the ledger — platforms, price, what each does and does
   not do — in one table. Every cell about X is sourced to X's own page, with its date.
4. Never claim anything about X that the ledger cannot back, never use X's logo or
   trade dress, and never imply an affiliation.

**Comparison** ("A vs B", or several options) — the same rules, and:

5. Compare on the criteria the reader in the brief would choose by, stated before the
   verdict, not on the ones where our product happens to win.
6. Include the options a fair comparison would include, even the ones that win.
7. Where the site's own product is in the comparison, say so at the top.

**Landing page** for one use case or audience.

8. Only where the product really serves that use differently — the brief must say how.
   A page that swaps the audience's name into the same copy is a doorway page.
9. The job, the proof (a real screenshot, a real number, a real workflow), the price, one
   action. Shorter than an article.

**Concept page** — an idea the site is built on, explained once.

10. Define it in the first sentence; explain it without selling; link to every page that
    uses it. It is the page the others point to instead of re-explaining.

**All four:** one call to action, the one the brief names; no countdowns, no invented
scarcity, no testimonial the owner cannot show the source of; and a visible "updated"
date, because prices and features in a comparison go stale.

## 3. Every other language — written, not translated

- Start from the brief's query **for that language**, which was researched separately;
  the title and `h1` follow it even when that changes the framing.
- Facts, numbers, code and sources are identical to the first version. Examples,
  idiom, sentence order and what needs explaining are that language's own.
- Terms the brief lists stay in their original script (product names, API names, error
  strings); everything else reads as natural prose in that language.
- All versions ship together and are updated together. A stale twin is worse than none.
- Where the brief says a language has no search demand for the topic, write it for its
  readers and say in the hand-over that its measure is readership.

## 4. Before handing over

1. **Read it against the ledger**, claim by claim. Anything the draft says that the
   ledger does not hold comes out.
2. **Read it as the reader in the brief**: after the first screen, do they have the
   answer? After the whole piece, can they do what the brief says they should?
3. **`copy-edit`** on every language version — the pass that finds the sentences a
   reader stumbles on, against the site's voice rules.
4. **The inbound links**: make the edits to the existing pages the brief names, or — if
   those pages are generated or owned by another skill — list each one with its exact
   anchor text for whoever owns them. A page with no inbound link does not ship.
5. **Build, do not publish.** Run the site's build command so the article renders and
   its share card, sitemap entry and language alternates exist; check the result. Going
   live is the site's own publish step and the owner's decision.

## 5. What comes back with the draft

- The files written, per language, and the existing pages edited for inbound links.
- **The claims ledger.**
- **TODOs** — every fact that was missing, every piece of evidence still to produce.
- **What in the brief could not be honoured**, and why.
- What the brief asked for after publication — the success metric and its date, the
  review date — so `seo-strategist` can log the action against its target.
- A reminder of the order for distribution: live → indexed → then `announce`, with a
  `utm_source` on every shared link.

## Boundaries

- **It does not choose the topic, the query or the angle.** `seo-strategist` does, in
  the brief; a brief with an empty gate goes back there.
- **It does not tighten copy that already exists.** `copy-edit` does — and edits this
  skill's own draft before it is handed over.
- **It does not write announcements or channel posts.** `announce` does, after the page
  is live.
- **It does not decide a page's structure.** `page-builder` does; this skill writes the
  words into the structure it is given.
- **It does not write the product's own page, its store listing or interface text.**
  Those come from the product's own facts through the skills that own them. An
  alternatives, comparison, landing or concept page is not the product page — it is a
  page for someone choosing, and it is written here.
- **It does not publish.** It writes source files and builds; the site's publish step
  is the owner's.
- **It does not invent.** A missing fact is a TODO, not a guess.
