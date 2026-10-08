---
name: ru-freelance-intake
description: "ALWAYS USE THIS SKILL when a user asks for help with their Russian taxes AND mentions freelancing, self-employment, самозанятый, ИП, or being an individual entrepreneur in Russia. Trigger on phrases like \"help me with my Russian taxes\", \"I'm самозанятый\", \"I'm an ИП\", \"налог на профессиональный доход\", \"НПД\", \"УСН\", \"ОСНО\", \"I freelance in Russia\", \"do my Russian self-employed return\", \"сколько налогов я плачу\", or any similar phrasing where the user is a Russia-resident self-employed individual needing tax help. This is the REQUIRED entry point for the Russia self-employed workflow; downstream skills (ru-self-employed-npd, ru-usn, ru-income-tax, ru-social-contributions, russia-vat, ru-return-assembly) depend on it running first to produce a structured intake package. Russia-resident self-employed only."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: RU
  category: orchestrator
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ru-freelance-intake"
  tax_year: 2026
  obligation: ORCH
---

# Russia Self-Employed Intake Skill v0.1 (ru-freelance-intake)

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

The intake orchestrator for a Russia-resident self-employed person (самозанятый, ИП). Every downstream Russia content skill — `ru-self-employed-npd`, `ru-usn`, `ru-income-tax`, `ru-social-contributions`, `russia-vat` — and the assembly orchestrator `ru-return-assembly` depend on this skill running first to produce a structured intake package.

This skill **computes nothing**. Its only job is to establish the facts, parse the uploaded documents, confirm them once, and route to the correct regime. Russia's self-employed landscape has three main tax paths and the routing decision drives everything downstream, so getting the routing right is the whole point of this file.

Reply to the user in their own language. If they write in Russian, answer in Russian; if in English, answer in English. Embed the native Russian terms (самозанятый, ИП, ООО, УСН, ОСНО, НПД, НДС, НДФЛ, страховые взносы) so the user recognises exactly which regime and form is meant.

---

## Design principles (upload-first)

Upload-first, inference-then-confirm:
1. **Compact refusal/routing sweep** — a few interactive questions, ~30 seconds, to establish form of business, regime, residency, the НПД cap, and VAT exposure.
2. **Upload-first** — the user dumps everything they have (the «Мой налог» / «Налоги ФЛ» export, bank statements, registration extract, prior declarations).
3. **Inference pass** — parse every document, extract as much as possible before asking anything.
4. **Gap-filling only** — ask only about what is genuinely missing or ambiguous after the inference pass.
5. **Single confirmation pass** — show the full picture once, then hand off downstream.

Do not narrate phases ("now I am inferring…"). Do not re-ask anything already visible in the uploaded documents. Apply conservative defaults when an answer is missing and flag the assumption for the reviewer rather than blocking.

---

## Step 1 — Refusal / routing sweep (route to the right regime)

Establish, fast and in this order:

1. **Самозанятый, ИП, or ООО?**
   - **Самозанятый (физлицо на НПД)** or **ИП** → continue in this workflow.
   - **ООО (a legal entity)** → **out of scope. Escalate** to a qualified Russian accountant. This workflow covers individuals only, not corporate profit tax (налог на прибыль).

2. **Which tax regime are you on?** This is the central routing question:
   - **НПД (налог на профессиональный доход)** — the simplest path. 4% on income from physical persons, 6% on income from companies and ИП. No страховые взносы required, no declaration, tax is calculated automatically inside «Мой налог». Available to physical persons and to ИП without employees. → routes to `ru-self-employed-npd`.
   - **УСН (упрощённая система)** — for ИП. Two objects: **«доходы»** (6%) or **«доходы минус расходы»** (15%); regional reduced rates may apply. → routes to `ru-usn`.
   - **ОСНО (общая система)** — НДФЛ (13%/15% progressive) plus НДС. Default for an ИП who never elected a special regime, or who exceeded a special-regime limit. → routes to `ru-income-tax`.
   - If the user does not know their regime, infer it from the documents (a «Мой налог» export ⇒ НПД; a УСН declaration / object on the ЕГРИП extract ⇒ УСН; otherwise treat as ОСНО pending confirmation).

3. **Russian tax resident for the year (183+ days in Russia in the 12-month period)?**
   - Non-residents have materially different НДФЛ treatment and cannot use some regimes the same way → flag prominently and **escalate** if non-resident; do not silently assume residency.

4. **Does annual income exceed the НПД cap of 2,400,000 ₽?**
   - The НПД limit remains **2,400,000 ₽ per calendar year** for 2026 (the experiment runs to 2028 and the cap is not being changed). There is no monthly cap, only the annual one.
   - If a самозанятый exceeds 2.4M ₽ mid-year, НПД status is lost for the rest of the year and income must move to another regime (УСН if previously elected, otherwise ОСНО). Flag this and route the post-cap income accordingly.

5. **VAT (НДС) exposure?**
   - Самозанятые on НПД do **not** charge НДС.
   - **Important 2026 change:** ИП on УСН are no longer automatically НДС-exempt. From 2026 the УСН revenue threshold for НДС exemption dropped to **20,000,000 ₽** (was 60M in 2025; scheduled to fall further to 15M in 2027 and 10M in 2028). If 2025 income exceeded 20M ₽, an НДС obligation arises from 1 January 2026; if the threshold is crossed during 2026, НДС applies from the 1st of the month following the breach. → engage `russia-vat`.
   - ИП on ОСНО charge НДС by default (subject to any Art. 145 exemption).

Conservative defaults if unanswered: самозанятый/НПД where a «Мой налог» export exists; otherwise ИП on УСН «доходы»; Russian resident; income under the 2.4M cap; no НДС. Always flag each default for the reviewer.

---

## Step 2 — Collect

Ask the user to upload (whatever they have — partial is fine):
- **«Мой налог» / «Налоги ФЛ» export** — the справка о доходах / receipts (чеки) for НПD users; this is the authoritative income record for самозанятые.
- **Bank statements** for all accounts (RUB and any FX) for the full year — to reconcile against declared income and catch unreported receipts.
- **Registration extract (выписка из ЕГРИП)** for an ИП — confirms regime, ОКВЭД activity codes, and employee status.
- **Prior-year declarations** — УСН declaration (КНД 1152017), 3-НДФЛ, НДС returns — and **страховые взносы** payment history (фиксированные взносы and any 1%-over-300k payments).
- Any **patent (ПСН)** documents if the user mentions a patent — note that ПСН is a separate ИП regime; flag for the reviewer and escalate if it materially affects routing.

## Step 3 — Infer & confirm

- Determine **form of business and regime** from the documents if not stated (export ⇒ НПД; ЕГРИП object ⇒ УСН; otherwise ОСНО).
- For НПД: total the чеки and check the running annual total against the **2,400,000 ₽** cap; flag if the user is approaching or has breached it.
- For УСН/ОСНО: separate genuine business income from internal transfers, loan movements, and personal funds in the bank data.
- Convert any **FX receipts to RUB** at the Bank of Russia (ЦБ РФ) rate on the date of receipt.
- Check **НДС exposure** against the 2026 УСН threshold (20M ₽) and ОСНО default.
- Confirm **страховые взносы** status for ИП (the 2026 fixed contribution is roughly 57,390 ₽ plus 1% on income over 300,000 ₽ — for the reviewer to compute, not this skill).
- Present one consolidated summary: form of business, regime, residency, income vs cap, НДС status, contributions status. Get a single confirmation.

## Step 4 — Hand off (the routing map)

Produce a structured intake package and route based on the confirmed regime:

- **Самозанятый / НПД:** `ru-self-employed-npd` (4%/6% НПД). No страховые взносы and no НДС unless the user voluntarily pays pension contributions — note that for the reviewer. → `ru-return-assembly`.
- **ИП on УСН:** `ru-usn` («доходы» 6% or «доходы минус расходы» 15%) **+** `ru-social-contributions` (фиксированные взносы + 1% over 300k) **+** `russia-vat` if 2026 income exceeds the 20M ₽ НДС threshold → `ru-return-assembly`.
- **ИП or individual on ОСНО:** `ru-income-tax` (НДФЛ) **+** `russia-vat` (НДС by default) **+** `ru-social-contributions` for an ИП → `ru-return-assembly`.
- **Cap breach mid-year:** route НПД income up to the breach date to `ru-self-employed-npd`, and post-breach income to `ru-usn` or `ru-income-tax` as applicable; flag prominently.
- **ООО, non-resident, or ПСН-driven complexity:** stop and escalate to a qualified Russian accountant.

Always pass forward: form of business, regime, residency status, annual income figure, НДС determination, страховые взносы status, and every assumption made under a conservative default.

---

## Disclaimer

This skill orchestrates intake only and computes no tax. It establishes facts and routes to downstream skills. All figures, regime determinations, and downstream outputs must be reviewed and signed off by a qualified Russian accountant (бухгалтер / налоговый консультант) before anything is filed with the ФНС. The most up-to-date version is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ru-freelance-intake) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
