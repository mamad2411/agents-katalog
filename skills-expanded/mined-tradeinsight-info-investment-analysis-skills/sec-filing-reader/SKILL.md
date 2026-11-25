---
name: sec-filing-reader
description: >
  This skill should be used when the user asks to read a 10-K, summarize a 10-Q,
  read an SEC filing, find a proxy statement, look up a DEF 14A, read an 8-K,
  summarize annual report, read quarterly report, check SEC filings, or look up
  Form 4 for a specific company or insider.
---

# SEC Filing Reader

## Purpose

Retrieve, parse, and summarize SEC filings for a given company by resolving the ticker to a CIK, locating the relevant filing on EDGAR, and extracting the most important sections. Produce a structured summary tailored to the filing type — whether it is an annual report (10-K), quarterly report (10-Q), current event report (8-K), proxy statement (DEF 14A), or insider transaction form (Form 4). Ensure every summary links back to the original filing so the user can verify details against the primary source.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

### Ticker-to-CIK Resolution

1. **Resolve the ticker.** Fetch `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`), locate the company's CIK, and pad it to 10 digits. Cache the CIK and official company name for subsequent requests. If the user provides a company name instead of a ticker, search the JSON for a matching `title` field and confirm the match with the user before proceeding.

2. **Handle ambiguity.** If multiple CIK entries match (e.g., different share classes), prefer the entry with the most common ticker symbol. If the user specifies an insider name rather than a company, use the EDGAR full-text search endpoint with the person's name as the query and `Form 4` as the form type.

### Filing Lookup via EFTS Search

3. **Search for the filing.** Use the EDGAR Full-Text Search System (EFTS) endpoint to locate the desired filing:
   ```
   https://efts.sec.gov/LATEST/search-index?q={company-name-or-CIK}&forms={form-type}&dateRange=custom&startdt={start}&enddt={end}
   ```
   - Set `forms` to the requested filing type: `10-K`, `10-Q`, `8-K`, `DEF 14A`, or `4`.
   - If the user requests the most recent filing, omit the date range or set a broad window (trailing 18 months for 10-K/10-Q, trailing 12 months for 8-K, trailing 24 months for DEF 14A, trailing 6 months for Form 4).
   - If the user specifies a fiscal year or date, narrow the date range accordingly.
   - Parse the JSON response to extract the filing URL, accession number, filing date, and reporting period.

4. **Resolve the filing document URL.** From the EFTS results, construct the path to the filing index page:
   ```
   https://www.sec.gov/Archives/edgar/data/{CIK}/{accession-number-no-dashes}/{accession-number}-index.htm
   ```
   Fetch the index page to identify the primary document (the `.htm` or `.txt` file that contains the actual filing text). Prefer the HTML version over plain text for better structure parsing.

### Filing Retrieval

5. **Fetch the filing content.** Retrieve the primary document URL via WebFetch. For 10-K and 10-Q filings, which can be extremely large, focus on fetching specific sections rather than the entire document when possible. If the document is too large for a single fetch, use multiple targeted requests.

6. **Handle filing variants.** Some filings use the `/ix?doc=` interactive viewer format. Strip the interactive wrapper and fetch the underlying document directly. For XBRL-tagged filings, work with the HTML rendering rather than the raw XBRL.

## Analysis Steps — Summarization by Filing Type

### 10-K (Annual Report)

Extract and summarize the following sections:

- **Item 1 — Business Description.** Summarize the company's principal products and services, revenue streams, key markets, competitive positioning, and any material changes to the business model during the fiscal year.
- **Item 1A — Risk Factors.** Identify the top five to seven risk factors by significance. Highlight any newly added risks compared to the prior year's 10-K, as these often signal emerging concerns. Categorize risks as operational, financial, regulatory, competitive, or macroeconomic.
- **Item 7 — Management's Discussion and Analysis (MD&A).** Extract management's narrative on revenue drivers, margin trends, capital allocation priorities, and forward-looking statements. Note any changes in accounting policies or restatements. Summarize liquidity and capital resources discussion.
- **Item 8 — Financial Statements.** Reference the income statement, balance sheet, and cash flow statement totals. Do not reproduce full financial statements — instead, highlight the key figures (revenue, net income, total assets, total debt, operating cash flow) and direct the user to the structured data endpoints for detailed numbers.
- **Footnotes.** Flag any significant footnotes: revenue recognition changes, lease obligations, contingent liabilities, pension obligations, or off-balance-sheet arrangements. Summarize the stock-based compensation footnote if present.

### 10-Q (Quarterly Report)

Focus on what has changed since the most recent 10-K:

- **MD&A Updates.** Summarize management commentary on quarterly performance, noting any deviation from annual trends or guidance.
- **Interim Financial Highlights.** Extract quarterly revenue, net income, and EPS. Compare to the same quarter in the prior year (YoY) and to the immediately preceding quarter (QoQ).
- **Risk Factor Updates.** Note any new or modified risk factors relative to the 10-K. If the 10-Q states "no material changes," report that explicitly.
- **Legal Proceedings.** Flag any new litigation or regulatory actions disclosed in the quarter.

### 8-K (Current Report)

Summarize the material event reported:

- **Event Type.** Identify the Item number (e.g., Item 2.02 — Results of Operations, Item 1.01 — Entry into a Material Agreement, Item 5.02 — Departure of Directors or Officers). Map the Item number to a plain-language description.
- **Event Summary.** Provide a concise three-to-five sentence summary of the material event, including key figures (deal values, executive names, effective dates).
- **Exhibits.** Note any significant attached exhibits (press releases, agreements) and provide the exhibit URL.

### DEF 14A (Proxy Statement)

Extract the following governance and compensation information:

- **Executive Compensation.** Summarize the Summary Compensation Table for the top five named executive officers. Include total compensation, base salary, bonus, stock awards, and option awards. Note any year-over-year changes in CEO total compensation.
- **Board Composition.** List all director nominees with their committee memberships, tenure, and independence status. Note any new nominees or departing directors.
- **Shareholder Proposals.** Summarize each shareholder proposal, the board's recommendation (for or against), and the voting results if available from a definitive proxy.
- **Say-on-Pay.** Report the advisory vote on executive compensation results if included.

### Form 4 (Insider Transaction)

Extract the following transaction details:

- **Insider Identity.** Name of the reporting person, title or relationship to the company (CEO, CFO, Director, 10% owner).
- **Transaction Details.** For each transaction reported: transaction date, transaction code (P = purchase, S = sale, A = award, M = exercise), number of shares, price per share, and total transaction value.
- **Post-Transaction Holdings.** Report the insider's total share ownership after the transaction.
- **Context.** Note whether the transaction was executed under a 10b5-1 pre-arranged trading plan. If multiple Form 4 filings exist for the same insider in the recent period, summarize the pattern (net buyer or net seller over trailing 90 days).

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Provide a one-to-two paragraph overview per section, a key highlights table with five to eight rows, and a link to the full filing. Aim for a total summary length of 400 to 600 words. Omit footnote analysis and limit risk factors to the top three.

- **Detailed depth.** Expand each section into multiple paragraphs with direct quotes from the filing where relevant. Include full risk factor categorization, complete executive compensation tables, all footnote summaries, and cross-references to prior filings for comparison. Total summary length may reach 1,500 to 2,000 words.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header (using the filing type as the analysis type, e.g., "10-K Summary"). Present section highlights in a table where appropriate, embed the direct link to the full filing on EDGAR prominently at the top of the response, include source links after each section, and close with the standard disclaimer.

Structure the summary as follows:

| Section | Key Highlight |
|---------|--------------|
| Business | [one-line summary] |
| Risk Factors | [top risk or change] |
| MD&A | [key driver or concern] |
| Financials | [headline figure] |
| Footnotes | [notable item or "No material items"] |

Conclude with the full filing URL in the format:
```
Full filing: [SEC EDGAR](https://www.sec.gov/Archives/edgar/data/{CIK}/{accession-path})
```
