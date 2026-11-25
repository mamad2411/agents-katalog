---
name: indonesia-references
description: Primary source references and related open-source projects for this jurisdiction.
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: ID
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/indonesia-references"
  obligation: OTHER
---

# Indonesia — References

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Open-source repositories

| Repository | License | Stars | What we extracted |
|---|---|---|---|
| [steevenz/id-payroll-calculator](https://github.com/steevenz/id-payroll-calculator) | MIT | 21 | PTKP amounts, BPJS Kesehatan rates (4%/1%), JHT (3.7%/2%), JP (2%/1%), JKK risk-grade table, JKM (0.3%), biaya jabatan (5% cap 500k/month), NPWP surcharge (20%), payroll calculation methods (NETT/GROSS/GROSS-UP) |
| [KejawenLab/PPH21](https://github.com/KejawenLab/PPH21) | MIT | 6 | PPh 21 progressive bracket structure and strategy-pattern calculation logic |

## Official sources

| Source | URL | What we verified |
|---|---|---|
| Direktorat Jenderal Pajak (DJP) | https://www.pajak.go.id | PPh 21 progressive brackets per UU HPP No. 7/2021 |
| PP 58/2023 | https://peraturan.bpk.go.id/Details/266564/pp-no-58-tahun-2023 | TER (Tarif Efektif Rata-rata) categories and rate tables |
| PMK 168/2023 | https://jdih.kemenkeu.go.id | TER implementation rules for monthly withholding |
| BPJS Ketenagakerjaan | https://www.bpjsketenagakerjaan.go.id | JP wage ceiling IDR 10,547,400 (March 2025), JKP program details |
| BPJS Kesehatan | https://www.bpjs-kesehatan.go.id | Health insurance contribution rates and wage cap IDR 12,000,000 |

## Notes

- The `steevenz/id-payroll-calculator` repo uses pre-HPP tax brackets (first bracket 0–50M, no 35% bracket). The skill file uses the current UU HPP brackets (first bracket 0–60M, includes 35% bracket above 5B).
- The JP wage ceiling in the repo code (IDR 7,000,000) is outdated. The skill file uses the 2025 ceiling of IDR 10,547,400.
- TER tables were sourced from PP 58/2023 Annex as published on official DJP and tax portal sites, not from the repos (which predate the TER scheme).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/indonesia-references) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
