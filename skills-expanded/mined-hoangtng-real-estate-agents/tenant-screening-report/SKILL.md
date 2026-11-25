---
name: tenant-screening-report
description: Generate a tenant screening criteria document, application evaluation framework, or screening decision report for any rental property. Use this skill whenever a user asks how to screen tenants, whether to approve an applicant, what criteria to use for rental applications, how to write a denial letter, or how to stay fair-housing compliant during tenant selection. Also use when evaluating multiple applicants for one unit. Produces written screening criteria, an applicant evaluation scorecard, and adverse action notice templates.
---

# Tenant Screening Report

Produces consistent, documented, fair-housing-compliant tenant screening tools. This is Sandra's work: every applicant evaluated on the same written criteria, every decision documented, zero improvisation.

## What You Need From the User

- **Use case:** (a) create new screening criteria, (b) evaluate a specific applicant, or (c) compare multiple applicants
- **Property details:** rent amount, property type, any HOA restrictions
- **Applicant data (if evaluating):** income, credit score, rental history, employment, any red flags mentioned
- **State:** screening criteria have state-specific legal requirements

## ⚠️ Fair Housing Reminder (always display)

> Screening criteria must be applied **identically to every applicant**. Never adjust standards based on who is applying. Protected classes under federal Fair Housing Act: race, color, national origin, religion, sex, familial status, disability. Many states add: source of income, sexual orientation, gender identity, age, marital status. **When in doubt, document your reasoning and consult an attorney.**

## Output A: Written Screening Criteria Document

```markdown
## Rental Application Screening Criteria
**Property:** [Address] | **Monthly Rent:** $[X]
**Effective Date:** [Date]
*Applied consistently and equally to all applicants.*

---

### 1. Income
- **Minimum gross monthly income:** [X]× monthly rent (= $[X]/month)
- **Acceptable documentation:** 2 most recent pay stubs OR 2 months bank statements OR prior year tax return + YTD P&L (self-employed)
- **Multiple applicants:** combined household income evaluated

### 2. Credit
- **Minimum credit score:** [X]
- **Medical collections:** under $[X] acceptable with explanation; over $[X] disqualifying
- **Non-medical collections:** all require written explanation; pattern of collections = disqualifying
- **Prior evictions (unlawful detainer filing):** disqualifying within [X] years
- **Bankruptcy:** discharged [X]+ years ago with no subsequent derogatory marks: acceptable
- **No credit history:** acceptable with [X] months additional deposit OR qualified co-signer

### 3. Rental History
- **Required:** [X] years verifiable rental history (or homeownership)
- **Reference contacts:** all landlords from last [X] years contacted
- **Acceptable:** positive references + on-time rent payment history
- **Disqualifying:** prior eviction filing, substantiated lease violations, unpaid balances to prior landlords

### 4. Employment / Income Stability
- **Employed:** [X]+ months at current employer preferred; recent job change acceptable with explanation
- **Self-employed:** [X] years tax history required
- **Unemployed:** must demonstrate sufficient liquid assets to cover [X] months rent + deposit

### 5. Criminal History
*Evaluated per [State] law. Each case reviewed individually for: nature of offense, time elapsed, evidence of rehabilitation, relevance to tenancy.*
- Registered sex offenders: disqualifying
- [State/local specific rules here]
- Arrests without conviction: not considered

### 6. Application Process
- **Application fee:** $[X] (covers actual screening costs)
- **Processing time:** [X] business days from complete application
- **Co-signers:** accepted; must meet [X]× rent income requirement independently
- **All applicants notified** of decision in writing
- **Adverse action notice** sent with denial, including screening report source per FCRA

---

*These criteria are subject to change with notice. Exceptions to any criterion require written approval from [Owner/Property Manager] and must be documented.*
```

## Output B: Applicant Evaluation Scorecard

```markdown
## Applicant Evaluation: [Applicant Name(s)]
**Property:** [Address] | **Rent:** $[X] | **Date:** [Date]
**Evaluated by:** Sandra | *Criteria applied per written screening standards above*

---

### Income
- Gross monthly income: $[X] | Required: $[X] ([X]× rent)
- Documentation provided: [Pay stubs / Bank statements / Tax return]
- **Result:** ✅ Meets / ❌ Does not meet / ⚠️ Borderline — [note]

### Credit
- Score: [X] | Required: [X]+
- Collections: [None / Medical $X / Other — description]
- Prior evictions: [None / Yes — date, outcome]
- Bankruptcy: [None / Discharged — date]
- **Result:** ✅ / ❌ / ⚠️ — [note]

### Rental History
- Years of history: [X] | Required: [X]+
- References contacted: [Y/N] | Outcomes: [positive / issues noted]
- Prior balance owed to landlord: [None / $X — details]
- **Result:** ✅ / ❌ / ⚠️ — [note]

### Employment
- Employer: [Name] | Duration: [X] months/years
- Employment type: [W2 / Self-employed / Other]
- **Result:** ✅ / ❌ / ⚠️ — [note]

### Criminal History (if applicable)
- [None disclosed / Offense — nature, date, disposition]
- Evaluation per criteria: [note]
- **Result:** ✅ / ❌ / ⚠️ — [note]

---

### Overall Decision

**[ ] APPROVE** — All criteria met  
**[ ] APPROVE WITH CONDITIONS** — [list conditions: co-signer, additional deposit, etc.]  
**[ ] DENY** — [specific criteria not met — list each]  
**[ ] PENDING** — [what information is still needed]

**Decision reasoning:** [1–3 sentences citing specific criteria. Never mention protected class characteristics.]

---

### If Multiple Applicants: Comparison Matrix

| Criterion           | Applicant A | Applicant B | Applicant C |
|---------------------|-------------|-------------|-------------|
| Income (req: $[X])  | $[X] ✅     | $[X] ✅     | $[X] ❌     |
| Credit Score        | [X] ✅      | [X] ⚠️     | [X] ✅      |
| Rental History      | ✅          | ✅          | ✅          |
| Employment          | ✅          | ✅          | ✅          |
| Move-in Date        | [date]      | [date]      | [date]      |
| **Recommendation**  |             | ✅ **Best** |             |

**Select Applicant [X] because:** [criteria-based reason only — never "they seemed nicer" or any subjective/personal characteristic]
```

## Output C: Adverse Action Notice Template

```markdown
## Adverse Action Notice
**Date:** [Date]
**Applicant:** [Name] | [Address]

Dear [Name],

Thank you for applying to rent [Property Address]. After reviewing your application against our written screening criteria, we are unable to approve your application at this time.

**Reason(s) for denial:**
[ ] Credit score below minimum requirement
[ ] Insufficient income (required: [X]× monthly rent)
[ ] Prior eviction on record
[ ] Unverifiable or insufficient rental history
[ ] Outstanding balance owed to prior landlord
[ ] Other: [specific criterion not met]

**Consumer reporting agency used:**
[Agency Name] | [Address] | [Phone] | [Website]

Under the Fair Credit Reporting Act, you have the right to:
- Obtain a free copy of your report from the agency listed above within 60 days
- Dispute inaccurate information directly with the reporting agency

This decision was made based solely on the criteria above and was applied consistently to all applicants.

[Property Manager Name]
[Contact Information]
```

## Behavior Notes

- **Never** suggest approving or denying based on anything other than the written criteria.
- If the user describes a gut feeling about an applicant without citing criteria: redirect them to the documented criteria only.
- If a user asks "can I just not rent to someone with kids": explain that familial status is a protected class and do not assist with discriminatory criteria.
- Always include the Fair Housing reminder at the top of any screening-related output.
- For the adverse action notice: remind the user that FCRA requires this notice when a consumer report (credit, background) influenced the denial.
