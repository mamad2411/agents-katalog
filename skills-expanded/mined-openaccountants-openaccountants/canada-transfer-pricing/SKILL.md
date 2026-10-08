---
name: canada-transfer-pricing
description: "> Use this skill whenever asked about Canada transfer pricing rules, documentation requirements, or CRA transfer pricing compliance. Trigger on phrases like \"transfer pricing Canada\", \"Canadian TP documentation\", \"CRA transfer pricing\", \"master file Canada\", \"local file Canada\", \"CbCR Canada\", \"APA Canada\", \"Section 247\", \"Form T106\", \"contemporaneous documentation Canada\", or any question about intercompany pricing for Canadian entities."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: CA
  category: transfer-pricing
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/canada-transfer-pricing"
  obligation: TP
---

# Canada Transfer Pricing Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | Canada |
| Tax authority | Canada Revenue Agency (CRA) |
| Key TP legislation | Section 247, Income Tax Act (ITA) |
| Documentation | Subsection 247(4) ITA -- contemporaneous documentation |
| CbCR | Form RC4649; Part XVIII of the ITA |
| OECD member? | Yes |
| BEPS signatory? | Yes |
| Currency | CAD |
| Documentation language | English or French |
| Skill version | 1.0 |

---

## Section 2 -- Documentation Requirements

### 2.1 Contemporaneous Documentation (Section 247(4))

| Item | Detail |
|---|---|
| Required? | Yes, for all taxpayers with non-arm's length transactions with non-residents (where Form T106 filed) |
| Threshold | Aggregate transactions > CAD 1 million with any single non-resident related party |
| Timing | Must be prepared or obtained by the "documentation-due date" (tax return filing deadline) |
| Content | Six prescribed items per s.247(4)(a): parties, terms, method, assumptions, comparable data, adjustments |
| Provision to CRA | Within 3 months of written request (reducing to 30 days for years beginning after 4 Nov 2025) |

### 2.2 Form T106 -- Information Return

| Item | Detail |
|---|---|
| Required? | Yes, if total non-arm's length transactions with non-residents > CAD 1 million in tax year |
| Filing deadline | 6 months after end of taxation year (aligns with corporate tax return) |
| Content | Summary of all non-arm's length transactions by non-resident party |

### 2.3 Master File / Local File

Canada does not formally mandate OECD-style Master File / Local File (no separate filing). However, the 2025 draft legislation introduces enhanced documentation aligning with OECD standards for years beginning after November 4, 2025.

### 2.4 Country-by-Country Report (Form RC4649)

| Item | Detail |
|---|---|
| Threshold | Consolidated group revenue ≥ EUR 750 million |
| Filing deadline | 12 months after fiscal year-end |
| Applies to | Canadian ultimate parent entities of qualifying MNE groups |
| Notification | Required (CBC2 notification form) |

---

## Section 3 -- Arm's Length Standard

### 3.1 Definition

Section 247(2) ITA: Where terms/conditions between a taxpayer and a non-arm's length non-resident differ from those that would have been made between arm's length parties, adjustments are made to reflect arm's length conditions.

### 3.2 Accepted Methods

| Method | Accepted |
|---|---|
| Comparable Uncontrolled Price (CUP) | Yes |
| Resale Price Method (RPM) | Yes |
| Cost Plus Method (CPM) | Yes |
| Transactional Net Margin Method (TNMM) | Yes |
| Profit Split Method (PSM) | Yes |

### 3.3 Preferred Method

No statutory hierarchy. CRA accepts most appropriate method per OECD Guidelines. IC 87-2R provides administrative guidance.

### 3.4 Recharacterization Power

Section 247(2)(b)(c)(d): CRA can recharacterize transactions if they would not have been entered into at all between arm's length parties (not just reprice them).

---

## Section 4 -- Filing Obligations

| Obligation | Detail |
|---|---|
| Contemporaneous documentation | Prepared by documentation-due date; provided within 3 months (30 days from 2025+) of CRA request |
| Form T106 | Annual information return (if threshold met) |
| Form T1134 | Information return for foreign affiliates |
| Form RC4649 (CbCR) | Annual filing (EUR 750m+ groups) |
| CBC2 notification | Annual notification |
| Corporate tax return (T2) | Annual self-assessment |

---

## Section 5 -- Deadlines

| Item | Deadline |
|---|---|
| Documentation preparation | By documentation-due date (corporate: 6 months after year-end) |
| Provision to CRA on request | 3 months from written request (30 days for years beginning after 4 Nov 2025) |
| Form T106 | 6 months after taxation year-end |
| CbCR (RC4649) | 12 months after fiscal year-end |
| T2 corporate tax return | 6 months after taxation year-end |
| T2 tax payment | 2-3 months after year-end (depending on entity type) |

---

## Section 6 -- Penalties

### 6.1 Transfer Pricing Penalty (s.247(3))

| Item | Detail |
|---|---|
| Trigger threshold | Net TP adjustment exceeds lesser of: CAD 5 million OR 10% of gross revenue (threshold increased to CAD 10 million from 2025+) |
| Penalty rate | 10% of the TP adjustment amount exceeding the threshold |
| Reasonable efforts defence | No penalty if taxpayer made "reasonable efforts" to determine arm's length pricing |
| Documentation impact | Failure to meet s.247(4) requirements = deemed NOT to have made reasonable efforts |

### 6.2 Other Penalties

| Offence | Penalty |
|---|---|
| Late filing Form T106 | CAD 25/day, minimum CAD 100, maximum CAD 2,500 |
| Failure to file Form T106 | Up to CAD 2,500 per return |
| Late CbCR | Standard administrative penalties |

---

## Section 7 -- Advance Pricing Agreements (APA)

| Item | Detail |
|---|---|
| Availability | Yes (active program) |
| Types | Unilateral, Bilateral, Multilateral |
| Governing guidance | IC 94-4R (International Circular) |
| Application | To CRA Competent Authority Division |
| Duration | Typically 5 years prospective; rollback for up to 5 prior years |
| Fees | No application fee |
| Processing time | 2-4 years (bilateral takes longer) |
| Annual compliance report | Required |
| Key benefit | Eliminates penalty exposure for covered transactions |

---

## Section 8 -- Safe Harbours

Canada does not have formal statutory safe harbour rules for transfer pricing.

| Area | Detail |
|---|---|
| Low-value services | No formal safe harbour; CRA may accept 5% cost-plus in low-risk scenarios |
| Interest rates | No safe harbour; market benchmarking required (thin cap rules separate) |
| Simplified documentation (2025+) | Draft legislation introduces simplified requirements where prescribed conditions met |
| Small transactions | No de minimis; all related-party transactions should be at arm's length |
| Form T106 threshold | Aggregate transactions ≤ CAD 1 million: no Form T106 filing required |

### 8.1 Practical Risk Assessment

CRA uses a risk-based approach to TP audits, focusing on:
- Large/complex transactions with high-risk jurisdictions
- Transactions involving intangibles and cost-sharing arrangements
- Financial transactions (intercompany loans, guarantees)
- Entities with thin capitalisation concerns
- Losses sustained over multiple years in Canada

### 8.2 2025 Simplified Documentation

Draft legislation for taxation years beginning after November 4, 2025 introduces:
- Simplified contemporaneous documentation for taxpayers meeting prescribed conditions
- Conditions and scope still being finalized through consultation
- Intended to reduce compliance burden for lower-risk transactions

---

## Section 9 -- Recent Developments

| Date | Development |
|---|---|
| August 2025 | Draft legislation: enhanced TP documentation requirements (OECD-aligned analytical framework) |
| November 2025 | New rules effective for taxation years beginning after 4 November 2025 |
| 2025 | Penalty threshold increased to lesser of CAD 10 million or 10% of gross revenue |
| 2025 | Response time for documentation reduced from 3 months to 30 days |
| 2024 | Pillar Two implementation underway |
| Ongoing | CRA increased TP audit activity on intangibles and financial transactions |
| Ongoing | Simplified documentation measures for prescribed conditions introduced |

---

## Section 10 -- Interaction with Other Skills

| Related skill | Interaction |
|---|---|
| canada-bookkeeping | TP documentation relies on Canadian accounting records |
| canada-corporate-tax | TP adjustments under s.247 directly affect taxable income |
| canada-gst-hst | TP adjustments may affect customs value |
| Thin capitalisation | Separate debt-to-equity rules (s.18(4)) interact with TP for intercompany loans |
| Form T106 | Annual information return; compliance gateway for TP |
| CbCR | Used by CRA for risk-based audit selection |

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/canada-transfer-pricing) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
