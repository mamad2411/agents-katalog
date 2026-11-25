---
name: cap-table-analysis
version: "1.0"
description: Guides Slice MCP cap-table and ESOP-pool analysis by combining company summary, cap table, ownership, stakeholder, share class, funding round, equity pool, valuation, and securities tools. Use when answering questions about cap table structure, stakeholder holdings, ownership, ESOP pools, share classes, rounds, dilution, option pools, or securities at company or stakeholder level.
---

# Cap Table Analysis

## Scope

Use for company or stakeholder ownership, ESOP pools, share classes, and rounds. For single-security deep dives or vesting timelines, use securities-analysis. For employee grant compensation or PTEP, use equity-compensation-analysis. For exit proceeds, use waterfall-analysis.

## Ground Truth And Calculation Modes

Slice data is the source of truth for specific cap-table answers. Stay scoped to the authenticated company tenant and keep every analysis anchored to the same as-of `date` when possible.

Always label the calculation mode:

- Outstanding: issued shares on the legal share register.
- Fully diluted: issued shares plus share-settled grants, warrants, and convertibles where applicable.
- As-converted: preferred shares converted into ordinary-equivalent shares using the current conversion ratio.

Use assumptions only as a last resort and state them. Common defaults are private company, current tenant only, and equity-based awards.

## Company-Level Workflow

For cap-table-wide questions:

1. Use `companies_get_summary` for a one-shot company snapshot: company identity, total stakeholders, total grants, outstanding and fully diluted shares, and ESOP pool breakdown.
2. Use `cap_table_get_summary` for cap-table aggregates: company outstanding, company fully diluted, total available pool, totals by security type, and totals by share class.
3. Use `ownership_get_company_breakdown` when the question is specifically about outstanding vs fully diluted ownership totals.
4. Use `share_classes_list` and `rounds_list` to explain the share-class and funding-round structure behind the cap table.
5. Use `rounds_get_total_raised` only after discovering the round's share class IDs with `rounds_list`.
6. Use `cap_table_search_entries` for paginated per-stakeholder cap-table rows when aggregate totals are not enough.

Prefer `cap_table_get_summary` before `cap_table_search_entries`; it is cheaper and already includes the high-level share-class and security-type breakdowns.

## Stakeholder-Level Workflow

For questions about one stakeholder:

1. Resolve the stakeholder first with `stakeholders_search_by_name` or `stakeholders_get_by_customer_facing_ids`.
2. Use `ownership_get_stakeholder_breakdown` for that stakeholder's outstanding and fully diluted ownership. Set `includeBeneficiaryShares` intentionally based on the user's question.
3. Use `stakeholders_get_holdings` for the stakeholder's flattened securities across grants, shares, warrants, and convertibles.
4. Use `cap_table_search_entries` with `stakeholderId` when the user wants cap-table rows with share-class names, outstanding units, fully diluted units, status, and customer-facing IDs.
5. Use `securities_get_one`, `securities_find`, or `securities_get_by_customer_facing_ids` only for the specific securities that need full records.

When comparing a stakeholder to the whole company, pair `ownership_get_stakeholder_breakdown` with `ownership_get_company_breakdown` or `cap_table_get_summary` using the same date. For funds or investors that may invest through multiple entities or SPVs, check whether several Stakeholder records should be aggregated before reporting investor-level ownership.

## ESOP Pools

Equity Pool and Equity Plan are different: the pool is authorized headroom, while the plan is the rulebook for grants. For ESOP or equity-pool questions:

- Use `companies_get_summary` for company-wide ESOP pool totals and a compact pool breakdown.
- Use `equity_pools_get_summaries` for per-pool `poolId`, name, size, allocated, available, promised, and type at a date.
- Use `cap_table_get_summary` when the ESOP question needs `totalAvailablePool` alongside company outstanding and fully diluted totals.
- Use `securities_find` with `securityType: "grant"` and relevant grant filters when the user asks which grants or stakeholders consume pool capacity.

Report pool utilization as aggregated figures first: size, allocated, available, promised, and utilization percentage when calculable. Do not recompute pool availability from raw grants unless the tool output is insufficient; if you must reason manually, account for granted outstanding, exercises/settlements, cancellations/expirations returning to the pool, and any pool rules such as sold units being removed.

## Share Classes, Rounds, And Secondaries

Use share-class and round tools as reference data for cap-table interpretation:

- `share_classes_list` maps share class IDs to names and terms for the current date.
- `share_classes_get_one` fetches a full share-class record when one class needs deeper explanation.
- `share_classes_get_events` explains historical changes for a single share class.
- `rounds_list` maps funding rounds to their associated share classes.
- `rounds_get_display_data` is enough for selector-style round names and IDs.
- `rounds_get_total_raised` needs a comma-separated set of share class IDs discovered from `rounds_list`.

Founder shares issued at nil or nominal consideration are normal formation shares, not an error. At round close, distinguish primary issuances from secondary transfers: primary issuances create new shares and cash goes to the company; secondaries transfer existing shares and cash goes to the seller.

## Data Quality Checks

Watch for reversed or corrected events, multiple stakeholder entities for the same economic investor, stale valuations, tax-treatment mismatches, expired PTEP windows, anti-dilution conversion ratios, and pool expansion events. Event logs explain audit/workflow history; use current/as-of records and tool aggregates for state and ownership calculations.

## Large Requests

Start with summary tools (`companies_get_summary`, `cap_table_get_summary`, `ownership_get_company_breakdown`, `equity_pools_get_summaries`). Filter and page `cap_table_search_entries` with `limit: 50`. Summarize in chat; for full exports, note file-report is the right shape — do not dump raw arrays.

## Response Style

Answer with the level of detail implied by the question: company totals for cap-table questions, per-pool summaries for ESOP questions, and stakeholder ownership plus holdings for stakeholder questions. Call out permission-scoped `null` or empty results: they can mean the caller lacks access, not necessarily that the data does not exist.
