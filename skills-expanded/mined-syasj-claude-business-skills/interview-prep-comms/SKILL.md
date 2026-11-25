---
name: interview-prep-comms
description: "Prepare a spokesperson with the known facts, the bridge to the point, and the questions they must not bluff. Use when the user mentions spokesperson prep, media training notes, interview prep, press Q&A, or asks for a spokesperson prep. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'interview-prep-comms' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Spokesperson Prep

Prepare a spokesperson with the known facts, the bridge to the point, and the questions they must not bluff.

## When to use this skill

Use this skill when the user:

- spokesperson prep
- media training notes
- interview prep
- press Q&A

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate quotes, sources, or images. Label opinion. Do not draft impersonation or defamation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The point
- Known facts
- Likely questions
- Off-limit topics

## Workflow


### 1. Step 1

Write the point and three supporting facts they can say.
### 2. Step 2

List likely questions, including the hostile fair one.
### 3. Step 3

For unknowns, the answer is that they do not know yet.
### 4. Step 4

Do not script a lie or a no-comment that hides a safety issue already confirmed.
### 5. Step 5

Bridge back to the point without dodging a factual question they can answer.
### 6. Step 6

Remind them not to invent a number on camera.

## Output

Deliver a **spokesperson prep**.

- Purpose of this spokesperson prep, in two sentences.
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

Jonah Ellis, assignment editor at Foothills Desk in Calgary, needs a spokesperson prep by 30 September 2026. Prep says to deny an outage that engineering has confirmed.

### Example data

```text
From: Jonah Ellis, assignment editor
Organization: Foothills Desk, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Prep says to deny an outage that engineering has confirmed.

The point: Prep says to deny an outage that engineering has confirmed. Stated once, in the ask. Not written down anywhere else
Known facts: Fare change. Stated in the ask, not documented anywhere else
Likely questions: Prep says to deny an outage that engineering has confirmed
Off-limit topics: Fare change. Partly documented: the what is written down, the who is not
```

### Example outcome

**Spokesperson prep**
To: Jonah Ellis, assignment editor, Foothills Desk
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Prep that tells the truth about the outage and refuses the denial script.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The point | Prep says to deny an outage that engineering has confirmed. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Known facts | Fare change. Stated in the ask, not documented anywhere else | Carried into the draft |
| Likely questions | Prep says to deny an outage that engineering has confirmed | Carried into the draft |
| Off-limit topics | Fare change. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Write the point and three supporting facts they can say**

**2. List likely questions, including the hostile fair one**

**3. For unknowns, the answer is that they do not know yet**

**4. Do not script a lie or a no-comment that hides a safety issue already confirmed**

**5. Bridge back to the point without dodging a factual question they can answer**

**Deliberately not done**
- A scripted lie.
- An invented live number.
- Dodging a confirmed safety fact.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Ellis by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A scripted lie
- An invented live number
- Dodging a confirmed safety fact

## Related skills

- `customer-communication-incident`
- `pr-pitch`
