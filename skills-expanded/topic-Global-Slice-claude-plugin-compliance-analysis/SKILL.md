---
name: compliance-analysis
version: "1.0"
description: Guides Slice MCP compliance analysis using compliance ticket breakdowns and object-level compliance tickets, plus related stakeholder, securities, equity plan, equity pool, valuation, tax-treatment, and cap-table tools. Use when answering questions about company compliance posture, compliance tickets, missing data, overdue issues, severity, affected objects, stale valuations, tax treatment issues, or compliance status for a stakeholder, security, equity pool, equity plan, valuation, share, grant, or exercise request.
---

# Compliance Analysis

## Scope

Use for compliance tickets and posture. Not a substitute for legal advice. For workflow process status without compliance focus, use workflows-analysis. For cap-table totals without compliance tickets, use cap-table-analysis.

## Core Principle

Use compliance tools as a compliance-ticket interface, not as a raw data export. Start with the bounded aggregate breakdown, then retrieve full ticket records only for a specific object after identifying that object with the relevant domain tool.

Slice data and compliance tickets are the ground truth for a specific company. Do not replace ticket findings with general legal advice. Use domain knowledge to interpret why a ticket matters, and separate "the ticket says" from "the domain implication is".

## Tool Selection

1. Use `compliance_get_tickets_breakdown` first for company-level compliance posture. It returns fixed-size aggregates only: total, active, completed, archived, status counts, severity counts, object type counts, top issue groups capped to 10, and time-sensitive counts.
2. Use `compliance_get_object_tickets` only for one known object. It returns full ticket records for `objectId` and `objectType`, including status, comments, events, `ticketData`, due date, and metadata.
3. Use domain tools to resolve the object before calling object tickets: stakeholder tools for stakeholders, securities tools for grants and shares, equity-pool tools for equity pools, valuation tools for FMV records, cap-table tools for cap-table context, and exercise-request tools when available.

Do not call object-ticket retrieval broadly across many objects unless the user explicitly asks for detailed ticket bodies and the object set is small.

## Object Types

`compliance_get_object_tickets` requires an object ID and one of these ticket object types:

- `corporateApprovals`
- `exerciseRequests`
- `grants`
- `stakeholders`
- `valuations`
- `equityPools`
- `equityPlans`
- `shares`

Use the object type that matches the compliance object, not the endpoint family used to discover it. For example, a grant discovered through `securities_search` still uses `objectType: "grants"`.

## Company-Level Workflow

For questions like "what is our compliance status?", "what issues are open?", or "what are the biggest compliance risks?":

1. Call `compliance_get_tickets_breakdown`.
2. Report the high-level posture: total tickets, active/completed/archived counts, severity mix, object type concentration, overdue active count, and top issue groups.
3. Prioritize risk by active high-severity issues, overdue active issues, and repeated top issue groups.
4. If the user asks why a top issue exists, ask for or identify representative affected objects before fetching full ticket records.

Do not imply that the aggregate breakdown contains ticket bodies or per-object details. It is intentionally bounded.

## Object-Level Workflow

For questions about compliance for a specific object:

1. Resolve the object ID using the right tool. Examples: `stakeholders_search_by_name`, `stakeholders_get_by_customer_facing_ids`, `securities_search`, `securities_find`, `securities_get_by_customer_facing_ids`, `equity_pools_get_summaries`, `valuations_list`, or cap-table tools for context.
2. Call `compliance_get_object_tickets` with that object's ID and ticket object type.
3. Summarize the full tickets by status, severity, due date, title, description, and actionable `ticketData`.
4. Include comments and events only when they explain current state, ownership, or timing.

For stakeholder questions, check stakeholder-level tickets with `objectType: "stakeholders"` and, if needed, separately check tickets on that stakeholder's grants or shares after retrieving the stakeholder's securities.

## Domain Checks To Pair With Tickets

Compliance analysis often needs these context checks:

- Valuation and FMV: options usually require exercise price to be set at or above grant-date FMV under many regimes; stale or missing valuations are a common risk.
- Tax treatment: qualified regimes such as ISO, EMI, BSPCE, or Section 102 have strict eligibility, holding, filing, and grantee-status requirements. Do not assume qualification unless Slice data or the user confirms it.
- Grantee classification: direct employee, PEO, EOR, contractor, director, and advisor status can change eligibility and withholding obligations.
- Mobility and jurisdiction: tax residence, employing entity location, and cross-border workdays can materially change an answer. Ask rather than defaulting when those variables matter.
- PTEP and termination: departed stakeholders may have expired exercise windows or forfeited awards.

## Combining With Securities And Cap Table Tools

Compliance often needs business context:

- For grant or share compliance, use securities tools to identify the security and fetch full details only for the relevant IDs.
- For stakeholder compliance, use stakeholder tools and `stakeholders_get_holdings` to understand affected holdings before checking related object tickets.
- For equity-pool or ESOP compliance, use `equity_pools_get_summaries` and cap-table summaries to understand pool impact before fetching pool-specific tickets.
- For cap-table-level compliance posture, pair `compliance_get_tickets_breakdown` with `cap_table_get_summary` or `companies_get_summary` to explain business impact without fetching every ticket.

Keep the compliance answer separate from the cap-table or securities facts: identify what the compliance tickets say, then add the domain context used to interpret them.

## Large Requests

Default to `compliance_get_tickets_breakdown`. Fetch full object tickets only for a small example set. Summarize in chat; for full exports, note file-report is the right shape — do not dump raw ticket arrays.

## Response Style

Lead with current compliance posture and risk. Use concise sections such as totals, risk drivers, affected object types, overdue work, and recommended next checks. Call out permission failures carefully: forbidden or empty compliance responses can reflect missing `COMPLIANCE:READ` access rather than an absence of compliance issues.
