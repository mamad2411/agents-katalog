---
name: experiment-readout
description: "Read out an experiment using the pre-written decision rule, the guardrail, and the sample they actually have. Use when the user mentions experiment readout, A/B test results, test results, did the experiment win, or asks for a experiment readout. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'experiment-readout' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Experiment Readout

Read out an experiment using the pre-written decision rule, the guardrail, and the sample they actually have.

## When to use this skill

Use this skill when the user:

- experiment readout
- A/B test results
- test results
- did the experiment win

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent numbers. If a source file is missing, say so. Distinguish observation from inference. Do not re-identify private data to make a point.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The pre-registered metric and rule if they have one
- The results they pasted
- Sample size
- Guardrail results

## Workflow


### 1. Step 1

Start from the decision rule they wrote. If none exists, say the readout is exploratory.
### 2. Step 2

Report the primary metric and the guardrail before secondary slices.
### 3. Step 3

Do not crown a winner on a slice that was not the plan, unless you label it a hypothesis.
### 4. Step 4

State whether the sample can support the decision they want.
### 5. Step 5

Separate a failed experiment from a broken implementation.
### 6. Step 6

Recommend ship, iterate, or stop, and say what would be fishing if you kept slicing.

## Output

Deliver a **experiment readout**.

- Purpose of this experiment readout, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs an experiment readout by 30 September 2026. The primary metric is flat, a secondary slice looks good, and the team wants to ship.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The primary metric is flat, a secondary slice looks good, and the team wants to ship.

The pre-registered metric and rule if they have one: plan 180, actual 90
The results they pasted: orders_daily, recorded 14 September 2026. No supporting file attached
Sample size: active_accounts, recorded 14 September 2026. No supporting file attached
Guardrail results: orders_daily, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Experiment readout**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the secondary-slice ship, notes the flat primary metric, and labels any follow-up as a new hypothesis.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The pre-registered metric and rule if they have one | plan 180, actual 90 | Needs confirmation |
| The results they pasted | orders_daily, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Sample size | active_accounts, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Guardrail results | orders_daily, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Start from the decision rule they wrote. If none exists, say the readout is exploratory**

**2. Report the primary metric and the guardrail before secondary slices**

**3. Do not crown a winner on a slice that was not the plan, unless you label it a hypothesis**

**4. State whether the sample can support the decision they want**

**5. Separate a failed experiment from a broken implementation**

**Deliberately not done**
- Moving the metric after seeing results.
- Ignoring a broken guardrail.
- Declaring a tiny sample conclusive.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Moving the metric after seeing results
- Ignoring a broken guardrail
- Declaring a tiny sample conclusive

## Related skills

- `experiment-design`
- `analysis-plan`
