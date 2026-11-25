---
name: complaint-resolution
description: "Creates complaint resolution frameworks with empathy scripts, escalation paths, recovery offers, and follow-up procedures for customer retention."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Complaint Resolution

## When to Use This Skill

Use this skill when you need to:
- Create a structured framework for handling customer complaints
- Write empathy scripts and response templates for common complaint types
- Define escalation paths and authority levels for resolution
- Build recovery offer guidelines and follow-up procedures

**DO NOT** use this skill for writing individual review responses (use review-response), crisis communication, or legal dispute resolution. This is for building the complaint handling system.

---

## Core Principle

A WELL-RESOLVED COMPLAINT CREATES MORE LOYALTY THAN NO COMPLAINT AT ALL — CUSTOMERS WHO FEEL HEARD AND HELPED BECOME YOUR STRONGEST ADVOCATES.

---

## Phase 1: Complaint Inventory

Understand the types and frequency of complaints.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What product or service do you provide?" | No default |
| **Common complaints** | "What are the top 5 complaints you receive?" | No default |
| **Current process** | "How do you handle complaints today?" | Ad hoc |
| **Resolution authority** | "What can you offer to resolve issues? (refunds, credits, replacements, discounts)" | Full authority (solopreneur) |
| **Response time goal** | "How quickly should complaints be acknowledged?" | Within 4 hours |

### Complaint Classification

```
## Complaint Types

| Type | Frequency | Severity | Example |
|------|-----------|----------|---------|
| Product/Service quality | [High/Med/Low] | [1-5] | [Example] |
| Delivery/Timeline | [H/M/L] | [1-5] | [Example] |
| Communication gap | [H/M/L] | [1-5] | [Example] |
| Billing/Pricing | [H/M/L] | [1-5] | [Example] |
| Expectation mismatch | [H/M/L] | [1-5] | [Example] |
```

**GATE: Confirm complaint types before building resolution framework.**

---

## Phase 2: Resolution Framework

Build the HEARD method for handling every complaint.

### The HEARD Framework

```
## Complaint Resolution: HEARD Method

### H — Hear
Listen fully without interrupting or defending. Let the customer finish.
"Tell me everything that happened."
"I want to understand the full picture."

### E — Empathize
Acknowledge their feelings before addressing the facts.
"I understand how frustrating that must be."
"That is not the experience you deserve, and I am sorry."

### A — Apologize
Take responsibility without excuses or blame-shifting.
"I am sorry this happened. We should have [specific failure]."
"You are right — we dropped the ball on [specific issue]."

### R — Resolve
Offer a specific solution with a timeline.
"Here is what I am going to do: [specific action] by [specific date]."
"I would like to offer you [resolution] to make this right."

### D — Document
Record the complaint, resolution, and follow-up plan.
Log in complaint tracker for pattern analysis.
```

### Resolution Authority Matrix

```
## Resolution Authority

| Complaint Severity | Resolution Options | Authority |
|-------------------|-------------------|-----------|
| Minor (Severity 1-2) | Apology + fix | Any team member |
| Moderate (Severity 3) | Apology + fix + small credit/discount | Team lead / owner |
| Major (Severity 4) | Full refund or replacement + apology | Owner |
| Critical (Severity 5) | Full refund + additional compensation + personal call | Owner — immediate |
```

### Response Templates by Complaint Type

**Quality Issue:**
```
Hi [Name],

Thank you for letting me know about [specific issue]. That is not the quality standard we hold ourselves to, and I am sorry.

Here is what I am doing:
- [Immediate fix — replacement, redo, correction]
- [Preventive step — what changes so it does not happen again]

[Resolution offer if appropriate]

I will follow up with you by [date] to make sure everything is right.

[Name]
```

**Timeline/Delivery Issue:**
```
Hi [Name],

You are right — we missed the [deadline/delivery date] and I understand how that impacts you.

[Brief, honest explanation — not an excuse]

Here is the updated timeline: [specific date/time].
[Compensation for the delay if applicable]

I take responsibility for this and will personally ensure the revised timeline is met.

[Name]
```

**GATE: Present framework and templates for review.**

---

## Phase 3: Escalation and Recovery

Define when and how to escalate, and what recovery looks like.

### Escalation Triggers

```
## Escalation Protocol

| Trigger | Escalate To | Timeframe |
|---------|------------|-----------|
| Customer mentions lawyer/legal | Owner | Immediately |
| Same customer complains 3+ times | Owner | Same day |
| Complaint goes public (social media, review) | Owner | Within 1 hour |
| Financial impact over $[amount] | Owner/Finance | Same day |
| Customer threatens to leave | Owner | Within 4 hours |
```

### Recovery Offer Guidelines

```
## Recovery Offer Matrix

| Severity | Our Fault | Shared Fault | Not Our Fault |
|----------|----------|-------------|--------------|
| Minor | Apology | Apology | Explanation |
| Moderate | Apology + 10-20% credit | Apology + 10% credit | Apology + goodwill gesture |
| Major | Full refund or redo | Partial refund + redo | Explanation + small gesture |
| Critical | Full refund + bonus credit | Full refund | Explanation + empathy |
```

### Follow-Up Protocol

- **48 hours after resolution:** Check in — "I wanted to make sure [resolution] worked for you."
- **1 week after resolution:** Brief follow-up — "Is everything still on track?"
- **30 days after resolution:** Final check — only for major/critical complaints

---

## Phase 4: Prevention

Use complaint data to prevent future issues.

### Complaint Tracker

```
## Complaint Log

| Date | Customer | Type | Severity | Resolution | Time to Resolve | Follow-Up Status |
|------|----------|------|----------|-----------|----------------|-----------------|
| | | | | | | |
```

### Monthly Analysis

1. How many complaints this month vs. last?
2. What type appears most frequently?
3. For the most common complaint: what systemic change would prevent it?
4. Average resolution time — is it improving?
5. Customer retention after complaint — did they stay?

### Root Cause Action Plan

When the same complaint appears 3+ times:
```
**Recurring complaint:** [Type]
**Root cause:** [Why it keeps happening]
**Systemic fix:** [Process, product, or communication change]
**Owner:** [Name]
**Deadline:** [Date]
```

---

## Anti-Patterns

- **Defending before empathizing** — explaining why something happened before acknowledging feelings feels dismissive.
- **One-size-fits-all resolution** — a 10% discount does not fix a major quality failure. Match the resolution to the severity.
- **No follow-up** — resolving the issue but never checking back misses the chance to rebuild trust.
- **Blaming the customer** — even if the customer made an error, frame the response around what you will do, not what they should have done.
- **Ignoring complaint patterns** — individual complaints are fires to put out. Patterns are systemic problems to fix.

---

## Recovery

- **Customer is extremely angry and will not calm down:** Acknowledge without matching their energy. "I hear how frustrated you are, and I want to fix this." If hostile, set a boundary: "I want to help you — let us focus on the solution."
- **User does not have budget for refunds/credits:** Offer non-monetary resolution: priority support, free consulting time, extended trial, or a personal apology call.
- **Complaint is unreasonable:** Empathize with the feeling, set clear boundaries on what you can offer, and document the interaction.
- **Same customer complains repeatedly:** Schedule a direct conversation to understand the underlying issue. Repeated complaints usually signal a fundamental mismatch.
- **User is emotionally affected by complaints:** Separate the complaint from personal identity. The complaint is about the product or service, not about you as a person.
