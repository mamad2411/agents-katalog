---
name: investment-funds-reits
description: "> Use this skill whenever a regulated investment fund, hedge fund, private equity fund, real estate investment trust (REIT), UCITS, AIF, mutual fund, or fund manager asks about sector-specific tax. Trigger on phrases like \"UCITS tax\", \"AIFMD\", \"RAIF\", \"SIF\", \"SICAR\", \"FCP\", \"FCPR\", \"SLP\", \"ELTIF\", \"PE fund\", \"carried interest tax\", \"carry\", \"promote\", \"GP / LP allocation\", \"K-1\", \"PFIC\", \"QEF election\", \"CFC for funds\", \"REIT\", \"Section 856-860\", \"PID\", \"UK REIT\", \"SOCIMI\", \"S-REIT Singapore\", \"J-REIT Japan\", \"Master fund / feeder fund\", \"Investment Tax Act Germany\", \"tax-transparent fund\", \"blockers\", or any question on fund / REIT-specific tax. Covers UCITS / AIF tax interaction, fund-level vs investor-level taxation, REIT regimes globally (US, UK, France, Germany, Netherlands, Spain SOCIMI, Australia AREIT, Singapore S-REIT, Japan J-REIT), carried interest tax (US, UK, France, Italy), and PFIC vs QEF mechanics for US-taxable investors."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GLOBAL
  category: vertical
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/investment-funds-reits"
  obligation: VERT
---

# Investment Funds & REITs Tax v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

A sector overlay for investment funds and REITs covering fund-level, GP-level, and investor-level taxation.

---

## Section 1 — Fund taxation principles

**[T1] Two foundational models:**

| Model | Fund-level tax | Investor-level tax |
|---|---|---|
| **Tax-transparent** | None (the fund "looks through" to investors) | Investor taxed on its share of fund income as if directly held |
| **Tax-opaque (blocker)** | Fund pays CIT (usually with offset for distributions) | Investor taxed only on distributions / dispositions |

**[T1] Special "fiscally transparent for tax / opaque for legal" structures:**
- US LP / LLC
- UK Partnership
- Cayman Exempted LP
- Luxembourg RAIF as SIF / SCSp (partnership)
- Irish ILP (Investment Limited Partnership)

---

## Section 2 — UCITS and AIF (EU)

### 2.1 UCITS

**[T1]** UCITS funds (Undertaking for the Collective Investment in Transferable Securities) under Directive 2009/65/EC are usually structured as:
- **Investment company with variable capital** (SICAV in Luxembourg, ICAV in Ireland)
- **Common contractual fund** (FCP in Luxembourg / France)
- **Unit trust** (UK)

**[T1] Fund-level tax:**
- **Luxembourg**: subscription tax (taxe d'abonnement) — 0.05% / 0.01% (annual on NAV); no CIT on UCITS profits
- **Ireland**: ICAV / UCITS exempt CIT under TCA s.739D — Investment Undertaking Tax (IUT) only on Irish resident investors
- **France**: FCP transparent; SICAV with specific regime
- **UK**: Authorised funds with specific UK fund tax regime

### 2.2 AIF (Alternative Investment Fund)

**[T1]** AIFs under AIFMD (Directive 2011/61/EU) have wider product range:
- Hedge funds
- Private equity funds
- Real estate funds
- Infrastructure funds
- Hybrid funds

Tax treatment depends on legal form and jurisdiction; typically tax-transparent or low-tax-blocker.

### 2.3 Specific Luxembourg vehicles

| Vehicle | Tax |
|---|---|
| **SIF (Specialised Investment Fund)** | Subscription tax 0.01% NAV; no CIT (Lux Law 13 February 2007) |
| **RAIF (Reserved Alternative Investment Fund)** | Choice of SIF-style or SICAR-style; flexible (Law 23 July 2016) |
| **SICAR (Société d'Investissement en Capital à Risque)** | Subscription tax-exempt; CIT but with extensive participation exemption; capital risk |
| **SCSp (Special Limited Partnership)** | Tax-transparent (partnership) (Law 12 July 2013) |

---

## Section 3 — Carried interest tax

**[T1] By jurisdiction:**

| Country | Treatment | Effective rate |
|---|---|---|
| **United States** | §1061 ITA: carried interest classified as long-term capital gain only if 3-year holding period (raised from 1 year by TCJA 2017); otherwise short-term ordinary | ~20% LTCG vs 37% short-term/ordinary |
| **United Kingdom** | Carried Interest from April 2025: 32% effective rate (reformed from CGT-only treatment); Disguised Investment Management Fees (DIMF) since 2015 | 32% (proposed from April 2025; consultation ongoing) |
| **France** | Carried interest treated as employment income (and capital gain on disposal) for managers; specific holding period requirement | Effective marginal rate close to top income tax |
| **Italy** | Carried interest classified as investment income if specific conditions met (commitment / employment) | 26% capital gain rate possible |
| **Germany** | 60% of carried interest treated as employment income (Halbeinkünfteverfahren) — favourable | Reduced rate |
| **Spain** | New 2025 rules characterise carried interest as employment income absent specific conditions | Up to ~50% |

---

## Section 4 — PFIC mechanics (US investors)

**[T1] §1297 ITA — Passive Foreign Investment Company:**

A foreign corporation is a PFIC if:
- ≥75% of gross income is passive (income test), OR
- ≥50% of average assets produce passive income (asset test)

**[T1] Tax consequences without election:**
- Excess distributions and dispositions taxed at maximum ordinary rate for prior years held
- Interest charge for deemed deferral

**[T1] QEF (Qualified Electing Fund) election:**
- US investor includes pro-rata share of fund's ordinary earnings and net capital gain annually
- Annual PFIC Annual Information Statement required from fund
- Avoids excess distribution / interest charge regime

**[T1] MTM (Mark-to-Market) election:**
- Annual gain/loss recognised on PFIC shares treated as ordinary income
- Available for "marketable" PFIC shares

**[T1] PFIC exception — Active insurance corporation** under §1297(f) — see `insurance-sector.md`.

---

## Section 5 — REIT regimes

### 5.1 US REIT (§§856-860 ITA)

**[T1] Requirements:**
- 75% gross income from real estate (rents, mortgages, gains on real estate)
- 95% gross income passive (75% real estate + interest, dividends, gains)
- 75% asset test (real estate, mortgages, cash, government securities)
- Distribute at least 90% of taxable income to shareholders
- ≥ 100 shareholders; not closely held (5-or-fewer test)
- Operated as REIT election (§856)

**[T1] Tax effect:**
- Distribution deduction at REIT level — effectively no CIT on distributed income
- Shareholders taxed on dividends at ordinary rate (except qualified REIT dividends get 20% §199A deduction post-TCJA — now confirmed permanent in OBBBA)

### 5.2 UK REIT

**[T1] FA 2006 (now CTA 2010 Part 12):**
- 75% gross income from rental of UK property
- 75% asset value in property rental business
- Listed on recognised stock exchange (or with 35% rule for institutional ownership)
- 90% distribution requirement
- 75% non-resident-investor cap during 3 years from entry
- Property Income Distributions (PID) — gross-paid; income tax at 20% basic; 40% higher; 45% additional

### 5.3 French SIIC / OPCI

**[T1]**
- SIIC: listed real estate companies, 85% rental income distribution, 50% gain distribution; CIT exemption on rental and capital gains
- OPCI: non-listed open-ended collective investment in real estate

### 5.4 German G-REIT

**[T1]** Less popular than other markets; ~5 G-REITs listed.

### 5.5 Spanish SOCIMI

**[T1]** Sociedad Anónima Cotizada de Inversión en el Mercado Inmobiliario:
- Listed on recognised market
- 80% asset and gross income in real estate
- 80% distribution of rental income; 100% distribution of REIT-source distributions; 50% of capital gains over 3 years
- 0% CIT but 19% specific levy on dividend distributions

### 5.6 Singapore S-REIT

**[T1]**
- Tax-transparent for distributions to qualifying unitholders (no S-REIT corporate tax)
- 90% distribution requirement
- Listed on SGX
- Cross-border property investment common

### 5.7 Japanese J-REIT

**[T1]**
- Investment corporations under Investment Trust Act
- 90% distribution requirement
- Reduced or zero CIT on distributed income

### 5.8 Australian A-REIT

**[T1]**
- Listed stapled trust + corporation structures common
- Mostly tax-transparent at trust level
- AMIT (Attribution Managed Investment Trust) regime since 2016

---

## Section 6 — Blocker structures

**[T1]** "Blocker" entities interpose tax-opaque vehicles to:
- Convert ordinary income to capital gains for US investors
- Block US ECI for foreign LP investors
- Prevent CFC consequences for US shareholders
- Avoid PFIC exposure for US-taxable investors

Common structures:
- US-blocker (C-corp) below partnership / LLC
- Cayman or BVI blocker above offshore investments
- Luxembourg SICAV/SCSp for EU fund families
- Multi-tier structures with hybrid mismatches (now constrained by ATAD II)

---

## Section 7 — Self-checks

- [ ] Fund legal form classified for tax (transparent vs opaque)
- [ ] UCITS / AIF status verified for regulatory regime
- [ ] Local fund-level tax computed (subscription tax / IUT / CIT)
- [ ] Investor-level tax mechanics documented per investor country
- [ ] PFIC test applied for US-taxable investors with appropriate election
- [ ] Carried interest classification per jurisdiction
- [ ] REIT distribution requirements met (75/95/90/etc.)
- [ ] Property Income Distribution (UK PID) gross-up treatment correct
- [ ] Blocker structures support business purpose
- [ ] Pillar Two GloBE Income excludes "Investment Entity" income per Article 7
- [ ] Output flags every [T2]/[T3] item for reviewer judgement

---

## Section 8 — Disclaimer

Fund and REIT taxation is highly specialised and varies dramatically by structure. Outputs must be reviewed by credentialed fund-sector practitioners. The most up-to-date version is at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/investment-funds-reits) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
