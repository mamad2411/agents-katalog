---
name: keyword-trend-hunter
description: Discover hot or emerging domain-registration keywords, validate each detected spike against an aligned new-registration cohort from the global open domain market using .com participation, concentration, persistence, and naming-structure signals, and optionally surface related lifecycle inventory without recommending acquisition. Use when a user wants to browse registration trends. For a full evidence analysis of one known keyword use keyword-intel; for a specific domain use domain-analyze; for market news use domain-market-beat.
---

# Keyword Registration Trend Hunter

**What this does:** discovers keyword spikes, checks whether each spike is supported by broad participation in the same new-registration event cohort, and optionally surfaces related dropped, expiring, or listed inventory. It evaluates open-market registration participation, not aftermarket demand or investment merit.

**Data interfaces it needs.** DomainKits MCP supplies part of the evidence through the tools below; it is not the complete analysis engine. Use equivalent sources when available and use host-provided web access for public-page checks. Never assume a field exists merely because the workflow needs it. Mark an unavailable field or capability `Unavailable` and continue.

- Market-wide keyword registration trends, that is, what people are registering recently (hot, emerging, prefix), with source-computed aggregate metrics, DomainKits: `keywords_trends`. Read registrar Top-1 / Top-3 and nameserver concentration only from this trend source when returned.
- Newly registered domain rows for naming-pattern and coarse timing detail, DomainKits: `nrds`. It does not provide registrar / provider, so never calculate registrar concentration from it.
- Registrable / expiring / listed inventory, DomainKits: `deleted` / `expired` / `market` (`aged` as a supplement for names with long registration histories)
- Availability confirmation, DomainKits: `bulk_available`
- Web access for a lightweight brand-dominance and collision check before candidate inventory is surfaced

**Skill boundary:** this skill owns trend discovery, event-cohort integrity, preliminary open-market validation, and optional lifecycle inventory. Use `keyword-intel` for the full evidence picture of a selected keyword, including search-audience, advertiser, installed supply, active offers, and completed transactions. Do not reproduce those layers here.

## Open-market participation model

This skill evaluates trends within the global, general-purpose open domain market. Its core evidence is new-registration participation: `.com` participation is necessary confirmation of open-market interest, but it is never sufficient by itself. The full model requires broad, persistent, and structurally diverse participation rather than one concentrated registration pattern.

`.com` is the primary confirmation layer because it is the most established global namespace and aftermarket: registration cost and quality-name scarcity are higher, global recognition and end use are broader, secondary-market liquidity is stronger, and registering a `.com` means accepting more competition. It remains the largest single TLD by registration volume. A keyword trend with little or no `.com` participation is not considered validated by the open domain market, especially when registrations are concentrated in one low-cost TLD, one registrar, or a repeated naming pattern.

This model does not claim a non-.com ecosystem cannot be active. It means such activity has not been validated as a broad open-market domain trend. Extension-native ecosystems require a separate model.

Independent participation, not raw `.com` count. A large `.com` block created through one concentrated pattern is not broad participation. Read the cohort from nine signals together: absolute `.com` count, `.com` share, registrar concentration, nameserver concentration, naming-pattern diversity, persistence across windows, low-base status, single-TLD concentration, and sale-platform nameserver share. Registrar and nameserver concentration are participant-diversity proxies, not direct participant counts; sale-platform nameserver share bears on how much of the participation is resale. Each signal is defined under Signal thresholds.

The yardstick is a balanced free market: many independent participants across registrars, nameservers, TLDs, and naming patterns, over several windows, with end use and resale both present. A spike dominated by any one of them is concentrated.

## Event-cohort integrity

The trend record and the detailed `nrds` sample must describe the same event before their signals are combined.

- Record the detected keyword, provider-defined match semantics, provider-supplied window or bucket definition, data date when supplied, query observation time, TLD or feed coverage, and event-cohort total from `keywords_trends`. Do not manufacture exact event start or end dates from the query date. If the source exposes only a nominal rolling window, report that window and mark exact boundaries `Unavailable`.
- Pull `nrds` for the same keyword and constrain it to the same dates and TLD or feed coverage where the interface permits. If exact alignment is impossible, label `nrds` as supplemental and do not merge its ratios or concentration metrics into the provider's event-cohort figures.
- For domains reviewed from `nrds` or inventory, include the keyword only when it is an exact label, a hyphen-delimited component, or an unambiguous component in a concatenated label. Exclude accidental substrings and ambiguous segmentations from the primary sample; variants belong in a separately labeled secondary sample.
- Before calculating any ratio from `nrds`, deduplicate the sample and record returned count, pagination completed, result cap, and whether the source claims completeness. When coverage is incomplete or unknown, label ratios as `observed-sample ratios`. If the missing data could materially change `.com` participation, concentration, or persistence, the outcome is uncertain.

## Signal thresholds (heuristic bands)

The following bands are heuristic starting points, not statistical laws. Treat a value near a band edge as uncertain, not decisive, and always show the underlying figure.

Data semantics: all ratios and concentration metrics are calculated from registrations contributing to the detected keyword spike, not from the total installed domain base. They therefore describe revealed choices within the incremental event cohort.

- `.com` share: core-market participation. Roughly, higher (around 15% and up) is consistent with genuine open-market interest; very low (around 5% and below) is consistent with bulk activity on cheap TLDs.
- Largest-TLD share: single-suffix concentration. High (around 70% and up) on a non-.com TLD is consistent with concentration in one suffix rather than broad demand.
- Digit share: naming-structure signal. High (around 20% and up) is consistent with template or bulk-driven registration.
- Registration persistence: measure as the number of distinct time windows (for example days within the cohort period) that carry new registrations, and the share of the cohort falling in its single busiest window. Persistent is roughly activity in several windows with no single window dominating (busiest-window share well under half); a single-day burst (one window holding most of the cohort) is not persistent. Show the per-window counts.
- Registrar / provider concentration and pattern concentration: use source-computed registrar shares from `keywords_trends`, reporting the single largest registrar's share and the Top-3 cumulative share when each is returned, stated with the provider cohort size. Do not reconstruct Top-3 from `nrds` or from an incomplete registrar list. Measure pattern concentration from the aligned domain-row sample as the share following one repeated template. A largest-registrar share around half and up weakens the evidence of broad participation but does not establish how many actors exist. A dominant template is direct evidence of structural concentration. Interpret registrar concentration together with pattern, suffix, and time concentration; never convert it into a participant count.
- Nameserver concentration: the largest single nameserver's share of the cohort, from `keywords_trends` when returned. A share around half and up is consistent with one operator or one parking or hosting setup behind much of the spike and weakens the evidence of broad participation. A popular registrar's default nameservers can produce the same reading, so interpret it together with registrar concentration.
- Sale-platform nameserver share: the share of the cohort whose nameservers point at sale platforms, from `keywords_trends` when returned. It is not a verified listing count: names listed without those nameservers are missed, and a parked name is not proof of an active listing. When most of the cohort sits on sale-platform nameservers, infer speculation-led participation and label it as inference; it counts as concentration. Nameserver concentration on the same platforms is the same finding, not a second signal.
- Low base: flag whenever the cohort total is small enough that ratios are unstable (for example a cohort in the low tens or fewer, or any single suffix or window driven by only a handful of names). A low-base flag caps the outcome at uncertain regardless of how the ratios read.

If these bands have been back-tested on historical data, state it and record: the calibration sample's date range; which TLDs the sample covers; the label used for a "validated" trend; and whether the bands are updated periodically. If they have not been back-tested, keep them as heuristic bands: the model supports the direction of each signal, but the specific numbers are not derived laws. Do not present a specific cutoff as a proven threshold without that calibration record.

## Evidence discipline

- **Use a fixed outcome order.** Classify each selected trend in this order:
  1. `Brand-specific / model not applied` when the keyword mainly identifies one existing brand; do not surface candidate inventory.
  2. `Uncertain` when the cohort has a low base, cannot be aligned, has materially incomplete coverage, or is missing a signal that could change the result.
  3. `Not validated by the open market` when an adequately covered cohort has no `.com` participation or falls in the very-low `.com` band.
  4. `Concentrated` when `.com` participates but suffix, template, time, nameserver, or combined registrar-plus-structure evidence shows the spike is materially concentrated, or sale-platform nameservers dominate the cohort (inferred speculation-led participation).
  5. `Open-market validated` only when `.com` participation is meaningful, the cohort is not low-base, activity persists across windows, naming patterns are diverse, and no material concentration signal contradicts the reading.
  Mixed evidence that fits none of these rules is `Uncertain`. Always show the underlying figures. These are open-market registration outcomes, not investment instructions.
- **Read participation from multiple signals**, per the model above; never from `.com` count alone.
- **Brand boundary.** Run a lightweight public-web check on a selected keyword before validation is finalized or candidates are surfaced. If it mainly identifies one existing brand, report the observed spike only as brand-specific registration activity, stop the open-market model, and do not surface registrable, expiring, or listed names as opportunities. State that the check is not trademark clearance or legal advice.
- **Do not infer a cause.** Registration concentration, timing, or naming co-occurrence does not establish a promotion, sale, news event, or other catalyst. Use `keyword-intel` or `domain-market-beat` when the user asks for deeper market or event evidence.
- **Lifecycle verification is stage-specific.** `bulk_available` confirms only whether a name can be registered now, so it applies to `deleted` candidates. It does not validate `expired` (confirm backorder / auction status and provider) or a for-sale listing from `market` or `aged` (a current listing, not a sale). For a listing, attempt to re-check it against the listing tool or the named marketplace before presenting it. If that re-check succeeds, record the verification source; if the marketplace cannot be reached, present the tool-reported listing labeled "listing not re-verified" and treat it as weaker evidence rather than dropping the candidate. Record status and observation time either way.

## Workflow

Proceed end to end when the user names a keyword, requests a fixed number of trends, or explicitly asks for candidates. Pause after discovery only when the user must choose which surfaced keyword to validate. Pause before `expired` or for-sale listings only when willingness to backorder or purchase a registered name is unknown. Do not force phase-by-phase confirmation when the user's requested scope is already clear.

1. **Discover.** Surface trending keywords with `keywords_trends` (hot, emerging, or prefix). For each surfaced keyword, deliver a fixed set so runs stay comparable, marking any field the source does not provide as Unavailable rather than omitting it:
   - the provider-supplied cohort window or bucket definition, any provider data date, and the separate query observation timestamp. Never stamp or reconstruct event boundaries from the current date; if only a nominal rolling window is known, say so;
   - the coverage the source provides (which TLDs or feeds the cohort is drawn from, and whether it is a sample or claims completeness), so a difference between runs is not mistaken for a real change;
   - the spike / event-cohort total (how many new registrations define the trend);
   - the absolute `.com` count in that cohort when the source returns it, alongside the `.com` share; never derive a supposedly exact count from a rounded ratio, and mark the count `Unavailable` otherwise;
   - the provider's structure metrics when returned: digit share, the largest TLD, and its share (single-TLD concentration);
   - a preliminary participation reading from the provider's available metrics, using the heuristic bands and showing every underlying figure; never label it the final open-market outcome while registrar concentration, pattern diversity, or persistence remains Pending;
   - a low-base flag whenever the cohort total is small.
   - registrar Top-1 and Top-3 shares from `keywords_trends` when returned; mark either metric `Unavailable` when absent;
   - nameserver concentration (largest-nameserver share) and sale-platform nameserver share from `keywords_trends` when returned; mark either `Unavailable` when absent;
   Pattern diversity and detailed time structure come from `nrds` in step 2, so mark those fields Pending here. Two cohorts are comparable only when their provider window, data date, coverage, and keyword-match semantics align. If the user has not chosen a keyword or requested an end-to-end top-N analysis, ask which keyword(s) to validate; otherwise continue.

2. **Validate the event cohort.** For each selected keyword:
   - Apply the brand boundary and event-cohort integrity rules.
   - Pull `nrds` for the aligned cohort and report its matching rule, returned count, pagination / result-cap status, naming-pattern diversity, hyphen / digit / length structure, repeated-template share, and the coarse time clustering supported by its day-level registration dates or the available recency buckets. If it cannot be aligned to the trend record, keep it supplemental and make the outcome uncertain rather than merging unlike samples.
   - Apply the fixed outcome order to all nine signals. Report the outcome, confidence, exact figures, cohort dates, observation date, coverage, and unavailable fields.
   - If the user requests search-audience, advertiser, supply, offer, transaction, or catalyst evidence for the chosen keyword, use `keyword-intel`; do not rebuild those layers here.

3. **Surface lifecycle candidates when requested.** Skip this phase for a brand-specific keyword. Filter every result through the same keyword-matching rule used for the event cohort:
   - `deleted` for dropped names, each re-confirmed registrable with `bulk_available`.
   - `expired` only when the user accepts backorder (confirm lifecycle / provider).
   - `market` filtered to for-sale listings, with `aged` as a supplement for names with long registration histories (a listing, not a sale).
   Present each candidate with: domain; exact keyword component and position; matching category (exact / hyphen-delimited / unambiguous concatenation); relation to the validated trend; lifecycle stage; acquisition path; verification source and result; price type, amount, currency, and date where applicable; observation date; and any brand-collision caveat. Exclude ambiguous matches. Mark unavailable fields explicitly. Present candidates as options, not recommendations.

## Next steps

Only if the user asks: use `keyword-intel` for a full evidence analysis of a selected keyword, `domain-analyze` for one domain, monitoring for later changes, or repeat discovery for another trend set. Do not push acquisition or tell the user to act.

## Key principles

- Judge each trend against a balanced free market by aligned new-registration evidence; `.com` is necessary confirmation, not sufficient proof.
- Combine the trend record and `nrds` only when they describe the same event cohort; never fabricate event boundaries.
- Read all nine signals together, show every underlying figure, and measure each signal the same way on every run; thresholds are heuristic bands, not laws.
- Apply the fixed outcome order in Evidence discipline; mixed evidence is uncertain.
- Record sample size, pagination, coverage, and observation dates; partial ratios are observed-sample ratios, not population claims.
- Stop at the brand boundary, verify lifecycle candidates by stage, and present candidates as options, not recommendations.
- Leave full known-keyword intelligence to `keyword-intel`.
