---
name: dispute-intake
description: "Organize the facts of a dispute for counsel, preserving what is known, unknown, and time-sensitive. Use when the user mentions dispute intake, we may be sued, contract dispute facts, demand letter arrived, or asks for a dispute intake memo. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'dispute-intake' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Dispute Intake

Organize the facts of a dispute for counsel, preserving what is known, unknown, and time-sensitive.

## When to use this skill

Use this skill when the user:

- dispute intake
- we may be sued
- contract dispute facts
- demand letter arrived

## When not to use this skill

- Destroying or hiding evidence
- Drafting a deceptive response

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

- What the other side claims
- The timeline the user knows
- Documents they have
- Any stated deadline

## Workflow


### 1. Chronology

Dates and facts only. Label disputed facts as disputed. Do not pick a winner.
### 2. Documents

List what exists and where. Do not tell anyone to destroy, hide, or alter records.
### 3. Preservation

Recommend they keep relevant records and talk to counsel about a legal hold. Do not run a hold yourself as if you were counsel.
### 4. Deadlines

Record only deadlines written in the document they received. Do not calculate a statute of limitations from memory.
### 5. Business impact

Cash, customers, and operations, so counsel sees context.
### 6. Tone

The memo is internal and calm. No threats to draft, no public posts, no admissions dressed up as apologies.

## Output

Deliver a **dispute intake memo**.

- Purpose of this dispute intake memo, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a dispute intake memo by 30 September 2026. A customer sent a demand letter with a response date, and the team is arguing about blame in chat.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A customer sent a demand letter with a response date, and the team is arguing about blame in chat.

What the other side claims: the draft sentence is broader than the note
The timeline the user knows: five working days, due 30 September 2026
Documents they have: one PDF, 2 pages, dated 14 September 2026
Any stated deadline: 30 September 2026
```

### Example outcome

**Dispute intake memo**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A chronology, a document list, a preservation reminder, and the written response date flagged for counsel.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What the other side claims | the draft sentence is broader than the note | Needs confirmation |
| The timeline the user knows | five working days, due 30 September 2026 | Carried into the draft |
| Documents they have | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Any stated deadline | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Chronology**  
Dates and facts only. Label disputed facts as disputed. Do not pick a winner.

**2. Documents**  
List what exists and where. Do not tell anyone to destroy, hide, or alter records.

**3. Preservation**  
Recommend they keep relevant records and talk to counsel about a legal hold. Do not run a hold yourself as if you were counsel.

**4. Deadlines**  
Record only deadlines written in the document they received. Do not calculate a statute of limitations from memory.

**5. Business impact**  
Cash, customers, and operations, so counsel sees context.

**Deliberately not done**
- Advising anyone to delete evidence.
- Inventing a limitation period.
- A fiery response sent without counsel.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Advising anyone to delete evidence.
- Inventing a limitation period.
- A fiery response sent without counsel.

## Related skills

- `legal-hold-notice`
- `outside-counsel-brief`
- `contract-risk-review`
