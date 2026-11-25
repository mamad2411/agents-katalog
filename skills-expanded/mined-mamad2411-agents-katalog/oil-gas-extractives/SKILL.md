---
name: oil-gas-extractives
description: "> Use this skill whenever a producer, refiner, miner, oilfield services company, midstream operator, or LNG developer asks about sector-specific tax and accounting. Trigger on phrases like \"petroleum revenue tax\", \"PRT\", \"ring-fence corporation tax\", \"RFCT\", \"supplementary charge\", \"energy profits levy\", \"EPL\", \"OBPS\", \"carbon levy\", \"EU Solidarity Contribution\", \"windfall tax energy\", \"Norwegian special tax\", \"petroleum tax\", \"production sharing contract\", \"PSC\", \"concession\", \"royalty\", \"ad valorem royalty\", \"severance tax\", \"depletion allowance\", \"intangible drilling costs\", \"IDC\", \"successful efforts vs full cost\", \"decommissioning ARO\", \"EITI\", \"extractive industries transparency initiative\", \"country-by-country resource payments\", \"mining royalty\", or any question on extractives. Maps petroleum and mining fiscal regimes for 25+ jurisdictions plus the windfall taxes introduced 2022-2025."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GLOBAL
  category: vertical
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/oil-gas-extractives"
  obligation: VERT
---

# Oil, Gas, and Extractives Sector Tax v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

A sector overlay for oil & gas, mining, and other extractives companies.

---

## Section 1 — Fiscal regimes overview

**[T1] Three main regime models:**

| Regime | Mechanism | Examples |
|---|---|---|
| **Concession / Royalty + Tax** | Operator pays royalty + standard CIT (often ring-fenced) | UK (Brent, North Sea), Norway, US (federal + state royalty + CIT), Canada, Australia |
| **Production Sharing Contract (PSC)** | Operator recovers costs from "cost oil/gas"; "profit oil/gas" split with government per scale | Indonesia, Nigeria, Angola, Egypt, Algeria, Brazil pre-salt, Kazakhstan |
| **Service / Risk Service** | Operator paid fee per unit produced; government retains ownership | Mexico (pre-2014 reform), Iran (buyback), Iraq (technical services contract) |

---

## Section 2 — UK North Sea fiscal regime

### 2.1 The ring-fence

**[T1]** UK upstream petroleum activities are "ring-fenced" — losses and profits from non-ring-fence trades cannot offset ring-fence profits.

### 2.2 Three taxes

**[T1]**
- **Ring-Fence Corporation Tax (RFCT)** — 30% (Finance Act 2002)
- **Supplementary Charge (SC)** — 10% additional tax (reduced from 32% in 2016, reinstated to 10% in 2024)
- **Energy Profits Levy (EPL)** — 35% (Energy Profits Levy Act 2022; rate increased to 38% from 1 November 2024 under Finance Act 2025 amendments; sunset extended to March 2030)
- **Total effective rate**: 30% + 10% + 38% = **78%** (post-November 2024)
- **Petroleum Revenue Tax (PRT)** — frozen at 0% from 2016 for new fields

### 2.3 Allowances

- Capital allowances (100% first-year on most plant and machinery in ring-fence)
- Loss carryforward / carryback intricate
- EPL investment allowance (44% — reduced from 80%) for qualifying ring-fence investment expenditure

---

## Section 3 — Norwegian Special Tax

**[T1]**
- **Standard CIT**: 22%
- **Special petroleum tax (SPT)**: 56% (effective rate)
- Combined marginal rate: 78%
- Recently introduced cash-flow basis for tax reform: full first-year deduction of qualifying upstream investment (reformed 2022); SPT calculated on operating cash flow less qualified investment expense

---

## Section 4 — EU Solidarity Contribution

**[T1] Council Regulation (EU) 2022/1854** (October 2022):
- Temporary solidarity contribution on fossil fuel sector "surplus profits"
- 33% surcharge on profits above 120% of 4-year average
- Member States implemented as temporary windfall taxes for 2022 and 2023
- Most Member States extended through 2024-2025; UK has its own EPL outside EU framework

---

## Section 5 — US oil and gas

**[T1]**
- **Federal CIT**: 21%
- **State CIT**: variable
- **Severance taxes**: state-level on extracted product (Texas oil severance 4.6%; Oklahoma 7%; ND 6.5%; WV 5%; etc.)
- **Royalty**: federal lease 18.75% offshore / 12.5% onshore (raised from 12.5% to 16.67% in 2022 reform); state and private lease rates negotiated
- **IDC (Intangible Drilling Costs)** — election to expense currently (§263(c))
- **Depletion allowance** — percentage depletion for small producers (§613A) or cost depletion (§612)
- **Successful Efforts vs Full Cost** — financial accounting method choice (ASC 932)

---

## Section 6 — Mining sector

### 6.1 Major mining jurisdictions

| Country | Royalty | CIT | Notable |
|---|---|---|---|
| **Australia** | Mineral Resources Rent Tax (MRRT) repealed 2014; state royalties (NSW, QLD, WA variable 2-10%) | 30% CIT; full expensing of capital | Major iron ore, coal, gold |
| **Canada** | Provincial royalty + CIT 26.5% combined | Federal 15% + provincial | Major potash, oil sands |
| **Chile** | Mining royalty (2024 reform: ad-valorem + margin-based 1-2% + 10-32% on profits above thresholds) | 25% CIT | World's largest copper |
| **Peru** | Mining royalty 1-12% by margin; Special Mining Tax 2-8.4% on operating margin; CIT 29.5% | 29.5% | Major copper, gold, zinc |
| **South Africa** | Mining royalty 0.5-7% by refined vs unrefined | 27% CIT (post-2024) | Major platinum, gold |
| **Indonesia** | Royalty 3-6% by mineral; PSC for oil/gas | 22% CIT | Major coal, nickel |

### 6.2 EITI (Extractive Industries Transparency Initiative)

**[T1]** 50+ implementing countries publish reconciled extractive payments and receipts. EU Accounting and Transparency Directives require listed extractive companies to publish payments to governments (Country-by-Country Reporting equivalent).

---

## Section 7 — Accounting issues

### 7.1 Successful Efforts vs Full Cost

**[T1] Successful Efforts** — only successful exploration costs capitalised; dry holes expensed.
**Full Cost** — all exploration and development costs capitalised in "cost pool" by country.

US GAAP ASC 932 permits both. IFRS 6 (Exploration and Evaluation Assets) allows choice for E&E phase but development phase aligned to IAS 16 / IAS 38.

### 7.2 Asset Retirement Obligation (ARO) / Decommissioning

**[T1]** IAS 37 / ASC 410: provision for future decommissioning recognised at discounted PV of cost when constructive obligation arises (typically at first production).
- Provision debited as asset addition; depleted with the reserve
- Tax deduction generally only when actually incurred (jurisdiction-specific)
- Material deferred tax timing difference

### 7.3 Reserves estimation (PRMS)

**[T1]** Petroleum Resources Management System: 1P (proved), 2P (proved + probable), 3P (proved + probable + possible). Recoverable reserves drive depletion accounting.

---

## Section 8 — Pillar Two interaction

**[T1]** Extractives jurisdictions with low CIT but high royalty/severance face Pillar Two complexity:
- Royalty is typically treated as "Covered Tax" if levied on income (some jurisdictions classify as production tax, ambiguous)
- Severance taxes mostly NOT Covered Taxes
- Carve-out for "International Shipping Income" exists; no equivalent for extractives
- Substance-Based Income Exclusion (SBIE) particularly material for capital-intensive extractives

---

## Section 9 — Self-checks

- [ ] Fiscal regime classified (concession / PSC / service)
- [ ] Ring-fence applied where required (UK)
- [ ] EPL / SC rate current
- [ ] Royalty treatment (revenue vs Covered Tax) confirmed
- [ ] Successful Efforts vs Full Cost election documented
- [ ] ARO / decommissioning provision recognised
- [ ] Depletion / depreciation per tax basis
- [ ] EITI / CbC reporting submitted where applicable
- [ ] Pillar Two analysis for in-scope groups
- [ ] Output flags every [T2]/[T3] item for reviewer judgement

---

## Section 10 — Disclaimer

Extractives taxation is highly specialised. Outputs must be reviewed by credentialed extractives sector practitioners. The most up-to-date version is at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/oil-gas-extractives) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
