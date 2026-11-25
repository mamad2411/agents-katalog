---
name: freelancer-management
description: "Creates systems for managing multiple freelancers with briefing templates, feedback processes, payment workflows, and quality control. Use when scaling with contract talent."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Freelancer Management

## When to Use This Skill

Use this skill when you need to:
- Build a system to manage multiple freelancers consistently
- Create briefing templates that reduce revision cycles
- Design payment and invoicing workflows for contract workers
- Establish quality standards and feedback processes for freelance talent

**DO NOT** use this skill for full-time employee management, vendor procurement, or agency hiring. This is for managing individual freelancers and contractors.

---

## Core Principle

CLEAR BRIEFS AND CONSISTENT PROCESSES ELIMINATE 80% OF FREELANCER MANAGEMENT PROBLEMS — INVEST TIME UPFRONT TO SAVE TIME ON EVERY PROJECT.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Freelancer types** | "What roles do your freelancers fill? (writers, designers, developers, VAs)" | Must be provided |
| **Number of freelancers** | "How many freelancers are you managing?" | 3-5 |
| **Project frequency** | "How often do you assign work? (daily, weekly, per project)" | Weekly |
| **Current pain points** | "What's going wrong? (missed deadlines, quality issues, communication gaps)" | General disorganization |
| **Payment method** | "How do you pay? (PayPal, wire, platform-based, invoicing)" | Invoicing monthly |
| **Tools used** | "What tools do you use for project management and communication?" | Slack and email |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Design

### Management System Components

1. **Onboarding checklist** — what every new freelancer needs before first assignment
2. **Briefing template** — standardized project briefs by role type
3. **Communication protocol** — channels, response times, check-in cadence
4. **Feedback framework** — structured review process for deliverables
5. **Payment workflow** — invoicing, approval, payment schedule
6. **Performance tracking** — quality scores, reliability metrics, rate history

**GATE: Present the system design and get approval before building templates.**

---

## Phase 3: Build

### Deliverables

**1. Freelancer Onboarding Package**
- Welcome message template with expectations and key contacts
- Brand and style guidelines summary
- Tool access and login instructions checklist
- Sample brief and sample deliverable for reference

**2. Project Brief Template (per role type)**
- Project name and deadline
- Objective and context (why this matters)
- Specific deliverables with format requirements
- Reference materials and examples
- Revision policy (number of rounds included)
- Approval workflow (who reviews, timeline)

**3. Feedback and Revision Framework**
- First-pass review checklist per deliverable type
- Structured feedback format: what works, what needs changing, priority of changes
- Revision request template with deadline
- Quality scoring rubric (1-5 on criteria relevant to the role)

**4. Payment and Admin System**
- Invoice template with required fields
- Payment schedule (net 15, net 30, or milestone-based)
- Expense approval process if applicable
- Tax document checklist (W-9, contractor agreement)

**5. Freelancer Roster Tracker**
- Contact info, rates, specialties, availability
- Project history and quality scores
- Preferred communication channel
- Contract renewal dates

---

## Phase 4: Polish

### Performance Review Cadence

- After every project: quick quality score (1-5)
- Monthly: review aggregate scores and identify top and underperforming freelancers
- Quarterly: rate renegotiation conversations if warranted
- Annually: roster cleanup — keep, develop, or replace

### Scaling Checklist

When ready to add more freelancers, verify: templates are documented, quality standards are clear, and onboarding can run without the founder's direct involvement.

---

## Example 1: Content Team (3 writers, weekly blog posts)

Brief template includes: topic, target keyword, word count, tone reference, internal links, deadline. Feedback uses editorial markup in Google Docs. Payment: monthly invoice, net 15.

## Example 2: Design Support (2 designers, project-based)

Brief template includes: deliverable type, dimensions, brand guidelines link, reference examples, file format requirements. Feedback via Figma comments. Payment: per project, 50% upfront / 50% on delivery.

---

## Anti-Patterns

- **Vague briefs** — "Make it pop" is not a brief. Specific requirements reduce revisions by 70%.
- **No revision limits** — unlimited revisions incentivize sloppy first drafts. Set clear limits (2 rounds included).
- **Payment delays** — freelancers who chase invoices deprioritize your work. Pay on time, every time.
- **Single point of dependency** — relying on one freelancer for a critical function is risky. Have a backup.
- **Micromanaging process** — hire for output, not hours. Do not require freelancers to track time unless billing hourly.

---

## Recovery

- **Consistent quality issues:** Review your briefs first. If briefs are clear and quality is still low, provide examples of good vs. bad work and set a trial period.
- **Freelancer ghosts mid-project:** Always have a backup contact for critical roles. Build a clause for communication expectations into contracts.
- **Budget too tight for good talent:** Pay fewer freelancers better rates rather than many freelancers at rock-bottom rates.
- **Scaling beyond founder management:** Document all processes so a project manager or VA can run the system.
