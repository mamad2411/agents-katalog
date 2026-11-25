---
name: portfolio-prioritization
description: "Rank a set of initiatives by constraint, not by who argued last, and make the cut visible. Use when the user mentions prioritize initiatives, what should we stop, portfolio review, too many projects, or asks for a prioritized portfolio. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'portfolio-prioritization' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Portfolio Prioritization

Rank a set of initiatives by constraint, not by who argued last, and make the cut visible.

## When to use this skill

Use this skill when the user:

- prioritize initiatives
- what should we stop
- portfolio review
- too many projects

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The list of initiatives
- The scarce resource: people, cash, or attention
- Strategy bets
- Which items are truly mandatory

## Workflow


### 1. Name the constraint

Prioritize against the scarce resource. If everything is priority one, nothing is.
### 2. Separate mandatory from chosen

Regulatory, contractual, or safety work the user confirms as mandatory sits above discretionary bets.
### 3. Score simply

Use impact on the stated bet, cost in the scarce resource, and time to evidence. Do not use a fake-precise 14-factor model.
### 4. Make the cut

Recommend a stop, pause, and continue list. A ranking with no cut is not prioritization.
### 5. Show the losers

Write why attractive work is waiting. Silent cuts become shadow projects.
### 6. Set a reopen date

The portfolio is reviewed on a date, not whenever someone escalates.

## Output

Deliver a **prioritized portfolio**.

- Purpose of this prioritized portfolio, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a prioritized portfolio by 30 September 2026. A leadership team has 22 active initiatives and 9 managers, and wants a portfolio cut before annual planning.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A leadership team has 22 active initiatives and 9 managers, and wants a portfolio cut before annual planning.

The list of initiatives: Cedar Clinic; Lantern Inn; open item
The scarce resource: people, cash, or attention: people: in the file; cash: not in the file; attention: open
Strategy bets: 65 in the last period. No prior period attached, so no trend
Which items are truly mandatory: open item. Stated in the ask, not documented anywhere else
```

### Example outcome

**Prioritized portfolio**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A continue, pause, and stop list tied to manager capacity, with the reason each stopped item is waiting.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The list of initiatives | Cedar Clinic; Lantern Inn; open item | Needs confirmation |
| The scarce resource: people, cash, or attention | people: in the file; cash: not in the file; attention: open | Carried into the draft |
| Strategy bets | 65 in the last period. No prior period attached, so no trend | Carried into the draft |
| Which items are truly mandatory | open item. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Name the constraint**  
Prioritize against the scarce resource. If everything is priority one, nothing is.

**2. Separate mandatory from chosen**  
Regulatory, contractual, or safety work the user confirms as mandatory sits above discretionary bets.

**3. Score simply**  
Use impact on the stated bet, cost in the scarce resource, and time to evidence. Do not use a fake-precise 14-factor model.

**4. Make the cut**  
Recommend a stop, pause, and continue list. A ranking with no cut is not prioritization.

**5. Show the losers**  
Write why attractive work is waiting. Silent cuts become shadow projects.

**Deliberately not done**
- Prioritizing by executive volume.
- Keeping every project and 'focusing' in the narrative only.
- A weighted model nobody can explain.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Prioritizing by executive volume.
- Keeping every project and 'focusing' in the narrative only.
- A weighted model nobody can explain.

## Related skills

- `prioritization-rice`
- `strategic-plan-builder`
