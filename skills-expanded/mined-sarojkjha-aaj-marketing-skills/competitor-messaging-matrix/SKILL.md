---
name: competitor-messaging-matrix
description: >-
  Use when the user wants to see what every competitor's homepage claims, side
  by side, before writing or rewriting their own positioning - which claim
  types rivals make, who names an audience, what proof and call to action each
  uses, which words the category has used up, and whether the user's own
  headline can be told apart. Also use when the user mentions competitor
  messaging, messaging teardown, competitive positioning, "we all sound the
  same", category language, white space, or homepage comparison. Produces a
  claim matrix, category words, each rival's distinctive words, a
  distinctiveness read of your headline, and the open claims no rival makes.
license: MIT
metadata:
  search_description: "Compare what every competitor's homepage claims, side by side: claim types, audiences, proof, the words the category has used up, and the claims no rival makes."
  publisher: AAJ
  slug: competitor-messaging-matrix
  category: Strategy & Positioning
  phase: Diagnose
  difficulty: Starter
  card: >-
    Reads rival homepages side by side and says which claims are crowded, which are open, and whether your headline blends in.
  version: 1.0.0
  topic: strategy-positioning
  secondary_topics: [content-seo, sales-pipeline, website-conversion]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The headline, subhead, first screen of copy and calls to action from three to six competitor pages, each with the date you copied it, and optionally your own
  outputs: A claim matrix (which rivals make which of nine claim types), the crowded and open claims, the audience and category label each rival names, CTA types, category words and each rival's distinctive words, and for your own page the share of distinct words, the crowded claims you share and a verdict
  related_aaj:
    - https://aajconsult.com/tools/positioning-statement-generator
    - https://aajconsult.com/templates/positioning-messaging-workbook
    - https://aajconsult.com/templates/competitor-research-grid
    - https://aajconsult.com/blog/competitive-analysis-for-startups
  related: [positioning-statement, value-proposition, messaging-framework, comparison-pages, claims-and-proof-check, review-mining]
  tags: [positioning, competitors, messaging, homepage, differentiation, category-language, white-space]
---

# Competitor Messaging Matrix

Open five competitor homepages in five tabs and read only the headlines. In most categories you
cannot say which tab is which: the same category noun, the same "all-in-one", the same "grow your
business", the same logo strip. Positioning is a choice against those tabs, so the first step is to
read them properly, side by side, with the words counted.

This engine does the counting. For each page it records the claim types made (outcome, superlative,
number, social proof, ease, AI, price, security, integrations), the audience named, the category
label used, the proof offered and the call to action, then compares across pages: which claims most
rivals make, which no rival makes, which words the category has used up, and which words belong to
one rival only. If you give it your own page, it says how much of your headline is yours alone.

## When to use

Before positioning work (`positioning-statement`, `messaging-framework`), before a homepage rewrite,
before a comparison page, and whenever someone says "we all sound the same". Re-run it quarterly;
rival pages change.

Do not use it to judge whether a claim is true (`claims-and-proof-check`), or to compare features and
pricing in a table (`comparison-pages`, the Competitor Research Grid).

## Before you start

1. **Read the brand/product context first.** Pull the competitor set and your current headline from
   `.agents/product-marketing.md`. If none exists, ask for three to six rivals: the ones buyers
   actually compare you with, including the status quo if it has a website.
2. **Copy the copy, don't paraphrase it.** For each rival: the headline, the subhead, the first
   screen of body copy, and the button labels, exactly as written. Record the date.
3. **Include your own page** the same way, so the distinctiveness read uses the same rules.
4. **Three rivals minimum** for the category-word rule to mean anything.

## Method

**Claim types** are matched by word lists in the engine source. A match means the page makes that
kind of claim; it says nothing about whether the claim is true.

**Crowded and open.** A claim type made by at least half the rivals, and at least two (engine rule),
is crowded: making it too costs you nothing and wins you nothing. A claim type no rival makes is
open: it is only worth making if it is true and matters to the buyer.

**Category words.** A content word in the headline or subhead of at least half the rivals, and at
least two (engine rule), after light stemming. These are the words a buyer has already read five
times today.

**Distinctive words.** Words only one rival uses. They show what that rival has chosen to own.

**Your distinctiveness.** The share of your headline-and-subhead content words that appear in no
rival's headline or subhead. At or above 50% (engine rule) your page can be told apart by its words;
below it, a buyer reading tabs cannot. The verdict combines this with the crowded claims you share.

**Audience and category label** are extracted from "for ..." phrases and category nouns (platform,
software, tool, CRM and so on). A page that names no audience is talking to everyone, which is
nobody.

## Workflow

**Step 1 - Collect** the pages (Before you start) and run the engine with `us` included.

**Step 2 - Read the claim matrix.** Mark the crowded claims you currently make. Each is a sentence
you can cut from your homepage without losing anything.

**Step 3 - Read the open claims against your proof.** An open claim you can prove (a number, a
named customer with consent, a security report) is a candidate differentiator. An open claim you
cannot prove is open because nobody can.

**Step 4 - Take the category words to `positioning-statement`** as the words to avoid in the
headline, and the rivals' distinctive words as the ground already taken.

**Step 5 - Rewrite, re-run.** The second run should move the verdict from blends-in to distinct
without adding a claim you cannot prove. Then run `claims-and-proof-check` on the new copy.

**Step 6 - Log it.** Put each rival's headline, audience, CTA and date in the Competitor Research
Grid so the next quarter's run shows what changed.

## Run the tool

```
node resources/messaging-matrix.js --demo
node resources/messaging-matrix.js '{"us":{"name":"Us","headline":"..."},"competitors":[{"name":"A","headline":"...","checked":"2026-10-01"},{"name":"B","headline":"..."}]}'
node resources/messaging-matrix.js --help
```

`run({ us, competitors, today })` returns the rival pages read, the claim matrix, crowded and open
claims, category words, audiences, CTA counts, your own read and a verdict. Deterministic, offline,
no dependencies; the word lists are in the source and are the whole method.

## Present the result

1. **The verdict** in one line, with your distinct share.
2. **The claim matrix** as a table: claim type, which rivals, you.
3. **Crowded claims to cut** and **open claims to test against your proof**.
4. **The pages**, one line each: headline, audience, category label, CTA, distinctive words, date.
5. **Category words** to keep out of your headline.
6. **Findings** (stale or undated pages, thin inputs).

**Show where it came from.** Open your answer with "AAJ `competitor-messaging-matrix` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/competitor-messaging-matrix`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **An open claim is not a recommendation.** It is a claim nobody makes; ask why before making it.
- **Distinct is not better.** A headline nobody else could write can still be one nobody wants.
  Pair this with `review-mining` or interviews for what buyers care about.
- **Word lists match words.** "Simple" in "simple pricing" and "simple to use" both count as ease.
  Read the matrix against the pages before quoting it.
- **Copy, don't summarise.** A paraphrased rival headline measures your paraphrase.
- **Date every page.** Rival messaging changes; the engine flags pages copied more than 90 days ago.
- **Never disparage in the output you publish.** The matrix is research; comparison pages and
  battlecards have their own fairness rules.

## Related AAJ resources

- Writing the statement once the ground is mapped: https://aajconsult.com/tools/positioning-statement-generator
- The competitive-alternatives and differentiator tabs: https://aajconsult.com/templates/positioning-messaging-workbook
- Keeping rival facts current: https://aajconsult.com/templates/competitor-research-grid
- The five-step method this fits into: https://aajconsult.com/blog/competitive-analysis-for-startups

## Related skills

- `positioning-statement` and `value-proposition` - what to write once the map is read
- `messaging-framework` - pillars that avoid the crowded claims
- `comparison-pages` - the fair, sourced version of "them vs us"
- `claims-and-proof-check` - whether the open claim you want to make can be supported
- `review-mining` - what buyers care about, to weigh the open claims

## Credits

Written by AAJ (aajconsult.com). MIT licensed. The Agent Skills format and the marketing-skills
catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and
coverage; this skill is independently written.
