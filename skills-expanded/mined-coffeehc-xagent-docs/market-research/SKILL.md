---
name: market-research
description: Use when researching or summarizing a market, industry, competitor landscape, customer segment, trend, category, TAM/SAM/SOM assumption, market entry opportunity, positioning space, or competitive differentiation. Prefer this Skill when the task needs market structure, competitors, buyers, demand signals, risks, and source-grounded conclusions. Do not use for simple fact lookup, investment advice, or unsupported market-size certainty.
meta:
  version: 3
  display_name: 市场研究
---

# Market Research

## Purpose

Turn market information into a clear view of category structure, customers, competitors, demand signals, risks, and opportunities.

## Use When

Use for:

- market landscape
- competitor overview
- customer segment research
- trend analysis
- market entry assessment
- positioning research
- TAM/SAM/SOM assumption framing

## Material Gate

Identify:

- geography, industry, segment, time horizon, and research question
- target customers, competitors, substitutes, and channels
- available sources and freshness needs
- whether output should be neutral research, opportunity brief, or report

If sources are not current or complete, mark coverage gaps.
If the task asks for industry analysis, market landscape, competitor research, concrete cases, current opportunities, ratings, or recommendations, treat source discovery and evidence retrieval as required. `http_request` and `web_fetch` only retrieve known URLs; they are not enough for unknown-source market discovery. If no search/source-discovery tool is visible, use `tools_find` when available, ask for source material, or report an evidence blocker instead of relying only on model memory.
If the task asks for a final report, treat final presentation as a separate capability from market analysis. Use `skills_find` / `skills_load` for `html-report-builder` or an equivalent visual report Skill when available. Use this Skill for market judgment; use the report Skill for final user-facing packaging.

## Workflow

1. Define market boundary and segmentation.
2. Build an evidence plan: source types, freshness need, required examples/cases, and minimum corroboration.
3. Gather or inspect source material through currently visible tools. If unknown-source discovery is needed, find a real search/retrieval capability before synthesis.
4. Identify buyers, users, jobs-to-be-done, and buying triggers from evidence.
5. Map competitors, substitutes, and adjacent categories.
6. Extract demand signals, growth drivers, constraints, and regulatory or macro risks.
7. Compare positioning and differentiation opportunities.
8. State confidence, source coverage, and next research needs.
9. For deep multi-source evidence, concrete case analysis, conflicting sources, or citeable conclusions, use `skills_find` / `skills_load` for `research-synthesis` or an equivalent evidence synthesis Skill when available.
10. For market landscape reports, use `skills_find` / `skills_load` for `html-report-builder` or an equivalent visual report Skill when available, then build the final self-contained HTML report from the market findings and evidence ledger.
11. Keep Markdown for source logs, drafts, and intermediate analysis unless the user explicitly asks for Markdown as the final format.

## Checks

- Market definition is not too broad.
- Competitors include direct, indirect, and manual alternatives.
- Trend claims include source dates when available.
- Market sizing is assumption-based unless backed by sources.
- Opportunity is separated from evidence.
- Ratings and recommendations show evidence basis, assumptions, confidence, and gaps.
- Source-backed reports include real source URLs, workspace source refs, or concrete tool/raw refs. Do not mark a market research task complete as source-backed when evidence refs are only self-authored artifacts.

## Outputs

- market landscape
- competitor matrix
- customer segment profile
- trend brief
- market entry assessment
- positioning map
- market research report

## Boundary

This Skill owns market framing, competitor structure, demand signal synthesis, and opportunity mapping. It does not own live data collection, paid database access, investment advice, pricing execution, or guaranteed market forecasts.

It must not run shell, Python, Node, npm, curl, MCP, browser automation, market database, CRM, ads, scraping, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
