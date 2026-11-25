---
name: scope-of-work
description: "Creates detailed scope of work documents with deliverables, milestones, assumptions, and exclusions for client projects."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Scope of Work

## When to Use This Skill

Use this skill when you need to:
- Define project deliverables, timeline, and boundaries before starting work
- Create a formal scope of work document for a client engagement
- Document assumptions, exclusions, and acceptance criteria
- Prevent scope creep by establishing clear expectations upfront

**DO NOT** use this skill for proposals (use consulting-proposal-template), retainer agreements (use retainer-agreement), or internal project plans. This is for client-facing scope documents.

---

## Core Principle

A SCOPE OF WORK IS A SHIELD AGAINST SCOPE CREEP — WHAT IS NOT EXPLICITLY INCLUDED IS EXCLUDED. THE MORE SPECIFIC THE SOW, THE SMOOTHER THE PROJECT.

---

## Phase 1: Project Definition

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Project name** | "What is the project?" | No default — must be provided |
| **Client** | "Who is the client?" | No default — must be provided |
| **Objective** | "What is the primary goal of this project?" | No default — must be provided |
| **Timeline** | "When does the project need to be completed?" | 4-6 weeks |
| **Budget** | "What is the project budget or fee?" | No default — must be provided |

**GATE: Confirm project scope and objectives before drafting the document.**

---

## Phase 2: SOW Document

### Scope of Work Template

```
## SCOPE OF WORK

**Project:** [Project name]
**Client:** [Client name]
**Provider:** [Your name/business]
**Date:** [Date]
**Version:** [1.0]

---

### 1. PROJECT OVERVIEW

[2-3 sentences describing the project objective, context, and expected outcome.
Focus on the business goal, not the tactical details.]

### 2. DELIVERABLES

| # | Deliverable | Description | Format | Due Date |
|---|------------|-------------|--------|----------|
| 1 | [Deliverable name] | [What it includes, specifically] | [PDF, Figma, code, etc.] | [Date] |
| 2 | [Deliverable name] | [What it includes, specifically] | [Format] | [Date] |
| 3 | [Deliverable name] | [What it includes, specifically] | [Format] | [Date] |

### 3. MILESTONES AND TIMELINE

| Phase | Description | Duration | Completion Date |
|-------|-------------|----------|----------------|
| Phase 1: Discovery | [Activities] | [X] weeks | [Date] |
| Phase 2: [Phase name] | [Activities] | [X] weeks | [Date] |
| Phase 3: [Phase name] | [Activities] | [X] weeks | [Date] |
| Phase 4: Delivery | Final deliverables and handoff | [X] weeks | [Date] |

### 4. ASSUMPTIONS

- Client will provide [specific materials, access, feedback] by [dates]
- Feedback will be provided within [X] business days of each deliverable
- [X] rounds of revisions are included per deliverable
- Project timeline assumes no delays in client approvals
- [Any technology, platform, or access assumptions]

### 5. EXCLUSIONS

The following are NOT included in this scope of work:
- [Specific task that might be assumed but is excluded]
- [Another exclusion]
- [Ongoing maintenance, support, or training unless stated]
- [Any additional work outside the deliverables listed above]

Additional work may be quoted separately upon request.

### 6. ACCEPTANCE CRITERIA

Each deliverable is considered accepted when:
- Client provides written approval (email confirmation is sufficient)
- If no response is received within [5] business days of delivery, the deliverable is deemed accepted
- Revisions requested after acceptance are billed at $[rate]/hour

### 7. FEES AND PAYMENT

- Total project fee: $[amount]
- Payment schedule:
  - [50%] upon signing: $[amount]
  - [25%] at [milestone]: $[amount]
  - [25%] upon final delivery: $[amount]
- Payment terms: Due within [X] days of invoice
- Late payment: [1.5%] per month on overdue balances

### 8. CHANGE ORDERS

Any changes to the scope, deliverables, or timeline require a written change order signed by both parties. Change orders may affect the project fee and timeline.
```

---

## Phase 3: Key Sections Deep Dive

### Writing Strong Assumptions

List everything that must be true for the project to succeed on time and on budget:

- Client-provided content, assets, or access
- Technology or platform requirements
- Response time expectations
- Decision-maker availability
- Third-party dependencies (hosting, APIs, vendors)

### Writing Clear Exclusions

Think about what the client might expect that you are NOT doing:

- Ongoing maintenance or updates after delivery
- Content creation (if you are designing but not writing)
- Training beyond the specified sessions
- Additional revisions beyond the stated rounds
- Work on platforms or channels not listed in deliverables

### Revision Rounds

Define revisions precisely:
- What counts as "one round" of revisions (consolidated feedback, not drip-fed changes)
- How many rounds are included (typically 2-3)
- What happens after included revisions are exhausted (hourly rate for additional changes)
- Revision turnaround time from provider side

---

## Phase 4: Review & Finalization

### SOW Checklist

- [ ] Project objective is clearly stated in business terms
- [ ] Every deliverable is specific, measurable, and has a due date
- [ ] Milestones align with the payment schedule
- [ ] All assumptions are documented
- [ ] Exclusions cover likely "but I thought that was included" scenarios
- [ ] Acceptance criteria are defined
- [ ] Payment schedule and late fees are specified
- [ ] Change order process is included
- [ ] Both parties have signature lines
- [ ] Version number is included for tracking revisions

### Presentation

Save the SOW in a professional format and present it alongside the proposal or contract. The SOW is often an attachment or exhibit to the master service agreement.

---

## Anti-Patterns

- **Vague deliverables** — "website design" could mean 3 pages or 30. Specify page count, functionality, and content responsibility.
- **No exclusions section** — omitting exclusions guarantees the client will assume everything is included.
- **Payment 100% on completion** — never start a project without an upfront deposit. Split payments across milestones.
- **Unlimited revisions** — this is an invitation for endless rework. Cap revision rounds explicitly.
- **No change order clause** — without a process for scope changes, every request becomes a negotiation.
- **Verbal scope agreements** — if it is not written in the SOW, it does not exist. Document everything.

---

## Recovery

- **Client wants to add deliverables mid-project:** Reference the change order clause. Quote the additional work separately with timeline impact.
- **Client delays feedback:** Reference the assumption about response times. Formally notify that delays push the project timeline accordingly.
- **Disagreement on what was included:** Point to the specific deliverables table and exclusions list. This is why specificity matters.
- **Project running over budget:** Review whether scope has expanded beyond the SOW. If so, issue a change order. If not, absorb the cost and adjust future estimates.
- **Client refuses to sign SOW:** Do not start work without a signed scope document. Offer to discuss and revise, but protect yourself.
