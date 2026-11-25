---
name: champion-map
description: "Test whether a supposed champion can actually move a deal, and plan how to support them ethically. Use when the user mentions champion map, find a champion, deal coach, internal advocate, or asks for a champion map. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'champion-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Champion Map

Test whether a supposed champion can actually move a deal, and plan how to support them ethically.

## When to use this skill

Use this skill when the user:

- champion map
- find a champion
- deal coach
- internal advocate

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The person the seller thinks is the champion
- Evidence of their influence
- What they have asked for
- The economic buyer

## Workflow


### 1. Define champion

Someone with access, influence, and a personal reason to see the problem solved. Friendship is not enough.
### 2. Evidence

What they have done: introduced a buyer, shared criteria, or scheduled a working session. Intentions do not count.
### 3. Gap

If they cannot reach the economic buyer, write the introduction you still need.
### 4. Support

Give them materials that are true. Do not ask them to hide facts from their employer.
### 5. Multi-thread

Name one other relationship to build so the deal is not a single point of failure.
### 6. Relabel

If the evidence is thin, call them a coach or a user, not a champion.

## Output

Deliver a **champion map**.

- Purpose of this champion map, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a champion map by 30 September 2026. The day-to-day user replies quickly but has never met procurement, and the seller calls them the champion.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The day-to-day user replies quickly but has never met procurement, and the seller calls them the champion.

The person the seller thinks is the champion: Harbor Goods, recorded 14 September 2026. No supporting file attached
Evidence of their influence: one PDF, 2 pages, dated 14 September 2026
What they have asked for: The day-to-day user replies quickly but has never met procurement, and the seller calls them the champion
The economic buyer: Redline Parts
```

### Example outcome

**Champion map**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Relabels the user as a coach and names the missing introduction to the economic buyer.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The person the seller thinks is the champion | Harbor Goods, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Evidence of their influence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| What they have asked for | The day-to-day user replies quickly but has never met procurement, and the seller calls them the champion | Carried into the draft |
| The economic buyer | Redline Parts | Needs confirmation |

**How this draft was built**

**1. Define champion**  
Someone with access, influence, and a personal reason to see the problem solved. Friendship is not enough.

**2. Evidence**  
What they have done: introduced a buyer, shared criteria, or scheduled a working session. Intentions do not count.

**3. Gap**  
If they cannot reach the economic buyer, write the introduction you still need.

**4. Support**  
Give them materials that are true. Do not ask them to hide facts from their employer.

**5. Multi-thread**  
Name one other relationship to build so the deal is not a single point of failure.

**Deliberately not done**
- Asking a champion to conceal information from their company.
- Equating responsiveness with power.
- A single-threaded deal described as covered.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Asking a champion to conceal information from their company.
- Equating responsiveness with power.
- A single-threaded deal described as covered.

## Related skills

- `qualification-meddic`
- `account-plan`
