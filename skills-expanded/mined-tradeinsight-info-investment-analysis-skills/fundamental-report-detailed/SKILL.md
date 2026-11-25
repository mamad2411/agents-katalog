---
name: fundamental-report-detailed
description: >
  This skill should be used when the user invokes "/fundamental-report-detailed"
  followed by a stock ticker. Generates a comprehensive fundamental analysis
  research note at detailed depth covering all 14 analysis areas with full data
  tables, multi-year trend analysis, and extended commentary.
user-invocable: true
disable-model-invocation: true
---

# Fundamental Report — Detailed Depth

Generate a comprehensive, in-depth fundamental analysis research note for a publicly traded company. This is the detailed variant of the fundamental report — every analysis area provides full multi-year data tables, trend analysis, and extended commentary.

## Orchestration Process

Follow the same orchestration as the summary report (`${CLAUDE_PLUGIN_ROOT}/skills/fundamental-report/SKILL.md`) with one critical difference:

**All analysis skills produce detailed depth output.**

### Step 0: Ticker Resolution

Identical to summary report. Resolve ticker to CIK, fetch company metadata (name, sector, exchange, price, market cap).

### Step 1: Parallel Dispatch

Launch the same 17 parallel tasks as the summary report:
- 14 analysis skills
- 2 utility skills (peer-comparison, sec-filing-reader)
- 1 signal-rater agent

**Critical difference:** Instruct each skill to provide **detailed depth** output:
- Full multi-year data tables (5-10 years of annual data, 8 quarters of quarterly data where available)
- Year-over-year and period-over-period change calculations
- Trend analysis with commentary on inflection points
- Extended interpretation connecting metrics to business context
- Sector-specific deep dives where applicable

### Step 2: Sequential Cross-Validation

Identical to summary report. Cross-validate key metrics across sources after all parallel results collected.

### Step 3: Report Assembly

Do not announce or enumerate data sources, tools, or fetching details to the user at this stage. Simply compile the results.

Compile results into the same 9-section structure as the summary report:

1. **Key Metrics Summary** — same quick-reference table
2. **Signal Rating** — same aggregated rating with per-source breakdown
3. **Detailed Analysis** — all skill results organized Tier 1 → Tier 2 → Tier 3, now at **detailed depth** with full data tables and extended commentary per area
4. **Cross-Validation** — same discrepancy table
5. **Reasons to Consider** — 5-7 bull case arguments (more than summary) with supporting data points
6. **Reasons to Avoid** — 5-7 bear case arguments with supporting data points
7. **Summary** — concise terminal-friendly summary (same template as summary report)
8. **Source Links** — all URLs grouped by source
9. **Disclaimer**

Write the full report to `reports/YYYY-MM-DD-HH-MM-SS-{TICKER}.md` and display only the Summary section in the terminal. See the summary report skill for the Summary template and file output instructions.

### Detailed Depth Guidelines

For each analysis area in Section 3, provide:

**Data tables:** Present 5-10 years of annual data in a markdown table with all relevant metrics. Include a separate quarterly table for the most recent 8 quarters.

**Trend analysis:** Identify and comment on:
- Multi-year trends (improving, deteriorating, stable)
- Inflection points (when did a metric change direction?)
- Cyclical patterns (quarterly seasonality)
- Outliers (one-time items, pandemic effects, restructuring charges)

**Contextual interpretation:** Connect the numbers to the business:
- Why did revenue accelerate/decelerate?
- What drove margin expansion/compression?
- How does management's capital allocation track record look?
- What are the competitive dynamics behind market share shifts?

**Comparative context:** Where relevant, compare against:
- The company's own historical averages
- Industry/sector averages
- Closest peer companies

## Additional Resources

Consult `${CLAUDE_PLUGIN_ROOT}/skills/fundamental-report/SKILL.md` for the complete orchestration process (Steps 0-3) and full report section specifications.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for data fetching instructions and source priority matrix.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for detailed output formatting guidance.
