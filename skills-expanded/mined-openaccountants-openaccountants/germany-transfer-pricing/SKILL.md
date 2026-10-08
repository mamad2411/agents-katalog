---
name: germany-transfer-pricing
description: "> Use this skill whenever asked about Germany transfer pricing rules, documentation requirements, or Verrechnungspreise compliance. Trigger on phrases like \"transfer pricing Germany\", \"German TP documentation\", \"Verrechnungspreise\", \"master file Germany\", \"local file Germany\", \"CbCR Germany\", \"APA Germany\", \"§90 AO\", \"transaction matrix Germany\", \"BZSt\", or any question about intercompany pricing for German entities."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: DE
  category: transfer-pricing
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/germany-transfer-pricing"
  tax_year: 2025
  obligation: TP
---

# Germany Transfer Pricing Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | Germany (Federal Republic of Germany) |
| Tax authority | Federal Central Tax Office (Bundeszentralamt für Steuern -- BZSt); local tax offices for audits |
| Key TP legislation | §90(3) Abgabenordnung (AO -- General Tax Code); §1 Außensteuergesetz (AStG -- Foreign Tax Act) |
| Documentation regulation | GAufzV (Gewinnabgrenzungsaufzeichnungsverordnung) |
| OECD member? | Yes |
| BEPS signatory? | Yes |
| Effective date (current regime) | Three-tier approach from FYs beginning after 31 Dec 2016; major reforms from 1 Jan 2025 |
| Currency | EUR |
| Documentation language | German (English accepted for Master File in practice) |
| Skill version | 1.0 |

---

## Section 2 -- Documentation Requirements

### 2.1 Master File (Stammdokumentation)

| Item | Detail |
|---|---|
| Required? | Yes, if consolidated group revenue in prior FY ≥ EUR 100 million |
| Format | OECD Annex I to Chapter V |
| Filing | Submit within 30 days of audit order (from 1 Jan 2025) |
| Language | German preferred; English accepted in practice |

### 2.2 Local File (Landesspezifische Dokumentation)

| Item | Detail |
|---|---|
| Required? | Yes, if related-party transaction thresholds exceeded |
| Thresholds | Goods: EUR 6 million/year; Other transactions (services, IP, finance): EUR 600,000/year |
| Format | Detailed arm's length analysis per transaction category |
| Filing | On separate request during audit (30-day deadline from request, from 2025) |

### 2.3 Transaction Matrix (Aufzeichnungen über die Geschäftsbeziehungen)

From 1 January 2025 (Fourth Bureaucracy Reduction Act -- BEG IV):

| Item | Detail |
|---|---|
| Content | Overview of all cross-border related-party transactions |
| Submission | Within 30 days of audit order announcement |
| Format | Standardized; clarified by BMF notice of 2 April 2025 |

### 2.4 Country-by-Country Report (CbCR)

| Item | Detail |
|---|---|
| Threshold | Consolidated group revenue ≥ EUR 750 million (prior FY) |
| Filing deadline | Within 12 months of end of FY |
| Filing method | Electronic (XML) to BZSt |
| Notification | Required from constituent entities |
| Effective | FYs beginning after 31 December 2015 |

---

## Section 3 -- Arm's Length Standard

### 3.1 Definition

§1 AStG: Income of a taxpayer from cross-border transactions with related parties must be determined as if the transactions had been agreed between unrelated parties under comparable conditions (arm's length principle). Germany applies a "hypothetical arm's length test" where no comparable exists.

### 3.2 Accepted Methods

| Method | Accepted |
|---|---|
| Comparable Uncontrolled Price (CUP) | Yes |
| Resale Price Method (RPM) | Yes |
| Cost Plus Method (CPM) | Yes |
| Transactional Net Margin Method (TNMM) | Yes |
| Profit Split Method (PSM) | Yes |
| Hypothetical arm's length test | Yes (unique to Germany) |

### 3.3 Preferred Method

Standard CUP is preferred where reliable comparables exist. The hypothetical arm's length test applies when no comparable transactions are available (particularly for unique intangibles and business restructurings).

### 3.4 Range/Median

Tax authorities may use the median of the interquartile range for adjustments if taxpayer's result falls outside the arm's length range.

---

## Section 4 -- Filing Obligations

| Obligation | Detail |
|---|---|
| Transaction matrix | Submit within 30 days of audit order (from 2025) |
| Master File | Submit within 30 days of audit order (from 2025) |
| Local File | Submit within 30 days of separate request during audit |
| Extraordinary transactions | Submit within 30 days of audit order |
| CbCR | Annual electronic filing with BZSt |
| CbCR notification | Annual notification to BZSt |
| Corporate tax return | No separate TP disclosure form |

---

## Section 5 -- Deadlines

| Item | Deadline |
|---|---|
| Documentation preparation | Contemporaneous; must be available when audit begins |
| Transaction matrix + Master File submission | 30 days from audit order (audits from 1 Jan 2025) |
| Local File submission | 30 days from separate request |
| Extraordinary transactions | 30 days from audit order |
| CbCR filing | 12 months after end of FY |
| Corporate tax return | Generally 31 July of year following FY (with extensions) |

---

## Section 6 -- Penalties

| Offence | Penalty |
|---|---|
| Non-submission or unusable documentation | 5-10% surcharge on income adjustment (minimum EUR 5,000 per transaction) |
| Late submission of documentation | EUR 100/day (minimum), up to EUR 1,000,000 |
| Non-submission of transaction matrix | EUR 5,000 minimum surcharge |
| Late/missing CbCR | Up to EUR 10,000 |
| Late/missing CbCR notification | Up to EUR 10,000 |
| Adverse estimation | Tax authorities may estimate income to taxpayer's disadvantage |
| Burden of proof | Shifts to taxpayer where documentation is inadequate |

---

## Section 7 -- Advance Pricing Agreements (APA)

| Item | Detail |
|---|---|
| Availability | Yes |
| Types | Unilateral, Bilateral, Multilateral |
| Governing authority | BZSt (coordinates with local tax office) |
| Application fee | EUR 20,000 (simplified: EUR 10,000) |
| Typical duration | 3-5 years prospective; rollback possible |
| Processing time | 12-36 months (bilateral longer) |
| Binding effect | Binding on tax authorities for covered period |
| Annual reporting | Compliance reports required |

---

## Section 8 -- Safe Harbours

Germany does not have broad statutory safe harbour rules.

| Area | Detail |
|---|---|
| Low-value intra-group services | OECD simplified approach (cost-plus 5%) generally accepted in practice |
| Interest rates | No formal safe harbour; Bundesbank reference rates used as benchmarks |
| Documentation thresholds | Below EUR 6m (goods) / EUR 600k (other), no Local File required but arm's length must still be demonstrated |
| Small transactions | No statutory de minimis; all cross-border related-party transactions subject to arm's length principle |

### 8.1 Practical Implications of Documentation Thresholds

While Germany has no formal safe harbour, the documentation thresholds effectively reduce compliance burden:
- Below EUR 6m goods / EUR 600k other: no Local File required
- Below EUR 100m group revenue: no Master File required
- However, the general obligation under §90 AO to cooperate with tax authorities remains
- Tax authorities can still challenge pricing even without formal documentation requirements

---

## Section 9 -- Recent Developments

| Date | Development |
|---|---|
| January 2025 | BEG IV: Transaction matrix mandatory; shortened submission deadlines (30 days) |
| April 2025 | BMF information sheet on transaction matrix content |
| 2024 | Pillar Two (GloBE) implemented via Mindeststeuergesetz (MinStG) for FYs from 31 Dec 2023 |
| Ongoing | Increased audit intensity on TP; digital audit tools deployed |
| 2022 | §1 AStG reform: enhanced hypothetical arm's length test for function relocations |
| Ongoing | OECD Pillar One Amount B: Germany monitoring implementation |

---

## Section 10 -- Interaction with Other Skills

| Related skill | Interaction |
|---|---|
| germany-bookkeeping | TP documentation builds on general bookkeeping records; related-party disclosures |
| germany-corporate-tax | TP adjustments directly affect corporate income tax (Körperschaftsteuer) and trade tax (Gewerbesteuer) |
| germany-vat | TP adjustments may affect customs value and import VAT |
| CbCR | Risk assessment tool used by BZSt to select audit targets |
| Financial statements | HGB/IFRS related-party disclosures must be consistent with TP positions |

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/germany-transfer-pricing) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
