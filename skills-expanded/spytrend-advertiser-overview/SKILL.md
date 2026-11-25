---
name: spytrend-advertiser-overview
description: >-
  Rank the top advertiser pages in a chosen vertical and country and profile
  each in depth with SpyTrend MCP data: current winning ads, freshly launched
  ads, creatives and destination pages, from a database of 1B+ tracked Meta ads.
  Use when the user wants to see who the biggest advertisers in a market are and
  what they run, profile market leaders' current ads, check which pages have the
  most active ads, or catch fresh launches from top pages. Triggers: "spy on
  competitor ads", "top advertisers in a niche or country", "biggest
  advertisers", "longest-running ads", "whose ads dominate this geo"; RU «кто
  крупнейшие рекламодатели и что они крутят», «топ рекламных страниц рынка»,
  «спай конкурента»; ES «espiar anuncios de la competencia»; PT «anúncios dos
  concorrentes»; JA «競合の広告». Not for a whole-vertical map (use spytrend-
  vertical-intel), one website (use spytrend-website-review) or a text search
  (use spytrend-keyword-search).
---

# SpyTrend advertiser overview

Read `references/spytrend-contract.md` before making any data call.

## Inputs

- Required: vertical and ISO-2 country.
- Default profile count: five; allow three or ten when the user chooses depth.
- Default output: chat; default media: off.

## Preflight

Call `get_usage`, state the profile count and maximum spend, and get media
confirmation separately. If the account does not own the requested vertical,
show the returned access state instead of calling an unfiltered market and
pretending it answers the original question.

## Workflow

1. Call `get_trends` with `dimension=advertisers`, the selected AI category,
   country, `min_geo_share=0.3`, explicit limit and the current-volume sort.
   The geo-share gate limits the ranking to pages for which the selected country
   is a dominant geography; a bare country filter is only a present-in match and
   ranks global pages with a marginal local slice first. State the threshold
   beside the leaderboard. Preserve server order.
2. When an exact-filter state is returned, use `filter_match.exact_active` only
   if `filter_match.exact_available` is true. Otherwise label the page as a
   server-ranked candidate and do not claim exact filtered activity.
3. For recently discovered advertiser activity, make a separate `get_trends`
   call using `sort_by=launched_14d`. This field currently counts ads first
   discovered by SpyTrend in that window; label it exactly that way, never as
   Facebook launches. Never derive this table by re-sorting the bounded current
   leaderboard.
4. For each admitted advertiser, call `search_creatives` with its page id and
   category, without country, ordered by current activity with a small explicit
   limit. Call the result an exact advertiser slice only when the response's
   slice/sort status says so; otherwise label it a bounded candidate sample.
   Country-specific examples come from the ad query below, not by weakening the
   advertiser creative slice.
5. Call `search_ads` with `page_id` set to the advertiser page id, the selected
   `categories` and `countries`, `status_today=active`, `sort_by=date`,
   `dedupe=true` and a small explicit limit. A first-discovered date stays
   labeled as first discovered unless the response supplies the platform launch
   date. Pass the page id in `page_id`, never in `advertiser_id`: that parameter
   takes the internal advertiser UUID returned by `search_advertisers`, and a page
   id placed there is ignored without an error — the call then answers for the
   whole unfiltered market. If you hold the UUID instead, pass it in
   `advertiser_id`. Before reporting, verify the binding: every returned row must
   carry the identifier you filtered on.
6. Use advertiser card data for exact page counters and destination coverage
   when the card carries no `card_status` field: a complete card does not emit
   it. When `card_status` is `building`, the card is a placeholder and its
   counters are unavailable, not zero; say so instead of reporting numbers.
   Category counters describe the labeled subset and must be presented with
   coverage.
7. With media confirmed, fetch only the final selected ids. Prefer the lower-cost
   representative-ad media path when one placement example is sufficient, and
   state that choice.

## Report

Show two separately sourced leaderboards (current activity and recently first
discovered ads), profiled-versus-returned coverage,
current creative winners, fresh ads, destinations, exact/unavailable states and
spend. Do not present a bounded candidate pool as the complete market.

Use `references/report-template.md` or the packaged renderer with
`references/report-template.html`. Chat must contain the full result when file
creation is unavailable.
