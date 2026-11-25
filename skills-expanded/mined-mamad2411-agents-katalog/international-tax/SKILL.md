# international-tax

International tax structures — double taxation treaties, BEPS, Pillar 1/2.

## When to Activate

- Structuring cross-border investments to minimize withholding taxes
- Analyzing treaty eligibility and applying for treaty benefits
- Assessing BEPS exposure and compliance with anti-avoidance rules
- Evaluating Pillar 2 (global minimum tax) impact on group structures
- Reviewing CFC rules and their interaction with holding structures
- Advising on substance requirements for entities in low-tax jurisdictions
- Planning repatriation of profits (dividends, royalties, interest, management fees)

## Core Concepts

### Double Taxation Relief

Double taxation arises when the same income is taxed in two jurisdictions — residence state and source state. Relief mechanisms:

- **Credit method**: Residence state taxes worldwide income but allows a credit for tax paid in the source state, up to the domestic tax on that income. Excess credits may be carried forward
- **Exemption method**: Residence state exempts foreign-source income entirely (full exemption) or includes it only for rate-setting purposes (exemption with progression)
- **Deduction method**: Foreign tax treated as a deductible expense rather than a credit — less favorable, rarely used as primary method
- **Underlying tax credit**: Credit for corporate tax paid by a foreign subsidiary on profits out of which dividends are paid — increasingly rare as countries adopt participation exemptions

### Treaty Benefits

Tax treaties (bilateral agreements based on the OECD or UN Model) reduce source-state taxation:

- **Withholding tax (WHT) reduction**: Treaties typically reduce WHT on dividends (often 5-15%), interest (often 0-10%), and royalties (often 0-10%) versus domestic rates
- **Business profits (Article 7)**: Taxable in the source state only if attributable to a permanent establishment
- **Capital gains (Article 13)**: Generally taxable only in the residence state, except for gains from immovable property or PE assets
- **Limitation on Benefits (LOB)**: Anti-treaty-shopping provisions requiring active trade/business, ownership tests, or derivative benefits
- **Principal Purpose Test (PPT)**: BEPS Multilateral Instrument introduced this — denies treaty benefits if one of the principal purposes of an arrangement was to obtain the benefit

### BEPS Action Plans

The OECD/G20 BEPS project addresses tax planning strategies that exploit gaps and mismatches:

- **Action 1**: Tax challenges of the digital economy (now subsumed into Pillar 1/2)
- **Action 2**: Neutralize hybrid mismatch arrangements (deduction/no-inclusion, double deduction)
- **Action 3**: Strengthen CFC rules
- **Action 4**: Limit interest deductions (fixed ratio rule — 30% of EBITDA)
- **Action 5**: Counter harmful tax practices (substance requirements for preferential regimes)
- **Action 6**: Prevent treaty abuse (LOB, PPT)
- **Action 7**: Prevent artificial avoidance of PE status (commissionaire arrangements, contract splitting)
- **Actions 8-10**: Transfer pricing alignment with value creation
- **Action 13**: Country-by-Country Reporting
- **Action 14**: Improve dispute resolution (MAP)
- **Action 15**: Multilateral Instrument (MLI) — modifies bilateral treaties without renegotiation

### Pillar 1 — Reallocation of Profits

Reallocates a portion of residual profits of large multinationals to market jurisdictions:

- **Amount A**: Applies to groups with global revenue above EUR 20 billion and profitability above 10%. Allocates 25% of residual profits (above 10% margin) to market jurisdictions based on revenue
- **Amount B**: Standardized return for baseline marketing and distribution activities — simplifies transfer pricing for routine functions in market jurisdictions
- **Scope exclusions**: Extractive industries, regulated financial services

### Pillar 2 — Global Minimum Tax (15%)

Ensures large multinationals pay at least 15% effective tax in every jurisdiction:

- **Income Inclusion Rule (IIR)**: Parent jurisdiction tops up tax on low-taxed income of subsidiaries
- **Undertaxed Profits Rule (UTPR)**: Backstop — denies deductions if the ultimate parent does not apply IIR
- **Qualified Domestic Minimum Top-up Tax (QDMTT)**: Domestic law allowing the source jurisdiction to collect the top-up tax first
- **ETR calculation**: GloBE income divided by adjusted covered taxes — jurisdiction-by-jurisdiction, not entity-by-entity
- **Substance-based carve-out**: Excludes 5% of tangible asset carrying value and 5% of payroll cost (transitional rates higher, declining over 10 years)
- **Safe harbors**: Transitional CbCR safe harbor — no top-up tax if simplified ETR is above 15%, or revenue and profit are below de minimis thresholds

### CFC Rules

Controlled Foreign Company rules attribute passive or low-taxed income of foreign subsidiaries to the parent jurisdiction:

- **Control test**: Typically more than 50% ownership (votes or value); some jurisdictions use 25% or significant influence
- **Income test**: Passive income (dividends, interest, royalties, capital gains) or income taxed below a threshold
- **Exemptions**: Active business income, high-tax exclusion, treaty protection (limited)
- **Interaction with Pillar 2**: CFC taxes are included in adjusted covered taxes for GloBE ETR purposes

### Substance Requirements

Tax structures require genuine economic substance to be respected:

- **OECD BEPS Action 5**: Substantial activity requirement for preferential regimes (nexus approach for IP)
- **EU Anti-Tax Avoidance Directive (ATAD)**: Substance requirements; EU list of non-cooperative jurisdictions requires substance
- **Key substance indicators**: Qualified employees, office space, local decision-making, board meetings in jurisdiction, operational expenditure
- **Economic substance legislation**: Cayman Islands, BVI, Jersey, Guernsey, and others enacted domestic substance requirements

## Methodology

1. **Group structure mapping**: Chart legal entities, jurisdictions, ownership chains, and intercompany flows (dividends, interest, royalties, management fees)
2. **Treaty network analysis**: For each flow, identify available treaty benefits, applicable WHT rates, LOB/PPT implications
3. **BEPS risk assessment**: Screen for hybrid mismatches, interest deduction limitations, PE exposure, CFC triggers
4. **Pillar 2 impact modeling**: Calculate GloBE ETR by jurisdiction, identify top-up tax exposure, evaluate QDMTT adoption
5. **Substance review**: Assess whether each entity meets substance requirements — employees, premises, decision-making
6. **Structure optimization**: Propose restructuring to reduce WHT leakage, improve treaty access, and ensure Pillar 2 compliance
7. **Implementation and monitoring**: Execute restructuring steps; monitor for legislative changes, treaty renegotiations, and Pillar 2 developments

## Templates

### Withholding Tax Matrix

```
Flow                 | From     | To       | Domestic WHT | Treaty WHT | Conditions
---------------------|----------|----------|-------------|------------|------------------
Dividends            | Germany  | NL Hold  | 26.375%     | 5%         | >10% ownership
Interest             | France   | UK FinCo | 25%         | 0%         | Beneficial owner
Royalties            | Japan    | Ireland  | 20%         | 10%        | LOB satisfied
Management fees      | India    | Singapore| 10% (FTS)   | Nil*       | No FTS article
Dividends            | US       | LuxCo    | 30%         | 5%         | LOB active trade

Total annual WHT cost: EUR [X]M
Savings via treaty planning: EUR [Y]M
```

### Pillar 2 — GloBE ETR by Jurisdiction

```
Jurisdiction | GloBE Income | Adjusted Taxes | GloBE ETR | Top-Up Tax | QDMTT?
             | (EUR M)      | (EUR M)        |           | (EUR M)    |
-------------|-------------|----------------|-----------|------------|--------
Ireland      | 50          | 6.25           | 12.5%     | 1.25       | Yes
Singapore    | 30          | 5.1            | 17.0%     | Nil        | N/A
Luxembourg   | 20          | 5.0            | 25.0%     | Nil        | N/A
Cayman       | 15          | 0              | 0%        | 2.25       | Yes (pending)
Netherlands  | 80          | 20.0           | 25.0%     | Nil        | N/A

Substance carve-out applied: Tangible assets and payroll deductions reduce top-up in Ireland by EUR 0.3M
```

### CFC Screening Matrix

```
Subsidiary         | Jurisdiction | Local Tax Rate | Passive Income % | CFC Trigger? | Action
-------------------|-------------|----------------|-----------------|--------------|--------
IP HoldCo          | Ireland     | 12.5%          | 80% (royalties) | Yes          | Review exemptions
Treasury Co        | Luxembourg  | 24.9%          | 100% (interest) | No (high tax)| Monitor
Sales Sub          | Singapore   | 17%            | 5%              | No           | None
Dormant entity     | BVI         | 0%             | 100%            | Yes          | Liquidate or redomicile
```

## Quality Gate

- [ ] Group structure chart current, showing all entities, jurisdictions, and intercompany flows
- [ ] Treaty eligibility confirmed for each flow — LOB/PPT analysis documented
- [ ] Withholding tax rates applied are treaty-compliant and supported by certificates of residence
- [ ] BEPS risk areas reviewed: hybrid mismatches, interest limitation, PE exposure
- [ ] Pillar 2 GloBE ETR calculated for each jurisdiction; top-up tax exposure quantified
- [ ] QDMTT legislation tracked in jurisdictions where the group has low-taxed entities
- [ ] CFC rules analyzed in all parent jurisdictions; passive income attributed where required
- [ ] Substance requirements met in every jurisdiction — documented with employee lists, board minutes, lease agreements
- [ ] MLI positions reviewed for impact on existing treaty benefits
- [ ] Tax authority rulings obtained where appropriate (e.g., advance rulings on PE, WHT, CFC exemption)
- [ ] Annual review mechanism in place to capture legislative changes and treaty amendments
