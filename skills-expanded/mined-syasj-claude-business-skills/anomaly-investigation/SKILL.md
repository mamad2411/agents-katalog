---
name: anomaly-investigation
description: "Investigate a metric anomaly by separating a data break from a real change before anyone acts. Use when the user mentions anomaly, metric spiked, number looks wrong, investigate a drop, or asks for a anomaly note. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'anomaly-investigation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Anomaly Investigation

Investigate a metric anomaly by separating a data break from a real change before anyone acts.

## When to use this skill

Use this skill when the user:

- anomaly
- metric spiked
- number looks wrong
- investigate a drop

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

- The metric and the unexpected movement
- Recent pipeline or tracking changes
- Business events they know about
- The decision waiting on the number

## Workflow


### 1. Step 1

Confirm the movement against the definition and the source.
### 2. Step 2

Check freshness, duplicates, and tracking changes before a business story.
### 3. Step 3

If a business event is known, test whether its timing matches. Do not invent a campaign or outage.
### 4. Step 4

Quantify who is affected using their slices, and stop if the slice is tiny.
### 5. Step 5

Say whether the number is safe to use today.
### 6. Step 6

Recommend a data fix or a business investigation, not both as if they were the same work.

## Output

Deliver a **anomaly note**.

- Purpose of this anomaly note, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs an anomaly note by 30 September 2026. Conversion halves on the day a tracking change shipped, and marketing wants a new campaign.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Conversion halves on the day a tracking change shipped, and marketing wants a new campaign.

The metric and the unexpected movement: plan 180, actual 90
Recent pipeline or tracking changes: requested 14 September 2026. Not yet approved
Business events they know about: customers. Partly documented: the what is written down, the who is not
The decision waiting on the number: Conversion halves on the day a tracking change shipped, and marketing wants a new campaign
```

### Example outcome

**Anomaly note**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Pauses the campaign idea until tracking is ruled in or out.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The metric and the unexpected movement | plan 180, actual 90 | Needs confirmation |
| Recent pipeline or tracking changes | requested 14 September 2026. Not yet approved | Carried into the draft |
| Business events they know about | customers. Partly documented: the what is written down, the who is not | Carried into the draft |
| The decision waiting on the number | Conversion halves on the day a tracking change shipped, and marketing wants a new campaign | Needs confirmation |

**How this draft was built**

**1. Confirm the movement against the definition and the source**

**2. Check freshness, duplicates, and tracking changes before a business story**

**3. If a business event is known, test whether its timing matches. Do not invent a campaign or outage**

**4. Quantify who is affected using their slices, and stop if the slice is tiny**

**5. Say whether the number is safe to use today**

**Deliberately not done**
- A business story for a broken pipeline.
- Ignoring a tracking change.
- Acting on a tiny slice.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A business story for a broken pipeline
- Ignoring a tracking change
- Acting on a tiny slice

## Related skills

- `data-quality-check`
- `funnel-analysis`
