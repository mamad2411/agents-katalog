---
name: reconciliation
description: Reconciles GL balances against subledgers, bank statements, intercompany counterparties, and third-party data sources — produces a structured rec workpaper, categorized reconciling-item register, aging analysis, materiality assessment, and recommended adjusting journal entries with preparer/reviewer trail. Make sure to use this skill whenever the user says reconcile [account], bank rec, GL-to-subledger tie-out, intercompany rec, find what doesn't tie, what's the AR/AP/cash difference, build a rec workpaper, age the open items, identify reconciling items, prove out the [account] balance, or describes any process of comparing two financial sources to find and explain differences. Specifically tuned for Puerto Rico (Hacienda withholding clearing, IVU sales-tax payable, local bank statements, patente municipal accruals) and cybersecurity-startup contexts (Stripe/payment-processor recs for MSSP recurring billing, deferred revenue for multi-year SaaS, milestone-based pen test billings, cyber-insurance recoverable accounts, sub-processor pass-through clearing). Do NOT use for: booking the resulting JE (defer to finance:journal-entry — this skill recommends, that skill posts), generating P&L / BS / CF (defer to finance:financial-statements), explaining why a number changed period-over-period or vs. budget (defer to finance:variance-analysis), SOX-specific control testing of the reconciliation control itself (defer to finance:audit-support / finance:sox-testing), orchestrating the full close calendar (defer to finance:close-management), or general non-financial data comparison (defer to data:analyze).
argument-hint: "<account> [period]"
---

# Reconciliation

Account reconciliation — bank, GL-to-subledger, intercompany, and third-party — producing audit-ready workpapers and adjusting-entry recommendations.

**Important:** This skill assists with workflows. All reconciliations must be reviewed and signed off by a qualified financial professional before close.

## When to use vs. adjacent skills (defer matrix)

| Situation | Skill |
|---|---|
| Comparing GL ↔ bank, subledger, IC counterparty, or third party | **this skill** |
| Booking the adjusting JE that this rec recommends | `finance:journal-entry` |
| Building the full P&L / BS / CF | `finance:financial-statements` |
| Explaining "why did cash drop $X vs. last month / vs. budget" | `finance:variance-analysis` |
| Orchestrating the whole close (calendar, dependencies) | `finance:close-management` |
| Testing the rec control for SOX evidence | `finance:audit-support` / `finance:sox-testing` |
| Generic two-dataset diff with no GL context | `data:analyze` |

This skill **chains to** `finance:journal-entry` when an adjustment is required and is **orchestrated by** `finance:close-management` during the monthly close.

## Reconciliation types

### Bank reconciliation
GL cash account ↔ bank statement.

Standard reconciling items:
- Outstanding checks (issued, not yet cleared)
- Deposits in transit (received, not yet posted by bank)
- Bank charges / wire fees not booked
- Interest income not booked
- ACH/Stripe/processor settlements in transit
- Bank or book errors

**PR specifics:** major local banks (e.g., the dominant retail banks in PR) statements close on the last calendar day; reconciliations should pull the official monthly statement, not a mid-cycle snapshot. Hacienda withholding (7% professional services, 10% rent, etc.) hits a separate clearing account that must be reconciled to Form 480 filings.

### GL-to-subledger
GL control account ↔ detailed subledger.

Common pairs:
- AR control ↔ AR aging
- AP control ↔ AP aging
- Fixed assets ↔ FA register / depreciation schedule
- Inventory ↔ inventory valuation
- Prepaid ↔ amortization schedule
- Deferred revenue ↔ contract/waterfall schedule
- Accrued liabilities ↔ accrual support schedules

**Cybersec-startup specifics:**
- **Deferred revenue:** Multi-year SaaS / MSSP contracts — subledger is the revenue waterfall; reconcile invoiced-not-yet-earned to GL deferred balance.
- **Unbilled AR (contract assets):** Milestone pen test fees where work delivered before invoice — separate sub-account, reconciled to project burn report.
- **Sub-processor pass-throughs:** AWS, Cloudflare, Datadog charges re-billed to clients — clearing account should net to ~$0 each period.

### Intercompany
Entity A's IC payable ↔ Entity B's IC receivable. Must net to $0 on consolidation.

Standard items: timing, FX, transfer-pricing markup, one-sided entries.

### Third-party
Internal records ↔ external statement (Stripe, Gusto/Justworks payroll, brokerage, cyber-insurance carrier).

Standard items: cut-off, fees, refunds, chargebacks, reversals on either side.

**Cybersec-startup specifics:**
- **Stripe/payment processor:** Reconcile Stripe gross → fees → net deposit to bank → revenue recognized. Settlement timing differences are normal.
- **Cyber-insurance recoverable:** When a covered incident triggers a claim, the recoverable asset must reconcile to the carrier's adjuster letter, not just internal estimates.

## Standard rec workpaper (output template)

```markdown
# Reconciliation: [Account #/Name] — [Period YYYY-MM]
Prepared by: [Name]   Date: [YYYY-MM-DD]
Reviewed by: [Name]   Date: [YYYY-MM-DD]
(Bilingual EN/ES note if filing requires — see PR section)

## Source A: [Internal — usually GL]
- Account: [#] [Name]
- Balance: $X     As of: [date]
- Source: [GL extract reference / report ID]

## Source B: [External — bank / subledger / counterparty]
- Source: [Statement #, vendor, system]
- Balance: $Y     As of: [date]

## Difference: A − B = $Z

## Reconciling items

| # | Date | Description | Amount | Side | Category | Age (days) | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | YYYY-MM-DD | Outstanding check #1234 | (500) | A | Timing | 5 | AP | Open |
| 2 | YYYY-MM-DD | Local-bank wire fee not booked | (25) | B | Adjustment needed | 0 | GL | JE recommended |

## Adjusted balances
A adjusted: $X_adj   B adjusted: $Y_adj   Variance: $0 (or explained)

## Recommended adjusting JEs (chain to finance:journal-entry)
| DR | CR | Amount | Memo |
|---|---|---|---|
| 6810 Bank fees | | 25 | Local-bank wire fee Apr-26 |
| | 1010 Cash – BPPR opg | 25 | |

## Aging of unresolved items
0–30 / 31–60 / 61–90 / 90+ — items in 60+ flagged.

## Materiality assessment
Threshold applied: $X (basis: __% of [pretax income / total assets / cash])
Items above threshold: [list]   Items aggregated below: $X total

## Conclusion
- All differences explained: [Y/N]
- Material unresolved: [None / list]
- Recommended action: [Clean / Adjust per JEs above / Investigate / Escalate]
- Sign-off chain: Preparer → Reviewer → Controller (if material)
```

## Reconciling-item categorization (5 categories)

| Category | Definition | Resolution |
|---|---|---|
| **Timing** | Will clear naturally next cycle | Monitor, do not book |
| **Adjustment needed** | Books are wrong | Recommend JE → `finance:journal-entry` |
| **External error** | Counterparty / bank / vendor wrong | Contact, document, follow up |
| **Documentation** | Neither wrong, rec needs more support | Attach evidence, no JE |
| **Investigation** | Unknown root cause | Dig in, escalate if aged or material |

## Materiality discipline

Apply the entity's documented threshold. When undocumented, defaults for a Series A/seed cybersec startup:

| Account class | Default threshold | Basis |
|---|---|---|
| Bank | greater of $100 or 0.1% of balance | Operating cash sensitivity |
| GL ↔ subledger | greater of $1,000 or 0.5% of balance | Detail-level signal |
| Intercompany | greater of $5,000 or 1% of balance | Eliminates anyway |
| Deferred revenue | greater of $2,500 or 0.25% of ARR | Revenue-cycle sensitivity |
| Cyber-insurance recoverable | $0 — always investigate | Audit-sensitive |

**Aged-item escalation (mandatory):**
- 30+ days unresolved → owner follow-up logged
- 60+ days → supervisor / controller review
- 90+ days → CFO / management escalation; consider write-off memo
- Recurring same-item across 3+ periods → process-defect investigation, not just rebooking

## Puerto Rico specifics

- **IVU sales-tax payable** (state 10.5% + municipal 1%): reconcile GL balance to SURI filing; SURI uses calendar month; verify nexus rules for SaaS sales.
- **Hacienda withholding clearing accounts:** one per withholding type (7% pro services, 10% rent, 29% non-resident). Reconcile monthly to Form 480 filings; balance after filing should be $0.
- **Patente municipal accrual:** annual but accrue monthly 1/12; reconcile YTD accrual to last filed declaration.
- **Act 60 / 20 / 22 entities:** if exempt-eligibility tracking applies, deferred-tax recs use the decreed rate (e.g., 4%), not statutory 37.5%.
- **Bilingual workpapers:** for filings going to Hacienda or municipal authorities, include a Spanish summary block (Cuenta, Saldo, Diferencias, Conclusión). Internal recs may stay English-only.

## Anti-patterns (auto-flag)

- "Plug to balance" JE with no detail
- Stale recs (prior period not closed before current period starts)
- No reviewer signature
- Aged items >90 days carried period after period
- Timing items booked as adjustments
- Round-number plugs ($1,000.00 with no source)
- Reverse-engineering items to match a target difference

## Output

1. Completed rec workpaper (template above)
2. Recommended JEs in finance:journal-entry handoff format
3. Aged-items report
4. Materiality assessment per item + aggregate
5. Sign-off chain populated
6. Next-action recommendation (clean / adjust / investigate / escalate)
7. PR-filing bilingual block when applicable
