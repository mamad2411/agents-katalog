---
name: dispatch-plan
description: "Plan a dispatch from orders, hours, and equipment limits the user stated. Use when the user mentions dispatch plan, route plan, fleet dispatch, delivery plan, or asks for a dispatch plan. Transport and logistics operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: transport
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'dispatch-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Dispatch Plan

Plan a dispatch from orders, hours, and equipment limits the user stated.

## When to use this skill

Use this skill when the user:

- dispatch plan
- route plan
- fleet dispatch
- delivery plan

## When not to use this skill

- Concealing hours or cargo
- Evading inspections

## Professional boundary

Transport plans follow hours, load, and safety rules the user states. Do not advise concealment of cargo or evasion of inspections.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Orders
- Hours rules they follow
- Equipment limits
- Known delays

## Workflow


### 1. Step 1

Assign work inside the hours and equipment limits they stated.
### 2. Step 2

Do not advise concealing hours or cargo.
### 3. Step 3

Show which order slips if a vehicle is down.
### 4. Step 4

Name the customer promise at risk.
### 5. Step 5

Include a check-in rule.
### 6. Step 6

Replan from actual departures, not from the morning hope.

## Output

Deliver a **dispatch plan**.

- Purpose of this dispatch plan, in two sentences.
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

Luis Ortega, dispatch lead at Kite Freight in Calgary, needs a dispatch plan by 30 September 2026. A dispatcher is told to log a break that did not happen so the route stays legal on paper.

### Example data

```text
From: Luis Ortega, dispatch lead
Organization: Kite Freight, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A dispatcher is told to log a break that did not happen so the route stays legal on paper.

Orders: Load tally 118, last reviewed 14 September 2026. No owner named since
Hours rules they follow: two people, 8 hours each
Equipment limits: Hours-of-service log, last reviewed 14 September 2026. No owner named since
Known delays: Load tally 118. Stated in the ask, not documented anywhere else
```

### Example outcome

**Dispatch plan**
To: Luis Ortega, dispatch lead, Kite Freight
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the false log and shows which order must move instead.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Orders | Load tally 118, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Hours rules they follow | two people, 8 hours each | Carried into the draft |
| Equipment limits | Hours-of-service log, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Known delays | Load tally 118. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Assign work inside the hours and equipment limits they stated**

**2. Do not advise concealing hours or cargo**

**3. Show which order slips if a vehicle is down**

**4. Name the customer promise at risk**

**5. Include a check-in rule**

**Deliberately not done**
- Concealed hours.
- A plan over a stated limit.
- No view of the slipped order.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Luis Ortega by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Concealed hours
- A plan over a stated limit
- No view of the slipped order

## Related skills

- `logistics-exception`
- `schedule-look-ahead`
