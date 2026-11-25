---
name: log-web-competitor-traffic
description: "Competitor traffic: finding how to rank on your competitors' names. A log play (docs/useCases/web/competitorTraffic.md): Work out how a tool gets search and AI-search traffic from its competitors: what each competitor ranks for, who pays affiliate commission, what the people in the owner's DMs could link from, and what forums like BlackHatWorld say works this month. Then rank what to do first with a SubQ matrix and write it up. It reads and researches only. It publishes nothing and contacts nobody."
when_to_use: "Use when matt asks for this, in words like: \"find out all of our competitors\", \"what are we lacking\", \"go through the bhw mcp and see what they're saying\", \"compare this month to last month\", \"find who in my messages has a website for a backlink\", \"competitor pages that backlink to us\", \"make affiliate money through it\", \"run it through subq matrices\", \"do some deeper research\""
metadata:
  summary: "Competitor traffic: finding how to rank on your competitors' names"
---

# Competitor traffic: finding how to rank on your competitors' names

This is the log play `web/competitorTraffic`. Before anything else, call the log MCP tool `getGuide({ useCase: "web/competitorTraffic" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and matt's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Work out how a tool gets search and AI-search traffic from its competitors: what each competitor ranks for, who pays affiliate commission, what the people in the owner's DMs could link from, and what forums like BlackHatWorld say works this month. Then rank what to do first with a SubQ matrix and write it up. It reads and researches only. It publishes nothing and contacts nobody.

How the owner asks for it: "find out all of our competitors", "what are we lacking", "go through the bhw mcp and see what they're saying", "compare this month to last month", "find who in my messages has a website for a backlink", "competitor pages that backlink to us", "make affiliate money through it", "run it through subq matrices", "do some deeper research"

## Run it from a fresh context

Say: **"go on docs/useCases/web/competitorTraffic.md for <tool>"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Read what's already been found before searching again: earlier competitor, keyword and positioning research, and the open plans | `RESEARCH/`, `PLANS/` | the known competitors, their keywords and the gaps are listed with their files |
| 2 | What each competitor ranks for on Google, and the keywords with a competitor's name in them ("<competitor> alternatives", "<competitor> pricing", "x vs y") | [treg](https://treg.to/?ref=matthewdonse-aebsh)'s ranked-keywords endpoint through `tregGet` then `tregCall` (priced: say the price and run it only when the owner asked) | a TSV of competitor-name keywords with volume, position and the site ranking |
| 3 | Each competitor's affiliate programme, from its own page | `tregCall` { id: "tinyfish.web.search" } (free), one search per competitor, run by a subagent | a table: programme, terms in its own words, source URL; disagreeing sources shown side by side |
| 4 | What the forum says works now, this month against the two before: comparison and alternatives pages, brand mentions, listicles, directories, open source, internal linking | the bhw MCP (`bhwSearch` { order: "date", titlesOnly }, `bhwThread`, `bhwForum`) | each point quoted with the thread, its date and its link; anything a research report claims that the forum doesn't back is marked unproven |
| 5 | Who in the owner's DMs has a website, and where a link could go | `twitterDms` { account, limit: "200" } for the people, the niche map for their sites, `tregCall` { id: "tinyfish.web.fetch" } (free) for each site's blog, resources, tools or partners page | a table: person, site, what it is, where a link could go, what they're doing now |
| 6 | Deeper research, only when the owner asks for it, in his scope only | the Parallel deep research skill (priced) | the report saved in `RESEARCH/` |
| 7 | Rank the options with a SubQ matrix: only the options the owner named, criteria from his goal, and every file above as evidence | a `runMatrix.mjs` like `docs/decisions/mcpReload`, with `SUBQ_API_KEY` | `subqResults.json` with a choice per criterion, do first, do last and a score per option |
| 8 | Write it up: what's missing next to the competitors, what the forum backs, the order from SubQ with the forum's conditions, and which parts the tool can run itself | `RESEARCH/<NAME>.md`, `PLANS/<NAME>.md` | the owner has the order, every claim with its source, and the open decisions (which programmes to join, where pages live) |

## What the runs taught

- **The forum over the SEO tools' own studies.** Numbers from a tool vendor's study (citation shares, correlations) that the forum doesn't discuss are marked unproven, not passed on as fact.
- **Ranking on a competitor's name works only with real facts on each page.** A template with the name swapped converts badly and can be taken down. Each comparison page answers a different question with tested facts.
- **What gets named by AI is Reddit threads and comparison posts people read**, not big press. A listicle placement is worth it only if that page already gets traffic.
- **Free first.** TinyFish search and fetch through treg cost nothing. Ranked keywords, profile lookups and deep research cost money: say the price and ask before running anything the owner didn't ask to pay for (rule 41).
- **"Open source" on a competitor's page isn't always the whole thing.** Say exactly what each one is, as the owner knows it.
- **On Windows the Parallel CLI can fail writing the report** (a charmap error). Read the finished run from Parallel's API instead and save it as UTF-8.
