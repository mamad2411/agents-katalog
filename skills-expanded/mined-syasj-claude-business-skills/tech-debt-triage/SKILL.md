---
name: tech-debt-triage
description: "Triage tech debt by the risk and delay it causes, and cut the list to what the team will actually pay down. Use when the user mentions tech debt, debt triage, engineering backlog cleanup, what debt matters, or asks for a tech debt triage. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tech-debt-triage' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Tech Debt Triage

Triage tech debt by the risk and delay it causes, and cut the list to what the team will actually pay down.

## When to use this skill

Use this skill when the user:

- tech debt
- debt triage
- engineering backlog cleanup
- what debt matters

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The debt items
- The incidents or delays they cause
- Team capacity
- Upcoming product bets

## Workflow


### 1. Evidence

Each item needs a cost: incidents, slow changes, or a named risk. Vague dislike is parked.
### 2. Rank

User risk first, then change delay, then cosmetics.
### 3. Cut

Choose a few items that fit the capacity. A debt program that consumes the quarter needs an explicit product trade.
### 4. Shape

Paydown as slices inside product work where possible.
### 5. Owner

One owner per chosen item.
### 6. Review

A date to see if the cost actually dropped.

## Output

Deliver a **tech debt triage**.

- Purpose of this tech debt triage, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a tech debt triage by 30 September 2026. A team has 60 debt tickets and wants them all in next sprint alongside a launch.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team has 60 debt tickets and wants them all in next sprint alongside a launch.

The debt items: Checkout service, recorded 14 September 2026. No supporting file attached
The incidents or delays they cause: Checkout service, first seen 14 September 2026. No root cause recorded yet
Team capacity: two people on shift, one off
Upcoming product bets: Status page and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Tech debt triage**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps the debt tied to launch risk, parks the rest, and makes the capacity trade explicit.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The debt items | Checkout service, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The incidents or delays they cause | Checkout service, first seen 14 September 2026. No root cause recorded yet | Carried into the draft |
| Team capacity | two people on shift, one off | Carried into the draft |
| Upcoming product bets | Status page and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Evidence**  
Each item needs a cost: incidents, slow changes, or a named risk. Vague dislike is parked.

**2. Rank**  
User risk first, then change delay, then cosmetics.

**3. Cut**  
Choose a few items that fit the capacity. A debt program that consumes the quarter needs an explicit product trade.

**4. Shape**  
Paydown as slices inside product work where possible.

**5. Owner**  
One owner per chosen item.

**Deliberately not done**
- A debt list with no capacity cut.
- Ranking by disgust.
- A rewrite program with no product trade made explicit.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A debt list with no capacity cut.
- Ranking by disgust.
- A rewrite program with no product trade made explicit.

## Related skills

- `refactor-plan`
- `portfolio-prioritization`
