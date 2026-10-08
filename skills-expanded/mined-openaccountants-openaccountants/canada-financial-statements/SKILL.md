---
name: canada-financial-statements
description: "> Use this skill when preparing, reviewing, or advising on annual financial statements for a Canadian company. Trigger on phrases like \"ASPE\", \"IFRS Canada\", \"Canadian GAAP\", \"CPA Canada Handbook\", \"financial statements Canada\", \"compilation engagement\", \"review engagement Canada\", \"audit Canada\", \"CBCA\", \"OBCA\", \"annual return Canada\", \"CSRE 2400\", or any question about preparing and reporting statutory accounts under Canadian corporate law. Covers ASPE/IFRS frameworks, assurance level options, required statements, formats, notes, filing requirements, and audit/review thresholds."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: CA
  category: financial-statements
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/canada-financial-statements"
  obligation: FS
---

# Canada Financial Statements Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | Canada |
| Currency | CAD |
| Filing authority | Corporations Canada (federal); Provincial corporate registries (provincial) |
| Primary legislation | Canada Business Corporations Act (CBCA); Provincial acts (OBCA, BCBCA, ABCA, etc.) |
| Supporting legislation | Income Tax Act (R.S.C. 1985, c.1); CPA Canada Handbook |
| Accounting standards | IFRS (publicly accountable enterprises); ASPE Part II (private enterprises); ASNPO Part III (not-for-profit) |
| Financial year | Any fiscal year-end chosen by the corporation |
| CRA filing deadline | 6 months after fiscal year-end (corporate tax return T2) |
| Annual return | Within 60 days of anniversary of incorporation (CBCA); varies by province |
| Digital filing | CRA My Business Account (T2); Corporations Canada Online Filing |

---

## Section 2 -- Reporting Framework

| Entity type | Applicable standard | CPA Handbook |
|---|---|---|
| Publicly accountable enterprises (PAE) | IFRS as issued by IASB (Canadian-adopted) | Part I |
| Private enterprises | ASPE (Accounting Standards for Private Enterprises) | Part II |
| Not-for-profit organizations | ASNPO | Part III |
| Pension plans | Part IV (specific standards) | Part IV |
| Private enterprise choosing IFRS | IFRS (permitted but not required) | Part I |

### Key difference: ASPE vs IFRS

| Area | ASPE | IFRS |
|---|---|---|
| Financial instruments | Simplified (cost/amortised cost focus) | Complex (IFRS 9 — ECL, fair value hierarchy) |
| Leases | Finance/operating distinction | IFRS 16 — right-of-use model |
| Revenue | Risks/rewards transfer model | IFRS 15 — five-step model |
| Goodwill | Amortised over useful life (max 10 years) | Not amortised; annual impairment test |
| Employee benefits | Simplified pension accounting | IAS 19 — full actuarial measurement |

---

## Section 3 -- Size Thresholds

Canada does not have statutory "size thresholds" determining accounting framework in the way EU countries do. Instead:

| Criterion | Determining factor |
|---|---|
| Public accountability | If securities are publicly traded or entity holds assets in fiduciary capacity → must use IFRS |
| Private enterprise | May choose ASPE or IFRS |
| Audit requirement | Determined by corporate statute and shareholder agreement (not size per se) |

### Audit waiver conditions (CBCA s.163)

Private corporations may waive the audit if:
- All shareholders consent annually (unanimous resolution)
- Corporation is not a distributing corporation (publicly traded)
- Revenue ≤ specified thresholds do NOT apply federally (it's purely consent-based)

### Provincial variations (examples)

| Jurisdiction | Audit waiver condition |
|---|---|
| CBCA (federal) | Unanimous shareholder consent (s.163) |
| OBCA (Ontario) | Unanimous shareholder consent (s.148) |
| BCBCA (British Columbia) | Shareholder resolution; no exemption for reporting issuers |
| ABCA (Alberta) | Unanimous shareholder consent |
| Quebec (QBCA) | Shareholder resolution; restrictions for certain entities |

---

## Section 4 -- Required Financial Statements

Under ASPE (Section 1400, 1521) and CBCA/provincial statutes:

| Document | ASPE | IFRS |
|---|---|---|
| Balance Sheet / Statement of Financial Position | Required | Required |
| Income Statement / Statement of Comprehensive Income | Required | Required (+ OCI) |
| Statement of Retained Earnings / Changes in Equity | Required (retained earnings) | Required (full equity) |
| Statement of Cash Flows | Required | Required |
| Notes to Financial Statements | Required | Required (full IFRS disclosure) |
| Comparative information | Encouraged (not mandatory under ASPE) | Mandatory (minimum one prior period) |

---

## Section 5 -- Year-End Adjustments Checklist

| # | Adjustment | Canada-specific notes |
|---|---|---|
| 1 | Amortization/depreciation | ASPE 3061; systematic and rational; CCA rates for tax (not accounting) |
| 2 | Provisions | ASPE 3290; likely, estimable contingencies |
| 3 | Employee benefits | ASPE 3462; accrued vacation, bonus; pension funding vs expense |
| 4 | Bad debt allowance | ASPE 3856; incurred loss model (not ECL for ASPE) |
| 5 | Inventory | ASPE 3031; lower of cost (FIFO/weighted average) and NRV; no LIFO |
| 6 | Income taxes | ASPE 3465; taxes payable method OR future income taxes method (choice) |
| 7 | Foreign exchange | ASPE 1651; temporal method; current rate for monetary |
| 8 | Leases | ASPE 3065; finance/operating classification |
| 9 | Government assistance | ASPE 3800; cost reduction or income approach |
| 10 | Goodwill impairment | ASPE 3064; test when events indicate; amortise max 10 years |
| 11 | Related party transactions | ASPE 3840; measured at exchange amount or carrying value |
| 12 | Scientific Research & Experimental Development (SR&ED) | Capitalise or expense; ITC recognition |

---

## Section 6 -- Income Statement Format

ASPE does not prescribe a rigid format. Common Canadian presentation:

```
Revenue
Cost of goods sold
  ─── Gross profit ───

Expenses:
  Selling expenses
  General and administrative expenses
  Amortization of capital assets
  Amortization of intangible assets
  ─── Total expenses ───

  ─── Income from operations ───

Other income (expenses):
  Interest income
  Interest expense
  Gain (loss) on disposal of assets
  Foreign exchange gain (loss)
  ─── Total other income (expenses) ───

  ─── Income before income taxes ───

Provision for income taxes (current and future/deferred)
  ─── Net income for the year ───
```

---

## Section 7 -- Balance Sheet Format

Common Canadian ASPE presentation:

```
ASSETS

Current assets
  Cash and cash equivalents
  Short-term investments
  Accounts receivable
  Inventories
  Prepaid expenses
  Current portion of notes receivable

Capital assets (Property, plant and equipment)
  Land
  Buildings (net of accumulated amortization)
  Equipment (net of accumulated amortization)
  Leasehold improvements (net)

Intangible assets
  Goodwill
  Patents, trademarks, licences

Other assets
  Long-term investments
  Due from related parties

Total assets

─────────────────────────────────────

LIABILITIES

Current liabilities
  Bank indebtedness
  Accounts payable and accrued liabilities
  Income taxes payable
  Current portion of long-term debt
  Deferred revenue

Long-term liabilities
  Long-term debt
  Obligations under capital leases
  Future income tax liability (or deferred tax)

Total liabilities

─────────────────────────────────────

SHAREHOLDERS' EQUITY
  Share capital
  Contributed surplus
  Retained earnings

Total shareholders' equity

Total liabilities and shareholders' equity
```

---

## Section 8 -- Notes to Financial Statements

| # | Disclosure | ASPE | IFRS |
|---|---|---|---|
| 1 | Significant accounting policies | Required (Section 1505) | Required (IAS 1/IAS 8) |
| 2 | Capital assets / PPE | Required (Section 3061) | Required (IAS 16) |
| 3 | Financial instruments | Required (Section 3856) | Required (IFRS 7 — extensive) |
| 4 | Related party transactions | Required (Section 3840) | Required (IAS 24) |
| 5 | Commitments and contingencies | Required (Section 3290) | Required (IAS 37) |
| 6 | Income taxes | Required (Section 3465) | Required (IAS 12) |
| 7 | Revenue | Simplified | Required (IFRS 15 — extensive) |
| 8 | Leases | Required (Section 3065) | Required (IFRS 16) |
| 9 | Employee benefits / pensions | If applicable (Section 3462) | Required (IAS 19) |
| 10 | Subsequent events | Required (Section 3820) | Required (IAS 10) |
| 11 | Going concern | Required if uncertainty | Required (IAS 1) |
| 12 | Segment information | Not required | Required (IFRS 8 — listed) |

---

## Section 9 -- Filing Requirements

| Item | Detail |
|---|---|
| Corporate tax return (T2) | Filed with CRA within 6 months of fiscal year-end |
| Financial statements attached to T2 | Required — GIFI (General Index of Financial Information) coded |
| GIFI | Standard classification system for mapping financial statement lines to T2 |
| Annual return (CBCA) | Within 60 days of anniversary of incorporation |
| Provincial annual return | Varies (e.g., Ontario: within 6 months of fiscal year-end) |
| Public companies (securities filings) | File with provincial securities commissions (e.g., OSC, BCSC) — within 90 days of year-end (annual) |
| Filing format | T2 electronically via CRA My Business Account or certified tax software |
| Late filing penalty — T2 | 5% of unpaid tax + 1% per month (max 12 months) |
| Failure to file penalty | CRA can assess federal penalty + provincial equivalent |

### Assurance levels for CRA

| Level | Standard | When used |
|---|---|---|
| Audit | CAS (Canadian Auditing Standards) | Required by statute or shareholders; PAEs |
| Review | CSRE 2400 | Lender requirements; shareholder preference |
| Compilation (Notice to Reader) | CSRS 4200 | Owner-managed private companies; no assurance |

---

## Section 10 -- Audit Requirements

| Category | Requirement |
|---|---|
| Publicly accountable enterprise (PAE) | Mandatory audit (CAS) |
| CBCA private corporation | Audit required UNLESS unanimous shareholder waiver (s.163) |
| OBCA private corporation | Audit required UNLESS unanimous shareholder consent (s.148) |
| Federal not-for-profit (CNCA) | Audit required unless revenue < CAD 50,000 (review permitted < CAD 250,000) |
| Provincial NPO | Varies by province and revenue thresholds |
| Registered charity | Audit if revenue > CAD 250,000 (CRA requirement) |

### Practical guidelines (lender-driven)

| Loan amount | Typical assurance required |
|---|---|
| < CAD 250,000 | Compilation (Notice to Reader) often accepted |
| CAD 250,000–1,000,000 | Review engagement typically required |
| > CAD 1,000,000 | Audit typically required |

### Auditor qualification

Licensed CPA (Chartered Professional Accountant) holding a public accounting licence issued by a provincial CPA body. Must meet independence and continuing professional development requirements.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/canada-financial-statements) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
