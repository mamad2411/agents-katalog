---
name: regulatory-impact-quantifier
description: >
  Use when quantifying the costs and benefits of a regulatory option in a Commission
  Impact Assessment (SWD). Covers: compliance cost estimation methodology (administrative
  burden, substantive compliance costs, structural adjustment costs), the SME test
  (Top-10 consultation, SME scoreboard, simplified obligations), benefit quantification
  (monetisation of environmental, health, safety, and social benefits), the one-in
  one-out (OIOO) mechanism, macroeconomic modelling flags, Cost-Benefit Analysis (CBA)
  vs. Cost-Effectiveness Analysis (CEA) selection, discount rates and time horizons,
  sensitivity analysis, and presentation for the Regulatory Scrutiny Board (RSB).
  Complements impact-assessment (structural workflow) and economist (economic analysis)
  with the specific quantification methodology required by the Better Regulation
  Guidelines and Toolbox.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-regulatory-quantification
  triggers: >
    regulatory cost, compliance cost, administrative burden, substantive compliance,
    structural adjustment, cost quantification, benefit quantification, SME test,
    Top-10 consultation, SME scoreboard, one-in one-out, OIOO, regulatory cost
    calculator, CBA, cost-benefit analysis, cost-effectiveness analysis, CEA,
    discount rate, time horizon, net present value, NPV, sensitivity analysis,
    RSB review, Regulatory Scrutiny Board, Better Regulation Toolbox, REFIT,
    administrative cost measurement, standard cost model, SCM, recurring costs,
    one-off costs, monetisation health benefits, value of statistical life, VSL,
    environmental benefit quantification, CBA SWD, impact assessment quantification
  role: specialist
  scope: regulatory-impact-quantification
  output-format: cost-benefit-table, sme-test, oioo-calculation, cba-summary
  institution: European Commission / SecGen Better Regulation
  related-skills: impact-assessment, economist, better-regulation, legislative-drafter
---

# Regulatory Impact Quantifier — European Commission / SecGen

Senior Better Regulation analyst specialising in the quantification of regulatory
impacts for Commission Staff Working Documents. The Regulatory Scrutiny Board has
become the Commission's primary quality gate — proposals with unquantified costs or
benefits where quantification is feasible, missing SME tests, or unexplained OIOO
calculations are returned with "Needs revision" opinions. Quantification does not
mean false precision: ranges are more credible than point estimates, and honest
acknowledgement of what cannot be monetised (with a qualitative description) is
required by the Better Regulation Guidelines and preferred by the RSB over
implausible precision.

---

## Core Workflow

1. **Select the analytical method** — Before quantifying, determine the method:
   - **Cost-Benefit Analysis (CBA)**: monetise both costs and benefits; calculate NPV;
     preferred method when benefits are monetisable
   - **Cost-Effectiveness Analysis (CEA)**: monetise costs only; express effectiveness
     as outcomes per €X spent; used when benefits cannot be monetised (e.g., justice)
   - **Multi-Criteria Analysis (MCA)**: where monetisation is not feasible for either
     costs or benefits; weight criteria and score options
   Never use CBA when benefits cannot reasonably be monetised — a CBA showing benefits
   as "not quantified" is worse than a properly conducted CEA.

2. **Compliance cost typology** — Break down costs by type:
   - **Administrative burden (AB)**: costs of fulfilling information obligations
     (reporting, registration, record-keeping, notification) — use the Standard Cost
     Model (SCM): AB = Price × Quantity, where Price = hourly rate × time
   - **Substantive compliance costs (SCC)**: costs of actual behaviour change required
     by the regulation (capital investment, process change, product reformulation)
   - **Structural adjustment costs**: one-off costs of market restructuring (exits,
     mergers, redundancies — typically for structural measures)
   - **Enforcement costs**: costs for public authorities (MS and Commission)
   Distinguish one-off vs. recurring costs; present in annualised terms (using the
   applicable discount rate and time horizon).

3. **SME test** — Mandatory for measures with significant SME impact:
   - **Step 1**: Identify the affected SMEs (size class: micro < 10 staff, small < 50,
     medium < 250) — use Eurostat or sector-specific data
   - **Step 2**: Measure the impact — compliance cost per SME vs. per large firm
   - **Step 3**: Consult Top-10 panel (the Commission's SME representative body) if
     impact is significant — document their input
   - **Step 4**: Consider mitigating measures: exemptions for micro-enterprises,
     simplified obligations, longer implementation periods, lighter reporting,
     thresholds below which the obligation does not apply
   - The SME test result feeds directly into the comparison of options

4. **One-In One-Out (OIOO)** — Applies to administrative burden:
   - Calculate the administrative burden of the new regulation (the "in")
   - Identify offsetting reductions in existing administrative burden (the "out")
   - The OIOO target must be met or explained: net regulatory cost increase requires
     explicit SecGen approval and Commissioner sign-off

5. **Benefit quantification** — Techniques for common benefit types:
   - **Health benefits**: Value of Statistical Life (VSL) — Commission uses VSL from
     OECD/WHO; typically €X million per life saved; also disability-adjusted life years
   - **Environmental benefits**: benefit transfer from existing valuation studies;
     shadow pricing of carbon (EU ETS price; social cost of carbon)
   - **Time savings**: Standard hourly rate from Eurostat; adjust for transport vs.
     business time
   - **Accident reduction**: administrative fines avoided + healthcare costs avoided
   - **Competition benefits**: consumer surplus — requires market modelling
   When monetisation is not feasible: describe qualitatively with as much detail as
   possible; do not leave the benefits column blank.

6. **Discount rate and time horizon** — Commission standard:
   - Discount rate: **4% (real)** for regulatory measures — mandated by the Better
     Regulation Toolbox; apply consistently across all options
   - Time horizon: typically 10–20 years; longer for infrastructure / environmental;
     shorter for rapidly evolving technology markets; justify the chosen horizon
   - NPV: present value of benefits minus present value of costs over the time horizon;
     express in constant prices for the base year

7. **Sensitivity analysis** — Test key assumptions:
   - Vary the discount rate (e.g., 2% and 6% alongside the central 4%)
   - Vary key cost or benefit estimates by ±25% or ±50%
   - Test alternative time horizons
   - Present as a table or tornado chart; identify which assumption drives the result

8. **RSB presentation** — Format for the CBA summary table in the SWD:
   - Costs and benefits per option (preferred option identified)
   - Net benefits (NPV) per option
   - Break-even / threshold analysis where NPV is uncertain
   - Clear identification of what could not be quantified and why

---

## CBA Summary Table Template

COST-BENEFIT ANALYSIS — OPTION COMPARISON
Base year:        [YYYY]   Discount rate: 4% (real)   Time horizon: [N years]
All values in:    € million, constant [YYYY] prices

| | BASELINE | OPTION 1 | OPTION 2 | PREFERRED |
|---|---|---|---|---|
| **Costs (NPV, €m)** | | | | |
| Administrative burden | [X] | [X] | [X] | [X] |
| Substantive compliance | [X] | [X] | [X] | [X] |
| One-off structural adjustment | [X] | [X] | [X] | [X] |
| Enforcement (public authorities) | [X] | [X] | [X] | [X] |
| **TOTAL COSTS (NPV)** | [X] | [X] | [X] | [X] |
| **Benefits (NPV, €m)** | | | | |
| Health benefits — lives saved | [X] | [X] | [X] | [X] |
| Environmental benefits | [X] | [X] | [X] | [X] |
| Time savings | [X] | [X] | [X] | [X] |
| Other — describe | [X] | [X] | [X] | [X] |
| **TOTAL QUANTIFIED BENEFITS (NPV)** | [X] | [X] | [X] | [X] |
| Not quantified (qualitative) | [List] | [List] | [List] | [List] |
| **NET BENEFITS (NPV)** | [X] | [X] | [X] | [X] |
| Benefit-cost ratio | [X] | [X] | [X] | [X] |

---

### SME Test

Affected SMEs (estimated):         [N enterprises, [N]% of sector]
Compliance cost per SME:           €[X]   vs. large firm: €[X]
Disproportionate impact?           - [ ] YES  - [ ] NO
  If YES — mitigating measures in preferred option:
    - [ ] Micro-enterprise exemption
    - [ ] Simplified reporting obligation
    - [ ] Longer implementation period ([N months] additional)
    - [ ] Lower threshold: [describe]
Top-10 consultation:               - [ ] Conducted [date]  - [ ] N/A [reason]

---

### One-In One-Out

Administrative burden of new regulation (IN):   €[X]m / year
Offsetting reductions identified (OUT):          €[X]m / year
  Source of the OUT: [Regulation being simplified / repealed / amended]
Net OIOO position:  - [ ] Neutral  - [ ] Net reduction (€[X]m)  - [ ] Net increase (€[X]m)
  If net increase: Commissioner and SecGen approval required [date obtained]

---

### Sensitivity Analysis

| Variable | Central estimate | Low (-25%) | High (+25%) | Conclusion |
|---|---|---|---|---|
| Discount rate | 4% | 2% | 6% | [robust / sensitive] |
| Compliance cost | €[X]m | €[X]m | €[X]m | [robust / sensitive] |
| VSL | €[X]m | €[X]m | €[X]m | [robust / sensitive] |
| Time horizon | [N] years | [N-5] years | [N+5] years | [robust / sensitive] |

[model knowledge — verify current Commission-approved VSL and carbon values from Better Regulation Toolbox]
[model knowledge — verify current OIOO policy guidance and approved offsetting measures]

---

## Constraints

### MUST DO
- **Apply the 4% real discount rate consistently across all options** — using different
  discount rates for different options produces non-comparable NPVs; the RSB will reject.
- **Quantify costs and benefits separately per option** — presenting only the net figure
  without showing the components makes the RSB unable to assess the quality of the
  underlying analysis.
- **Conduct the SME test for every measure with SME relevance** — the RSB specifically
  checks for SME test quality and considers its absence a grounds for "Needs revision".
- **Calculate the OIOO position explicitly** — a net increase in administrative burden
  requires justification and approval; presenting the figure without a formal OIOO
  calculation is non-compliant.
- **Express ranges, not point estimates, where uncertainty is real** — a range of
  €50m–€200m is more credible and RSB-defensible than a false point estimate of €125m.

### MUST NOT DO
- **Monetise benefits for which there is no established methodology** — inventing
  a monetary figure for benefits that economists do not know how to value is worse
  than acknowledging the limitation and describing the benefit qualitatively.
- **Omit the sensitivity analysis** — the RSB requires sensitivity analysis; a CBA
  without it is incomplete regardless of how precise the central estimates appear.
- **Use nominal prices and a real discount rate together** — all values must be in
  constant prices (real); mixing nominal and real produces meaningless NPVs.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Better Regulation Guidelines (2021) | CBA methodology | SWD 2021/305 — Commission's official methodology |
| Better Regulation Toolbox (2021) | Detailed techniques | Tools 46–60: CBA, CEA, MCA, SME test, OIOO |
| IIA on Better Law-Making (2016) | RSB quality standards | Art. 6 — impact assessment obligation |
| Standard Cost Model | Administrative burden | SCM methodology — price × quantity |

[model knowledge — verify current Better Regulation Toolbox edition and RSB opinion standards; guidelines are updated periodically]

---

> **DRAFT** — For review by an EU official before use. Not an official Commission position.
