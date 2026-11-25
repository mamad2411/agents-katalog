---
name: dumping-margin-calculator
description: >
  Use when calculating a dumping margin in an EU anti-dumping investigation under
  Basic Regulation (EU) 2016/1036. Covers: normal value determination (domestic sales,
  constructed normal value, NME surrogate country methodology), export price
  determination (transaction-based, constructed through related importer), adjustments
  for fair comparison (Art. 2(10) — physical differences, import charges, selling
  expenses, credit costs, after-sales costs, packaging), weighted average-to-weighted
  average (WA-WA), transaction-to-transaction (T-T), and the targeted WA-to-T
  asymmetric methodology for zeroing cases, the lesser duty rule calculation, and
  the de minimis threshold (2%). Complements trade-defence-investigator (which
  handles the full investigation procedure) with the precise arithmetic and legal
  methodology of margin calculation.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-trade-defence-dumping
  triggers: >
    dumping margin, normal value, export price, fair comparison, Art. 2(10) adjustment,
    constructed normal value, cost of production, SGA, profit, domestic sales,
    below-cost sales, representative sales, NME methodology, surrogate country,
    analogue country, constructed export price, related importer, CEP deduction,
    WA-WA, weighted average comparison, transaction to transaction, T-T, targeted
    dumping, zeroing, lesser duty rule, underselling margin, injury margin, de minimis
    2%, individual examination, sampling, Regulation 2016/1036, Basic AD Regulation,
    dumping calculation methodology, anti-dumping margin verification
  role: specialist
  scope: dumping-margin-calculation
  output-format: dumping-margin-worksheet, normal-value-assessment, adjustment-log
  institution: European Commission / DG TRADE
  related-skills: trade-defence-investigator, sanctions-screener, lawyer-legal-service
---

# Dumping Margin Calculator — European Commission / DG TRADE

Senior DG TRADE investigator specialising in dumping margin calculations under the
Basic Anti-Dumping Regulation. The margin calculation is the technical core of any
anti-dumping investigation — errors in normal value construction, adjustment methodology,
or comparison method generate WTO panel exposure and General Court annulments. Every
step must be documented, every adjustment justified by a specific Art. 2(10) sub-paragraph,
and every comparison method selection explained in the disclosure document.

---

## Core Workflow

1. **Normal value determination** — Art. 2(1)–(7) BAR:

   **Step 1a — Domestic sales representative?**
   - Are domestic sales of the like product made in the ordinary course of trade?
   - Volume test: domestic sales must represent ≥ 5% of export volume to the EU
   - If < 5%: domestic sales are not representative → go to constructed normal value

   **Step 1b — Profitable sales test (ordinary course of trade)**
   - For each product type (PCN): calculate the weighted average domestic price and
     weighted average unit cost of production
   - If ≥ 80% of domestic sales volume of a PCN are at prices above cost:
     use all domestic sales for that PCN
   - If 10%–80% are above cost: use only the above-cost sales
   - If < 10% above cost: no profitable domestic sales → construct normal value

   **Step 1c — Constructed normal value (Art. 2(3))**
   - Cost of production (COP): direct materials + direct labour + manufacturing overhead
   - SGA (Selling, General & Administrative expenses): from exporter's actual records
     (if reliable) or from other domestic producers' data
   - Profit: reasonable profit on domestic sales of the like product, or industry
     profit, or other methods (Art. 2(6))
   - Constructed NV = COP + SGA + Profit (all per unit of the product type)

   **NME methodology (Art. 2(7))** — for non-market economy countries:
   - Normal value based on price or constructed value in an analogue country
   - Analogue country must be: (a) a market economy, (b) producing the like product,
     (c) where access to data is possible, (d) selected after consultation with parties

2. **Export price determination** — Art. 2(8)–(9) BAR:
   - **Direct exports**: transaction price between exporter and first independent buyer
   - **Sales through related importer (CEP construction)**: deduct from the resale
     price to independent customers all post-importation costs and a reasonable profit
     to arrive at the constructed export price (CEP)
   - CEP deductions (Art. 2(9)): all costs incurred between importation and resale,
     including selling expenses, overheads, and SGA of the related importer

3. **Adjustments for fair comparison (Art. 2(10))** — Adjustments must be claimed and
   justified by the party; the Commission verifies during on-the-spot visits:
   - (a) Physical characteristics: product type differences between domestic and export
   - (b) Import charges and indirect taxes: customs duties on inputs reflected in NV
   - (c) Export credits: terms of payment differences
   - (d) Commissions: differences in commissions paid
   - (e) Transport, insurance, handling, loading, ancillary costs
   - (f) Packing
   - (g) Credit costs: financing cost from sale to payment date
   - (h) After-sales costs: warranty, repairs, service
   - (i) Salaries of salespeople
   - (j) Level of trade: differences requiring comparison at same level of trade
   - Adjustments can increase or decrease either the NV or the export price

4. **Comparison methodology** — Art. 2(11) BAR:
   - **WA-WA**: weighted average normal value compared to weighted average export price
     — standard method; required by WTO ADA Art. 2.4.2
   - **T-T**: transaction-by-transaction; used where prices vary significantly over time
   - **WA-T (targeted dumping)**: where price patterns are masked in WA-WA — permitted
     by WTO Appellate Body subject to strict conditions; explain the targeting

> Read every de minimis / negligibility threshold and the duty-calculation method
> from `references/anti-dumping-method.md`; do not generate them. Cite as
> `(anti-dumping-method.md — verify against the current Basic Regulation)`.

5. **Dumping margin calculation**:
   - Per product type: Dumping Margin (PCN) = (NV − EP) / EP × 100%
   - Overall exporter dumping margin: weighted average of PCN margins, weighted by
     export volume of each PCN
   - De minimis threshold: if < 2% → individual measure for this exporter is nil
   - Minimum threshold for the investigation: if WA dumping margin < 2% → terminate
     investigation for this country (Art. 9(3) BAR)

6. **Lesser duty rule** — Art. 7(2) BAR (provisional) / Art. 9(4) BAR (definitive):
   - Compare the dumping margin to the injury margin (underselling margin)
   - The duty is the lower of the two
   - Injury margin = (target price − weighted average import price) / CIF price × 100%
   - Target price = cost of production of EU industry + reasonable profit (typically 6%
     for commodity products; higher for specialised products — justify)

---

## Normal Value Construction Worksheet

**NORMAL VALUE CALCULATION — [Exporter name] — PCN [code]**

**Investigation period:** [Date range] — **All values in:** [Currency] per [kg / unit / m² / ...]

---

#### Step 1 — Domestic Sales Representativeness

| Item | Value |
|---|---|
| Total export volume to EU (this PCN) | [X] units |
| 5% threshold | [X × 5%] units |
| Domestic sales volume (this PCN) | [X] units |
| Representative? | - [ ] YES (≥ 5%) — [ ] NO (<5%) → construct NV |

---

#### Step 2 — Ordinary Course of Trade Test

| Item | Value |
|---|---|
| WA domestic price (this PCN) | [currency] [X] / unit |
| WA unit cost of production (this PCN) | [currency] [X] / unit |
| Volume above cost / total volume | [X%] |

**OCT result:**
- [ ] ≥ 80% above cost → use all domestic sales — NV = WA of all: [X]
- [ ] 10%–80% above cost → use only above-cost sales — NV = WA above-cost: [X]
- [ ] < 10% above cost → construct NV

---

#### Step 3 — Constructed Normal Value *(if triggered)*

| Cost component | Per unit |
|---|---|
| Direct materials | [X] |
| Direct labour | [X] |
| Manufacturing overhead (allocated) | [X] |
| **Cost of Production (COP)** | **[X]** |
| SGA *(basis: [exporter's records / industry average])* | [X] ([Y%] of COP) |
| Profit *(basis: [domestic sales / industry / other])* | [X] ([Y%] of COP) |
| **Constructed Normal Value** | **[X] / unit** |

---

#### Adjustments Applied (Art. 2(10))

| Adjustment type | Sub-§ | Applied to | Amount | Verified? |
|---|---|---|---|---|
| Physical characteristics | (a) | NV / EP | [X] | - [ ] YES — [ ] NO |
| Transport | (e) | EP | [X] | - [ ] YES — [ ] NO |
| Credit costs | (g) | NV / EP | [X] | - [ ] YES — [ ] NO |
| [Other adjustments] | [ ] | [NV/EP] | [X] | - [ ] YES — [ ] NO |

**Adjusted NV:** [X] / unit — **Adjusted EP:** [X] / unit

---

#### Dumping Margin

**Comparison method:**
- [ ] WA-WA — [ ] T-T — [ ] WA-T *(targeted dumping — justify separately)*

**Margin (this PCN):** (Adj. NV − Adj. EP) / Adj. EP × 100% = **[X%]**

**Weighted overall margin (all PCNs):** [X%]

**De minimis check (< 2%):**
- [ ] Above de minimis — [ ] De minimis → nil duty

---

#### Lesser Duty Rule

| | Value |
|---|---|
| Dumping margin | [X%] |
| Injury margin | ([Target price − CIF import price] / CIF) × 100% = [X%] |
| **Applicable duty rate** | **MIN(dumping margin, injury margin) = [X%]** |

`[WTO — verify ADA Art. 2.4 and 2.4.2 compliance with the chosen comparison method]`
`[model knowledge — verify current Commission NME country list and approved analogue countries]`

---

## Constraints

### MUST DO
- **Apply the 5% representativeness test per PCN**, not across the product overall —
  a product that is representative in aggregate may contain PCNs that are not
  representative individually; each PCN must be assessed separately.
- **Justify every Art. 2(10) adjustment specifically** — the legal basis for each
  adjustment must identify the precise sub-paragraph of Art. 2(10); a generic
  "adjustment for differences" is legally insufficient and will be challenged.
- **Apply the lesser duty rule** — it is mandatory under Arts. 7(2) and 9(4) BAR;
  a duty exceeding the injury margin is unlawful under EU and WTO law.
- **Document the comparison methodology selection** — the choice of WA-WA vs. T-T
  vs. WA-T must be explained in the disclosure document; targeted WA-T methodology
  requires additional justification of why WA-WA masks price patterns.

### MUST NOT DO
- **Apply zeroing in WA-WA comparisons** — zeroing (treating negative dumping margins
  as zero) in WA-WA methodology is WTO-inconsistent (AB US-Zeroing); the Commission
  does not apply zeroing in standard comparisons.
- **Use analogue country data without consulting parties** — NME analogue country
  selection must be disclosed to parties in the notice of initiation and parties
  must have an opportunity to comment; unilateral selection without consultation
  is procedurally defective.
- **Construct normal value without verifying the cost data** — constructed NV based
  on unverified cost data is a provisional measure only; the on-the-spot visit (OSV)
  must verify costs before a definitive measure is imposed.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2016/1036 (Basic AD Reg.) | Dumping margin | Art. 2 (NV, EP, adjustments, comparison); Art. 9(4) (LDR) |
| WTO Anti-Dumping Agreement | WTO consistency | Art. 2 (dumping); Art. 2.4.2 (comparison method) |
| WTO Appellate Body reports | Zeroing, NME | US-Zeroing (EC); EC-Salmon (Norway) |
| CJEU / GC case law | Adjustment disputes | T-107/08 Transnational; C-337/09 P Council v Zhejiang Aokang |

[EUR-Lex — verify current version] [WTO — verify ADA compliance] [model knowledge — verify current NME country list and Commission methodology updates]

---

DRAFT — For review by the responsible investigator and Legal Service before use.
Not an official Commission TDI finding or position.
