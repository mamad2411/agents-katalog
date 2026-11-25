---
name: stakeholder-update
description: "Draft a stakeholder update that tells each audience what changed for them and what you need. Use when the user mentions stakeholder update, project update email, sponsor update, client status note, or asks for a stakeholder update. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'stakeholder-update' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Stakeholder Update

Draft a stakeholder update that tells each audience what changed for them and what you need.

## When to use this skill

Use this skill when the user:

- stakeholder update
- project update email
- sponsor update
- client status note

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Delivery plans are commitments only when owners and dates are real. Do not fabricate status to make a report look healthy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What changed
- Who is affected
- What you need from them
- What must not be overclaimed

## Workflow


### 1. Step 1

Segment the update if audiences need different actions.
### 2. Step 2

Lead with the change, not the backstory.
### 3. Step 3

State what you need and by when.
### 4. Step 4

Include a delay or a cut if one exists. Do not imply you are on track.
### 5. Step 5

Keep promises limited to decisions already made.
### 6. Step 6

Offer a path for questions.

## Output

Deliver a **stakeholder update**.

- Purpose of this stakeholder update, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a stakeholder update by 30 September 2026. A client update draft says the launch is on track after scope was cut.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A client update draft says the launch is on track after scope was cut.

What changed: requested 14 September 2026. Not yet approved
Who is affected: Owen Blake, delivery lead
What you need from them: Change request 118, last reviewed 14 September 2026. No owner named since
What must not be overclaimed: the draft sentence is broader than the note
```

### Example outcome

**Stakeholder update**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
States the cut and asks the client to confirm the reduced scope.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What changed | requested 14 September 2026. Not yet approved | Needs confirmation |
| Who is affected | Owen Blake, delivery lead | Carried into the draft |
| What you need from them | Change request 118, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| What must not be overclaimed | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Segment the update if audiences need different actions**

**2. Lead with the change, not the backstory**

**3. State what you need and by when**

**4. Include a delay or a cut if one exists. Do not imply you are on track**

**5. Keep promises limited to decisions already made**

**Deliberately not done**
- A single vague update for audiences with different decisions.
- Hiding a delay.
- A promise not yet made.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A single vague update for audiences with different decisions
- Hiding a delay
- A promise not yet made

## Related skills

- `status-report`
- `internal-comms-plan`
