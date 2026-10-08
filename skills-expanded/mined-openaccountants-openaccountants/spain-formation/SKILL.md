---
name: spain-formation
description: "> Use this skill whenever asked about forming, incorporating, or registering a company in Spain. Trigger on phrases like \"set up a company in Spain\", \"SL formation\", \"sociedad limitada\", \"Registro Mercantil\", \"Spanish company formation\", \"register a business Spain\", \"CIF Spain\", \"autónomo societario\", \"NIF\", \"escritura de constitución\", or any question about starting a business entity in Spain. Covers entity types (SL, SA, autónomo, sociedad civil), registration process, capital requirements, costs, post-formation compliance, and bank account opening. ALWAYS read this skill before advising on Spanish company formation."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: ES
  category: formation
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/spain-formation"
  obligation: FORM
---

# Spain Company Formation Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | Spain (Kingdom of Spain) |
| Currency | EUR |
| Company registrar | Registro Mercantil (Provincial) + Registro Mercantil Central (name reservation) |
| Key legislation | Real Decreto Legislativo 1/2010 (Ley de Sociedades de Capital); Ley 18/2022 (Crea y Crece) |
| Typical formation time | 1--3 weeks (standard); 4--5 days (fast-track via PAE/CIRCE) |
| Corporate tax rate | 25% (standard); 15% (first 2 years with profits for new companies) |
| Skill version | 1.0 |

---

## Section 2 -- Entity Types Comparison

| Feature | Autónomo (Sole Trader) | S.L. (Sociedad Limitada) | S.L.U. (Unipersonal) | S.A. (Sociedad Anónima) |
|---|---|---|---|---|
| Legal personality | No | Yes | Yes | Yes |
| Liability | Unlimited | Limited to contributions | Limited | Limited |
| Min. founders | 1 | 1 (S.L.U.) or 2+ | 1 | 1 (non-listed) |
| Min. share capital | N/A | €1 (since Ley Crea y Crece 2022) | €1 | €60,000 |
| Recommended capital | N/A | €3,000 (avoid legal-reserve constraints) | €3,000 | €60,000 (25% paid up) |
| Tax treatment | IRPF (personal) | Impuesto sobre Sociedades | Impuesto sobre Sociedades | Impuesto sobre Sociedades |
| Admin burden | Low | Medium | Medium | High |
| Audit required | No | Only if thresholds exceeded | Only if thresholds exceeded | Yes (if thresholds exceeded) |

**Recommended default:** S.L. (Sociedad Limitada) with €3,000 capital for most commercial purposes.

**Note on €1 capital:** Since the Ley Crea y Crece (Ley 18/2022, 28 September 2022), the legal minimum capital for an S.L. is €1. However, if capital is below €3,000, special rules apply: 20% of profits must be allocated to legal reserves until reserves reach €3,000, and directors are jointly liable with the company for debts if the company is wound up with insufficient assets.

---

## Section 3 -- Registration Process

### Step 1: Reserve Company Name (Certificación Negativa de Denominación)
- Apply to Registro Mercantil Central (rmc.es)
- Up to 5 name proposals
- Cost: ~€16--€22; processing: 1--3 working days
- Valid for 6 months (renewable for 3 more)

### Step 2: Open Bank Account and Deposit Capital
- Open account in the name of "sociedad en constitución"
- Deposit share capital (min. €1; recommended €3,000)
- Obtain certificado de ingreso (bank certificate) for notary

### Step 3: Draft Estatutos Sociales (Articles of Association)
- Include: company name, registered office, objects, capital, share distribution, governance structure
- Can use standard or custom estatutos

### Step 4: Sign Escritura de Constitución Before Notary
- All founders must appear (or be represented by poder notarial)
- Bring: NIE/DNI, bank certificate, name certificate, estatutos
- Notary fee: €150--€600 depending on capital and complexity

### Step 5: Obtain CIF Provisional (Tax ID)
- Apply at Agencia Tributaria (AEAT) with Modelo 036
- Provisional CIF issued immediately; definitive CIF after Registro Mercantil registration

### Step 6: File with Registro Mercantil Provincial
- Submit escritura to the provincial mercantile registry
- Cost: €100--€400 depending on capital and region
- Processing: 5--15 working days
- Company legally exists upon registration

### Step 7: Register for Taxes and Social Security
- Modelo 036: register for Impuesto sobre Sociedades and IVA with AEAT
- Autónomo societario: the administrador must register with Seguridad Social (~€370/month in 2026)
- Register as employer with Tesorería General de la Seguridad Social (if hiring)

---

## Section 4 -- Capital Requirements

| Entity Type | Min. Share Capital | Min. Paid-Up | Payment Timing | In-Kind Contributions |
|---|---|---|---|---|
| S.L. | €1 (legal min. since 2022) | 100% of subscribed capital | At constitution | Permitted (founders liable for valuation accuracy for 5 years) |
| S.L. (recommended) | €3,000 | 100% | At constitution | Permitted |
| S.A. | €60,000 | 25% (€15,000) | At constitution | Permitted (independent expert report required) |

---

## Section 5 -- Costs Breakdown

| Cost Component | Amount (EUR) | Notes |
|---|---|---|
| Certificación negativa (name) | ~€16 | Registro Mercantil Central |
| Notary fees | €150--€600 | Scales with capital amount |
| Registro Mercantil Provincial | €100--€400 | Registration of escritura |
| AEAT registration (CIF) | Free | Modelo 036 |
| Share capital deposit | €3,000 (recommended) | Minimum €1 |
| **Total government/notary fees** | **€270--€1,000** | Excluding capital |
| Gestoría / legal fees (optional) | €300--€1,200 | Full formation service |
| **Total with professional help** | **€600--€2,200** | Excluding capital |

### Annual Maintenance

| Item | Cost (EUR) |
|---|---|
| Autónomo societario (administrador) | ~€370/month (~€4,440/year) |
| Asesoría fiscal / gestoría | €100--€300/month |
| Registro Mercantil (cuentas anuales deposit) | ~€40--€80 |
| Impuesto sobre Actividades Económicas (IAE) | Exempt if turnover < €1M |

---

## Section 6 -- Post-Formation Compliance

| Obligation | Deadline | Authority |
|---|---|---|
| Cuentas anuales (annual accounts) | Approve within 6 months of year-end; deposit within 1 month of approval | Registro Mercantil |
| Impuesto sobre Sociedades (corporate tax) | 25 July (for calendar year-end) | AEAT |
| IVA declarations | Quarterly (Modelo 303) + annual summary (Modelo 390) | AEAT |
| Retenciones (withholding returns) | Quarterly (Modelo 111 for salaries; Modelo 115 for rent) | AEAT |
| Titularidad real (UBO register) | At constitution and on any change | Registro Mercantil |
| Legalización de libros (book legalisation) | Within 4 months of year-end | Registro Mercantil |

---

## Section 7 -- Bank Account Opening

### Documents Typically Required
- Escritura de constitución inscrita en Registro Mercantil (or provisional for opening)
- CIF / NIF
- NIE or DNI of all founders and directors
- Proof of address
- Business activity description

### Typical Timeline
- 1--5 days (digital banks)
- 1--3 weeks (traditional banks)

### Common Banks
- Santander, BBVA, CaixaBank, Sabadell (traditional)
- Qonto Spain, Revolut Business (digital)

---

## Section 8 -- Foreign Founder Considerations

| Question | Answer |
|---|---|
| Non-resident directors allowed? | Yes, but NIE (Número de Identidad de Extranjero) required |
| NIE for incorporation | Mandatory before notary appointment; obtainable at Spanish consulate or police station |
| Physical presence required? | Yes for notary (power of attorney possible but must be notarised and apostilled) |
| Apostille requirements | Foreign documents require apostille + sworn Spanish translation |
| Autónomo obligation | Foreign administradores must register as autónomo societario with Seguridad Social |
| EU/non-EU differences | EU citizens: simpler NIE process; non-EU: may need visa depending on activity |

---

## Section 9 -- Common Mistakes and Refusals

**R-ES-F1 -- Capital of €1 without understanding consequences.** "While €1 is the legal minimum since 2022, capitals below €3,000 trigger mandatory profit-reserve rules and potential joint director liability. Always advise on these constraints before proceeding."

**R-ES-F2 -- Forgetting autónomo societario obligation.** "The administrador of an S.L. must register as autónomo societario and pay social security contributions (~€370/month in 2026). This is a significant ongoing cost that founders frequently overlook."

**R-ES-F3 -- Not depositing annual accounts.** "Failure to deposit cuentas anuales with the Registro Mercantil results in the company being unable to file new deeds (cierre registral) and potential fines up to €60,000."

**R-ES-F4 -- NIE not obtained before notary appointment.** "All founders and directors must have a valid NIE before the notary can execute the escritura. This is the most common cause of delay for foreign founders."

**R-ES-F5 -- Shell company request.** "This skill will not assist in forming a company without genuine economic substance. Spanish anti-money-laundering regulations require identification of beneficial owners and real business activity."

---

## Section 10 -- Timeline

| Step | Duration | Cumulative |
|---|---|---|
| Obtain NIE (if foreign founder) | 1--6 weeks | Day 1--42 |
| Name reservation (certificación negativa) | 1--3 days | Day 2--45 |
| Draft estatutos and prepare documents | 1--3 days | Day 3--48 |
| Open bank account and deposit capital | 1--5 days | Day 4--53 |
| Notary appointment (escritura) | 1 day | Day 5--54 |
| CIF provisional (AEAT) | 1 day | Day 6--55 |
| Registro Mercantil registration | 5--15 days | Day 11--70 |
| Social security registration | 1--3 days | Day 12--73 |
| **Ready to trade** | | **~2--4 weeks (with NIE already in hand)** |

The bottleneck for foreign founders is obtaining the NIE, which should be started well in advance.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute legal, tax, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/spain-formation) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._
