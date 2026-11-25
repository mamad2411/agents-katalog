---
name: marketing
description: Writes the words for a site or a product from evidence, not from adjectives. Crawls the actual source (a repo, a folder, a live site, a package), searches the category for what competitors claim and what buyers say, decides the positioning as one block, then writes the copy for every page with a claim-to-proof ledger beside it. Use when the user asks for copy, headlines, a tagline, a value proposition, landing page words, messaging, positioning, a pitch, pricing text, meta descriptions, or says the copy sounds generic, corporate, or like it was written by a machine.
license: CC-BY-4.0
---

# Marketing

Most product copy fails for one reason: it was written before anyone knew what the product does. Adjectives fill the gap where a fact should be. This skill removes the gap. Read the thing first, then the category, then decide, then write.

The order is fixed. Skipping to the writing step is what produces "seamlessly supercharge your workflow".

## What good looks like

- **A stranger can repeat it.** One sentence, no jargon, a noun that belongs to this product.
- **Every claim has an address.** A line of copy either points at something the product really does, or it gets smaller until it does.
- **The reader is one person in one situation.** Not "teams", not "businesses". A person with a problem at a specific moment.
- **It survives the swap test.** Put a competitor's name in the headline. If it still reads true, the headline is about the category, not the product.
- **Nothing shouts.** No exclamation marks, no "revolutionary", no exclamation stacked on a promise nobody can check.

## Run it

1. **Crawl the source.** Get the material before forming an opinion.
   - A URL, a folder, or a repo: `node <skill folder>/scripts/crawl.mjs <url|dir> --out site-brief.raw.md`
   - It writes every page's title, meta, headings, body paragraphs, links and prices for a site; for a folder it reads the README, manifests, docs, routes and CLI help. Every block is tagged with its source path.
   - Read that file before writing a word. What it could not find is listed at the bottom, and that list is your work queue.
   - See [references/research.md](references/research.md) for what to do when the crawl is thin.
2. **Search the category.** Two questions: what do competitors claim, and what words do buyers use when they complain. Sources and queries are in [references/research.md](references/research.md). Collect the phrases verbatim, with the URL beside each. Those phrases become your headlines; competitor claims become the sentences you can say and they cannot.
3. **Decide.** Write the block in [Positioning](#positioning) below. It is short and it is the input to everything after it. Show it when the user is present.
4. **Write.** Follow [references/copy.md](references/copy.md). Write into the page, not into a document. Every page gets: `h1`, subhead, sections, one primary call to action, microcopy, meta title, meta description, alt text for every image that carries meaning. Plus the 404 and the empty states.
5. **Audit the words.** Run the copy checklist at the end of this file against the finished page. Anything that fails gets rewritten, not softened.

## Positioning

Write these eight lines. Never publish them; they keep the writing honest.

- **Product.** What it does, for whom, in one plain sentence with no adjectives.
- **Reader.** One person, one situation, one thing they are trying to finish today.
- **Pain.** The problem in their words, copied from a review, an issue or a forum post. With the source.
- **Promise.** The one change after they use it. Measurable if a number exists; concrete if not.
- **Mechanism.** How it delivers that promise, in one line. This is what makes the copy impossible to swap.
- **Proof.** Two or three facts that make it believable, ranked strongest first. Each tagged `verified`, `found` or `needs: ...`.
- **Objections.** The three reasons a real buyer says no, in their words, with the honest answer to each.
- **Banned claims.** What this product must never say, because it cannot back it up.

## The ledger

Every claim on the page gets a row. Keep it beside the copy or in the report, never inside the page.

| Claim on the page | Evidence | Label |
| --- | --- | --- |
| "113 of 113 tools passing" | test run output, 2026-11-14 | verified |
| "replayed before delivery" | code path `replay.ts:41` | found |
| "used by 10,000 teams" | nobody knows | needs: real number or cut |

Rules: `verified` means you or the user saw it happen. `found` means it is in the source. `needs:` means it ships marked or it does not ship. An inference from code is `found`, never `verified`, and it never becomes a customer-facing number.

## Standing headings

Reusable shapes, in order of how much proof they need. Fill them with this product's nouns.

- **Outcome + mechanism.** "Pentesting that only touches what you've signed for." The second half is the mechanism. Without it the headline fits anyone.
- **Constraint as the promise.** "Nothing runs until four gates pass." A refusal is easier to believe than a capability.
- **Before and after.** "Stop rewriting the same README." The pain, then the exit.
- **Number with a reference.** "4 gates, 25 assets, one run." Only when the numbers are real and the reader can check them.
- **What it is, plainly.** "A hosted pentesting engine for your AI workspace." Weaker than the above, and always available when there is nothing else.

## Checklist

- [ ] The headline contains a noun from this product and could not be swapped onto a competitor's
- [ ] One primary action per page, named by what the reader gets, not by what the product does
- [ ] Every claim has a ledger row, and every `needs:` claim is marked in the page or cut
- [ ] No exclamation marks, no "!", no "!!" anywhere in interface text
- [ ] No hype words: supercharge, seamless, unlock, magic, revolutionize, game-changing, effortlessly, next-generation, AI-powered
- [ ] No greeting headline, no "Welcome to", no "Introducing" badge
- [ ] Headlines, subheads, labels, buttons and captions end without a period; only paragraphs of several sentences keep theirs
- [ ] Labels are short: "Search", not "Search anything..."
- [ ] A change states its comparison: "+12% vs last month", never "+12%"
- [ ] Numbers use one format across the page, with `tabular-nums`
- [ ] Sentence case; no uppercase labels; no italics for emphasis
- [ ] Every image that means something has descriptive alt; decorative images get empty alt
- [ ] Meta title 50 to 60 characters, description about 150, both unique per page
- [ ] Placeholders are visible as `[needs: ...]` in the page and listed in the report
- [ ] The 404 and the empty states exist and say something real
- [ ] Read it aloud. Anything you cannot say to a person's face gets cut

## Do not

- Do not invent customers, logos, numbers, reviews, awards or timelines.
- Do not use scarcity that is not real, or countdowns to dates that do not exist.
- Do not promise a feature the product does not have, even if the design has a place for it.
- Do not write a section the product cannot fill with a fact.
- Do not keep a sentence because it sounds good. Keep it because it is true and specific.

Full rules for voice, lengths and controls: [references/copy.md](references/copy.md). Category research and source etiquette: [references/research.md](references/research.md).
