---
name: wealth-estate-tax-workflow-base
description: "> Tier 1 workflow base for wealth tax, inheritance / estate tax, gift tax, and property transfer tax skills. Covers asset inventory, valuation, beneficiary / heir identification, exemption / relief analysis, computation, double-tax relief, and filing assembly. Workflow architecture only — no country rate tables. MUST be loaded alongside a content skill — wealth-tax-matrix, inheritance-estate-gift-matrix, property-transfer-tax-matrix, or a country-specific skill. Assumes a credentialed estate planning practitioner (private client lawyer, notary, CPA, EA, or equivalent) reviews and signs off on every output. Does NOT cover: probate procedure, will drafting, trust administration beyond tax mechanics."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GLOBAL
  category: foundation
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/wealth-estate-tax-workflow-base"
  obligation: FW
---

# Wealth / Estate / Gift / Property Transfer Tax Workflow Base v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

Tier 1 workflow base for transfer-on-death, gift, annual wealth, and property purchase tax skills.

---

## Section 1 — Audience and assumptions

This base covers a family of related taxes triggered by:
- **Holding** — annual wealth tax
- **Transfer at death** — inheritance / estate tax
- **Inter-vivos transfer** — gift tax
- **Real estate purchase / transfer** — property transfer tax / stamp duty

This base assumes:
- The taxpayer (or their representative) is preparing an accurate inventory
- Cross-border situs rules require multi-jurisdictional analysis
- A credentialed practitioner signs off before filing or transfer

---

## Section 2 — Universal lifecycle

### Step 1 — Identify the chargeable event

**[T1]**

| Event | Tax(es) potentially triggered |
|---|---|
| Annual reference date (31 Dec typically) | Wealth tax (Spain, Norway, Switzerland, Argentina, Colombia, Uruguay, France IFI, NL Box 3) |
| Death of holder | Inheritance / estate tax (DE, FR, ES, IT, NL, BE, UK, US, JP, KR) |
| Gift / lifetime transfer | Gift tax (DE, FR, ES, IT, NL, BE, UK, US, JP, KR) |
| Real estate purchase | Property transfer tax (UK SDLT, DE GrESt, FR DMTO, IT registro, ES ITP/AJD, NL OB, SG BSD+ABSD, HK AVD) |

### Step 2 — Determine personal scope

**[T1]** For wealth / estate / gift:
- Tax residence / domicile / long-term residence (UK from April 2025) of taxpayer / decedent / donor
- Worldwide assets if resident; local-situs only if non-resident

**[T1]** For property transfer:
- Purchaser's residence affects surcharge (UK 2% non-resident; Singapore ABSD 60% foreign; Canada NRST 25%; Australia state surcharges 7-8%)
- Property's situs determines primary tax

### Step 3 — Inventory all assets

**[T1] For each asset, document:**
- Class (real estate, listed shares, unlisted shares, bank deposit, debt instrument, private equity, art / collectibles, crypto-asset, pension rights, life insurance, business interest)
- Location (situs per jurisdiction's rules)
- Valuation date
- Valuation method (cadastral value, FMV, latest transaction, IFRS book value, professional appraisal)
- Ownership share

### Step 4 — Apply valuation rules

**[T1]** Each tax / country has specific rules:
- **Spanish ISD / wealth tax**: cadastral value for real estate; "valor real" elsewhere
- **French IFI**: market value with 30% discount for primary residence (wealth tax)
- **German Erbschaftsteuer**: Bewertungsgesetz fair market value with specific business property mechanics
- **UK IHT**: open market value at date of death
- **US estate tax**: fair market value at date of death OR alternate valuation date (6 months later, electable)
- **Italian successioni**: cadastral value × multiplier (110 for first home, 120 for second, etc.)

### Step 5 — Deduct liabilities

**[T1]**
- Mortgages secured on the relevant asset
- Funeral expenses (US, UK estate)
- Administration expenses
- Outstanding tax liabilities
- Loans where foreign-bank-debt restrictions apply (Spain ISD, Uruguay)

### Step 6 — Identify beneficiaries and apply relationship rules

**[T1]** For inheritance / gift:
- Spouse / civil partner / cohabitant
- Direct descendants (children, grandchildren)
- Direct ascendants (parents, grandparents)
- Siblings
- Other relatives within a defined degree
- Unrelated

Each relationship has distinct exemptions and rates (Germany Class I-III; Spain Group I-IV; France direct line vs collateral).

### Step 7 — Apply exemptions and reliefs

**[T1] Common reliefs:**
- Marital deduction (US unlimited; UK unlimited for LTR spouse; EUR 500k Germany)
- Habitual residence exemption (Spain national EUR 300k)
- Family business / Pacte Dutreil 75% (France) / Verschonungsabschlag 85-100% (Germany) / BPR 100% (UK)
- Agricultural property relief (UK APR; various national reliefs)
- Charitable beneficiary deduction
- Disabled beneficiary supplementary allowance

### Step 8 — Apply rate schedule

**[T1]** Rate schedule may be:
- Progressive by amount (US estate 18-40%; French succession 5-45%; German IHT 7-50%)
- Flat by class (Italian successioni 4% / 6% / 8%)
- Regional variation (Spanish ISD by CCAA; Swiss canton)

### Step 9 — Apply caps and integration

**[T1]**
- **Spain**: combined IRPF + IP + Solidaridad capped at 60% of IRPF base
- **France IFI**: capped at 75% of prior year income
- **US**: estate, gift, GST share a unified credit
- **UK**: 7-year cumulation rule (lifetime transfers within 7 years before death come back into estate)

### Step 10 — Compute and apply foreign tax credits

**[T1]** Treaty article 22 (wealth) or estate / inheritance tax treaties (rare; ~15 bilateral). Unilateral credit usually available for same asset taxed twice.

### Step 11 — Filing and payment

**[T1]**
- Identify filing form per regime
- Filing deadline (typically 6-12 months from event)
- Payment terms (instalments for family businesses)
- Currency translation rules
- Documentation index

---

## Section 3 — Cross-border specifics

### 3.1 Situs determination

| Asset class | Typical situs |
|---|---|
| Real estate | Land location |
| Tangible movable | Physical location at event |
| Shares in companies | Country of incorporation OR share register |
| Bank deposits | Country of bank |
| Government bonds | Country of issue |
| Private equity / unlisted | Country of company residence |
| Crypto | Owner's residence (contested) |

### 3.2 Treaties

Wealth / estate / inheritance tax treaties exist sparsely. Most relief is unilateral.

---

## Section 4 — Reviewer brief

```
1. Personal scope
   - Tax residence / domicile / LTR confirmation
   - Worldwide vs local-situs basis

2. Asset inventory
   - Class, situs, value, ownership

3. Liabilities and deductions

4. Beneficiary / heir register
   - Relationship classification per jurisdiction

5. Exemptions and reliefs schedule

6. Computation per jurisdiction

7. Cap analysis (Spain 60%, France 75%, US unified credit)

8. Cross-border credit

9. Filing schedule and payment plan

10. Reviewer questions — [T2]/[T3] items
```

---

## Section 5 — Self-checks (14)

1. [ ] Tax residence / domicile / LTR tested per each jurisdiction's specific definition
2. [ ] Reference date applied correctly (31 December for wealth; date of death for IHT; date of gift)
3. [ ] All assets inventoried with situs determination
4. [ ] Valuation methodology per jurisdiction (cadastral, FMV, multiplier, professional appraisal)
5. [ ] Deductible liabilities only included where regime permits
6. [ ] Beneficiary relationships classified per jurisdiction taxonomy
7. [ ] Exemptions applied (marital, habitual residence, business, agricultural)
8. [ ] Rate schedule applied to net not gross
9. [ ] Caps applied (Spain 60%, France IFI 75%)
10. [ ] 7-year cumulation applied (UK IHT)
11. [ ] Cross-border foreign tax credit applied where double taxation
12. [ ] Filing form, deadline, payment plan per jurisdiction
13. [ ] Step-up basis impact recorded (US beneficiaries' income tax)
14. [ ] Output flags every [T2]/[T3] item for reviewer judgement

---

## Section 6 — Refusal catalogue

| Refusal | Trigger |
|---|---|
| R-WET-1 | Beneficiary / heir under disability and lacking representative |
| R-WET-2 | Trust / nominee / hidden beneficial ownership without disclosure |
| R-WET-3 | Asset class not clearly classified (NFT, crypto, complex derivative) |
| R-WET-4 | Family business with relief eligibility uncertain (continuation, payroll, holding period) |
| R-WET-5 | Cross-border situs in dispute |
| R-WET-6 | DAC6 / MDR reportable arrangement |
| R-WET-7 | Pre-existing tax authority audit or controversy |

---

## Section 7 — Disclaimer

This workflow base produces working papers for review by credentialed estate planning practitioners. Estate, gift, wealth, and property transfer taxes have material magnitude and are jurisdiction-specific. Every output must be reviewed and signed off by a credentialed practitioner before filing or executing a transfer.

The most up-to-date, verified version of this workflow base is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/wealth-estate-tax-workflow-base) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
