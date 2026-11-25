---
name: client-agreement
description: "Drafts client service agreements with scope, deliverables, timelines, revisions, and payment terms. Use when creating contracts for client engagements."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Client Agreement

## When to Use This Skill

Use this skill when you need to:
- Draft a service agreement for a client engagement
- Define scope, deliverables, timelines, and revision limits
- Establish payment terms, cancellation policies, and IP ownership
- Create a reusable client agreement template

**DO NOT** use this skill for contractor agreements (use independent-contractor-agreement), SaaS terms (use saas-agreement), or partnership agreements. This is for agreements where YOU provide services to a CLIENT. Have an attorney review before use.

---

## Core Principle

A CLIENT AGREEMENT EXISTS TO PREVENT SCOPE CREEP, PAYMENT DISPUTES, AND MISALIGNED EXPECTATIONS — THE CLEARER THE AGREEMENT, THE SMOOTHER THE ENGAGEMENT.

---

## Phase 1: Engagement Details

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Your business name** | "What is your legal business name?" | No default — must be provided |
| **Client name** | "Who is the client?" | No default — must be provided |
| **Services** | "What services will you provide?" | No default — must be provided |
| **Deliverables** | "What are the specific deliverables?" | No default — must be provided |
| **Timeline** | "What is the project timeline?" | No default — must be provided |
| **Pricing** | "How is this priced? (project, hourly, retainer)" | Project-based |
| **Revisions** | "How many revision rounds are included?" | 2 rounds |

**GATE: Do not proceed without services, deliverables, and pricing.**

---

## Phase 2: Agreement Structure

```
## Client Service Agreement

**This Agreement** is entered into as of [Date] between:

**Service Provider:** [Your Business Legal Name] ("Provider")
**Client:** [Client Name/Business] ("Client")

### 1. Services

Provider agrees to perform the following services:

[Detailed description of services]

### 2. Deliverables and Timeline

| # | Deliverable | Description | Due Date |
|---|------------|-------------|----------|
| 1 | [Deliverable] | [Specific description] | [Date] |
| 2 | [Deliverable] | [Specific description] | [Date] |
| 3 | [Deliverable] | [Specific description] | [Date] |

**Project start date:** [Date]
**Estimated completion:** [Date]

Timelines are contingent on Client providing required materials and
feedback by agreed-upon dates. Delays in Client responses will extend
the project timeline proportionally.

### 3. Revisions

- [2] rounds of revisions are included in the project fee
- A "revision" is defined as changes to the direction, content, or
  design within the approved scope
- Additional revision rounds are billed at $[X]/hour or $[X] per round
- Revisions requested more than [30] days after deliverable presentation
  are considered new work and quoted separately

### 4. Compensation

| Component | Amount |
|-----------|--------|
| Project fee | $[X] |
| Payment schedule | [50]% due at signing / [50]% due on completion |
| Additional work (out of scope) | $[X]/hour or quoted per request |
| Payment method | [ACH / credit card / check] |
| Payment terms | Due within [15] days of invoice |
| Late payment fee | [1.5]% per month on overdue balances |

[For retainers:]
Monthly retainer of $[X] due on the [1st] of each month. Retainer
covers [X] hours of work. Unused hours [roll over for 1 month / expire].
Hours exceeding the retainer are billed at $[X]/hour.

### 5. Client Responsibilities

Client agrees to:
- Provide necessary materials, content, access, and feedback by
  agreed-upon dates
- Designate a single point of contact for communication and approvals
- Respond to requests for feedback within [3-5] business days
- Provide timely approval of deliverables

Failure to fulfill these responsibilities may result in project
delays and additional charges.

### 6. Intellectual Property

**Option A — Provider transfers IP:**
Upon full payment, all intellectual property rights in the deliverables
transfer to Client. Provider retains the right to display the work in
their portfolio unless Client requests otherwise in writing.

**Option B — Provider licenses IP:**
Provider retains ownership of all deliverables and grants Client a
[non-exclusive / exclusive] license to use the deliverables for
[specific purposes]. Provider retains portfolio rights.

[Select the appropriate option for the engagement]

### 7. Confidentiality

Both parties agree to keep confidential information private during
and after the engagement. Confidential information includes business
strategies, customer data, financial information, and any information
marked as confidential. This obligation survives for [2] years after
termination.

### 8. Cancellation and Termination

**Client cancellation:**
- Before work begins: Full refund minus [10]% administrative fee
- After work begins: Client pays for work completed plus [any
  upfront payment is non-refundable]
- After [50]% completion: Client pays for work completed; no refund
  of upfront payment

**Provider cancellation:**
- Provider may terminate with [14] days notice
- Client receives all completed work and a refund for unperformed services

**For retainers:**
Either party may cancel with [30] days written notice. No refund of
the current month's retainer.

### 9. Limitation of Liability

Provider's total liability shall not exceed the total fees paid under
this Agreement. Provider is not liable for indirect, consequential,
or incidental damages, including lost profits or revenue.

### 10. Indemnification

Client shall indemnify Provider against claims arising from Client's
materials, instructions, or use of the deliverables in a manner not
contemplated by this Agreement.

### 11. Dispute Resolution

Disputes shall be resolved through [mediation / arbitration] in
[jurisdiction] before either party may pursue litigation.

### 12. General Provisions

- **Entire Agreement:** This is the complete agreement.
- **Amendments:** Require written agreement by both parties.
- **Governing Law:** Laws of [State].
- **Force Majeure:** Neither party is liable for delays due to
  circumstances beyond reasonable control.

---

**Provider:**
Signature: _______________ Date: _______________

**Client:**
Signature: _______________ Date: _______________
```

---

## Phase 3: Scope of Work Attachment

```
## Attachment A: Scope of Work

### Project Overview
[Detailed description of the project]

### In Scope
- [Specific item 1]
- [Specific item 2]
- [Specific item 3]

### Out of Scope
- [Item explicitly not included 1]
- [Item explicitly not included 2]

### Assumptions
- [Assumption about tools, access, or materials]
- [Assumption about timeline or availability]

### Change Order Process
Any work outside the defined scope requires a written change order
signed by both parties before work begins. Change orders will include
scope, timeline, and cost of the additional work.
```

---

## Phase 4: Finalize

```
## Agreement Checklist

- [ ] Scope of work is specific and measurable
- [ ] Deliverables are clearly defined with due dates
- [ ] Payment schedule and amounts are clear
- [ ] Revision limits are stated
- [ ] IP ownership is explicitly addressed
- [ ] Cancellation terms protect both parties
- [ ] Client responsibilities are defined
- [ ] Out-of-scope items are listed to prevent scope creep
- [ ] Both parties have signed
- [ ] Agreement reviewed by legal counsel
```

---

## Example: Brand Strategy Consultant

**Services:** Brand positioning, messaging framework, and visual identity guidelines. **Deliverables:** Brand audit report (Week 2), positioning statement and messaging framework (Week 4), visual identity guide (Week 6). **Fee:** $5,000 — $2,500 upfront, $2,500 on final delivery. **Revisions:** 2 rounds per deliverable. **IP:** Transfers to client upon full payment. **Cancellation:** Deposit non-refundable after Week 1.

---

## Anti-Patterns

- **No scope of work** — "help with marketing" is not a scope. Without specific deliverables, scope creep is guaranteed.
- **No payment before work starts** — always collect a deposit. It confirms commitment and protects against non-payment.
- **Unlimited revisions** — "revisions until you are happy" sounds generous but leads to endless cycles. Set a number.
- **No out-of-scope list** — explicitly stating what is NOT included prevents assumptions.
- **Verbal agreements for anything over $500** — put it in writing. Every time.

---

## Recovery

- **Client requesting work outside scope:** Reference the agreement, point to the out-of-scope list, and propose a change order with additional cost and timeline.
- **Client not responding to feedback requests:** Send a reminder citing the agreement's response timeline. Document delays. After [10] business days, put the project on hold with written notice.
- **Payment is late:** Follow the late payment terms in the agreement. Send reminders at 1, 7, and 14 days past due. Pause work at 15+ days past due.
- **No agreement signed and work already started:** Stop and get it signed immediately. Even a simple email with key terms confirmed by both parties is better than nothing.
