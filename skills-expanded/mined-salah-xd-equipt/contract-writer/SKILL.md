---
name: contract-writer
description: "Drafts service agreements, freelance contracts, and partnership agreements with standard clauses and plain-language annotations explaining each section. Use when a user needs a professional contract template, wants to formalize a client relationship, or needs a starting point for legal review."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Contract Writer

## When to Use This Skill

Use this skill when:
- A user needs a service agreement, freelance contract, retainer agreement, partnership agreement, or NDA
- Someone wants to formalize a client or vendor relationship before starting work
- A user says they are "working on a handshake" and wants something in writing
- A freelancer, consultant, or agency owner needs a contract template for a new engagement
- A user asks for a starting point they can send to their attorney for review

**DO NOT** use this skill for:
- Employment contracts (W-2 employee agreements require HR/employment law expertise)
- Real estate, securities, or regulatory filings
- Contracts involving litigation, settlements, or court orders
- Any situation where the user explicitly needs licensed legal counsel

---

## Legal Disclaimer

**THIS SKILL GENERATES CONTRACT TEMPLATES FOR INFORMATIONAL PURPOSES ONLY. IT DOES NOT PROVIDE LEGAL ADVICE. EVERY CONTRACT PRODUCED BY THIS SKILL MUST BE REVIEWED BY A QUALIFIED ATTORNEY BEFORE SIGNING OR ENFORCEMENT. THE AUTHOR AND THIS TOOL ACCEPT NO LIABILITY FOR CONTRACTS USED WITHOUT PROFESSIONAL LEGAL REVIEW.**

This disclaimer MUST appear at the top of every generated contract document.

---

## Core Principle

EVERY CONTRACT MUST PROTECT BOTH PARTIES FAIRLY, USE PLAIN LANGUAGE WHEREVER POSSIBLE, AND BE TREATED AS A STARTING TEMPLATE FOR ATTORNEY REVIEW — NEVER AS A FINAL LEGAL DOCUMENT.

---

## Contract Type Quick Reference

| Type | Best For | Key Sections | Typical Length |
|------|----------|-------------|----------------|
| **Freelance Service** | One-time projects (design, dev, copywriting) | Scope, deliverables, payment milestones, IP transfer | 2-4 pages |
| **Retainer** | Ongoing monthly engagements (consulting, marketing) | Monthly scope, hours cap, renewal terms, rate adjustments | 2-4 pages |
| **Partnership** | Co-ventures, revenue shares, joint projects | Roles, profit split, decision authority, exit terms | 3-5 pages |
| **NDA** | Pre-engagement confidentiality | Definition of confidential info, duration, exclusions | 1-2 pages |

When the user does not specify a type, default to **Freelance Service Agreement** and confirm before proceeding.

---

## Phase 1: Gather Contract Details

Collect essential terms before drafting. Ask in order, waiting for responses between groups.

**Group 1 — Parties and Purpose (ask all at once):**
1. What type of contract do you need? (freelance service, retainer, partnership, NDA)
2. Who are the two parties? (your name/business name and the client/partner name)
3. In one or two sentences, what is the service or relationship being formalized?

**Group 2 — Commercial Terms (ask after Group 1):**
4. What is the total price, rate, or compensation structure? (flat fee, hourly, monthly, revenue share)
5. What is the payment schedule? (upfront, milestones, net-30, monthly)
6. What are the specific deliverables or services being provided?
7. What is the project timeline or contract duration? (start date, end date, or ongoing)

**Group 3 — Protections (ask after Group 2):**
8. Who owns the intellectual property after delivery? (client owns all, retained until paid, shared, licensed)
9. Is a confidentiality clause needed? (yes/no — default yes)
10. What are the termination terms? (notice period, what happens to work in progress)
11. Is there a preferred governing law state or jurisdiction?

**Defaults for unanswered questions:**

| Question | Default |
|----------|---------|
| IP ownership | Client owns all deliverables upon full payment |
| Confidentiality | Mutual, 2-year duration |
| Termination notice | 30 days written notice by either party |
| Governing law | User's state if known, otherwise `[STATE]` for attorney to fill |
| Dispute resolution | Mediation first, then binding arbitration |
| Late payment | 1.5% monthly interest on overdue balances |
| Limitation of liability | Capped at total contract value |

**GATE: Do not proceed to Phase 2 until you have answers to at least questions 1-7.** Apply defaults for unanswered protection questions and flag them with `[DEFAULT — confirm with your attorney]`.

---

## Phase 2: Draft the Contract

Structure every contract with these 12 sections. Each section includes a **plain-language annotation** in brackets explaining what it means in everyday terms.

### Required Sections (in order)

**Header:** Disclaimer, contract type title, effective date, both parties with names/addresses/emails and role labels.

**1. Scope of Work**
- Annotation: "This defines exactly what work is being done. If it is not listed here, it is not included."
- Detailed service description from user input
- Explicit exclusions (what is NOT included)

**2. Deliverables**
- Annotation: "These are the specific items the service provider will hand over."
- Table format: Deliverable | Description | Due Date

**3. Payment Terms**
- Annotation: "How much is owed, when payments are due, and what happens if late."
- Total compensation, payment schedule with milestones/dates, late payment terms, accepted methods

**4. Timeline and Milestones**
- Annotation: "The project calendar — start date, key checkpoints, end date."
- Table format: Milestone | Target Date | Notes

**5. Intellectual Property**
- Annotation: "Who owns the work product after the project is complete."
- Ownership terms per user input (transfer, license, or retained)

**6. Confidentiality**
- Annotation: "Both parties agree not to share private business information with outsiders."
- Mutual obligation, survival period, exclusions for public/independent/legally-required info

**7. Termination**
- Annotation: "The exit clause — how to end the contract, notice required, what happens to payments."
- Notice period, payment for completed work, refund of prepaid fees, termination for cause with cure period

**8. Limitation of Liability**
- Annotation: "Caps the maximum amount either party could owe if something goes wrong."
- Liability cap (typically total contract value), exclusion of indirect/consequential damages

**9. Dispute Resolution**
- Annotation: "How to resolve disagreements without going to court."
- Mediation first, then binding arbitration, jurisdiction

**10. Governing Law**
- Annotation: "Which state's laws apply to this contract."
- State, conflict of laws provision

**11. General Provisions**
- Annotation: "Standard housekeeping clauses for edge cases."
- Entire agreement, amendments in writing, severability, force majeure, notices

**12. Signatures**
- Annotation: "The contract is not binding until both parties sign and date it."
- Signature lines, printed names, dates for both parties

### Drafting Rules

- **Plain language always.** Write "The client pays $5,000 within 10 days of signing" not "The Client shall remit the sum of Five Thousand Dollars ($5,000.00) within ten (10) business days of the Effective Date hereof."
- **Never leave a critical term blank.** Use defaults and flag them: `[DEFAULT — confirm with your attorney]`.
- **Keep under 5 pages** for freelance/retainer. Partnership may extend to 6.
- **Adapt sections to the contract type.** An NDA skips Deliverables. A partnership adds Profit Distribution. A retainer adds Term and Renewal.

**GATE: Present the complete draft to the user before saving to file.**

---

## Phase 3: Review with User

Present the full contract draft in chat. Then ask:

1. "Does this accurately reflect the terms you described? Anything wrong or missing?"
2. "Are you comfortable with the default terms I used? (Flagged with [DEFAULT] markers.)"
3. "Do you want to adjust any financial terms, timelines, or IP ownership?"
4. "Anything your attorney has flagged in past contracts that we should add?"

Make requested changes and re-present the updated version.

**If more than 3 revision rounds, pause and ask:** "Would you like to finalize the current version and let your attorney handle the remaining adjustments, or keep refining here?"

**GATE: Do not save to file until the user explicitly approves.** Acceptable: "looks good," "approved," "save it," "finalize," or similar.

---

## Phase 4: Deliver to File

**Step 1:** Ask where to save. Suggest default: `contracts/[party-b-name]-[contract-type]-agreement.md`

**Step 2:** Write the complete contract using the Write tool. Include the disclaimer at the top.

**Step 3:** Confirm delivery with summary:
- Type, parties, total value, duration, key terms
- **Always end with:** "Send this document to a qualified attorney for review before either party signs."

---

## Example 1: Freelance Web Design Contract ($5,000 Project)

**User says:** "I need a contract for a website redesign project. I am charging $5,000."

**Phase 1 produces:**
```
Type: Freelance service agreement
Party A: Sarah Mitchell Design LLC
Party B: Greenleaf Bakery (contact: Tom Reeves)
Service: Complete website redesign — 5 pages (homepage, about, menu, catering, contact)
Price: $5,000 flat fee ($2,500 on signing, $2,500 on delivery)
Deliverables: Wireframes (day 7), mockups (day 14), 2 revision rounds (day 21),
  final files (day 28), deployed site (day 35)
IP: Client owns all upon full payment. Provider retains portfolio rights.
Termination: 14 days written notice, client pays for completed work
Governing law: Oregon
```

**Phase 2 drafts all 12 sections.** Key excerpt:

```
1. SCOPE OF WORK
[Plain-language annotation: This defines exactly what work is being
done. If it is not listed here, it is not included.]

Service Provider will design and develop a complete website redesign
for Client consisting of 5 pages: Homepage, About, Menu, Catering,
and Contact. Includes wireframing, visual design, two revision
rounds, and deployment to Client's hosting.

Work outside this scope (copywriting, photography, SEO, ongoing
maintenance) requires a separate agreement.

3. PAYMENT TERMS
[Plain-language annotation: How much is owed, when, and what
happens if late.]

Total: $5,000 USD
- $2,500 due upon signing
- $2,500 due upon delivery of deployed website
Late Payment: 1.5% monthly interest on balances overdue past 15 days
```

**Phase 3:** User adds "revision rounds beyond 2 cost $150 each." Change made, approved.

**Phase 4:** Saved to `contracts/greenleaf-bakery-freelance-service-agreement.md`.

---

## Example 2: Monthly Retainer Agreement ($2,500/mo Consulting)

**User says:** "I need a retainer contract for marketing consulting at $2,500/month."

**Phase 1 produces:**
```
Type: Retainer agreement
Party A: James Okoro Consulting
Party B: Brightpath Labs Inc. (contact: Priya Sharma, CEO)
Service: Fractional CMO — strategy, campaign review, team mentorship
Price: $2,500/month, due 1st of month net-15
Hours: 20/month cap, additional at $150/hr with written approval
Duration: 3-month initial term, then month-to-month auto-renewal
Monthly deliverables: 2 strategy sessions, marketing plan review,
  campaign audit, ad-hoc Slack (Mon-Fri 9-5 ET)
IP: Client owns deliverables. Provider may reference engagement in case studies.
Termination: 30 days notice, effective at end of billing month
Governing law: New York
Rate adjustment: 60 days written notice, client may decline and terminate
```

**Phase 2 drafts with retainer-specific sections.** Key excerpt:

```
1. SCOPE OF WORK
[Plain-language annotation: This defines what services are included
each month. If not listed, not included in the retainer.]

Consultant provides fractional CMO services: marketing strategy,
campaign performance review, and team mentorship. Delivered remotely.
Monthly cap: 20 hours. Overages at $150/hr require written approval.

3. COMPENSATION AND PAYMENT
[Plain-language annotation: Monthly cost, when it is due, and what
happens if overdue.]

Monthly Retainer: $2,500 USD, due 1st of each month, net-15
Additional Hours: $150/hr (prior written approval required)
Late Payment: 1.5% monthly interest on overdue balances
Rate Adjustments: 60 days written notice; client may decline and terminate
```

**Phase 3:** User adds "mid-month cancellation still owes the full month." Change made, approved.

**Phase 4:** Saved to `contracts/brightpath-labs-retainer-agreement.md`.

---

## Anti-Patterns

**NEVER do these when drafting contracts:**

- **Overly complex legalese.** "Party of the First Part hereby covenants and agrees to indemnify..." is worse than "The service provider agrees to protect the client from claims caused by the provider's work." Plain language is not less enforceable.
- **Skipping or vague payment terms.** "Payment upon completion" is a dispute waiting to happen. Specify exact amount, exact due date, and late-payment consequences.
- **Promising enforceability.** **NEVER** say "legally binding," "enforceable," or "compliant." Always say it needs attorney review.
- **Inserting unflagged clauses.** If you add a clause the user did not request, flag it: `[ADDED — common for this contract type. Confirm with your attorney.]`
- **Boilerplate contradicting user terms.** Cross-check every section against stated terms. If user said "client owns IP," no clause should say "provider retains rights."
- **Out-of-scope contract types.** Employment, securities, real estate are out of scope. Redirect to specialized counsel.
- **Omitting the legal disclaimer.** Every generated contract must include it. No exceptions.

---

## Recovery

**User cannot provide key details:**
1. Offer common defaults: "Most freelance contracts use a 50/50 split — half upfront, half on delivery. Does that work?"
2. If still unsure, mark with `[TO BE DETERMINED — discuss with attorney or client before signing]`.
3. **If 3 attempts fail on basic terms (who, what, how much), stop:** "Finalize these terms with your client first. Once you know the scope, price, and timeline, we can draft this in minutes."

**Contract type outside scope:**
1. Explain: "That requires specialized legal expertise. I can help with service agreements, freelance contracts, retainers, partnerships, and NDAs."
2. Offer the closest alternative: "If you are hiring a contractor rather than an employee, I can draft an independent contractor agreement."

**User wants to combine multiple contract types:**
1. Recommend separate documents: "For clarity, keep these as separate agreements. Your attorney will thank you."
2. If they insist, combine with clearly separated sections and independent annotations.

**File write fails:**
1. Report error, present contract in chat for manual copying.
2. Offer alternative path.
3. **If 3 failures, deliver in chat:** "File saving is not working. The complete contract is above — copy it into your document editor."

---

## Pre-Delivery Checklist

- [ ] Legal disclaimer appears at the top of the document
- [ ] Both parties named correctly throughout
- [ ] Payment amount, schedule, and late-payment terms explicitly stated
- [ ] Every deliverable has a description and due date
- [ ] IP ownership clause matches user's specification
- [ ] Termination clause includes notice period and payment handling
- [ ] Limitation of liability cap stated as specific dollar amount
- [ ] Governing law state filled in (unless user left it open)
- [ ] All `[DEFAULT]` flags present where defaults were applied
- [ ] Plain-language annotations included for every section
- [ ] No internal contradictions between sections
- [ ] Contract type matches user's request
- [ ] Signature block includes both parties with date
