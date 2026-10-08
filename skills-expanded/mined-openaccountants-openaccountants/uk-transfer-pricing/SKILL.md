---
name: uk-transfer-pricing
description: "> Use this skill whenever asked about UK transfer pricing rules, documentation, or HMRC compliance. Trigger on phrases like \"transfer pricing UK\", \"UK TP documentation\", \"HMRC transfer pricing\", \"arm's length UK\", \"master file UK\", \"local file UK\", \"CbCR UK\", \"APA HMRC\", \"TIOPA Part 4\", \"Transfer Pricing Records Regulations 2023\", or any question about intercompany pricing compliance for UK entities."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GB
  category: transfer-pricing
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/uk-transfer-pricing"
  tax_year: 2025-26
  obligation: TP
---

# UK Transfer Pricing Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

> **Year applicability:** Rules in this skill apply across **2024-25, 2025-26, and 2026-27** unless a specific section flags a year-dated change. The pack is read alongside the rate-bearing skills (`uk-income-tax-sa100`, `uk-national-insurance`, `uk-dividends`, etc.) which carry full 3-year tables.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | United Kingdom |
| Tax authority | HM Revenue & Customs (HMRC) |
| Key TP legislation | Part 4, Taxation (International and Other Provisions) Act 2010 (TIOPA 2010) |
| Documentation regulations | Transfer Pricing Records Regulations 2023 (SI 2023/818) |
| OECD member? | Yes |
| BEPS signatory? | Yes |
| Effective date (documentation regs) | Corporation Tax: accounting periods beginning on/after 1 April 2023; Income Tax: from 2024-25 |
| Currency | GBP |
| Documentation language | English |
| Skill version | 1.0 |

---

## Section 2 -- Documentation Requirements

### 2.1 Master File

| Item | Detail |
|---|---|
| Required? | Yes, for in-scope UK entities (MNEs meeting CbCR threshold with material controlled transactions) |
| Format | OECD Annex I to Chapter V of TP Guidelines (2022 edition) |
| Filing | Not filed; must be available on HMRC request within 30 days |
| Threshold | Part of a multinational group meeting the EUR 750m CbCR threshold |

### 2.2 Local File

| Item | Detail |
|---|---|
| Required? | Yes, for in-scope UK entities with material controlled transactions |
| Format | OECD Annex II to Chapter V of TP Guidelines (2022 edition) |
| Filing | Not filed; available on HMRC request within 30 days |
| Supplementary | Summary Audit Trail (SAT) -- subject to further consultation |

### 2.3 Exemptions from Specified TP Records

- UK-to-UK transactions (domestic exemption)
- Transactions covered by an APA
- Non-material controlled transactions
- Entities not part of a qualifying MNE group

Even if exempt from specified records, general TP documentation must still demonstrate arm's length compliance.

### 2.4 Country-by-Country Report (CbCR)

| Item | Detail |
|---|---|
| Threshold | Consolidated group revenue ≥ EUR 750 million |
| Filing deadline | 12 months after end of reporting period |
| Filing method | Electronic (XML), via HMRC |
| Notification | Required annually |

---

## Section 3 -- Arm's Length Standard

### 3.1 Definition

Section 147 TIOPA 2010: where conditions differ from those that would have been made between independent enterprises, profits may be adjusted to reflect arm's length conditions.

### 3.2 Accepted Methods

| Method | Accepted |
|---|---|
| Comparable Uncontrolled Price (CUP) | Yes |
| Resale Price Method (RPM) | Yes |
| Cost Plus Method (CPM) | Yes |
| Transactional Net Margin Method (TNMM) | Yes |
| Profit Split Method (PSM) | Yes |

### 3.3 Preferred Method

No strict hierarchy; most appropriate method based on facts and circumstances. HMRC follows OECD Guidelines.

### 3.4 Scope

- Applies to cross-border and domestic transactions
- Exemption for SMEs (from Part 4 adjustment): turnover < £10m and < 50 employees and assets < £5m
- One-way application: HMRC can only adjust upwards (taxpayer cannot self-adjust downwards without claim)

---

## Section 4 -- Filing Obligations

| Obligation | Detail |
|---|---|
| Specified TP records (Master/Local File) | Maintain; provide within 30 days of HMRC request |
| TP return/disclosure | No separate TP return; self-assessment within CT600 |
| CT600 declaration | Confirm arm's length compliance |
| CbCR filing | Annual electronic filing |
| APA annual report | Filed with company tax return |

---

## Section 5 -- Deadlines

| Item | Deadline |
|---|---|
| Documentation preparation | Before filing the relevant tax return |
| Documentation provision to HMRC | Within 30 days of information notice |
| Corporate tax return (CT600) | 12 months after end of accounting period |
| CbCR filing | 12 months after end of reporting period |
| CbCR notification | Within 12 months of end of reporting period |

---

## Section 6 -- Penalties

| Offence | Penalty |
|---|---|
| Failure to keep/preserve specified TP records | Up to £3,000 per failure per return period |
| Tax-geared penalty (inaccuracy in return) | Careless: 0-30%; Deliberate: 20-70%; Deliberate and concealed: 30-100% |
| Failure to notify CbCR | Standard information penalties |
| Late CbCR filing | Standard penalties for late returns |
| Failure to provide information on request (general) | £300 initial + £60/day ongoing |

---

## Section 7 -- Advance Pricing Agreements (APA)

| Item | Detail |
|---|---|
| Availability | Yes |
| Types | Unilateral, Bilateral, Multilateral |
| Governing legislation | Sections 218-230, TIOPA 2010 |
| Application | Expression of Interest (EOI) to BAI Transfer Pricing Team |
| Fees | No fees charged by HMRC |
| Typical duration | 3-5 years prospective (rollback possible) |
| Annual reporting | APA report filed with CT return |
| Process timeline | Unilateral: 12-18 months; Bilateral: 18-36 months |
| Competent Authority | HMRC BAI Transfer Pricing Team |

---

## Section 8 -- Safe Harbours

The UK does not have formal statutory safe harbour rules for transfer pricing.

However, several practical reliefs exist:

| Area | Detail |
|---|---|
| SME exemption | Entities with turnover < £10m, < 50 employees, assets < £5m: exempt from Part 4 adjustment |
| Medium-sized exemption | May apply for medium companies (< 250 employees, turnover < £36m or assets < £18m) unless transaction is with a tax haven |
| Low-value services | HMRC accepts OECD simplified approach (cost-plus 5%) for qualifying services |
| Materiality | HMRC applies practical materiality in audit selection; immaterial transactions unlikely to be challenged |
| UK-to-UK exemption | Domestic related-party transactions exempt from specified TP record requirements |

### 8.1 SME and Medium-Sized Company Exemptions

The SME and medium-sized company exemptions from Part 4 adjustments significantly narrow the scope of UK TP rules in practice. Medium-sized companies are exempt unless the counterparty is in a non-qualifying territory (tax haven).

### 8.2 Diverted Profits Tax Interaction

Companies within the SME/medium exemption may still be exposed to the Diverted Profits Tax (25% rate) if profits are diverted from the UK through arrangements lacking economic substance.

---

## Section 9 -- Recent Developments

| Date | Development |
|---|---|
| August 2023 | Transfer Pricing Records Regulations 2023 (SI 2023/818) published |
| April 2023 | Specified TP records effective for CT periods beginning on/after this date |
| 2024-25 | Specified TP records effective for Income Tax purposes |
| Ongoing | Summary Audit Trail (SAT) under further consultation |
| 2024 | BEPS Pillar Two (GloBE) implemented via Finance Act 2023 for periods from 31 Dec 2023 |
| Ongoing | OECD Pillar One Amount B: UK monitoring but not yet adopted |
| 2024 | Transfer pricing mismatch provisions under review |

---

## Section 10 -- Interaction with Other Skills

| Related skill | Interaction |
|---|---|
| uk-corporation-tax | TP adjustments increase taxable profits; interaction with loss utilisation |
| uk-vat | TP adjustments may affect customs value and VAT on imports |
| uk-bookkeeping | Related-party disclosures in financial statements must align with TP positions |
| Diverted Profits Tax (DPT) | 25% rate applies where profits diverted from UK; TP documentation relevant to DPT risk |
| CbCR | Global risk assessment tool; feeds HMRC compliance approach |

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/uk-transfer-pricing) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
