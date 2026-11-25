---
name: retrospective
description: "Run a retrospective that produces one system change, not a pile of feelings and no owner. Use when the user mentions retrospective, retro, iteration review of process, what should we change, or asks for a retrospective. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'retrospective' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Retrospective

Run a retrospective that produces one system change, not a pile of feelings and no owner.

## When to use this skill

Use this skill when the user:

- retrospective
- retro
- iteration review of process
- what should we change

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Delivery plans are commitments only when owners and dates are real. Do not fabricate status to make a report look healthy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What happened in the period
- What the team already tried
- The metric or pain
- Time available

## Workflow


### 1. Step 1

Open with the sprint goal or project outcome, so the retro is about the work.
### 2. Step 2

Collect observations, not character judgments.
### 3. Step 3

Cluster and pick one change the team can finish next cycle.
### 4. Step 4

Write the change as an experiment with a check.
### 5. Step 5

Assign an owner.
### 6. Step 6

Park the rest. A retro with ten actions will repeat itself.

## Output

Deliver a **retrospective**.

- Purpose of this retrospective, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a retrospective by 30 September 2026. A retro produces a list of twelve improvements every sprint and none are present the next week.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A retro produces a list of twelve improvements every sprint and none are present the next week.

What happened in the period: month ending 14 September 2026
What the team already tried: two people on shift, one off
The metric or pain: plan 170, actual 90
Time available: five working days, due 30 September 2026
```

### Example outcome

**Retrospective**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
One owned experiment and an explicit parking of the other eleven.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What happened in the period | month ending 14 September 2026 | Needs confirmation |
| What the team already tried | two people on shift, one off | Carried into the draft |
| The metric or pain | plan 170, actual 90 | Carried into the draft |
| Time available | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Open with the sprint goal or project outcome, so the retro is about the work**

**2. Collect observations, not character judgments**

**3. Cluster and pick one change the team can finish next cycle**

**4. Write the change as an experiment with a check**

**5. Assign an owner**

**Deliberately not done**
- A blame round.
- Ten actions.
- No check on the chosen change.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A blame round
- Ten actions
- No check on the chosen change

## Related skills

- `continuous-improvement`
- `lessons-learned`
