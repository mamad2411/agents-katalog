---
name: offer-letter
description: "Drafts employment offer letters with position details, compensation, benefits, start date, and key terms for professional hiring communication."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Offer Letter

## When to Use This Skill

Use this skill when you need to:
- Draft a professional offer letter for a new employee or contractor
- Include position details, compensation, benefits, and start date
- Create a reusable offer letter template for future hires
- Formalize a verbal offer into a written document

**DO NOT** use this skill for full employment contracts, contractor agreements, or legal compliance documents. This is for the offer letter — the document that communicates the offer. Consult legal counsel for binding employment contracts.

---

## Core Principle

AN OFFER LETTER IS A FIRST IMPRESSION AS AN EMPLOYER — IT SHOULD BE CLEAR, PROFESSIONAL, AND EXCITING ENOUGH THAT THE CANDIDATE FEELS GREAT ABOUT SAYING YES.

---

## Phase 1: Offer Details

Gather the specific terms of the offer.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Candidate name** | "Who is the offer for?" | No default |
| **Position title** | "What is the job title?" | No default |
| **Employment type** | "Full-time, part-time, or contractor?" | No default |
| **Start date** | "When should they start?" | No default |
| **Compensation** | "What is the salary or rate?" | No default |
| **Pay frequency** | "How often will they be paid? (weekly, biweekly, monthly)" | Biweekly |
| **Benefits** | "What benefits are included? (health, PTO, remote stipend, etc.)" | Varies |
| **Manager** | "Who will they report to?" | Business owner |
| **Work location** | "Remote, hybrid, or on-site?" | Remote |
| **Response deadline** | "When do they need to respond by?" | 5 business days |

### Pre-Offer Checklist

```
- [ ] Compensation confirmed and within budget
- [ ] Start date is feasible (onboarding prep time included)
- [ ] Benefits and perks clearly defined
- [ ] Any conditions (background check, references) identified
- [ ] Manager and team notified of expected hire
```

**GATE: Confirm all offer details before drafting the letter.**

---

## Phase 2: Draft Letter

Write the offer letter.

### Employee Offer Letter Template

```
[Business Name]
[Business Address]
[Date]

[Candidate Name]
[Candidate Address]

Dear [Candidate First Name],

I am thrilled to offer you the position of **[Position Title]** at **[Business Name]**. After our conversations, I am confident you will be a great addition to the team, and I am excited to work together.

## Position Details

**Title:** [Position Title]
**Reports to:** [Manager Name and Title]
**Start date:** [Date]
**Work location:** [Remote / Hybrid / On-site at Address]
**Employment type:** [Full-time / Part-time] [Exempt / Non-exempt if applicable]

## Compensation

**Base salary:** $[Amount] per year, paid [biweekly / monthly]
[**Bonus:** Eligible for [bonus structure] based on [criteria] — if applicable]
[**Equity:** [Details] — if applicable]

## Benefits

- [Benefit 1 — e.g., Health insurance (eligible after 30 days)]
- [Benefit 2 — e.g., X days paid time off per year]
- [Benefit 3 — e.g., Remote work stipend of $X/month]
- [Benefit 4 — e.g., Professional development budget of $X/year]
- [Additional benefits]

## Conditions

This offer is contingent upon:
- [Successful completion of background check — if applicable]
- [Satisfactory reference checks — if applicable]
- [Proof of eligibility to work in [country] — if applicable]
- [Signing of employment agreement and NDA — if applicable]

## At-Will Employment

[For US-based employment:] Employment with [Business Name] is at-will, meaning either party may end the employment relationship at any time, with or without cause or notice.

## Response

Please confirm your acceptance by signing and returning this letter by **[Response Deadline Date]**. If you have any questions, do not hesitate to reach out to me directly at [email/phone].

I am genuinely excited about what we will accomplish together. Welcome aboard!

Warm regards,

[Your Name]
[Your Title]
[Business Name]
[Email]
[Phone]

---

**Acceptance:**

I, [Candidate Name], accept the offer of employment as described above.

Signature: _______________ Date: _______________
```

### Contractor Offer Letter Template

```
Dear [Name],

I am pleased to offer you a contractor engagement with [Business Name] as a **[Role/Title]**.

**Engagement details:**
- **Scope:** [Brief description of work]
- **Start date:** [Date]
- **Duration:** [Ongoing / Fixed term through Date]
- **Rate:** $[Amount] per [hour / project / month]
- **Payment terms:** [Net 15 / Net 30 / Upon delivery]
- **Expected hours:** [X hours per week, flexible schedule]

**Next steps:**
1. Sign and return this letter by [Date]
2. Sign the contractor agreement (attached)
3. Complete W-9 form
4. [Additional setup steps]

Looking forward to working with you!

[Name]
```

**GATE: Present the draft offer letter for review.**

---

## Phase 3: Personalize

Customize the letter to make it compelling.

### Personal Touch Points

Add 1-2 sentences that reference:
- Something specific from the interview ("Your experience with [X] really stood out")
- A project or goal they will work on ("Your first project will be [X], which I think you will find exciting")
- Why they were chosen ("You were our top candidate because [specific reason]")

### Compensation Presentation

If the offer includes multiple components, present as a total compensation summary:

```
## Your Total Compensation

| Component | Annual Value |
|-----------|-------------|
| Base salary | $[X] |
| Target bonus | $[X] |
| Benefits value | ~$[X] |
| Perks (stipends, development budget) | $[X] |
| **Total** | **$[X]** |
```

### Attachments to Include

- Employee handbook or culture document (if available)
- Benefits summary sheet
- NDA or confidentiality agreement (for signing)
- Employment agreement (if separate from offer letter)
- W-4 or W-9 form

---

## Phase 4: Deliver

Send the offer professionally and follow up.

### Delivery Process

1. Call the candidate first to deliver the offer verbally (builds excitement)
2. Send the written offer letter within 2 hours of the call
3. Give them the stated deadline (typically 3-5 business days)
4. Check in after 2 days if no response ("Any questions I can answer?")

### Negotiation Prep

If the candidate negotiates:
- Know your maximum before the conversation
- Be open to creative alternatives (remote stipend, extra PTO, flexible hours) if base salary is firm
- Respond within 24 hours to counter-offers
- Get final agreement in writing

### After Acceptance

```
## Post-Acceptance Checklist

- [ ] Send confirmation email with next steps
- [ ] Begin onboarding preparation (see onboarding-checklist skill)
- [ ] Notify the team about the new hire and start date
- [ ] Prepare tool access and accounts
- [ ] Schedule Day 1 welcome meeting
```

---

## Anti-Patterns

- **Verbal offer only** — always put offers in writing. Verbal offers lead to misunderstandings about terms.
- **Vague compensation** — "Competitive salary" is not an offer. State the exact number.
- **No response deadline** — without a deadline, offers linger and create uncertainty for both sides.
- **Cold delivery** — emailing an offer without a phone call first misses the chance to build excitement and answer questions.
- **Overpromising benefits** — do not list benefits you cannot deliver. Under-promise and over-deliver.

---

## Recovery

- **Candidate declines the offer:** Ask what would change their mind. Sometimes a small adjustment (start date, remote flexibility, title) makes the difference. If they decline, respond graciously — they may refer someone.
- **Candidate negotiates higher than budget:** Know your walk-away number before the conversation. Offer non-monetary alternatives if salary is at max.
- **Candidate ghosts after receiving the offer:** Follow up at Day 3 and Day 5. If no response by the deadline, send a final message and move to your backup candidate.
- **User has never written an offer letter:** Use the template above with minimal customization. A simple, clear offer letter is better than a delayed one.
- **Legal concerns about the language:** Add a disclaimer: "This letter is not a contract of employment." Recommend the user have a lawyer review the template before first use.
