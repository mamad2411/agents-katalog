---
name: qbo-audit
description: >
  Contains verified AJE/RJE/PJE posting workflows (AuditAdjustment and MaterialityThresholds
  data structures), TrialBalanceRow extraction with debit/credit normal-balance logic, and
  TaxLineMapping tables for Form 1120 Page 1, Schedule L, M-1, M-2, and Schedule C DRD
  calculations. Covers trial balance pulls, comparative trial balance with significance
  flagging, audit adjustment posting to QBO, passed adjustment materiality evaluation,
  book-tax reconciliation, and QBO-to-1120 account mapping. Consult when extracting QBO
  data for audit workpapers, posting year-end adjustments, building Schedule M-1
  reconciliation, mapping QBO accounts to Form 1120 lines, evaluating passed adjustments
  against materiality, generating adjustment summary logs, or pulling comparative trial
  balances for analytical procedures.
---

# QBO Audit Support

Operational procedures for extracting audit and tax data from QuickBooks Online,
posting audit adjustments, and mapping QBO account data to Form 1120 schedules
for C-corporation engagements.

## Adjustment Types and Posting Rules

Three adjustment types exist in audit workflows. Only one type gets posted to QBO.

- **AJE (Adjusting Journal Entry)** — Corrects the books. Post to QBO as a journal entry. Must balance (total debits = total credits) before posting. Use sequential numbering (AJE-1, AJE-2) within each engagement.
- **RJE (Reclassifying Journal Entry)** — Presentation only. Does NOT post to QBO. Affects financial statement grouping without changing underlying balances. Examples: reclassify current portion of long-term debt, separate gross/contra presentation (gross AR vs. allowance).
- **PJE (Passed Journal Entry)** — Identified but waived. Does NOT post to QBO. Must be tracked for management representation letter and evaluated against materiality thresholds.

**Posting guard**: Attempting to post an RJE or PJE to QBO is an error. Only AJEs are posted.

## Common RJE Patterns

### Current Portion of Long-Term Debt (RJE-DEBT)

Reclassifies proper current/long-term split for balance sheet presentation.
- Debit: Long-Term Debt (reduces LT balance)
- Credit: Current Portion of LT Debt (records current portion)
- Workpaper ref: CC-1

### Gross vs. Net Presentation (RJE-CONTRA)

Shows gross amount and contra account separately instead of a netted balance.
- Debit: Gross account (e.g., Gross AR)
- Credit: Contra account (e.g., Allowance for Doubtful Accounts)
- Use when GAAP requires separate disclosure of gross and contra balances

## Posting AJEs to QBO

When posting audit adjustments as QBO journal entries:

1. **Validate type** — Confirm the adjustment is an AJE, not an RJE or PJE
2. **Verify balance** — Total debits must equal total credits
3. **Set the date** — Use the agreed-upon audit date (typically fiscal year-end)
4. **Set DocNumber** — Use the AJE reference number (e.g., "AJE-1")
5. **Set PrivateNote** — Include description and workpaper reference for traceability
6. **Build lines** — Each line needs PostingType (Debit/Credit), Amount, and AccountRef
7. **Save and record** — After posting, capture the QBO JournalEntry ID back to the adjustment log

For batch posting, iterate through the adjustment list, skip non-AJE types, and collect results with success/failure status per entry.

## Adjustment Summary and Tracking

Generate a master adjustment log that groups by type (AJE/RJE/PJE) and tracks:
- Reference number, type, description, workpaper reference
- Debit and credit totals per adjustment
- Posted status (with QBO JE ID for posted AJEs)
- Account-level impact (net effect by account across all adjustments)

Export to Excel with three sheets: Summary (counts and totals), Adjustments (detail rows), and By Account (net effect per account).

## Materiality and Passed Adjustments

Evaluate passed adjustments (PJEs) against three thresholds:
- **Overall materiality** — Total passed amount vs. overall materiality
- **Performance materiality** — Working threshold during the audit
- **Trivial threshold** — Below this amount, adjustments are clearly trivial

If total passed adjustments exceed the trivial threshold, management representation letter disclosure is required. If they exceed overall materiality, reconsider whether they should be recorded as AJEs.

## Trial Balance Extraction

### Standard Trial Balance

Extract balances from QBO for all active accounts as of a specified date:
- Sort by account number (unnumbered accounts sort last)
- Present as debit/credit columns based on normal balance rules:
  - Asset and Expense accounts: positive balance = debit column
  - Liability, Equity, and Revenue accounts: positive balance = credit column
  - Negative balances flip to the opposite column
- Optionally include zero-balance accounts
- Each row carries: account ID, number, name, type, classification, debit, credit, workpaper reference

Export format: Excel with company name header, as-of date, standard audit columns (Acct #, Account Name, Debit, Credit, WP Ref), totals row with balance check, and difference row flagged red if non-zero.

### Comparative Trial Balance

Extract current-year and prior-year trial balances and compute:
- Current balance, prior balance, dollar change, percentage change
- Significance flag: absolute change > $1,000 OR percentage change > 10%
- Index by account ID to pair current/prior rows (accounts in current but not prior get zero prior balance)

Use comparative analysis for analytical procedures during audit planning and as a basis for substantive testing decisions.

## Form 1120 Tax Data Mapping

Map QBO account balances to Form 1120 lines using account type and name-pattern matching. This section covers QBO-specific extraction — invoke `tax-prep:form-1120-prep` for broader Form 1120 context and preparation rules.

### Page 1: Income (Lines 1-10)

Account type and name pattern determine line placement:
- **Line 1a** — Income accounts matching "gross receipts" (sign: +1)
- **Line 1b** — Income accounts matching "returns" (sign: -1, reduces gross)
- **Line 4** — Other Income matching "dividend" (Schedule C drives DRD)
- **Line 5** — Other Income matching "interest"
- **Line 6** — Other Income matching "gross rents"
- **Line 7** — Other Income matching "royalt" (partial match for royalty/royalties)
- **Line 8** — Other Income matching "capital gain"
- **Line 9** — Other Income matching "1231" (net gain Form 4797)
- **Line 10** — Other Income with no specific pattern (catch-all)

### Page 1: Deductions (Lines 12-26)

- **Line 12** — Expense matching "officer" (compensation of officers)
- **Line 13** — Expense matching "salaries|wages"
- **Line 14** — Expense matching "repair"
- **Line 15** — Expense matching "bad debt"
- **Line 16** — Expense matching "rent"
- **Line 17** — Expense matching "tax|license"
- **Line 18** — Expense matching "interest"
- **Line 19** — Expense matching "charitable|contribution" (10% taxable income limit)
- **Line 20** — Expense matching "depreciation" (Form 4562)
- **Line 21** — Expense matching "depletion"
- **Line 22** — Expense matching "advertising"
- **Line 23** — Expense matching "pension|profit sharing"
- **Line 24** — Expense matching "employee benefit"
- **Line 26** — Expense with no specific pattern (other deductions catch-all)

**Pattern matching is case-insensitive regex**. Accounts not matching any specific pattern on their type fall to the catch-all line (10 for income, 26 for deductions). Verify catch-all aggregations during review — unmapped accounts accumulate there silently.

## Schedule L: Balance Sheet per Books

Extracts beginning-of-year and end-of-year balances for each Schedule L line. Account matching uses QBO account type and name patterns.

### Asset Lines

- **Line 1** Cash — Bank accounts
- **Line 2a** Trade receivables — Accounts Receivable
- **Line 2b** Allowance — Other Current Asset matching "allowance"
- **Line 3** Inventories — Other Current Asset matching "inventor"
- **Line 4** U.S. government obligations — matching "treasury|t-bill"
- **Line 5** Tax-exempt securities — matching "muni|tax.exempt"
- **Line 6** Other current assets — Other Current Asset (catch-all)
- **Line 7** Loans to shareholders — matching "loan.\*shareholder|due.\*shareholder"
- **Line 8** Mortgage/real estate loans — matching "mortgage|real estate loan"
- **Line 9** Other investments — Other Asset matching "investment"
- **Lines 10a/10b** Depreciable assets and accumulated depreciation — Fixed Asset
- **Lines 11a/11b** Depletable assets and accumulated depletion — Fixed Asset
- **Line 12** Land — Fixed Asset matching "land"
- **Lines 13a/13b** Intangibles and accumulated amortization — Other Asset
- **Line 14** Other assets — Other Asset (catch-all)

### Liability and Equity Lines

- **Line 15** Accounts payable
- **Line 16** Short-term notes/mortgages — Other Current Liability matching "note|loan|mortgage"
- **Line 17** Other current liabilities — Other Current Liability (catch-all)
- **Line 18** Shareholder loans — Long Term Liability matching "loan.\*shareholder|due.\*shareholder"
- **Line 19** Long-term notes/mortgages — Long Term Liability matching "note|loan|mortgage"
- **Line 20** Other liabilities — Long Term Liability (catch-all)
- **Lines 21-27** Equity — preferred stock, common stock, APIC, appropriated/unappropriated retained earnings, OCI adjustments, treasury stock

**Reconciliation check**: Schedule L ending retained earnings (Line 25) must tie to Schedule M-2 Line 8. Variance indicates missing transactions or misclassification.

## Schedule M-1: Book-Tax Reconciliation

Starts with net income per books (Line 1) and reconciles to taxable income (Line 10).

### Additions (Lines 2-5)

- **Line 2** — Federal income tax per books. Pull from Expense accounts matching "federal.\*tax|income tax"
- **Line 3** — Excess of capital losses over capital gains (calculated, not pulled directly)
- **Line 4** — Income subject to tax not recorded on books (e.g., prepaid income)
- **Line 5a** — Depreciation difference (book vs. tax)
- **Line 5b** — Charitable contribution difference
- **Line 5c** — Travel and entertainment (50% meals disallowance). Pull Expense matching "meal|entertainment", multiply by 0.50
- **Line 5d** — Other (penalties/fines, 100% disallowed). Pull Expense matching "penalty|fine"

### Subtractions (Lines 7-8)

- **Line 7** — Income on books not included on return (e.g., tax-exempt interest). Pull Other Income matching "tax.exempt|muni"
- **Line 8** — Deductions on return not charged against books (e.g., bonus depreciation difference)

### Calculation

- Line 6 = Lines 1 + 2 + 3 + 4 + 5a + 5b + 5c + 5d
- Line 9 = Lines 7 + 8
- Line 10 (taxable income) = Line 6 - Line 9

User-supplied tax adjustments override automatically extracted values for any line.

## Schedule M-2: Retained Earnings Analysis

Traces retained earnings from beginning to end of year:
- **Line 1** — Beginning balance (retained earnings account balance as of BOY)
- **Line 2** — Net income per books (from P&L report)
- **Line 3** — Other increases
- **Line 4** — Total (Lines 1-3)
- **Lines 5a/5b/5c** — Distributions (cash, stock, property)
- **Line 6** — Other decreases
- **Line 7** — Total distributions and decreases
- **Line 8** — Ending balance (Line 4 - Line 7)

**Variance check**: Compare calculated Line 8 to the actual QBO retained earnings balance at year-end. Any difference greater than $0.01 indicates unaccounted transactions — investigate before filing.

## Schedule C: Dividends Received Deduction

DRD rates are year-dependent. Apply rates for the tax year under preparation:
- **Less than 20% ownership** — 50% (post-TCJA) / 70% (pre-TCJA) (IRC 243(a)(1))
- **20% to less than 80%** — 65% (post-TCJA) / 80% (pre-TCJA) (IRC 243(c))
- **80% or more** — 100% (all years) (IRC 243(a)(3))

Taxable income limitation (IRC 246(b)): the sub-100% tiers are each limited to the SAME tier-specific percentage of taxable income computed without the DRD. This is per-tier, not a blanket 65%. If the full unlimited DRD creates or increases a net operating loss, the limitation does not apply (IRC 246(b)(2)). The 100% tier has no taxable income limitation. For the complete DRD computation algorithm (holding period, debt-financed stock, foreign corporation rules, Schedule C line walkthrough, worked examples), invoke `tax-prep:form-1120-prep` and read `references/dividends-received-deduction.md`.

## Complete Tax Data Export

The full Form 1120 data package extracts all schedules (Page 1, L, M-1, M-2, C) and exports to JSON. Requires:
- QBO client connection
- Tax year
- Tax adjustments dict (overrides for M-1 lines)
- Dividends paid amount (for M-2)
- Dividends received list with ownership percentages (for Schedule C)

## Best Practices

1. **Number adjustments sequentially** — AJE-1, AJE-2, RJE-1, etc. within each engagement year
2. **Link every adjustment to a workpaper** — No orphaned entries
3. **Balance before posting** — Verify debits = credits on every AJE
4. **Second review before posting** — All AJEs reviewed by a second person before QBO posting
5. **Track all passed adjustments** — Required for management representation letter
6. **Verify M-2 ties to balance sheet** — Retained earnings must reconcile between Schedule L Line 25 and Schedule M-2 Line 8
7. **Review catch-all lines** — Lines 10, 26 (Page 1), Lines 6, 14, 17, 20 (Schedule L) accumulate unmatched accounts
8. **Document M-1 adjustments** — Keep workpapers for each book-tax difference with permanent/temporary classification
9. **Run reports for fiscal year** — Use consistent date ranges across all extractions
10. **Review QBO account classifications** — Correct account types simplify all downstream mapping

## Supporting References

Read these for implementation detail, code patterns, and complete data structures:

- `references/audit-rje-patterns.md` — Python code for creating RJE and AJE adjustment objects, posting AJEs to QBO via the python-quickbooks library, generating adjustment summaries with Excel export, and evaluating passed adjustments against materiality thresholds. Read when building or modifying adjustment posting workflows or when you need the exact data structures (AuditAdjustment, AdjustmentLine, MaterialityThresholds).
- `references/audit-trial-balance.md` — Python code for trial balance extraction from QBO including the TrialBalanceRow data structure, normal balance debit/credit assignment logic, Excel formatting with standard audit layout, and comparative trial balance with significance flagging. Read when implementing trial balance extraction or customizing the Excel output format.
- `references/tax-form-1120-page1.md` — TaxLineMapping data structure and complete income/deduction mapping tables for Form 1120 Page 1 (Lines 1-26). Includes pattern-based account matching functions and the extract_form_1120_data workflow. Read when troubleshooting account-to-line mappings or extending the mapping tables.
- `references/tax-schedule-l-m.md` — Complete Schedule L asset/liability/equity line mappings, Schedule M-1 book-tax reconciliation logic with auto-extraction of federal tax, meals, penalties, and tax-exempt interest, Schedule M-2 retained earnings analysis with variance checking, Schedule C dividends received deduction calculator with ownership-tiered rates and taxable income limitation, and the full Form 1120 package export function. Read when working with any supporting schedule or the complete tax data export workflow.

## Cross-Plugin References

- Invoke `qbo-integration:qbo-api` for low-level QBO API operations (authentication, report queries, account lookups) underlying the extraction functions in this skill
- Invoke `qbo-integration:qbo-coa` for QBO-specific chart of accounts setup, detail types, and tax-line configuration within QBO
- Invoke `accounting-foundation:chart-of-accounts` for account type taxonomy, numbering conventions, and the conceptual Form 1120 mapping framework
- Invoke `tax-prep:form-1120-prep` for Form 1120 preparation context, filing rules, and tax computation logic beyond QBO data extraction
- Invoke `tax-prep:tax-planning` for book-tax difference analysis, deferred tax calculations, and permanent vs. temporary difference classification
