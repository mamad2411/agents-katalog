---
name: weekly-review
description: "Run a weekly review that closes open loops and picks next week's outcomes. Use when the user mentions weekly review, plan my week, personal review, Friday review, or asks for a weekly review. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'weekly-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Weekly Review

Run a weekly review that closes open loops and picks next week's outcomes.

## When to use this skill

Use this skill when the user:

- weekly review
- plan my week
- personal review
- Friday review

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

- Open commitments
- Calendar
- Waiting-for items
- The outcomes that matter

## Workflow


### 1. Step 1

List commitments still open.
### 2. Step 2

Close, defer, or schedule each one. A review that only worries is incomplete.
### 3. Step 3

Pick a few outcomes for next week, not a pile of tasks.
### 4. Step 4

Note what is waiting on others.
### 5. Step 5

Protect time for the outcome that slips every week.
### 6. Step 6

Do not plan a week that ignores meetings already booked.

## Output

Deliver a **weekly review**.

- Purpose of this weekly review, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a weekly review by 30 September 2026. A weekly plan has 40 tasks and 30 hours of existing meetings.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A weekly plan has 40 tasks and 30 hours of existing meetings.

Open commitments: Friday review block and one other, both unconfirmed as of 14 September 2026
Calendar: Inbox triage batch. Partly documented: the what is written down, the who is not
Waiting-for items: Friday review block. Stated in the ask, not documented anywhere else
The outcomes that matter: A weekly plan has 40 tasks and 30 hours of existing meetings. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Weekly review**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Cuts to a few outcomes and schedules them in the remaining time.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Open commitments | Friday review block and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |
| Calendar | Inbox triage batch. Partly documented: the what is written down, the who is not | Carried into the draft |
| Waiting-for items | Friday review block. Stated in the ask, not documented anywhere else | Carried into the draft |
| The outcomes that matter | A weekly plan has 40 tasks and 30 hours of existing meetings. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. List commitments still open**

**2. Close, defer, or schedule each one. A review that only worries is incomplete**

**3. Pick a few outcomes for next week, not a pile of tasks**

**4. Note what is waiting on others**

**5. Protect time for the outcome that slips every week**

**Deliberately not done**
- A wish list longer than the calendar.
- No closures.
- Ignoring booked meetings.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A wish list longer than the calendar
- No closures
- Ignoring booked meetings

## Related skills

- `founder-operating-review`
- `meeting-operating-system`
