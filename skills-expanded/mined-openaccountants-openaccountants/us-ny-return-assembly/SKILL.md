---
name: us-ny-return-assembly
description: "Final orchestrator skill that assembles the complete federal and New York State filing package for New York resident sole proprietors and single-member LLCs disregarded for federal tax. Consumes outputs from all federal content skills (bookkeeping, Schedule C/SE, QBI, retirement, SE health insurance, quarterly estimated tax, federal assembly, 1099-NEC) and all New York content skills (IT-201 individual return, NYC UBT Form NYC-202 where applicable, NY estimated tax IT-2105, MCTMT) to produce a single unified reviewer package. Handles reconciliation between federal AGI and NY AGI adjustments, NY itemized vs standard deduction election, NYC income tax surcharge, NYC UBT credit against personal income tax, and MCTMT computation. New York full-year residents only."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-NY
  category: orchestrator
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/us-ny-return-assembly"
  obligation: ORCH
---

# US+NY Return Assembly Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## CRITICAL EXECUTION DIRECTIVE — READ FIRST

**When this skill is invoked, you have already passed through intake. The user has consented to the full workflow. Execute all steps without pausing for permission.**

- Do NOT ask "how deep do you want me to go" or "do you want the full package." Produce it.
- Do NOT announce token counts or tool calls.
- Do NOT ask which deliverables to prioritize. Produce all deliverables listed in Section 6.
- Do NOT re-validate scope that intake already validated.
- Do NOT pause between content skills to check in.
- Self-checks are targets, not blockers. If one fails, flag it for reviewer and continue.
- If you feel the urge to ask "how should I proceed," pick the most defensible path and flag the decision in the reviewer brief.

---

## Section 1 — Scope

Produces the complete federal + New York filing package for:
- Full-year New York State residents (including NYC residents)
- Sole proprietors or single-member LLCs disregarded for federal tax
- Tax year 2025
- Filing Form 1040 (federal), IT-201 (NY State), NYC-202 (NYC UBT, if applicable)

---

## Section 2 — Execution order

1. `us-sole-prop-bookkeeping`
2. `us-schedule-c-and-se-computation`
3. `us-self-employed-retirement`
4. `us-self-employed-health-insurance`
5. `us-qbi-deduction`
6. `us-federal-return-assembly`
7. `us-quarterly-estimated-tax` (needs federal total tax)
8. `us-1099-nec-issuance` (parallel, needs bookkeeping only)
9. `ny-it-201-individual-return` (needs federal assembly)
10. `nyc-ubt-form-202` (if NYC resident with business income; parallel with IT-201)
11. `ny-estimated-tax-it-2105` (needs NY total tax)
12. `ny-mctmt` (if MCTD area; parallel)
13. **THIS SKILL** — final assembly and verification

---

## Section 3 — Verification matrix

### Federal internal consistency

- Schedule C net profit → Schedule 1 Line 3 → Form 1040 Line 8
- Schedule SE tax → Schedule 2 Line 4 → Form 1040 Line 23
- Half of SE tax → Schedule 1 Line 15 → Form 1040 Line 10
- SE retirement → Schedule 1 Line 16 → Form 1040 Line 10
- SE health insurance → Schedule 1 Line 17 → Form 1040 Line 10
- QBI deduction → Form 1040 Line 13
- Total tax → Form 1040 Line 24
- Form 2210 penalty (if applicable)
- Total payments → Form 1040 Line 33

### New York internal consistency

- Federal AGI → IT-201 Line 19 (starting point)
- NY additions (IT-201 Lines 20-23): interest income on non-NY state/local bonds, QBI deduction add-back (NY does not allow QBI deduction)
- NY subtractions (IT-201 Lines 24-32): interest on US government obligations, NY state/local pension exclusion
- NY AGI → IT-201 Line 33
- NY standard deduction ($8,000 single / $16,050 MFJ) vs NY itemized deduction (IT-201 Line 34-35)
- NY itemized deduction limitations (for high-income taxpayers: 50% limitation on charitable contributions and other adjustments if NY AGI > $525,000)
- NY taxable income → IT-201 Line 38
- NY tax → IT-201 Line 39 (from tax computation worksheet or tax table)
- NYC resident tax → IT-201 Lines 47-51 (if NYC resident)
- NYC UBT credit → IT-201 Line 51 (partial credit against NYC personal income tax)
- NY household credit → IT-201 Line 40 (if income below threshold)
- Total NY tax → IT-201 Line 62
- NY estimated tax payments → IT-201 Line 67
- NY refund or balance due → IT-201 Line 78 or 80

### NYC UBT consistency (if applicable)

- Gross income from NYC business → Form NYC-202 Line 1
- NYC UBT deductions → Form NYC-202 Lines 2-12
- NYC UBT taxable income → Form NYC-202 Line 13
- Exemption calculation ($95,000, phaseout $95K-$150K) → Form NYC-202 Line 14-16
- NYC UBT (4% rate) → Form NYC-202 Line 17
- UBT credits available → NYC-202 Line 18+
- UBT estimated payments → NYC-202 Schedule F
- UBT balance due or refund

### Federal-NY coordination

- Federal AGI used correctly as NY starting point
- QBI deduction properly added back for NY (NY does not conform to §199A)
- Filing status consistent
- Dependents consistent
- NY itemized deductions use federal Schedule A as starting point but apply NY modifications:
  - State/local tax deduction: included for NY purposes (no $10,000 SALT cap at state level)
  - College tuition deduction (IT-201 Line 30): up to $10,000 per student
- Depreciation: NY generally conforms to federal MACRS but has modifications for bonus depreciation (NY decoupled from 100% bonus; add-back required, then NY allows its own depreciation deduction)

### MCTMT verification

- Net self-employment earnings allocated to MCTD
- Threshold: $50,000 (only taxed if net SE earnings in MCTD exceed $50,000)
- Rate: 0.34%
- MCTMT amount → Form MTA-6

### Estimated tax reconciliation

- Federal: 4 quarterly payments cross-checked against safe harbor (100% prior year tax if AGI ≤ $150K, 110% if AGI > $150K)
- NY State: payments on IT-2105 cross-checked against NY safe harbor (100% prior year NY tax or 90% current year)
- NYC UBT: quarterly payments if UBT > $3,400
- Form IT-2105.9 (NY underpayment penalty) if applicable

---

## Section 4 — NY-specific adjustments detail

### Additions to federal AGI (common for freelancers)

1. **QBI deduction add-back**: NY does not allow the §199A deduction. Full federal QBI deduction amount added back on IT-225 Line 1 (code A-201)
2. **Bonus depreciation add-back**: If federal return claimed bonus depreciation, NY requires add-back of the federal bonus amount, then allows NY depreciation (generally MACRS without bonus). IT-225 code A-110.
3. **Other states' municipal bond interest**: Interest from non-NY state/local bonds is added to NY income

### Subtractions from federal AGI (common for freelancers)

1. **US government obligation interest**: Interest on US Treasury securities subtracted from NY income (IT-225 code S-103)
2. **College tuition**: Up to $10,000 per eligible student (IT-225 code S-106)
3. **NY depreciation**: Replacement depreciation deduction for assets where bonus depreciation was added back (IT-225 code S-110)

### NYC UBT credit mechanism

The taxpayer cannot deduct NYC UBT as a business expense on the federal Schedule C (it is a tax, not a deductible business expense). However:
- NYC UBT paid generates a partial credit against NYC personal income tax (IT-201 Line 51)
- The credit equals the lesser of: (a) the UBT tax, or (b) the NYC personal income tax before the credit
- Effectively prevents double-taxation of NYC business income at both UBT and personal income tax levels, but the credit is not always dollar-for-dollar

---

## Section 5 — Refusals

**R-NY-1 — Upstream skill did not run.** Name the specific skill and refuse until it executes.

**R-NY-2 — Multi-state allocation required.** If income sourced to states other than NY was not identified at intake and appears in documents, refuse. Multi-state allocation requires IT-203/credit for taxes paid analysis.

**R-NY-3 — NYC UBT allocation dispute.** If the taxpayer performed significant business activity outside NYC but is a NYC resident, allocation percentage is complex. Flag for reviewer if allocation is not clearly 100%.

**R-NY-4 — Partnership/S-corp income discovered.** K-1 income appearing in documents that was not disclosed at intake. Refuse and recommend CPA.

**R-NY-5 — NY PTET (Pass-Through Entity Tax) election.** If the SMLLC elected into NY PTET, different treatment applies. Refuse unless PTET skill is available.

---

## Section 6 — Final reviewer package contents

### Documents

1. **Executive summary** — filing status, income, federal tax, NY tax, NYC tax, NYC UBT, MCTMT, total liability, refund/balance due
2. **Federal Form 1040 worksheet** — line-by-line
3. **Schedule C** — sole prop P&L
4. **Schedule SE** — SE tax
5. **Schedule 1, 2, 3** — adjustments, additional taxes, credits
6. **Form 8995 or 8995-A** — QBI
7. **Form 2210** — federal underpayment penalty (if applicable)
8. **Form 1040-ES** — 2026 federal estimated tax schedule
9. **NY IT-201 worksheet** — line-by-line state return
10. **IT-225** — NY addition and subtraction modifications
11. **NYC-202 worksheet** — UBT computation (if NYC resident)
12. **IT-2105** — 2026 NY estimated tax schedule
13. **IT-2105.9** — NY underpayment penalty (if applicable)
14. **Form MTA-6** — MCTMT (if applicable)
15. **1099-NEC batch** — contractor information returns (if applicable)
16. **Reviewer brief** — comprehensive narrative
17. **Taxpayer action list** — deadlines, amounts, payment methods

### Reviewer brief structure

```markdown
# Complete Return Package: [Taxpayer Name] — Tax Year 2025

## Executive Summary
- Filing status: [X]
- Residence: New York ([NYC / rest of state])
- Business: Sole proprietor / SMLLC disregarded
- Federal total tax: $X
- NY State tax: $X
- NYC personal income tax: $X
- NYC UBT: $X
- MCTMT: $X
- Total 2025 tax liability: $X
- Total payments (federal + NY + NYC): $X
- Net refund or balance due: $X

## Federal Return
[Federal assembly content]

## New York State Return (IT-201)
- Federal AGI: $X
- NY additions: $X (QBI add-back $X, bonus depreciation $X, other $X)
- NY subtractions: $X
- NY AGI: $X
- NY deduction (standard/itemized): $X
- NY taxable income: $X
- NY tax (from table/worksheet): $X
- NYC personal income tax: $X
- NYC UBT credit applied: $X
- NY household credit: $X (if applicable)
- Net NY/NYC tax: $X
- NY estimated payments applied: $X
- NY balance due or refund: $X

## NYC Unincorporated Business Tax (if applicable)
- Gross business income in NYC: $X
- Allocable deductions: $X
- NYC UBT taxable income: $X
- Exemption applied: $X
- UBT at 4%: $X
- UBT credits: $X
- Net UBT: $X
- UBT estimated payments: $X
- UBT balance due or refund: $X

## MCTMT (if applicable)
- Net SE earnings in MCTD: $X
- MCTMT (0.34%): $X

## Cross-jurisdiction reconciliation
- Federal AGI matches IT-201 starting point: [verified]
- QBI add-back computed correctly: [verified]
- NYC UBT credit does not exceed NYC personal income tax: [verified]
- All estimated payments allocated correctly: [verified]

## Reviewer attention flags
[Aggregated flags]

## Positions taken
[With citations to IRC, NY Tax Law, NYC Admin Code]

## Planning notes for 2026
- NY PTET election consideration (if beneficial)
- NYC UBT estimated tax adjustment
- Federal/NY/NYC estimated tax coordination
- S-corp election analysis (potential NYC UBT savings)
```

---

## Section 7 — Taxpayer action list structure

```markdown
## Taxpayer Action List

### Before April 15, 2026:
1. Review and sign return package
2. Pay federal balance due: $X via EFTPS / IRS Direct Pay
3. Pay NY balance due: $X via NY DTF Online Services
4. Pay NYC UBT balance due: $X via NYC DOF eFiling (if applicable)
5. Pay 2026 Q1 federal estimated tax: $X
6. Pay 2026 Q1 NY estimated tax: $X (25% of annual estimate)
7. Pay 2026 Q1 NYC UBT estimated tax: $X (if applicable)
8. File MCTMT annual return (if applicable)

### Before June 16, 2026:
1. Pay 2026 Q2 federal estimated tax: $X
2. Pay 2026 Q2 NY estimated tax: $X (25% of annual estimate)
3. Pay 2026 Q2 NYC UBT estimated tax: $X (if applicable)

### Before September 15, 2026:
1. Pay 2026 Q3 federal estimated tax: $X
2. Pay 2026 Q3 NY estimated tax: $X (25% of annual estimate)
3. Pay 2026 Q3 NYC UBT estimated tax: $X (if applicable)

### Before January 15, 2027:
1. Pay 2026 Q4 federal estimated tax: $X
2. Pay 2026 Q4 NY estimated tax: $X (25% of annual estimate)
3. Pay 2026 Q4 NYC UBT estimated tax: $X (if applicable)

### Ongoing:
1. Collect W-9 from new contractors before payment
2. Track business expenses with receipts
3. Monitor income for UBT exemption phaseout
4. Consider S-corp election if net SE income exceeds $150K+ (reduces SE tax and eliminates UBT)
```

---

## Section 8 — Self-checks

**Check NY-A1 — All upstream skills executed.**
**Check NY-A2 — Federal AGI correctly flows to IT-201 Line 19.**
**Check NY-A3 — QBI deduction added back on IT-225 (NY does not allow §199A).**
**Check NY-A4 — NYC UBT computed if NYC resident with business income.**
**Check NY-A5 — NYC UBT credit does not exceed NYC personal income tax.**
**Check NY-A6 — MCTMT computed for MCTD-area self-employed with earnings > $50K.**
**Check NY-A7 — NY estimated tax underpayment penalty evaluated (IT-2105.9).**
**Check NY-A8 — Bonus depreciation add-back and replacement NY depreciation computed.**
**Check NY-A9 — NY standard vs itemized deduction: correct election made (NY allows different election than federal).**
**Check NY-A10 — Payment instructions include all four jurisdictions where applicable (federal, NY, NYC personal, NYC UBT).**

---

## Section 9 — Output files

Three files:

1. **`[taxpayer_slug]_2025_master.xlsx`** — Sheets: Cover, Income, Schedule C, Schedule SE, Retirement, SE Health, QBI, Schedule 1, Form 1040, Form 2210, IT-201, IT-225, NYC-202, IT-2105.9, MTA-6, 1099-NEC batch, 2026 Est Tax (Fed+NY+NYC).

2. **`reviewer_brief.md`** — Full narrative covering federal, NY State, NYC, MCTMT, cross-jurisdiction reconciliation, flags, citations, planning.

3. **`taxpayer_action_list.md`** — Step-by-step with dates, amounts, and payment URLs (EFTPS, NY DTF, NYC DOF).

---

## Section 10 — Known gaps

1. NY PTET election analysis not automated (requires entity-level election before filing deadline)
2. NYC UBT allocation for taxpayers performing work both inside and outside NYC is complex and may require reviewer judgment
3. NY bonus depreciation add-back computation requires detailed asset-by-asset tracking
4. Form IT-2658 (group estimated tax for partnerships) not applicable but flagged to avoid confusion
5. NYC-210 (Claim for NYC School Tax Credit) automatically claimed on IT-201 if eligible — verify $125 (single) or $250 (MFJ) credit
6. NY Earned Income Credit (30% of federal EIC) — verify if applicable

---

## End of Skill

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/us-ny-return-assembly) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
