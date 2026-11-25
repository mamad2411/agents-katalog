---
name: service-recovery-plan
description: "Designs service recovery protocols for when things go wrong with response scripts, compensation guidelines, and follow-up procedures."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Service Recovery Plan

## When to Use This Skill

Use this skill when you need to:
- Design proactive protocols for recovering from service failures
- Create response scripts and compensation guidelines for different failure types
- Build follow-up procedures that turn service failures into loyalty opportunities
- Standardize how your business handles things when they go wrong

**DO NOT** use this skill for individual complaint responses (use complaint-resolution), crisis communication, or business continuity planning. This is for designing the overall service recovery system.

---

## Core Principle

THE SERVICE RECOVERY PARADOX IS REAL — CUSTOMERS WHO EXPERIENCE A FAILURE THAT IS WELL-RECOVERED OFTEN BECOME MORE LOYAL THAN CUSTOMERS WHO NEVER HAD A PROBLEM.

---

## Phase 1: Failure Inventory

Identify what can go wrong and how often it does.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What product or service do you provide?" | No default |
| **Common failures** | "What are the top 5 things that go wrong for customers?" | No default |
| **Current recovery** | "How do you handle things when they go wrong today?" | Ad hoc |
| **Compensation budget** | "What can you afford to offer when you fail? (refunds, credits, free work)" | Flexible |
| **Past incidents** | "Describe the worst service failure you have experienced." | No default |

### Failure Classification

```
## Service Failure Types

| Failure Type | Severity | Frequency | Impact on Customer | Example |
|-------------|----------|-----------|-------------------|---------|
| Delivery delay | Medium | [H/M/L] | Inconvenience | Deliverable 3 days late |
| Quality issue | High | [H/M/L] | Rework or dissatisfaction | Deliverable does not meet brief |
| Communication gap | Low-Medium | [H/M/L] | Confusion or frustration | No update for 1 week |
| Billing error | Medium | [H/M/L] | Financial impact | Overcharged or double-billed |
| Complete failure | Critical | [Low] | Major business impact | Service not delivered at all |
```

**GATE: Confirm failure inventory before building recovery plans.**

---

## Phase 2: Recovery Protocols

Design specific recovery procedures for each failure type.

### Recovery Framework: LAER

```
## LAER Recovery Model

### L — Listen
Let the customer describe their experience fully. Do not interrupt or defend.
"Help me understand exactly what happened."

### A — Acknowledge
Validate their experience and take ownership.
"You are right — we did not deliver what we promised, and I take full responsibility."

### E — Execute
Deliver a specific fix with a timeline.
"Here is exactly what I am going to do and when: [action] by [date]."

### R — Recover Plus
Go beyond fixing the problem. Deliver unexpected value.
"In addition to [the fix], I am also [additional gesture]."
```

### Recovery Protocol by Failure Type

```
## Recovery Protocols

### Delivery Delay
**Acknowledge within:** 2 hours of delay becoming known
**Response script:** "I want to be upfront — your [deliverable] will be [X days] later than promised. That is on me. Here is the new timeline: [date]. [Compensation if appropriate]."
**Compensation:** 10-15% discount on current project, or priority scheduling for next project
**Follow-up:** Day of delivery + 3 days after

### Quality Issue
**Acknowledge within:** Same day as reported
**Response script:** "Thank you for flagging this. The quality is not where it should be. I am going to [redo/revise] this and have an improved version to you by [date]."
**Compensation:** Free revision + 10% credit on next project
**Follow-up:** After revision delivery + 1 week later

### Communication Gap
**Acknowledge within:** 4 hours
**Response script:** "You should not have had to chase me for an update. I apologize for the silence. Here is the current status: [update]. Going forward, I will [new communication commitment]."
**Compensation:** Usually not needed — improved communication is the recovery
**Follow-up:** Proactive update within 48 hours

### Billing Error
**Acknowledge within:** Same day
**Response script:** "You are right — there was a billing error. I have [corrected it / issued a refund] immediately. You should see [amount] back in your account within [timeframe]."
**Compensation:** Refund + small credit for the inconvenience
**Follow-up:** Confirm refund received within 3 days

### Complete Failure
**Acknowledge within:** Immediately
**Response script:** "I need to be honest with you — [what happened]. There is no excuse. Here is what I am doing: [full remedy]. [Significant compensation]."
**Compensation:** Full refund + redo at no cost OR full refund + additional credit
**Follow-up:** Personal call within 48 hours + 1-week check-in + 30-day check-in
```

**GATE: Present recovery protocols for review.**

---

## Phase 3: Compensation Guidelines

Define what to offer and when.

### Compensation Matrix

```
## Compensation Guidelines

| Severity | Our Fault (100%) | Shared Responsibility | Minor Inconvenience |
|----------|-----------------|----------------------|-------------------|
| Low | Apology + expedited fix | Apology + fix | Apology |
| Medium | Fix + 10-20% credit | Fix + 10% credit | Fix + goodwill gesture |
| High | Fix + 25-50% refund | Fix + 15-25% refund | Fix + 10% credit |
| Critical | Full refund + redo free | Full refund | Partial refund + fix |
```

### Compensation Rules

- Always fix the issue FIRST, then discuss compensation
- Offer compensation proactively — do not wait for the customer to demand it
- Never offer more than the total project/subscription value
- Monetary compensation for monetary impact; time compensation for time wasted
- Document all compensation for financial tracking

---

## Phase 4: Prevention and Measurement

Use recovery data to prevent future failures.

### Failure Prevention

After each recovered incident, document:
```
## Post-Incident Review

**Failure:** [What happened]
**Root cause:** [Why it happened]
**Recovery executed:** [What was done]
**Customer outcome:** [Retained / Lost / Upgraded loyalty]
**Preventive action:** [What changes to prevent recurrence]
**Owner:** [Who implements the change]
**Deadline:** [When]
```

### Recovery Metrics

```
## Service Recovery Dashboard

| Metric | Target | Current |
|--------|--------|---------|
| Mean time to acknowledge | Under [X hours] | — |
| Mean time to resolve | Under [X days] | — |
| Recovery satisfaction rate | 80%+ | — |
| Customer retention after failure | 85%+ | — |
| Repeat failure rate (same type) | Decreasing | — |
```

### Quarterly Recovery Review

1. How many service failures occurred?
2. What types are most common?
3. What is the retention rate after recovery?
4. Are preventive actions reducing failure rates?
5. Is the compensation budget on track?

---

## Anti-Patterns

- **Denying the failure** — customers know when something went wrong. Denial insults their intelligence and kills trust.
- **Over-compensating** — giving away the farm for a minor delay trains customers to expect excessive compensation.
- **Under-compensating** — a 5% discount for a catastrophic failure is insulting. Match the recovery to the impact.
- **No follow-up** — fixing the problem without following up leaves the relationship in limbo. Close the loop.
- **Same failure repeating** — if the same failure happens 3+ times, the recovery plan is not the problem — the process is.

---

## Recovery

- **User has never built a recovery plan:** Start with the single most common failure type. One protocol is better than none.
- **Customer refuses the recovery offer:** Ask what would make it right for them. Sometimes it is not about compensation — it is about being heard.
- **User cannot afford monetary compensation:** Offer non-monetary recovery: priority service, personal attention, free consultation time, early access to new features.
- **Recovery failed and customer is leaving:** Conduct a graceful exit. Ask for feedback, apologize sincerely, and leave the door open. Some customers return later.
- **Team does not follow recovery protocols:** Role-play scenarios during team meetings. Make the protocols accessible (not buried in a document no one reads).
