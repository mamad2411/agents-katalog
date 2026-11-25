---
name: workshop-decision-record
description: "Turn a client workshop into a decision record rather than a photo of sticky notes. Use when the user mentions workshop readout, decision record workshop, sticky note synthesis, working session notes, or asks for a workshop decision record. Consulting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: consulting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'workshop-decision-record' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Workshop Decision Record

Turn a client workshop into a decision record rather than a photo of sticky notes.

## When to use this skill

Use this skill when the user:

- workshop readout
- decision record workshop
- sticky note synthesis
- working session notes

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Client work stays confidential to the engagement. Do not fabricate findings to please a sponsor. Separate evidence from recommendation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision sought
- Options generated
- The choice if one was made
- Dissent

## Workflow


### 1. Step 1

State whether a decision was made. If not, say so.
### 2. Step 2

Record options in the client's words.
### 3. Step 3

Note dissent. Do not convert silence into agreement.
### 4. Step 4

Assign owners only for actions the room accepted.
### 5. Step 5

Park ideas that lost.
### 6. Step 6

Do not add recommendations the room did not hear and call them workshop output.

## Output

Deliver a **workshop decision record**.

- Purpose of this workshop decision record, in two sentences.
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

Elena Voss, engagement manager at Clearlane Advisors in Calgary, needs a workshop decision record by 30 September 2026. Notes say the client chose a market, but the room only brainstormed.

### Example data

```text
From: Elena Voss, engagement manager
Organization: Clearlane Advisors, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Notes say the client chose a market, but the room only brainstormed.

The decision sought: Notes say the client chose a market, but the room only brainstormed
Options generated: keep Scope item 4, or stop. No third option written
The choice if one was made: Scope item 4, recorded 14 September 2026. No supporting file attached
Dissent: Interview set A. Partly documented: the what is written down, the who is not
```

### Example outcome

**Workshop decision record**
To: Elena Voss, engagement manager, Clearlane Advisors
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Labels the market as an idea, not a decision, and lists the open choice.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision sought | Notes say the client chose a market, but the room only brainstormed | Needs confirmation |
| Options generated | keep Scope item 4, or stop. No third option written | Carried into the draft |
| The choice if one was made | Scope item 4, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Dissent | Interview set A. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. State whether a decision was made. If not, say so**

**2. Record options in the client's words**

**3. Note dissent. Do not convert silence into agreement**

**4. Assign owners only for actions the room accepted**

**5. Park ideas that lost**

**Deliberately not done**
- Fake consensus.
- Owners the room did not accept.
- A novel of sticky notes.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Fake consensus
- Owners the room did not accept
- A novel of sticky notes

## Related skills

- `decision-log`
- `workshop-facilitation`
