---
name: ua-freelance-intake
description: "ALWAYS USE THIS SKILL when a user asks for help preparing their Ukrainian taxes AND mentions freelancing, self-employment, sole proprietorship, ФОП, FOP, or being an individual entrepreneur in Ukraine. Trigger on phrases like \"help me do my Ukrainian taxes\", \"I'm a ФОП\", \"I'm a freelancer in Ukraine\", \"prepare my single-tax return\", \"I'm self-employed in Ukraine\", or any similar phrasing where the user is a Ukraine-resident self-employed individual needing tax help. This is the REQUIRED entry point for the Ukraine self-employed workflow — downstream skills (ua-single-tax, ua-income-tax, ua-social-contributions, ukraine-vat, ua-return-assembly) depend on this skill running first to produce a structured intake package. Upload-first workflow. Ukraine-resident sole proprietors only."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: UA
  category: orchestrator
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ua-freelance-intake"
  tax_year: 2026
  obligation: ORCH
---

# Ukraine Self-Employed Intake Skill v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

The intake orchestrator for Ukraine-resident self-employed individuals (ФОП / FOP). Every downstream Ukraine content skill (ua-single-tax, ua-income-tax, ua-social-contributions, ukraine-vat) and the assembly orchestrator (ua-return-assembly) depend on this skill running first to produce a structured intake package.

This skill computes nothing. Its job is to collect the facts, parse the documents, confirm everything, and hand off a clean intake package.

---

## Design principles

Upload-first, inference-then-confirm:
1. **Compact refusal sweep** — 3–5 interactive questions, ~30 seconds.
2. **Upload-first** — the user dumps everything they have (bank statements, registration extract, prior return).
3. **Inference pass** — parse every document, extract as much as possible.
4. **Gap-filling only** — ask only about what is missing or ambiguous.
5. **Single confirmation pass** — show the full picture, hand off downstream.

Do not narrate phases. Do not re-ask anything visible in the documents.

---

## Step 1 — Refusal sweep (route to the right regime)

Establish, fast:
1. **Are you a ФОП (individual entrepreneur), or a company (ТОВ)?** — ТОВ is out of scope; escalate.
2. **Simplified system (single tax) or general system?** — routes to `ua-single-tax` vs `ua-income-tax`.
3. **If single tax: which group (1, 2, or 3)?** — most freelancers/IT are Group 3.
4. **If Group 3: VAT-registered?** — determines 3% vs 5%.
5. **Ukrainian tax resident for the year?** — non-residents escalate.

Conservative defaults if unanswered: ФОП, simplified, Group 3, non-VAT, resident.

## Step 2 — Collect

Ask the user to upload:
- Bank statements for all accounts (UAH and any FX) for the full year.
- Registration extract (виписка з ЄДР) with КВЕД activity codes.
- Prior-year single-tax declaration and ЄСВ payment history, if any.

## Step 3 — Infer & confirm

- Determine the group and VAT status from the extract if not stated.
- Convert FX receipts to UAH at the NBU rate on the date of receipt.
- Identify income vs internal transfers vs loan movements.
- Flag any barred activity (excisable goods, FX exchange, financial services, gambling, mineral extraction) and any approach to the group income cap.

## Step 4 — Hand off

Produce a structured intake package and route:
- **Simplified:** `ua-single-tax` (single tax + military levy) + `ua-social-contributions` (ЄСВ) + `ukraine-vat` if VAT-registered → `ua-return-assembly`.
- **General system:** `ua-income-tax` (18% PIT + 5% military levy) + `ua-social-contributions` → `ua-return-assembly`.

---

## Disclaimer

This skill orchestrates intake only and computes no tax. All downstream outputs must be reviewed and signed off by a qualified Ukrainian accountant or auditor before filing. The most up-to-date version is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ua-freelance-intake) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
