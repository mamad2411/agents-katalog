---
name: analyst-estimates
description: This skill should be used when the user asks about price targets, analyst ratings, consensus estimates, analyst recommendations, buy ratings, sell ratings, hold ratings, EPS estimates, revenue estimates, analyst coverage, estimate revisions, wall street consensus, or analyst forecasts for a publicly traded company.
---

# Analyst Estimates

## Purpose

Compile and present Wall Street analyst consensus estimates, price targets, and recommendation distributions for a publicly traded company. This skill aggregates forward-looking data from analyst coverage to help investors understand market expectations for revenue, earnings, and share price. The analysis highlights estimate revision trends to identify shifts in analyst sentiment that may precede price movements.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full data-fetching instructions, ticker resolution, and fallback behavior.

### Primary Data — Stock Analysis Forecast

The primary and preferred source for analyst estimates is the Stock Analysis forecast page:

```
https://stockanalysis.com/stocks/{ticker}/forecast/
```

This page provides:

- Consensus revenue and EPS estimates for multiple future periods.
- Number of analysts contributing estimates.
- High, low, and mean estimates.
- Analyst price targets (high, low, average, median).
- Recommendation distribution (Strong Buy, Buy, Hold, Sell, Strong Sell).
- Estimate revision data showing changes over 30-day and 90-day periods.

### Secondary Data — Stock Analysis Financials

Fetch the income statement for historical actuals to compare against past estimates:

```
https://stockanalysis.com/stocks/{ticker}/financials/
https://stockanalysis.com/stocks/{ticker}/financials/?p=quarterly
```

### Supplementary Context — WebSearch

Search for additional analyst commentary and recent rating changes:

- `"{ticker} analyst upgrade downgrade {current month} {current year}"`
- `"{ticker} price target change {current year}"`
- `"{ticker} earnings estimate revision"`
- `"{ticker} analyst coverage initiation"`

## Analysis Steps

### Step 1 — Compile Consensus Earnings Estimates

Extract and present consensus EPS estimates for multiple forward periods:

| Period | Mean EPS | High | Low | # Analysts |
|--------|----------|------|-----|------------|
| Current Quarter (Q_ FY____) | | | | |
| Next Quarter (Q_ FY____) | | | | |
| Current Year (FY____) | | | | |
| Next Year (FY____) | | | | |

Fill in the actual quarter and fiscal year labels based on the company's fiscal calendar. Calculate the spread between high and low estimates as a percentage of the mean — a wide spread indicates high uncertainty or divergence among analysts.

For each period, compute the implied YoY growth rate by comparing the estimate against the corresponding prior-period actual result.

### Step 2 — Compile Consensus Revenue Estimates

Extract and present consensus revenue estimates for the same forward periods:

| Period | Mean Revenue | High | Low | # Analysts |
|--------|-------------|------|-----|------------|
| Current Quarter | | | | |
| Next Quarter | | | | |
| Current Year | | | | |
| Next Year | | | | |

Compute implied revenue growth rates and note the estimate spread. Flag any period where the number of analysts is low (fewer than 5), as thin coverage reduces the reliability of the consensus.

### Step 3 — Analyze Estimate Revision Trends

Present how estimates have changed over recent periods to identify momentum in analyst sentiment:

**EPS Estimate Revisions:**

| Period | 30 Days Ago | Current | Change | 90 Days Ago | Change |
|--------|-------------|---------|--------|-------------|--------|
| Current Quarter | | | | | |
| Current Year | | | | | |
| Next Year | | | | | |

**Revenue Estimate Revisions:**

| Period | 30 Days Ago | Current | Change | 90 Days Ago | Change |
|--------|-------------|---------|--------|-------------|--------|
| Current Quarter | | | | | |
| Current Year | | | | | |
| Next Year | | | | | |

Interpret revision trends:

- **Upward revisions** across multiple periods indicate improving business momentum and often precede positive price action.
- **Downward revisions** across multiple periods suggest deteriorating fundamentals and may signal further downside.
- **Stable estimates** indicate the business is tracking in line with expectations.
- **Mixed signals** (e.g., near-term revisions down but long-term up) may reflect timing shifts rather than fundamental changes.

Count the number of analysts revising up versus down over the last 30 days if this data is available.

### Step 4 — Present Price Targets

Extract analyst price target data:

| Metric | Value |
|--------|-------|
| Average Price Target | $XXX.XX |
| Median Price Target | $XXX.XX |
| High Price Target | $XXX.XX |
| Low Price Target | $XXX.XX |
| Current Price | $XXX.XX |
| Upside to Average | +XX.X% |
| Upside to Median | +XX.X% |
| Number of Analysts | XX |

Calculate the implied upside or downside from the current share price to the average and median price targets. Note the range between high and low targets as an indicator of conviction dispersion.

Flag if the current price is above the average price target (bearish signal) or significantly below the low price target (potential deep value or broken thesis).

### Step 5 — Summarize Recommendation Distribution

Present the current distribution of analyst recommendations:

| Rating | Count | % of Total |
|--------|-------|------------|
| Strong Buy | | |
| Buy | | |
| Hold | | |
| Sell | | |
| Strong Sell | | |
| **Total** | | 100% |

Calculate the **consensus score** as a weighted average (Strong Buy=5, Buy=4, Hold=3, Sell=2, Strong Sell=1) and classify:

- 4.5-5.0: Strong Buy consensus
- 3.5-4.5: Buy consensus
- 2.5-3.5: Hold consensus
- 1.5-2.5: Sell consensus
- 1.0-1.5: Strong Sell consensus

Note any recent changes in the distribution (e.g., "3 analysts upgraded from Hold to Buy in the last 30 days") if available from WebSearch.

### Step 6 — Compare Estimates to Historical Actuals

Provide context by comparing current estimates against the company's recent track record of beating or missing estimates:

- For the most recent 4 quarters, show the estimate versus actual EPS and whether the company beat or missed.
- Calculate the average earnings surprise percentage over the last 4 quarters.
- If the company consistently beats by a predictable margin, note this pattern (the "whisper number" concept).

| Quarter | EPS Estimate | EPS Actual | Surprise | Beat/Miss |
|---------|-------------|------------|----------|-----------|
| Q_ FY____ | | | | |
| Q_ FY____ | | | | |
| Q_ FY____ | | | | |
| Q_ FY____ | | | | |

### Step 7 — Assess Analyst Coverage Quality

Evaluate the reliability and depth of the analyst consensus:

- **Coverage depth:** Number of analysts covering the stock. Fewer than 5 indicates thin coverage with less reliable consensus — note this prominently as it reduces confidence in all consensus figures. Between 5-15 analysts is typical mid-cap coverage. More than 20 indicates deep institutional coverage with a well-established consensus.
- **Estimate dispersion:** Calculate the spread between high and low estimates as a percentage of the mean. A spread below 10% indicates strong consensus agreement. A spread above 25% indicates significant disagreement, which may reflect uncertainty about a key business driver, an upcoming binary event (e.g., regulatory decision, clinical trial), or different modeling assumptions among analysts.
- **Revision momentum:** Consistent direction of revisions (mostly up or mostly down) is more informative than mixed signals. Count the ratio of upward to downward revisions over the last 30 days if available — a ratio above 2:1 in either direction indicates strong directional consensus.
- **Staleness risk:** Identify whether estimates may be stale by checking the most recent earnings date. If a new quarter has been reported but estimates have not been widely updated, note that some figures may not yet reflect the latest results.

### Step 8 — Synthesize Analyst Sentiment

Provide an overall summary of what the analyst community expects:

- State whether the consensus outlook is **Bullish** (majority Buy/Strong Buy, positive revisions, meaningful price target upside), **Neutral** (majority Hold, stable estimates, limited price target movement), or **Bearish** (presence of Sell ratings, downward revisions, price target below current price) based on the combination of recommendation distribution, price target upside, and estimate revision trends.
- Identify any disconnect between the recommendation consensus (e.g., mostly Buy) and implied price target upside (e.g., limited upside to average target). This disconnect is common in stocks that have rallied to meet targets but where analysts have not yet downgraded. It often precedes a wave of price target increases or rating downgrades.
- Note whether the stock appears to be in an estimate revision upgrade cycle (accelerating positive revisions) or downgrade cycle (accelerating negative revisions), and how long the current cycle has persisted.
- Highlight the key upcoming catalyst (next earnings date) that will test current estimates. Compute the number of days until the next expected earnings report if known.
- Summarize in one sentence the core expectation embedded in the consensus: what must the company deliver for the current estimates and price targets to be met?

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for depth and formatting guidelines.

**Summary depth (default):** Present current-year and next-year consensus EPS and revenue estimates with implied growth rates, the average price target with upside/downside, and the recommendation distribution. Include a 2-3 sentence narrative on the overall analyst sentiment.

**Detailed depth:** Expand to include all forward periods (current quarter through next year), full revision trend tables for 30-day and 90-day windows, earnings surprise history for the last 4 quarters, price target range analysis, coverage quality assessment, and extended narrative synthesizing the analyst outlook with potential risks and catalysts.

## Output Format

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for the standard response structure including header, source links, and disclaimer.
