---
name: financial-statement-analysis
description: Use when analyzing company financial statements, fundamentals, ratios, margins, cash flow, working capital, financial health, historical trends, forecast assumptions, budget variance, or valuation context from available financial data. Prefer this Skill when the central work is financial performance understanding, not trading or portfolio management. Do not use for personalized investment advice, order execution, tax/legal/accounting advice, or broad investment thesis writing unless statement analysis is the main step.
meta:
  version: 1
  display_name: 财务报表分析
  source: alirezarezvani/claude-skills financial-analyst; claude-office-skills financial-modeling and stock-analysis
  license: MIT
---

# Financial Statement Analysis

## Purpose

Analyze financial statements and related company metrics with source discipline, clear formulas, stated assumptions, and explicit uncertainty. This Skill owns financial performance understanding: statement mapping, ratio analysis, trend interpretation, cash-flow quality, forecast reasonableness, and valuation context.

This Skill adapts open-source finance analysis practices for XAgent while removing spreadsheet automation, market-data, MCP, Office, Python, and script assumptions. It describes the analysis process only.

## Use When

Use for:

- interpreting income statements, balance sheets, cash-flow statements, annual reports, quarterly reports, earnings releases, investor presentations, or management discussion material;
- calculating or explaining profitability, liquidity, leverage, coverage, efficiency, growth, valuation, and cash-flow metrics;
- comparing current performance against prior periods, budget, guidance, peers, or industry norms;
- reviewing revenue quality, margin structure, working capital, debt capacity, free cash flow, and earnings quality;
- checking DCF, comparable-company, or forecast assumptions as part of a financial analysis;
- preparing statement-grounded inputs for `investment-research`, `research-synthesis`, `weekly-report`, or `solution-brief`.

Prefer `investment-research` when the user asks for an investment thesis, diligence memo, market view, catalysts, or opportunity assessment. Prefer `data-visual-report-builder` when the main task is charting or statistical reporting over structured data.

## Do Not Use When

Do not use for:

- executing transactions, portfolio changes, brokerage actions, banking actions, or money movement;
- personalized investment advice, suitability assessment, tax advice, legal advice, audit assurance, or accounting sign-off;
- real-time market-data retrieval or external data access unless an XAgent tool explicitly provides that capability;
- broad research across companies, sectors, and markets where financial statements are only one evidence source;
- spreadsheet, Office, PDF, or document conversion tasks.

## Material Gate

Before analyzing, identify:

- entity, ticker if relevant, reporting period, fiscal year-end, reporting currency, units, and accounting basis;
- source material, source date, version, and whether numbers are audited, unaudited, restated, consolidated, or segment-level;
- requested lens: performance review, trend analysis, ratio analysis, valuation support, forecast check, variance analysis, peer comparison, or risk review;
- required comparators: prior periods, budget, guidance, industry, peers, management targets, or market price date;
- known limitations: missing statements, missing notes, mixed currencies, one-time items, accounting changes, M&A, discontinued operations, seasonality, or stale market data.

If a key input is missing, continue only with a scope-limited analysis and mark the missing item `待确认`. Do not invent line items, prices, market caps, debt terms, tax rates, peer sets, or management guidance.

## Workflow

1. Restate the analysis objective and decision context without turning it into investment advice.
2. Inventory the available financial materials and dates before calculating anything.
3. Track source, date, period, currency, units, accounting basis, and whether figures are audited, unaudited, restated, consolidated, or segment-level.
4. Normalize the statement view: revenue, gross profit, operating income, EBITDA if available, net income, assets, liabilities, equity, working capital, debt, cash, operating cash flow, capital expenditures, and free cash flow.
5. Check consistency across statements: net income to cash flow, cash movements, debt changes, working-capital movements, and non-recurring items.
6. Choose only relevant analyses from `references/statement-analysis-rules.md`: trend, common-size, profitability, liquidity, leverage, coverage, efficiency, growth, cash-flow quality, or variance.
7. State each material formula, denominator, period, and unit before relying on the result.
8. Interpret results in business context: revenue drivers, margin mix, operating leverage, capital intensity, working capital, financing structure, and industry dynamics.
9. Use `references/valuation-rules.md` only when the user needs valuation support. Present valuation as ranges and sensitivities, not certainty.
10. Separate financial facts, calculations, assumptions, interpretation, risks, and open questions.
11. Hand off to `investment-research` only after financial evidence, assumptions, and limitations are clear.

## Checks

- Every material number has a source, date, period, currency, and unit.
- Ratios compare consistent periods and definitions; denominators are visible.
- One-time items, restatements, accounting changes, acquisitions, divestitures, and seasonality are not silently treated as recurring performance.
- Profitability, growth, and cash conversion are not interpreted from one metric alone.
- Leverage and coverage metrics consider cash, debt maturity, interest expense, and cash-flow quality when available.
- Peer comparisons use comparable business models, geography, size, growth, margin, and accounting basis when possible.
- Valuation work states price date, market data date, assumptions, sensitivities, and sanity checks.
- Missing or stale data is marked as a limitation, not filled by guesswork.

## Outputs

Return the form the user asks for: concise explanation, metric table, ratio interpretation, financial health review, variance analysis, forecast critique, valuation assumption review, risk notes, diligence questions, or handoff context. Do not force a fixed template when the user only needs the analysis process or a short answer.

## Boundary

Skill owns financial statement understanding, metric definitions, ratio interpretation, trend analysis, financial health review, cash-flow quality, forecast reasonableness, valuation support, and risk flagging from available data.

This Skill does not provide investment advice, accounting advice, tax advice, legal advice, audit assurance, trade recommendations, or financial guarantees. It does not decide suitability, approve filings, authorize transactions, or replace human professional review.

It must not run shell, Python, Node, npm, curl, MCP, trading, brokerage, banking, market-data, spreadsheet, Office, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/statement-analysis-rules.md`: financial statement analysis modes, ratio definitions, cash-flow checks, variance logic, and data-quality cautions.
- `references/valuation-rules.md`: DCF, comparable valuation, sensitivity, and valuation-boundary rules.
- `LICENSE`: source and license notice.
