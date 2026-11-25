---
name: employee-handbook-builder
description: |
  Builds a legally-informed employee handbook or policy manual tailored to
  company size, jurisdiction, and operating model — with sectioned policies on
  conduct, leave, remote work, AI usage, and DEI. Use when the user says
  "create our employee handbook", "draft a policy manual", "write a remote work
  policy section", "update our AI usage policy", or "review our handbook for
  compliance". For formal policy and legal-shield documentation, not values or
  culture rituals (company-culture-doc-builder).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="employee-handbook-builder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including company name, jurisdiction history, prior handbook versions, organisational values, and any standing legal or compliance notes.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Company profile**: Company name, industry, headcount, and entity structure (single entity, multi-state, international)
- **Jurisdiction(s)**: Primary operating jurisdiction(s) and any additional states/countries where employees are based
- **Scope**: Full handbook build, update/refresh of an existing handbook, or targeted policy section(s) only?
- **Existing materials**: Upload any current handbook, policy documents, offer letter templates, or cultural manifesto documents
- **Cultural posture**: Where does the company sit on the spectrum — formal/institutional ↔ casual/startup? Any specific tone or voice guidelines?
- **Priority topics**: Are there specific areas of urgency? (e.g. new remote/hybrid policy, AI acceptable use, recent regulatory change, post-acquisition harmonisation)
- **Target audience**: Who is the ICA for this handbook — all employees, specific business unit, contractors, or a combination?
- **Review stakeholders**: Who will approve the final document? (e.g. General Counsel, CHRO, CEO, Board)

If FutureProof context already contains answers to any of the above, confirm them with the user rather than re-asking.

## Step 3: Conduct Jurisdictional & Compliance Mapping

Before drafting, build a **Compliance Requirements Matrix**:

| Policy Area | Federal/National Requirement | State/Provincial Requirement | Local/Municipal Requirement | Company-Specific Enhancement |
|---|---|---|---|---|
| At-will employment / termination | ✓/✗ + citation | ✓/✗ + citation | ✓/✗ + citation | — |
| Anti-discrimination & harassment | — | — | — | — |
| Leave entitlements (FMLA, parental, sick) | — | — | — | — |
| Wage & hour / overtime | — | — | — | — |
| Workplace safety (OSHA or equivalent) | — | — | — | — |
| Privacy & data protection | — | — | — | — |
| Accommodations (ADA or equivalent) | — | — | — | — |

Populate each cell with the applicable statute or regulation. Flag any **multi-jurisdiction conflicts** (e.g. California meal-break rules vs. federal standards) and recommend the most protective standard unless the user's counsel directs otherwise.

**Note**: Advise the user that this matrix informs drafting but does not constitute legal advice — final review by qualified employment counsel in each jurisdiction is mandatory.

## Step 4: Define Handbook Architecture

Produce a **Table of Contents & Section Map** structured as follows:

### Part I — Welcome & Company Foundation
1. Welcome letter (CEO/Founder)
2. Company mission, vision, and values
3. Handbook purpose, scope, and at-will disclaimer
4. How to use this handbook / acknowledgement of receipt

### Part II — Employment Fundamentals
5. Equal employment opportunity statement
6. Employment classifications (full-time, part-time, temporary, contractor)
7. Recruitment, hiring, and onboarding
8. Background checks and eligibility verification
9. Introductory/probationary period (if applicable)

### Part III — Compensation & Benefits
10. Pay practices, pay periods, and payroll deductions
11. Overtime and timekeeping
12. Benefits overview (health, retirement, equity, wellness)
13. Expense reimbursement policy
14. Employee referral programme

### Part IV — Time Off & Leaves
15. Paid time off (PTO) / vacation policy
16. Sick leave
17. Statutory leaves (FMLA, parental, bereavement, jury duty, voting)
18. Sabbatical and extended leave (if applicable)
19. Holiday schedule

### Part V — Workplace Conduct & Culture
20. Code of conduct and professional standards
21. Anti-harassment and anti-discrimination policy
22. Workplace violence prevention
23. Drug and alcohol policy
24. Dress code and personal appearance
25. Conflict of interest and outside employment
26. Whistleblower protection

### Part VI — Operational Policies
27. Work location policy (on-site / hybrid / remote)
28. Working hours, scheduling, and flexible work
29. Technology and acceptable use policy
30. AI and generative technology acceptable use policy
31. Social media policy
32. Confidentiality, trade secrets, and intellectual property
33. Data privacy and employee monitoring disclosure
34. Company property and equipment

### Part VII — Health, Safety & Security
35. Workplace health and safety
36. Emergency procedures
37. Workers' compensation
38. Workplace accommodations

### Part VIII — Performance & Development
39. Performance review process and cadence
40. Learning and development opportunities
41. Internal mobility and promotions
42. Corrective action and progressive discipline

### Part IX — Separation
43. Voluntary resignation procedures
44. Involuntary termination
45. Exit interview process
46. Return of company property
47. Post-employment obligations (non-compete, non-solicitation — jurisdiction-permitting)

### Part X — Acknowledgement
48. Handbook acknowledgement and receipt form

Present this architecture to the user for approval. Add, remove, or reorder sections based on their input and any standing `instructions` from FutureProof context.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Draft the Handbook

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Draft each section following this methodology:

### Drafting Standards

1. **Plain language first**: Write at an 8th-grade reading level. Avoid legalese in the body; place statutory citations in footnotes or a compliance appendix.
2. **Jurisdiction-specific callouts**: Use clearly labelled callout boxes (e.g. `📍 California Employees:`) for any state- or locale-specific variations rather than creating separate handbooks.
3. **Cultural voice alignment**: Match the tone the user specified — formal handbooks use third person and passive construction; casual handbooks use "you/we" and conversational framing. Maintain consistency throughout.
4. **Policy structure per section**:
   - **Purpose**: Why this policy exists (1–2 sentences)
   - **Scope**: Who it applies to
   - **Policy statement**: The substantive rules
   - **Procedures**: Step-by-step actions for employees and managers
   - **Exceptions**: How to request exceptions and who approves
   - **Contact**: Role/department for questions (not a named individual — reduces update burden)
5. **Inclusive language audit**: Use gender-neutral language throughout. Reference "spouse or domestic partner," "caregiver," and "parent" rather than gendered equivalents.
6. **Future-proofing**: Avoid embedding specific benefit plan details, dollar amounts, or dated references that change annually — instead reference "the current Benefits Summary available on [intranet/HRIS]."

### Section-by-Section Drafting

Draft all approved sections in sequence. For each section, cross-reference the Compliance Requirements Matrix from Step 3 to ensure statutory minimums are met or exceeded.

Flag any sections where:
- The user's current policy falls **below** statutory minimums → **Compliance Risk**
- Industry best practice significantly exceeds the statutory minimum → **Enhancement Opportunity**
- Multi-jurisdiction conflict exists → **Counsel Review Required**

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce the following deliverables:

### Deliverable 1: Employee Handbook (Full Document)
- Format: Structured document with table of contents, numbered sections, and page-ready formatting
- Includes: All drafted sections, jurisdiction-specific callout boxes, acknowledgement form as final page
- Naming convention: `[Company Name] Employee Handbook — [Month Year]`

### Deliverable 2: Compliance Requirements Matrix
- Format: Table (as developed in Step 3, fully populated)
- Purpose: Working document for legal counsel review
- Naming convention: `[Company Name] Compliance Matrix — [Month Year]`

### Deliverable 3: Counsel Review Checklist
- Format: Prioritised checklist of items requiring employment law review
- Includes: Section number, issue description, jurisdiction, risk level (High / Medium / Low), and recommended reviewer (e.g. "California employment counsel")
- Naming convention: `[Company Name] Handbook — Legal Review Checklist`

### Deliverable 4: Implementation Memo
- Format: 1-page memo to HR leadership / review stakeholders
- Includes:
  - Summary of key policy decisions embedded in the handbook
  - Distribution and acknowledgement collection plan
  - Recommended rollout timeline (announcement → manager briefing → all-hands → acknowledgement deadline)
  - Annual review cadence recommendation
- Naming convention: `[Company Name] Handbook — Implementation Memo`

### Deliverable 5: Change Log (if update/refresh scope)
- Format: Table showing section, previous policy summary, new policy summary, rationale for change
- Purpose: Enables stakeholders to review only what changed
- Naming convention: `[Company Name] Handbook — Change Log [Month Year]`

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="employee-handbook-builder", experiment={
  hypothesis: "Providing a 2-page visual quick-start guide alongside the full handbook increases new-hire acknowledgement completion rate within the first 5 business days",
  variants: ["control: full handbook PDF only", "variant: full handbook PDF + visual quick-start guide"],
  measurement: "Acknowledgement completion rate and average days-to-completion for next 50 new hires",
  expected_impact: "20% increase in on-time acknowledgement completion; reduction in HR follow-up burden"
})
```

```
FutureProof:save_experiment(skill="employee-handbook-builder", experiment={
  hypothesis: "Replacing legalistic section headers with question-based headers (e.g. 'What happens if I need time off?' vs. 'Leave of Absence Policy') increases employee self-service policy lookups and reduces HR inquiry volume",
  variants: ["control: standard policy headers", "variant: question-based headers"],
  measurement: "HR helpdesk ticket volume for policy clarification questions over 90 days post-rollout",
  expected_impact: "15% reduction in routine policy-related HR enquiries"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="employee-handbook-builder",
  query="2024-2025 emerging employment law changes, state-level paid leave expansions, AI workplace regulation, and NLRB handbook enforcement trends affecting employee handbook drafting",
  reason="Ensure handbook templates reflect the latest statutory requirements and enforcement posture — particularly rapid changes in AI workplace policy, state paid leave mandates, and NLRB scrutiny of overbroad handbook provisions"
)
```

```
FutureProof:request_research(skill="employee-handbook-builder",
  query="Best practices for employee handbook design, digital distribution, and acknowledgement tracking in distributed/remote-first organisations 2024",
  reason="Optimise handbook delivery format and acknowledgement workflows for companies with no central office — increasingly the dominant operating model for ICA organisations"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="employee-handbook-builder", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```