---
name: real-estate-analyzer
description: Coordinate real estate investment screening, underwriting, pro formas, financing comparisons, tax and legal issue spotting, stress tests, syndication analysis, hospitality analysis, and international risk assessment. Use when a user asks to analyze a property or deal, build an investment model, compare financing, review investment documents, or evaluate cap rate, NOI, cash-on-cash return, DSCR, IRR, RevPAR, a 1031 exchange, a syndication, or cross-border real estate.
---

# Real Estate Investment Analyzer

Route each request to the smallest useful set of specialist agents, preserve a clear audit trail from source data to conclusions, and make uncertainty visible. For a full or mixed-scope deal, delegate first to the `orchestrator` agent provided by this plugin.

## Safety and data freshness

Real estate analysis can affect consequential financial, tax, and legal decisions.

- Treat rates, loan terms, rents, sale comparables, cap rates, vacancy, taxes, statutes, filing thresholds, ownership rules, permits, and incentives as time-sensitive.
- Research current values when they materially affect the answer. Prefer regulators, tax authorities, statutes, official statistics, lender term sheets, executed deal documents, and attributable market sources.
- Record each material source, its publication or effective date, and the retrieval date. Distinguish sourced facts, user inputs, estimates, and scenarios.
- Never reuse example values as market defaults. If a required input is missing, ask for it or provide a labeled range and sensitivity analysis.
- Do not present issue spotting as individualized legal, tax, accounting, lending, or investment advice. Identify questions for appropriately licensed professionals before commitment.
- Never fabricate a comparable, quote, sponsor record, permit, law, or source. Say when reliable evidence is unavailable.

## Data handling

- Collect and retain only what is necessary for the requested decision. Redact or
  omit tenant, investor, identity, and financial-account information unless it
  is necessary and the user is authorized to provide it.
- Do not send confidential deal materials to a third-party service, repository,
  API, or shared output without explicit authorization and a review of the
  service's terms and data handling.
- Never request or store credentials, passwords, government ID numbers, or full
  account details. Keep completed deal files in an authorized private location.
- Read [data-handling.md](references/data-handling.md) whenever a request uses
  confidential documents or external data services.

## Minimum deal inputs

Collect only what the analysis needs. Typical inputs are:

- property, location, asset type, strategy, and current stage;
- purchase price and total project cost;
- current or projected income, vacancy, operating expenses, and capital needs;
- financing amount, rate, term, amortization, fees, and recourse;
- ownership structure, investor terms, hold period, and exit assumptions;
- source documents such as listing details, rent roll, T-12, leases, loan quote, PPM, operating agreement, or development budget.

Proceed with partial information when useful, but label every gap and show which conclusion it could change.

## Routing

| Need | Delegate to | Output |
|---|---|---|
| Full or mixed-scope analysis | `orchestrator` | Sequenced analysis and investment memo |
| Fast preliminary screen | `deal-screener` | Pass, borderline, or fail with caveats |
| Detailed property economics | `property-underwriter` | NOI, cash flow, returns, and break-even analysis |
| Multi-year forecast | `pro-forma-builder` | Annual projections and exit sensitivities |
| Debt or capital comparison | `financing-analyzer` | Side-by-side financing economics |
| Tax issue spotting | `tax-strategist` | Potential treatments and questions for a tax adviser |
| Downside analysis | `stress-tester` | Base, downside, severe, and break-even cases |
| Fund, SPV, or passive deal | `syndication-analyzer` | Waterfall, fee, alignment, and protection analysis |
| Cross-border deal | `international-risk-assessor` | Ownership, currency, repatriation, and jurisdiction risks |
| Hotel, resort, or STR | `hospitality-underwriter` | ADR, occupancy, RevPAR, GOP, and ramp-up analysis |
| Contract or offering document | `legal-reviewer` | Red flags, missing terms, and counsel questions |

Use [data-sources.md](references/data-sources.md) only when a task needs market-data discovery, external data services, or batch screening patterns.

## Reproducible analysis assets

Use the assets in `templates/` when the user needs a reusable or auditable
deliverable:

- start with `templates/deal-intake.template.json` and record source status and
  dates in `templates/source-assumption-register.csv`;
- run the dependency-free calculator for a single-property, fixed-rate summary:
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/real_estate_calculations.py" <completed-intake.json>`;
- use `templates/real-estate-underwriting-template.xlsx` for an editable
  single-property workbook; and
- use the memo, risk, diligence, financing, and legal templates to preserve
  decisions, evidence gaps, and questions for qualified advisers.

The calculator does not validate market evidence, legal terms, tax treatment,
or lender eligibility. Inspect its JSON output against the source register and
do not use it as a substitute for a multi-period model where timing matters.

## Analysis sequence

1. Classify the request by asset, strategy, geography, stage, decision, and complexity.
2. Establish an as-of date and separate user-provided facts from externally verified facts.
3. Identify decision-critical gaps. Ask focused questions when a missing value would materially change the result.
4. Delegate to only the necessary specialists. Run independent analyses in parallel only when they do not depend on one another.
5. Reconcile units, currencies, time periods, definitions, and conflicting assumptions before combining outputs.
6. Recalculate important metrics from source inputs. Do not simply repeat sponsor or listing projections.
7. Compare a base case with at least one plausible downside. Add severe or break-even cases when leverage, construction, hospitality, lease-up, or currency risk is material.
8. Synthesize a decision-oriented memo with evidence, limitations, and next diligence actions.

## Calculation rules

- Show formulas or calculation logic for decision-critical outputs.
- Use consistent periods: monthly with monthly, annual with annual.
- Separate property-level returns from investor-level returns and pre-tax from after-tax estimates.
- Include acquisition costs, financing fees, reserves, capital expenditures, management, disposition costs, and waterfall economics when applicable.
- Do not compare an unlevered metric with a levered benchmark.
- For ranges, identify the low, base, and high inputs rather than reporting false precision.
- Treat rule-of-thumb thresholds as screening aids, not universal pass/fail standards.

## Final memo

Return the shortest format that supports the decision:

1. **Verdict** — proceed, proceed only if conditions are met, gather more evidence, or pass.
2. **Deal snapshot** — scope, as-of date, capital structure, and decision being evaluated.
3. **Key economics** — decision-critical metrics with formulas or traceable calculations.
4. **Scenarios** — base and downside results, plus break-even points where useful.
5. **Risks and red flags** — ranked by severity and likelihood, with mitigations.
6. **Evidence and assumptions** — sources with dates, user inputs, estimates, and unresolved gaps.
7. **Next diligence steps** — documents, quotes, inspections, and professional reviews required before commitment.

Use tables for comparisons, a spreadsheet for an interactive model, and a longer document only when the user asks for a deliverable.
