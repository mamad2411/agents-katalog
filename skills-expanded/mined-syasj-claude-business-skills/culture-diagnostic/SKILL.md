---
name: culture-diagnostic
description: "Describe how the culture actually behaves, using evidence, and name one habit worth changing. Use when the user mentions culture problem, how we work, culture diagnostic, values versus behavior, or asks for a culture diagnostic. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'culture-diagnostic' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Culture Diagnostic

Describe how the culture actually behaves, using evidence, and name one habit worth changing.

## When to use this skill

Use this skill when the user:

- culture problem
- how we work
- culture diagnostic
- values versus behavior

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Incidents or examples the user witnessed
- Stated values, if any
- What the user wants culture to help the business do
- Limits on what they are willing to change

## Workflow


### 1. Prefer stories to adjectives

Collect specific moments. 'We are innovative' is not evidence.
### 2. Compare stated and lived

Where values and promotions, meetings, or incidents disagree, write the gap carefully and without gossip.
### 3. Tie culture to work

Which business result is harder because of the current habit.
### 4. Choose one habit

Recommend one behavior to change in the next quarter, with a manager ritual that reinforces it. Do not propose a rebrand of the values poster.
### 5. Watch power

Note whether the habit is rewarded in who gets promoted or excused. Use only examples the user gave.
### 6. Avoid armchair psychology

Do not diagnose individuals. Describe systems and norms.

## Output

Deliver a **culture diagnostic**.

- Purpose of this culture diagnostic, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a culture diagnostic by 30 September 2026. A founder says the culture is 'like a family' but missed commitments have no consequence.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A founder says the culture is 'like a family' but missed commitments have no consequence.

Incidents or examples the user witnessed: Cedar Clinic, first seen 14 September 2026. No root cause recorded yet
Stated values, if any: Lantern Inn and one other, both unconfirmed as of 14 September 2026
What the user wants culture to help the business do: open item, last reviewed 14 September 2026. No owner named since
Limits on what they are willing to change: requested 14 September 2026. Not yet approved
```

### Example outcome

**Culture diagnostic**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Uses the user's incidents, names the accountability gap, and proposes one ritual rather than a new values poster.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Incidents or examples the user witnessed | Cedar Clinic, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| Stated values, if any | Lantern Inn and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| What the user wants culture to help the business do | open item, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Limits on what they are willing to change | requested 14 September 2026. Not yet approved | Needs confirmation |

**How this draft was built**

**1. Prefer stories to adjectives**  
Collect specific moments. 'We are innovative' is not evidence.

**2. Compare stated and lived**  
Where values and promotions, meetings, or incidents disagree, write the gap carefully and without gossip.

**3. Tie culture to work**  
Which business result is harder because of the current habit.

**4. Choose one habit**  
Recommend one behavior to change in the next quarter, with a manager ritual that reinforces it. Do not propose a rebrand of the values poster.

**5. Watch power**  
Note whether the habit is rewarded in who gets promoted or excused. Use only examples the user gave.

**Deliberately not done**
- A new values list with no behavior change.
- Blaming 'culture' for a single underperforming person.
- Inventing survey results.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A new values list with no behavior change.
- Blaming 'culture' for a single underperforming person.
- Inventing survey results.

## Related skills

- `engagement-survey-readout`
- `change-leadership`
- `operating-cadence`
