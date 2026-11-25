---
name: tenant-screening-checklist
description: "Creates tenant screening checklists with verification steps, reference check questions, and evaluation criteria."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Tenant Screening Checklist

## When to Use This Skill

Use this skill when you need to:
- Build a consistent tenant screening process for rental properties
- Create verification checklists for income, credit, and rental history
- Write reference check questions for landlords and employers
- Design evaluation criteria that select reliable tenants fairly

**DO NOT** use this skill for commercial tenant evaluation, roommate screening, or tenant eviction processes. This is for residential landlord screening of prospective tenants.

---

## Core Principle

CONSISTENT SCREENING APPLIED EQUALLY TO EVERY APPLICANT PROTECTS YOU LEGALLY AND SELECTS BETTER TENANTS — NEVER SKIP STEPS OR APPLY DIFFERENT STANDARDS TO DIFFERENT PEOPLE.

---

## Phase 1: Screening Standards

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Property type** | "What type of rental — single family, multi-family, condo?" | Single-family rental |
| **Monthly rent** | "What is the monthly rent?" | No default — must be provided |
| **Minimum credit score** | "What credit score do you require?" | 620 |
| **Income requirement** | "Income-to-rent ratio?" | 3x monthly rent |
| **Pet policy** | "Do you allow pets? Restrictions?" | Case by case |
| **State/jurisdiction** | "What state is the property in?" | No default — affects legal requirements |

**GATE: Confirm screening standards and local legal requirements before building the checklist.**

---

## Phase 2: Application Checklist

### Required Documents

```
## Tenant Application Checklist

### Identity Verification
- [ ] Government-issued photo ID (driver's license, passport)
- [ ] Social Security Number (for credit/background check)
- [ ] Signed application form with authorization for screening

### Income Verification
- [ ] Last 3 pay stubs (or 2 months of bank statements for self-employed)
- [ ] Employment verification letter or offer letter
- [ ] Tax returns (if self-employed — last 2 years)
- [ ] Income meets minimum [3x] monthly rent: $[amount]/month required

### Rental History
- [ ] Contact information for last 2-3 landlords
- [ ] Rental addresses and dates for the last 3-5 years
- [ ] Explanation for any gaps in rental history

### Credit & Background
- [ ] Credit report pulled (score: minimum [620])
- [ ] Background check completed
- [ ] Eviction history search completed
- [ ] Sex offender registry check (where legally required/permitted)
```

---

## Phase 3: Verification Procedures

### Landlord Reference Questions

Call previous landlords and ask:

```
## Landlord Reference Check

**Tenant name:** _______________
**Property address:** _______________
**Landlord name:** _______________
**Date of call:** _______________

1. Can you confirm [tenant name] rented from you at [address]?
2. What were the lease dates? (From ___ to ___)
3. What was the monthly rent? $___
4. Was rent paid on time consistently? (Yes / Usually / No)
5. Were there any lease violations or complaints? (Yes / No — details)
6. Was the security deposit returned in full? (Yes / Partial / No — reason)
7. Did they provide proper move-out notice? (Yes / No)
8. Would you rent to them again? (Yes / No — reason)
9. How many occupants lived in the unit?
10. Any property damage beyond normal wear and tear?
```

### Employer Verification

```
## Employment Verification

**Applicant name:** _______________
**Employer:** _______________
**Contact:** _______________

1. Can you confirm [name] is currently employed with your company?
2. What is their position/title?
3. How long have they been employed?
4. Is their position full-time or part-time?
5. Can you verify their stated income of $___/month? (Yes / No / Unable to disclose)
```

### Credit Report Evaluation

| Factor | Green Flag | Yellow Flag | Red Flag |
|--------|-----------|-------------|----------|
| Credit score | 700+ | 620-699 | Below 620 |
| Payment history | No late payments | 1-2 late (30-day) | Collections or charge-offs |
| Debt-to-income | Under 35% | 35-45% | Over 45% |
| Eviction history | None | None but short tenancies | Prior eviction |
| Bankruptcies | None | Discharged 5+ years ago | Recent or active |

---

## Phase 4: Decision Framework

### Scoring Matrix

```
## Applicant Evaluation — [Name]

| Criteria | Weight | Score (1-5) | Weighted Score |
|----------|--------|------------|----------------|
| Income qualification | 25% | [X] | [X] |
| Credit score/history | 25% | [X] | [X] |
| Rental references | 25% | [X] | [X] |
| Employment stability | 15% | [X] | [X] |
| Application completeness | 10% | [X] | [X] |
| **Total** | 100% | | **[X/5.0]** |

**Decision:** Accept / Conditional Accept / Deny
**Conditions (if applicable):** [Additional deposit, co-signer, etc.]
```

### Denial Process

If denying an application:
- Provide an adverse action notice as required by the Fair Credit Reporting Act
- State the reason for denial in objective, non-discriminatory terms
- Include the credit bureau contact information if credit was a factor
- Return application fees if required by local law
- Document the denial reason for your records

### Fair Housing Compliance

Apply every screening criterion identically to every applicant:
- Same credit score minimum for all
- Same income ratio for all
- Same reference check process for all
- Document everything — your consistency is your legal protection
- Never make exceptions based on protected class characteristics

---

## Anti-Patterns

- **Skipping reference checks** — a clean credit report does not tell you how the tenant treated the last property. Call previous landlords.
- **Inconsistent standards** — applying different criteria to different applicants creates fair housing liability.
- **Only checking the most recent landlord** — the current landlord may give a good reference just to move a problem tenant out. Check 2-3 landlords back.
- **No written criteria** — undocumented standards cannot be defended. Write your criteria down before screening anyone.
- **Rushing to fill a vacancy** — a bad tenant costs more than a vacant month. Screen thoroughly every time.

---

## Recovery

- **Applicant has no rental history:** Accept other references (employer, professional, personal). Consider a higher deposit or co-signer.
- **Cannot reach previous landlords:** Ask the applicant for alternative contacts. Check property records to verify ownership. Document your attempts.
- **Borderline credit score:** Consider the full picture — stable income, strong references, and a reasonable explanation may offset a lower score.
- **Applicant claims discrimination:** Review your records showing consistent criteria applied to all applicants. Consult an attorney if a formal complaint is filed.
- **Local laws restrict screening criteria:** Research your jurisdiction's specific limitations (some cities restrict credit checks or criminal history screening).
