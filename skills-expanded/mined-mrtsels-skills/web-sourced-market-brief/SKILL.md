---
name: web-sourced-market-brief
description: Use for sourced briefs on current market/macro conditions.
version: 1.0.0
---

# Web-Sourced Market/Macro Brief

Produce a factual brief on CURRENT market/macro conditions (Fed policy, rates, CPI/payrolls, yields, sell-side views) where **every number is sourced to a URL that was actually fetched** — never from memory. Trigger: "brief on ... as of <date>", "what did the Fed do", "market pricing for ...", "sourced summary of ...".

## Workflow

1. **Fetch → file → grep** (never dump whole pages into context):
   ```bash
   curl -s -m 120 -A "Mozilla/5.0" "https://r.jina.ai/https://<target-url>" -o /tmp/page.txt
   grep -n -i "<key terms>" /tmp/page.txt | head -40
   ```
   The `r.jina.ai/` prefix renders any page to markdown; works on federalreserve.gov, bls.gov, cnbc.com, foxbusiness.com, goldmansachs.com, frbsf.org. Use `head -c 4000` to preview before full fetch.
2. **Primary sources first**: Fed/BLS/FRED pages over news. Use news (CNBC/Fox/Reuters/AP) for presser quotes, market color, sell-side strategy commentary, and FedWatch numbers.
3. **Verify regime facts against primary sources** before trusting the task's assumptions (chairs change, policy regimes flip). If the task says "Powell presser" and sources say a different chair, report reality, note the discrepancy.
4. **Every figure carries a source URL + as-of date** (numbers drift between snapshots — e.g. FedWatch right-after-decision vs next day differ). Anything not verifiable: mark **UNVERIFIED** and state what was found instead.
5. Deliver ONLY the brief (markdown, respect word budget), with a compact numbered source list; cite inline.

## Verified technique stack

- **FRED CSV, no API key**: `curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>" | tail -6`. Key series: DGS10 (10Y yield), T10YIE (10Y breakeven), DFF (effective fed funds), UNRATE, PAYEMS (nonfarm k, monthly diff = jobs added).
- **CME FedWatch page is JS-only**: r.jina.ai returns an empty shell; browser may fail with ERR_HTTP2_PROTOCOL_ERROR. Use server-rendered third-party mirrors (rateprobability.com/fed, centralbank.watch, fedwatch.com — label as mirror, note "cached") and news articles quoting FedWatch for the headline meeting.
- **⭐ Fed pricing → Atlanta Fed Market Probability Tracker FIRST** (`atlantafed.org/research-and-data/data/market-probability-tracker`): authoritative (CME SOFR options, daily), server-rendered, browser-readable — hike/cut odds per meeting + target-range distribution + expected 3M SOFR path. **rateprobability.com mirrors can serve MONTHS-OLD caches** (priced cuts while reality priced hikes; `/fed` stale while `/ecb` fresh on the same visit) — detect via rows for past meetings contradicting actual outcomes, or direction flips vs the SR3 strip/MPT, and never trust a mirror un-cross-checked. Details + SOFR-path derivation in `references/us-macro-source-patterns.md`. ⚠️ The official `mpt_histdata.xlsx` is UNREADABLE by openpyxl (corrupted drawing refs → `KeyError: xl/drawings/drawing2.xml`); parse the sheet XML + sharedStrings directly — the DATA sheet is long-format (date / reference_start Excel-serial / target_range / field / value; fields `Rate: mean`, `Rate: 25th percentile`, `Prob: hike`, `Prob: various 25bps ranges`) — see `scripts/extract_mpt_path.py`.
- **URL discovery**: `curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=<query>"`, then extract links with `grep -o 'uddg=[^"&]*'` + urllib.parse.unquote (see references file for the one-liner).
- **Fetch in parallel batches** (independent sources in one block), serialize only when a later fetch depends on an earlier result.

## Pitfalls

- Reuters live blogs often return a ~700-byte stub via r.jina.ai — fall back to Fox/CNBC/AP coverage of the same event.
- State the as-of date for every probability/price; don't blend snapshots (e.g. 57.2% vs 62.4% Sep hike odds are different days).
- When markets price the OPPOSITE of the task's assumption (cuts vs hikes), trust the fetched data, not the brief's premise.
- Sell-side views: fetch the house's own insight page (e.g. goldmansachs.com/insights) + strategy-quote roundups in CNBC/Fox coverage; name the strategist.
- **ECB + some FRED series block bots**: ECB data-api / sdw-ws REST and FRED's `EURIBOR3MD156N` / `EURESTR` return bot-challenge HTML to curl (most other FRED graphfred.csv series work fine; don't hammer retries). Workarounds: EURIBOR 3M from euribor-rates.eu (current-rates page has ~10 daily rows; by-year pages have monthly tables), €STR level from the rateprobability.com/ecb page header.

## References

- `references/us-macro-source-patterns.md` — concrete URL patterns for Fed/BLS/FRBSF/CME and a worked example (July 2026 FOMC brief): what worked, what failed, snapshot drift.
