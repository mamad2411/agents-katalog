# AML/KYC Compliance

> Customer due diligence, suspicious activity reporting, PEP screening, sanctions — Anti-Money Laundering and Know Your Customer compliance.

## When to Activate

- Customer onboarding and KYC process design
- Risk classification of customers (CDD, EDD, SDD)
- PEP (Politically Exposed Persons) screening procedures
- Beneficial ownership identification and verification
- Suspicious transaction reporting (STR/SAR)
- Sanctions screening implementation
- Ongoing monitoring and periodic review design
- Travel rule compliance for fund transfers
- AML program assessment or audit preparation

## Core Concepts

### Customer Due Diligence Tiers

**Simplified Due Diligence (SDD)** — low-risk customers:
- Permitted only when ML/TF risk is demonstrably low
- Reduced identification requirements but identity must still be established
- Examples: regulated financial institutions, listed companies, government entities
- Still requires ongoing monitoring (at reduced frequency)

**Customer Due Diligence (CDD)** — standard tier:
- Identification and verification of customer identity (natural persons: name, DOB, address, ID document; legal entities: name, registration, registered address, directors)
- Identification of beneficial owners (typically > 25% ownership threshold)
- Understanding the purpose and intended nature of the business relationship
- Ongoing monitoring of transactions
- Must be completed before establishing business relationship

**Enhanced Due Diligence (EDD)** — high-risk situations:
- Mandatory for: PEPs, high-risk countries (FATF grey/black list), complex ownership structures, correspondent banking, unusual transaction patterns
- Additional measures: source of wealth, source of funds, senior management approval, enhanced ongoing monitoring, more frequent reviews

### Customer Risk Classification

**Risk factors to assess:**

| Category | Higher Risk Indicators |
|----------|----------------------|
| Customer type | Cash-intensive business, MSB, trust, shell company, PEP |
| Geography | FATF grey/black list, high corruption (CPI < 40), tax haven |
| Product/service | Private banking, correspondent banking, trade finance, crypto |
| Transaction | Unusual patterns, structuring, rapid movement of funds |
| Channel | Non-face-to-face, third-party introducers |

**Risk scoring model:**
- Assign risk weights to each factor category
- Score each factor (1 = low, 2 = medium, 3 = high)
- Weighted total determines overall risk tier
- Risk tier determines CDD level and review frequency

### PEP Screening

**PEP categories:**
- Heads of state, senior politicians, senior government officials
- Senior military officers, judiciary members
- Senior executives of state-owned enterprises
- Important political party officials
- Family members of PEPs (spouse, children, parents, siblings)
- Close associates of PEPs (known business partners, beneficial owners of entities jointly held)

**PEP handling:**
- All PEPs require EDD
- Senior management approval for relationship establishment and continuation
- Establish source of wealth and source of funds
- Enhanced ongoing monitoring
- PEP status does not automatically decline — risk-based approach applies
- De-PEP: After leaving office, typically 12-24 months continued EDD

### Beneficial Ownership

**Identification requirements:**
- Identify all natural persons who ultimately own or control > 25% of the entity (threshold varies by jurisdiction; EU: 25%, some jurisdictions: 10%)
- For complex structures: trace through multiple layers of ownership
- If no natural person identified above threshold: identify persons exercising control through other means
- Last resort: identify senior managing official

**Verification:**
- Corporate registry extracts, shareholder registers
- Annual returns, constitutional documents
- Trust deeds for trust structures
- Declarations from the customer, corroborated by independent sources

### Suspicious Transaction Reporting

**Red flags for suspicious activity:**
- Transactions inconsistent with customer profile or stated purpose
- Structuring (splitting transactions to avoid reporting thresholds)
- Rapid movement of funds with no apparent business rationale
- Transactions involving high-risk jurisdictions without business justification
- Reluctance to provide information, use of nominees
- Unusual cash transactions, round-amount transfers

**Reporting process:**
1. Front-line staff identifies unusual activity
2. Internal report to MLRO (Money Laundering Reporting Officer)
3. MLRO assesses and decides whether to file external report
4. STR/SAR filed with Financial Intelligence Unit (FIU) — in Germany: Zentralstelle für Finanztransaktionsuntersuchungen (FIU)
5. No tipping-off: Customer must not be informed about the report
6. Document retention: All records related to the STR for minimum 5 years

### Sanctions Screening

- Screen customers, beneficial owners, and counterparties against sanctions lists
- Key lists: UN, EU, OFAC (US), UK HMT, national lists
- Screen at onboarding, ongoing (batch screening), and per-transaction (real-time)
- Fuzzy matching for name variations, transliterations, aliases
- Disposition of hits: true match vs. false positive — document rationale
- Sanctions are absolute prohibitions (unlike AML, which is risk-based)

### EU AML Directives (5th and 6th AMLD)

**5th AMLD (effective 2020):**
- Beneficial ownership registers publicly accessible
- Crypto-asset providers brought into scope
- Prepaid card limits reduced (EUR 150 for anonymous use)
- Enhanced EDD for high-risk third countries
- Central bank account registries

**6th AMLD (effective 2021):**
- Harmonized list of 22 predicate offences including tax crimes and cybercrime
- Criminal liability for legal persons
- Extended aiding, abetting, inciting, and attempting
- Minimum 4-year imprisonment for ML offences
- Enhanced cooperation between FIUs

## Methodology

### AML Program Design

1. **Risk assessment**: Enterprise-wide ML/TF risk assessment covering customers, products, channels, geographies
2. **Policies and procedures**: Written AML/CFT policies approved by senior management
3. **Customer due diligence**: CDD/EDD/SDD procedures with clear escalation paths
4. **Transaction monitoring**: Rules-based and/or AI-based detection of suspicious patterns
5. **Screening**: Sanctions, PEP, and adverse media screening at onboarding and ongoing
6. **Reporting**: Internal escalation procedures and external STR/SAR filing
7. **Record keeping**: Minimum 5 years after end of business relationship
8. **Training**: Risk-based training program for all relevant staff
9. **Independent audit**: Regular independent review of AML program effectiveness
10. **Governance**: Designated MLRO with direct board access

### Ongoing Monitoring Design

- **Transaction monitoring rules**: Define scenarios (e.g., cash threshold, rapid movement, structuring patterns)
- **Periodic review frequency**: High risk — annually; Medium risk — every 2-3 years; Low risk — every 5 years
- **Trigger events**: Change in customer profile, adverse media, unusual transaction
- **Alert management**: Triage, investigation, escalation, disposition, documentation

## Templates

### Customer Risk Assessment

```
Customer: _______________     Date: ___________    Analyst: ___________

Risk Factor              Weight    Score (1-3)    Weighted Score
Customer type             25%        ____            ____
Geography                 25%        ____            ____
Product/service           20%        ____            ____
Transaction profile       15%        ____            ____
Channel                   15%        ____            ____
                                             Total: ____

Risk Tier: [ ] Low (SDD)  [ ] Medium (CDD)  [ ] High (EDD)
Review frequency: _______________
Approved by: _______________
```

### EDD Checklist

```
Customer: _______________     PEP: [ ] Yes [ ] No

[ ] Source of wealth documented and verified
[ ] Source of funds for the relationship documented
[ ] Senior management approval obtained
[ ] Enhanced transaction monitoring activated
[ ] Adverse media search completed — findings: _______________
[ ] Beneficial ownership verified through independent sources
[ ] Purpose of relationship clearly understood and documented
[ ] Review frequency set to: _______________
[ ] Next review date: _______________
```

## Quality Gate

- [ ] Enterprise-wide ML/TF risk assessment is current (updated annually)
- [ ] CDD tiers (SDD/CDD/EDD) are clearly defined with escalation criteria
- [ ] PEP screening covers family members and close associates
- [ ] Beneficial ownership is traced to natural persons above threshold
- [ ] Sanctions screening covers all relevant lists with fuzzy matching
- [ ] Transaction monitoring rules are calibrated (false positive rate managed)
- [ ] STR/SAR filing process ensures no tipping-off
- [ ] Record retention meets minimum 5-year requirement
- [ ] Staff training is risk-based and documented
- [ ] Independent audit of AML program performed regularly
