---
name: ks-sales-tax
description: "Use this skill whenever asked about Kansas sales and use tax. Trigger on phrases like \"Kansas sales tax\", \"KS sales tax\", \"KDOR\", \"K.S.A. §79-3603\", \"Kansas grocery tax\". ALWAYS load us-sales-tax first."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-KS
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ks-sales-tax"
  obligation: CT
---

# Kansas Sales and Use Tax Skill v2.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Section 1 -- Quick reference

| Field | Value |
|---|---|
| Jurisdiction | Kansas |
| State rate | 6.50% |
| Grocery food state rate | 0.00% (effective January 1, 2025 -- phased down from 6.5%) |
| Maximum combined rate | ~11.50% |
| Sourcing | Destination-based (SST) |
| Economic nexus | $100,000 in gross receipts |
| Tax authority | Kansas Department of Revenue (KDOR) |
| Portal | https://www.kdor.ks.gov |
| SST member | Yes -- Full Member |
| Skill version | 2.0 |

## Section 3 -- Transaction pattern library

| Pattern | Taxable? | Notes |
|---|---|---|
| General TPP | TAXABLE 6.50% + local | |
| Clothing | TAXABLE | No exemption |
| Grocery food (unprepared) | 0% state (as of Jan 2025) | Local rates still apply; phased down from 6.5% |
| Prepared food | TAXABLE 6.50% | |
| SaaS | NOT TAXABLE | Kansas has not clearly taxed SaaS |
| Canned software (download) | TAXABLE | |
| Professional services | NOT TAXABLE | |
| Manufacturing equipment | EXEMPT | |
| Prescription drugs | EXEMPT | |
| Resale | EXEMPT | |

## Section 10 -- Prohibitions

- NEVER apply state tax to grocery food as of 2025 -- state rate is 0%. Local still applies.
- NEVER forget the phase-down history of grocery food taxation.
- NEVER compute any number.

## Disclaimer

Informational only. Review by qualified professional required before filing.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ks-sales-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
