---
name: board-presentation-analysis
version: "1.0"
description: Guides creation of board-ready Slice presentations using MCP tools, especially offered-status grants and ESOP/equity-pool summaries. Use when preparing board decks, board approval packs, grant approval summaries, ESOP pool updates, option pool utilization slides, or board-facing equity recommendations.
---

# Board Presentation Analysis

## Scope

Use for board decks and grant-approval packs. For company cap-table totals without a board format, use cap-table-analysis. For compliance posture without board context, use compliance-analysis. For workflow status only, use workflows-analysis.

## Core Principle

Board materials should be concise, decision-oriented, and traceable to Slice data. Use the same as-of `date` across all tools when possible. Lead with the decision the board needs to make, then show the supporting grant and ESOP pool data.

Do not dump raw tool responses into the presentation. Aggregate first, show board-relevant tables, and keep full records or long grant lists in an appendix or future file report/export.

## Required Data Pull

For a standard grant approval / ESOP pool board update:

1. Fetch all offered grants with `securities_find`:
   - `securityType: "grant"`
   - `status: "offered"`
   - `limit: 50`
   - page with `offset` while `hasNext` is true
2. Fetch ESOP/equity-pool summaries with `equity_pools_get_summaries` for the same as-of date.
3. Fetch `cap_table_get_summary` when the board needs company fully diluted, outstanding, or total available pool context.
4. Fetch `companies_get_summary` when a one-shot company and ESOP overview is enough or when board materials need company-level totals.
5. Use `grants_get_types_breakdown` or `grants_get_pizza_tracker` for aggregate grant lifecycle context if the deck needs a company-wide grant pipeline view.

Only call `securities_get_one` for specific offered grants that need full terms, documents, vesting details, valuation, or tax-treatment context.

## Offered Grants Section

Use offered grants to build a proposed approval table. Include only fields needed for board review:

- Stakeholder name and stakeholder/customer-facing ID when available.
- Grant customer-facing ID and internal ID for traceability.
- Grant type.
- Quantity / total granted.
- Equity plan or share class when available.
- Grant date or proposed date when available.
- Vesting summary when available or required.
- Tax treatment and country only when relevant for approval or compliance.

Aggregate the offered grants before listing details: total offered units, number of grants, grant-type breakdown, stakeholder count, share-class or equity-plan breakdown, and largest proposed grants. If there are many offered grants, put only summary and top/notable rows in the main deck and keep the full list for appendix/export.

## ESOP Pool Section

Use `equity_pools_get_summaries` for each pool's name, size, allocated, available, promised, and type. For each pool, calculate utilization percentages when the inputs are present:

- allocated / size
- available / size
- promised / size
- offered grants impact / size, if offered grants can be tied to the pool or plan from returned data

Do not infer a pool-to-plan relationship unless the returned grant or pool data supports it. If offered grants cannot be tied to specific pools, present offered grant totals separately from per-pool utilization and say the pool attribution is not available from the retrieved fields.

## Recommended Board Deck Shape

Use this structure unless the user asks for another format:

1. Executive summary: key decisions, total offered grants, total offered units, ESOP pool availability, and any risks.
2. Proposed grant approvals: aggregate totals plus a concise table of offered grants.
3. ESOP pool status: per-pool size, allocated, promised, available, and utilization.
4. Cap-table impact: fully diluted/outstanding context from `cap_table_get_summary` when relevant.
5. Compliance and process checks: only include compliance tickets or workflow status if the board needs blockers before approval.
6. Appendix: full offered grant list, assumptions, as-of date, and tool filters used.

## Optional Checks

- Use `compliance_get_object_tickets` for specific offered grants if the board asks about approval blockers or compliance issues.
- Use `workflows_list` with `type: "corporateApproval"` or `type: "grantLetter"` when the board asks about approval/signature process status.
- Use `valuations_list` when exercise price or FMV support is a board concern.
- Use `share_classes_list` and `rounds_list` when offered grants need to be explained in broader share-class, round, or dilution context.

## Response Style

Write in board-ready language: concise, neutral, and decision-focused. State the as-of date, filters used, and any assumptions. Separate facts from recommendations. If there is too much data for chat, provide the slide outline and summarized tables, then note that the full offered-grant appendix should be generated as a file report/export when that tool is available.
