---
name: launch-readiness
description: "Run a launch-readiness review that checks support, measurement, rollback, and the promise. Use when the user mentions launch readiness, go-live checklist, release readiness, ship review, or asks for a launch readiness review. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'launch-readiness' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Launch Readiness

Run a launch-readiness review that checks support, measurement, rollback, and the promise.

## When to use this skill

Use this skill when the user:

- launch readiness
- go-live checklist
- release readiness
- ship review

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

- What will be announced
- Support and docs status
- Measurement
- Rollback path

## Workflow


### 1. Promise check

The announcement matches what the build does. Cut the rest.
### 2. Support

Agents have an FAQ and a known issue list. No launch to a blind support team.
### 3. Measurement

The event that tells you the launch worked is instrumented, or the gap is explicit.
### 4. Rollback

Who can stop the launch, and how customers are told if you do.
### 5. Legal and claims

Unapproved claims block the public line, not the internal note.
### 6. Decision

Go, go with limits, or hold. One decision, with the owner.

## Output

Deliver a **launch readiness review**.

- Purpose of this launch readiness review, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a launch readiness review by 30 September 2026. Product wants to announce automation that still requires a manual file from support.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Product wants to announce automation that still requires a manual file from support.

What will be announced: Usage limit warning, last reviewed 14 September 2026. No owner named since
Support and docs status: Trial day-3 email, last reviewed 14 September 2026. No owner named since
Measurement: not defined beyond plan 120 and actual 85
Rollback path: Trial day-3 email, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Launch readiness review**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Tells the truth about the manual step.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What will be announced | Usage limit warning, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Support and docs status | Trial day-3 email, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Measurement | not defined beyond plan 120 and actual 85 | Carried into the draft |
| Rollback path | Trial day-3 email, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Promise check**  
The announcement matches what the build does. Cut the rest.

**2. Support**  
Agents have an FAQ and a known issue list. No launch to a blind support team.

**3. Measurement**  
The event that tells you the launch worked is instrumented, or the gap is explicit.

**4. Rollback**  
Who can stop the launch, and how customers are told if you do.

**5. Legal and claims**  
Unapproved claims block the public line, not the internal note.

**Deliberately not done**
- A launch checklist that ignores support.
- Announcing unshipped scope.
- No one empowered to hold.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A launch checklist that ignores support.
- Announcing unshipped scope.
- No one empowered to hold.

## Related skills

- `launch-plan`
- `release-checklist`
