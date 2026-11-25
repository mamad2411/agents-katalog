---
name: fina-ib-check-deck
version: 1.0.0
description: Runs the classic investment-banking deck-check on a finished presentation, proofing cross-page number consistency, footnote sourcing, units and currency labels, rounding, chart-to-table agreement, math, and brand formatting before it goes out.
author: matrixx0070
tags: [finance, investment-banking, qc, proofing, deck-check, footnotes, formatting, sign-off]
capabilities: []
---

# Investment-Banking Deck Check

## When to use
Use this as the final proofing gate before a deck leaves the building: pitch, CIM, board, or fairness materials that are content-complete and need the standard IB deck-check for consistency, sourcing, units, rounding, math, and brand compliance. This is the "check the deck before it goes out" pass, run after the content is done, not while it is being written.

**Not for:** building the numbers or storyline (use fina-pptx-author), bringing a stale deck current (use fina-deck-refresh), or creating the template (use fina-ppt-template-creator). Errors traced to the analysis go back to fina-comps-analysis, fina-dcf-model, or fina-3-statement-model to fix at the source, not on the slide.

## Method
1. **Establish the source of truth.** You confirm which model and data pull the deck is supposed to tie to and get the as-of dates; every check reconciles against this, not against another slide. Decision point: if there is no traceable source model, you stop the check and send it back — you cannot proof numbers you cannot tie out.
2. **Sweep numbers for cross-page consistency.** You list every figure that appears more than once (revenue, EBITDA, transaction value, share count, multiples) and confirm each instance agrees to the same rounding across the whole deck.
3. **Enforce "no page left un-footnoted."** You verify every exhibit carries a source footnote with a provider and an as-of date; a slide with data and no source fails the check.
4. **Check units, currency, and scale.** You confirm each number states its unit ($mm, $bn, %, x, bps), currency, and scale, and that mixed-currency or mixed-scale exhibits are labeled and reconciled.
5. **Verify rounding consistency.** You confirm decimal places are consistent within each metric class (e.g., multiples to one decimal, margins to whole or one-tenth percent) and that rounded components still foot to the rounded total.
6. **Reconcile charts to tables.** You confirm each chart's plotted series equals its underlying table row and that axis scales are not truncated or dual-scaled in a way that distorts the message.
7. **Run the math checks.** You re-derive growth rates, CAGRs, margins, percentage splits (do they sum to 100%?), multiples, and per-share figures; you recompute rather than trust the label.
8. **Check identity and metadata.** You verify the correct company name, project code name, logos, deal date, and confidentiality legend appear and that no placeholder or prior-deal name survived. Decision point: if any wrong-client or wrong-project artifact is found, you escalate immediately and hold the deck regardless of other findings.
9. **Check formatting and brand compliance.** You confirm fonts, colors, alignment, table styling, and page numbers match the fina-ppt-template-creator master.
10. **Log findings and drive sign-off.** You record every finding with severity, route fixes to the owner, re-check fixed items, and issue the turn/sign-off record.

## Example
You receive a 22-slide pitch for "Project Meridian." Sweeping numbers, you find revenue shown as $1,204mm on slide 6 and $1.2bn on slide 14 — consistent in value but you flag the scale mismatch for one convention. Slide 9's pie chart segments sum to 101% (rounding), so you adjust one segment to force 100%. Slide 11's bar chart plots EBITDA of $310mm but the table beneath reads $301mm — a real chart-to-table break, flagged HIGH. Slide 17 has a comps table with no source footnote — flagged HIGH under "no page un-footnoted." The footer on slide 3 still says "Project Cascade" from the prior pitch — flagged CRITICAL, deck held until fixed. You log 9 findings (2 critical/high identity+sourcing, 4 medium, 3 low), route them, re-check, and sign off.

## Pitfalls
- **Un-footnoted exhibit.** A data slide with no source invites a "where's this from?" in the room; require a provider and as-of date on every exhibit.
- **Chart-table divergence.** A chart drawn from a stale paste while the table was updated shows two different numbers for one fact; reconcile every chart to its table row.
- **Rounding that does not foot.** Rounded line items that sum to a different rounded total look like an error to any client; check that components foot after rounding.
- **Wrong-deal artifact.** A leftover client or project name from the last pitch is an instant credibility loss; scan every footer, cover, and header for stale identity.
- **Percentages that miss 100%.** Splits that sum to 99% or 101% signal sloppiness; force segments to total exactly 100% and note the rounding.
- **Mixed units unlabeled.** Switching between $mm and $bn or reported and adjusted without labels misleads; label unit, currency, and adjusted/reported on every figure.
- **Distorted axes.** Truncated or dual-scaled chart axes overstate a trend; check that scale honesty matches the intended message.

## Output format
```
DECK CHECK — Project Meridian Pitch (v5)  |  Checker: <you>  |  Ties to: Meridian_Model_v12
Status: HOLD (1 critical open)

FINDINGS
ID   Sev       Slide  Category         Finding                                   Owner   State
F1   CRITICAL  3      Identity         Footer reads "Project Cascade"            Analyst OPEN
F2   HIGH      11     Chart-vs-table   Chart EBITDA $310mm vs table $301mm       Analyst FIXED
F3   HIGH      17     Sourcing         Comps table has no source footnote        Analyst FIXED
F4   MEDIUM    9      Math             Pie segments sum to 101%                   Analyst FIXED
F5   MEDIUM    6/14   Units            $1,204mm vs $1.2bn scale mismatch         Assoc   OPEN
F6   LOW       ...    Formatting       Slide 12 title misaligned 4pt             Assoc   FIXED

SUMMARY: 1 critical, 2 high, 2 medium, 1 low  |  4 fixed, 2 open
SIGN-OFF: withheld until F1 and F5 cleared and re-checked.
```

## Reference

### Deck-check checklist by category
| Category | Checks |
| --- | --- |
| Numbers / consistency | Repeated figures agree across pages; totals foot; subtotals roll up |
| Sourcing / footnotes | Every exhibit sourced with provider + as-of date; no page un-footnoted |
| Labels / units | $ scale, currency, %, x, bps stated; adjusted vs reported labeled |
| Rounding | Consistent decimals per metric class; components foot to rounded total |
| Charts | Chart series equals table row; axes not truncated/dual-scaled misleadingly |
| Math | Growth, CAGR, margins, splits sum to 100%, multiples, per-share re-derived |
| Identity / metadata | Company name, project code, logos, date, confidentiality legend correct |
| Formatting / brand | Fonts, colors, alignment, table style, page numbers match master |

### Common errors and what they signal
| Error | Root cause | Fix |
| --- | --- | --- |
| Chart differs from table | Stale chart paste | Relink chart to current table row |
| Split sums to 99/101% | Independent rounding | Force largest segment to close to 100% |
| Two values for one metric | No single source of truth | Reconcile both to source model cell |
| Missing footnote | Rushed exhibit build | Add provider + as-of date |
| Wrong project name | Copied prior deck | Scan all covers/footers/headers |
| Unlabeled currency | Multi-region data | Label currency + FX date per figure |

### Severity and turn process
| Severity | Definition | Gate |
| --- | --- | --- |
| Critical | Wrong client/deal, legal/confidentiality, sign error | Deck held until cleared |
| High | Number wrong, chart-table break, missing source | Fix before send |
| Medium | Rounding, unit label, math cosmetics | Fix this turn |
| Low | Alignment, spacing, typography | Fix if time permits |

### Tie-out to underlying model
| Item | Reconciles to |
| --- | --- |
| Financials on slide | Named cell in fina-3-statement-model |
| Multiples / peer set | fina-comps-analysis output |
| Valuation ranges | fina-dcf-model output |
| Market data | Single stated market close |
