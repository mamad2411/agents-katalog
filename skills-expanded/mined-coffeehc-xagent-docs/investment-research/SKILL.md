---
name: investment-research
description: Use when researching an investment opportunity, company, security, sector, market, industry trend, thesis, diligence question, earnings event, valuation context, catalysts, risks, or investment memo from available evidence. Prefer this Skill for source-grounded investment research workflow, not personalized advice, trade execution, portfolio management, or pure financial statement calculation.
meta:
  version: 1
  display_name: 投资研究
  source: claude-office-skills investment-memo, company-research, stock-analysis; alirezarezvani/claude-skills financial-analyst
  license: MIT
---

# Investment Research

## Purpose

Conduct source-grounded investment research by defining the research question, collecting and qualifying evidence, analyzing business quality, market context, financial support, valuation, risks, catalysts, and unresolved diligence items.

This Skill adapts open-source investment memo, company research, stock analysis, and financial analysis practices for XAgent while removing analytics, market-data, MCP, Office, spreadsheet, and script assumptions. It provides research workflow only.

## Use When

Use for:

- researching a company, security, fund target, sector, industry, market theme, earnings event, financing event, or transaction candidate;
- building or reviewing an investment thesis, diligence memo, research note, market view, catalyst map, risk review, or monitoring plan;
- comparing investment opportunities, peer groups, business models, competitive positions, or valuation context;
- turning financial analysis, company documents, news, filings, transcripts, or user-provided notes into an evidence-backed research view;
- identifying diligence questions, open risks, missing evidence, and next research steps.

Use `financial-statement-analysis` when the main work is interpreting financial statements, ratios, cash flow, or valuation mechanics. Use `research-synthesis` when the task is broad multi-source evidence gathering without an investment-specific decision lens.

## Do Not Use When

Do not use for:

- personalized financial planning, suitability assessment, legal advice, tax advice, accounting advice, or regulated investment recommendation;
- executing trades, placing orders, moving money, selecting a broker, or managing accounts;
- portfolio construction, rebalancing, quantitative backtesting, or risk model execution;
- guaranteeing returns, predicting prices with certainty, or issuing professional ratings;
- live market-data retrieval or external source access unless an XAgent tool explicitly provides that capability.

## Material Gate

Before researching, identify:

- target company, asset, security type, sector, geography, market, and time horizon;
- research purpose: education, internal memo, diligence, comparison, monitoring, event analysis, or scenario review;
- source scope: provided documents only, web research, filings, transcripts, news, data tables, user notes, or prior analysis;
- required freshness: filing period, market-data date, event date, news cutoff, and whether current data is needed;
- constraints and assumptions: mandate, objective criteria, comparable universe, valuation method, risk categories, and unavailable evidence.

If key evidence is missing, preserve the research structure and mark `待确认`. Do not invent financial data, market prices, peer performance, management claims, regulatory facts, or source citations.

## Workflow

1. Define the research question, user objective, scope, time horizon, and what decision the research can and cannot support.
2. Separate research framing from advice: do not infer personal suitability, transaction timing, or required allocation.
3. Build a source plan using `references/investment-research-rules.md`. Use primary and time-stamped sources where possible, and treat stale or secondary sources as lower confidence.
4. Analyze the business: model, revenue drivers, customers, unit economics when available, competitive position, management, governance, market size, and industry structure.
5. Analyze financial support. If the task requires statement work, invoke `financial-statement-analysis` for ratios, cash-flow quality, forecast assumptions, and valuation mechanics.
6. Analyze valuation context: method, assumptions, peer set, scenario range, market-data date, and where the view is sensitive.
7. Build the thesis and counter-thesis: evidence supporting the opportunity, evidence against it, alternative explanations, risks, catalysts, monitoring indicators, and open questions.
8. Use `references/diligence-rules.md` for private-company, public-equity, credit, sector, or event-specific diligence prompts.
9. Frame conclusions as research findings, diligence status, scenarios, or monitoring points rather than instructions to buy, sell, hold, allocate, or trade.
10. Make unresolved items visible so another agent or human reviewer can continue the work.

## Checks

- Sources, dates, and freshness limits are visible for material claims.
- Primary evidence is preferred over unsourced summaries when available.
- The thesis includes counter-evidence, risks, and what would change the view.
- Financial claims are either sourced, calculated with visible formulas, or marked `待确认`.
- Valuation views state method, price date, assumptions, sensitivity, and uncertainty.
- Catalysts are separated from already-known facts and from speculative hopes.
- The output does not personalize advice, guarantee returns, or tell the user to transact.
- High-impact or regulated use is explicitly left for qualified human review.

## Outputs

Return whatever the user needs: investment research note, diligence memo, thesis summary, company research brief, sector view, risk register, catalyst map, monitoring checklist, valuation context, peer comparison, open-question list, or handoff context. Do not force a fixed output format when the user only needs workflow guidance or a concise research answer.

## Boundary

Skill owns investment research workflow, evidence planning, business and market analysis, thesis construction, counter-thesis, risk framing, catalyst mapping, diligence questions, valuation context, and research-quality checks.

This Skill does not provide personalized investment advice, legal advice, tax advice, accounting advice, fiduciary advice, trade recommendations, broker selection, portfolio management, or financial guarantees. It does not authorize transactions, access accounts, move funds, or replace professional judgment.

It must not run shell, Python, Node, npm, curl, MCP, trading, brokerage, banking, market-data, CRM, email, Office, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/investment-research-rules.md`: source hierarchy, research modes, thesis construction, risk categories, and recommendation-language boundaries.
- `references/diligence-rules.md`: diligence prompts for public equity, private investment, credit, sector, and event research.
- `LICENSE`: source and license notice.
