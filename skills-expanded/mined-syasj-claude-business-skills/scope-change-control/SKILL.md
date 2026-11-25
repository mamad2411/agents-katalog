---
name: scope-change-control
description: "Write a scope change so the sponsor sees the trade before the team absorbs it silently. Use when the user mentions scope change, change request, gold plating, can we add this, or asks for a change request. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'scope-change-control' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Scope Change Control

Write a scope change so the sponsor sees the trade before the team absorbs it silently.

## When to use this skill

Use this skill when the user:

- scope change
- change request
- gold plating
- can we add this

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

- The requested change
- The current baseline
- The impact on date, cost, or scope
- The decider

## Workflow


### 1. Step 1

Restate the request and who asked.
### 2. Step 2

Show the impact on the binding constraint.
### 3. Offer options

add time, add cost, or remove something else.
### 4. Step 4

Recommend one option. Silent absorption is not an option to hide.
### 5. Step 5

Name the decider. The delivery team does not accept scope by being polite.
### 6. Step 6

Record the decision so the baseline stays honest.

## Output

Deliver a **change request**.

- Purpose of this change request, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a change request by 30 September 2026. A stakeholder adds a report and says it is tiny, with no estimate.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A stakeholder adds a report and says it is tiny, with no estimate.

The requested change: requested 14 September 2026. Not yet approved
The current baseline: Milestone 3 handover, recorded 14 September 2026. No supporting file attached
The impact on date, cost, or scope: CAD 18 direct. Overhead not in this line
The decider: Milestone 3 handover, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Change request**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the silent add and offers a trade against the baseline.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The requested change | requested 14 September 2026. Not yet approved | Needs confirmation |
| The current baseline | Milestone 3 handover, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The impact on date, cost, or scope | CAD 18 direct. Overhead not in this line | Carried into the draft |
| The decider | Milestone 3 handover, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Restate the request and who asked**

**2. Show the impact on the binding constraint**

**3. Offer options**  
add time, add cost, or remove something else.

**4. Recommend one option. Silent absorption is not an option to hide**

**5. Name the decider. The delivery team does not accept scope by being polite**

**Deliberately not done**
- Absorbing scope with no record.
- A change with no impact.
- The team acting as the decider by default.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Absorbing scope with no record
- A change with no impact
- The team acting as the decider by default

## Related skills

- `project-charter`
- `sprint-plan`
