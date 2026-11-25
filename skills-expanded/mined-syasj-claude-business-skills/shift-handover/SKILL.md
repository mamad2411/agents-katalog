---
name: shift-handover
description: "Write a shift handover that carries open issues, safety notes, and the next check. Use when the user mentions shift handover, shift report, production handover, operations handover, or asks for a shift handover. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'shift-handover' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Shift Handover

Write a shift handover that carries open issues, safety notes, and the next check.

## When to use this skill

Use this skill when the user:

- shift handover
- shift report
- production handover
- operations handover

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Open issues
- Safety or quality notes
- What the next shift must check
- Staffing gaps

## Workflow


### 1. Step 1

List open issues with status and the next action.
### 2. Step 2

Highlight safety and quality holds first.
### 3. Step 3

Say what was completed so the next shift does not redo it.
### 4. Step 4

Name the fragile item to recheck and when.
### 5. Step 5

Note staffing gaps that change what is possible.
### 6. Step 6

Keep rumors out. Unknowns are labeled unknown.

## Output

Deliver a **shift handover**.

- Purpose of this shift handover, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a shift handover by 30 September 2026. An outgoing shift leaves a quality hold unmentioned because the note says 'quiet night'.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

An outgoing shift leaves a quality hold unmentioned because the note says 'quiet night'.

Open issues: Tuesday shift is open. SOP 118 receiving was raised verbally and never logged
Safety or quality notes: one file, dated 14 September 2026. No earlier version attached for comparison
What the next shift must check: Dock exception log, last reviewed 14 September 2026. No owner named since
Staffing gaps: Tuesday shift is missing a source
```

### Example outcome

**Shift handover**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Leads with the hold, the next check, and an explicit not-quiet status.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Open issues | Tuesday shift is open. SOP 118 receiving was raised verbally and never logged | Needs confirmation |
| Safety or quality notes | one file, dated 14 September 2026. No earlier version attached for comparison | Carried into the draft |
| What the next shift must check | Dock exception log, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Staffing gaps | Tuesday shift is missing a source | Needs confirmation |

**How this draft was built**

**1. List open issues with status and the next action**

**2. Highlight safety and quality holds first**

**3. Say what was completed so the next shift does not redo it**

**4. Name the fragile item to recheck and when**

**5. Note staffing gaps that change what is possible**

**Deliberately not done**
- A handover that says nothing happened while a hold is open.
- Rumors.
- No next check.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A handover that says nothing happened while a hold is open
- Rumors
- No next check

## Related skills

- `oncall-handoff`
- `gemba-walk`
