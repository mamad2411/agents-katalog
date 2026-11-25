---
name: dividend-analysis
description: This skill should be used when the user asks about dividends, dividend yield, payout ratio, dividend safety, dividend growth, dividend aristocrat, dividend king, buyback, share repurchase, total shareholder return, dividend sustainability, or income investing for a publicly traded company.
---

# Dividend Analysis

## Purpose

Assess a company's dividend program and total shareholder return profile, including current yield, growth trajectory, payout sustainability, and share buyback activity. This skill is designed for income-focused investors who need to evaluate whether a dividend is safe, growing, and competitive relative to alternatives. The analysis covers both historical dividend patterns and forward-looking sustainability under stress scenarios.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full data-fetching instructions, ticker resolution, and fallback behavior.

### Primary Data — SEC EDGAR XBRL API

Fetch the company facts endpoint to retrieve historical financial data:

```
https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
```

Extract the following XBRL concepts for annual (FY) and quarterly (Q1-Q4) periods, sorted chronologically by `end` date:

- **Dividends Per Share:** `CommonStockDividendsPerShareDeclared`
- **Total Dividends Paid:** `PaymentsOfDividendsCommonStock` or `PaymentsOfDividends`
- **Net Income:** `NetIncomeLoss`
- **Diluted EPS:** `EarningsPerShareDiluted`
- **Free Cash Flow:** Derive from `NetCashProvidedByOperatingActivities` minus `PaymentsToAcquirePropertyPlantAndEquipment`
- **Shares Outstanding:** `CommonStockSharesOutstanding` or `WeightedAverageNumberOfDilutedSharesOutstanding`
- **Share Repurchases:** `PaymentsForRepurchaseOfCommonStock`
- **Share Issuance:** `ProceedsFromIssuanceOfCommonStock`

Collect at least 10 years of annual data to identify long-term dividend growth trends and consecutive increase streaks.

### Secondary Data — Stock Analysis

Fetch the cash flow statement for dividend payments and buyback data:

```
https://stockanalysis.com/stocks/{ticker}/financials/cash-flow-statement/
```

Fetch pre-computed ratios for yield and payout data:

```
https://stockanalysis.com/stocks/{ticker}/financials/ratios/
```

Fetch the income statement for earnings data:

```
https://stockanalysis.com/stocks/{ticker}/financials/
```

### Supplementary Context — WebSearch

Search for dividend history, aristocrat/king status, and management commentary on capital return policy:

- `"{ticker} dividend history consecutive increases"`
- `"{ticker} dividend aristocrat" OR "{ticker} dividend king"`
- `"{ticker} capital allocation policy buyback authorization"`
- `"{ticker} dividend safety analysis"`

## Analysis Steps

### Step 1 — Establish Current Dividend Profile

Determine the current state of the dividend program:

- **Current Annual Dividend Per Share (DPS):** Sum of the most recent four quarterly dividends (or the declared annual dividend if paid annually).
- **Current Dividend Yield:** Current Annual DPS / Current Share Price. Express as a percentage.
- **Most Recent Quarterly Dividend:** Amount and ex-dividend date.
- **Dividend Frequency:** Quarterly, semi-annual, annual, or irregular.

Present a summary:

| Metric | Value |
|--------|-------|
| Annual DPS | $X.XX |
| Quarterly DPS | $X.XX |
| Current Yield | X.XX% |
| Frequency | Quarterly |

### Step 2 — Compute Dividend Growth CAGRs

Calculate compound annual growth rates for DPS over multiple time horizons:

| Horizon | DPS CAGR |
|---------|----------|
| 1-Year | X.X% |
| 3-Year | X.X% |
| 5-Year | X.X% |
| 10-Year | X.X% |

Present a year-by-year DPS history table showing at least 10 years of annual dividends with year-over-year growth rates. Highlight any years where the dividend was cut, frozen, or where a special/irregular dividend was paid.

### Step 3 — Evaluate Payout Ratios

Compute both earnings-based and cash-flow-based payout ratios to assess sustainability from two perspectives:

- **Earnings Payout Ratio** = Total Dividends Paid / Net Income. Alternatively, DPS / Diluted EPS.
- **FCF Payout Ratio** = Total Dividends Paid / Free Cash Flow. This is the more conservative and operationally relevant measure.

Present a multi-year table:

| Metric | 2024 | 2023 | 2022 | 2021 | 2020 |
|--------|------|------|------|------|------|
| Earnings Payout Ratio | | | | | |
| FCF Payout Ratio | | | | | |

Interpret the payout ratios:

- **Below 50% (earnings-based):** Generally safe with room for growth.
- **50-75%:** Moderate; growth may slow but dividend is likely sustainable.
- **Above 75%:** Elevated; limited room for growth, and a downturn could threaten the dividend.
- **Above 100%:** Dividend exceeds earnings, funded by debt or reserves. Flag as a significant risk unless FCF payout is materially lower.

Always compare both ratios — companies with high depreciation (e.g., REITs, utilities) may have high earnings payout but sustainable FCF payout.

### Step 4 — Assess Consecutive Growth Streak

Count the number of consecutive years the company has increased its annual dividend:

- **Dividend Aristocrat status:** 25+ consecutive years of dividend increases (S&P 500 member requirement also applies, but note the streak regardless).
- **Dividend King status:** 50+ consecutive years of dividend increases.
- **Dividend Challenger:** 5-9 consecutive years.
- **Dividend Contender:** 10-24 consecutive years.

Report the exact number of consecutive years and the classification. Note any recent dividend cuts or freezes, even if the streak has since restarted.

### Step 5 — Analyze Share Buybacks and Total Shareholder Return

Compute buyback metrics to capture the full capital return picture:

- **Net Share Repurchases** = Share Repurchases minus Share Issuance. Use annual data.
- **Buyback Yield** = Net Share Repurchases / Current Market Capitalization. Express as a percentage.
- **Total Shareholder Return Yield** = Dividend Yield + Buyback Yield. Represents the total cash returned to shareholders as a percentage of market cap.
- **Share Count Trend:** Track shares outstanding over 5 years to confirm whether buybacks are actually reducing the share count (versus merely offsetting stock-based compensation dilution).

Present a table:

| Metric | 2024 | 2023 | 2022 | 2021 | 2020 |
|--------|------|------|------|------|------|
| Dividends Paid ($M) | | | | | |
| Net Buybacks ($M) | | | | | |
| Total Capital Return ($M) | | | | | |
| Shares Outstanding (M) | | | | | |

### Step 6 — Stress Test Dividend Sustainability

Evaluate whether the dividend can be maintained under adverse conditions:

- **Earnings Decline Scenario:** If earnings fell 20% from the most recent year, calculate the resulting earnings payout ratio and FCF payout ratio. Repeat for a 30% decline. If either ratio exceeds 100% under the 20% scenario, flag the dividend as vulnerable. Present results in a table:

| Scenario | Earnings Payout | FCF Payout | Sustainable? |
|----------|----------------|------------|-------------|
| Current | | | |
| Earnings -20% | | | |
| Earnings -30% | | | |

- **Historical Resilience:** During the most recent recession or downturn (2020 COVID, 2008 GFC, or the company's worst recent year), was the dividend maintained, frozen, or cut? If the company maintained or grew the dividend through a downturn, this is a strong positive signal. If it was cut, note the magnitude of the cut and how long it took to restore.
- **Debt Capacity:** Does the company have sufficient balance sheet strength (low leverage, strong interest coverage) to maintain the dividend even during a temporary earnings decline? Check whether debt covenants restrict dividend payments at certain leverage levels.
- **Cash Reserves:** Determine whether the company has sufficient cash on hand to cover 1-2 years of dividend payments from reserves alone if free cash flow temporarily turned negative.

Classify dividend sustainability as: **Very Safe** (FCF payout below 50%, long streak, survived recessions), **Safe** (FCF payout below 70%, consistent history), **Moderate Risk** (FCF payout 70-90%, limited headroom), **Elevated Risk** (FCF payout above 90%, thin coverage), or **Unsafe** (FCF payout above 100% or recent cut), with a brief justification.

### Step 7 — Special and Irregular Dividends

Note any special dividends, extra dividends, or variable dividend policies:

- Amount and date of any special dividends in the last 5 years.
- Whether the company uses a fixed-plus-variable dividend policy (common in energy and mining).
- Capital return distributions from spin-offs or asset sales.

### Step 8 — Synthesize Dividend Assessment

Provide an overall dividend investment characterization:

- Summarize the dividend's current yield relative to sector peers and the broader market.
- Assess whether the dividend growth rate is likely to continue at its historical pace based on payout headroom and earnings growth prospects.
- Identify the primary appeal (high current yield, strong growth, exceptional safety, or balanced profile).
- State the single biggest risk to the dividend.

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for depth and formatting guidelines.

**Summary depth (default):** Present current yield, DPS, 5-year DPS CAGR, earnings and FCF payout ratios for the most recent year, consecutive growth streak, and a 2-3 sentence sustainability assessment.

**Detailed depth:** Expand to full 10-year DPS history with YoY growth rates, multi-year payout ratio tables, complete buyback analysis with share count trend, stress test results, special dividend history, and extended narrative on dividend investment thesis.

## Sector-Specific Adjustments

Apply the following sector-specific considerations when the company operates in a relevant industry:

- **REITs:** REITs are required to distribute at least 90% of taxable income as dividends. Use FFO (Funds From Operations) payout ratio instead of earnings payout ratio, as GAAP net income understates REIT cash flow due to depreciation. An FFO payout ratio below 80% is generally considered sustainable.
- **Utilities:** Typically high payout ratios (60-80%) are normal and sustainable due to regulated, predictable earnings. Compare yield against the utility sector average rather than the broad market.
- **Energy / MLPs:** Variable distribution policies are common. Assess distribution coverage ratio (distributable cash flow / distributions). Coverage above 1.2x is generally considered safe.
- **Banks / Financial Services:** Dividend payments are subject to regulatory stress testing (CCAR/DFAST). Note any regulatory restrictions on capital returns. Compare payout as a percentage of net income against the 30-50% range typical for well-capitalized banks.
- **Technology / Growth:** Many tech companies prioritize buybacks over dividends. When the dividend yield is low but buyback yield is substantial, emphasize total shareholder return yield.

Only include sector-specific metrics when the company's industry warrants them. Do not force these metrics for unrelated sectors.

## Output Format

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for the standard response structure including header, source links, and disclaimer.
