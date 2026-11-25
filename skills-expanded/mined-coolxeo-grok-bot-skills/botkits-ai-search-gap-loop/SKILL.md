---
name: botkits-ai-search-gap-loop
description: >-
  use this when you want a site to show up more in Google and in AI answers
  (ChatGPT, Copilot, Gemini, Perplexity, AI Overviews) and need a repeatable
  loop: map buyer decisions to queries and prompts, measure both channels,
  diagnose each lost prompt, make one change, rerun, and log the result
---
# AI search gap loop

Use this skill to run a small, honest loop on one site. You start from the decisions your buyers make. You find the prompts and queries where the site loses. You find the cause. You make one change. You measure again.

This skill does not tell you how to write or mark up a page. For the fix itself, use [botkits-aeo-geo-site](../botkits-aeo-geo-site/SKILL.md). For a missing page, use [botkits-exact-match-intent-seo](../botkits-exact-match-intent-seo/SKILL.md) to pick the slug, title, and H1. For third-party sources that AI cites, use [botkits-ai-citation-sources](../botkits-ai-citation-sources/SKILL.md).

Helper files:

- [prompt-map-template.csv](prompt-map-template.csv): one row per tracked query or prompt.
- [loop-log-template.md](loop-log-template.md): one dated entry per cycle.

## Rules for numbers

- Record only numbers you read in this cycle from a real source: Search Console, an analytics tool, a live AI answer, a live search result.
- When a source is not available, write `missing`. Do not estimate. Do not fill a gap with a typical value.
- Write the date, the tool, and the exact prompt for every AI read. AI answers change between runs and between users. One read is a sample, not a rank.
- Keep Google numbers and AI numbers in separate columns. Do not add them together.

## Step 1. Map buyer decisions

1. List the 5 to 10 decisions a buyer makes before they choose a product like yours. Write each decision as the buyer would say it. Example shape: "Which [category] is safe for [situation]?"
2. For each decision, write:
   - 1 to 3 Google queries (short, keyword shaped).
   - 1 to 3 AI prompts (full sentences, the way a person asks an assistant).
3. Give each row the page on your site that should answer it. If no page exists, write `none`.
4. Put all rows in `prompt-map-template.csv`. This is the tracked set. Do not change the wording between cycles, or the results stop being comparable. Add new rows as new rows.

Do not start from a keyword tool. Start from the decision, then check the words against real search data if you have it.

## Step 2. Measure Google and AI separately

For each row:

- **Google**: from Search Console (or an equal source), read impressions, clicks, and average position for the query and for the target page. If you have no access, write `missing` in each column.
- **AI**: run the prompt in each AI tool you track. Record:
  - `site_cited`: yes / no. Your domain appears as a link or source.
  - `brand_named`: yes / no. Your brand or product is named in the answer text.
  - `other_owned_cited`: yes / no. Another property you own (channel, store page, profile) is cited.
  - `third_party_sources`: the domains the answer cites, in order.
- Mark a row **won** when your site or owned property is cited or named. Mark it **lost** when it is not.

When you have no access to a real AI tool, a web search result list with an AI summary is an acceptable proxy. Say so in the log. Do not call it an AI rank.

## Step 3. Diagnose each lost prompt

Give each lost row exactly one primary cause. Check them in this order, because each one blocks the next:

| Cause | Test | Next step |
| --- | --- | --- |
| **crawl-index** | The target page exists, but it is not indexed, is blocked for search crawlers in `robots.txt`, returns an error, has `noindex`, has a wrong canonical, or renders its main text only with JavaScript. | Fix access first. See the technical priority list below. |
| **missing** | No page on the site answers this decision. | Go to the missing-page branch. |
| **weak** | A page exists and is indexed, but it does not answer the prompt in plain words, is thin, is out of date, or answers a different question. | Improve that page with [botkits-aeo-geo-site](../botkits-aeo-geo-site/SKILL.md). |
| **third-party** | Your page is fine, but AI answers cite lists, reviews, forums, or directories instead. | Run [botkits-ai-citation-sources](../botkits-ai-citation-sources/SKILL.md) for this row. |

If the product does not truly answer the prompt (for example the prompt asks for a format or feature you do not have), mark the row `not-a-fit`, write why, and drop it from the next cycle. Do not bend a page to match a prompt it cannot honestly answer.

A row can show more than one cause. Write the primary cause, and add the others as notes.

Note the difference between search crawlers and training crawlers. Blocking a training crawler (for example `GPTBot` or `Google-Extended`) is a policy choice and does not remove a page from search. Blocking a search or answer crawler (for example `Googlebot`, `Bingbot`, `OAI-SearchBot`, `PerplexityBot`) can. Check each bot's own docs before you call it a cause.

### Missing page or weak page

- Improve an existing page before you make a new one. A new page is correct only when no page covers the decision and adding the answer to an existing page would make that page about two things.
- For a new page, use [botkits-exact-match-intent-seo](../botkits-exact-match-intent-seo/SKILL.md): one intent, slug, title, and H1 in the buyer's words. Then apply [botkits-aeo-geo-site](../botkits-aeo-geo-site/SKILL.md).
- Do not make many thin pages for close variants of one question.

### Technical SEO priority

Do not work from a site-wide warnings list. Rank each technical issue by its link to the demand pages in your prompt map:

1. Issues on a target page of a lost row (blocked, not indexed, broken, wrong canonical, slow to render main text).
2. Issues on pages that link to those target pages (navigation, hub pages, sitemap entries).
3. Issues that affect the whole site and also touch target pages (robots rules, redirects, HTTPS, server errors).
4. All other warnings. Leave them for later unless they are cheap and safe.

Write each issue with the row IDs it affects. An issue that affects no tracked row goes to the bottom.

## Step 4. Pick ONE change

1. From the lost rows, pick one change. Prefer the change that:
   - fixes a crawl-index cause (it blocks everything else), or
   - improves an existing page that serves the most lost rows.
2. Write the change as one sentence, with the page URL, the rows it targets, and what you expect to see if it works.
3. A human approves the change before it ships.
4. Make only that change in this cycle. If you change many things at once, you cannot tell which one worked.

## Step 5. Rerun and log

1. Wait long enough for the change to be crawled. Check the page in Search Console URL inspection if you have it. Write the wait time in the log.
2. Rerun every tracked row with the same wording and the same tools.
3. Add a dated entry to `loop-log-template.md`: what changed, before and after per row, Google and AI in separate columns, `missing` where you had no data.
4. If you track product signals (signups, activations, watch time), add them from the real source with the date range. If you cannot connect a signal to the change, say so.
5. Decide: keep and extend the change to similar pages, revert it, or try a different cause next cycle. Write the reason.

## Guardrails

- Same content for bots and people. No cloaking, no hidden text, no bot-only pages.
- No fake reviews, fake ratings, fake testimonials, or invented credentials.
- No astroturfing. Do not pose as a customer, parent, or neutral reviewer.
- No invented numbers. `missing` beats a guess.
- On sites for children or families: do not track or store personal data about children. Use only aggregate data from tools the site already uses with consent. Do not add new trackers for this loop.
- Any outbound text (posts, replies, emails, outreach) is a draft. A human reads and approves it before anyone sends it.
- A human approves each site change before it ships.
- Respect each AI tool's and search engine's terms. Do not automate queries in a way the tool forbids.
