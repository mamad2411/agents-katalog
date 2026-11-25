---
name: stamp-duty-calc
description: Calculate stamp duty payable on Hong Kong property transactions under the Stamp Duty Ordinance (Cap 117), including Ad Valorem Stamp Duty, Buyer's Stamp Duty, Special Stamp Duty, and New Residential Stamp Duty, with scenarios for HKPR, non-HKPR, corporate, and developer buyers.
---

# Stamp Duty Calculator — Skill

## Purpose

Calculate stamp duty payable on Hong Kong property transactions under the Stamp Duty Ordinance (Cap 117), covering all applicable duty types (AVD, BSD, SSD, NRSD) and providing guidance on reliefs, exemptions, and compliance timelines.

## Scope

- Ad Valorem Stamp Duty (AVD) — standard scale rates
- Buyer's Stamp Duty (BSD) — non-HKPR and corporate buyers
- Special Stamp Duty (SSD) — short-term resale
- New Residential Stamp Duty (NRSD) — additional residential property
- Stamp duty reliefs and exemptions
- Adjudication and payment process
- Double stamp duty and penalty provisions

## Workflow

### 1. Determine Property Classification

- **Residential** vs **non-residential** (commercial, industrial, car park)
- **Hong Kong** property (stamp duty only applies to HK property)
- **New development** (first-hand sale) vs **secondary market**
- **Single property** vs **multiple properties** in one transaction

### 2. Determine Buyer Status

- **Hong Kong Permanent Resident (HKPR)**: 
  - Buying as individual (not acting for a company)
  - No other residential property in HK → AVD Scale 2 (lower rates)
  - Already owns residential property → NRSD applies
- **Non-HKPR individual**: BSD + AVD + potentially NRSD
- **Company (any jurisdiction)**: BSD + AVD + potentially NRSD
- **Foreign buyer (non-HKPR)**: BSD + AVD + potentially NRSD
- **Developer buyer**: applicable duties per buyer type

### 3. Calculate Ad Valorem Stamp Duty (AVD)

#### Scale 2 Rates (HKPR first-time buyer, no other HK residential property)

| Property Value (HK$) | Rate |
|---------------------|------|
| Up to 3,000,000 | HK$100 |
| 3,000,001 – 3,500,260 | HK$100 + 10% of excess over 3,000,000 |
| 3,500,260 – 4,500,000 | 1.5% |
| 4,500,001 – 4,935,480 | HK$67,500 + 10% of excess over 4,500,000 |
| 4,935,480 – 6,000,000 | 2.25% |
| 6,000,001 – 6,642,860 | HK$135,000 + 10% of excess over 6,000,000 |
| 6,642,860 – 9,000,000 | 3% |
| 9,000,001 – 10,080,000 | HK$270,000 + 10% of excess over 9,000,000 |
| 10,080,000 – 20,000,000 | 3.75% |
| 20,000,001 – 21,739,130 | HK$750,000 + 10% of excess over 20,000,000 |
| Over 21,739,130 | 4.25% |

#### Scale 1 Rates (All other buyers / second property)

| Property Value (HK$) | Rate |
|---------------------|------|
| Up to 3,000,000 | 1.5% |
| 3,000,001 – 3,290,320 | HK$45,000 + 20% of excess over 3,000,000 |
| 3,290,320 – 4,000,000 | 3% |
| 4,000,001 – 4,428,570 | HK$120,000 + 20% of excess over 4,000,000 |
| 4,428,570 – 5,028,570 | 4.5% |
| 5,028,571 – 5,600,000 | HK$226,286 + 20% of excess over 5,028,571 |
| 5,600,001 – 6,720,000 | 6% |
| 6,720,001 – 7,200,000 | HK$403,200 + 20% of excess over 6,720,000 |
| 7,200,001 – 8,640,000 | 7.5% |
| 8,640,001 – 9,600,000 | HK$648,000 + 20% of excess over 8,640,000 |
| Over 9,600,000 | 8.5% |

### 4. Buyer's Stamp Duty (BSD)

- **Rate**: 7.5% on the higher of consideration or market value
- **Applies to**: 
  - Non-HKPR individuals purchasing residential property
  - Companies (any jurisdiction) purchasing residential property
  - HKPRs acting as nominees or trustees for non-HKPRs
- **Does not apply to**:
  - HKPR individuals buying in own name
  - Transfers between Hong Kong spouses
  - Transfers on divorce or inheritance
  - Certain intra-group corporate transfers

### 5. Special Stamp Duty (SSD)

- **Applies to**: residential property resold within short holding period
- **Rate** (sliding scale from date of acquisition):

| Holding Period | Rate |
|---------------|------|
| 6 months or less | 20% |
| More than 6 but ≤ 12 months | 15% |
| More than 12 but ≤ 24 months | 10% |
| More than 24 months | 0% |

- **Calculated on**: the higher of consideration or market value
- **Seller pays** (not buyer)
- **Applies regardless of buyer status**
- **Exemptions**: forced sales (mortgagee sale), involuntary transfers

### 6. New Residential Stamp Duty (NRSD)

- **Rate**: 7.5% on the higher of consideration or market value
- **Applies to**: HKPR individuals who already own residential property in HK
- **Does not apply to**: first-time buyers, non-residential property
- **Refund available**: if buyer replaces primary residence within 12 months (subject to conditions)

### 7. Total Stamp Duty Calculation

#### Example Scenarios

**Scenario A: First-time HKPR buyer, HK$8,000,000 residential property**
- AVD (Scale 2): 3% × 8,000,000 = HK$240,000
- BSD: N/A (HKPR individual)
- SSD: N/A (no short-term resale)
- NRSD: N/A (first property)
- **Total**: HK$240,000

**Scenario B: Non-HKPR buyer, HK$12,000,000 residential property**
- AVD (Scale 1): 3.75% × 12,000,000 = HK$450,000
- BSD: 7.5% × 12,000,000 = HK$900,000
- SSD: N/A
- NRSD: N/A (BSD already applies — NRSD may be revisited)
- **Total**: approximately HK$1,350,000 (confirm with latest IRD practice)

**Scenario C: Corporate buyer, HK$50,000,000 residential property**
- AVD (Scale 1): 4.25% × 50,000,000 = HK$2,125,000
- BSD: 7.5% × 50,000,000 = HK$3,750,000
- **Total**: approximately HK$5,875,000

**Scenario D: Seller reselling within 12 months, HK$8,000,000**
- SSD: 15% × 8,000,000 = HK$1,200,000 (seller pays)
- Buyer pays their own stamp duty separately

### 8. Stamp Duty Adjudication and Payment

#### Process
1. Prepare stamp duty adjudication form (IRD Stamp Office)
2. Submit within **30 days** of the agreement (signature date)
3. Pay duty on adjudication or within 30 days (whichever is later)
4. Obtain stamped instrument

#### Late Payment Penalties
- Up to 30 days late: HK$200
- 1–2 months late: HK$400
- 2+ months late: 10 × the duty otherwise payable

### 9. Reliefs and Exemptions

- **Spousal transfer**: between husband and wife (exempt from all duty)
- **Divorce/separation**: court-ordered transfer (exempt)
- **Inheritance**: estate administration (exempt)
- **Intra-group transfer**: corporate restructuring (AVD relief available)
- **Company reconstruction**: relief on qualifying reconstruction
- **First-time HKPR**: AVD Scale 2 (lower rates)
- **Replacement property**: NRSD refund on sale of old primary residence within 12 months
- **Charities**: exemption on charitable transfers

## Key Provisions (Cap 117)

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.19 | Instruments chargeable | Agreement for sale, assignment, lease |
| s.29D | BSD | 7.5% on residential by non-HKPR/company |
| s.29DA | SSD | 10–20% on short-term resale |
| s.29DF | NRSD | 7.5% on additional residential by HKPR |
| Schedule 1 | AVD rates | Scale rates for conveyances on sale |
| s.52 | Adjudication | Must adjudicate within 30 days |

## Tools & Resources

- IRD Stamp Office (https://www.ird.gov.hk/stamps) — duty rates, forms, e-Stamping
- Land Registry (https://www.landreg.gov.hk) — consideration verification, property records
- Rating and Valuation Department (https://www.rvd.gov.hk) — market value adjudication
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 117 provisions
- IRD Practice Directions on stamp duty


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
