---
name: founder-operating-review
description: "Run a weekly founder review of cash, pipeline, and the one bottleneck. Use when the user mentions founder review, weekly startup review, founder operating, what matters this week, or asks for a weekly founder review. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'founder-operating-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Founder Operating Review

Run a weekly founder review of cash, pipeline, and the one bottleneck.

## When to use this skill

Use this skill when the user:

- founder review
- weekly startup review
- founder operating
- what matters this week

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Startup advice is a set of choices, not a promise of funding or growth. Do not invent traction, customers, or investor interest.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Cash facts
- Pipeline or user facts
- The bottleneck
- The team's capacity

## Workflow


### 1. Step 1

Open with cash and the date it changes, from their numbers.
### 2. Step 2

One growth fact, sourced.
### 3. Step 3

Name the bottleneck in the system, not in a person's character.
### 4. Step 4

Choose one move for the week.
### 5. Step 5

Park new ideas that do not relieve the bottleneck.
### 6. Step 6

Do not add fake momentum for morale.

## Output

Deliver a **weekly founder review**.

- Purpose of this weekly founder review, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a weekly founder review by 30 September 2026. A review adds five new ideas while payroll is the unresolved issue.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A review adds five new ideas while payroll is the unresolved issue.

Cash facts: CAD 220,000 counted 14 September 2026
Pipeline or user facts: the one named in the ask. Version and owner not recorded
The bottleneck: First four paying accounts, recorded 14 September 2026. No supporting file attached
The team's capacity: two people on shift, one off
```

### Example outcome

**Weekly founder review**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps payroll as the bottleneck and parks the new ideas.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Cash facts | CAD 220,000 counted 14 September 2026 | Needs confirmation |
| Pipeline or user facts | the one named in the ask. Version and owner not recorded | Carried into the draft |
| The bottleneck | First four paying accounts, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The team's capacity | two people on shift, one off | Needs confirmation |

**How this draft was built**

**1. Open with cash and the date it changes, from their numbers**

**2. One growth fact, sourced**

**3. Name the bottleneck in the system, not in a person's character**

**4. Choose one move for the week**

**5. Park new ideas that do not relieve the bottleneck**

**Deliberately not done**
- Fake momentum.
- A character attack.
- Ten priorities.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Fake momentum
- A character attack
- Ten priorities

## Related skills

- `runway-and-burn`
- `weekly-review`
