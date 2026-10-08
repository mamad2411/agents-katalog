---
name: ms-sales-tax
description: "Use this skill whenever asked about Mississippi sales and use tax. Trigger on phrases like \"Mississippi sales tax\", \"MS sales tax\", \"Miss. Code §27-65\". ALWAYS load us-sales-tax first."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-MS
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ms-sales-tax"
  obligation: CT
---

# Mississippi Sales and Use Tax Skill v2.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Section 1 -- Quick reference

| Field | Value |
|---|---|
| Jurisdiction | Mississippi |
| State rate | 7.00% |
| Local taxes | Very limited (up to 0.25% in some areas) |
| Maximum combined rate | ~7.25% |
| Sourcing | Origin-based |
| Economic nexus | $250,000 in sales |
| Tax authority | Mississippi Department of Revenue |
| Portal | https://www.dor.ms.gov |
| SST member | No |
| Skill version | 2.0 |

**Mississippi taxes MOST services broadly and taxes grocery food at a reduced rate.**

## Section 3 -- Transaction pattern library

| Pattern | Taxable? | Notes |
|---|---|---|
| General TPP | TAXABLE 7% | |
| Clothing | TAXABLE | No exemption |
| Grocery food | TAXABLE at 5% | Reduced rate (not exempt) |
| Prepared food | TAXABLE 7% | |
| SaaS | NOT TAXABLE | Not clearly taxed |
| Canned software | TAXABLE | |
| Most services | TAXABLE | Mississippi taxes services broadly |
| Professional services | Varies | Many professional services taxable |
| Manufacturing equipment | REDUCED RATE | |
| Prescription drugs | EXEMPT | |
| Resale | EXEMPT | |

## Section 10 -- Prohibitions

- NEVER say grocery food is exempt -- Mississippi taxes it at 5%.
- NEVER assume services are exempt -- Mississippi taxes most services.
- NEVER forget origin-based sourcing.
- NEVER compute any number.

## Disclaimer

Informational only. Review by qualified professional required before filing.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ms-sales-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
