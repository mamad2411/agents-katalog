---
name: scenario-planning
description: "Build a small set of contrasting futures and the early signs that tell you which one you are in. Use when the user mentions scenario planning, what if, upside and downside cases, strategic scenarios, or asks for a scenario set with signposts. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'scenario-planning' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Scenario Planning

Build a small set of contrasting futures and the early signs that tell you which one you are in.

## When to use this skill

Use this skill when the user:

- scenario planning
- what if
- upside and downside cases
- strategic scenarios

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

- The decision the scenarios inform
- Two or three uncertainties that actually matter
- Time horizon
- Facts and constraints already known

## Workflow


### 1. Pick uncertainties

Choose two uncertainties the user believes could break the plan. Do not brainstorm twenty.
### 2. Build three or four futures

A base case, a downside, and an upside are enough. Name each future so people can talk about it.
### 3. Stay internally consistent

A downside case cannot also assume the best sales cycle and the cheapest hiring market unless the user says so.
### 4. Find signposts

For each scenario, name two observable signs that would tell you it is unfolding. Signs must be measurable in the user's world.
### 5. Pre-commit moves

For the downside, write the move you would make if the signpost hits, including what you would stop.
### 6. Do not pretend precision

Scenarios are stories with logic, not forecasts. Label them as such.

## Output

Deliver a **scenario set with signposts**.

- Purpose of this scenario set with signposts, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a scenario set with signposts by 30 September 2026. A services firm wants to know how to plan hiring if a key public-sector contract is delayed by two quarters.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A services firm wants to know how to plan hiring if a key public-sector contract is delayed by two quarters.

The decision the scenarios inform: A services firm wants to know how to plan hiring if a key public-sector contract is delayed by two quarters
Two or three uncertainties that actually matter: Fieldnote, recorded 14 September 2026. No supporting file attached
Time horizon: 13 weeks
Facts and constraints already known: no extra headcount, and no result that is not in this file
```

### Example outcome

**Scenario set with signposts**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Three named scenarios, the signposts for each, and a hiring move tied to the delay signpost rather than to hope.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision the scenarios inform | A services firm wants to know how to plan hiring if a key public-sector contract is delayed by two quarters | Needs confirmation |
| Two or three uncertainties that actually matter | Fieldnote, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Time horizon | 13 weeks | Carried into the draft |
| Facts and constraints already known | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Pick uncertainties**  
Choose two uncertainties the user believes could break the plan. Do not brainstorm twenty.

**2. Build three or four futures**  
A base case, a downside, and an upside are enough. Name each future so people can talk about it.

**3. Stay internally consistent**  
A downside case cannot also assume the best sales cycle and the cheapest hiring market unless the user says so.

**4. Find signposts**  
For each scenario, name two observable signs that would tell you it is unfolding. Signs must be measurable in the user's world.

**5. Pre-commit moves**  
For the downside, write the move you would make if the signpost hits, including what you would stop.

**Deliberately not done**
- A single forecast with a confidence interval dressed up as scenarios.
- Scenarios that differ only by a percentage.
- Inventing macro statistics to decorate the story.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A single forecast with a confidence interval dressed up as scenarios.
- Scenarios that differ only by a percentage.
- Inventing macro statistics to decorate the story.

## Related skills

- `strategic-plan-builder`
- `sensitivity-and-scenarios`
- `war-room-brief`
