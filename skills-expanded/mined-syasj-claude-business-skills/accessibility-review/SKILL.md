---
name: accessibility-review
description: "Review a product flow for accessibility barriers and turn them into concrete fixes, not a vague pledge. Use when the user mentions accessibility review, a11y review, screen reader flow, inclusive product review, or asks for a accessibility review. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'accessibility-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Accessibility Product Review

Review a product flow for accessibility barriers and turn them into concrete fixes, not a vague pledge.

## When to use this skill

Use this skill when the user:

- accessibility review
- a11y review
- screen reader flow
- inclusive product review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The flow
- Known barriers
- The standard the team says it targets
- User impact already reported

## Workflow


### 1. Scope the flow

One important path, not the whole product in one sitting.
### 2. Barriers

Keyboard, labels, contrast, errors, and media alternatives, based on the material provided. Do not claim a conformance audit you did not perform.
### 3. Impact

Who is blocked from the job, in practical terms.
### 4. Fixes

Specific design or engineering changes, ordered by who is completely blocked.
### 5. Tests

How the team can recheck the flow. Automated scans are a start, not a certificate.
### 6. No certificate

Do not claim WCAG conformance unless a qualified review the user supplied says so.

## Output

Deliver a **accessibility review**.

- Purpose of this accessibility review, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs an accessibility review by 30 September 2026. A checkout cannot be completed by keyboard, and the team wants a statement saying the product is accessible.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A checkout cannot be completed by keyboard, and the team wants a statement saying the product is accessible.

The flow: the one named in the ask. Version and owner not recorded
Known barriers: Activation checklist is open. Trial day-3 email was raised verbally and never logged
The standard the team says it targets: 140
User impact already reported: one file, dated 14 September 2026. No earlier version attached for comparison
```

### Example outcome

**Accessibility review**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the statement, names the keyboard barrier, and lists the fix and retest.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The flow | the one named in the ask. Version and owner not recorded | Needs confirmation |
| Known barriers | Activation checklist is open. Trial day-3 email was raised verbally and never logged | Carried into the draft |
| The standard the team says it targets | 140 | Carried into the draft |
| User impact already reported | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |

**How this draft was built**

**1. Scope the flow**  
One important path, not the whole product in one sitting.

**2. Barriers**  
Keyboard, labels, contrast, errors, and media alternatives, based on the material provided. Do not claim a conformance audit you did not perform.

**3. Impact**  
Who is blocked from the job, in practical terms.

**4. Fixes**  
Specific design or engineering changes, ordered by who is completely blocked.

**5. Tests**  
How the team can recheck the flow. Automated scans are a start, not a certificate.

**Deliberately not done**
- Claiming compliance from a glance.
- A pledge with no fixes.
- Ignoring a reported blocker because the visual design looks fine.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Claiming compliance from a glance.
- A pledge with no fixes.
- Ignoring a reported blocker because the visual design looks fine.

## Related skills

- `accessibility-engineering`
- `accessibility-design`
