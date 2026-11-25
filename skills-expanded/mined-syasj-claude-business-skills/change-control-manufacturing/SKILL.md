---
name: change-control-manufacturing
description: "Review a manufacturing change for approval, risk, and the point it becomes effective. Use when the user mentions manufacturing change control, process change, engineering change, ECO review, or asks for a change-control note. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'change-control-manufacturing' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Manufacturing Change Control

Review a manufacturing change for approval, risk, and the point it becomes effective.

## When to use this skill

Use this skill when the user:

- manufacturing change control
- process change
- engineering change
- ECO review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Quality and safety procedures are drafts for the site's quality system. Do not bypass a hold, calibration, or safety step.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The change
- The risk they see
- Approvers
- The effective lot or date

## Workflow


### 1. Step 1

Describe the change and the reason.
### 2. Step 2

Identify what must be revalidated or reinspected, using their rules. Do not invent a regulatory filing.
### 3. Step 3

Name approvers. A change without the required approver is not effective.
### 4. Step 4

Set the effective lot or date so old and new do not mix unlabeled.
### 5. Step 5

Update the work instruction as part of done.
### 6. Step 6

Flag customer or regulatory notice as a question if they said it might apply.

## Output

Deliver a **change-control note**.

- Purpose of this change-control note, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs a change-control note by 30 September 2026. A process tweak is already running and the change form is blank.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

A process tweak is already running and the change form is blank.

The change: requested 14 September 2026. Not yet approved
The risk they see: Line 2 is open. No score in the file
Approvers: Gus Moretti. They have not signed
The effective lot or date: 30 September 2026
```

### Example outcome

**Change-control note**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Stops the unofficial tweak until approval and an effective point exist.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The change | requested 14 September 2026. Not yet approved | Needs confirmation |
| The risk they see | Line 2 is open. No score in the file | Carried into the draft |
| Approvers | Gus Moretti. They have not signed | Carried into the draft |
| The effective lot or date | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Describe the change and the reason**

**2. Identify what must be revalidated or reinspected, using their rules. Do not invent a regulatory filing**

**3. Name approvers. A change without the required approver is not effective**

**4. Set the effective lot or date so old and new do not mix unlabeled**

**5. Update the work instruction as part of done**

**Deliberately not done**
- An effective change with no approver.
- Mixed lots with no label.
- An invented filing.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An effective change with no approver
- Mixed lots with no label
- An invented filing

## Related skills

- `work-instruction`
- `traceability-lot`
