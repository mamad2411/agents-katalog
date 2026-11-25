---
name: outside-counsel-brief
description: "Brief outside counsel with the question, the facts, and the business constraint, so the meter starts on the right problem. Use when the user mentions brief outside counsel, lawyer brief, counsel instructions, legal question memo, or asks for a outside counsel brief. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'outside-counsel-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Outside Counsel Brief

Brief outside counsel with the question, the facts, and the business constraint, so the meter starts on the right problem.

## When to use this skill

Use this skill when the user:

- brief outside counsel
- lawyer brief
- counsel instructions
- legal question memo

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not legal advice and does not create an attorney-client relationship. Do not invent statutes, case names, or filing deadlines. Drafts are for qualified counsel in the relevant jurisdiction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision needed
- The deadline
- Facts and documents
- The business constraint

## Workflow


### 1. Ask one question

A brief that asks counsel to 'look at this' will return a seminar. Write the decision the company must make.
### 2. Facts in order

Chronology, documents attached or listed, and unknowns. Do not hide a bad fact to get a comforting answer.
### 3. Business constraint

Budget, launch date, or relationship risk, labeled as context, not as an instruction to reach a preferred legal answer.
### 4. Prior advice

Note advice already received so counsel does not restart blindly.
### 5. Privilege care

Mark the draft as a request for legal advice if the user says that is the intent. Do not claim privilege as a magic label on ordinary business notes.
### 6. Desired deliverable

A short advice note, a markup, or a call. Say which.

## Output

Deliver a **outside counsel brief**.

- Purpose of this outside counsel brief, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs an outside counsel brief by 30 September 2026. The CEO wants counsel to review a partnership in three days and has sent a 40-page data room link with no question.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The CEO wants counsel to review a partnership in three days and has sent a 40-page data room link with no question.

The decision needed: The CEO wants counsel to review a partnership in three days and has sent a 40-page data room link with no question
The deadline: 30 September 2026
Facts and documents: one PDF, 2 pages, dated 14 September 2026
The business constraint: no extra headcount, and no result that is not in this file
```

### Example outcome

**Outside counsel brief**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A one-question brief, a chronology, the three-day deadline, and a requested short advice note.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision needed | The CEO wants counsel to review a partnership in three days and has sent a 40-page data room link with no question | Needs confirmation |
| The deadline | 30 September 2026 | Carried into the draft |
| Facts and documents | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The business constraint | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Ask one question**  
A brief that asks counsel to 'look at this' will return a seminar. Write the decision the company must make.

**2. Facts in order**  
Chronology, documents attached or listed, and unknowns. Do not hide a bad fact to get a comforting answer.

**3. Business constraint**  
Budget, launch date, or relationship risk, labeled as context, not as an instruction to reach a preferred legal answer.

**4. Prior advice**  
Note advice already received so counsel does not restart blindly.

**5. Privilege care**  
Mark the draft as a request for legal advice if the user says that is the intent. Do not claim privilege as a magic label on ordinary business notes.

**Deliberately not done**
- Hiding an inconvenient fact.
- Asking for a predetermined answer.
- A brain dump with no question.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Hiding an inconvenient fact.
- Asking for a predetermined answer.
- A brain dump with no question.

## Related skills

- `contract-risk-review`
- `dispute-intake`
- `board-memo-writer`
