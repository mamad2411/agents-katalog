---
name: banking-sector
description: "> Use this skill whenever a bank, neobank, payment institution, e-money institution, or regulated financial holding company asks about accounting, regulatory capital, or tax issues specific to financial institutions. Trigger on phrases like \"bank tax\", \"bank levy\", \"IRB approach\", \"standardised approach\", \"IFRS 9 ECL\", \"FRTB\", \"Basel III\", \"Basel IV\", \"CRR/CRD\", \"Prudential regulation\", \"PRA\", \"ECB SSM\", \"FED CCAR\", \"OSFI\", \"expected credit loss\", \"ICAAP\", \"ILAAP\", \"stress testing\", \"interchange fee\", \"MREL\", \"TLAC\", \"resolution planning\", \"deposit guarantee scheme contribution\", or any question about bank accounting / tax / regulation. Covers IFRS 9 ECL, capital adequacy interactions with tax (DTA recognition), bank levies (UK, EU), specific tax rules for banks (FTT, securitisation, hedge accounting). Does NOT cover: detailed banking regulation (CRR/CRD specifics, FRTB calibration); audit of banks (see statutory-audit-workflow-base); routine corporate tax (see corporate-income-tax-workflow-base)."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GLOBAL
  category: vertical
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/banking-sector"
  obligation: VERT
---

# Banking Sector Tax & Accounting v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

A sector overlay for banks, neobanks, payment institutions, e-money institutions, and regulated financial holding companies. Loads alongside the country corporate income tax skill and addresses bank-specific items.

---

## Section 1 — Scope

This skill covers:

- **IFRS 9 / ASC 326 ECL** computation and tax interaction
- **Bank levies** (UK Bank Levy, EU Single Resolution Fund / DGS contributions, IRPS Italy, German bank levy, France contribution sur les établissements de crédit)
- **Capital adequacy interaction with tax** — DTA recognition under Basel III; phased prudential filters
- **Sector tax-specific items**:
  - Interest income / expense recognition (effective interest rate method)
  - Loan origination fees deferral
  - Securitisation tax treatment (SPV consolidation, look-through)
  - Treasury / hedge accounting and tax
  - Interchange and merchant services revenue
  - Trading book vs banking book classification
- **Country-specific bank taxes**:
  - UK Bank Levy (Finance Act 2011 Sch 19) — 0.10% of taxable bank balance sheet equity and liabilities
  - UK Bank Corporation Tax Surcharge — 3% additional CT on bank profits above GBP 100m (reduced to 3% from 8% in April 2023)
  - US BEAT (Base Erosion and Anti-Abuse Tax) — banks subject to BEAT at lower revenue thresholds
  - US §163(j) interest deduction limitation overlays
  - Italian IRES + IRAP banking sector rules

This skill does NOT cover:

- **Detailed Basel III/IV calibration** beyond high-level connections
- **Day-to-day VAT on financial services** (see country VAT skills with banking carve-outs)
- **MiFID / consumer protection compliance**
- **Anti-money-laundering operational compliance**
- **CRD/CRR/PRA specific reporting**

---

## Section 2 — Key sector accounting differences (IFRS 9 vs ASC 326)

**[T1] See `ifrs-local-gaap-reconciliation.md` for the underlying difference catalogue.**

For banking specifically:

| Item | IFRS 9 | ASC 326 (CECL) |
|---|---|---|
| Loss model | 3-stage Expected Credit Loss | Current Expected Credit Loss — lifetime ECL from inception |
| Day-1 allowance | 12-month ECL only | Lifetime ECL (typically higher) |
| Significant increase in credit risk (SICR) | Threshold (typically 30-day past due rebuttable presumption + qualitative) | n/a in CECL but used for monitoring |
| Originated credit-impaired (POCI) | Effective interest rate based on lifetime expected cash flows; subsequent ECL changes through P&L | ASU 2022-02 conformed POCI treatment |
| Off-balance-sheet (loan commitments, financial guarantees) | Stage-based ECL | CECL |

---

## Section 3 — Tax treatment of loan loss provisions

**[T1] By jurisdiction (sample):**

| Country | Treatment |
|---|---|
| **US** | Loan loss reserve deductible only for small banks (assets ≤ USD 500m) under §585; non-thrift banks use specific charge-off method (§166). ASC 326 CECL accounting does not flow through 1:1 to tax. |
| **UK** | General provisions not deductible; specific provisions deductible if linked to identifiable loss event and meets HMRC commercial test. IFRS 9 Stage 3 generally deductible; Stages 1/2 generally not |
| **Germany** | Allgemeine Risikovorsorge limited; spezifische Wertberichtigungen deductible when "objectively required" — pre-tax overlay |
| **France** | Provisions pour dépréciation generally deductible if probable and quantifiable |
| **Italy** | Banking sector loan loss provisions deductible on schedule (18% of book in year 1 historically; now reformed to align IRES treatment) |
| **Australia** | Specific loss provisions deductible; general not |
| **Canada** | Specific allowance deductible; general allowance non-deductible |
| **India** | Specific provisions allowed only to extent prescribed by RBI; bad-debt write-offs deductible |

**[T1]** Material book-tax difference creates substantial deferred tax assets (DTAs) for banks. Recoverability assessment under IAS 12 / ASC 740 critical — Pillar Two interacts as DTAs may recapture under the 5-year rule.

---

## Section 4 — Bank levies and surcharges

### 4.1 UK Bank Levy + Bank Surcharge

**[T1] UK Bank Levy** (Finance Act 2011 Schedule 19):
- Rate: **0.10%** of taxable balance sheet equity and liabilities (reduced to 0.10% from 0.21% in stages, FA 2017)
- Half rate (0.05%) on long-term funding
- De minimis: GBP 20bn balance sheet
- Filing: HMRC bank levy return, due 9 months 1 day after period end

**[T1] UK Bank Corporation Tax Surcharge** (FA 2015 s.17 amended FA 2022):
- Rate: **3%** on bank profits above GBP 100m (reduced from 8% effective 1 April 2023)
- Applies in addition to standard 25% CT
- Effective rate on banking profits above threshold: 28%

### 4.2 EU Single Resolution Fund (SRF) contribution

**[T1]** Ex-ante annual contributions under Regulation (EU) 806/2014 to fund bank resolution; calculated by the Single Resolution Board based on liabilities. Target level: 1% of covered deposits at SRF maturity (2024). Distinct from country deposit guarantee scheme (DGS) contributions.

### 4.3 EU Member State bank levies

| Country | Rate | Base |
|---|---|---|
| **Germany** | EUR 410-1.6bn annually distributed across banks | Risk-weighted liabilities — Bankenabgabe |
| **France** | Contribution sur les établissements de crédit reformed; merged into SRF + national supplement | Risk-weighted exposures |
| **Italy** | Imposta straordinaria 2023 (40% on certain net interest gains) — converted to optional reserve contribution following ECB pushback | Net interest income excess |
| **Spain** | 4.8% on net interest + commissions (extraordinary 2023-2025; targeted "windfall" tax) | Spanish-source banking gross income > EUR 800m threshold |
| **Hungary** | Bank levy — 0.15% / 0.20% balance sheet thresholds | Liabilities |
| **Sweden** | Bank tax — 6% on liabilities; reduced 2024 | Total liabilities |
| **Belgium** | Bank levy on liabilities | Liabilities |
| **Netherlands** | Bankenbelasting — 0.044% short-term / 0.022% long-term liabilities | Liabilities |
| **Poland** | Bank levy 0.0366% per month (0.44% annually) | Excess assets above PLN 4bn threshold |

### 4.4 Deposit Guarantee Scheme (DGS) contributions

**[T1]** EU Directive 2014/49/EU. Country DGS funds ex-ante and ex-post contributions from member banks.

---

## Section 5 — DTAs and Pillar Two interaction

**[T1]** Banks typically hold material DTAs from:
- IFRS 9 ECL (book in advance of tax)
- Pension obligations (book provisions in advance of tax)
- Deferred compensation
- Operating loss carryforwards
- Securitisation losses

**[T1] Basel III prudential filter** under Article 36(1)(c) CRR:
- DTAs that rely on future profitability must be deducted from CET1 above a 10% threshold (combined with other deductions)
- DTAs from temporary differences taxed at deferred 15%+ generally less restrictive

**[T2] Pillar Two interaction:**
- DTAs / DTLs revalued to lower of statutory rate or 15% (per `pillar-two-globe-minimum-tax.md`)
- 5-year DTL recapture rule may add back loan loss DTL recoveries
- ETR may fall below 15% for banks with material loss carryforwards in low-rate jurisdictions

---

## Section 6 — Sector-specific issues

### 6.1 Trading book vs banking book

**[T1]** Trading book positions:
- IFRS 9: typically FVPL (held for trading)
- Tax: most jurisdictions tax mark-to-market gains on banking trading books (UK FA 2002 Sch 26; US §475 mark-to-market election for dealers)

Banking book positions:
- IFRS 9: amortised cost or FVOCI
- Tax: realised basis typically

### 6.2 Hedge accounting and tax

**[T1]** IFRS 9 / ASC 815 hedge accounting reduces P&L volatility but creates timing differences for tax:
- Cash flow hedges: deferred in OCI, recycled to P&L on hedged item recognition — tax follows P&L timing
- Fair value hedges: P&L immediate offset — tax generally follows

### 6.3 Securitisation

**[T1]** Tax treatment depends on consolidation and risk transfer:
- True sale + non-consolidated SPV: gain/loss on sale, no further bank tax on SPV income
- Synthetic / retained risk: continued bank tax on underlying loans
- IFRS 10 / ASC 810 may differ from regulatory consolidation
- §163(j) US interest deduction limitation interactions

### 6.4 Interchange and merchant services

Card interchange revenue is service revenue subject to standard CIT. Merchant discount rate (MDR) flows to processor / bank. Specific country VAT exemptions for "financial services" generally cover interchange.

### 6.5 Credit valuation adjustment (CVA)

Tax treatment varies — some jurisdictions allow deduction of CVA P&L volatility; others require add-back of fair value losses on counterparty risk.

---

## Section 7 — Self-checks

- [ ] IFRS 9 ECL computation reconciled to tax deductible provisions per jurisdiction rules
- [ ] Bank levy / surcharge applied if jurisdictional thresholds met
- [ ] DTA recoverability assessed under IAS 12 / ASC 740 with bank-specific income forecasts
- [ ] Basel III prudential filter deduction modelled for CET1
- [ ] Pillar Two ETR analysis includes loan loss DTA temporary differences
- [ ] Trading book vs banking book classification confirmed for tax marks
- [ ] Hedge accounting timing differences identified
- [ ] Securitisation true-sale vs retained-risk position confirmed for tax
- [ ] DGS / SRF contributions deductibility per jurisdiction
- [ ] Output flags every [T2]/[T3] item for reviewer judgement

---

## Section 8 — Disclaimer

This skill produces working papers for review by credentialed banking-sector practitioners. Bank accounting, regulation, and tax are highly specialised. Every output must be reviewed and signed off by a credentialed practitioner (typically Big 4 banking sector specialist, in-house Head of Tax, or audit partner) before any filing or capital reporting.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/banking-sector) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
