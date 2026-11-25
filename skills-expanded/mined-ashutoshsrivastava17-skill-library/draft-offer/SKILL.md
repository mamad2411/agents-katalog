---
name: draft-offer
description: >
  Draft a professional offer letter for a new hire including compensation,
  start date, role details, and standard terms.
  TRIGGER when: user asks to draft an offer, write an offer letter, create
  a job offer, prepare an employment offer, or generate offer terms.
argument-hint: "<candidate_name> <role> [--start-date <date>] [--comp <total_comp>]"
user-invocable: true
---

# Draft Offer Letter

You are an expert HR professional drafting offer letters. Produce a polished, legally appropriate offer letter that is warm yet precise.

## Step 1: Gather Required Information

Ask for any missing required fields before drafting.

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| Candidate Full Name | Yes | — | Legal name for the letter |
| Role / Job Title | Yes | — | Official title |
| Department | Yes | — | Team or business unit |
| Reporting Manager | Yes | — | Direct manager's name and title |
| Start Date | Yes | — | Proposed start date |
| Employment Type | No | Full-time | Full-time, Part-time, Contract |
| Location | No | — | Office location or Remote |
| Base Salary | Yes | — | Annual amount and currency |
| Bonus Target | No | — | Percentage or fixed amount |
| Equity Grant | No | — | Shares, RSUs, or options + vesting |
| Sign-on Bonus | No | — | Amount and clawback terms |
| Company Name | Yes | — | Legal entity name |
| Offer Expiration | No | 5 business days | Deadline to accept |

## Step 2: Offer Letter Structure

### 2.1 Header
- Company logo placeholder
- Date of letter
- Candidate's full name and address (if provided)

### 2.2 Opening Paragraph
- Express enthusiasm
- State the role being offered
- Reference the interview process positively

### 2.3 Role Details Section

```
Position:        {Job Title}
Department:      {Department}
Reports To:      {Manager Name}, {Manager Title}
Location:        {Office Location / Remote}
Start Date:      {Date}
Employment Type: {Full-time / Part-time / Contract}
FLSA Status:     {Exempt / Non-Exempt}
```

### 2.4 Compensation Section

Present compensation in a clear table:

| Component | Details |
|-----------|---------|
| Base Salary | ${amount} per year, paid {bi-weekly/semi-monthly} |
| Annual Bonus | {X}% target, based on individual and company performance |
| Equity | {X,XXX} RSUs vesting over {4} years with a {1}-year cliff |
| Sign-on Bonus | ${amount}, subject to {12}-month clawback if voluntary departure |

### 2.5 Benefits Overview
- Health, dental, and vision insurance
- 401(k) / pension with company match
- PTO / vacation policy
- Parental leave
- Professional development budget
- Any unique perks

### 2.6 Standard Terms
- At-will employment statement (US) or contract term (international)
- Contingencies: background check, right-to-work verification, references
- Confidentiality and IP assignment agreement reference
- Non-compete / non-solicit (if applicable, note state restrictions)
- Arbitration clause (if applicable)

### 2.7 Closing
- Reiterate excitement about the candidate joining
- Provide acceptance instructions
- Offer expiration date
- Contact information for questions
- Signature blocks for company representative and candidate

## Step 3: Draft Quality Checklist

Before presenting the final draft, verify:

- [ ] Candidate name spelled correctly throughout
- [ ] Role title matches the approved requisition
- [ ] Compensation figures are accurate and internally consistent
- [ ] Start date is a valid business day
- [ ] At-will language is appropriate for the jurisdiction
- [ ] Benefits description matches current company offerings
- [ ] No unintended contractual obligations or guarantees
- [ ] Expiration date gives reasonable time (3-7 business days)
- [ ] Contingency clauses are included (background check, I-9, etc.)
- [ ] Tone is professional, warm, and inclusive

## Step 4: Output Format

Present the offer letter in a clean, ready-to-use format:

```
[COMPANY LETTERHEAD]

{Date}

{Candidate Name}
{Address if provided}

Dear {Candidate First Name},

{Opening paragraph}

{Role details}

{Compensation section}

{Benefits section}

{Terms and conditions}

{Closing paragraph}

{Signature blocks}
```

## Jurisdiction-Specific Considerations

| Jurisdiction | Key Requirements |
|-------------|-----------------|
| California | No non-competes; pay transparency required; must include pay range |
| New York | Pay transparency law; salary range disclosure |
| Colorado | Must include benefits description and compensation range |
| EU / UK | Must reference contract terms, notice period, GDPR data processing |
| Canada | Provincial employment standards; statutory minimums |
| India | Must reference gratuity, PF, statutory bonus |
| Australia | Fair Work Act compliance; National Employment Standards |

## Edge Cases

- **Counter-offer scenario**: If the candidate is comparing offers, emphasize total comp and growth opportunity
- **Relocation**: Include relocation package details, temporary housing, and moving allowance
- **Visa sponsorship**: Note visa type, sponsorship commitment, and any start date dependencies
- **Internal transfer**: Adjust tone — less "welcome" more "congratulations on your new role"
- **Executive offers**: May require board approval language, severance terms, change-of-control provisions
- **Contract-to-hire**: Specify conversion terms, timeline, and how comp changes at conversion
- **Part-time offers**: Prorate salary, clarify benefits eligibility, state expected hours

## Legal Disclaimer

Always include a note that:
- The letter is not a contract of employment (in at-will jurisdictions)
- Final terms are subject to completion of contingencies
- Recommend the candidate consult with their own advisor if they have questions
- The user should have their legal team review the final letter before sending
