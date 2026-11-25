---
name: spytrend-website-review
description: >-
  Review one website or store domain with SpyTrend MCP data: monthly traffic
  estimate, advertising footprint over time, which advertiser pages run ads to
  it and its leading creatives, from a database of 1B+ tracked Meta ads. Use
  when the user gives a domain or URL and wants its traffic, whether and since
  when it runs ads, who sends paid traffic to it, or how its ad volume changed
  month by month. Triggers: "store spy", "does this site run ads", "how much
  traffic does this store get", "check this domain: traffic, ads, creatives",
  "competitor website traffic"; RU «крутит ли домен рекламу», «сколько трафика у
  сайта», «спай магазина». Use this instead of guessing about a specific site's
  ads or traffic. Not for discovering new stores (use spytrend-shop-discovery),
  whole niches (use spytrend-vertical-intel) or the operation behind the ads
  (use spytrend-webmaster-overview).
---

# SpyTrend website advertising review

Read `references/spytrend-contract.md` before making any data call.

## Normalize and preflight

1. Accept one domain, remove scheme, path and leading `www`, and preserve the
   user's exact input as context. Reject credentials and IP-literal targets.
2. Call `get_usage`. State explicit seed limits, profile cap, media count and
   worst-case spend.
3. Default media to off. Do not download or inspect the website itself.

## Workflow

1. Call `search_shops` with the domain, optional selected `country` and a small
   explicit limit. Match the exact host or registrable root deliberately and
   state which scope was selected.
2. Call `get_shop` for the primary returned surface. Extract only bounded public
   fields. Traffic history is a monthly estimate for its stated month.
3. Label `ads_monthly` as ads first discovered by SpyTrend. It is not a Facebook
   launch series. Mark the open current month incomplete.
4. For a closed launch window, call `search_ads` with `landing_domain`,
   `landing_domain_exact=true`, optional selected `country`, concrete dates and
   a one-row limit, then use
   `pagination.total` only with its date-axis
   and total status. If launch-period analytics are unavailable, say so; do not
   substitute the discovery series.
5. Call `search_webmasters` by exact domain with optional selected `countries`
   and a small limit; present matches as observed advertising-network
   attribution, not ownership.
6. Call one bounded `search_ads` seed page per selected surface with
   `landing_domain_exact=true` and optional selected `country`. Use its total for
   volume and its returned rows only to discover advertiser candidates. Cap
   advertiser cards, call `get_advertiser` for only those unique ids, and
   report processed-versus-seen coverage. A card without a `card_status` field
   is complete; `card_status=building` means the card is a placeholder whose
   counters are unavailable, not zero.
7. For website-scoped creative reuse, call `search_ads` again with the exact
   domain/country/date filters and `sort_by=most_reused_creative`, using a small
   selection: on a high-volume domain this ranking exceeds the analytics deadline
   and returns a timeout instead of rows. Always pair it with a concrete date
   window, and add the selected country when the domain is large; widen only if
   the bounded call returned rows. Report the bound you used. Also treat the
   two reuse counters as separate measurements: when
   `same_creative_ads_in_selection` exceeds `same_creative_ads_lifetime`, report
   both as returned and do not present the pair as a subset relation.
   explicit limit. Its representative ads and selection reuse counts are the
   website-scoped ranking. Do not substitute a country-global
   `search_creatives` page or re-sort a bounded lifetime list.
8. With confirmation, retrieve media once for the selected representative ad ids
   and reuse it in every report section.

## Report

Keep Markdown and HTML sections equivalent: website snapshot, traffic period and
quality, advertising volume, advertisers, networks, creative leaders, coverage,
period-axis notes and spend. A different landing domain is a returned fact, not
proof that businesses are unrelated.

Use `references/report-template.md` or the packaged renderer with
`references/report-template.html`; otherwise provide the full report in chat.
