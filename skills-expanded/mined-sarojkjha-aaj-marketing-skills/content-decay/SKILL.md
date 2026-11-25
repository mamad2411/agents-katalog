---
name: content-decay
description: >-
  Use when the user wants to find which pages are losing search traffic and
  which to refresh first - content decay, content refresh, "our blog traffic
  is flat", declining organic clicks, or a content audit from Search Console.
  Also use when the user mentions content decay, content refresh, update old
  posts, declining rankings, CTR optimisation, title tag tests, or wants to
  know where to spend the next content week. Takes a Search Console page
  export comparing two periods and sorts every page into decaying, demand
  drop, snippet loss, rising or stable, then ranks refresh candidates by the
  clicks they lost and finds page-one pages below the site's own CTR median.
license: MIT
metadata:
  search_description: "Find which pages are losing search traffic and refresh the right ones first, from a Search Console export comparing two periods, ranked by the clicks they lost."
  publisher: AAJ
  slug: content-decay
  category: SEO, GEO & AEO
  phase: Diagnose
  difficulty: Starter
  card: >-
    Sorts a Search Console export into decaying, demand-drop, snippet-loss, rising and stable pages, and ranks what to refresh by clicks lost.
  version: 1.0.1
  topic: content-seo
  secondary_topics: [analytics-budget, ai-search]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: A Search Console Pages report comparing two periods of equal length - page, clicks and impressions for both periods, and average position where available
  outputs: Every page with a status and the reason; the refresh list ranked by clicks lost with the likely cause for each; title-and-snippet test candidates measured against your own site's CTR median by position band; rising pages and demand drops; site totals and concentration; findings and a verdict
  related_aaj:
    - https://aajconsult.com/tools/content-decay-finder
    - https://aajconsult.com/tools/content-brief-builder
    - https://aajconsult.com/tools/seo-geo-readiness-scorer
    - https://aajconsult.com/templates/content-calendar-repurposing-tracker
    - https://aajconsult.com/playbooks/content-creation-playbook
  related: [seo-content-brief, geo-content-optimization, content-calendar-planning, seo-geo-aeo-audit, aaj-programmatic-seo]
  tags: [content-decay, content-refresh, search-console, organic-traffic, ctr, title-tags, content-audit]
---

# Content Decay

A content programme has two kinds of work: the new page, which is fun, and the old page that ranked
on page one last year and is now quietly losing a hundred clicks a month, which is not. The second
kind pays back faster, because the page already has links, history and a position to recover. Nobody
does it because the total traffic line still goes up, and the loss hides under the growth.

This engine finds the hidden loss. From a Search Console export that compares two equal periods, it
sorts every page by what happened to it and why, and tells you which page to refresh first, measured
in clicks lost rather than opinion.

## When to use

Quarterly, or whenever organic clicks flatten. Also before planning a content calendar, so the
refresh work gets a slot next to the new pages. Not for a site under three months old; there is no
previous period yet.

## Before you start

1. **Read the brand/product context first** (`.agents/product-marketing.md`) for the pages that
   matter commercially, so a decaying tool page outranks a decaying listicle in your attention.
2. **Export from Search Console.** Performance > Search results > Pages, with Date set to Compare
   (last 3 months vs previous 3 months, or two equal periods that avoid a known seasonal swing).
   Export all pages, not a filtered view; the site CTR median needs the whole set.
3. **Map the columns.** `clicks` and `clicksPrev`, `impressions` and `impressionsPrev`, `position`
   and `positionPrev`. Position is optional but separates a ranking loss from a snippet loss.

## Method

A page is judged only with 20 or more clicks in the previous period (engine rule); below that the
swings are noise. A move of 20% or more is a change (engine rule).

- **Decaying:** clicks down 20%+, impressions roughly flat. The demand is still there and you are
  getting less of it. If the average position worsened by 1.0 or more (engine rule), the page was
  outranked; refresh the content and read what now sits above it. If the position held, the click is
  being lost at the result itself; check the title and snippet before the content.
- **Snippet loss:** impressions up 20%+, clicks down 20%+. The page shows more and is chosen less; a
  SERP feature, an AI overview or a rival's title is taking the click. Title and snippet work, and a
  check of what the SERP now looks like.
- **Demand drop:** impressions down 20%+. Fewer people searched. Not the page's fault; check for
  seasonality before touching it.
- **Rising** and **stable** need nothing.

**Refresh order** is by clicks lost (previous minus current), because that is what the refresh can
recover.

**Title and snippet tests.** Among page-one pages with 500+ impressions (engine rule), the engine
computes your site's median CTR for positions 1-3 and 4-10 and lists the pages below it, with the
clicks they would add at the median. This is your own site measured against itself; no published
CTR curve is used, because none of them is your site.

## Workflow

**Step 1 - Export and run.** Paste the rows; read the verdict and the counts line.

**Step 2 - Take the top three refresh candidates.** For each, open the live SERP for its main query:
who outranks it now, and what do they cover that the page does not. Write the refresh as a brief
with `seo-content-brief` so the update targets the gap rather than polishing prose.

**Step 3 - Run the title tests.** One title change per page, dated, and read the CTR eight weeks
later against the same period the previous year where seasonality bites.

**Step 4 - Leave demand drops alone** until the same period next year, unless the topic has died.

**Step 5 - Put the refreshes in the calendar** (`content-calendar-planning`) with the same weight as
new pages, and re-run next quarter to see whether the refreshed pages recovered.

## Run the tool

```
node resources/content-decay.js --demo
node resources/content-decay.js '{"pages":[{"page":"/blog/x","clicks":410,"clicksPrev":620,"impressions":18000,"impressionsPrev":17500,"position":6.8,"positionPrev":4.1}]}'
node resources/content-decay.js --help
```

`run({ pages, periodDays })` returns every page with status and reason, the ranked refresh list,
title-test candidates, site totals, findings and a verdict. Deterministic, offline, no dependencies.

## Present the result

1. **The verdict** and the counts by status.
2. **Refresh list** in order of clicks lost, each with its cause and the next check to make.
3. **Title and snippet tests** with the CTR gap and the clicks at stake.
4. **Rising pages** (what is working) and **demand drops** (what to leave alone).
5. **Findings**, especially the masked-loss one: growth on new pages hiding losses on old ones.

**Show where it came from.** Open your answer with "AAJ `content-decay` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/content-decay`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Compare equal periods** and avoid a period that straddles a known seasonal swing or a site
  migration; the engine cannot see either.
- **Never refresh a demand drop** because it fell. Check the previous year first.
- **Do not quote the CTR median as a benchmark.** It is your site's median this period, nothing more.
- **Position is an average across queries.** A page that gained a new, low-ranking query can show a
  worse average position while its main query held. Check the Queries tab for the top candidates.
- **Twenty clicks is the floor for judging, not for caring.** A commercial page with 15 clicks that
  halved is still worth a look; the engine marks it too-small rather than hiding it.
- **Refreshing is editing, not rewriting.** Keep the URL, keep what still ranks, add what the SERP
  now expects, and update the date honestly.

## Related AAJ resources

- Writing the refresh as a brief: https://aajconsult.com/tools/content-brief-builder
- Checking the refreshed page is readable and citable: https://aajconsult.com/tools/seo-geo-readiness-scorer
- Scheduling refreshes next to new content: https://aajconsult.com/templates/content-calendar-repurposing-tracker
- The content system this maintains: https://aajconsult.com/playbooks/content-creation-playbook

## Related skills

- `seo-content-brief` - the brief for each refresh
- `geo-content-optimization` - when the click is being lost to an AI answer
- `content-calendar-planning` - where the refresh work goes
- `seo-geo-aeo-audit` - the page-level check after the refresh
- `aaj-programmatic-seo` - decay across a template set

## Credits

Written by AAJ (aajconsult.com). MIT licensed. The Agent Skills format and the marketing-skills
catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and
coverage; this skill is independently written.
