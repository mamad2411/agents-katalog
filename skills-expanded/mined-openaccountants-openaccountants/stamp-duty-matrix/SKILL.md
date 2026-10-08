---
name: stamp-duty-matrix
description: "> Use this skill whenever an attorney, transaction lawyer, or in-house counsel asks about stamp duty on documents, securities transfers, or financial transactions. Trigger on phrases like \"stamp duty\", \"stamp tax\", \"SDRT\", \"stamp duty reserve tax\", \"stamp duty on shares\", \"share transfer tax\", \"FTT\", \"financial transaction tax\", \"France FTT\", \"Italy FTT\", \"Spain FTT IFT\", \"Ireland stamp duty shares\", \"Hong Kong stamp duty shares\", \"Singapore ACD additional conveyance duty\", \"stamp duty Australia\", \"Indian stamp duty\", \"Schedule I Indian Stamp Act\", \"stamp duty Bahamas\", \"Brazil IOF\", \"Argentina impuesto de sellos\", \"Mexico ISN\", or any request to assess stamp duty exposure on a document, security transfer, lease, or financial transaction. Maps stamp duty AND financial transaction tax (FTT) regimes across 40+ jurisdictions. Excludes the property/real-estate transfer side (see property-transfer-tax-matrix)."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GLOBAL
  category: cross-border
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/stamp-duty-matrix"
  tax_year: 2025
  obligation: STAMP
---

# Stamp Duty & Financial Transaction Tax Matrix v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

**This file is a content skill that loads on top of `cross-border-workflow-base`.** It covers stamp duties on documents, securities transfers, and the parallel financial transaction tax (FTT) regimes that economically resemble stamp duty.

**Tax year coverage.** Current for **calendar 2025**, reflecting:
- **UK stamp taxes** — SDRT 0.5% on chargeable securities; stamp duty on physical paper transfers; 1.5% SDRT/stamp duty on issuances to clearance services / depositary receipts confirmed by HMRC after the CJEU HSBC ruling
- **Italian FTT** unchanged at 0.2% (regulated market) / 0.22% (OTC); derivatives schedule
- **French FTT** at 0.3% on French listed company shares (in-scope > EUR 1bn cap)
- **Spanish FTT (IFT)** at 0.2% on Spanish listed shares > EUR 1bn cap
- **Hong Kong stamp duty on shares** reduced 0.10% buyer + 0.10% seller (cut from 0.13% in November 2023)
- **Singapore ACD (Additional Conveyance Duty)** rules for property-rich entities
- **Indian Stamp Act** as substantively amended (federal stamp duties on securities since 2020 + state stamp duty on instruments)

**The reviewer is the customer of this output.** Stamp duty assessments depend on precise document characterisation and jurisdiction. Every output must be reviewed by a credentialed local practitioner before any document is executed.

---

## Section 1 — Scope statement

This skill covers:

- **Stamp duty on securities (shares, bonds, partnership interests)**
- **Stamp duty on instruments** (loan agreements, mortgages, leases — to the extent not in property transfer skill)
- **Financial transaction taxes (FTT)** — France, Italy, Spain, OTC + listed
- **Documentary stamp taxes** — US state-level documentary stamp taxes, Philippines DST, India state stamp duty
- **Bank levies and securities account taxes** (Belgium TCT, illustrative)

This skill does NOT cover:

- **Real estate transfer tax / stamp duty on property** — see `property-transfer-tax-matrix.md`
- **VAT/GST on financial services** — see country VAT skills
- **Inheritance/gift documentary tax** — see `inheritance-estate-gift-matrix.md`
- **Customs duty** — see customs/duties skills

---

## Section 2 — UK Stamp Duty Reserve Tax (SDRT) and Stamp Duty

### 2.1 SDRT (FA 1986 Part IV)

**[T1] Rate**: 0.5% of consideration for the transfer of chargeable securities.

**Chargeable securities (s.99 FA 1986):** UK-incorporated company shares (and similar), some loan notes, units in unit trusts.

**Trigger**: agreement to transfer (regardless of whether share register is updated) settled through the CREST system → SDRT applied automatically; for off-CREST, payable via Stock Transfer Form + HMRC stamping.

### 2.2 Stamp duty on paper instruments

**[T1] Rate**: 0.5% of consideration; minimum stamp GBP 5. Applies when transfer effected by paper instrument (Stock Transfer Form).

### 2.3 The "1.5% charge" — depositary receipts and clearance services

**[T1] FA 1986 ss.67-70 / s.93:**
- 1.5% SDRT (or stamp duty) on issuance to:
  - A "depositary receipt issuer" (most commonly the bank issuing ADRs)
  - A "clearance service" (e.g., DTC for US investors)
- Confirmed by HMRC post-2009 CJEU HSBC ruling: the 1.5% on issuance is not generally enforced for EU/EEA destinations (CJEU C-569/07); however, HMRC's position post-Brexit and current administrative practice (FA 2024 amendments) treats issuance into Crest as not subject to 1.5%; complex issue requires specialist review

### 2.4 Exemptions

- Intra-group relief (s.42 FA 1930 / Sch 19 FA 1999): 0% for transfers within 75%+ group
- Demergers and reconstructions (ss.75-77 FA 1986)
- Loan capital (corporate debt) — most non-convertible debt
- Shares listed on a "recognised growth market" (AIM, AQSE Growth, certain SME markets) — 0% SDRT since 2014

### 2.5 Filing

- CREST: automatic
- Off-CREST: file STF with HMRC within 30 days of execution; instrument stamped

---

## Section 3 — Italy Financial Transaction Tax (FTT)

### 3.1 Three pillars

**[T1] Decreto Legge 24 aprile 2012 n.16:**

| Pillar | Rate | Base |
|---|---|---|
| **Tobin tax (cash equities)** | 0.2% (regulated market) / 0.22% (OTC) | Net daily balance per ISIN per intermediary; Italian-resident issuer share value > EUR 500m cap |
| **Derivatives** | EUR 0.01875 to EUR 200 per contract (sliding scale by notional value) | Derivatives on FTT-in-scope underlyings |
| **High frequency trading** | 0.02% on cancelled / modified orders | Orders cancelled within 0.5 seconds, > 60% modify-cancel ratio |

### 3.2 In-scope securities

- Shares of Italian companies with EUR > 500m market cap
- Securitised products (ETF) on Italian shares
- Derivatives referencing Italian shares

### 3.3 Exemptions

- Market making activities
- Pension funds and EU-equivalent retirement vehicles
- Sovereign wealth funds / central banks
- ETF creation / redemption (in-kind)
- Inheritance and gift transfers

### 3.4 Filing

- Italian intermediary acts as withholding agent
- Monthly remittance Model F24
- Annual reporting to Agenzia delle Entrate

---

## Section 4 — France FTT

### 4.1 Three components

**[T1] CGI Articles 235 ter ZD - ZE:**

| Component | Rate | Base |
|---|---|---|
| Tax on equity acquisitions | **0.3%** | Acquisitions of French-listed shares of EUR 1bn+ market cap issuers |
| Tax on HFT cancellations | 0.01% | Orders modified or cancelled within 0.5 seconds |
| Tax on sovereign CDS | 0.01% | Naked sovereign credit default swap purchases |

### 4.2 Scope

- French-incorporated companies listed on regulated EU market with market cap > EUR 1bn on 1 December prior year
- Maintained list published annually by Ministry of Finance (~140 issuers)

### 4.3 Exemptions

- Primary market issuances
- Liquidity provision / market making
- Intra-group transfers
- Acquisitions by employee schemes

### 4.4 Filing

- Withheld by accountable person (Euroclear France or intermediary)
- Returned via Form 3375 monthly

---

## Section 5 — Spain FTT (IFT — Impuesto sobre las Transacciones Financieras)

### 5.1 Mechanics (Ley 5/2020)

**[T1]:**
- **Rate**: 0.2%
- **Scope**: acquisitions of Spanish-listed shares of EUR 1bn+ market cap issuers (annually published list)
- **Liable party**: the financial intermediary
- **Exclusions**: primary market issuance, intra-group transfers, market making

### 5.2 Filing

- Monthly Form 604

---

## Section 6 — Other European stamp / FTT

| Country | Mechanism | Rate |
|---|---|---|
| **Ireland** | Stamp duty on share transfers | 1% on Irish shares (FA 1999 Sch 1) |
| **Ireland** | Stamp duty on residential property | 1% / 2% / 10% (see property skill) |
| **Switzerland** | Stamp duties on securities (Umsatzabgabe) | 0.15% Swiss securities / 0.30% non-Swiss (per dealer) |
| **Switzerland** | Issuance stamp duty (Emissionsabgabe) | 1% above CHF 1m on equity issuance (planned abolition); 0.06%-0.12% on certain debt |
| **Liechtenstein** | Mirrors Swiss stamps for shares | Same Swiss rates |
| **Luxembourg** | Registration duty on certain documents | Variable; capital duty long abolished |
| **Belgium** | Securities Transactions Tax (TOB) | 0.12% / 0.35% / 1.32% by category |
| **Belgium** | Securities Account Tax (TCT) | 0.15% above EUR 1m per account |
| **Greece** | Stamp duty on certain agreements | 2.4% or 3.6% |
| **Cyprus** | Stamp duty on transactions of capital value > EUR 5,000 | 0.15% on EUR 5,001 - 170,000; 0.20% above |
| **Malta** | Stamp duty on share transfers | 2% (5% if real-estate-rich entity) |
| **Portugal** | Imposto do Selo on financial transactions, leases, loans, insurance, guarantees | 0.04%-25% by category |
| **Norway** | Document duty (real-property only) | 2.5% (see property skill) |
| **Sweden, Finland, Denmark** | No stamp duty on shares / FTT |

---

## Section 7 — Asia-Pacific

| Country | Mechanism | Rate |
|---|---|---|
| **Hong Kong** | Stamp duty on share transfers | 0.10% buyer + 0.10% seller (reduced from 0.13%, November 2023) |
| **Singapore** | Stamp duty on share transfers | 0.2% of consideration (BSD subset for share transfers; ACD applies for residential property-rich entities) |
| **Singapore — ACD** | Additional conveyance duty | Up to 65% on acquisition of significant equity interests in property-rich entities |
| **Australia** | Stamp duty on share transfers | Abolished federally 2002; state-level mostly abolished for shares but landholder/property-rich rules apply (each state) |
| **New Zealand** | No stamp duty on shares | n/a |
| **India** | Indian Stamp Act (federal stamp on securities since 2020; state stamp on instruments) | 0.005% on equity issuance and transfer; 0.015% on equity delivery-based; state-specific for other instruments |
| **Japan** | Stamp duty on contracts and securities | Document-based (Stamp Tax Law, fixed amounts by document type); no FTT on share transfers |
| **South Korea** | Securities Transaction Tax | 0.15% to 0.35% by market (reduced from previous 0.43%) |
| **China** | Securities Transaction Stamp Tax | 0.1% one-sided (sale only since 2008 reform) on A-shares; reduced to 0.05% temporarily in August 2023 |
| **Taiwan** | Securities Transaction Tax | 0.3% on equities; 0.1% on bonds (mostly exempt) |
| **Indonesia** | No FTT on shares; small documentary stamp | n/a |
| **Thailand** | Stamp duty on instruments | Fixed amounts by document type; share transfer 0.1% |
| **Philippines** | Documentary Stamp Tax (DST) | Wide-ranging, see NIRC §173-201 |
| **Malaysia** | Stamp duty on share transfers | 0.3% on physical shares; 0% on shares of public listed companies traded on Bursa Malaysia (FA 2023) |
| **Vietnam** | Securities Transaction Tax | 0.1% on sale |

---

## Section 8 — Americas

| Country | Mechanism | Rate |
|---|---|---|
| **United States — Federal** | No federal stamp on shares; SEC Section 31 fee (~0.00229%) levied on equity transactions | n/a |
| **United States — State** | New York stock transfer tax in force but 100% rebate has applied since 1981 (effectively 0% federal-state); Florida documentary stamp on stock = 35 cents per USD 100; other state DSTs by document | Varies |
| **Canada** | No federal or provincial stamp duty on shares | n/a (subject to LTT in QC for certain documents) |
| **Mexico** | Impuesto sobre Adquisición de Inmuebles ("ISAI") and Impuesto a la Adquisición de Acciones ("if applicable") | n/a as general FTT — primarily local property |
| **Brazil — IOF on securities (IOF/títulos)** | Tax on securities transactions | 0% to 1.5% depending on issuer / holding period / instrument; complex matrix |
| **Argentina — Impuesto de Sellos** | Provincial stamp duty | 0.5%-3% on contracts (mostly real estate, leases, loans) — varies by province |
| **Chile — Impuesto de Timbres y Estampillas** | Stamp tax on loans and other documents | 0.066% per month (capped at 0.8%) on loan amount |
| **Colombia — Impuesto de Timbre** | Stamp tax | Specific rates by document; reformed 2022 |
| **Peru — Impuesto a las Transacciones Financieras (ITF)** | Tax on bank account movements | 0.005% per debit/credit on local bank accounts |

---

## Section 9 — Africa and Middle East

| Country | Mechanism | Rate |
|---|---|---|
| **South Africa** | Securities Transfer Tax (STT) | 0.25% on share transfers and beneficial ownership changes |
| **Egypt** | Stamp tax on securities transactions | 0.05% per side for tax residents (0.15% on disposal for non-residents) |
| **Nigeria** | Stamp duty on instruments | 0.075% on share transfer; 1.5% on documentary purchases above NGN 10k |
| **Kenya** | Stamp duty on shares | 1% on transfer; 0% on listed transfers since 2006 |
| **UAE** | No general stamp duty | n/a (sector-specific fees apply) |
| **Saudi Arabia** | No general stamp duty | n/a (5% real estate transaction tax separately) |
| **Bahrain** | No stamp duty | n/a |
| **Qatar** | No stamp duty | n/a |
| **Israel** | Stamp duty abolished 2006 | n/a |

---

## Section 10 — Computation walk-through

### Example 1 — UK share acquisition

A UK private equity fund acquires GBP 50m of shares in a UK-incorporated AIM-listed company via CREST.

- AIM exemption applies → **0% SDRT** on the AIM portion
- Confirm AIM listing on relevant Recognised Growth Markets list as published by HMRC

### Example 2 — Italian listed share — non-resident purchaser

A French institutional buyer purchases EUR 10m of shares in Generali (Italy-listed, > EUR 500m market cap).

- Italian FTT: 0.2% × EUR 10m = **EUR 20,000**
- Italian intermediary remits; non-resident bears the cost

### Example 3 — Hong Kong share transfer

HKD 100m share transfer in a Hong Kong-incorporated private company.

- Buyer side: 0.10% × HKD 100m = **HKD 100,000**
- Seller side: 0.10% × HKD 100m = **HKD 100,000**
- Both parties pay; intermediated through IRD stamping

### Example 4 — Singapore share-acquisition with property-rich target

Foreign investor acquires 100% of a Singapore Pte Ltd whose >50% of total tangible assets is Singapore residential property.

- Basic transfer stamp duty: 0.2% × consideration
- ACD: applies to "significant owner" (≥50% of qualifying equity interest) acquisitions of "property-holding entities"; **up to 65%** total when combined with the underlying property's ABSD rates
- Specialist advice required; reviewer escalation

---

## Section 11 — Output specification

The reviewer brief must include:

1. **Transaction classification** — document type, instrument, security, financial transaction
2. **Stamp / FTT analysis** per applicable jurisdiction
3. **Rate and base** with statutory citation
4. **Exemption analysis** — intra-group relief, market making, primary issuance, listed status
5. **Liable party** (buyer / seller / both / intermediary withholding)
6. **Filing mechanics** — when, how, by whom
7. **Reviewer questions** — open items flagged as [T2] or [T3]

---

## Section 12 — Self-checks

- [ ] Document characterisation tested per local taxonomy (each country has distinct "instruments" list)
- [ ] Each transaction party's stamp duty position computed separately (buyer vs seller)
- [ ] Intra-group relief documentary requirements confirmed (75% common ownership for UK)
- [ ] AIM / recognised growth market exemption (UK) confirmed against current list
- [ ] French / Italian / Spanish FTT scope confirmed against current annual list
- [ ] Hong Kong rate (0.10% per side; 0.13% old rate not applied post-November 2023)
- [ ] Singapore ACD tested for property-rich entity transfers
- [ ] India federal + state stamp duty stacked correctly
- [ ] Brazil IOF / Argentina sellos / Chile timbres per applicable transaction type
- [ ] Output flags every [T2]/[T3] item for reviewer judgement

---

## Section 13 — Prohibitions

- **Do not** apply the old 0.13% Hong Kong stamp duty rate to transactions executed after November 2023 — the rate is 0.10% per side.
- **Do not** assume UK intra-group relief applies without confirming 75% common beneficial ownership AND the relief application has been correctly notified.
- **Do not** advise that AIM-listed shares are exempt without confirming the listing is on a HMRC-recognised growth market.
- **Do not** ignore Italian / French / Spanish FTT for non-resident purchasers — the tax is at the security level, not the purchaser's residence.
- **Do not** apply property-rich entity rules (Singapore ACD, Australian landholder duty) without confirming the threshold (typically 50% of tangible assets) and qualifying equity interest tests.

---

## Section 14 — Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Stamp duty depends on precise document characterisation and is jurisdiction-specific. Every output must be reviewed and signed off by a credentialed local practitioner before any document is executed.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/stamp-duty-matrix) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
