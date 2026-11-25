---
name: financial-relief
description: >
  Advise on and draft financial remedy applications under the Matrimonial Proceedings and Property Ordinance (Cap 192), including periodical payments, lump sum orders, property adjustment, and pension sharing.
---
# Financial Relief — Skill

## Purpose

Advise on and draft financial remedy applications under the Matrimonial Proceedings and Property Ordinance (Cap 192), including periodical payments, lump sum orders, property adjustment, and pension sharing.

## Scope

- Types of financial relief orders under Cap 192
- Statutory factors (s.7)
- Principles of distribution (needs, sharing, compensation)
- Matrimonial vs non-matrimonial property distinction
- Clean break and final orders
- Variation applications
- Consent orders

## Workflow

### 1. Initial Assessment

- Identify all financial resources of both parties:
  - Real property (HK and overseas)
  - Bank accounts, investments, securities
  - Business interests and shareholdings
  - Pension/MPF entitlements
  - Motor vehicles, jewellery, art
  - Trust assets
  - Inherited or expected inheritances
- Categorise assets as matrimonial or non-matrimonial
- Identify any dissipation of assets or non-disclosure concerns

### 2. Financial Disclosure

**Form E — Statement of Financial Position**:
- Full and frank disclosure required
- Includes all assets, income, liabilities, outgoings
- Sworn affidavit required
- Exchange within 35 days of directions (or as ordered)

**Further Disclosure**:
- Bank statements (usually 12 months)
- Business accounts (3 years)
- Property valuations
- Pension valuations
- If non-disclosure suspected: third-party disclosure orders, bank account tracing

### 3. Apply Statutory Factors (s.7, Cap 192)

| Factor | Consideration |
|--------|--------------|
| Resources | Income, earning capacity, property, financial resources of both parties |
| Needs | Financial needs, obligations, responsibilities of the parties |
| Standard of living | Pre-breakdown standard of living |
| Age and duration | Age of parties, length of marriage |
| Disability | Physical or mental disability of either party |
| Contributions | Financial and non-financial (including home and family care) |
| Conduct | Only if inequitable to disregard |
| Loss of benefit | Loss of pension rights or other benefits |

### 4. Three-Stage Analysis

**Stage 1: Needs**
- Primary consideration
- Based on housing, income to meet reasonable requirements
- Budget-driven assessment

**Stage 2: Sharing (long marriages)**
- Equal division of matrimonial assets
- Length of marriage is critical
- Short marriages (<3 years): sharing principle applies less often

**Stage 3: Compensation**
- Economic disadvantage from marriage roles
- Loss of career, pension, earning capacity
- Hard to establish in practice

### 5. Draft Orders

**Periodical Payments (s.5)**:
- Ongoing regular payments — secured or unsecured
- Tax consequences: payments are tax deductible for payer; taxable income for recipient (HK — no tax on spousal maintenance in most cases)

**Lump Sum Order (s.6)**:
- Single payment or instalments
- Can be used to adjust capital disparity
- Secured against property if needed

**Property Adjustment Order (s.6–7)**:
- Transfer of home to one party
- Settlement of property on trust
- Mesher order (deferred sale — e.g. until youngest child finishes education)
- Variation of settlements

**Pension Sharing (s.7A–7D)**:
- Applies to MPF and private pension schemes
- Sharing order requires actuarial valuation
- Offset against other assets also possible

**Sale of Property (s.8)**:
- Order for sale with division of proceeds
- Used where parties cannot agree

### 6. Clean Break

- Final settlement ending financial claims
- Achieved by: lump sum, property transfer, dismissal of claims
- Advantages: finality, no future litigation, emotional closure
- Consider: loss of variation rights, inheritance claims

### 7. Consent Orders

- Parties agree on terms and submit draft order for court approval
- Requires: draft order, statement of financial information, undertakings
- Court must be satisfied the order is fair — may request further evidence
- Binding once approved

### 8. Variation (s.11)

- Court may vary periodical payments and settlement orders
- Grounds: change of circumstances, new facts, order based on inaccurate information
- Remarriage: periodical payments to the recipient cease automatically
- Applications to vary should be supported by updated financial disclosure

### 9. Child Maintenance

- Applied under Child Maintenance Guidelines:
  - 1 child: 20% of net income
  - 2 children: 30% of net income
  - 3+ children: 40% of net income
- Court has discretion to depart from guidelines
- Maintainable until 18 (21 if in education)

### 10. Enforcement

- **Attachment of earnings** — deduction from wages
- **Charging order** — secured against property
- **Third-party debt order** — against bank or other
- **Committal** — imprisonment for wilful refusal to pay
- **Warrant of execution** — bailiff seizure of goods

## Key Sections

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.5 | Periodical payments | Ongoing spousal maintenance |
| s.6 | Lump sum orders | Single capital payment |
| s.6–7 | Property adjustment | Transfer, settlement, variation of settlements |
| s.7 | Statutory factors | Check list of considerations |
| s.7A–7D | Pension sharing | MPF and private pension division |
| s.11 | Variation | Changing existing orders |
| s.16–17 | Child maintenance | Guidelines percentage application |

## Case Law

| Case | Principle |
|------|-----------|
| **White v White** | Yardstick of equality; no discrimination against non-financial contributions |
| **Miller v Miller** | Three-stage approach: needs, sharing, compensation |
| **Chai v Chai** | Milburnie principle re long marriages; equal sharing of matrimonial assets |
| **NN v WH** | Non-matrimonial property distinction confirmed in HK |
| **KM v CG** | Clean break approach; duration of maintenance |

## Common Pitfalls

- **Incomplete disclosure**: Non-disclosure may lead to orders being set aside
- **Overlooking pensions**: MPF and occupational pensions must be valued
- **Ignoring tax consequences**: While HK has no spousal maintenance tax, overseas tax may apply to foreign assets
- **Conduct allegations**: Generally irrelevant unless egregious — focus on needs not blame
- **Consent orders without legal advice**: Ensure each party has independent advice

## Tools & Resources

- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 192, Cap 13, Cap 16
- Child Maintenance Guidelines (Judiciary)
- Form E — Statement of Financial Position
- Pension valuation calculators
- HK Family Court practice directions


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
