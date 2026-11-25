---
name: escalation-procedure
description: "Defines escalation procedures with trigger criteria, escalation levels, response time requirements, and resolution tracking for support issues."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Escalation Procedure

## When to Use This Skill

Use this skill when you need to:
- Define when and how support issues should be escalated
- Create tiered escalation levels with clear trigger criteria
- Set response time requirements for each escalation level
- Build resolution tracking for escalated issues

**DO NOT** use this skill for complaint resolution frameworks, crisis communication, or change management. This is for defining the operational escalation path.

---

## Core Principle

ESCALATION IS NOT FAILURE — IT IS A SYSTEM THAT ENSURES THE RIGHT PERSON HANDLES THE RIGHT ISSUE AT THE RIGHT TIME, PREVENTING SMALL PROBLEMS FROM BECOMING BIG ONES.

---

## Phase 1: Define Scope

Understand the current support structure and pain points.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Team structure** | "Who handles customer issues? (just you, team, contractors)" | Solopreneur |
| **Support channels** | "Where do issues come in? (email, chat, phone, social)" | Email |
| **Issue types** | "What types of issues do you deal with?" | No default |
| **Current pain** | "What happens when an issue is too complex or urgent for the front line?" | Ad hoc / handled personally |
| **External resources** | "Do you have specialists, lawyers, accountants, or tech support you can escalate to?" | Limited |

**GATE: Confirm scope before building the procedure.**

---

## Phase 2: Build Escalation Structure

Define escalation levels, triggers, and response requirements.

### Escalation Levels

```
## Escalation Levels

### Level 1: Front Line
**Handled by:** [Support person / VA / You]
**Scope:** Standard questions, known issues, documented solutions
**Response time:** Within [4 hours]
**Resolution target:** Within [1 business day]

### Level 2: Specialist
**Handled by:** [Business owner / Senior team member / Subject matter expert]
**Scope:** Complex issues, unresolved L1 issues, technical problems
**Response time:** Within [2 hours]
**Resolution target:** Within [2 business days]

### Level 3: Executive
**Handled by:** [Business owner / Legal / External specialist]
**Scope:** Critical incidents, legal threats, data breaches, major service failures
**Response time:** Within [1 hour]
**Resolution target:** Within [24 hours for acknowledgment, varies for resolution]
```

### Escalation Trigger Matrix

```
## When to Escalate

| Trigger | From | To | Timeframe |
|---------|------|----|-----------|
| Issue unresolved after [X] hours | L1 | L2 | Automatic |
| Customer requests a manager | L1 | L2 | Immediate |
| Issue involves financial loss over $[X] | L1 | L2 | Immediate |
| Customer mentions legal action | Any | L3 | Immediate |
| Data breach or security incident | Any | L3 | Immediate |
| Same issue reported by 3+ customers | L1 | L2 | Within 1 hour |
| Negative public review/social mention | L1 | L2 | Within 1 hour |
| Issue exceeds L2 authority or expertise | L2 | L3 | Immediate |
| VIP customer issue | L1 | L2 | Immediate |
```

### Escalation Process

```
## How to Escalate

### Step 1: Document
Before escalating, capture:
- Customer name and contact info
- Full issue description
- What has been tried so far
- Customer's emotional state (calm, frustrated, angry)
- Urgency assessment

### Step 2: Notify
Contact the next level using [method]:
- L1 → L2: [Slack message / Email with "ESCALATION" subject / Direct call]
- L2 → L3: [Phone call + email documentation]

### Step 3: Hand Off
- Introduce the customer to the new handler (do not make them repeat everything)
- Transfer the documentation
- Set expectation with the customer: "I am connecting you with [Name] who specializes in this."

### Step 4: Track
- Log the escalation in [tracking tool/spreadsheet]
- Set a follow-up reminder
- Confirm resolution was achieved
```

**GATE: Present escalation structure for review.**

---

## Phase 3: Communication Templates

Create the messages used during escalation.

### Customer Communication

**Escalation Notification:**
```
Hi [Name],

I want to make sure you get the best possible help on this. I am bringing in [Name/Role] who has more expertise in [issue area].

They will reach out to you within [timeframe]. In the meantime, here is what we have done so far: [summary].

You are in good hands — I will stay looped in to make sure this gets resolved.

[Name]
```

**Internal Escalation Message:**
```
## Escalation: [Customer Name]

**Level:** L1 → L2
**Urgency:** [Critical / High / Medium]
**Customer:** [Name, account details]
**Issue:** [Summary]
**Steps taken:** [What L1 already tried]
**Customer sentiment:** [Calm / Frustrated / Angry]
**Required action:** [What needs to happen]
**Deadline:** [Response time requirement]
```

---

## Phase 4: Track and Improve

Monitor escalation patterns and optimize the process.

### Escalation Tracker

```
## Escalation Log

| Date | Customer | Issue | Level | Trigger | Response Time | Resolution Time | Resolved? |
|------|----------|-------|-------|---------|--------------|----------------|-----------|
| | | | | | | | |
```

### Monthly Escalation Review

1. How many escalations this month? Trending up or down?
2. What is the most common escalation trigger?
3. Are escalated issues being resolved within target times?
4. Can any L2 issues be prevented by improving L1 training or documentation?
5. Were any escalations unnecessary? (Could have been resolved at L1)

### Reducing Escalations

For each common escalation type, ask:
- Can L1 be empowered with more authority to resolve this?
- Is there a knowledge base article that could prevent this?
- Is the root cause a product or process issue that should be fixed?

---

## Anti-Patterns

- **No clear triggers** — if "escalate when it feels right" is the policy, issues will be escalated too late or not at all.
- **Escalation as punishment** — escalating should not feel like failure. It is the system working correctly.
- **Customer repeats their story** — every escalation must include documentation so the customer does not start from zero.
- **No response time requirements** — escalated issues without deadlines drift. Every level needs a time commitment.
- **Escalating to avoid responsibility** — escalation is for issues beyond your scope, not for issues you do not feel like handling.

---

## Recovery

- **User is the only person (no one to escalate to):** Create a tiered response system based on issue severity. For L3 issues, build a network of external specialists (lawyer, accountant, tech expert).
- **Escalations are too frequent:** L1 needs better training, tools, or authority. The most common escalation types should become L1-resolvable.
- **Escalated issues still take too long:** Add response time alerts. If L2 does not respond within the window, auto-escalate to L3.
- **Customer is angry about being transferred:** Improve the handoff — always warm-transfer with context, never cold-transfer.
- **No tracking system:** Start with a simple spreadsheet. Even basic tracking reveals patterns that improve the process.
