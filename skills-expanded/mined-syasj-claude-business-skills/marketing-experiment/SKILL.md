---
name: marketing-experiment
description: "Design a marketing experiment with a hypothesis, a single change, and a decision rule. Use when the user mentions marketing experiment, A/B test, growth test, what should we test, or asks for a experiment brief. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'marketing-experiment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Marketing Experiment

Design a marketing experiment with a hypothesis, a single change, and a decision rule.

## When to use this skill

Use this skill when the user:

- marketing experiment
- A/B test
- growth test
- what should we test

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent testimonials, reviews, metrics, or claims the user cannot support. Do not draft spam, cloaking, fake scarcity, or impersonation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The hypothesis
- The single change
- The event that measures it
- The sample or spend available

## Workflow


### 1. Hypothesis

If we change X for audience Y, event Z will move, because of a reason you can state.
### 2. One change

Extra changes void the learning. Park them.
### 3. Decision rule

What result would scale, iterate, or stop the idea. Write it before the test.
### 4. Sample honesty

If the available traffic cannot support the decision, say the test will be directional only.
### 5. Ethics

No experiment that hides price, consent, or material terms.
### 6. Readout

A date and an owner. An unread test is a hobby.

## Output

Deliver a **experiment brief**.

- Purpose of this experiment brief, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs an experiment brief by 30 September 2026. A team wants to test a new headline, a new price, and a new form in one week and then 'see what happens'.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to test a new headline, a new price, and a new form in one week and then 'see what happens'.

The hypothesis: A team wants to test a new headline, a new price, and a new form in one week and then 'see what happens'. Stated once, in the ask. Not written down anywhere else
The single change: requested 14 September 2026. Not yet approved
The event that measures it: Fall service page, recorded 14 September 2026. No supporting file attached
The sample or spend available: Fall service page, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Experiment brief**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
The sample may only be directional.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The hypothesis | A team wants to test a new headline, a new price, and a new form in one week and then 'see what happens'. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The single change | requested 14 September 2026. Not yet approved | Carried into the draft |
| The event that measures it | Fall service page, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The sample or spend available | Fall service page, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Hypothesis**  
If we change X for audience Y, event Z will move, because of a reason you can state.

**2. One change**  
Extra changes void the learning. Park them.

**3. Decision rule**  
What result would scale, iterate, or stop the idea. Write it before the test.

**4. Sample honesty**  
If the available traffic cannot support the decision, say the test will be directional only.

**5. Ethics**  
No experiment that hides price, consent, or material terms.

**Deliberately not done**
- Testing five changes at once.
- A decision rule written after seeing the data.
- Dark-pattern experiments.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Testing five changes at once.
- A decision rule written after seeing the data.
- Dark-pattern experiments.

## Related skills

- `experiment-design`
- `landing-page-cro`
