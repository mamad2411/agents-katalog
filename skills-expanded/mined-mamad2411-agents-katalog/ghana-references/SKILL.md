---
name: ghana-references
description: Primary source references and related open-source projects for this jurisdiction.
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GH
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ghana-references"
  obligation: OTHER
---

# Ghana — Related Open-Source Projects

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

OpenAccountants is AGPL-3.0. Projects below are used as reference for tax rate data.

## taxcalculatorgh

- Repository: [Kessir/taxcalculatorgh](https://github.com/Kessir/taxcalculatorgh)
- License: verify before code reuse (no explicit license file)
- Stars: 32
- Language: JavaScript (Vue.js)
- Scope: Most popular Ghana income tax calculator on GitHub. Implements GRA PAYE (Pay As You Earn) monthly tax brackets with historical rate tables from 2021 through 2024. Includes SSNIT (Social Security) contribution calculation at 5.5%.
- Why it matters: Actively maintained with bracket updates tracking GRA announcements. 32 stars indicates real usage among Ghanaian developers and taxpayers.
- Integration approach: Monthly PAYE bracket tables and SSNIT rate used as reference for the income tax skill. Rate data (public domain tax law) incorporated with attribution.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ghana-references) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
