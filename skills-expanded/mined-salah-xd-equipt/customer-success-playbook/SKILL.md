---
name: customer-success-playbook
description: "Creates customer success playbooks with lifecycle stages, touchpoint cadence, and expansion opportunity identification for retention and growth."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Customer Success Playbook

## When to Use This Skill

Use this skill when you need to:
- Design a proactive customer success program with defined touchpoints
- Map the customer lifecycle from onboarding through renewal and expansion
- Create playbooks for common scenarios (new customer, at-risk, expansion-ready)
- Standardize how you nurture and retain customers long-term

**DO NOT** use this skill for customer onboarding flows (use onboarding-flow), support templates, or sales processes. This is for the ongoing success strategy across the full customer lifecycle.

---

## Core Principle

CUSTOMER SUCCESS IS NOT REACTIVE SUPPORT — IT IS A PROACTIVE SYSTEM THAT ENSURES CUSTOMERS ACHIEVE THEIR GOALS WITH YOUR PRODUCT, BECAUSE THEIR SUCCESS IS YOUR RETENTION.

---

## Phase 1: Lifecycle Definition

Map the customer journey from purchase to advocacy.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business model** | "Subscription, project-based, retainer, or product?" | Subscription |
| **Average customer lifetime** | "How long does a typical customer stay?" | 12 months |
| **Revenue per customer** | "Average revenue per customer per year?" | No default |
| **Churn rate** | "What percentage of customers leave per year?" | Unknown |
| **Current touchpoints** | "When do you proactively reach out to customers today?" | Rarely / only when they contact us |
| **Success definition** | "What outcome means a customer is successful with your product?" | No default |

**GATE: Confirm lifecycle context before designing the playbook.**

---

## Phase 2: Design Playbooks

Create stage-specific playbooks for the customer lifecycle.

### Lifecycle Stages

```
## Customer Lifecycle Map

| Stage | Duration | Goal | Key Metric |
|-------|----------|------|-----------|
| Onboarding | Days 1-30 | First value realization | Time to first win |
| Adoption | Days 30-90 | Regular usage established | Feature adoption rate |
| Growth | Months 3-9 | Expanded usage and value | Expansion revenue |
| Renewal | Month 9-12 | Retention and commitment | Renewal rate |
| Advocacy | Ongoing | Referrals and testimonials | Referral count, NPS |
```

### Stage Playbooks

**Onboarding Playbook:**
```
## Onboarding (Days 1-30)

**Touchpoints:**
- Day 1: Welcome email + first action prompt
- Day 3: Check-in — did they complete first action?
- Day 7: Quick call or video to confirm progress
- Day 14: Milestone check — are they using key features?
- Day 30: Onboarding review — health score baseline

**Success signals:** Completed setup, used core feature 3+ times, asked questions
**Risk signals:** No login after Day 3, no response to check-ins, support ticket filed
```

**Adoption Playbook:**
```
## Adoption (Days 30-90)

**Touchpoints:**
- Monthly check-in email with usage tips
- Day 45: Share a relevant case study or best practice
- Day 60: Proactive value review ("Here is what you have achieved so far")
- Day 90: Quarterly business review (formal or informal)

**Success signals:** Regular usage, exploring advanced features, positive feedback
**Risk signals:** Declining usage, no response to outreach, complaints about value
```

**Growth Playbook:**
```
## Growth (Months 3-9)

**Touchpoints:**
- Monthly value-add email (tips, features, industry insights)
- Quarterly business review
- Feature announcements relevant to their use case
- Expansion conversation when usage signals readiness

**Expansion triggers:**
- Customer hits usage limits
- Customer asks about additional features
- Customer's team or business is growing
- Customer achieves original goal and needs new ones
```

**Renewal Playbook:**
```
## Renewal (Month 9-12)

**Touchpoints:**
- Month 9: Pre-renewal health check and value summary
- Month 10: Renewal conversation with ROI data
- Month 11: Formal renewal proposal
- Month 12: Renewal confirmation or save conversation

**Renewal preparation:**
1. Compile value delivered (metrics, outcomes, usage data)
2. Identify any unresolved issues and fix them before renewal
3. Prepare expansion offer if appropriate
4. Have a save playbook ready if they hesitate
```

**GATE: Present playbooks for review and customization.**

---

## Phase 3: Touchpoint Content

Write the key messages and templates.

### Quarterly Business Review Template

```
## Quarterly Business Review: [Customer Name]

**Period:** [Quarter]
**Prepared by:** [Your name]

### Value Delivered
- [Metric 1: What they achieved using your product]
- [Metric 2: Time saved, revenue generated, problems solved]
- [Metric 3: Progress toward their stated goal]

### Usage Highlights
- [Feature/service usage data]
- [Adoption milestones reached]

### Recommendations
1. [Suggestion to deepen usage]
2. [Feature they have not tried yet]
3. [Best practice from similar customers]

### Next Quarter Goals
- [Goal aligned with their business objectives]
```

### Save Conversation Framework

When a customer signals they may leave:

1. **Listen first** — understand the real reason (do not sell)
2. **Acknowledge** — validate their concern
3. **Address** — present a specific solution to their issue
4. **Offer** — if appropriate, provide a concession (discount, pause, service credit)
5. **Follow up** — regardless of outcome, check in within 1 week

---

## Phase 4: Measure

Track the effectiveness of the customer success program.

### Success Metrics

```
## Customer Success Dashboard

| Metric | Target | Current |
|--------|--------|---------|
| Gross retention rate | 90%+ | — |
| Net revenue retention | 100%+ | — |
| Time to first value | Under [X] days | — |
| Quarterly business review completion | 80%+ | — |
| NPS score | 50+ | — |
| Expansion rate | [X]% of customers | — |
```

### Monthly Review

1. Which customers moved between lifecycle stages?
2. Are touchpoints happening on schedule?
3. Which playbook actions are driving the best outcomes?
4. Are there new risk signals to add to the playbooks?

---

## Anti-Patterns

- **Reactive only** — waiting for customers to contact you means you have already lost proactive influence.
- **Same treatment for all customers** — a new customer and a 2-year customer need different touchpoints. Stage matters.
- **Touchpoints without value** — "Just checking in" emails with no content get ignored. Every touchpoint must deliver value.
- **Ignoring expansion signals** — customers who hit usage limits and ask about features are buying signals. Do not miss them.
- **No renewal preparation** — starting the renewal conversation 30 days out is too late. Start at 90 days.

---

## Recovery

- **User has no customer data:** Start with a simple spreadsheet: customer name, start date, last contact, health status (green/yellow/red). Build from there.
- **User has too many customers to manage individually:** Automate low-touch stages (onboarding emails, usage tips). Reserve manual effort for at-risk and expansion-ready accounts.
- **Churn rate is high and unknown cause:** Start with exit interviews for the next 5 churned customers. The patterns will emerge quickly.
- **User is the only person doing customer success:** Focus on the highest-value customers first. Automate or templatize everything possible.
- **Customers do not respond to check-ins:** Change the channel, the timing, or the content. A "Here is what you achieved" email gets more response than "Just checking in."
