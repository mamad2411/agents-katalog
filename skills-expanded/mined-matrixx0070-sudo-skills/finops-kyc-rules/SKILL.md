---
name: finops-kyc-rules
version: 1.0.0
description: Apply KYC/AML risk-rating and acceptance rules to a structured customer profile — score risk factors, set the CDD tier, resolve screening hits, and produce an auditable accept / EDD / reject decision.
author: matrixx0070
tags: [kyc, aml, risk-rating, edd, cdd, screening, sanctions, pep, operations]
capabilities: []
---

# KYC Rules

## When to use
Use this to turn a completed customer profile into a decision — rate the money-laundering risk across the standard factor categories, set the due-diligence tier (simplified / standard / enhanced), disposition sanctions/PEP/adverse-media screening hits, and output an accept, EDD-required, or reject outcome with the rationale an auditor and MLRO can rely on.

**Not for:** extracting or verifying the underlying documents (use finops-kyc-doc-parse first) or running the screening engine itself. This *adjudicates* a profile whose data and screening results are already in hand.

## Method
1. **Confirm inputs are complete.** Decision point: if CDD is incomplete (missing UBO, expired ID, unresolved doc exception), you cannot rate — return "pending information," don't guess a rating.
2. **Score each risk category:** customer type, geography, product/service, channel, and behavior/transaction profile. Assign each a level (low/medium/high) with the reason.
3. **Apply mandatory escalators.** Certain factors force high risk regardless of the composite: sanctions nexus, PEP status, high-risk jurisdiction, cash-intensive or shell-company traits.
4. **Compute the composite rating.** Combine categories per the methodology (weighted or highest-wins for escalators). Decision point: any hard escalator overrides a low composite.
5. **Set the CDD tier.** Low → simplified (where permitted); standard → standard CDD; high → Enhanced Due Diligence (source of wealth/funds, senior sign-off, tighter review cycle).
6. **Disposition screening hits.** For each sanctions/PEP/adverse-media hit, decide true match / false positive / needs-review using identifiers (name, DOB, nationality, entity number); a true sanctions match is a hard stop.
7. **Decide and record.** Output accept / accept-with-EDD / reject / escalate-to-MLRO, the driving factors, required ongoing-monitoring frequency, and next review date — fully evidenced.

## Example
Profile: private investment company, incorporated in a low-risk jurisdiction, but one UBO is a foreign senior government official (PEP) resident in a higher-risk country; product is a pooled fund subscription; channel is non-face-to-face via an introducer. Scoring: customer type medium, geography high (UBO residence), product low, channel medium (non-F2F), behavior unknown-new. Escalator: PEP → forces high risk. Composite: HIGH. Tier: EDD — obtain source of wealth for the PEP, senior management approval, enhanced ongoing monitoring, 12-month review shortened to 6. Screening: PEP hit confirmed true (matches DOB/role); no sanctions hit; one adverse-media article resolved as a different individual (DOB mismatch) → false positive. Decision: accept with EDD, MLRO sign-off obtained, next review 6 months.

## Pitfalls
- **Averaging away an escalator.** A sanctions nexus, PEP, or high-risk-country factor forces high risk; a weighted average that dilutes it to "medium" is a methodology failure.
- **Clearing a screening hit without identifiers.** Dismissing a name match as a false positive without checking DOB/nationality/entity number is how a true match slips through; document the discriminating data.
- **Rating on incomplete CDD.** No UBO or an expired ID means you don't have the facts to rate — pend, don't approve on assumptions.
- **Static risk rating.** Risk is not set-and-forget; a customer's rating and monitoring must update on trigger events (new adverse media, ownership change, unusual activity) and at the scheduled review.
- **Simplified CDD where prohibited.** SDD is only allowed for demonstrably low-risk cases and never where any high-risk factor or escalator is present.

## Output format
```
Customer: <name/id> | Type: <individual/entity> | CDD complete: Y/N
Risk factor scoring:
  | category | level | rationale |
  customer type | ... | ...
  geography     | ... | ...
  product       | ... | ...
  channel       | ... | ...
  behavior/txn  | ... | ...
Escalators triggered: <sanctions / PEP / high-risk country / shell / cash> 
Composite rating: LOW / MEDIUM / HIGH
CDD tier: simplified / standard / enhanced (EDD)
Screening dispositions:
  | hit | type (sanctions/PEP/adverse) | match/false-pos/review | discriminating data |
Decision: accept / accept-with-EDD / reject / escalate-MLRO
EDD actions required: <SoW/SoF, senior approval, ...>
Ongoing monitoring: frequency <> | next review: <date>
Sign-off: <analyst / MLRO / date>
```

## Reference

### The risk-based approach (RBA)
AML frameworks (FATF Recommendations, and their transposition such as the EU AMLDs and national rules) require a **risk-based approach**: assess each customer's ML/TF risk and apply due diligence proportionate to it. Higher risk → more scrutiny and enhanced measures; lower risk → simplified measures where permitted. The rating drives the CDD tier, the depth of verification, senior sign-off, and the ongoing-monitoring cadence.

### The five risk-factor categories
| Category | Higher-risk indicators |
|---|---|
| Customer type | PEP, complex/opaque ownership, shell/holding structures, cash-intensive business, bearer shares, nominee arrangements |
| Geography | Sanctioned or FATF grey/black-list jurisdictions, high-corruption or high-terrorism-finance countries, tax havens |
| Product/service | Private banking, correspondent banking, trade finance, crypto, anonymous or high-value products, cross-border |
| Channel | Non-face-to-face onboarding, introduced business, intermediaries, digital-only |
| Behavior/transaction | Unusual volume/pattern, activity inconsistent with profile, rapid movement, structuring |

### CDD tiers
- **Simplified (SDD):** reduced measures for proven low-risk customers (e.g., certain regulated entities, listed companies) — only where no high-risk factor is present and the regime permits it.
- **Standard (CDD):** identify and verify the customer and UBOs, understand the purpose and nature of the relationship, conduct ongoing monitoring.
- **Enhanced (EDD):** for high-risk customers — establish **source of funds** and **source of wealth**, obtain senior management approval, apply enhanced ongoing monitoring, and shorten the review cycle. Mandatory for PEPs and high-risk-jurisdiction nexus.

### PEPs, sanctions, and adverse media
- **PEP (Politically Exposed Person):** an individual entrusted with a prominent public function, plus their family members and close associates. Being a PEP is not itself wrongdoing but mandates EDD and senior approval due to corruption risk. Status can persist after leaving office (a risk-based, time-decaying assessment).
- **Sanctions:** a true match to a designated person/entity (OFAC SDN, UN, EU, UK OFSI, etc.) is a **hard stop** — you cannot onboard or transact and may have a reporting/freezing obligation.
- **Adverse media:** negative news (fraud, corruption, ML, terrorism) is a risk input; assess relevance, credibility, and recency and whether it is the same individual.

### Screening hit disposition
For each alert, compare discriminating identifiers — full name, date of birth, nationality, place of birth, entity registration number, and known aliases — against the customer. A **true match** on a sanctions list stops onboarding; a PEP true match triggers EDD; a **false positive** (e.g., DOB or nationality mismatch, different entity) is cleared *with the reason recorded*. Fuzzy name matches, transliterations, and common names produce most alerts; never clear one without documenting the data that resolved it.

### Ongoing monitoring and periodic review
KYC is dynamic. Transaction monitoring flags activity inconsistent with the expected profile; unusual activity may require enhanced review or a Suspicious Activity Report (SAR/STR) to the financial intelligence unit. Risk ratings are refreshed at a scheduled cadence (commonly annually for high risk, every 2–3 years for medium, longer for low) and on **trigger events** — ownership change, new adverse media, sanctions designation, or anomalous behavior. Records and rationale are retained (commonly 5 years post-relationship) and must be reproducible for audit and regulators.

### Governance and sign-off
High-risk acceptances and PEP relationships require senior management / MLRO approval. The MLRO (Money Laundering Reporting Officer) owns the AML program, the SAR decision, and escalation. Every decision — rating, tier, hit disposition, accept/reject — must be evidenced with the driving factors and the approver, so the file stands on its own for an examiner.
