---
name: mi-sales-tax
description: "Use this skill whenever asked about Michigan sales and use tax. Trigger on phrases like \"Michigan sales tax\", \"MI sales tax\", \"MCL 205.51\", \"Michigan Treasury\". ALWAYS load us-sales-tax first."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-MI
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/mi-sales-tax"
  obligation: CT
---

# Michigan Sales and Use Tax Skill v2.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Section 1 -- Quick reference

| Field | Value |
|---|---|
| Jurisdiction | Michigan |
| State rate | 6.00% (flat -- no local sales tax) |
| Local taxes | None |
| Maximum combined rate | 6.00% |
| Sourcing | Destination-based (SST) |
| Economic nexus | $100,000 OR 200 transactions |
| Tax authority | Michigan Department of Treasury |
| Portal | https://www.michigan.gov/treasury |
| SST member | Yes (full member) |
| Skill version | 2.0 |

## Section 3 -- Transaction pattern library

| Pattern | Taxable? | Notes |
|---|---|---|
| General TPP | TAXABLE 6% | |
| Clothing | TAXABLE | No exemption |
| Grocery food | EXEMPT | |
| Prepared food | TAXABLE | |
| SaaS | NOT TAXABLE | Michigan does not tax SaaS |
| Canned software (download) | TAXABLE | Prewritten software is TPP |
| Professional services | NOT TAXABLE | |
| Manufacturing equipment | EXEMPT | Industrial processing exemption |
| Prescription drugs | EXEMPT | |
| Resale | EXEMPT | |

## Section 10 -- Prohibitions

- NEVER add local tax -- Michigan has no local sales taxes.
- NEVER treat SaaS as taxable in Michigan.
- NEVER compute any number.

## Disclaimer

Informational only. Review by qualified professional required before filing.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/mi-sales-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
