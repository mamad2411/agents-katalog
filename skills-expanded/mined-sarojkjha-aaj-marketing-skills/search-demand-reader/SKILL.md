---
name: search-demand-reader
description: >-
  Use when the user wants to know what people search for in their category
  and where the demand is going unmet, using their own Search Console data
  rather than an estimated keyword tool - reading a Queries export by intent,
  grouping it into topics, finding the topics they already appear for on page
  two or worse, queries split across their own pages, the branded share of
  their traffic, and rival-brand searches they show up in. Also use when the
  user mentions keyword research, search demand, Search Console queries,
  keyword gaps, cannibalisation, branded vs non-branded, or "what should we
  write next". Never estimates a search volume it cannot see.
license: MIT
metadata:
  search_description: "Read your Search Console queries by intent and topic: page-two topics, queries split across your pages, branded share and rival-brand searches you appear in."
  publisher: AAJ
  slug: search-demand-reader
  category: SEO, GEO & AEO
  phase: Diagnose
  difficulty: Starter
  card: >-
    Reads a Search Console Queries export by intent and topic, and names the demand you already appear for but do not yet win.
  version: 1.0.1
  topic: content-seo
  secondary_topics: [audience-research, gtm-growth-planning, ai-search]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: A Search Console Queries export (query, clicks, impressions, average position, and the page where available), your brand words, and optionally rival brand words
  outputs: Impressions and clicks by intent; topics grouped by their most common word with position and pages; the gaps you already appear for past position 10; queries split across two of your pages; the branded share of clicks; rival-brand searches you appear in; findings and a verdict naming the first topic to build or refresh
  related_aaj:
    - https://aajconsult.com/tools/search-console-query-reader
    - https://aajconsult.com/tools/content-brief-builder
    - https://aajconsult.com/tools/bottom-up-market-sizer
    - https://aajconsult.com/playbooks/market-research-playbook
    - https://aajconsult.com/playbooks/content-creation-playbook
  related: [content-decay, seo-content-brief, content-calendar-planning, market-sizing, aaj-programmatic-seo, review-mining]
  tags: [search-demand, keyword-research, search-console, intent, topics, cannibalisation, content-planning]
---

# Search Demand Reader

Keyword tools estimate. Search Console counts. The counts are limited to searches where one of
your pages appeared, and that limit is the point: every query in the export is one you can already
win more of, because Google has already shown you for it. This engine reads that export the way a
content lead would with a free afternoon: which intents your traffic serves, which topics carry the
demand, where you rank past page one for something people search a lot, and where two of your own
pages are fighting over one query.

## When to use

Before planning content for a quarter, when deciding between a new page and a refresh, when the
founder asks "what do people search for", and when branded traffic seems to be all there is.

Not for a site with no Search Console history, and not for sizing a market: a query you never
appeared for is not in this data and the engine will not guess it. For the demand you cannot see,
use interviews, `review-mining`, and the sizing method in `market-sizing`.

## Before you start

1. **Read the brand/product context first** (`.agents/product-marketing.md`) for the brand words,
   rival names and the commercial topics that matter.
2. **Export Queries for at least three months.** Performance > Search results > Queries, all rows.
   Add the Page dimension if the interface lets you export query-and-page pairs; otherwise export
   Queries and, separately, filter by page for the few topics you care about.
3. **List your brand words** (name, misspellings, product names) and the rival brands buyers compare
   you with.

## Method

**Intent** is read from modifier words, in order: a brand word makes it branded; a rival's name makes
it rival-brand; "demo", "trial", "buy", "pricing" and the like make it transactional; "best", "vs",
"alternative", "software", "tool" make it commercial; "how", "what", "guide", "template" make it
informational; anything else is unqualified, which means the words did not say, not that the engine
guessed.

**Topics** are groups of queries sharing their most common content word, after light stemming.
This is coarse on purpose: a word-level grouping you can check beats a clustering you cannot. Read
the top queries under each topic before acting on it.

**Gaps you already appear for.** A topic with 200+ impressions (engine rule) whose
impression-weighted average position is worse than 10 (engine rule). Google shows you for it and
nobody clicks because you are on page two. These are the cheapest content wins on the list, because
the search intent is proven and the page often exists.

**Cannibalisation.** A query where two or more of your pages each take 20% or more of its
impressions (engine rule). Google is choosing between your pages, and the ranking suffers for it.

**Branded share of clicks** says how much of your organic traffic is people who already knew you.
There is no right number; a rising non-branded share is the sign the content programme is working.

**Rival-brand searches you appear in** are comparison intent you have already earned a place in;
`comparison-pages` is the next step.

## Workflow

**Step 1 - Export, run, read the verdict.**

**Step 2 - Take the largest gap.** Look at its top queries. If one page already holds them, refresh
it with `seo-content-brief` aimed at that query set. If no page is built for the topic, brief a new
one. Do not build a page per query.

**Step 3 - Resolve cannibalisation** by choosing the page that should win and pointing the other at
it (a link, a consolidation, or a canonical), then watch the query's position next quarter.

**Step 4 - Put the rival-brand queries into `comparison-pages`.**

**Step 5 - Put the rest in the calendar** (`content-calendar-planning`), gaps before new ideas.

**Step 6 - Re-run quarterly** and track the non-branded share of clicks and the number of gaps.

## Run the tool

```
node resources/search-demand.js --demo
node resources/search-demand.js '{"brand":["acme"],"queries":[{"query":"crm for dentists","clicks":3,"impressions":400,"position":12.1,"page":"/blog/dental-crm"}]}'
node resources/search-demand.js --help
```

`run({ brand, rivals, queries })` returns totals, intents, topics, gaps, cannibalisation,
rival-brand queries, findings and a verdict. Deterministic, offline, no dependencies.

## Present the result

1. **The verdict** and the branded share of clicks.
2. **Intent table**: queries, impressions and clicks by intent.
3. **Gaps**, each with its top queries and the page that currently appears.
4. **Cannibalised queries** with the page split.
5. **Rival-brand searches** you appear in.
6. **Topics table** (top 15) for the broader picture.
7. **Findings**, especially missing pages or positions, which limit what can be read.

**Show where it came from.** Open your answer with "AAJ `search-demand-reader` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/search-demand-reader`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never present an impression count as search volume.** It is the number of times your page was
  shown, which is at most the volume and usually far less.
- **Never fill the gap you cannot see.** If a topic is absent from the export, say that the data
  cannot speak to it rather than estimate.
- **Unqualified is a category, not a guess.** Read those queries by hand before assigning intent.
- **One page per topic, not per query.** The gap list groups queries for a reason.
- **Branded share has no benchmark.** Compare it with your own last quarter.
- **Three months minimum.** A month of queries is mostly noise for a small site.

## Related AAJ resources

- Briefing the page that closes a gap: https://aajconsult.com/tools/content-brief-builder
- Sizing the market from accounts rather than searches: https://aajconsult.com/tools/bottom-up-market-sizer
- Where search data fits among other sources: https://aajconsult.com/playbooks/market-research-playbook
- The content system this feeds: https://aajconsult.com/playbooks/content-creation-playbook

## Related skills

- `content-decay` - the same export, read page by page over time
- `seo-content-brief` - the brief for the gap page
- `content-calendar-planning` - scheduling gaps and refreshes
- `market-sizing` - demand you cannot see in search data
- `aaj-programmatic-seo` - when a gap is a template set, not a page
- `review-mining` - the language of the demand, from reviews

## Credits

Written by AAJ (aajconsult.com). MIT licensed. The Agent Skills format and the marketing-skills
catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and
coverage; this skill is independently written.
