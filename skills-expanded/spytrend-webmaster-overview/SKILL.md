---
name: spytrend-webmaster-overview
description: >-
  Profile the advertising network behind a domain or a group of ads with
  SpyTrend MCP data: connected domains, advertiser pages, identifiers tying ads
  to one operator, target countries and the creatives that operation reuses
  most, from a database of 1B+ tracked Meta ads. Use when the user wants to know
  who is behind a set of ads, see everything one operator or competitor runs
  across pages and domains, or check whether identical ads on different pages
  belong to one player. Triggers: "ads spy across pages", "who is behind these
  ads", "everything this operator runs", "the whole operation", "network behind
  a landing domain"; RU «кто стоит за рекламой этого домена», «какие ещё домены
  у этого рекламодателя», «вся связка страниц оператора». Not for ranking
  advertiser pages in a market (use spytrend-advertiser-overview) and not for a
  website's traffic review (use spytrend-website-review).
---

# SpyTrend advertising network overview

Read `references/spytrend-contract.md` before making any data call. The skill
name preserves the MCP entity name for routing; user-facing output says
"advertising network" or "network".

## Resolve one network

1. Call `get_usage` and disclose the planned depth and media choice.
2. If the input is not already a canonical id, call `search_webmasters` by exact
   domain or query with a small limit. Show ambiguous candidates and ask the user
   to choose rather than merging them.
3. Read market size from `pagination.total` only with its status. Never read a
   top-level total and never promise a complete list from a capped response.
4. Call `get_webmaster` with the chosen canonical id. If
   `analytics_pending=true`, treat counters as pending, not zero.

## Bounded profile

1. Render the returned domains, advertiser pages, the identifiers that tie ads
   to one operator, and countries with their returned counts, caps and statuses. A missing inventory is unavailable,
   not proof that no identifier exists.
2. Present attribution edges as evidence of observed combinations. A small edge
   does not prove common ownership, and inherited identifiers do not describe
   current operation by themselves.
3. Call `search_creatives` with `webmaster_id`, optional category and
   `sort_by=total_ads` for the exact global network slice. Do not add `country`:
   the current read path cannot preserve the exact network slice together with
   that filter. Use returned geo fields as context, not as a country ranking.
4. Call `search_ads` with `webmaster_id`, the selected `categories` and
   `countries`, `country_match=any`, `status_today=active`, `sort_by=date`,
   `dedupe=true` and a small explicit limit for fresh examples. This means the
   selected country is present in the ad's known geographies; it does not mean
   that country is dominant. Label dates according to the returned date axis.
5. If the card contains a network-specific creative slice, use its slice order
   for "most reused by this network". Keep market-wide family size as separate
   context; do not use it to reorder the network slice.
6. With confirmation, retrieve media for only the chosen rows. A representative
   ad is a cheaper placement example; a creative fetch represents the material
   family. State which path was used.

## Report

Include resolution evidence, current/pending status, returned identifier
coverage, country activity, creative rankings, fresh examples, period labels and
spend. Say "processed N of M" whenever a bounded cap is used.

Use `references/report-template.md` or the packaged renderer with
`references/report-template.html`; otherwise return the same report in chat.
