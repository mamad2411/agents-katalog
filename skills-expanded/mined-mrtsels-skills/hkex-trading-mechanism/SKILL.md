---
name: hkex-trading-mechanism
description: Use for HKEX securities trading mechanism research.
metadata:
  source_frontmatter:
    version: 1.0.0
  imported_from: hermes
---

# HKEX Securities Trading Mechanism Research

Research HKEX (Hong Kong Exchanges and Clearing) securities-market rules from OFFICIAL sources only (hkex.com.hk pages + official info-book PDFs). Every fact must carry its hkex.com.hk source URL; never invent numbers — mark unverifiable facts `UNVERIFIED` explicitly.

## CRITICAL PITFALL: HKEX site redesign broke legacy URLs

The old URL scheme (`/Services/Trading/Securities/Overview/Trading-Hours`, `.../Order-Types`, `.../Volatility-Control-Mechanism`, `.../Securities-Breakers`, `.../Special-Arrangements`, `.../Price-Bands`, `.../Tick-Sizes`) ALL return a ~2.9 KB "page relocated, renamed or removed" stub. Task briefs and older docs carry these dead links — resolve them first.

- **Discovery key**: the Trading Mechanism hub page is still live and links to every sub-page + official PDF info book:
  `https://www.hkex.com.hk/Services/Trading/Securities/Overview/Trading-Mechanism?sc_lang=en`
- Extract its links with `re.findall(r'href="([^"]+)"', content)` and filter by keyword.
- Current working URLs and the full verified fact bank: see `references/hkex-trading-mechanism-facts.md`.

## Workflow

1. **Fetch** with curl + Mozilla UA (pages are server-rendered, ~300–500 KB, plain curl works):
   `curl -s -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" "<url>" -o out.html`
2. **Strip nav noise** with python: remove `<script>`/`<style>` blocks → strip tags → `html.unescape` → collapse whitespace; locate content by keyword anchors (e.g. "Pre-opening Session").
3. **PDFs** (official info books are the richest sources): `pip install pymupdf`; `fitz.open()` → `page.get_text()` per page. Text extraction is clean.
4. **Search**: Google/Bing are often Cloudflare-blocked; DuckDuckGo html endpoint works: `https://html.duckduckgo.com/html/?q=site:hkex.com.hk+<terms>`.
5. **Verify, don't invent**: cite exact URL per fact; if a page 404s, find the renamed page via the hub or site search before writing anything.

## Key verified facts (condensed — full detail in the reference file)

- **Trading hours**: POS 9:00–9:30; CTS Morning 9:30–12:00, Extended Morning 12:00–13:00 (N/A half-day), Afternoon 13:00–16:00; CAS 16:00 to random close 16:08–16:10 (half-day 12:00–12:08/12:10). Half-days = eves of Christmas/New Year/Lunar New Year.
- **POS periods**: Order Input 9:00–9:15 (±15% prev close, amend/cancel OK) → No-cancellation 9:15–9:20 (Stage 2 limits = highest bid & lowest ask at 9:15) → Random Matching 9:20–9:22 (random) → Blocking to 9:30. Matching at final IEP, priority AO → ALO → price → time.
- **CAS periods**: Reference Price Fixing 16:00–16:01 (median of 5 snapshot nominal prices @15s from 15:59:00) → Order Input 16:01–16:06 (±5% of Reference Price) → No Cancellation 16:06–16:08 → Random Closing 16:08–16:10. No IEP → Reference Price becomes closing price.
- **Order types**: POS/CAS accept ONLY at-auction (AO) and at-auction limit (ALO) orders; limit/enhanced limit/special limit/odd lot/special lot rejected in CAS (those are the CTS types).
- **VCM**: dynamic price limit vs last automatch trade 5 min ago; thresholds HSCI LargeCap ±10% / MidCap ±15% / SmallCap ±20%; SPAC Shares ±30% (±15% 1st month); SPAC Warrants ±50% (±25% 1st month); eligible ETFs/−1× ±5%; 2×/−2× ±10%. 5-min cooling-off, multiple triggers allowed. NOT applied in POS/CAS, not in first 15 min of CTS, not in last 20 min of day. No exchange-wide daily limit up/down for HK stocks.
- **Severe weather**: Typhoon Signal 8+/Black Rainstorm/Extreme Conditions → trading CONTINUES (both markets).
- **Tick sizes**: full table NOT re-verified in Aug 2026 — the old Tick-Sizes URL 404s; go via Trading-Mechanism hub → `Reduction-of-Minimum-Spreads` page. Do not quote the well-known table from memory without an hkex.com.hk source.

## Pitfalls

- Never quote the tick-size table or CTS order-type semantics without a live hkex.com.hk page — flag UNVERIFIED.
- Bing/Google searches on the topic get Cloudflare-challenged; use DuckDuckGo html or HKEX site search.
- HKEX info books carry version dates (e.g. 10 Apr 2026, 3 May 2022) — cite them; rules change over time (e.g. CAS expanded Oct 2019, enhanced POS Oct 2020, VCM tiering May 2020).
