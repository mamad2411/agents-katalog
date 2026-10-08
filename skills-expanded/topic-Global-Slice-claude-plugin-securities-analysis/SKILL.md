---
name: securities-analysis
version: "1.0"
description: Guides analysis of Slice securities through MCP securities search, find, list, get, valuation, tax-treatment, and vesting timeline tools. Use when answering questions about grants, shares, warrants, convertibles, stakeholder securities, security status, quantities, IDs, tax treatments, valuations, or vesting timelines from Slice MCP data.
---

# Securities Analysis

## Scope

Use for any security type (grants, shares, warrants, convertibles) and vesting timelines. For employee grant compensation, exercise, or PTEP focus, prefer equity-compensation-analysis. For company ownership totals, use cap-table-analysis. For compliance tickets, use compliance-analysis.

## Ground Truth And Defaults

Slice data is the source of truth for any specific company, stakeholder, grant, share, warrant, or convertible. Stay scoped to the authenticated company tenant and keep every query on the same as-of `date` when possible.

Only use domain defaults as a last resort after retrieval and clarification are exhausted. Defaults that may be used transparently: the grantor is a private company, awards are equity-based, an unspecified instrument is a stock option only for a specific record, and a generic non-qualified tax treatment applies unless Slice data or the user says otherwise. State any assumption you use.

## Tool Selection

Use the securities tools in this order:

1. Start with `securities_search` for broad discovery across grants, shares, warrants, and convertibles. Prefer compact filters: `stakeholderName`, `stakeholderId`, `securityType`, `status`, and `date`.
2. Use `securities_find` when the user asks for one security type with structured filters such as stakeholder, beneficiary, date range, status, grant type, equity plan, or share class.
3. Use `securities_list` only when the user really wants all rows of one security type and no filters apply.
4. Use `securities_get_one` for full details after narrowing to a small set of internal UUIDs.
5. Use `securities_get_by_customer_facing_ids` when the user provides customer-facing IDs instead of internal UUIDs.
6. Use `valuations_list` / `valuations_get_one` when exercise price, FMV, 409A, or grant-date valuation compliance matters.

All securities pagination is bounded. Use `limit` up to 50 and advance `offset` while `hasNext` is true.

## Grant And Award Mechanics

For grants, always distinguish the award type because it drives cap-table and tax behavior:

- `option`: right to buy shares at an exercise price; cap table impact occurs on exercise.
- `rsu`: promise of shares at settlement; no exercise price.
- `rsa`: shares issued immediately subject to forfeiture.
- `sars`, `phantomStock`, `piu`: may be cash-settled or non-corporate interests; do not assume share-register dilution.
- `growthShares`: share-like award with a hurdle; often immediate cap-table impact.

For fully diluted analysis, include share-settled outstanding grants, warrants, and convertibles as appropriate, but do not double-count exercised grants because they are already shares. For departed stakeholders, check status, expiry, and PTEP implications before treating vested options as actionable.

## Tax Treatment And Valuation Checks

When tax, compliance, or exercise price is part of the question, surface these fields when available: grant date, grant type, exercise price, tax treatment, stakeholder tax residence at grant, valuation/FMV effective at grant date, and vesting or exercise status.

Exercise price requirements are anchored to FMV in many regimes. Missing or stale valuation data can be a compliance risk. Do not infer a qualified regime such as ISO, EMI, BSPCE, or Section 102 unless Slice data or the user identifies it.

## Large Requests

Filter in MCP calls; aggregate compact search/find rows before fetching full records. Page with `limit: 50` and `offset` while `hasNext` is true. Summarize in chat; for full exports, note file-report is the right shape — do not dump raw arrays.

## Vesting Timeline

`securities_get_one` supports `includeVestingTimeline: true` for grants, shares, and warrants. Use it when the user asks about tranche-level vesting, vesting schedules, future vesting, pause/acceleration effects already reflected in the record, or event logs.

Do not request vesting timelines for convertibles; they are unsupported. For quick grant vesting summaries, `grants_get_vesting_bullet_chart` gives vested, unvested, and exercisable breakdown for one grant. Use `securities_get_one` with `includeVestingTimeline: true` when the full tranche-level timeline is needed.

For many vesting timelines, first identify the small target set with `securities_search` or `securities_find`, then fetch timelines one by one only for securities that require tranche-level analysis. Aggregate the timeline facts before answering; do not paste every tranche unless the user explicitly asks for a specific security's timeline.

## Response Style

Answer from aggregated findings: counts, totals, notable exceptions, and a short list of representative securities or IDs. Label calculation mode when relevant: outstanding, fully diluted, vested-only, or as-of date. Mention permission-scoped empty results carefully: an empty response can mean no matching securities or no read access for that security type.
