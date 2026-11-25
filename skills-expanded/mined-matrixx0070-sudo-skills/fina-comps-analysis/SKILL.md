---
name: fina-comps-analysis
version: 1.0.0
description: Value a company against its peers using trading comparables and precedent transactions, producing calendarized multiples and a football-field valuation range.
author: matrixx0070
tags: [finance, valuation, comps, comparable-companies, precedent-transactions, enterprise-value, multiples, football-field]
capabilities: []
---

# Comparable Company Analysis (Trading Comps and Precedent Transactions)

## When to use
Use this to value a target relative to the market by benchmarking it against a set of publicly traded peers (trading comps) and past M&A deals (precedent transactions), then translating peer multiples into an implied valuation range.

**Not for:** an intrinsic discounted-cash-flow valuation (fina-dcf-model), building the projection engine that feeds it (fina-3-statement-model), cleaning the raw filing extract before you spread it (fina-clean-data-xls), or laying out the finished comps set as a workbook (fina-xlsx-author).

## Method
1. **Define the target and its universe.** State the company, sector, geography, and the metrics you will value on (revenue, EBITDA, EPS). Pull the target's own capital structure and latest financials as the yardstick everything else is scaled to.
2. **Screen the peer set.** Select 6-12 comparables by industry, business model, size (revenue/market cap within roughly 0.3x-3x), growth, and margin profile. Decision point: if a candidate matches the SIC code but has a fundamentally different margin or growth structure (e.g. a distributor vs a manufacturer), exclude it or move it to a labeled secondary tier rather than diluting the core median.
3. **Build the enterprise value bridge for each name.** EV = equity value (diluted shares x price) + total debt + minority interest + preferred equity - cash and equivalents. Use the treasury stock method for options and count in-the-money converts.
4. **Calendarize and LTM-adjust.** Put every company on a common period. Convert off-calendar fiscal years to a calendar basis and compute last-twelve-months figures: LTM = most recent full year + current-year stub - prior-year stub.
5. **Normalize the financials.** Strip non-recurring items (restructuring, impairments, litigation, one-time gains) from EBITDA/EBIT/EPS so multiples compare clean run-rate economics. Adjust for stock-based comp treatment consistently across all names.
6. **Compute the multiples.** EV/Revenue, EV/EBITDA, EV/EBIT for capital-structure-neutral metrics; P/E and PEG for equity-level metrics. Keep numerator and denominator on the same footing (unlevered metric under an EV numerator; per-share earnings under an equity numerator).
7. **Scrub for non-comparability.** Flag outliers and understand them before trimming. Decision point: if a name trades at a multiple more than ~1.5 interquartile ranges from the pack, decide whether it reflects a real difference (superior growth, takeover speculation) that justifies exclusion, versus a data error you must fix.
8. **Apply the reference multiple.** Multiply the peer median (primary) and mean (sensitivity) multiple by the target's corresponding metric to get implied EV, then bridge back to implied equity value and per-share price.
9. **Add precedent transactions.** Repeat with deal multiples from comparable acquisitions; these embed a control premium and sit above trading levels. Present them as a separate, higher range.
10. **Assemble the football field.** Stack the low-high ranges from each method (trading EV/EBITDA, trading EV/Revenue, precedents, and any DCF from fina-dcf-model) into one chart so the overlap zone frames the defensible valuation.

## Example
Target: LTM revenue $500M, LTM EBITDA $100M (20% margin), net debt $150M, 40M diluted shares.

Peer set median EV/EBITDA = 11.0x, mean = 11.6x. Implied EV = 11.0x x $100M = $1,100M. Implied equity = $1,100M - $150M net debt = $950M. Per share = $950M / 40M = $23.75.

Cross-check on EV/Revenue: peer median 2.2x x $500M = $1,100M EV - same, because the target's 20% margin sits on the peer median, so both multiples reconcile.

Precedent transactions median EV/EBITDA = 13.5x (embeds a control premium): implied EV = $1,350M, equity = $1,200M, $30.00/share. Football field: trading range $22-$26, precedents $28-$32.

## Pitfalls
- **Equity-to-EV mismatch.** Pairing an EV numerator with a levered denominator (net income) or an equity numerator with an unlevered denominator (EBITDA) produces a meaningless multiple; keep both sides on the same capital-structure footing.
- **Stale share count.** Using basic shares or an old diluted count understates equity value; recompute treasury-stock-method dilution at the current price.
- **Un-calendarized peers.** Comparing a March fiscal-year company to a December one without stubbing mixes different economic periods and skews the median.
- **Reported over normalized EBITDA.** Leaving a one-time impairment in EBITDA depresses that name's multiple and drags the median toward a false-cheap read.
- **Blending trading and deal multiples.** Precedent multiples carry a control premium; averaging them with trading multiples double-counts control and inflates the range.
- **Peer set stuffing.** Padding the list with loosely related names to hit a count widens the range until it says nothing; a tight 6-8 name set beats a noisy 15.

## Output format
```
Target: <name> | Metric basis: LTM, calendarized to <date>
Target metrics: Revenue <..> | EBITDA <..> (<margin>) | Net debt <..> | Diluted shares <..>

Trading comps:
| Company | EV | EV/Rev | EV/EBITDA | EV/EBIT | P/E | PEG |
| Peer 1  | .. | ..x    | ..x       | ..x     | ..x | ..  |
| ...     |    |        |           |         |     |     |
| Median  |    | ..x    | ..x       | ..x     | ..x | ..  |
| Mean    |    | ..x    | ..x       | ..x     | ..x | ..  |

Implied valuation (EV/EBITDA, median):
Implied EV = <mult> x <EBITDA> = <..>
- net debt <..> - minority - preferred + cash = Implied equity <..>
/ diluted shares = Implied price <..>/share

Precedent transactions (control): median <mult>x -> equity <..> | <..>/share

Football field (per share): Trading <lo>-<hi> | Precedents <lo>-<hi> | DCF <lo>-<hi>
```

## Reference

### Enterprise value bridge
EV is what an acquirer effectively pays for the operating business, independent of how it is financed.

| Component | Sign | Note |
|---|---|---|
| Equity value (diluted) | + | Share price x diluted shares (treasury stock method) |
| Total debt | + | Short- and long-term borrowings, at face/market |
| Minority (non-controlling) interest | + | Share of consolidated subs not owned |
| Preferred equity | + | At liquidation/redemption value |
| Cash and equivalents | - | Includes short-term investments |
| = Enterprise value | | |

Bridge back the other way for implied equity: Implied equity = Implied EV - debt - minority - preferred + cash.

### Multiple formulas
| Multiple | Numerator | Denominator | Footing |
|---|---|---|---|
| EV/Revenue | Enterprise value | Revenue | Unlevered |
| EV/EBITDA | Enterprise value | EBITDA | Unlevered, pre-D&A |
| EV/EBIT | Enterprise value | EBIT | Unlevered, post-D&A |
| P/E | Price (or equity value) | EPS (or net income) | Levered/equity |
| P/B | Equity value | Book equity | Equity |
| PEG | P/E | EPS growth rate (%) | Growth-adjusted |
| EV/EBITDA-capex | Enterprise value | EBITDA - capex | Capital-intensity aware |

### When to use which multiple
| Situation | Preferred multiple | Why |
|---|---|---|
| Different leverage across peers | EV/EBITDA, EV/EBIT | Capital-structure neutral |
| Heavy, varied D&A | EV/EBIT | Captures capital intensity |
| Pre-profit / high-growth | EV/Revenue | EBITDA/EPS not meaningful yet |
| Banks, insurers | P/E, P/B | EV undefined; balance sheet is the business |
| Clean, mature, similar leverage | P/E | Direct to equity holders |
| Comparing across growth rates | PEG | Normalizes P/E for growth |

### Calendarization and LTM mechanics
Put every company on the same clock before comparing.

- Calendarize: to convert a June fiscal-year to calendar-year, take FY figures and add/subtract quarterly stubs so the window ends on the calendar date. Calendar-year estimate = FY + (fraction of next FY in the calendar year x next FY) - (fraction of prior FY outside the calendar year).
- LTM (trailing): LTM = latest fiscal year + latest interim stub - prior-year comparable interim stub. Example: LTM at Q3 = FY + 9M current - 9M prior.
- Forward: use consensus NTM (next-twelve-months) or fiscal-year-forward estimates; label the period so you never compare LTM to forward.

### Normalizing (non-recurring) adjustments
Add back or remove so multiples reflect run-rate economics; apply the same rule to every peer.

| Adjustment | Direction on EBITDA/EBIT | Notes |
|---|---|---|
| Restructuring/severance | Add back | One-time |
| Asset impairment/write-down | Add back | Non-cash, non-recurring |
| Litigation settlement | Add back | Unless recurring |
| Gain/loss on asset sale | Remove | Non-operating |
| Stock-based comp | Treat consistently | Add back only if all peers do |
| Transaction/deal costs | Add back | One-time |
| Change in accounting/one-off tax | Normalize | Reconcile to statutory rate |

### Precedent transactions
Deal multiples are computed the same way (EV / target metric at announcement) but embed a control premium and deal-specific synergies, so they run above trading comps.

| Concept | Definition |
|---|---|
| Control premium | (Offer price - unaffected price) / unaffected price; typically 20-40% |
| Deal EV | Offer equity value + target net debt at close |
| Synergy adjustment | Strip buyer-specific synergies to see standalone multiple |
| Timing/market context | Adjust for cycle; a peak-market deal overstates today's level |

### Checks
- [ ] Every EV built from a fully diluted, current share count.
- [ ] Numerator/denominator footing matches on every multiple (EV<->unlevered, equity<->levered).
- [ ] All peers calendarized to the same period; LTM vs forward never mixed.
- [ ] EBITDA/EPS normalized identically across the set.
- [ ] Outliers understood before trimming; exclusions labeled and justified.
- [ ] Median used as primary; mean shown only as a sensitivity (mean is outlier-sensitive).
- [ ] Trading and precedent ranges presented separately (control premium not double-counted).
- [ ] Implied equity bridged correctly from implied EV; per-share on diluted count.
