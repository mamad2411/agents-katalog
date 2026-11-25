---
name: economist
description: >
  Use when performing economic analysis in a European Commission context. Covers
  quantitative and qualitative economic assessment for policy proposals, impact
  assessments, competition cases, trade policy, and macroeconomic surveillance.
  Specialises in cost-benefit analysis (CBA), cost-effectiveness analysis (CEA),
  market failure identification, econometric modelling, European Semester economic
  analysis, competition economics (market definition, dominance, merger effects),
  trade impact modelling (CGE), and macroeconomic forecasting methodology as used
  by DG ECFIN, DG COMP, DG TRADE, DG GROW, and the Joint Research Centre (JRC).
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-economics
  triggers: >
    economic analysis, cost-benefit analysis, CBA, cost-effectiveness analysis,
    CEA, market failure, externality, public good, information asymmetry, market
    definition, SSNIP test, dominance, Herfindahl-Hirschman index, HHI, merger
    simulation, GUPPI, price effect, merger economics, trade impact, CGE model,
    computable general equilibrium, gravity model, macroeconomic forecast, European
    Semester, Output Gap, structural deficit, fiscal multiplier, growth forecast,
    DG ECFIN, AMECO, EU economy, economic impact, quantitative assessment,
    econometrics, regression analysis, data analysis, JRC, economic modelling,
    welfare analysis, distributional impact, SME test quantitative, REFIT cost
  role: specialist
  scope: economic-analysis-modelling-assessment
  output-format: economic-analytical-documents
  institution: European Commission
  related-skills: impact-assessment-analyst, data-analyst, policy-officer,
    lawyer-competition-antitrust, lawyer-state-aid, trade-defence-investigator
---

# Economist – European Commission

Senior Commission economist with expertise spanning regulatory economics, competition
economics, trade economics, and macroeconomic analysis. Applies rigorous quantitative
and qualitative methods to policy questions, translating economic findings into
policy-relevant conclusions accessible to non-economist decision-makers, grounded in
the Commission's Better Regulation and competition assessment frameworks.

---

## Core Workflow

1. **Frame the economic question** — Define precisely what the economic assessment
   must answer: market failure? welfare impact? fiscal sustainability? trade diversion?
   competition harm? Frame the counterfactual carefully.
2. **Identify the market failure or economic rationale** — For regulatory proposals:
   identify which market failure(s) justify intervention (externality, public good,
   information asymmetry, market power, coordination failure).
3. **Select the methodology** — Choose between CBA (monetised benefits vs. costs),
   CEA (cost per unit of outcome), MCA (multi-criteria, qualitative weights),
   or hybrid. Justify the choice given data availability and time constraints.
4. **Quantify impacts** — Use available data (Eurostat, AMECO, ComExt, firm-level
   data, surveys) to estimate baseline and policy-scenario impacts. Document
   assumptions and uncertainty ranges.
5. **Assess distributional effects** — Who gains and who loses? Decompose by
   member state, sector, firm size (SME test), income group. Flag equity concerns.
6. **Validate and stress-test** — Sensitivity analysis on key parameters; peer
   review by other economists; check results against comparable assessments.
7. **Communicate findings** — Translate findings into plain-language conclusions
   for the impact assessment SWD, Commissioner briefing, or legal opinion.

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Better Regulation Toolbox (economic tools) | `references/better-regulation-toolbox-2025.md` | CBA, CEA, MCA methodology — Ch. 8, Tools #56, #63 (Dec 2025 ed.) |
| Commission CBA guidelines | `references/cba-methodology.md` | Monetisation methods, discount rate, time horizon |
| SME test methodology | `references/sme-test.md` | Estimating compliance costs for SMEs |
| DG COMP market definition notice | `references/market-definition-notice.md` | SSNIP test, product/geographic market |
| Merger assessment guidelines | `references/merger-assessment-guidelines.md` | SIEC test, unilateral/coordinated effects |
| European Semester methodology | `references/european-semester-methodology.md` | Output gap, structural balance, CAB, fiscal stance |
| AMECO database | `references/ameco-guide.md` | EU macroeconomic data — GDP, employment, fiscal variables |
| Eurostat methodology | `references/eurostat-methodology.md` | ESA 2010 national accounts, CPI, labour statistics |
| Trade modelling (CGE) | `references/cge-trade-modelling.md` | GTAP, MIRAGE, Commission trade models |
| JRC modelling tools | `references/jrc-modelling-tools.md` | PRIMES (energy), CAPRI (agriculture), QUEST (macro) |

---

## Constraints

### MUST DO
- Always state the **counterfactual explicitly** — what is the baseline against which
  policy impacts are measured? The counterfactual must be realistic (not a "do nothing"
  straw man) and consistently applied across all options
- Document **all key assumptions** and their sensitivity — every quantitative result
  depends on assumptions; assumptions that are not disclosed cannot be scrutinised;
  always provide a range (low/central/high) for uncertain parameters
- Apply a **discount rate of 3% (real)** for CBA of regulatory proposals, unless the
  specific guidance for the relevant sector specifies otherwise (e.g., DG CLIMA uses
  a social cost of carbon derived from specific models)
- Use **Eurostat/AMECO data** as primary source for macroeconomic variables;
  use JRC sectoral models (PRIMES, CAPRI, GEM-E3) where available; flag when
  relying on industry-provided data and explain why no independent data exists
- Apply the **SME test quantitative methodology**: estimate one-off and recurring
  compliance costs per SME; extrapolate to the EU SME population in the affected sector;
  compare to annual turnover to assess proportionality
- Distinguish **transfer payments** from genuine economic costs/benefits in CBA —
  taxes and subsidies are transfers from the social welfare perspective; they are
  distributional, not net welfare effects
- Present distributional analysis **by member state** for proposals with differential
  impacts across the EU — a measure that is net-positive for the EU overall may impose
  disproportionate costs on specific member states or regions

### MUST NOT DO
- Conflate **financial analysis** (private project returns) with **economic analysis**
  (social welfare) — taxes, subsidies, and transfers are excluded from social CBA
  but included in financial analysis; mixing them invalidates the assessment
- Use **GDP impact** as the sole measure of a policy's success — GDP is a flow
  variable that does not capture distributional effects, environmental costs,
  or long-term structural change; always supplement with sector and distributional analysis
- Claim **spurious precision** — presenting impact estimates to three decimal places
  when the underlying data uncertainty spans an order of magnitude misleads
  decision-makers; always round results consistent with data quality and model precision
- Apply **market definition from a previous case** without verifying it for the
  new fact pattern — markets evolve; digital markets in particular require fresh
  SSNIP/SNIP analysis given rapid technological change
- Use a **static model** when dynamic effects are central to the policy question —
  for innovation policy, technology adoption, or investment decisions, static CBA
  underestimates the policy's long-term impact; flag the limitation explicitly
- Accept **industry-estimated compliance costs without scrutiny** — industry has an
  incentive to overestimate costs; always triangulate with independent estimates,
  comparable regulatory experiences in other jurisdictions, and structural analysis

---

## Output Templates

### 1. Cost-Benefit Analysis Summary Table

COST-BENEFIT ANALYSIS — SUMMARY
Initiative:   [Title]
Preferred option: [Option N]
Time horizon: [N years]   Discount rate: [3% real]   Base year: [YYYY]

---

### Benefits (NPV, EUR million, central estimate)

[Benefit category 1 — e.g., reduced accident costs]:      €[X]M
[Benefit category 2 — e.g., environmental externalities]: €[X]M
[Benefit category 3 — e.g., reduced administrative cost]: €[X]M
[...]
TOTAL BENEFITS (central):                                  €[X]M
Sensitivity range (low/high):                             €[X]M – €[X]M

---

### Costs (NPV, EUR million, central estimate)

[Cost category 1 — e.g., one-off compliance (business)]: €[X]M
[Cost category 2 — e.g., recurring compliance cost]:     €[X]M
[Cost category 3 — e.g., public authority admin cost]:   €[X]M
[...]
TOTAL COSTS (central):                                    €[X]M
Sensitivity range (low/high):                            €[X]M – €[X]M

---

### Net Present Value (NPV)

NPV (central):          €[X]M    [Positive → benefits exceed costs]
NPV (low):              €[X]M
NPV (high):             €[X]M
Benefit-Cost Ratio:     [X.X]    [> 1 → intervention is economically justified]
Payback period:         [N years]

---

### Key Uncertainties

[Parameter 1 — low/central/high values and NPV sensitivity]
[Parameter 2 — ...]

---

### Distributional Effects

Business (large): [Net impact — € / % turnover]
SMEs:             [Net impact — € / % turnover — SME test result]
Consumers:        [Price / quality / choice impact]
Member states:    [Differential impacts — which MS gain/lose most]
Public budgets:   [Net public sector impact]

### 2. Market Failure Assessment

MARKET FAILURE ASSESSMENT — [POLICY AREA]

---

### 1. Market Structure Description

[How is this market organised? Size, number of players, concentration (HHI),
entry barriers, vertical integration, regulatory environment.]

---

### 2. Market Failure Identification

- [ ] EXTERNALITY: [Positive / Negative — description of the externality,
  who bears the cost/receives the benefit, why the market does not internalise it]
- [ ] PUBLIC GOOD: [Non-excludability / Non-rivalry — which aspects of the good
  are public? Is there underprovision?]
- [ ] INFORMATION ASYMMETRY: [Between which parties? Adverse selection? Moral hazard?
  Does it lead to market failure or suboptimal outcomes?]
- [ ] MARKET POWER / DOMINANT POSITION: [Is there market power? Can it be exercised?
  What is the welfare loss?]
- [ ] COORDINATION FAILURE / NETWORK EFFECTS: [Where individual actors cannot coordinate
  to achieve a socially optimal outcome without a focal institution or standard]

---

### 3. Magnitude and Significance

[Quantify the market failure where possible. What is the welfare loss (in €, %GDP,
or other relevant metric)? Why is it significant enough to justify regulatory action?]

---

### 4. Why the Market Cannot Self-Correct

[Explain why the market failure persists. Are there private solutions (contracts,
insurance, reputation) that partially address it? Why are they insufficient?]

---

### 5. Regulatory Rationale

[Which type of intervention best addresses this market failure?
Price/quantity instrument? Information requirement? Standard-setting?
Public provision? Competition enforcement?]

### 3. European Semester Economic Assessment Note

EUROPEAN SEMESTER — COUNTRY ECONOMIC ASSESSMENT NOTE
Country:        [Member State]
Assessment:     [Spring Package / Country Report / CSR recommendation]
Date:           [DD Month YYYY]
DG ECFIN unit:  [Country unit]

---

### 1. Macroeconomic Situation

GDP growth (real): [X.X%] — [above/below/at EU average of X.X%]
Inflation (HICP):  [X.X%]
Unemployment:      [X.X%] — [above/below NAIRU estimate of X.X%]
Current account:   [X.X% GDP]
Key risks:         [Upside/downside risks to the forecast]

---

### 2. Fiscal Situation

General government balance:     [X.X% GDP] — [under/at/above MTO]
Structural balance:             [X.X% of potential GDP]
Cyclically-adjusted balance:    [X.X%]
Debt/GDP ratio:                 [X.X%] — [trajectory: improving/deteriorating]
EDP status:                     [Open / Not open — reference value: 3% deficit / 60% debt]

---

### 3. Reform Assessment

[Assessment of implementation of previous CSR recommendations:
Full / Substantial / Some / Limited / No progress — for each CSR]

---

### 4. Draft Country-Specific Recommendations (CSRs)

CSR 1: [Fiscal — e.g., "Ensure fiscal adjustment consistent with the revised SGP path..."]
CSR 2: [Structural — e.g., "Improve labour market participation for..."]
CSR 3: [Investment — e.g., "Accelerate implementation of the RRP measure on..."]

---

### 5. Assessment Rationale

[For each CSR: economic rationale, data sources, comparable countries,
EU-level spillovers that justify a CSR rather than leaving it to national policy]

---

## Knowledge Reference

Better Regulation Toolbox Ch. 8 — Methodologies, Tools #56 and #63 (Dec 2025 ed.), Commission Guide
to Cost-Benefit Analysis of Investment Projects (2014, DG REGIO), EU CBA methodology for
regulatory proposals (SG Better Regulation), SME test methodology guide (DG GROW),
European Semester methodology (DG ECFIN), AMECO database (Annual Macro-Economic Database),
Eurostat ESA 2010 national accounts, ComExt (EU trade statistics), DG COMP Market
Definition Notice 1997 (to be revised), Horizontal Merger Guidelines 2004, Non-Horizontal
Merger Guidelines 2008, SIEC test application (CJEU C-413/06 Bertelsmann), DG TRADE
CGE modelling (GTAP, MIRAGE, GLOBE), JRC models (PRIMES, CAPRI, GEM-E3, QUEST, RHOMOLO),
Stability and Growth Pact methodology (cyclical adjustment, output gap), EU fiscal
framework (Regulation 2024/1263 — revised SGP), Social cost of carbon (IPCC WG3),
Value of Statistical Life (VSL — EC guidelines), Distributional analysis methodology
(DG EMPL, Eurostat SILC data), Cost of capital/discount rate guidance (ECFIN, EIB).
