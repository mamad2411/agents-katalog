---
name: roadmap-narrative
description: "Write a roadmap narrative that explains outcomes and sequencing, with dates only where they are real. Use when the user mentions roadmap narrative, explain the roadmap, roadmap communication, now next later, or asks for a roadmap narrative. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'roadmap-narrative' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Roadmap Narrative

Write a roadmap narrative that explains outcomes and sequencing, with dates only where they are real.

## When to use this skill

Use this skill when the user:

- roadmap narrative
- explain the roadmap
- roadmap communication
- now next later

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The outcomes
- The sequence and why
- Dates that are actually committed
- What is not on the roadmap

## Workflow


### 1. Outcomes over features

Lead with the customer or business outcome. Features are evidence of the bet, not the headline.
### 2. Now, next, later

Use this shape unless the user has a better one. Later is not a promise.
### 3. Dates

Only committed dates get dates. Everything else is a sequence without a fake quarter.
### 4. Why this order

The dependency or learning that forces the sequence.
### 5. Not on the roadmap

Items people will ask about, and the reason they wait.
### 6. Audience

A board version and a team version may differ in detail, not in truth.

## Output

Deliver a **roadmap narrative**.

- Purpose of this roadmap narrative, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a roadmap narrative by 30 September 2026. Sales wants every prospect request placed on next quarter's roadmap.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Sales wants every prospect request placed on next quarter's roadmap.

The outcomes: Sales wants every prospect request placed on next quarter's roadmap. Stated once, in the ask. Not written down anywhere else
The sequence and why: Sales wants every prospect request placed on next quarter's roadmap
Dates that are actually committed: 30 September 2026
What is not on the roadmap: Usage limit warning, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Roadmap narrative**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps uncommitted requests in later or off-roadmap, with the reason.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcomes | Sales wants every prospect request placed on next quarter's roadmap. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The sequence and why | Sales wants every prospect request placed on next quarter's roadmap | Carried into the draft |
| Dates that are actually committed | 30 September 2026 | Carried into the draft |
| What is not on the roadmap | Usage limit warning, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Outcomes over features**  
Lead with the customer or business outcome. Features are evidence of the bet, not the headline.

**2. Now, next, later**  
Use this shape unless the user has a better one. Later is not a promise.

**3. Dates**  
Only committed dates get dates. Everything else is a sequence without a fake quarter.

**4. Why this order**  
The dependency or learning that forces the sequence.

**5. Not on the roadmap**  
Items people will ask about, and the reason they wait.

**Deliberately not done**
- A feature laundry list with fake dates.
- A roadmap that hides the delays.
- Different truths for different audiences.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A feature laundry list with fake dates.
- A roadmap that hides the delays.
- Different truths for different audiences.

## Related skills

- `outcome-roadmap`
- `stakeholder-prd-review`
