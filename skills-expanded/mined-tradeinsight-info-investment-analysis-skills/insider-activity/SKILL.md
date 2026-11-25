---
name: insider-activity
description: >
  This skill should be used when the user asks about insider buying, insider selling, insider transactions,
  Form 4 filings, insider ownership, insider activity, executive compensation, management governance,
  board independence, capital allocation, insider trading filings, or management skin in the game
  for a publicly traded company.
---

# Insider Activity & Governance Analysis

## Purpose

Analyze insider ownership, transaction patterns, executive compensation structures, capital allocation decisions, and corporate governance quality for a publicly traded company. Assess management alignment with shareholders by examining whether insiders are buying or selling, how executives are compensated, and whether governance structures protect or disadvantage outside investors. Provide a holistic view of management quality and shareholder-friendliness.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full data-fetching instructions, ticker resolution, and fallback behavior.

### Step 1 — Resolve Ticker and Retrieve Insider Filings

1. Resolve the company ticker to a CIK via the SEC company tickers JSON endpoint.
2. Search for recent Form 4 filings using the EFTS search endpoint: query the company name or ticker with `forms=4` and a date range covering the past 12 months.
3. For each Form 4 filing returned, fetch the filing page via WebFetch to extract: reporting person name and title, transaction type (purchase, sale, option exercise), number of shares, price per share, date, and post-transaction holdings.
4. If EDGAR Form 4 data is difficult to parse, fall back to Stock Analysis or WebSearch for "{ticker} insider transactions" to find pre-aggregated insider activity summaries.

### Step 2 — Retrieve Proxy Statement (DEF 14A)

1. Search for the most recent DEF 14A filing using EFTS: query the company name with `forms=DEF%2014A`.
2. Fetch the filing page and extract:
   - Executive compensation tables: base salary, bonus, stock awards, option awards, non-equity incentive plan, and total compensation for the top 5 named executive officers.
   - Director compensation table.
   - Beneficial ownership table: shares held by each director and officer, and by major institutional holders.
   - Governance provisions: board size, independence ratio, classified board status, poison pill, dual-class share structure, related-party transactions.
3. If the full DEF 14A is too long to parse effectively, use WebSearch for "{ticker} executive compensation" and "{ticker} corporate governance" to find summary analyses.

### Step 3 — Gather Capital Allocation History

1. Use WebSearch to research the company's capital allocation track record over the past 5-10 years:
   - Major acquisitions: target, price paid, strategic rationale, post-acquisition performance.
   - Share buyback history: total spent, timing relative to valuation (bought at high vs low multiples).
   - Dividend initiation, growth rate, and payout ratio trend.
   - Organic investment: R&D spending trend, capital expenditure trend.
2. Fetch cash flow data from Stock Analysis (`/financials/cash-flow-statement/`) to quantify capital allocation across buybacks, dividends, capex, and M&A.

## Analysis Steps

### Step 1 — Analyze Insider Ownership and Transactions

**Insider Ownership Assessment**
- Calculate aggregate insider ownership as a percentage of shares outstanding.
- Identify the largest individual insider holders (CEO, founder, board members).
- Compare insider ownership to peer companies in the same sector.
- Assess whether insider ownership is meaningful enough to align management interests with shareholders (generally above 1-3% is notable for large-caps; higher thresholds for small/mid-caps).
- Evaluate whether insider ownership is concentrated in the founder/CEO or distributed across multiple executives and directors. Broad-based insider ownership is a stronger alignment signal.
- Note any recent changes in ownership: significant increases through open-market purchases indicate confidence, while significant decreases may signal concern.
- Check for pledged shares: insiders who have pledged shares as collateral for personal loans create forced-selling risk during stock price declines.

**Transaction Pattern Analysis**
- Aggregate insider purchases and sales over the past 3, 6, and 12 months.
- Distinguish between open-market purchases (strongest signal), option exercises followed by sales (weaker signal), and 10b5-1 pre-planned sales (neutral signal).
- Calculate the buy/sell ratio: number of insider buyers versus sellers.
- Identify any cluster buying (multiple insiders buying within a short window), which is a stronger bullish signal than isolated purchases.
- Note any unusually large transactions relative to the insider's total holdings.
- Flag any insider sales that are disproportionately large or occur before negative news.
- Contextualize insider sales: regular diversification sales by executives with high concentration are less concerning than sudden, unplanned sales outside of normal patterns. Review whether the insider has a history of consistent selling at a fixed schedule versus sporadic, discretionary transactions.
- Compare the current insider activity trend to the company's historical pattern and to sector norms. Some industries (e.g., biotech, tech startups) naturally see more insider selling due to equity-heavy compensation.

Present insider transaction data in a table:

| Insider | Title | Date | Type | Shares | Price | Value | Holdings After |
|---------|-------|------|------|--------|-------|-------|----------------|
| ... | ... | ... | Buy/Sell | ... | ... | ... | ... |

### Step 2 — Evaluate Executive Compensation

**Compensation Structure Assessment**
- Present the total compensation for the CEO and top 5 executives in a table.
- Break down compensation into components: base salary, annual bonus, stock awards, option awards, non-equity incentive plan, other compensation, and total.
- Calculate the percentage of total compensation that is performance-based (stock awards + incentive plan) versus fixed (salary + other).
- Assess whether the compensation structure incentivizes long-term value creation or short-term earnings manipulation.

**Pay-for-Performance Alignment**
- Compare CEO total compensation to company performance metrics (revenue growth, EPS growth, total shareholder return) over the past 3-5 years.
- Evaluate whether pay increased when performance declined (a red flag).
- Compare CEO pay to peer company CEO compensation.
- Note the CEO pay ratio (CEO compensation divided by median employee compensation, required in proxy filings since 2018).

**Compensation Red Flags**
- Excessive perquisites or supplemental retirement benefits.
- Large one-time "retention" or "transformation" awards outside the normal plan.
- Low performance hurdles that are easy to achieve.
- Repricing of underwater stock options.
- Golden parachutes with excessively generous change-of-control provisions.
- Tax gross-up provisions on severance or change-of-control payments, which amplify the cost to shareholders.
- Clawback policy weakness: evaluate whether the company has a robust clawback policy for incentive compensation in cases of restatement or misconduct, as required by SEC rules adopted under Dodd-Frank.

### Step 3 — Assess Corporate Governance

**Board Quality**
- Calculate the percentage of independent directors (at least two-thirds is best practice).
- Assess board diversity in terms of skills, industry experience, and backgrounds.
- Identify any directors who are overboarded (serving on too many boards, typically more than 4).
- Check whether the CEO also serves as board chair (combined role is a governance concern).
- Note the average board tenure and whether there is adequate board refreshment.

**Governance Structure**
- Classified (staggered) board: reduces shareholder ability to replace directors quickly.
- Dual-class share structure: gives founders disproportionate voting control.
- Poison pill (shareholder rights plan): deters hostile takeovers, can entrench management.
- Majority vs plurality voting for directors.
- Shareholder ability to call special meetings and act by written consent.
- Related-party transactions: any business dealings between the company and insiders.

**Management Transparency**
- Assess the quality and consistency of earnings guidance: does management provide guidance, and how accurate has it been historically.
- Evaluate the gap between GAAP and non-GAAP earnings: a persistently large gap may indicate aggressive adjustments.
- Review management commentary in earnings calls for clarity, candor, and willingness to discuss challenges.

### Step 4 — Evaluate Capital Allocation Track Record

**Acquisition Track Record**
- List major acquisitions over the past 5-10 years with approximate deal value.
- Assess whether acquisitions have created or destroyed value based on post-deal performance.
- Note the frequency of acquisitions: serial acquirers require closer scrutiny of integration execution.
- Flag any goodwill impairments, which indicate overpayment for past acquisitions.

**Buyback Effectiveness**
- Calculate total cash spent on buybacks over the past 5 years.
- Compare buyback timing to share price levels: effective management buys back stock when it is undervalued.
- Assess whether buybacks are reducing the share count meaningfully or merely offsetting dilution from stock-based compensation.

**Dividend Policy**
- Note the dividend initiation date and consecutive years of payment or growth.
- Calculate the current payout ratio and assess sustainability.
- Compare the dividend growth rate to earnings growth rate.

**Overall Capital Allocation Framework**
- Calculate how cumulative free cash flow over the past 5 years was distributed across: dividends, buybacks, M&A, debt repayment, and cash accumulation. Present this as a percentage breakdown.
- Assess whether capital allocation priorities are appropriate given the company's lifecycle stage: growth companies should prioritize reinvestment, mature companies should return capital, and transitioning companies should balance both.
- Evaluate management's stated capital allocation philosophy (from earnings calls and investor presentations) against actual behavior. Consistency between words and actions is a positive governance signal.

Summarize the capital allocation assessment with a rating: Excellent, Good, Mixed, or Poor, with supporting evidence.

## Depth Handling

- **Summary depth (default):** Insider ownership percentage and buy/sell summary for the past 12 months, CEO compensation total with performance-based percentage, key governance flags (dual-class, classified board, CEO-chair), and a one-paragraph capital allocation assessment.
- **Detailed depth:** Full insider transaction table, complete executive compensation breakdown with peer comparison, comprehensive governance structure review, and multi-year capital allocation analysis with M&A track record.
- **Specific question:** If the user asks about a single aspect (e.g., "Is AAPL management buying or selling?"), focus the analysis on that topic with supporting data and context.

## Output Formatting

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard output structure, table formatting, source citations, and the required disclaimer.

Present insider transaction tables and compensation tables prominently. Use narrative for governance assessment and capital allocation evaluation. Always cite the specific SEC filing (Form 4 or DEF 14A with filing date) or data source for each data point.
