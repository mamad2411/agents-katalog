---
name: equity-compensation-analysis
version: "1.0"
description: Guides Slice MCP analysis of equity compensation, grants, options, RSUs, vesting, exercises, forfeitures, PTEP, tax treatments, and valuations. Use when answering questions about employee equity, grant positions, vested or exercisable quantities, exercise price, FMV/409A, option pool consumption, tax treatment, or award-type mechanics.
---

# Equity Compensation Analysis

## Scope

Use for employee grant compensation, vesting, exercise, PTEP, and tax treatment. For warrants, convertibles, or non-grant securities, use securities-analysis. For company-wide cap table or ESOP pool totals, use cap-table-analysis.

## Ground Truth And Clarification

For a specific person, grant, or event, retrieve Slice data before relying on general knowledge. Ask for missing variables when they materially change the answer: jurisdiction, grantee classification, tax residence, employing entity, award type, tax treatment, grant date, exercise/vesting date, or public/private company status.

Use defaults only as a last resort and state them: private company grantor, equity-based award, direct employee, non-qualified/local tax treatment, no cross-border mobility, and stock option when an exercise event is specifically referenced.

## Grant Workflow

1. Resolve the stakeholder with `stakeholders_search_by_name` or `stakeholders_get_by_customer_facing_ids` when the user names a person or entity.
2. Use `securities_find` with `securityType: "grant"` for filtered grant discovery by stakeholder, beneficiary, date range, status, grant type, equity plan, or share class.
3. Use `securities_get_one` for full grant details after narrowing to a small set.
4. Add `includeVestingTimeline: true` when the user asks for vesting tranches, vesting over time, future vesting, acceleration, pauses, or event-log context.
5. Use `grants_get_vesting_bullet_chart` for a quick single-grant vested/unvested/exercisable breakdown.
6. Use `valuations_list` or `valuations_get_one` when FMV, 409A, exercise price, or grant-date valuation compliance matters.

## Award-Type Mechanics

Award type drives the answer:

- Stock options: right to buy shares at exercise price; taxable event often exercise; cap-table impact on exercise.
- RSUs/performance rights: no exercise price; taxable event usually settlement or delivery; cap-table impact on share issuance.
- RSAs: shares issued immediately, subject to forfeiture; tax may arise at grant or vesting depending on elections/regime.
- SARs and phantom stock: often cash-settled; do not assume cap-table dilution.
- Growth shares: shares with a hurdle; often immediate cap-table impact.
- PIUs: partnership interests for LLC/partnership structures; do not treat as ordinary corporate shares without data support.

When computing fully diluted positions, include share-settled outstanding awards but avoid double-counting exercised awards that have become shares.

## Vesting, Exercises, And Forfeitures

For vested or exercisable questions, check grant quantity, vesting start date, schedule, cliff, vested quantity, exercised/settled quantity, cancellations, expiry, stakeholder termination, and PTEP. For departed stakeholders, vested options may expire if the PTEP window has closed.

For exercise questions, confirm the quantity is vested and unexpired, then relate exercise cost to `exercisePrice * quantity`. If the user asks about tax, identify the tax treatment and jurisdiction before giving more than a general explanation.

## Tax Treatment And Valuation

Tax treatment is jurisdiction-specific and depends on the grantee, employing entity, award type, and grant terms. Common qualified regimes include US ISO, UK EMI/CSOP, Israel Section 102, France BSPCE, and Australia Start-Up Concession. Non-qualified/local treatment is the fallback when qualification is not supported by Slice data or the user.

Many regimes require exercise price to be at least FMV on the grant date. Use valuation tools to check the relevant FMV record and effective date. Missing, stale, or mismatched valuation data should be flagged as a compliance risk, not silently filled.

## Output

For a stakeholder grant position, summarize totals first: total granted, vested, unvested, exercised/settled, outstanding, exercisable, expiry/PTEP risk, and grant-type mix. Then show per-grant highlights only for the relevant grants. Label the as-of date and assumptions.
