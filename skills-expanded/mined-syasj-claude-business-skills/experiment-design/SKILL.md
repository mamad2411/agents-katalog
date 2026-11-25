---
name: experiment-design
description: "Design a product experiment with a hypothesis, a guardrail, and a decision rule written in advance. Use when the user mentions experiment design, product experiment, A/B test design, hypothesis test, or asks for a experiment design. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'experiment-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Experiment Design

Design a product experiment with a hypothesis, a guardrail, and a decision rule written in advance.

## When to use this skill

Use this skill when the user:

- experiment design
- product experiment
- A/B test design
- hypothesis test

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

- The hypothesis
- The change
- The primary metric and guardrail
- The available sample

## Workflow


### 1. Hypothesis

The user behavior you expect to change, and why.
### 2. Change

One treatment. Name the control.
### 3. Metrics

A primary metric and a guardrail that would make a 'win' unacceptable, such as errors or complaints.
### 4. Decision rule

Ship, iterate, or stop, written before results.
### 5. Sample

If the sample is too small, call the work a probe, not a conclusive test.
### 6. Ethics

No experiment that tricks users about price, privacy, or safety.

## Output

Deliver a **experiment design**.

- Purpose of this experiment design, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs an experiment design by 30 September 2026. A team wants to ship the winner of a three-day test on a rare flow.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to ship the winner of a three-day test on a rare flow.

The hypothesis: A team wants to ship the winner of a three-day test on a rare flow. Stated once, in the ask. Not written down anywhere else
The change: requested 14 September 2026. Not yet approved
The primary metric and guardrail: plan 180, actual 90
The available sample: Activation checklist, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Experiment design**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Labels the work a probe, adds a guardrail, and refuses a conclusive ship decision.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The hypothesis | A team wants to ship the winner of a three-day test on a rare flow. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The change | requested 14 September 2026. Not yet approved | Carried into the draft |
| The primary metric and guardrail | plan 180, actual 90 | Carried into the draft |
| The available sample | Activation checklist, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Hypothesis**  
The user behavior you expect to change, and why.

**2. Change**  
One treatment. Name the control.

**3. Metrics**  
A primary metric and a guardrail that would make a 'win' unacceptable, such as errors or complaints.

**4. Decision rule**  
Ship, iterate, or stop, written before results.

**5. Sample**  
If the sample is too small, call the work a probe, not a conclusive test.

**Deliberately not done**
- Peeking and moving the metric.
- No guardrail.
- Calling a tiny sample conclusive.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Peeking and moving the metric.
- No guardrail.
- Calling a tiny sample conclusive.

## Related skills

- `marketing-experiment`
- `experiment-readout`
