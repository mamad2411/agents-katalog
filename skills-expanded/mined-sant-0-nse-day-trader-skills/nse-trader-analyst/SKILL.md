---
name: nse-trader-analyst
description: Indian Earnings Analyst. Reads consolidated quarterly revenue, net profit, EPS and margins from Screener.in, computes QoQ, YoY and TTM changes, and falls back to official NSE result-filing links rather than inventing data. Use when the user says "analyze RELIANCE results", "how were TCS earnings", "quarterly result kaisa tha", "revenue growing?", "compare margins", or before trading an Indian stock around results.
---

# nse-trader-analyst

Reads reported Indian-company numbers quarter by quarter: revenue, net profit,
EPS, operating margin and calculated net margin, with QoQ, YoY and trailing
twelve months. Primary source is Screener.in's consolidated table. If parsing
fails, it lists official NSE result PDFs and leaves the numeric fields empty.
It never fills gaps with estimates.

## Run it

```bash
python scripts/facts.py --ticker RELIANCE
python scripts/facts.py --ticker TCS --screener
```

`--screener` is optional because Screener is already the primary source; it is
kept so automated workflows can state the source explicitly.

Example report fields:

| Metric | Unit / comparison |
|---|---|
| Revenue | Rs crore; QoQ and same-quarter YoY |
| Net profit | Rs crore; QoQ and YoY |
| EPS | rupees per share |
| OPM | reported operating margin % |
| Net margin | calculated net profit / revenue % |
| TTM | sum of latest four reported quarters |

## Source discipline

- Consolidated results are used when Screener provides them.
- The page's displayed periods and units are preserved.
- Missing cells remain `null` / `N/A`.
- If the HTML table changes or the ticker is absent, the script searches NSE
  corporate announcements for results links. It says that the PDF must be read
  or pasted; it does **not** infer the numbers from a headline.
- Always open the company filing for audit-sensitive decisions.

## Earnings-call transcripts

If the user pastes a transcript, summarize separately:

1. management guidance and changes from the previous call
2. demand, pricing, margin and capex commentary
3. explicit risks and unanswered analyst questions
4. contradictions between management language and filed numbers

Label quoted management claims as claims, not facts, unless reconciled to a
filing.

## Files

| File | What |
|---|---|
| `nse-trader/facts.json` | all parsed quarters, TTM and source notes |
| `nse-trader/facts.md` | short human-readable report |

Results can cause gaps and circuit moves. Analysis is educational and not a
recommendation to trade before or after earnings.
