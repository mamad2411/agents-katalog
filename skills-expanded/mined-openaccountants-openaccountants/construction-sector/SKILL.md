---
name: construction-sector
description: "> Use this skill whenever a construction contractor, subcontractor, developer, or design-build firm asks about sector-specific tax / accounting. Trigger on phrases like \"construction industry scheme\", \"CIS\", \"CIS deduction\", \"reverse charge construction VAT\", \"domestic reverse charge construction services\", \"developer's relief\", \"long-term contract\", \"percentage of completion\", \"completed contract\", \"ASC 606 construction\", \"uninstalled materials\", \"retention\", \"subcontractor 1099\", \"USDOL prevailing wage\", \"Davis-Bacon\", \"construction VAT zero-rate new residential\", or any construction-sector tax question. Covers UK Construction Industry Scheme (CIS), UK domestic reverse charge VAT for construction services (effective 1 March 2021), US construction tax (long-term contracts under IRC §460; percentage-of-completion-capitalisable; small contractor exception), EU developer reliefs and new-build zero/reduced VAT rates, retentions and progress billing accounting."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GLOBAL
  category: vertical
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/construction-sector"
  obligation: VERT
---

# Construction Sector Tax & Accounting v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

A sector overlay for construction contractors, subcontractors, developers, and design-build firms.

---

## Section 1 — Revenue recognition for long-term contracts

### 1.1 IFRS 15 / ASC 606

**[T1] Performance obligation satisfied over time** if any of:
- Customer simultaneously receives and consumes the benefits (typically for routine services)
- Work creates or enhances an asset the customer controls
- No alternative use to seller + enforceable right to payment for work performed to date

**[T1] Input method** (proportion of costs incurred to total expected costs) — most common for construction.
**Output method** (units produced / milestones / surveys) — used where measurable units.

**[T1] Uninstalled materials** — exclude from cost-to-cost calculation to avoid overstating progress (IFRS 15 IE19 example).

### 1.2 US tax — long-term contracts (IRC §460)

**[T1]** A "long-term contract" is one not completed within the tax year started.

**[T1] Percentage of Completion Method (PCM)** — required for most contracts; based on cost-to-cost.

**[T1] Small Contractor Exception** — exempt from PCM if:
- Average annual gross receipts ≤ USD 30m (2025; indexed)
- Contract estimated to complete within 2 years

Small contractor may use Completed Contract Method (CCM) or Cash method for short-duration contracts.

**[T1] Home Construction Contract Exception** — residential construction not required to use PCM.

### 1.3 Look-back interest (US)

**[T1] §460(b)(2)**: at completion of long-term contract, recompute PCM based on actual rather than estimated costs; if difference creates over- or under-payment, interest computed.

---

## Section 2 — UK Construction Industry Scheme (CIS)

**[T1]** A withholding regime for payments by contractors to subcontractors in construction operations.

### 2.1 Contractor obligations

- Verify subcontractor with HMRC
- Withhold and remit to HMRC based on subcontractor status:
  - **Gross payment status** — 0% deduction
  - **Registered subcontractor** — 20% deduction
  - **Unregistered subcontractor** — 30% deduction
- Monthly CIS return (CIS300) by 19th of month
- Payment of CIS deducted by 22nd (electronic) / 19th (cheque)

### 2.2 Subcontractor

- Register as contractor (if employs other subbies)
- Apply for gross payment status if turnover ≥ GBP 30k per individual / GBP 30k per partner / GBP 200k per company
- Recover CIS deductions against own tax liability

### 2.3 Scope

**[T1]** "Construction operations" include site preparation, demolition, installation, building, painting/decorating, alteration. Excludes architecture, engineering, surveying.

**[T1] Mixed contracts** — full CIS applies unless the construction element is incidental and minor.

---

## Section 3 — UK Domestic Reverse Charge for Construction VAT

**[T1] Effective 1 March 2021** — domestic reverse charge applies to most construction services in the UK construction supply chain (subject to certain exceptions for end-user / intermediary supplier).

### 3.1 Mechanics

- Supplier issues invoice **without VAT** (notation: "reverse charge applies; customer pays VAT directly")
- Customer accounts for output VAT on their return AND recovers as input VAT (subject to standard rules)
- Net cash effect: nil for customer
- Disadvantages: smaller supplier cash flow worsens (no VAT on receipts)

### 3.2 Scope

**[T1]** Same as CIS for "construction services" between VAT-registered parties — supplier must charge reverse charge to other contractors. Excludes:
- Supplies to "end-users" (the final customer in the chain — typically the developer or building owner)
- Supplies to "intermediary suppliers" (those who acquire and on-supply construction services to end-users)

### 3.3 End-user / intermediary supplier notification

End-user / intermediary must notify supplier in writing; failure to notify means supplier should charge VAT normally.

---

## Section 4 — Construction VAT

### 4.1 New-build residential

**[T1]**
- **UK**: Zero-rated (Item 2(a) Group 5 Schedule 8 VATA)
- **France**: Reduced rate 5.5% for social housing (HLM); 10% for certain renovations
- **Germany**: Standard 19% on most; some construction services in residential sector exempt
- **Italy**: 4% on first-home purchase; 10% on non-first-home new build
- **Spain**: Reduced 10% on new residential

### 4.2 Renovation

**[T1]**
- **UK**: Reduced rate 5% for certain residential renovation (over-2-years empty; energy-saving materials)
- **EU**: Reduced rates per Annex III PVD allowed

### 4.3 Land

**[T1]** Most jurisdictions exempt sale of unimproved land. UK option to tax permitted for commercial land.

---

## Section 5 — Retention and progress billing

### 5.1 Retention

**[T1]** Construction contracts typically retain 5-10% of each progress payment for defects liability period. Accounting:
- Contract asset (under IFRS 15 / ASC 606) for amount earned but not billed
- Retention receivable recognised when retention released
- Bad debt provision for retention if collection uncertain

### 5.2 Progress billing

**[T1]**
- Issue progress invoice based on completion
- Recognise revenue on % completion (not invoice timing)
- Variance between billed amount and earned revenue → contract asset (earned > billed) or contract liability (billed > earned)

---

## Section 6 — Subcontractor classification

**[T1] Employment vs self-employed status** — material in construction:
- US: §530 relief; misclassification penalties; specific Department of Labor (Davis-Bacon) prevailing wage requirements on federal contracts
- UK: IR35 test for personal service companies; off-payroll worker rules
- Many jurisdictions: "deemed employment" tests for construction subcontractors

---

## Section 7 — Reviewer brief

```
1. Contract register — every active project
2. Revenue recognition — PCM input method calculation per contract
3. Uninstalled materials exclusion documented
4. CIS register (UK) — subcontractor list with status, deductions, monthly returns
5. Domestic reverse charge VAT (UK) — supply chain map, end-user notifications
6. New-build VAT zero/reduced rate claim support
7. Contract assets / liabilities reconciliation
8. Retention schedule by project / customer
9. Long-term contract look-back interest (US)
10. Subcontractor employment status assessments
11. Reviewer questions — [T2]/[T3] items
```

---

## Section 8 — Self-checks

- [ ] Long-term contracts on PCM input cost-to-cost
- [ ] Uninstalled materials excluded from cost-to-cost
- [ ] Small contractor exception applied where eligible (US)
- [ ] CIS subcontractor verification current (UK)
- [ ] CIS return CIS300 filed monthly
- [ ] Domestic reverse charge applied where required (UK)
- [ ] End-user notification documented (UK)
- [ ] New-build zero/reduced rate VAT supported with HMRC notice/EU PVD reference
- [ ] Retention receivable recognised when contractually due
- [ ] Look-back interest computed at contract completion (US)
- [ ] Subcontractor employment status documented (IR35 / §530 / Davis-Bacon)
- [ ] Output flags every [T2]/[T3] item for reviewer judgement

---

## Section 9 — Disclaimer

Construction sector taxation is highly fact-specific. Outputs must be reviewed by credentialed construction sector practitioners. The most up-to-date version is at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/construction-sector) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
