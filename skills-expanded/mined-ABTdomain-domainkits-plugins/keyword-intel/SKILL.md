---
name: keyword-intel
description: Map available evidence around a known keyword in the domain market, keeping search-audience, advertiser, new-registration open-market participation, supply and active offers, and completed transactions as distinct layers. Treat .com participation as necessary but not sufficient confirmation of open-market registration interest, and never merge the layers into one demand score or investment verdict. Use when a user wants a deep evidence picture for one known keyword. Not for analyzing a specific domain (use domain-analyze), browsing trends (use keyword-trend-hunter), or a market overview (use domain-market-beat).
---

# Keyword Domain-Market Evidence Map

**What this does:** assembles available evidence around one known keyword, applies a reproducible domain-sample rule, grades each layer by its coverage, and explains where the layers support, limit, or conflict with one another. It gives a layer-specific open-market participation reading but no merged demand score, invest / watch / avoid verdict, or instruction to act.

Different signals measure different things and must be named separately. They can corroborate each other, but none of them alone is "domain demand":

- **Search-audience signal**: search volume, an approximate provider-defined metric (often a trailing average). Report the provider's actual window, geography, language, network, and close-variant treatment.
- **Advertiser signal**: CPC and ad competition (these measure competition for search-ad slots, not domain value).
- **Open-market registration signal**: registration trends and newly registered domains, with `.com` as the necessary confirmation layer and participation breadth checked separately.
- **Domain-market supply and active offers**: current observed registered inventory, listings, bids, and asking prices.
- **Registrable / expiring inventory**: dropped names confirmed registrable and expiring names confirmed by lifecycle and provider.
- **Transaction evidence**: public sale records.

**Data interfaces it needs.** DomainKits MCP supplies part of the evidence through the tools below; it is not the complete analysis engine. Use equivalent sources when available and use host-provided web access for original records and public context. Never assume that an MCP response contains a field that its actual payload does not return. Mark missing fields or capabilities `Unavailable` and continue; do not abort the report because one source is missing.

- Search volume and ad metrics (search-audience and advertiser signals), DomainKits: `keyword_data`
- Market-wide keyword registration trends, that is, what people are registering recently, with source-computed aggregate metrics, DomainKits: `keywords_trends`. It is not a per-keyword query: its figures apply only when the keyword appears on a trend list
- Newly registered domain rows for name structure and coarse timing analysis, DomainKits: `nrds` (no registrar / provider field)
- Cross-TLD registration data, DomainKits: `tld_check`
- Registered and for-sale inventory, DomainKits: `active` / `market` / `aged`
- Registrable / expiring inventory, DomainKits: `deleted` / `expired`
- Availability confirmation, DomainKits: `bulk_available`
- Web access for original transaction records, authoritative sale reports, and context

## Input normalization

Before analyzing, establish the exact keyword; singular, plural, spacing, and hyphen treatment; language; intended meaning or industry; relevant geography for search and advertising data; TLD scope; and the reporting window. Many keywords carry several meanings (`apple`, `flow`, `java`). If the meaning would materially change the sample, ask one concise question; otherwise disclose the defaults.

**Brand-dominant boundary.** If the keyword corresponds mainly to one existing brand, switch to brand-risk / defensive-observation mode. Describe registration, supply, and transaction evidence only as brand-specific activity; do not call it broad keyword-market participation, present registrable or listed names as opportunities, or produce favorable acquisition framing. State that a public-web check is not trademark clearance or legal advice.

**Domain-sample matching rule.** Define and disclose the primary sample before pulling domain data:

- Include an exact label match or a hyphen-delimited component equal to the keyword.
- Include a concatenated label only when the keyword is a complete, unambiguous component and the remaining prefix or suffix is a recognizable word or purposeful modifier. For `art`, `arthub` and `getart` qualify; `cart`, `smart`, `chart`, and `artisan` do not.
- Exclude ambiguous segmentations from the primary sample. If useful, show them in a separately labeled ambiguous sample that does not enter counts, ratios, concentration, or conclusions.
- Decide whether plurals, spelling variants, and translated forms belong in separately labeled secondary samples. Never blend them silently with the exact-keyword primary sample.
- Apply the same manually reviewable rule across `nrds`, `active` / `market` / `aged`, `deleted` / `expired`, and transaction search. When a provider supplies an aggregate whose matching or close-variant rules cannot be reconstructed, report it using the provider's own semantics and do not combine it mathematically with the manually filtered domain sample.

## Evidence discipline

- Attach a source, provider, observation date, and relevant scope to every factual claim; mark every interpretation as inference. Report geography and language for search or advertiser data and wherever a source actually provides them. For registration, supply, and transaction layers, report TLD, feed, marketplace, or source coverage instead of inventing a geographic scope.
- **Coverage gate for ratios.** Before calculating a ratio from domain rows, deduplicate the sample and record its returned sample size, provider window or recency buckets, TLD or feed coverage, pagination completed, result cap, and whether the source claims completeness. Exhaust available pages when practical. If coverage or pagination is incomplete or unknown, label every derived ratio as an `observed-sample ratio`, do not generalize it to the full cohort, and lower the layer confidence. Treat aggregate `.com`, TLD, and registrar metrics from `keywords_trends` as provider-computed cohort metrics and retain their stated scope; do not recompute or silently combine them with a differently covered `nrds` sample. Do not report an open-market validation conclusion when missing coverage could materially change `.com` participation.
- **Currency on every price.** Every CPC, listing, and sale price carries its original currency, the data date, and the provider; if converted, note the exchange-rate source and conversion date. Do not combine prices in different currencies without conversion.
- **Search and advertiser metrics are not domain demand.** Volume is a search-audience signal; CPC and ad competition are advertiser signals. Report them as such; do not translate them into domain value. Search volume is a provider-defined metric with its own window and close-variant handling; report the provider's actual window, geography, language, network, and variant treatment. Do not sum singular, plural, spelling, or close-variant volumes when the provider may already aggregate them; report the possible overlap instead.
- **Time discipline.** Build search queries from the current date and the reporting window (default the last 12 months, with more recent events listed separately). Never hard-code a year. Distinguish event date from article publication date; an old sale re-reported is not a new sale.
- **`.com` is necessary, not sufficient.** In a sufficiently covered new-registration cohort, no `.com` participation means the registration layer is `not validated by the open domain market`. When coverage is insufficient, the result is `unresolved`, not negative. The presence of `.com` is only the first condition: interpret it together with the absolute `.com` count, `.com` share, registrar concentration, nameserver concentration, naming-pattern diversity, persistence across windows, low-base risk, single-TLD concentration, and sale-platform nameserver share. Registrar and nameserver concentration are participant-diversity proxies, not proof of participant count. Sale-platform nameserver share is the share of the cohort whose nameservers point at sale platforms, not a verified listing count; a high share suggests resale-led participation, which is an inference. Judge the layer against a balanced free market: many independent participants, with end use and resale both present. A cohort dominated by one registrar, nameserver, naming template, or by sale-platform nameservers is concentrated; a high sale-platform nameserver share together with nameserver concentration on the same platforms is one finding (inferred heavy speculation), not two. Do not describe non-`.com` activity as nonexistent; state only whether it is validated by the open domain market.
- **Supply is point-in-time and partial.** `deleted` is not confirmed registrable until re-checked with `bulk_available`; `expired` is not necessarily backorderable until lifecycle and provider are confirmed; `aged` filtered to for-sale listings is a current listing, not a sale; `active` returns a set that is not the total `.com` market unless the tool guarantees full coverage. Record status, source, and observation time.
- **Registration-velocity discipline.** A short-window comparison (for example 0 to 10 days vs 10 to 20 days) is affected by reporting lag, weekend/weekday effects, low base, promotions, incomplete coverage, and seasonality. Report current-window count, comparison-window count, absolute change, percentage change, data coverage, whether a low base is present, and a longer baseline if the tool supports one. When the comparison-window count is zero, the percentage change is undefined: report it as Not Meaningful (a rise from zero) and show the absolute counts, rather than an infinite or 0-based percentage. Without full data, report only observed acceleration or deceleration, not an "investment window".
- **Naming structure is not quality.** Hyphen share, numeric share, and length are structural features, not a "junk" verdict; acceptance of digits and hyphens varies by language, region, and industry. Report hyphen share, numeric share, median/average length, and prefix/suffix patterns from the domain rows, and label any quality reading as inference.
- **Define concentration the same way every run.** Report registrar / provider concentration only from the source-computed distribution returned by `keywords_trends`: the single largest registrar's share and the Top-3 cumulative share when each is provided, stated with the provider cohort size and scope. Do not reconstruct Top-3 from `nrds` or an incomplete registrar list, and do not report a bare "high / low concentration" without the underlying share. Apply the same disclosure discipline to single-TLD concentration (largest-suffix share) and nameserver concentration (largest-nameserver share). Mark missing concentration fields `Unavailable` rather than substituting another population.
- **Co-occurrence is not causation.** Co-occurring naming themes (for example the keyword plus `ai` or `cloud`) are observed associations. Do not call them causal drivers unless an authoritative source explicitly establishes the connection.
- **Transaction evidence levels.** A `verified completed sale` requires an original marketplace or auction result, or an authoritative transaction record, explicitly stating that the sale completed and at what price. A `publicly reported sale` is a named credible publication or sale database reporting a completed transaction when the original record is unavailable. A `finalized auction result` requires the venue or authoritative record to mark the auction closed and sold or won; an ended listing or last visible bid is insufficient. Search snippets, copied lists, and unsourced aggregations are leads only: open the underlying source before retaining an item. Current bids and asking prices belong only in active offers. Record price, currency, venue, event date, publication date, source, and level; deduplicate republications. If nothing qualifies, write "no public transaction records found in the searched sources", never "no transactions".
- **No verdict, and no single overall grade.** Characterize each layer separately and allow only layer-specific conclusions, including the open-market registration reading. Attach a provider rating only to the layer it measures. Present supporting signals, limiting or speculative signals, conflicts, and per-layer confidence without an overall score, invest / watch / avoid verdict, or instruction to act quickly.

## Workflow

Gather each layer independently; a failed source marks that layer Unavailable and does not stop the report.

1. **Scope and sample rule.** Normalize the keyword and window, apply the brand boundary, and define the primary, secondary, and ambiguous domain samples.

2. **Search-audience and advertiser signals.** `keyword_data` for volume (search-audience) and CPC / ad competition (advertiser), each labeled as its own signal with geography and time.

3. **Registration activity and open-market participation.** If the keyword appears on a `keywords_trends` list, use that trend cohort and its `.com`, TLD, registrar, nameserver, and sale-platform nameserver metrics when returned; if it does not, the cohort-level metrics are Unavailable and this layer rests on `nrds` rows. Use `nrds` only as a domain-row sample for naming-pattern diversity and the timing detail its day-level registration dates or recency buckets support. Do not merge the two populations unless their keyword semantics, provider window, data date, and coverage align. Report absolute `.com` count only when the trend source returns it; never reverse it from a rounded ratio. Apply the coverage gate to every derived `nrds` metric. Conclude this layer as `open-market participation supported`, `participation concentrated`, `not validated by the open domain market`, or `unresolved`, with the underlying figures, missing fields, and coverage. `.com` is necessary for support but never sufficient by itself; a missing material signal makes the result unresolved.

4. **Installed supply and active offers.** Use `tld_check` for the installed cross-TLD base and `active` / `market` / `aged` for observed registered and for-sale inventory. Deduplicate by normalized domain across those interfaces; count each domain once for supply and each distinct offer once, noting cross-venue price differences. Treat for-sale `aged` results, current bids, and asking prices as active offers, never transactions. State coverage rather than calling the result the total market.

5. **Registrable and expiring inventory.** Query `deleted` for dropped names and retain only those re-confirmed by `bulk_available`, with availability timestamp and registration pricing when returned. Query `expired` for expiring inventory and retain only names whose lifecycle, auction or backorder status, and provider are confirmed; do not use `bulk_available` on names that remain registered. Keep this inventory separate from installed supply and active offers. In brand-dominant mode, report aggregate risk context only and do not surface names as opportunities.

6. **Transaction evidence.** Search the web within the reporting window, open the underlying source, apply the transaction evidence levels, and record the required fields. Current bids and listings remain in step 4.

7. **Naming-pattern observations.** From the filtered `nrds` cohort, report structural shares and co-occurring themes as observations, not drivers.

8. **Report** using the compact output structure below.

## Output structure

1. **Scope, matching, and coverage:** keyword meaning, primary / secondary / ambiguous samples, TLD and reporting scope, provider matching semantics, returned sample sizes, pagination, result caps, and completeness limits. State whether brand-dominant mode applies.
2. **Search-audience and advertiser layers:** report volume separately from CPC and ad competition, with each provider's geography, language, network, metric window, and close-variant treatment.
3. **Registration activity and open-market participation:** trend and velocity figures; the `.com`, TLD, registrar, nameserver, pattern, persistence, low-base, and sale-platform nameserver signals; coverage qualification; and one layer conclusion (`supported`, `concentrated`, `not validated by the open domain market`, or `unresolved`).
4. **Installed supply and active offers:** observed registered / listed inventory, deduplicated counts, current bids and asking prices, listing type, currency, source, observation date, and coverage limits.
5. **Registrable and expiring inventory:** deleted names confirmed available at check time and expired names confirmed by lifecycle / auction / backorder status and provider, kept in separate groups. Omit candidate-level opportunity framing in brand-dominant mode.
6. **Public transaction evidence:** qualifying completed-sale items with evidence level, price, currency, venue, event and publication dates, and source; otherwise the fixed no-public-records statement.
7. **Naming-pattern observations:** structural shares and co-occurring themes, labeled as observations or inference rather than quality or causation.
8. **Layer synthesis:** supporting signals, limiting or speculative signals, conflicts, and confidence for each layer. Do not merge them into one demand score or recommendation.
9. **Evidence limits and source trail:** Unavailable capabilities, partial coverage, low-base or lag caveats, and source / provider / observation date / relevant scope for every factual layer.

## Next steps

Only if the user asks: a deep analysis of a specific domain (domain-analyze), monitoring, a saved strategy to re-run later, or analysis of a different keyword. Do not push the user toward acquisition or tell them to act.

## Key principles

- Keep the evidence layers distinct; never merge them into one demand figure, overall grade, or investment verdict.
- `.com` is necessary, not sufficient; judge registration participation against a balanced free market, and measure each signal the same way on every run.
- Fix the primary sample before pulling data, and apply the coverage gate before every ratio.
- Count each domain and each offer once; active offers are not transactions, and transaction evidence is verified at its source.
- Keep registrable and expiring inventory in its own section; `bulk_available` measures registrability only.
- In brand-dominant mode, report brand-specific activity and risk context only.
- Source, provider, observation date, and scope on every fact; inference on every interpretation; Unavailable on missing sources without aborting.
