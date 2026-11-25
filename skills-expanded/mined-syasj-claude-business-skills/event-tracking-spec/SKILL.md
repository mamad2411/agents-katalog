---
name: event-tracking-spec
description: "Specify product or marketing events so a later analyst can trust the trigger, the properties, and the privacy boundary. Use when the user mentions tracking plan, event taxonomy, instrument this flow, analytics events, or asks for a tracking spec. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'event-tracking-spec' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Event Tracking Spec

Specify product or marketing events so a later analyst can trust the trigger, the properties, and the privacy boundary.

## When to use this skill

Use this skill when the user:

- tracking plan
- event taxonomy
- instrument this flow
- analytics events

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

- The question the events answer
- The actions to instrument
- Existing naming rules
- Privacy limits

## Workflow


### 1. Step 1

Write the question first. Events without a question are rejected.
### 2. Define trigger timing precisely

on success, not on click, if success is what matters.
### 3. Step 3

List properties and ban secrets, payment card data, and raw credentials.
### 4. Step 4

Match their naming rules. Do not invent a parallel taxonomy.
### 5. Step 5

Specify how the team will verify the event before release.
### 6. Step 6

Note identity rules they already use. Do not design a covert fingerprint.

## Output

Deliver a **tracking spec**.

- Purpose of this tracking spec, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a tracking spec by 30 September 2026. A spec adds the user's national ID as a property to count button clicks.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A spec adds the user's national ID as a property to count button clicks.

The question the events answer: A spec adds the user's national ID as a property to count button clicks
The actions to instrument: orders_daily; customers. Both unassigned as of 14 September 2026
Existing naming rules: their one-page rule dated 2 Mar 2026. No exception log since
Privacy limits: email and billing address. They said no health data
```

### Example outcome

**Tracking spec**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the ID, defines the success trigger, and names the verification step.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question the events answer | A spec adds the user's national ID as a property to count button clicks | Needs confirmation |
| The actions to instrument | orders_daily; customers. Both unassigned as of 14 September 2026 | Carried into the draft |
| Existing naming rules | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Privacy limits | email and billing address. They said no health data | Needs confirmation |

**How this draft was built**

**1. Write the question first. Events without a question are rejected**

**2. Define trigger timing precisely**  
on success, not on click, if success is what matters.

**3. List properties and ban secrets, payment card data, and raw credentials**

**4. Match their naming rules. Do not invent a parallel taxonomy**

**5. Specify how the team will verify the event before release**

**Deliberately not done**
- Tracking secrets.
- A parallel naming scheme.
- Events with no verification step.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Tracking secrets
- A parallel naming scheme
- Events with no verification step

## Related skills

- `product-analytics-spec`
- `privacy-by-design`
