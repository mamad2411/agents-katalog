---
name: grant-report
description: "Writes grant progress and final reports with metric tracking, narrative updates, and financial accounting."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Grant Report

## When to Use This Skill

Use this skill when you need to:
- Write a progress or final report for a grant funder
- Track and present metrics against grant objectives
- Create narrative updates with financial accounting for grant compliance
- Build reusable grant reporting templates for recurring funding cycles

**DO NOT** use this skill for grant applications, impact reports for donors, or internal program evaluations. This is for reports submitted to a specific grant funder to demonstrate how their funds were used.

---

## Core Principle

A GRANT REPORT MUST PROVE TWO THINGS: YOU DID WHAT YOU SAID YOU WOULD DO, AND THE MONEY WAS SPENT EXACTLY AS PROPOSED — FUNDERS WHO TRUST YOUR REPORTING FUND YOU AGAIN.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Funder name** | "Which funder are you reporting to?" | No default — must be provided |
| **Grant purpose** | "What was the grant awarded for?" | No default — must be provided |
| **Report type** | "Progress report or final report?" | Progress report |
| **Reporting period** | "What dates does this report cover?" | No default — must be provided |
| **Original objectives** | "What objectives were stated in the grant proposal?" | No default — must be provided |
| **Funder template** | "Does the funder have a required report format or template?" | No required format |

**GATE: Confirm the brief and gather all data before writing.**

---

## Phase 2: Structure

### Report Architecture

If no funder template is required, use this structure:

```
1. Cover information — grant ID, organization, reporting period, contact
2. Executive summary — 1 paragraph overview of progress
3. Objectives and outcomes — each objective with metrics and narrative
4. Activities and milestones — what was done during the period
5. Challenges and adaptations — what changed and why
6. Financial report — budget vs. actual spending
7. Lessons learned — insights for future work
8. Next steps (progress report) or Sustainability plan (final report)
9. Appendix — supporting data, photos, testimonials
```

### Objectives Tracking Table

```
| Objective | Target | Actual | % Complete | Status |
|-----------|--------|--------|-----------|--------|
| [Objective 1] | [Target metric] | [Actual] | [%] | On track / Behind / Complete |
| [Objective 2] | [Target metric] | [Actual] | [%] | On track / Behind / Complete |
```

**GATE: Present the structure and confirm all objectives are captured before writing.**

---

## Phase 3: Write

### Section-by-Section Guide

**Executive Summary (100-150 words)**
- Grant purpose in one sentence
- Key accomplishments this period
- Any significant challenges or changes
- Overall status assessment

**Objectives and Outcomes**
For each objective from the original proposal:

```
## Objective [N]: [Objective statement from proposal]
**Target:** [What was promised]
**Progress:** [What was achieved, with specific numbers]
**Evidence:** [How this was measured]
**Narrative:** [2-3 sentences explaining the context behind the numbers]
```

**Activities and Milestones**
```
| Activity | Planned Date | Actual Date | Status | Notes |
|----------|-------------|-------------|--------|-------|
| [Activity 1] | [Date] | [Date] | Complete / In progress / Delayed | [Brief note] |
```

**Challenges and Adaptations**
- State each challenge directly — do not hide problems
- Explain what adaptation was made
- Note whether the adaptation required a change to the original plan
- If budget was reallocated, explain and justify

**Financial Report**
```
## Financial Summary

| Budget Category | Approved Budget | Spent This Period | Spent to Date | Remaining |
|----------------|----------------|------------------|--------------|-----------|
| Personnel | $[X] | $[X] | $[X] | $[X] |
| Supplies | $[X] | $[X] | $[X] | $[X] |
| Travel | $[X] | $[X] | $[X] | $[X] |
| Other | $[X] | $[X] | $[X] | $[X] |
| **Total** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |

**Variance explanations:** [Explain any category where spending differs from budget by more than 10%]
```

---

## Phase 4: Polish

### 1. Compliance Check

```
- [ ] All original objectives are addressed (even if behind schedule)
- [ ] Metrics match the measurement plan in the proposal
- [ ] Financial report accounts for every dollar of grant funds
- [ ] Budget variances over 10% are explained
- [ ] Any scope or timeline changes are documented
- [ ] Report matches the funder's required format (if applicable)
- [ ] Submission deadline will be met
```

### 2. Narrative Quality Check

- Facts and data, not opinions or vague language
- Specific numbers replace words like "many," "several," or "significant"
- Challenges are stated honestly, not hidden or minimized
- Tone is professional and factual — not defensive or promotional

### 3. Submission Package

```
## Submission Checklist
- [ ] Narrative report (Word or PDF)
- [ ] Financial report (Excel or matching format)
- [ ] Supporting documents (photos, testimonials, data)
- [ ] Cover letter (if required)
- [ ] Sent to the correct contact at the funder
- [ ] Copy filed in organization's grant records
```

---

## Example 1: Education Grant Progress Report

```
Objective: Provide tutoring to 100 students over 12 months
Progress (6 months): 62 students enrolled, 45 attending regularly
Challenge: Lower-than-expected enrollment in rural areas
Adaptation: Added a transportation stipend program, enrollment increased 30%
Budget: 48% spent at the 50% mark — on track
```

## Example 2: Community Health Grant Final Report

```
Objective: Conduct 500 health screenings in underserved neighborhoods
Result: 547 screenings completed (109% of target)
Key outcome: 83 individuals referred to ongoing care, 61 confirmed follow-up
Budget: $49,200 of $50,000 spent — $800 returned to funder
Sustainability: Partnered with 3 clinics for ongoing screening access
```

---

## Anti-Patterns

- **Hiding bad news** — funders respect honesty. Unreported problems destroy trust when discovered later.
- **Vague metrics** — "We helped many people" is unacceptable. Use exact numbers from your tracking system.
- **Missing financial detail** — every dollar must be accounted for. Unexplained variances trigger audits.
- **Copy-pasting the proposal** — the report should describe what happened, not what you planned to do.
- **Submitting late** — late reports jeopardize future funding. Build in a 1-week buffer before the deadline.
- **Ignoring the funder's format** — if they provide a template, use it exactly. Do not substitute your own format.

---

## Recovery

- **Objectives not met:** Report honestly. Explain why, what was learned, and what adjustments were made. Funders fund learning organizations, not perfect ones.
- **Financial records are incomplete:** Reconstruct from bank statements and receipts. Flag any amounts that could not be verified and explain the gap.
- **Funder template is confusing:** Call the program officer and ask for clarification. They would rather answer questions than receive a wrong report.
- **Multiple grants with overlapping reporting:** Create a master tracking spreadsheet that maps each expense and metric to the correct grant. Never double-count.
