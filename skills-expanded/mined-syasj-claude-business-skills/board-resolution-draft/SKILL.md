---
name: board-resolution-draft
description: "Draft resolution language from a decision the board is actually being asked to make, for counsel or the secretary to finalize. Use when the user mentions board resolution, written consent, director resolution draft, approve a resolution, or asks for a board resolution draft. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'board-resolution-draft' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Board Resolution Draft

Draft resolution language from a decision the board is actually being asked to make, for counsel or the secretary to finalize.

## When to use this skill

Use this skill when the user:

- board resolution
- written consent
- director resolution draft
- approve a resolution

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

- The exact decision
- The approving body
- Any recusal the user mentioned
- Supporting paper already prepared

## Workflow


### 1. Use their decision

The resolution authorizes only what they described. Do not add broad powers for convenience.
### 2. Identify the body

Board, committee, or shareholder, as the user stated. If they are unsure which body must approve, flag that for counsel instead of guessing.
### 3. Recusals

If they named a conflict, the draft notes the recusal and does not count that person in favor.
### 4. Authority

Who may sign documents after approval, by name or role they gave.
### 5. Attachments

Refer to the memo or agreement by title. Do not invent a document date.
### 6. Secretary review

Mark the draft unofficial until the corporate secretary or counsel accepts it.

## Output

Deliver a **board resolution draft**.

- Purpose of this board resolution draft, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a board resolution draft by 30 September 2026. The board is asked to approve a bank account change, and one director works for the bank.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The board is asked to approve a bank account change, and one director works for the bank.

The exact decision: The board is asked to approve a bank account change, and one director works for the bank
The approving body: Harbor renewal, recorded 14 September 2026. No supporting file attached
Any recusal the user mentioned: Contractor NDA. Partly documented: the what is written down, the who is not
Supporting paper already prepared: Contractor NDA, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Board resolution draft**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A narrow draft authorizing the account change, noting the recusal, and waiting for the secretary.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The exact decision | The board is asked to approve a bank account change, and one director works for the bank | Needs confirmation |
| The approving body | Harbor renewal, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Any recusal the user mentioned | Contractor NDA. Partly documented: the what is written down, the who is not | Carried into the draft |
| Supporting paper already prepared | Contractor NDA, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Use their decision**  
The resolution authorizes only what they described. Do not add broad powers for convenience.

**2. Identify the body**  
Board, committee, or shareholder, as the user stated. If they are unsure which body must approve, flag that for counsel instead of guessing.

**3. Recusals**  
If they named a conflict, the draft notes the recusal and does not count that person in favor.

**4. Authority**  
Who may sign documents after approval, by name or role they gave.

**5. Attachments**  
Refer to the memo or agreement by title. Do not invent a document date.

**Deliberately not done**
- A resolution that grants open-ended authority.
- Guessing the approving body.
- Ignoring a stated conflict.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A resolution that grants open-ended authority.
- Guessing the approving body.
- Ignoring a stated conflict.

## Related skills

- `board-memo-writer`
- `corporate-records-hygiene`
- `board-meeting-facilitator`
