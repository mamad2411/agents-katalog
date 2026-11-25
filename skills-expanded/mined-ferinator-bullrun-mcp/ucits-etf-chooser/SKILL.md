---
name: ucits-etf-chooser
description: Compare UCITS ETFs that track the same index with Bullrun data. Use when a European investor asks for the cheapest or lowest-fee fund for an index (MSCI World, S&P 500, FTSE All-World, Nasdaq-100, MSCI EM and so on), which ticker or exchange line of a fund to use, whether two ETFs overlap, accumulating versus distributing share classes, or what a fund's ongoing costs add up to over time.
---

# Choosing between UCITS ETFs on one index

This skill uses the Bullrun connector's ETF tools to compare funds that track the same index. The aim is a dated, sourced comparison the user can check with their broker. It does not pick a fund for them.

## Ground rules

- **Count funds, not tickers.** One UCITS fund (one ISIN) trades on several exchanges under different tickers. Treat those as one choice. Two listings of the same ISIN are never diversification.
- **Watch for share classes.** Share classes of one fund, such as "EUR Capitalisation" and "USD Capitalisation", or hedged and unhedged, have different ISINs but hold the same portfolio. When the cheapest rows are classes of one fund, say so. Count them as one choice, and use the other slot in a shortlist for a different issuer.
- **Fees and yields are percentage points.** `0.07` means 0.07% a year, in tool inputs and outputs.
- **Missing means unknown.** A fund with no published fee, AUM, holdings or price is reported as missing. It is not "zero" and not "fine". Don't fill gaps from memory.
- **Show disagreements.** If two tools report different values for the same fund, for example AUM from `get_etf_index_group` and from `compare_etfs`, show both. Don't pick one. AUM currency is often not stored, so don't compare AUM across funds as if it were in one currency.
- **Never guess a filter value.** Index keys, categories, exchanges and domiciles match exactly. A wrong string returns zero rows, which looks like "no such fund". Resolve every value first.
- **Prices are stored daily closes**, not live quotes. Give the date with every price or return.

## Steps

### 1. Pin down the index and the user's constraints

Work out which index the user means and what they have already said: payout (accumulating or distributing), exchange or trading currency (for example XETRA in EUR, SIX in CHF, LSE in GBP or USD), any AUM floor or issuer preference, and any amount and horizon for a cost estimate. Ask only about things that change the answer, in one short question. Sensible defaults are any payout, any venue, and no cost simulation.

- If the user quotes an ISIN or a ticker, call `get_etf_fund` with `isin` or `ticker`. It returns the fund, its index, its costs and every venue it trades on.
- To resolve the index, call `get_etf_index_group` with no `indexKey`. It lists the index families that have funds. Or call `get_etf_filter_options` with `facets: ["indexKeys"]`. Use the exact key returned, such as `MSCI_WORLD` or `SP500`.

### 2. List every UCITS fund on that index, cheapest first

Call `get_etf_index_group` with `indexKey`, `scope: "ucits"`, and `distributionPolicy`, `exchange` or `currency` only when the user asked for them. It returns one row per fund with its fee, listing count and venues. It also says how many funds publish no fee. Never call a fund "the cheapest" without that caveat.

`scope: "all"` adds US-domiciled trackers. A European retail investor generally can't buy those, so add them only if the user asks.

### 3. Narrow with extra criteria (optional)

If the user wants more than the fee ranking, such as a minimum size, a fund older than three years, one issuer, or currency hedging, run **one** precise `screen_etfs` call. Use `indexKey`, `ucitsStatus: "UCITS"`, and `rules` such as `{metric: "totalAssets", operator: ">=", value: 1, unit: "B"}` or `{metric: "fundAgeYears", operator: ">=", value: 3}`, with `sortBy: "expenseRatioPct"` and `order: "asc"`. `screen_etfs` is an expensive whole-universe read, so build one good screen rather than several loose ones. A fund missing a ruled metric is excluded by that rule. Say so when it matters.

### 4. Compare a shortlist of two or three distinct funds

Take two or three funds with different ISINs. For each, pick the one listing on the user's exchange or currency; `get_etf_fund` shows every venue if you need it. Then call `compare_etfs` with those listing tickers and `include: ["costs", "fund_data", "income", "benchmark", "overlap"]`. Add `"performance"` or `"risk"` only if the user asks about returns or volatility.

- **Overlap:** two funds on the same index usually overlap almost completely, so holding both adds little. Many stored snapshots are only the top 10 holdings (about a quarter of the fund's weight). Then the overlap figure is a lower bound, and it can't exceed the weight both snapshots cover. Read `coveredWeightPct` and `isComplete` for each fund and say which snapshot date each figure comes from.
- **Leaders** in the comparison are mechanical extremes, such as the lowest fee or the largest AUM. They are not a verdict.

For country, sector or currency look-through on one fund, call `get_etf_exposures`. The currency split is the currency each holding is quoted in, not the fund's real FX risk. Unclassified weight stays unclassified. This tool can be expensive, so call it only when the user asks.

### 5. Costs over time (only when the user gives the inputs)

The ongoing charge (TER) is one part of the cost. Spreads, broker commissions, FX conversion, taxes and tracking difference also matter. Bullrun doesn't store most of them, so never invent them.

If the user gives an amount and a horizon, call `simulate_etf_cost` with `ticker`, `initialInvestment`, `contributionAmount`, `contributionFrequency` and `years`. Pass `spreadPct` and `commissionPerTrade` only with numbers the user supplied, and leave `grossAnnualReturnPct` at 0 unless they give a return assumption. Present the result as an illustration of fee drag under those inputs, not a forecast.

## Output

Start with a one-line scope: the index, `scope`, any filters, and the date of the data.

Then add a table with one row per fund: fund name, ISIN, TER (%), payout, domicile, AUM (with currency and date), and the listing on the user's venue (ticker, exchange, currency). Add the number of other venues.

After the table:
- **What the data shows:** the fee spread between the funds, any size or age differences, the overlap result, and any cost illustration.
- **Gaps:** funds with no published fee, partial holdings, missing AUM, and old snapshot dates.
- **Check with your broker:** whether the line can be bought there, the spread and commission, and the tax treatment of the domicile and payout. You can't see the user's tax situation, so don't assess it.

Write "lowest disclosed fee in Bullrun's data", not "best ETF", and "the comparison shows", not "you should buy". The user makes the choice.

Tool results can include a `platformLink`, a link to the same view on bull-run.org. Show it only when it helps the user check the comparison.
