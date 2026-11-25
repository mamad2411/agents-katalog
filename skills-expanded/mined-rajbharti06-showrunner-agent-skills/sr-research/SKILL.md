---
name: sr-research
description: Maps a niche without scraping anything. Studies five to ten accounts the creator names, lists the topics, formats, cadence and gaps, and checks current platform facts with their source and age. Use when someone asks "what are others in my niche doing", "who should I study", "is this niche crowded", "what topics are missing" or wants competitor analysis before planning content. Works from public pages, the person's own exports and any connected research tool, and labels every claim with where it came from.
license: MIT
compatibility: Any agent that loads Agent Skills. Web search or a connected analytics tool helps but is not required; the person can paste what they see.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Research: map the niche honestly

Good research here means seeing what already works, where the gaps are, and what you do not know. It does not mean collecting every number you can find.

## Ask first

- Which five to ten accounts do you already watch in this niche? Include two or three that are about your size, not only the giants.
- Which one do you wish you had made?
- Which topics do you think are overdone? Which are missing?

If they cannot name any, search the public web for the niche on the hub platform and propose a shortlist for them to approve.

## Where the information comes from

In order of preference:

1. **What the person pastes or exports.** Their own analytics, a competitor's public numbers they copied by hand.
2. **A connected research tool.** If a keyword or competitor tool is connected (for example, vidIQ's MCP connector, which the vendor says works with Claude, ChatGPT and Cursor; Showrunner is not affiliated with vidIQ), use it and quote the numbers as that tool's.
3. **Public web pages** through your search or fetch tools.
4. **Nothing else.** Do not scrape logged-in pages, do not guess numbers.

When a site cannot be read, say so and ask the person to paste the text.

## Build the niche map

For each account, one row:

| Account | Promise in a line | Main formats | Cadence | Best topics | What they never cover |
|---|---|---|---|---|---|

Then look across the rows for:

- **Topics that recur.** Demand is probably real.
- **Formats that recur.** The audience has learned to expect them.
- **Gaps.** Topics or angles nobody covers, or covers badly. A gap is only useful if the creator has proof for it.
- **Size-matched winners.** Pieces from small accounts that did well. Those are the models, not the giants.

Hand the list of standout posts to `sr-outliers` for ranking.

## Check the platform facts that matter

Call `facts_search` for the hub platform's limits, formats and policy. Quote the status (official, reported, inferred, study) and the age. If a fact is more than 90 days old, say so (`facts_stale`).

## Write it down

One page: the table, three recurring topics, two gaps worth testing, one thing not to copy, and what you could not find out. Keep sources next to claims.

## Gate

`approve`. The person picks which gaps to test first.

## Do not

- Quote subscriber, follower or view counts without saying where they came from and when.
- Say a niche is "saturated" or "untouched" without evidence. Say what you saw.
- Copy another creator's structure word for word. Study the shape, not the words.
