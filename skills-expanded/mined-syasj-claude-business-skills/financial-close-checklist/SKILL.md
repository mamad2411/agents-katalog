---
name: financial-close-checklist
description: "Tighten a monthly close so the numbers arrive once, with owners, and with fewer heroic journals. Use when the user mentions month-end close, financial close, close checklist, why is the close late, or asks for a close checklist. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'financial-close-checklist' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Financial Close Checklist

Tighten a monthly close so the numbers arrive once, with owners, and with fewer heroic journals.

## When to use this skill

Use this skill when the user:

- month-end close
- financial close
- close checklist
- why is the close late

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not investment, tax, or financial advice. Do not invent rates of return, tax rates, or valuation multiples. A qualified finance professional must review any decision that moves money.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Current close calendar
- Late or repeated tasks
- Systems involved
- Who signs off

## Workflow


### 1. Map day zero to sign-off

List tasks in order, with the predecessor each task waits on.
### 2. Assign one owner

A task owned by a team is a task that slips. Name a person the user identifies, or mark owner unknown.
### 3. Move work before day one

Recurring reconciliations that can start earlier should. Say which ones.
### 4. Define materiality for journals

Not every difference deserves an entry. Use the user's threshold or propose one as a proposal.
### 5. Add a flux review

A short review of movements before sign-off, aimed at surprises, not at reprinting the ledger.
### 6. Measure the close

Days to sign-off and number of post-close fixes. Improving the close is an operations problem.

## Output

Deliver a **close checklist**.

- Purpose of this close checklist, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a close checklist by 30 September 2026. The close takes 15 business days and three reconciliations always land on the last afternoon.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The close takes 15 business days and three reconciliations always land on the last afternoon.

Current close calendar: two deals cited from memory. Neither has a written loss reason
Late or repeated tasks: The close takes 15 business days and three reconciliations always land on the last afternoon. Stated once, in the ask. Not written down anywhere else
Systems involved: the one named in the ask. Version and owner not recorded
Who signs off: Mara Chen, founder
```

### Example outcome

**Close checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
A sequenced checklist, earlier starts for the late reconciliations, and two measures of close health.

**Checklist**

- [x] **Current close calendar** — two deals cited from memory. Neither has a written loss reason  
      Evidenced in the file
- [x] **Late or repeated tasks** — The close takes 15 business days and three reconciliations always land on the last afternoon. Stated once, in the ask. Not written down anywhere else  
      Evidenced in the file
- [x] **Systems involved** — the one named in the ask. Version and owner not recorded  
      Evidenced in the file
- [ ] **Who signs off** — Mara Chen, founder  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Map day zero to sign-off
2. Assign one owner
3. Move work before day one
4. Define materiality for journals
5. Add a flux review

**Deliberately not done**
- A checklist copied from a generic calendar that ignores their systems.
- Sign-off with no flux review.
- Heroic journals every month treated as normal.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Mara Chen closes the open items before 30 September 2026.

## Anti-patterns

- A checklist copied from a generic calendar that ignores their systems.
- Sign-off with no flux review.
- Heroic journals every month treated as normal.

## Related skills

- `month-end-close`
- `journal-entry-review`
- `management-reporting-pack`
