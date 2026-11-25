---
name: marketing-attribution
description: Choose and interpret marketing attribution — last-click vs first-click vs linear vs time-decay vs position-based vs data-driven attribution, MMM (marketing mix modeling), incrementality and holdout tests, attribution window and lookback window, view-through vs click-through conversions, SKAdNetwork and AdAttributionKit privacy limits, ATT and cookie deprecation, MTA multi-touch attribution, platform-reported conversion double-counting and de-overlapping channels, deduplication, and when attribution cannot answer the question.
---

# Marketing Attribution (models, windows, incrementality)

## Attribution answers "who gets credit", never "what did spend cause"

Every rule-based model is an accounting convention chosen before the data arrives: it redistributes
credit among observed touchpoints and cannot say what would have happened without the spend. That
question is causal and needs a holdout. Attribution is for budgeting hygiene and daily routing;
incrementality decides whether a channel deserves funding at all.

## The model menu and what each one is biased toward

```
last-click / last-touch  → over-credits closing, high-intent, retargeting, branded search
first-click / first-touch→ over-credits discovery, upper funnel, prospecting
linear                   → equal split; ignores that touches differ in influence
time-decay               → weights recency via a half-life; still last-click-leaning
data-driven / algorithmic→ fits observed paths (Shapley/Markov-style); sees only tracked touches
MMM                      → aggregate time-series on spend/seasonality/price/promo; no user IDs
incrementality / holdout → randomized exposed vs withheld; the only design measuring causation
```

Rule-based models differ only in the weighting rule, so "which is right" is unanswerable in their own
terms — all are wrong about causation and differ in which channel they flatter. Data-driven models inherit
every observability gap: untracked, offline and privacy-suppressed touches are absent from the path, so
credit flows to whatever is measurable. MMM needs long history and real spend variance and reaches
untrackable channels, but stays correlational until calibrated against experiments.

## Windows, lookback, and view-through

State the window on every figure: click-through lookback (commonly 7 days), view-through lookback
(commonly 1 day), and the post-install conversion window. Changing a window changes the reported result
with no change in reality, so rule that out before believing a step-change. View-through conversions
(impression, no click) are the softest currency here: a 1-day-view and a 7-day-click conversion are
different objects, never summable, and view-through-heavy "performance" is unproven without a holdout.

## Privacy-era measurement (SKAdNetwork / AdAttributionKit, ATT, cookies)

Post-ATT iOS attribution is aggregated, delayed by a randomized timer, coarse (a small conversion value
per install), often without campaign-level granularity, and suppressed below privacy thresholds (null
crowd data). So iOS campaign ROAS is partly modelled, day-level reporting is unreliable near the timer
window, and iOS/Android are not comparable. On web, cookie loss and consent gating push platforms to
modelled conversions reported as observed; decisions below the aggregation floor are noise.

## Double-counting and de-overlapping

Each platform self-attributes with its own model and window inside its own walled garden, so summing
platform-reported conversions exceeds reality — two networks claim the same install. Fixes by strength:
one source of truth (MMP/warehouse) applying a single dedup rule across channels; reconcile the total
against actual orders and distribute the discrepancy explicitly; carry each channel's platform-claimed-to-
MMP ratio as a known bias; run holdouts to size the overlap between paid brand, retargeting and organic.
Retargeting and branded search intercept demand that already existed, and last-click credits them for it.

## When attribution is the wrong tool

Only a holdout (geo split, randomized user-level PSA/ghost-ads cell, or a staged on/off test) answers:
is this channel incremental, does brand spend lift organic, is retargeting buying demand we already had,
what does the next dollar return. Fix cell assignment in advance, keep a pre-period for validation, run
one exposed and one withheld arm, and compute the minimum detectable effect before launch — an
underpowered holdout showing "no lift" has shown nothing. Attribution then routes daily decisions
inside the boundaries the holdout established.

## Failure modes

- Comparing two channels' ROAS from their own dashboards, each with a different model and window.
- Switching model or window and reading the shift as a performance change.
- Merging view-through with click conversions; or treating SKAN-modelled output as observed fact.
- Calling last-click retargeting ROAS a "return" when it is largely intercepted organic demand.

## Reviewer checklist

- [ ] Model, click and view lookback, and conversion window stated for every figure
- [ ] Click-through and view-through reported separately, never summed
- [ ] One source of truth and one dedup rule; total reconciled against orders; overlap sized
- [ ] iOS/SKAN figures labelled aggregated, delayed, partly modelled; no calls below the privacy floor
- [ ] Causal or incrementality claims backed by a holdout, not by attributed conversions
- [ ] Holdout design states cells, pre-period and minimum detectable effect before launch

## Provenance

Standard industry practice for attribution modelling, MMP deduplication and incrementality testing. The
windows named (7-day click, 1-day view) and the described SKAdNetwork behaviour are **derived, unverified**
as stated — verify against current platform documentation, since privacy frameworks change often. Replace
every numeric threshold with the project's own measured values before treating as a target; no vendor
benchmark or lift statistic is claimed.
