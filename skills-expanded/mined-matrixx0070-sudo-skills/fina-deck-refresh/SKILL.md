---
name: fina-deck-refresh
version: 1.0.0
description: Refreshes an existing pitch or board deck to current data, re-pulling financials, market data, and comps, updating every linked number and chart, and producing a redlined change log tied back to the source model.
author: matrixx0070
tags: [finance, investment-banking, presentation, powerpoint, deck-refresh, version-control, qc]
capabilities: []
---

# Finance Deck Refresh

## When to use
Use this when a previously built pitch, board, or committee deck already exists and you need to bring it current: new fiscal period, new market close, new comps set, or a materially moved number since the last version. This is the "update the deck we sent last quarter" workflow, not a build from a blank file.

**Not for:** authoring a new deck from scratch (use fina-pptx-author), building the reusable master/template (use fina-ppt-template-creator), or the final pre-send proofing pass (use fina-ib-check-deck). Rebuild the underlying analysis in fina-comps-analysis, fina-dcf-model, or fina-3-statement-model before you refresh the slides that display it.

## Method
1. **Freeze the baseline first.** You duplicate the current deck as an immutable `vN` snapshot and record the as-of date, source model file names, and data-provider timestamps before touching anything. Decision point: if the deck has no traceable source model or the links are broken, you stop refreshing and escalate to a rebuild rather than editing numbers by hand.
2. **Inventory every dynamic element.** You walk the deck slide by slide and tag each figure, table, chart, date, logo, and footnote as either static (thesis text, section dividers) or dynamic (anything sourced from a model, market feed, or comps set). The dynamic list becomes your refresh worklist.
3. **Choose refresh scope.** Decision point: if fewer than roughly a third of exhibits moved and the storyline is unchanged, you do a partial refresh of only the tagged elements; if the storyline, comps universe, or period definition changed, you escalate to a structural rebuild and hand the analysis back to the relevant model skill.
4. **Re-pull the sources.** You regenerate the underlying numbers from the current model and market data: latest reported financials from fina-3-statement-model, updated multiples from fina-comps-analysis, refreshed valuation from fina-dcf-model, and current share prices, FX, and index levels as of a single stated market close.
5. **Update linked numbers and charts.** You push the refreshed values through every dependent exhibit, keeping units, currency, rounding, and chart axes identical to the prior version so changes read as data changes, not formatting drift.
6. **Refresh chrome and metadata.** You update the cover date, "as of" and "market data as of" lines, footer dates, page numbers, project code name, deal team, and any changed logos or disclaimers.
7. **Tie back every number to the source.** You verify each refreshed figure reconciles to the model cell or data pull it came from and record the tie-out in a verification table; nothing ships that you cannot trace to a source.
8. **Flag material moves.** Decision point: if a headline metric moves beyond your materiality threshold (default: 5% relative or any sign flip, credit-metric breach, or covenant trip), you flag it for the deal lead with a note rather than silently overwriting; immaterial moves are updated in place and still logged.
9. **Redline and version.** You produce a change log of every altered value and slide, save the new version under the naming convention, and hand off to fina-ib-check-deck for the final proofing pass.

## Example
A board deck from Q1 shows revenue of $412.0mm and a peer median EV/EBITDA of 11.4x, "market data as of 15-Feb." You freeze it as `Project Atlas_BoardDeck_v3_2026-02-15`. You re-pull Q2 actuals from the 3-statement model (revenue now $438.5mm) and refresh comps as of the 14-May close (median now 10.8x). Revenue moved +6.4% (above the 5% flag threshold), so you flag it: "Rev +6.4% QoQ, driven by segment X; confirm narrative on slide 4." The comps move (-5.3% on the multiple) is also flagged. You update slides 4, 7, and the valuation football field, refresh the cover to "as of 14-May," bump page count after adding one appendix exhibit, tie every number back to the model, and write the change log entry before saving `v4`.

## Pitfalls
- **Silent material moves.** Overwriting a number that jumped 20% without telling the deal lead lets a stale narrative ship next to fresh data; always flag beyond threshold.
- **Broken model links.** Trusting an old linked cell that no longer points at the live model produces confidently wrong numbers; re-pull from the source, never nudge a value manually.
- **Mixed as-of dates.** Refreshing financials to Q2 but leaving comps at the old market close creates internally inconsistent exhibits; pin one financial period and one market-data date and state both.
- **Formatting drift.** Changing rounding, units, or axis scale during a refresh makes real changes indistinguishable from cosmetic noise; hold formatting constant so deltas are legible.
- **Untracked chrome.** Forgetting the cover date, footers, or project code leaves the deck looking stale even when every number is current; treat metadata as a first-class refresh item.
- **No baseline snapshot.** Editing the live file in place destroys your ability to redline what changed; always freeze `vN` before touching `vN+1`.

## Output format
```
DECK REFRESH SUMMARY — Project Atlas Board Deck
Baseline:      v3  (financials as of Q1; market data as of 15-Feb)
Refreshed to:  v4  (financials as of Q2; market data as of 14-May)
Scope:         PARTIAL (11 of 34 dynamic elements updated)

CHANGE LOG
Slide  Element              Old        New        Delta      Flag
4      Revenue             $412.0mm   $438.5mm   +6.4%      MATERIAL — narrative confirm
7      Peer median EV/EBITDA 11.4x     10.8x     -5.3%      MATERIAL — football field shifted
7      Implied EV          $4,700mm   $4,735mm   +0.7%      —
12     Net leverage        3.1x       2.9x       -6.5%      MATERIAL — covenant headroom up
Cover  Market data as of   15-Feb     14-May     —          metadata

TIE-BACK: 11/11 refreshed values reconciled to source model/data pull.
NEXT: hand to fina-ib-check-deck for final proof.
```

## Reference

### Refresh checklist
| Category | What you refresh | Source |
| --- | --- | --- |
| Financials | Reported actuals, estimates, growth rates, margins | fina-3-statement-model |
| Valuation | DCF output, implied ranges, football field | fina-dcf-model |
| Comps | Peer set, multiples, premia | fina-comps-analysis |
| Market data | Share price, FX, index levels, rates | Single stated market close |
| Charts | Data series, axis labels, data labels | Linked to refreshed tables |
| Dates | Cover, "as of" lines, footers | Current period + market date |
| Chrome | Logos, page numbers, project code, deal team, disclaimers | Deck metadata |
| Footnotes | Source citations, "as of" qualifiers | Matched to each refreshed exhibit |

### Tie-back verification
| Check | Pass condition |
| --- | --- |
| Number-to-cell | Every displayed figure maps to a named model cell or data pull |
| Single period | All financials share one fiscal period definition |
| Single market date | All market data shares one close date |
| Chart-to-table | Chart series equals its underlying table row exactly |
| Rounding constant | Rounding convention unchanged from prior version |
| Cross-slide | Repeated numbers (e.g., revenue) agree on every slide |

### Materiality flag thresholds (defaults)
| Metric type | Flag when |
| --- | --- |
| Revenue / EBITDA / EPS | >= 5% relative move |
| Multiples (EV/EBITDA, P/E) | >= 5% relative move |
| Leverage / coverage | Any covenant-relevant move or breach |
| Any metric | Sign flip (positive to negative or vice versa) |
| Valuation range | Midpoint moves outside prior stated range |

### Version-control conventions
| Element | Convention |
| --- | --- |
| File name | `Project<Code>_<DeckType>_v<N>_<YYYY-MM-DD>` |
| Snapshot | Freeze prior `vN` read-only before editing `vN+1` |
| As-of stamp | Cover carries "financials as of" and "market data as of" |
| Redline | Change log lists slide, element, old, new, delta, flag |
| Handoff | Every refreshed deck exits through fina-ib-check-deck |
