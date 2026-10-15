---
name: boi-economic-data
description: "Fetch and analyze Bank of Israel (BOI) economic data: interest rates, CPI (madad hamchirim), exchange rates (sha'ar yatzig), and CBS statistics. Use when user asks about BOI interest rate, ribit Bank Israel, exchange rates, sha'ar yatzig, CPI index, madad, inflation data, or Israeli economic indicators. Foundation skill for Israeli financial analytics. Provides API access to the BOI SDMX API at edge.boi.gov.il and CBS data. Do NOT use for stock market data (use tase-stock-analysis instead) or for currency conversion (use shekel-currency-converter instead)."
license: MIT
compatibility: "Requires network access for Bank of Israel API. Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI."
---

# BOI Economic Data

## Instructions

### Step 1: Identify the Data Type
Ask the user what economic data they need:

| Data Type | Hebrew | Source | Update Frequency |
|-----------|--------|--------|--------|
| Interest rate | ריבית בנק ישראל | BOI Monetary Committee | 8 scheduled decisions in 2026, announced at 16:00 |
| Exchange rates | שערי חליפין (שער יציג) | BOI | Business days Mon-Fri, soon after 15:15 (12:15 on Fridays and holiday eves) |
| CPI (Consumer Price Index) | מדד המחירים לצרכן | CBS (Lishkat HaStatistika) | Monthly (around 15th of following month) |
| Inflation expectations | ציפיות אינפלציה | BOI | Monthly |
| Government bonds yield | תשואת אג"ח ממשלתי | BOI / TASE | Daily |
| Monetary aggregates | אגרגטים מוניטריים | BOI | Monthly |

### Step 2: Fetch Data from the BOI and CBS APIs
The Bank of Israel serves public data from its "new series database" (Fusion Edge Server) using the SDMX 2.1 REST API. Two data paths are live and return the same observations:

```
https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/{DATAFLOW}/{series}
https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/{DATAFLOW}/1.0/{series}
```

Both accept `format=csv` as well as the default SDMX-XML. Observations arrive as `<Obs TIME_PERIOD="..." OBS_VALUE="..." RELEASE_STATUS="..."></Obs>` elements, with the series metadata as attributes on the enclosing `<Series>`. Always send an explicit `User-Agent`. The canonical endpoint reference is `references/boi-api.md`.

**Bound every query.** A bare dataflow query with no date filter returns every series in the dataflow with its full history: `.../data/EXR/` is roughly 20 MB across 35 series going back to 1948. Name the series, or add `startPeriod` / `endPeriod`, or use `lastNObservations`. A date-bounded dataflow query is genuinely useful when you want every currency at once (`.../data/EXR/?startPeriod=2026-08-26&endPeriod=2026-08-26` returns that day's series in a few kilobytes). The dataflow also holds series that are not exchange rates: the trade-weighted basket `NER_ILS_BSK_*`, implied-volatility `WEB_STD_IMPVOL_*`, and `RER_USD_ILS_GLBLIMP` / `RER_USD_ILS_LCLIMP`, which share the `RER_` prefix but have `UNIT_MEASURE="NBRE"`. Keep only series named exactly `RER_<CUR>_ILS` with `DATA_TYPE="OF00"`.

**Exchange Rates (Sha'ar Yatzig):** representative rates live in the `EXR` dataflow as per-currency series `RER_<CUR>_ILS` (e.g. `RER_USD_ILS`, `RER_EUR_ILS`):
```
GET .../data/EXR/RER_USD_ILS?startPeriod={date}&endPeriod={date}
```

**Interest Rate:** the Bank of Israel policy rate (ribit Bank Israel) is the `BR` dataflow, daily series `MNT_RIB_BOI_D`:
```
GET .../data/BR/MNT_RIB_BOI_D?startPeriod={date}
```
Do NOT use the `BIR` dataflow for this. `BIR` is "ריביות וביצועים - לא לדיור", commercial-bank credit rates excluding housing loans. It resolves and returns data, so querying it fails silently by answering a different question.

**CPI:** the headline index comes from the CBS index API, not from the BOI. See Step 4.

**Fetching only the latest value:** use `lastNObservations=1`. Do NOT use `lastNPeriods`, which the BOI server accepts, answers HTTP 200 for, and silently ignores, returning the entire series back to 1948.

Use `scripts/fetch_boi_rates.py` for all three data types.

### Step 3: Process Exchange Rate Data
BOI publishes representative exchange rates (sha'ar yatzig) daily:

| Currency | Code | Typical Use |
|----------|------|-------------|
| US Dollar | USD | Primary foreign currency, investment pricing |
| Euro | EUR | EU trade, travel |
| British Pound | GBP | UK trade |
| Japanese Yen | JPY | Per 100 JPY |
| Swiss Franc | CHF | Safe haven |

Key points:
- Representative rate calculated once per business day, Monday to Friday, and published soon after 15:15 (soon after 12:15 on Fridays, holiday eves and some other Jewish holidays). The BOI says the time is not fixed. No rate on Saturday or Sunday (Friday is a publication day, and the BOI series shows the same Monday-Friday pattern in 2015, 2023 and 2025, so it holds for historical dates too), on Israeli holidays, or on Christmas Day, New Year's Day and Easter, when most foreign-exchange markets are closed. The BOI also reserves the right not to publish on other days (there is no rate for Friday 26 December 2025), so never model the calendar: take the last rate published on or before the date (`--date YYYY-MM-DD`)
- Its force comes from whatever adopts it. The BOI states the representative rates have no official or legal standing of their own and are used mainly for valuations and in contracts; between contracting parties a representative rate binds only when stipulated, and the contract decides which date's rate applies. Statutes adopt it too: the Income Tax (Inflationary Adjustments) Law, for example, defines the exchange rate for a date as the BOI representative dollar rate published that day, or the last one published before it (that law applied mainly to tax years 1985-2007, so treat it as an illustration of how a statute adopts the rate, not as the rule for a current year). So ask which rule governs (the contract, or the tax or accounting rule the user is applying) and use that rule's date and fallback
- For a date with no published rate, the usual fallback is the last published rate, but a contract may name a different one (the rate on the transaction date, or on a set date before or after it)
- **Annual average and year-end rate:** the BOI EXR dataflow has no annual or monthly average series for individual currencies. The usual method is the simple mean of the rates published in the year, without filling in non-publication days (`--from 2025-01-01 --to 2025-12-31 --average`: 246 published USD rates in 2025, mean 3.4529). The year-end rate is the last rate published on or before 31 December (3.19 on 2025-12-31). Whether an average is acceptable for a given report is that reporting rule's decision
- For intraday rates, use forex platforms (BOI rate is indicative)

### Step 4: Analyze CPI Data
The headline Consumer Price Index (Madad HaMchirim LaTzarchan) is published by the CBS and is available from its index API as index id `120010` ("מדד המחירים לצרכן - כללי"):

```
GET https://api.cbs.gov.il/index/data/price?id=120010&format=json&last=6
```

The response carries, per month, the index value, its base period (`baseDesc`), the monthly change (`percent`) and the year-on-year change (`percentYear`). For specific months use `startPeriod` / `endPeriod` in `mm-yyyy` form (`&startPeriod=01-2019&endPeriod=03-2019`). Add `coef=true` to get `prevBase`: the same month restated on every earlier base through the CBS chaining coefficients.

**Each month is published on the base that was current at the time.** January 2019 comes back as 100.1 on base "2018 ממוצע", August 2026 as 105.8 on base "2024 ממוצע". Dividing those two raw values is wrong. Compare on the OLDER month's base, which the newer month carries in its `prevBase` (August 2026 on base 2018 is 120.6943227684), or let `fetch_boi_rates.py --cpi` do it: its "On <base>" column restates every row on the oldest row's base.

**Responses are paged at 100 months** (`paging.last_page`, `paging.next_url`). A wider range or `last` above 100 needs every page, or the oldest months, usually the contract's base month, silently go missing.

**Validate the payload, not the status code.** This API answers HTTP 200 with `"month": null` for an unknown index id, and HTTP 200 with an HTML error page for an undefined path. A caller that checks only the status code will treat both as success.

**The BOI `PRI` dataflow is not the headline CPI.** `PRI` carries BOI price-index and analytical series on different bases and scopes; its `CP000000` series is not the published מדד. Use the CBS API for any figure a user will rely on.

CPI components tracked by the CBS include housing (דיור, the rent component rather than home prices), food (מזון), transport (תחבורה), education and culture (חינוך ותרבות), health (בריאות), and clothing and footwear (הלבשה והנעלה). Basket weights are revised periodically; read them from the CBS basket publication rather than assuming.

CPI uses:
- **CPI-linked bonds (Galil):** Index-linked government bonds adjust by CPI
- **Rent adjustments:** Many Israeli leases are CPI-linked (tzmud madad)
- **Alimony and legal judgments:** Often CPI-linked

**Linkage (hatzmada) has conventions that change the answer.** Before computing any adjustment, settle three things:
- **Madad yadua or madad bagin?** *Madad bagin* month X is the index *for* X, published around the 15th of X+1. *Madad yadua* on a given date is the last index *published* by then. Contracts name one; using the other shifts the base by a month or two. The CBS linkage calculator treats month X as known from the 16th of X+1: a date of 15 March 2019 resolves to the January 2019 index and 16 March to February. Where the contract's own wording differs, the contract governs.
- **Which base period?** The current CBS base is the 2024 average. An index quoted on an older base cannot be divided by one on the current base without the CBS linking coefficient.
- **Is there a floor clause (taniyat ritzpa)?** Many Israeli linkage clauses do not reduce the payment when the index falls. The raw formula yields a negative adjustment; the contract may not allow it.

**For linking an amount by date, the CBS calculator looks up the index known on each date and handles the rebase itself:** `https://api.cbs.gov.il/index/data/calculator/120010?value=1000&date=03-15-2019&toDate=10-12-2026&format=json` (dates `mm-dd-yyyy`) returns the known index on each date, the chaining coefficient and the result (here January 2019 at 100.1 to August 2026 at 105.8, 1000 becomes 1205.74, +20.6%). It answers HTTP 500 for a `toDate` in the future. It always applies madad yadua: for a madad-bagin contract measuring month X, pass a date between the 16th of X+1 and the 15th of X+2. It ignores floor clauses and the contract's adjustment schedule.

Note: CPI is typically published around the 15th of the following month; verify against the CBS release calendar.

### Step 5: Track Interest Rate Decisions
BOI Monetary Committee sets the interest rate. In 2026 it has 8 scheduled decisions, announced at 16:00, and each takes effect on a later date (announced 1 September 2026, effective 3 September). The BR series and the script's change points carry the EFFECTIVE date, which is also when prime moves. Check the next decision date on the BOI schedule (https://www.boi.org.il/en/economic-roles/monetary-policy/interest-rate-announcement-dates-2026/) before telling a user what prime will be next month.

**The policy rate is not the borrower's rate.** Variable-rate ("prime" / פריים) mortgages and most consumer credit are priced at the Bank of Israel rate plus a fixed spread set by banking convention, and then plus or minus the borrower's own margin. Never quote the policy rate to a user as the interest they pay. Read the current prime from the bank's published prime rate, and state the policy rate only as the thing prime moves with. The spread is a bank convention, not a published BOI series: Bank Hapoalim and Mizrahi-Tefahot both state prime as the Bank of Israel rate plus 1.5% (checked October 2026). Quote 1.5% as the current convention, not as a rule, and still take the figure from the bank's own published prime.

| Rate Level | Typical Context | Impact |
|------------|----------------|--------|
| Rising | Inflation above target (1-3%) | Higher mortgage rates, stronger NIS |
| Stable | Inflation within target | Predictable borrowing costs |
| Falling | Low inflation or economic slowdown | Lower mortgage rates, weaker NIS |

For the current rate and the dates it last changed, run `python scripts/fetch_boi_rates.py --interest`, which reads the daily `BR/MNT_RIB_BOI_D` series and prints each change point. The Monetary Committee's reasoning, and the accompanying minutes, are on the BOI press-releases / monetary-policy pages (see Reference Links).

### Step 6: Combine Data for Analysis
Cross-reference multiple data points for comprehensive analysis:
1. **Mortgage planning:** Interest rate + CPI trend + exchange rate outlook
2. **Business planning:** Exchange rate + CPI for cost projections
3. **Investment analysis:** Bond yields + inflation expectations
4. **Import/export pricing:** Exchange rates + CPI for contract negotiations

## Examples

### Example 1: Current Exchange Rate
User says: "What is today's dollar-shekel exchange rate?"
Actions:
1. Run `python scripts/fetch_boi_rates.py --currency USD`
2. Display representative rate (sha'ar yatzig) with date
3. Note: rate published soon after 15:15 Mon-Thu and soon after 12:15 Fri; before that (or on Sat/Sun or a non-publication holiday), the last published business-day rate is the latest available
Result: Current USD/NIS representative rate with context

### Example 2: Interest Rate Impact
User says: "What is the current BOI interest rate and how does it affect mortgages?"
Actions:
1. Run `python scripts/fetch_boi_rates.py --interest`
2. Show the current rate and the dates it changed (both come from the BR series)
3. Explain: variable-rate (prime) mortgages move with this rate, but the borrower's actual rate is prime, which is the policy rate plus the banks' spread (1.5% by current convention) plus the borrower's own margin. Point the user at their bank's published prime rather than quoting the policy rate as their rate
4. Note: Fixed-rate mortgages set at time of signing, not affected by changes
Result: Interest rate with mortgage impact analysis

### Example 3: CPI Trend for Rent Adjustment
User says: "My lease says rent adjusts by CPI. How much did it go up?"
Actions:
1. Determine: Lease start date and adjustment schedule (most leases adjust at set dates, such as yearly or at renewal, not continuously)
2. Confirm the convention: does the lease say madad yadua or madad bagin, and does it name a base MONTH or a base index VALUE (e.g. "101.2 points, base 2016 average")? For madad yadua, map each date to the month known on it (month X is known from the 16th of X+1)
3. Fetch: `python scripts/fetch_boi_rates.py --cpi --cpi-from MM-YYYY --cpi-to MM-YYYY` from the base month to the adjustment month. If the lease names a value, start the range at a month published on that base and check the value matches that row's Index before using the "On <base>" column. Cross-check with the CBS calculator (Step 4)
4. Calculate: Percentage change = (CPI_current - CPI_base) / CPI_base * 100, with BOTH values on the same base (the script's "On <base>" column, never the raw Index column across a rebase)
5. Apply: New rent = original_rent * (1 + percentage_change / 100), unless a floor clause blocks a decrease
Result: CPI adjustment computed on the convention the lease actually names

## Bundled Resources

### Scripts
- `scripts/fetch_boi_rates.py` -- Fetches representative exchange rates (`--currency USD`; `--latest` for the newest rate; `--date YYYY-MM-DD` for the rate on a date or the last one before it; `--from`/`--to` for a range, with `--average` for its simple mean), the BOI policy rate (`--interest`, widen the change-point scan with `--interest-days`), and the CBS CPI (`--cpi`, reach an older base month with `--cpi-from MM-YYYY --cpi-to MM-YYYY` or `--cpi-last N`, reading every page of a long range). `--json` carries the quotation unit alongside the observations, so a per-100 currency cannot be misread; for `--cpi` it also carries the bases in the range, whether the requested end month is still unpublished, and whether every page arrived. Transient connection resets are retried before it gives up; a TLS certificate failure is reported as a local CA-bundle problem and is never retried or bypassed. Exits non-zero when a source is unreachable or returns no observations, so it never presents placeholder numbers as data. `--example` prints clearly-labelled sample output. Run: `python scripts/fetch_boi_rates.py --help`

### References
- `references/boi-api.md` -- Bank of Israel API endpoints (SDMX format), authentication, rate limits, and data structure. Consult when building integrations or troubleshooting API calls.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| BOI Data and Statistics | https://www.boi.org.il/en/economic-roles/statistics/ | Official portal for interest rates, exchange rates, monetary aggregates |
| BOI interest-rate announcement dates 2026 | https://www.boi.org.il/en/economic-roles/monetary-policy/interest-rate-announcement-dates-2026/ | The 8 scheduled decisions, publication time (16:00) and each decision's effective date |
| BOI SDMX data API root | https://edge.boi.gov.il/FusionEdgeServer/ws/public/sdmxapi/rest/data/ | Live data path used by `scripts/fetch_boi_rates.py`. Append a dataflow AND a series, e.g. `EXR/RER_USD_ILS` or `BR/MNT_RIB_BOI_D` |
| BOI dataflow list (structure API) | https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/structure/dataflow/BOI.STATISTICS | Dataflow ids: `EXR` rates, `BR` policy rate, `PRI` price indices, `ZCM` inflation expectations and zero curve, `MAG` monetary aggregates, `TLB` Telbor |
| CBS index API (CPI) | https://api.cbs.gov.il/index/data/price?id=120010&format=json&last=6 | Headline CPI value, base period, monthly and year-on-year change |
| BOI Press Releases | https://www.boi.org.il/en/communication-and-publications/press-releases/ | Most recent Monetary Committee rate decisions and accompanying minutes |
| BOI explanatory notes on the representative rates | https://www.boi.org.il/en/economic-roles/financial-markets/explanatory-notes-to-the-representative-exchange-rates/ | Legal standing (none of its own), non-publication days including Christmas Day, New Year's Day and Easter, sampling window, publication time |
| CBS Consumer Price Index | https://www.cbs.gov.il/en/subjects/Pages/Consumer-Price-Index.aspx | Current monthly CPI release schedule, historical index, weighting structure |

## Gotchas
- Agents often query BOI exchange rates for Saturday or Sunday, but the representative rate (sha'ar yatzig) is only published Monday-Friday, and has been for years, so for a weekend the last rate is normally Friday's, not Thursday's, for historical dates too. Agents that only skip weekends and Jewish holidays also miss Christmas Day, New Year's Day, Easter and other unannounced gaps (Friday 26 December 2025 has no rate). Ask for the last rate on or before the date instead of computing which day to use.
- The BOI SDMX API returns XML by default. Add `format=csv` for a flat table; the observation values are identical either way.
- Agents routinely reach for the `BIR` dataflow for the BOI interest rate because of the name. `BIR` is commercial-bank credit rates; the policy rate is `BR/MNT_RIB_BOI_D`. Both return HTTP 200, so the mistake surfaces as a plausible wrong number rather than an error.
- `lastNPeriods` looks like it works on the BOI API and does not: the server returns HTTP 200 and the full series back to 1948. Use `lastNObservations`.
- The CBS index API returns HTTP 200 for an unknown index id (with `"month": null`) and for an undefined path (with an HTML body). Agents that branch on the status code will treat a failed CPI lookup as a success.
- `api.cbs.gov.il` intermittently resets the connection under repeated automated requests (curl exit 56, no HTTP status at all). This is transient, not a dead endpoint. Retry with a short backoff rather than concluding the API is gone or switching to a different index id.
- Agents may confuse the BOI representative rate (indicative, published once per business day, soon after 15:15 Mon-Thu and 12:15 Fri) with real-time forex rates. The BOI rate is not suitable for intraday trading decisions.
- CPI data from CBS lags by about 6 weeks: January's CPI is published around February 15th. Agents may try to fetch current-month CPI that does not exist yet.

## Troubleshooting

### Error: "BOI API returned empty data"
Cause: the date range covers only non-publication days (a weekend, or a Jewish holiday), so the series exists but has no observation in the window.
Solution: use `lastNObservations=1` to get the most recently published value without modelling the calendar at all. That handles weekends and the Tishrei holiday cluster alike. (Note the opposite failure too: a dataflow query with no date filter does not return nothing, it returns the entire dataflow history.)

### Error: "CPI data not yet available"
Cause: CBS publishes CPI around the 15th of the following month, so the current month's index does not exist yet.
Solution: use the latest published index. If the API returned HTTP 200 but `"month"` is null, the index id is wrong rather than the data being late; the headline index is `120010`.

### Error: "Connection reset by peer" from api.cbs.gov.il
Cause: the CBS index API intermittently drops connections under repeated automated requests. It returns no HTTP status, so this is not a 4xx or 5xx you can branch on.
Solution: retry with a short backoff. The endpoint recovers on its own; forcing HTTP/2 has also succeeded when HTTP/1.1 was resetting. Do not treat it as a permanent failure and do not substitute a different index id.

### Error: "Exchange rate seems stale"
Cause: Using representative rate before daily publication time
Solution: BOI representative rate is published soon after 15:15 Monday-Thursday and soon after 12:15 on Friday and holiday eves, Israel time, and the BOI says the time is not fixed. Before that (or on Saturday/Sunday), the last published business-day rate is the latest available. For intraday indicative rates, use bank or forex feeds.