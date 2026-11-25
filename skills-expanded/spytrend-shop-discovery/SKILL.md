---
name: spytrend-shop-discovery
description: >-
  Discover store domains by traffic, qualified growth and advertising activity
  with SpyTrend MCP data, then inspect a bounded set of leading stores' ads and
  advertisers, from a database of 1B+ tracked Meta ads. Use when the user wants
  to find growing e-commerce or dropshipping stores, see which shops advertise
  most in a niche or country, run product research through stores that are
  taking off, or scout new stores that just started running heavy ads. Triggers:
  "shop spy", "fast-growing Shopify stores", "find winning products", "product
  research", "stores scaling their ads"; RU «найди быстрорастущие магазины»,
  «товарка: какие магазины взлетают», «спай магазинов и товаров»; ES «productos
  ganadores»; PT «produtos vencedores». Not for one known domain (use spytrend-
  website-review) and not for advertiser rankings without stores (use spytrend-
  advertiser-overview).
---

# SpyTrend shop discovery

Read `references/spytrend-contract.md` before making any data call.

## Inputs

- Require at least one of vertical or ISO-2 country.
- Platform is optional. Omit the parameter for "any platform"; never send a
  made-up wildcard value.
- Default: five admitted rows per cut, up to three store drilldowns, chat output,
  media off.

## Preflight

Call `get_usage`, state the three page limits, drilldown cap, media choice and
worst-case spend. Decide whether domain scope is exact host or root plus
subdomains and label it.

## Workflow

1. Call `search_shops` three times with the same filters and separate server
   sorts: traffic, qualified growth, and advertising activity. Never re-sort one
   bounded page to manufacture another cut.
   The growth cut returns only stores whose growth estimate the service has
   qualified, and that qualification depends on how fresh the traffic snapshot is.
   When the cut comes back empty, say that no store currently qualifies and give
   the snapshot month from `traffic_as_of` as the reason. Render the other two
   cuts and continue. Never substitute a re-sorted traffic page for it, and never
   report an empty qualified cut as "no growing stores".
2. Apply the public quality fields returned by the service. Reject infrastructure
   and redirect surfaces. Preserve server order among admitted rows.
3. If filtering leaves fewer rows than requested, page forward with the returned
   offset only until the target is filled or three pages have been inspected.
   Report fetched, admitted and rendered counts. Never promise implicit top-up.
4. Traffic is a monthly estimate for `traffic_as_of`. Growth is shown only when
   qualified. `ads_monthly` counts ads first discovered by SpyTrend; it is not a
   platform-launch series, and the open month is incomplete.
5. Select at most one unique admitted store from each cut for drilldown. For each,
   use `search_ads` with `landing_domain_exact=true`, the exact domain and
   concrete dates for a bounded count and representative ads. Use the response's
   total status and date axis.
6. Use the server's selected-window creative reuse ordering when available. Keep
   window reuse and lifetime reuse separate.
7. Call advertiser cards only for unique returned advertiser ids and
   `search_webmasters` by exact domain with a small limit for advertising-network
   attribution. A card without a `card_status` field is complete;
   `card_status=building` means its counters are unavailable, not zero.
8. With confirmation, fetch media only for the representative ads in the final
   drilldowns.

## Report

Show each cut independently, monthly estimate period, first-discovery label,
quality admission, fetched/admitted coverage, store drilldowns, unavailable
sections and spend. A domain surface is not automatically a brand or company.

Use `references/report-template.md` or the packaged renderer with
`references/report-template.html`; otherwise provide the complete result in
chat.
