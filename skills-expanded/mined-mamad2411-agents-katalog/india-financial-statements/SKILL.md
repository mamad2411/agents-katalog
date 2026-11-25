---
name: india-financial-statements
description: "> Use this skill when preparing, reviewing, or advising on annual financial statements for an Indian company. Trigger on phrases like \"financial statements India\", \"MCA filing\", \"AOC-4\", \"Schedule III\", \"Ind AS\", \"Indian Accounting Standards\", \"Companies Act 2013\", \"CARO\", \"statutory audit India\", \"ROC filing\", \"small company India\", \"OPC\", \"balance sheet format India\", or any question about preparing and filing statutory accounts under the Companies Act 2013. Covers Ind AS/AS frameworks, Schedule III formats, size thresholds, required statements, notes, MCA filing, and audit requirements."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: IN
  category: financial-statements
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/india-financial-statements"
  obligation: FS
---

# India Financial Statements Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | India (Republic of India) |
| Currency | INR |
| Filing authority | Ministry of Corporate Affairs (MCA) — Registrar of Companies (ROC) |
| Primary legislation | Companies Act, 2013 (Sections 128–138) |
| Supporting legislation | Companies (Accounts) Rules, 2014; Companies (Audit and Auditors) Rules, 2014 |
| Accounting standards | Ind AS (Indian Accounting Standards — IFRS-converged) or AS (Accounting Standards) |
| Financial year | 1 April – 31 March (mandatory for most companies) |
| Filing deadline | 30 days from AGM (e-Form AOC-4); AGM within 6 months of year-end |
| Late filing penalty | Additional fee of INR 100 per day of delay |
| Digital filing | MCA21 portal (e-Form AOC-4 / AOC-4 XBRL / AOC-4 CFS) |

---

## Section 2 -- Reporting Framework

| Entity type | Applicable standard |
|---|---|
| Listed companies | Ind AS (mandatory) |
| Unlisted companies — net worth ≥ INR 250 crore | Ind AS (mandatory) |
| Unlisted companies — net worth < INR 250 crore | AS (Indian GAAP) unless voluntarily adopting Ind AS |
| Banking companies | Ind AS (mandatory from 2019) |
| Insurance companies | Ind AS (mandatory from 2023) |
| NBFCs — net worth ≥ INR 250 crore | Ind AS (mandatory) |
| Small companies (Section 2(85)) | AS (simplified requirements) |
| One Person Companies (OPC) | AS (simplified) |

### Ind AS applicability (phased rollout)

| Phase | Companies covered | Effective from |
|---|---|---|
| Phase I | Listed + net worth ≥ INR 500 crore | 1 April 2016 |
| Phase II | Unlisted net worth ≥ INR 250 crore + listed on SME exchange | 1 April 2017 |
| Others | Voluntary adoption permitted; mandatory if thresholds met | Ongoing |

---

## Section 3 -- Size Thresholds

### Small Company (Section 2(85) — effective 1 December 2025)

A private company qualifies as a "Small Company" if:

| Criterion | Threshold |
|---|---|
| Paid-up share capital | ≤ INR 10 crore (INR 100,000,000) |
| Turnover (per last P&L) | ≤ INR 100 crore (INR 1,000,000,000) |

Both conditions must be met. Excludes: public companies, Section 8 companies, and companies governed by special Acts.

### One Person Company (OPC) — Section 2(62)

| Criterion | Threshold |
|---|---|
| Paid-up share capital | ≤ INR 50 lakh |
| Turnover | ≤ INR 2 crore |

### Implications of Small Company status

- Exempt from cash flow statement in financial statements
- Exempt from CARO 2020
- Exempt from auditor rotation requirements
- Abridged directors' report permitted
- No requirement for internal financial controls (IFC) reporting by auditor
- Board meetings: minimum 2 per year (instead of 4)

---

## Section 4 -- Required Financial Statements

Under Section 2(40) and Section 129 of Companies Act 2013:

| Document | All companies | Small company exemptions |
|---|---|---|
| Balance Sheet | Required (Schedule III format) | Required |
| Statement of Profit and Loss | Required (Schedule III format) | Required |
| Statement of Changes in Equity | Required (Ind AS companies) | Not required (AS companies) |
| Cash Flow Statement | Required | Exempt (small companies and OPCs) |
| Notes to Financial Statements | Required | Required (simplified) |
| Directors' Report (Section 134) | Required | Abridged version permitted |
| Auditor's Report | Required (all companies must be audited) | Required (but CARO exempt) |
| Consolidated Financial Statements | Required if subsidiary/associate/JV exists (Section 129(3)) | Required if applicable |

---

## Section 5 -- Year-End Adjustments Checklist

| # | Adjustment | India-specific notes |
|---|---|---|
| 1 | Depreciation | Schedule II to Companies Act prescribes useful lives; component accounting under Ind AS |
| 2 | Provisions | Ind AS 37 / AS 29; present obligation, probable, reliably estimable |
| 3 | Employee benefits | Ind AS 19 / AS 15; gratuity (actuarial valuation mandatory); leave encashment |
| 4 | Expected credit losses | Ind AS 109 (ECL model); AS 4 (incurred loss) for non-Ind AS |
| 5 | Inventory | Ind AS 2 / AS 2; lower of cost and NRV; FIFO or weighted average |
| 6 | Deferred tax | Ind AS 12 / AS 22; temporary differences; effective rate ~25.17% (new regime) or 30%+ |
| 7 | Foreign exchange | Ind AS 21 / AS 11; monetary items at closing rate |
| 8 | Lease accounting | Ind AS 116 (right-of-use); AS 19 (finance/operating) for non-Ind AS |
| 9 | Revenue recognition | Ind AS 115 (5-step model); AS 9 for non-Ind AS |
| 10 | Government grants | Ind AS 20 / AS 12 |
| 11 | Gratuity provision | Payment of Gratuity Act 1972; actuarial valuation by qualified actuary |
| 12 | CSR provision | Section 135; if criteria met, provide for unspent CSR amount |

---

## Section 6 -- Statement of Profit and Loss Format

Schedule III, Part II (by nature/function — Division I for non-Ind AS; Division II for Ind AS):

```
I.   Revenue from operations
     (a) Sale of products
     (b) Sale of services
     (c) Other operating revenue

II.  Other income

III. Total income (I + II)

IV.  Expenses:
     (a) Cost of materials consumed
     (b) Purchases of stock-in-trade
     (c) Changes in inventories of FG, WIP and stock-in-trade
     (d) Employee benefits expense
     (e) Finance costs
     (f) Depreciation and amortisation expense
     (g) Other expenses

V.   Total expenses

VI.  Profit before exceptional items and tax (III - V)

VII. Exceptional items

VIII. Profit before tax (VI + VII)

IX.  Tax expense:
     (a) Current tax
     (b) Deferred tax

X.   Profit for the period (VIII - IX)

XI.  Other comprehensive income (Ind AS only)
     (a) Items not reclassified to profit or loss
     (b) Items that will be reclassified to profit or loss

XII. Total comprehensive income (X + XI)
```

---

## Section 7 -- Balance Sheet Format

Schedule III, Part I:

```
EQUITY AND LIABILITIES

Shareholders' Funds
  (a) Share capital
  (b) Reserves and surplus
  (c) Money received against share warrants

Share Application Money Pending Allotment

Non-Current Liabilities
  (a) Long-term borrowings
  (b) Deferred tax liabilities (net)
  (c) Other long-term liabilities
  (d) Long-term provisions

Current Liabilities
  (a) Short-term borrowings
  (b) Trade payables
      - Total outstanding dues of MSMEs
      - Total outstanding dues of others
  (c) Other current liabilities
  (d) Short-term provisions

TOTAL

─────────────────────────────────────

ASSETS

Non-Current Assets
  (a) Property, plant and equipment
      - Tangible assets
      - Intangible assets
      - Capital work-in-progress
      - Intangible assets under development
  (b) Non-current investments
  (c) Deferred tax assets (net)
  (d) Long-term loans and advances
  (e) Other non-current assets

Current Assets
  (a) Current investments
  (b) Inventories
  (c) Trade receivables
  (d) Cash and cash equivalents
  (e) Short-term loans and advances
  (f) Other current assets

TOTAL
```

Note: Ind AS companies use Division II format which presents equity separately and has a different ordering.

---

## Section 8 -- Notes to Financial Statements

| # | Disclosure | AS (non-Ind AS) | Ind AS |
|---|---|---|---|
| 1 | Significant accounting policies | Required (AS 1) | Required (Ind AS 1/8) |
| 2 | Property, plant and equipment | Required (Schedule III) | Required (Ind AS 16) |
| 3 | Share capital details | Required | Required |
| 4 | Borrowings (terms, security) | Required | Required |
| 5 | Trade payables (MSME ageing) | Required (MSMED Act) | Required |
| 6 | Related party transactions | Required (AS 18) | Required (Ind AS 24 — extensive) |
| 7 | Contingent liabilities and commitments | Required (AS 29) | Required (Ind AS 37) |
| 8 | Employee benefits / gratuity | Required (AS 15) | Required (Ind AS 19 — full actuarial) |
| 9 | Deferred tax | Required (AS 22) | Required (Ind AS 12) |
| 10 | Revenue recognition | Simplified (AS 9) | Required (Ind AS 115 — disaggregation) |
| 11 | Financial instruments | Not applicable | Required (Ind AS 107 — extensive) |
| 12 | Earnings per share | Required (AS 20) — listed only | Required (Ind AS 33) |
| 13 | Segment reporting | Required (AS 17) — listed | Required (Ind AS 108) — listed |
| 14 | CSR expenditure | Required (if Section 135 applies) | Required |

---

## Section 9 -- Filing Requirements

| Item | Detail |
|---|---|
| Filing authority | MCA (Ministry of Corporate Affairs) via MCA21 portal |
| Filing form | e-Form AOC-4 (standalone); AOC-4 CFS (consolidated); AOC-4 XBRL (if applicable) |
| AGM deadline | Within 6 months from financial year-end (i.e., by 30 September for March year-end) |
| Filing deadline (AOC-4) | Within 30 days from date of AGM |
| Latest possible date | Approximately 31 October (for March year-end companies) |
| XBRL filing mandatory for | Companies with capital ≥ INR 5 crore OR turnover ≥ INR 150 crore; all listed companies |
| Filing fee | INR 200–600 depending on authorised capital |
| Additional fee (late filing) | INR 100 per day of delay (no maximum cap) |
| Digital signature | DSC of director + practicing professional (CA/CS/CMA) |
| Format | Figures in absolute rupees (not in lakhs/crores) |

### Non-filing consequences

- Additional fee accumulates daily
- Directors may be disqualified under Section 164(2) if 3 consecutive years' filings are missed
- Company may be struck off under Section 248

---

## Section 10 -- Audit Requirements

### Statutory audit (Section 139–147)

**ALL companies** incorporated under the Companies Act 2013 must have their financial statements audited by a Chartered Accountant. There is no audit exemption by size in India.

| Category | Audit requirement | CARO 2020 applicable? |
|---|---|---|
| Listed companies | Mandatory; audit + CARO | Yes |
| Public companies (non-listed) | Mandatory; audit + CARO | Yes (unless exempt) |
| Private companies (non-small) | Mandatory; audit + CARO | Yes (unless exempt) |
| Small companies | Mandatory; audit only | No — CARO exempt |
| OPC | Mandatory; audit only | No — CARO exempt |
| Section 8 companies (NPO) | Mandatory; audit only | No — CARO exempt |

### CARO 2020 exemption for private companies

A private company is also exempt from CARO 2020 (in addition to small companies) if it simultaneously meets ALL of:
- Paid-up capital + reserves ≤ INR 1 crore
- Total borrowings ≤ INR 1 crore (from banks/financial institutions)
- Total revenue ≤ INR 10 crore

### Auditor rotation (Section 139(2))

| Company type | Individual auditor | Audit firm |
|---|---|---|
| Listed / prescribed class | 1 term of 5 consecutive years | 2 terms of 5 years (total 10 years) |
| Small companies | Exempt from rotation | Exempt from rotation |
| OPC | Exempt from rotation | Exempt from rotation |

### Internal audit (Section 138)

Required if:
- Listed company
- Unlisted public company with: turnover ≥ INR 200 crore OR paid-up capital ≥ INR 50 crore OR loans/borrowings ≥ INR 100 crore OR deposits ≥ INR 25 crore
- Private company with: turnover ≥ INR 200 crore OR loans/borrowings ≥ INR 100 crore

### Auditor qualification

Chartered Accountant (CA) holding Certificate of Practice, or firm of Chartered Accountants, registered with the Institute of Chartered Accountants of India (ICAI). For companies requiring CARO reporting, the auditor must also comply with Standards on Auditing (SA) issued by ICAI.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/india-financial-statements) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
