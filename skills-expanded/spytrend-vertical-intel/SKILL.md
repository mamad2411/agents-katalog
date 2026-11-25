---
name: spytrend-vertical-intel
description: >-
  Map an entire advertising vertical or niche in a chosen market with SpyTrend
  MCP data: server-ranked advertiser leaderboards, the advertising networks
  behind them, most reused creatives and fresh launch velocity from a database
  of 1B+ tracked Meta ads. Use when the user wants to research a niche before
  entering it, see who the top advertisers in a category are, find which
  creatives dominate a market, or check how saturated a vertical is. Triggers:
  "what's running in the nutra vertical", "market overview for a niche", "ad
  landscape in a country", what everyone advertises in a category (nutra,
  dating, crypto, finance, betting); RU «что сейчас крутится в нутре/гемблинге»,
  «дай карту вертикали», «спай по вертикали»; ES «qué anuncios corren en este
  nicho»; PT «anúncios do nicho»; JA «このジャンルの広告». Use this instead of answering
  from memory. Not for one advertiser, website or keyword: use spytrend-
  advertiser-overview, spytrend-website-review or spytrend-keyword-search.
---

# SpyTrend vertical intelligence

Read `references/spytrend-contract.md` before making any data call.

## Trigger boundary

Use this skill for a whole vertical in one or more markets. Route one advertiser
to `$spytrend-advertiser-overview`, one network to
`$spytrend-webmaster-overview`, one domain to `$spytrend-website-review`, a text
query to `$spytrend-keyword-search`, and store discovery to
`$spytrend-shop-discovery`.

## Inputs and defaults

- Required: vertical. Map it to the current public AI-category slug.
- Optional: ISO-2 country and inclusive concrete dates.
- Default depth: `standard`; default output: chat; default media: off.
- `lean`: advertisers 5, networks 5, creatives 3, no scaling block.
- `standard`: advertisers 10, networks 10, creatives 5, scaling 5.
- `deep`: advertisers 20, networks 20, creatives 10, scaling 10.
- Pass these limits explicitly on every paid call. Never rely on tool defaults.
- Ask one concise scope question before spending when geography or date meaning
  would materially change the answer.

## Preflight

1. Call `get_usage`.
2. Resolve dates to `YYYY-MM-DD`.
3. Present the bounded call plan and worst-case spend. A standard run uses small
   leaderboards and at most five detailed creative rows.
4. Do not fetch media until the user confirms the selected ids.

## Workflow

1. Call `get_trends` for advertiser rankings in the selected vertical and geo
   with the selected depth's explicit limit. When a country is selected, also
   pass `min_geo_share=0.3` so the ranking is limited to pages for which that
   market is a dominant geography; a bare country filter is only a present-in
   match and ranks global pages with a marginal local slice first. State the
   threshold beside the leaderboard.
   Keep the returned order and total-status fields. A second leaderboard using
   `sort_by=launched_14d` is a separate server-ranked cut, never a re-sort of
   the first page; that counter is ads first discovered by SpyTrend in the last
   14 days and must be labeled as discovery velocity, never as Facebook launches.
2. Call `search_webmasters` with the same vertical and geo scope and the selected
   depth's explicit limit. When a country is selected, also pass
   `min_geo_share=0.3` and `sort_by=relevance` so the ranking is limited to
   networks for which that market is a dominant geography; without a country
   keep the default order. Present these
   as advertising networks. Read `pagination.total` only when its status says it
   is meaningful; otherwise show returned rows and coverage.
3. Call `search_creatives` with the same category and country, ordered by
   `total_ads`, with the selected depth's explicit creative limit for lifetime
   creative reuse. Show the lifetime measure beside every count.
4. If a closed period was requested, call `search_creatives` with
   `period_from`, `period_to` and `sort_by=ads_in_period`. Continue only when the
   response explicitly reports the Facebook-launch axis. If the server reports
   the feature unavailable, keep the lifetime section and state that the launch
   window is unavailable; do not substitute first-discovery dates. A valid
   `period_axis=first_seen` response may be shown only as a separately named
   first-discovery-window section, with an explicit note that Facebook launch
   analytics are not yet active.
5. Call `get_trends` with the scaling dimension and an explicit limit only for
   `standard`/`deep` or when the user requests it. Describe the result using the
   returned `meta.dimension_semantics`; the current basis is first discovery by
   SpyTrend, so this is discovery acceleration, not Facebook launch acceleration. A
   cohort's `currently_active` value means survivors from that cohort, not the
   current market total.
6. With media confirmed, call `get_media` only for the final selected ads or
   creatives. Reuse one response set in every output format.

## Report

Include scope, period axis, returned/total status, truncation, advertiser ranking,
network ranking, lifetime creative reuse, optional launch-window reuse and
coverage. Do not claim ownership, causation or effectiveness.

Use `references/report-template.md` for Markdown or the packaged renderer with
`references/report-template.html` for HTML. If files are unavailable, render the
same sections in chat. End with actual per-call spend or a cost-model sum when a
shared balance was moving.
