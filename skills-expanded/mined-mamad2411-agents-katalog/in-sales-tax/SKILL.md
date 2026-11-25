---
name: in-sales-tax
description: "Use this skill whenever asked about Indiana sales and use tax. Trigger on phrases like \"Indiana sales tax\", \"IN sales tax\", \"IC 6-2.5\", \"Indiana DOR\". Indiana has one of the SIMPLEST structures -- 7% flat with no local sales taxes. ALWAYS load us-sales-tax first."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-IN
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/in-sales-tax"
  obligation: CT
---

# Indiana Sales and Use Tax Skill v2.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Section 1 -- Quick reference

| Field | Value |
|---|---|
| Jurisdiction | Indiana |
| State rate | 7.00% (flat -- no local sales tax) |
| Local taxes | None |
| Maximum combined rate | 7.00% |
| Sourcing | Destination-based (SST) |
| Economic nexus | $100,000 OR 200 transactions |
| Tax authority | Indiana Department of Revenue |
| Portal | https://intime.dor.in.gov |
| SST member | Yes (full member) |
| Skill version | 2.0 |

**One of the simplest sales tax states -- 7% flat rate statewide, no local add-ons.**

## Section 3 -- Transaction pattern library

| Pattern | Taxable? | Notes |
|---|---|---|
| General TPP | TAXABLE 7% | Uniform statewide |
| Clothing | TAXABLE | No exemption |
| Grocery food | EXEMPT | |
| Prepared food | TAXABLE | |
| SaaS | NOT TAXABLE | Indiana does not tax SaaS |
| Canned software (download) | TAXABLE | |
| Professional services | NOT TAXABLE | |
| Manufacturing equipment | EXEMPT | IC 6-2.5-5-3 |
| Prescription drugs | EXEMPT | |
| OTC drugs | EXEMPT | |
| Resale | EXEMPT | |

## Section 10 -- Prohibitions

- NEVER add local tax -- Indiana has no local sales taxes.
- NEVER treat SaaS as taxable in Indiana.
- NEVER compute any number.

## Disclaimer

Informational only. Review by qualified professional required before filing.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/in-sales-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
