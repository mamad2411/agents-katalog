---
name: journal-entry
description: Prepares journal entries with proper debits, credits, account coding, ASC/GAAP framework reference, period assignment, reversal logic, and supporting documentation chain (calculation memo, source files, preparer/reviewer/approver). Make sure to use this skill whenever the user says book a JE, post an entry, accrue [expense/revenue/payroll], record depreciation or amortization, true up prepaids, recognize revenue, defer revenue, post a reclass, capitalize a fixed asset, write off a [receivable/asset], book the cyber-insurance accrual, record stock comp, document an entry for audit, or describes any GL adjustment that needs to land in the books. Tuned for cybersecurity-startup revenue patterns (multi-year SaaS deferred-revenue waterfall under ASC 606, MSSP recurring monthly recognition, milestone-based pen test fees with contract assets, sub-processor pass-through cost accounting) and Puerto Rico tax mechanics (Hacienda 7%/10%/29% withholding clearing entries, IVU payable accrual, patente municipal monthly accrual, Act 60/20/22 deferred-tax rate). Do NOT use for: finding the difference between two sources before booking (defer to finance:reconciliation — that skill identifies, this skill posts), generating financial statements (defer to finance:financial-statements), explaining variances after-the-fact (defer to finance:variance-analysis — explain, don't book), SOX control testing of the JE control itself (defer to finance:sox-testing / finance:audit-support), or orchestrating the close calendar (defer to finance:close-management).
argument-hint: "<entry type> [period]"
---

# Journal Entry

Prepares journal entries with proper debits/credits, ASC/GAAP framework citation, period and reversal discipline, and a complete supporting-documentation chain.

**Important:** This skill assists with workflows. All entries must be reviewed by a qualified financial professional before posting.

## When to use vs. adjacent skills (defer matrix)

| Situation | Skill |
|---|---|
| Booking debits/credits with support | **this skill** |
| First finding the variance/difference to be booked | `finance:reconciliation` (then chain back here) |
| Generating P&L / BS / CF | `finance:financial-statements` |
| Narrative on why a number changed (don't book — explain) | `finance:variance-analysis` |
| Testing the JE approval control for SOX | `finance:audit-support` / `finance:sox-testing` |
| Sequencing the whole close | `finance:close-management` |

**Chain pattern:** `finance:reconciliation` identifies an adjustment → **this skill** posts it → `finance:financial-statements` consumes the result.

## Standard JE structure

Every entry produced by this skill includes:

1. **Header** — Period (YYYY-MM), JE# (placeholder OK), one-line description, Reversing Y/N + reversal date if Y, Source skill (rec / standalone).
2. **Lines** — Account # + name, DR/CR, dept/cost-center/class, per-line memo if unusual.
3. **Supporting documentation** — Calculation memo (link or attached), source files (invoice, contract, payroll register, FA register, waterfall), approver chain (preparer → reviewer → poster).
4. **Sanity checks** — Total DR = Total CR; period open; account active; ASC/IFRS reference if material; no unusual round numbers or out-of-pattern amounts.

## ASC / GAAP framework references

| Entry type | Standard | Key points |
|---|---|---|
| Revenue recognition | **ASC 606** | 5-step model; performance obligation; over-time vs. point-in-time |
| Leases | **ASC 842** | ROU asset + lease liability; operating vs. finance |
| Stock compensation | **ASC 718** | Grant-date fair value; vesting schedule; forfeitures |
| Internal-use software | **ASC 350-40** | Capitalize during application-development stage |
| Intangibles / goodwill | **ASC 350** | Annual impairment test; finite vs. indefinite life |
| Accruals (expense incurred, not invoiced) | ASC 450 / accrual basis | Probable + estimable |
| Income taxes | **ASC 740** | Deferred tax assets/liabilities, valuation allowance |
| Cyber-insurance recoveries | ASC 410 / 450 | Recognize recoverable only when probable AND measurable |

PR-specific entities under Act 60 / 20 / 22 use the decreed rate (commonly 4% on eligible income) when computing deferred-tax effects, not the federal 21% or PR statutory 37.5%.

## Common entry types — quick reference

### Accrued expense
```
DR  Expense                              X
    CR  Accrued liability                    X
(reverse next month when invoice arrives)
```

### Prepaid amortization
```
DR  Expense                              X
    CR  Prepaid asset                        X
```

### Depreciation (straight-line)
```
DR  Depreciation expense                 X
    CR  Accumulated depreciation              X
```

### Revenue recognition — multi-year SaaS / MSSP (ASC 606, ratable over time)
```
DR  Deferred revenue                     X
    CR  Subscription revenue                  X
(monthly portion of annual contract earned)
```

### Revenue recognition — milestone pen test (ASC 606, point-in-time)
```
On milestone delivery (report issued):
DR  Contract asset (unbilled AR)         X       (if invoice not yet sent)
    CR  Professional services revenue         X

On invoice issuance:
DR  Accounts receivable                  X
    CR  Contract asset                        X
```

### Sub-processor pass-through (cost re-billed to client)
```
On vendor bill (AWS, Cloudflare):
DR  Sub-processor clearing               X
    CR  AP                                    X

On client re-bill:
DR  AR                                   X
    CR  Sub-processor clearing                X
(clearing should net to ~$0 each period)
```

### Payroll accrual (period-end)
```
DR  Salary expense                       X
DR  Payroll tax expense                  X
DR  Benefits expense                     X
    CR  Accrued payroll                       X
    CR  Accrued payroll tax                   X
    CR  Accrued benefits                      X
(reverse on next pay run)
```

### Cyber-insurance accrual (premium amortization)
```
At policy inception:
DR  Prepaid insurance                    X
    CR  Cash                                  X

Monthly:
DR  Insurance expense                    X/12
    CR  Prepaid insurance                     X/12
```

### Cyber-insurance recovery (post-incident, when probable + measurable)
```
DR  Insurance recoverable                X
    CR  Incident response expense (or loss)   X
(memo: carrier letter ref, ASC 410/450)
```

### Stock compensation (ASC 718, monthly straight-line over vesting)
```
DR  Stock-based comp expense             X
    CR  Additional paid-in capital            X
```

### PR Hacienda withholding on vendor payment (7% professional services)
```
On vendor invoice $1,000:
DR  Professional services expense        1,000
    CR  AP – vendor                           930
    CR  Hacienda withholding payable – 7%      70

On Form 480 remittance:
DR  Hacienda withholding payable – 7%       70
    CR  Cash                                   70
(clearing account should be $0 after remit)
```

### IVU sales-tax payable (collected on taxable sale)
```
On invoice for $1,000 taxable PR sale:
DR  AR                                   1,115
    CR  Revenue                              1,000
    CR  IVU payable – state 10.5%              105
    CR  IVU payable – municipal 1%              10
```

### Patente municipal monthly accrual
```
DR  Patente expense                      X/12
    CR  Accrued patente                       X/12
(annual filing trues up; accrue 1/12 of last-year base monthly)
```

## Period & account discipline

- **Right period:** Posting date = period being closed. Late-arriving invoice for goods received in prior period → accrue in prior period, reverse in current; do NOT post current.
- **Cut-off:** AP cut-off typically T-1 or T+0; revenue cut-off ties to delivery/POB satisfaction, not invoice date.
- **Reversal flag:** Accruals (AP, payroll, est-only items) auto-reverse next period. Amortization and depreciation do NOT reverse. Reclasses do NOT reverse.
- **Account coding:** validate account is active and at the right level (no posting to roll-up accounts); validate dept/cost-center/class as required by chart structure.
- **Balance:** Total DR must equal total CR before submission.

## Materiality & approval

| Amount vs. threshold | Documentation required | Approver |
|---|---|---|
| Below threshold | Streamlined memo, source ref | Preparer self-review |
| At/above threshold | Full memo, calculation, ASC ref | Reviewer signoff |
| > 5x threshold or unusual | Full memo + controller signoff | Controller |
| Year-end / audit-sensitive | Add: external auditor pre-clear | Controller + CFO |

Default startup threshold: greater of $5,000 or 1% of monthly revenue (override if entity has documented policy).

## Documentation trail (mandatory)

Every JE attaches/links:
1. **Calculation memo** — formula, inputs, assumptions, source data link
2. **Source files** — invoice PDF, contract, payroll register, FA register row, waterfall row
3. **Approver chain** — preparer name+date → reviewer name+date → poster name+date
4. **ASC reference** — for material or non-routine entries
5. **Reversal instruction** — explicit Y/N + date

## Anti-patterns (auto-flag)

- Unbalanced (DR ≠ CR)
- "Plug" entries with no calc
- Round numbers with no source ($10,000.00 flat)
- Posting to a closed period
- Posting to inactive or roll-up account
- Missing reviewer for material entry
- Accrual with no reversal flag
- Revenue recognized without delivery / POB satisfaction
- Capitalizing what should be expensed (training, maintenance, post-go-live SaaS dev)
- Hacienda withholding booked gross (must split payable + clearing)

## Output

1. Formatted JE (header + lines + memo + checks)
2. Calculation memo
3. Reversal instruction with date (if applicable)
4. Account/period validation result
5. ASC/GAAP reference (when material)
6. Reviewer flags (unusual amount, new account, missing approver, period concern)
7. Posting instructions (manual entry vs. ERP upload format)
