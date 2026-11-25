---
name: company-deep-dive
description: Research one listed company end to end with Bullrun data and write a dated summary that states its gaps. Use when the user asks for a deep dive, research note, overview or "tell me about" on a stock, wants to understand a company's financials, quality, valuation context, risks, suppliers, customers, competitors or recent news, or names a company or ticker outside the US (Europe, Switzerland, UK, Japan and others) as well as US ones.
---

# Company deep dive

This skill uses the Bullrun connector to research one company. It ends in a dated summary that says which data it is based on and which data is missing. It describes the company; it doesn't make a buy or sell call.

## Ground rules

- **Date everything.** Each figure carries its own date: the price date, the fiscal period, when a risk score was computed, when a news article was published. Never present stored data as live.
- **Native currency.** Prices are in the listing's trading currency. Financials are in the company's reporting currency (`sourceCurrency`). Don't convert silently. GBX (pence) and GBP are different units.
- **Missing means unknown.** An empty dataset, a null field, a dark risk dial or no relationship edges means Bullrun has no data. It does not mean zero risk, no news or no suppliers.
- **Bullrun's own scores are descriptive.** The valuation gap compares the current multiple with what similar companies typically command. It is not a price target. Risk bands (Contained, Normal, Elevated, Stretched, Acute) describe measured strain. Neither is a buy or sell view.
- **Reuse results.** Don't re-fetch what you already have. The free connection includes 700 successful tool calls per rolling 30 days, shared by anonymous network. Each successful call counts once; failed calls use no allowance. If a temporary capacity or pacing limit asks you to wait, follow its retry guidance.

## Steps

### 1. Resolve the listing

If the user gave a company name, an ISIN or an ambiguous symbol, call `search_stocks` with `query`. It returns candidate listings and never picks one when alternatives remain. If several listings or share classes match, show them (exchange, currency, ticker) and ask which one, or use the home-market listing when the user's wording makes that clear. Bullrun tickers are the plain local symbol for US and most European listings (AAPL, ASML, NESN) and keep the exchange suffix for most Asian ones (6324.T, 0700.HK).

### 2. Check what Bullrun has before going deep

Call `get_company_data_coverage` with `ticker`. It lists the datasets stored for the company, their latest periods and their timestamps, including the relationship graph status. Use it to decide which optional tools in step 4 are worth calling, and keep its answer for the gaps section.

### 3. Core reads (call each once)

1. `get_stock_metrics`: identity, latest daily price, market cap, P/E, dividend, latest reported financials and a short business description.
2. `get_financial_history` with `periodType: "annual"` and `years: 10`: revenue, margins, earnings, cash flow and leverage over time, with CAGR and consistency checks. Use `periodType: "both"` only if recent quarters matter to the question.
3. `get_quality_moat_metrics` with `years: 10`: ROIC, ROE, accruals, cash conversion, capex intensity, payout and share-count changes. Leave `estimatedWaccPct` unset unless the user supplies a WACC; without one the ROIC-versus-WACC spread stays null.
4. `get_valuation_model` with `tickers: [ticker]`: the valuation gap and relative forecast signal, with percentile and rank. A positive gap means the stock trades below the multiple the model sees as typical. Report it as context.
5. `get_company_risk`: the 0-100 composite, the six mechanism dials (market expectation, operating pressure, cash conversion, leverage, competitive position, concentration), filing-derived risk factors and supplier concentration. A dark dial is unmeasured, not safe.
6. `get_company_relationships` with `evidence: "sources"`: named competitors, suppliers, customers and partners. Separate VERIFIED edges (confirmed against a filing or primary source) from search-SUGGESTED ones. Status "none" means no graph has been built yet.
7. `get_company_news` with `limit: 10`: cached headlines, newest first, with publisher and publication date. An empty or old list does not prove nothing happened.

### 4. Optional reads (only when coverage says the data exists, or the user asks)

- `get_revenue_breakdown`: segment or geography split.
- `get_forward_estimates`: consensus revenue and EPS where available. The first read can be empty while a refresh runs.
- `get_operating_kpis`: domain KPIs. Coverage is limited.
- `get_earnings_call_transcript`: US companies only. The first read can be empty while an import runs.
- `get_corporate_calendar` with `q: ticker` and `include: ["earnings", "ex_dividend"]`: upcoming dates. Missing dates mean unknown.
- `get_company_risk_history`: how the risk readings changed and which inputs changed. A change in formula or coverage is not a business change by itself.
- `find_stock_peers`, then `compare_stocks` with the returned arguments: a classification-based peer table. Peers chosen by industry code are not verified competitors.

## Output: the dated summary

Use this structure and keep it tight:

```
# <Company> (<ticker>, <exchange>, <currency>): research summary, <today's date>

Data as of: price <date> · latest annual period <FY> · latest quarter <period or "none">
· risk computed <date> · valuation model <date or "date not reported"> · newest news item <date>

## Business
## Financial track record   (a small table: revenue, operating margin, net income, FCF, net debt across the years)
## Quality and capital allocation
## Valuation context        (multiples, plus Bullrun's model gap as context, not a target)
## Risk                     (composite and dials, top filing risk factors, supplier concentration)
## Relationships            (verified first; suggested ones labelled as such)
## Recent news              (dated headlines with sources)
## What matters most        (2-3 points), main risks, and what would change the picture
## Gaps and limits
```

**Gaps and limits is required.** List every dataset that was missing, empty, partial, stale or not checked. Use `get_company_data_coverage` and the warnings in each tool result. Examples: "no transcript (non-US)", "relationship graph not built", "two of six risk dials unmeasured", "latest annual period FY2024", "forward estimates empty on first read". If nothing was missing, say what was checked.

Close with one line: this summary describes stored data as of the dates shown and is not investment advice.

Avoid advice wording. Don't write "buy", "sell", "undervalued, so attractive", "a good investment" or "I recommend". Write what the data shows and what would change it. If the user asks directly whether to buy, explain that you can lay out the evidence but the decision is theirs.

Tool results can include a `platformLink`, a link to the same view on bull-run.org (charts, the risk network, filings). Show it only when it helps the user check a figure.
