---
name: email-triage
description: "Triage an inbox into reply, schedule, delegate, or drop, without pretending every message is urgent. Use when the user mentions email triage, inbox zero help, prioritize email, what should I answer, or asks for a email triage. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'email-triage' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Email Triage

Triage an inbox into reply, schedule, delegate, or drop, without pretending every message is urgent.

## When to use this skill

Use this skill when the user:

- email triage
- inbox zero help
- prioritize email
- what should I answer

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Productivity systems serve the person's actual constraints. Do not recommend surveillance of colleagues or hidden monitoring.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The messages or summaries
- Deadlines they contain
- Your role
- What can be delegated

## Workflow


### 1. Step 1

Sort by real deadline and by whether a person is blocked.
### 2. Step 2

Draft replies only where a decision or fact is needed.
### 3. Step 3

Schedule work that does not need a same-day reply.
### 4. Step 4

Delegate with context, not by forwarding a puzzle.
### 5. Step 5

Drop or file noise.
### 6. Step 6

Do not write deceptive delays or fake out-of-office claims.

## Output

Deliver a **email triage**.

- Purpose of this email triage, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Mara Chen, founder at Northline Studio in Calgary, needs an email triage by 30 September 2026. A triage plan answers newsletters before a customer blocked on a decision.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A triage plan answers newsletters before a customer blocked on a decision.

The messages or summaries: Friday review block, recorded 14 September 2026. No supporting file attached
Deadlines they contain: 30 September 2026
Your role: Q4 objective 2, recorded 14 September 2026. No supporting file attached
What can be delegated: Q4 objective 2, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Email triage — draft ready to send**

> To: the recipient named in the file
> From: Mara Chen, founder, Northline Studio
> Date: 14 September 2026

---

Hello,

Answers the blocked customer first and files the newsletters.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Mara Chen
founder, Northline Studio

---

**How this draft was checked**

1. **Sort by real deadline and by whether a person is blocked**
2. **Draft replies only where a decision or fact is needed**
3. **Schedule work that does not need a same-day reply**
4. **Delegate with context, not by forwarding a puzzle**

**Deliberately not done**
- Treating all mail as urgent.
- A forward with no context.
- A fake out-of-office.

Next: Mara Chen sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Treating all mail as urgent
- A forward with no context
- A fake out-of-office

## Related skills

- `support-macro`
- `weekly-review`
