---
name: ar-sales-tax
description: "Use this skill whenever asked about Arkansas sales and use tax. Trigger on phrases like \"Arkansas sales tax\", \"AR sales tax\", \"DFA\", \"A.C.A. §26-52\", \"Arkansas grocery tax\", \"Arkansas SST\". ALWAYS load us-sales-tax first."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-AR
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ar-sales-tax"
  obligation: CT
---

# Arkansas Sales and Use Tax Skill v2.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Section 1 -- Quick reference

| Field | Value |
|---|---|
| Jurisdiction | Arkansas |
| State rate | 6.50% |
| Grocery food state rate | 0.125% (reduced; local rates still apply at full rate) |
| Maximum combined rate | ~11.625% |
| Sourcing | Destination-based (SST) |
| Economic nexus | $100,000 OR 200 transactions |
| Tax authority | Arkansas Dept. of Finance and Administration |
| Portal | https://atap.arkansas.gov |
| SST member | Yes -- Full Member |
| Skill version | 2.0 |

## Section 3 -- Transaction pattern library

| Pattern | Taxable? | Notes |
|---|---|---|
| General TPP | TAXABLE 6.50% | |
| Clothing | TAXABLE | No exemption |
| Grocery food (unprepared) | 0.125% state + full local | Reduced, not exempt |
| Prepared food | TAXABLE 6.50% | |
| SaaS | NOT TAXABLE | Not clearly taxed |
| Canned software (download) | TAXABLE | |
| Professional services | NOT TAXABLE | |
| Manufacturing equipment | EXEMPT | |
| Prescription drugs | EXEMPT | |
| Resale | EXEMPT | |

## Section 10 -- Prohibitions

- NEVER say grocery food is exempt -- it is taxed at 0.125% state plus full local.
- NEVER forget SST certificates are accepted.
- NEVER compute any number.

## Disclaimer

Informational only. Review by qualified professional required before filing.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ar-sales-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
