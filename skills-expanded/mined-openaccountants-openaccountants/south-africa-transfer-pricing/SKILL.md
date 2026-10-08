---
name: south-africa-transfer-pricing
description: "> Use this skill whenever asked about South Africa transfer pricing rules, documentation requirements, or SARS transfer pricing compliance. Trigger on phrases like \"transfer pricing South Africa\", \"SA TP documentation\", \"SARS transfer pricing\", \"master file South Africa\", \"local file South Africa\", \"CbCR South Africa\", \"Section 31 ITA\", \"arm's length South Africa\", or any question about intercompany pricing for South African entities."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: ZA
  category: transfer-pricing
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/south-africa-transfer-pricing"
  obligation: TP
---

# South Africa Transfer Pricing Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | South Africa (Republic of South Africa) |
| Tax authority | South African Revenue Service (SARS) |
| Key TP legislation | Section 31, Income Tax Act 58 of 1962 |
| Documentation | Public Notice 1117 (under Tax Administration Act, 2011); CbC Regulations (GN R.1598, Dec 2016) |
| Interpretation Note | SARS Interpretation Note 127 (thin capitalisation and TP for loans) |
| OECD member? | No (but BEPS Inclusive Framework member; follows OECD Guidelines) |
| BEPS signatory? | Yes (Inclusive Framework member) |
| Currency | ZAR (South African Rand) |
| Documentation language | English |
| Skill version | 1.0 |

---

## Section 2 -- Documentation Requirements

### 2.1 Documentation Threshold

| Item | Detail |
|---|---|
| Mandatory TP documentation (Master File + Local File) | Aggregated cross-border connected party transactions (without offsetting) exceed or are reasonably expected to exceed R100 million for the tax year |
| Individual transaction records | Where an individual transaction exceeds or is expected to exceed R5 million |
| Below threshold | Must still substantiate arm's length pricing; TP policy/strategy recommended |

### 2.2 Master File

| Item | Detail |
|---|---|
| Required? | Yes, where R100m threshold met |
| Format | OECD-aligned (BEPS Action 13) |
| Filing | Filed with SARS (within 12 months of year-end) |
| Size limit | Each file ≤ 5MB; combined submissions ≤ 100MB (PDF format) |

### 2.3 Local File

| Item | Detail |
|---|---|
| Required? | Yes, where R100m threshold met |
| Format | OECD-aligned; entity-specific analysis of material transactions |
| Filing | Filed with SARS (within 12 months of year-end or assessment year) |
| Content | All material transactions, FAR analysis, method selection, comparables, financial data |

### 2.4 Country-by-Country Report (CbCR)

| Item | Detail |
|---|---|
| Threshold | MNE groups with consolidated group revenue ≥ R10 billion |
| Filing deadline | 12 months after last day of reporting FY of MNE group |
| Filing method | Electronic (CbC01 form via SARS eFiling) |
| Format | Per BEPS Action 13 / OECD Annex III |
| Effective | From fiscal years beginning on/after 1 January 2016 |

---

## Section 3 -- Arm's Length Standard

### 3.1 Definition

Section 31(2) ITA: Where a transaction has been entered into between connected persons and the terms/conditions differ from arm's length terms, and the taxpayer derives a tax benefit, an adjustment must be made to reflect arm's length conditions.

### 3.2 Connected Persons

Widely defined under Section 1 ITA -- includes entities where >50% voting rights/participation, common control, and other relationship criteria.

### 3.3 Accepted Methods

| Method | Accepted |
|---|---|
| Comparable Uncontrolled Price (CUP) | Yes |
| Resale Price Method (RPM) | Yes |
| Cost Plus Method (CPM) | Yes |
| Transactional Net Margin Method (TNMM) | Yes |
| Profit Split Method (PSM) | Yes |

### 3.4 Preferred Method

SARS follows OECD "most appropriate method" principle. CUP preferred where reliable comparables available. The ABD Limited Tax Court case (2024) confirmed CUP methodology based on prior independent party agreements.

### 3.5 Deemed Loan Rule (Secondary Adjustment)

Section 31(3): Where a TP adjustment is made, the "excess" amount is deemed to be a loan from the South African entity to the connected person, subject to interest at the official rate (unless repaid within prescribed time).

---

## Section 4 -- Filing Obligations

| Obligation | Detail |
|---|---|
| Master File + Local File | Filed via eFiling (where R100m threshold met) |
| CbCR (CbC01 form) | Annual electronic filing via eFiling |
| Income Tax Return (ITR14) | Annual; includes related-party transaction disclosures |
| International Tax compliance | Supplementary schedules in ITR14 |
| Below-threshold entities | No mandatory filing but must demonstrate arm's length compliance |

---

## Section 5 -- Deadlines

| Item | Deadline |
|---|---|
| Master File + Local File filing (R100m+ entities) | 12 months after end of year of assessment |
| CbCR filing | 12 months after last day of reporting FY of MNE group |
| ITR14 corporate tax return | 12 months after end of year of assessment |
| Provisional tax | Bi-annual (6 months and 12 months into assessment year) |
| Secondary adjustment (deemed loan) remedy | Repayment within time frame to avoid deemed loan |

---

## Section 6 -- Penalties

### 6.1 Understatement Penalty (Section 222-223, Tax Administration Act)

| Behaviour | Standard Case | Obstructive/Repeat |
|---|---|---|
| Substantial understatement | 10% | 20% |
| Reasonable care not taken | 25% | 50% |
| No reasonable grounds for position | 50% | 75% |
| Gross negligence | 100% | 125% |
| Intentional tax evasion | 150% | 200% |

### 6.2 Administrative Penalties

| Offence | Penalty |
|---|---|
| Late/non-filing of returns | Fixed amount per month (R250 to R16,000 depending on assessed tax) |
| Failure to file CbCR | Administrative non-compliance penalties |
| Inadequate documentation on audit | Shifts burden of proof; enables SARS estimation |

### 6.3 Bona Fide Defence

No penalty if understatement resulted from a bona fide inadvertent error by the taxpayer.

---

## Section 7 -- Advance Pricing Agreements (APA)

| Item | Detail |
|---|---|
| Availability | Limited (no formal legislative APA program) |
| Current mechanism | Advance Tax Ruling (ATR) system under Tax Administration Act |
| MAP | Available under South Africa's DTA network |
| Bilateral APA | May be achieved through MAP/competent authority negotiations |
| Formal APA legislation | Not yet enacted; SARS has indicated interest in developing formal program |
| Alternative | Taxpayers rely on proper documentation and Advance Tax Rulings |

---

## Section 8 -- Safe Harbours

South Africa does not have formal safe harbour rules for transfer pricing.

| Area | Detail |
|---|---|
| Low-value services | No safe harbour; arm's length analysis required |
| Interest rates | No safe harbour; SARS Interpretation Note 127 provides guidance on thin capitalisation |
| Thin capitalisation | 3:1 debt-to-equity ratio as starting point (IN 127); not a strict safe harbour |
| General | All cross-border connected party transactions must satisfy arm's length standard |

---

## Section 9 -- Recent Developments

| Date | Development |
|---|---|
| February 2024 | ABD Limited v CSARS -- first Tax Court judgment on transfer pricing (CUP method upheld) |
| 2024 | SARS Interpretation Note 127: guidance on thin capitalisation and intercompany loans |
| 2024 | Increased SARS audit focus on transfer pricing (royalties, management fees, IP) |
| 2023 | Pillar Two considerations under discussion (no legislation yet) |
| 2017 | CbCR reporting effective; Public Notice 1117 documentation requirements |
| 2016 | CbC Regulations published (GN R.1598) |
| Ongoing | SARS building TP audit capability; increasing enforcement |
| Ongoing | No formal APA legislation, but advance ruling system available |

---

## Section 10 -- Interaction with Other Skills

| Related skill | Interaction |
|---|---|
| south-africa-corporate-tax | TP adjustments under s.31 directly affect taxable income |
| south-africa-vat | TP adjustments may affect open market value for VAT purposes |
| south-africa-bookkeeping | TP documentation builds on IFRS-compliant accounting records |
| Thin capitalisation (IN 127) | Interacts with TP for intercompany loan pricing |
| Secondary adjustment (s.31(3)) | Deemed loan with interest implications |
| Exchange control | Cross-border pricing has exchange control implications (SARB) |
| CbCR | SARS uses CbCR for risk assessment and audit selection |

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/south-africa-transfer-pricing) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
