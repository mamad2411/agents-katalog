---
name: customer-discovery-sprint
description: "Plan a discovery sprint that books real conversations and writes down disconfirming evidence. Use when the user mentions discovery sprint, customer discovery, founder interviews, problem sprint, or asks for a discovery sprint. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'customer-discovery-sprint' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Customer Discovery Sprint

Plan a discovery sprint that books real conversations and writes down disconfirming evidence.

## When to use this skill

Use this skill when the user:

- discovery sprint
- customer discovery
- founder interviews
- problem sprint

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

- The hypothesis
- How they will reach people
- The number of conversations
- The disconfirming signal

## Workflow


### 1. Step 1

Write the hypothesis so a conversation can kill it.
### 2. Step 2

Recruit people who have the problem, not friends who will be kind, and say so.
### 3. Step 3

Use a script that asks for past behavior.
### 4. Step 4

Log disconfirming notes, not only excitement.
### 5. Step 5

Decide continue, pivot, or stop at the end.
### 6. Step 6

Do not help scrape personal data or misrepresent who they are.

## Output

Deliver a **discovery sprint**.

- Purpose of this discovery sprint, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a discovery sprint by 30 September 2026. A sprint plan interviews the founder's family and calls it validation.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A sprint plan interviews the founder's family and calls it validation.

The hypothesis: A sprint plan interviews the founder's family and calls it validation. Stated once, in the ask. Not written down anywhere else
How they will reach people: Runway to March, last reviewed 14 September 2026. No owner named since
The number of conversations: First four paying accounts, recorded 14 September 2026. No supporting file attached
The disconfirming signal: First four paying accounts, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Discovery sprint**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Recruits people with the problem and requires a disconfirming log.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The hypothesis | A sprint plan interviews the founder's family and calls it validation. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| How they will reach people | Runway to March, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The number of conversations | First four paying accounts, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The disconfirming signal | First four paying accounts, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Write the hypothesis so a conversation can kill it**

**2. Recruit people who have the problem, not friends who will be kind, and say so**

**3. Use a script that asks for past behavior**

**4. Log disconfirming notes, not only excitement**

**5. Decide continue, pivot, or stop at the end**

**Deliberately not done**
- Only talking to friends.
- Hiding disconfirming notes.
- Misrepresenting identity.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Only talking to friends
- Hiding disconfirming notes
- Misrepresenting identity

## Related skills

- `discovery-interview`
- `offer-hypothesis`
