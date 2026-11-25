---
name: spytrend-keyword-search
description: >-
  Search and analyze ads matching a keyword or phrase with SpyTrend MCP data,
  with country breakdowns and exact creative-reuse ranking inside the selection,
  from a database of 1B+ tracked Meta ads. Works like an ad library search by
  text when the user does not know who runs the ads. Use when the user wants to
  find ads mentioning a product, brand, slogan or offer, pull ad examples for a
  topic, or measure how many ads use a phrase by market. Triggers: "facebook ads
  spy", "ad spy", "find ads with the word X", "search the ad library for a
  phrase", "which ads use this slogan"; RU «найди объявления со словом…», «поиск
  по библиотеке рекламы по ключу», «спай рекламы по ключу»; ES «buscar anuncios
  por palabra clave»; PT «biblioteca de anúncios»; JA «広告ライブラリで検索». Not for a
  whole vertical (use spytrend-vertical-intel), a known advertiser (use
  spytrend-advertiser-overview) or a known domain (use spytrend-website-review).
---

# SpyTrend keyword advertising search

Read `references/spytrend-contract.md` before making any data call.

## Scope and preflight

- Required: keyword or short phrase.
- Optional: country, vertical and inclusive concrete dates.
- Ask whether the search is worldwide or country-specific when that choice is
  absent and materially affects the answer.
- Call `get_usage`, present maximum row depth and keep media off by default.

## Workflow

1. Call `search_ads` with the exact query, selected filters and an explicit small
   limit. Keep response order and date axis.
2. When a market breakdown is requested, bound the selection first: a free-text
   query needs concrete `date_from`/`date_to` (a week or two is enough) on top of
   the country. An open-ended text selection does not settle — its sections stay
   `ready=false` no matter how many times the call is re-issued, and the advertised
   `retry_after_seconds` will not change that. Say that the window was added and
   why. Then call `get_ads_analytics` with the same
   query/country/category/date filters and an explicit
   `max_items_per_section`. If that tool is disabled or the account cannot use
   it, continue with the bounded ad rows and report the returned access state.
3. For each analytics section, read its own `status`, `ready`,
   `available_count`, `returned_count` and `truncated`. A section's
   `available_count` is bounded section inventory, not market breadth. Market
   breadth comes only from `total` with `total_status`.
4. When analytics are pending, render ready sections and their coverage. Do not
   paid-poll after a response has delivered rows.
5. Use one-row counter calls only for explicitly requested exact slices and name
   the total status. Missing or unavailable is not zero.
6. For creative reuse inside the selected filters, use the server's selection
   reuse ordering and the response field that counts ads in that selection. Keep
   lifetime reuse as a separate labeled value when returned.
7. A representative ad is one example placement from a creative group; its copy
   and destination do not describe every ad in that group.
8. With media confirmation, call `get_media` for only the representative ads the
   user selected. Do not fetch broad creative media automatically.

## Report

Show exact filters, axis, total status, returned rows, truncation, advertisers,
networks, destinations and top reused creative groups in the selection. State
which analytics sections were returned and which were unavailable. Do not call a
bounded item count a market total.

Use `references/report-template.md` or the packaged renderer with
`references/report-template.html`; otherwise provide the full report in chat.
