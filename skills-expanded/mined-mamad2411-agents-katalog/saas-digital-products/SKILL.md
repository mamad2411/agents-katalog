---
name: saas-digital-products
description: "> Use this skill whenever a SaaS company, digital platform, app developer, marketplace, or other digital-product business asks about sector-specific tax / accounting / cross-border issues. Trigger on phrases like \"SaaS revenue recognition\", \"ASC 606 SaaS\", \"IFRS 15 SaaS\", \"subscription revenue\", \"ARR\", \"MRR\", \"deferred revenue\", \"termed license vs subscription\", \"ASC 985-20 software\", \"SaaS sales tax US\", \"Wayfair nexus SaaS\", \"EU OSS digital services\", \"marketplace facilitator\", \"permanent establishment server\", \"EU place of supply digital\", \"EU MOSS\", \"VAT digital services B2C\", \"GST low-value imported services\", \"US state sales tax SaaS\", \"MTD VAT SaaS UK\", or any SaaS-specific tax / accounting question. Covers IFRS 15 / ASC 606 SaaS revenue recognition, US state sales tax SaaS nexus (Wayfair post-2018), EU OSS / IOSS for digital services to consumers, EU VAT place of supply for cross-border B2B/B2C SaaS, Australia GST low-value imported services, India OIDAR / Equalisation Levy, Canada digital service…"
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GLOBAL
  category: vertical
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/saas-digital-products"
  obligation: VERT
---

# SaaS & Digital Products Sector Tax & Accounting v0.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## What this file is

A sector overlay for SaaS, digital platforms, app developers, marketplaces, and other digital-product businesses.

---

## Section 1 — Revenue recognition (IFRS 15 / ASC 606)

### 1.1 Five-step model

**[T1]**
1. Identify the contract with a customer
2. Identify the performance obligations
3. Determine the transaction price
4. Allocate the price to the performance obligations
5. Recognise revenue when each performance obligation is satisfied

### 1.2 Key SaaS issues

| Topic | Treatment |
|---|---|
| **Subscription / SaaS access** | Generally one performance obligation, satisfied over time (stand-ready obligation) — straight-line revenue over the term |
| **Implementation services** | Distinct (separate PO) only if customer can benefit from the SaaS without them; otherwise combined and recognised over the SaaS term |
| **Right of use license vs hosted service** | If the customer has a right to use the underlying software (e.g., download), revenue at point in time; if hosted, recognise over the contract term (stand-ready) |
| **Setup fees / activation fees** | Combine with subscription if not distinct; recognise over the customer's expected life |
| **Discounts and ramps** | Allocate to all POs proportionately, not just to specific period |
| **Variable consideration** | Constrain to amount unlikely to require significant reversal; commonly estimated for usage-based |
| **Customer acquisition costs (commissions)** | Capitalise per IFRS 15 ¶91-94 / ASC 340-40; amortise over expected customer life (often longer than contract term) |
| **Hosting agreement under SaaS arrangement (customer-side accounting)** | Cloud Computing Arrangement (CCA) — generally expensed as incurred; ASU 2018-15 allows capitalisation of certain implementation costs aligned to ASC 350-40 |

### 1.3 Examples of common SaaS issues

**[T1] Multi-year contract with discount in year 1:**
Contract: 3 years; $100k year 1, $150k years 2 and 3. Total $400k.
- Straight-line allocation: $133k/yr recognised
- Year 1 deferred revenue $33k; recognised in years 2/3

**[T1] SaaS + implementation services:**
- If implementation specific to SaaS and customer can't benefit without it → one PO, recognise both over SaaS contract term
- If implementation could be sold separately and customer can use other vendors → separate POs, implementation recognised on completion

---

## Section 2 — US state sales tax on SaaS (post-Wayfair)

**[T1] South Dakota v. Wayfair (2018)** overturned the physical presence test for sales tax nexus. Economic nexus now applies — typically $100,000 in sales or 200 transactions to the state.

### 2.1 SaaS taxability by state (sample)

| State | SaaS taxable? | Notes |
|---|---|---|
| **California** | No (generally) — service not tangible personal property | But certain "canned software" downloads taxable |
| **New York** | Yes — sales tax on SaaS to NY customers since 2010 |
| **Texas** | Yes — "data processing service" since 1980s; 20% exemption under §151.351 |
| **Florida** | No — service, not tangible | |
| **Washington** | Yes — Retail Sales Tax + B&O Tax | |
| **Illinois** | Generally no for SaaS but specific products taxable | |
| **Pennsylvania** | Yes — Sales and Use Tax on "computer services" | |
| **Massachusetts** | Yes if "prewritten" but no if customer-specific | |
| **Ohio** | Yes if "electronic information services" | |
| **Virginia** | No — service | |
| **Tennessee** | Yes — Telecommunication Sales Tax also applies | |
| **Georgia** | No — service | |
| **North Carolina** | Yes — "digital codes" but SaaS itself contested | |

**[T1] Marketplace facilitator laws** — most states require marketplaces (Amazon, Etsy, etc.) to collect on behalf of sellers above thresholds.

---

## Section 3 — EU VAT for digital services

### 3.1 Place of supply

**[T1] Article 58 PVD:**
- B2C electronic services: place of supply is **where the customer is established / has permanent address / usually resides**
- B2B electronic services: place of supply is **where the customer is established** (reverse charge)

### 3.2 OSS (One-Stop-Shop) and IOSS (Import OSS)

**[T1]**
- **Union OSS**: EU established supplier registers in home MS, declares all B2C cross-border EU sales of services + intra-EU B2C distance sales of goods
- **Non-Union OSS**: non-EU supplier registers in chosen MS for B2C EU electronic services
- **IOSS**: import OSS for goods ≤ EUR 150 imported into EU

### 3.3 VAT rates by country

Country-specific. For digital services to consumers, the destination MS rate applies. See country VAT skills.

---

## Section 4 — Other major SaaS VAT/GST regimes

### 4.1 United Kingdom

**[T1]** Post-Brexit, UK applies own VAT regime:
- Same place-of-supply rules as EU but UK-specific
- VAT on Electronic Services (VOES) registration for non-UK suppliers
- Standard rate 20%

### 4.2 Australia — GST low-value imported services

**[T1]** Since 1 July 2017 (digital services) and 1 July 2018 (goods ≤ AUD 1,000):
- Non-resident suppliers must register and collect 10% GST on supplies to Australian consumers if turnover ≥ AUD 75k
- B2B reverse charge

### 4.3 Canada — GST/HST on digital products

**[T1]** Since 1 July 2021:
- Non-resident suppliers register and collect GST/HST on B2C digital services if Canadian sales ≥ CAD 30k
- Provincial PST/RST/QST may also apply (BC, MB, QC)

### 4.4 India — OIDAR + Equalisation Levy

**[T1]**
- **OIDAR (Online Information Database Access or Retrieval)** services to Indian consumers — non-resident supplier registers and collects GST (18%)
- **Equalisation Levy 2.0 — 6% on advertising income** (the 2% e-commerce levy was repealed 1 August 2024)

### 4.5 Other notable

- **New Zealand** — 15% GST on remote digital services from non-residents (since 2016)
- **Singapore** — 9% GST on B2C digital services from non-residents (raised from 7% in 2024)
- **Japan** — 10% consumption tax on B2C digital services
- **South Korea** — 10% VAT on B2C digital services
- **Mexico** — 16% VAT on digital services from non-residents (since 2020)
- **Chile** — 19% VAT on digital services
- **Argentina** — 21% VAT plus 8% withholding on digital services

---

## Section 5 — Permanent establishment risk for SaaS

**[T1]** OECD Model Article 5 — physical presence threshold. Pure SaaS without local server typically does not create PE. Risk areas:
- Dependent agents soliciting business
- Customer success / support staff in country
- Co-located servers (Article 5 commentary: server can be a PE if customised, owned, and CIGAs performed there)
- Marketing / sales offices

**[T1] BEPS Action 1 / digital PE**: OECD Pillar One Amount A would create a new taxing right for "market jurisdictions" — pending ratification. DSTs continue in 25+ countries (see `digital-services-tax-matrix.md`).

---

## Section 6 — IFRS 15 / ASC 606 acquisition cost capitalisation

**[T1]** Sales commissions paid on customer acquisition:
- Capitalise if incremental and recoverable (IFRS 15 ¶91-94 / ASC 340-40)
- Amortise over the **expected customer life** (often longer than initial contract — including expected renewals)
- Practical expedient: expense if amortisation period < 1 year

This typically generates a significant balance sheet asset for high-growth SaaS companies.

---

## Section 7 — SaaS-specific KPIs interaction with accounting

**[T1] Non-GAAP / management measures:**

| Metric | Definition | Accounting interaction |
|---|---|---|
| **MRR / ARR** | Monthly / annual recurring revenue | Often gross; differs from GAAP revenue (which is subscription net of discounts, recognised over time) |
| **Bookings** | New contract value signed | Pre-recognition |
| **Deferred revenue** | Cash received before service delivered | Balance sheet liability under ASC 606 / IFRS 15 |
| **RPO (Remaining Performance Obligations)** | Contractually committed future revenue | ASC 606 ¶54 / IFRS 15 ¶120 disclosure |
| **Customer churn / NRR (Net Revenue Retention)** | Customer departures and expansions | Drives expected customer life for commission amortisation |
| **CAC (Customer Acquisition Cost)** | Total sales+marketing ÷ new customers | Forms basis of LTV/CAC ratio |
| **LTV (Lifetime Value)** | Gross margin × expected customer life | Critical for impairment testing |

---

## Section 8 — Self-checks

- [ ] Revenue recognition timing matches IFRS 15 / ASC 606 — over time for hosted SaaS
- [ ] Implementation services tested for distinct PO status
- [ ] Setup fees combined or separated per distinct test
- [ ] Multi-year contracts allocated for ramps and discounts
- [ ] Customer acquisition costs capitalised and amortised per expected customer life
- [ ] US state sales tax registration where economic nexus thresholds met
- [ ] EU OSS / IOSS registration if cross-border B2C
- [ ] Non-EU VAT registration (UK, Australia, Canada, India OIDAR, Singapore, Japan, Korea, Mexico, Chile)
- [ ] DST exposure assessed per `digital-services-tax-matrix.md`
- [ ] PE risk assessed for any country with local employees / customer-facing roles
- [ ] Deferred revenue reconciled to bookings and contract value
- [ ] Output flags every [T2]/[T3] item for reviewer judgement

---

## Section 9 — Disclaimer

SaaS sector taxation involves substantial cross-border complexity. Outputs must be reviewed by credentialed practitioners. The most up-to-date version is at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/saas-digital-products) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
