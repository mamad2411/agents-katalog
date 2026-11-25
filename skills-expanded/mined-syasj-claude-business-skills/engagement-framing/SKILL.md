---
name: engagement-framing
description: "Frame a consulting engagement with the decision, the evidence, and what is out of scope. Use when the user mentions engagement brief, consulting scope, statement of work narrative, frame the work, or asks for a engagement brief. Consulting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: consulting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'engagement-framing' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Engagement Framing

Frame a consulting engagement with the decision, the evidence, and what is out of scope.

## When to use this skill

Use this skill when the user:

- engagement brief
- consulting scope
- statement of work narrative
- frame the work

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

- The client decision
- Evidence you can access
- Time
- Out-of-scope items

## Workflow


### 1. Step 1

Write the decision the client must make.
### 2. Step 2

List evidence already available and evidence you will not pretend to have.
### 3. Step 3

Cut scope that does not serve the decision.
### 4. Step 4

Name the client owner.
### 5. Step 5

State what would make the engagement stop early.
### 6. Step 6

Do not promise a finding before the evidence is reviewed.

## Output

Deliver a **engagement brief**.

- Purpose of this engagement brief, in two sentences.
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

Elena Voss, engagement manager at Clearlane Advisors in Calgary, needs an engagement brief by 30 September 2026. A proposal promises a 20 percent savings number before any baseline exists.

### Example data

```text
From: Elena Voss, engagement manager
Organization: Clearlane Advisors, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A proposal promises a 20 percent savings number before any baseline exists.

The client decision: A proposal promises a 20 percent savings number before any baseline exists
Evidence you can access: one PDF, 2 pages, dated 14 September 2026
Time: five working days, due 30 September 2026
Out-of-scope items: this decision only
```

### Example outcome

**Engagement brief**
To: Elena Voss, engagement manager, Clearlane Advisors
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Replaces the number with a baseline task and a decision.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The client decision | A proposal promises a 20 percent savings number before any baseline exists | Needs confirmation |
| Evidence you can access | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Time | five working days, due 30 September 2026 | Carried into the draft |
| Out-of-scope items | this decision only | Needs confirmation |

**How this draft was built**

**1. Write the decision the client must make**

**2. List evidence already available and evidence you will not pretend to have**

**3. Cut scope that does not serve the decision**

**4. Name the client owner**

**5. State what would make the engagement stop early**

**Deliberately not done**
- A promised conclusion.
- Scope with no decision.
- Hidden out-of-scope work.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A promised conclusion
- Scope with no decision
- Hidden out-of-scope work

## Related skills

- `proposal-writer`
- `outside-counsel-brief`
