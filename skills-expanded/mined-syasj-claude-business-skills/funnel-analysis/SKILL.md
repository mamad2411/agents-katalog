---
name: funnel-analysis
description: "Analyze a funnel with explicit step definitions and a focus on the biggest leak that the team can affect. Use when the user mentions funnel analysis, conversion funnel, drop-off, where do users drop, or asks for a funnel analysis. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'funnel-analysis' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Funnel Analysis

Analyze a funnel with explicit step definitions and a focus on the biggest leak that the team can affect.

## When to use this skill

Use this skill when the user:

- funnel analysis
- conversion funnel
- drop-off
- where do users drop

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

- The steps and their definitions
- Counts they provided
- How users are identified
- Known tracking gaps

## Workflow


### 1. Step 1

Write the step definitions. If two steps can fire out of order, say the funnel is messy.
### 2. Step 2

Compute conversion only from counts they gave. Show the arithmetic.
### 3. Step 3

Find the largest loss of people, not the largest percentage on a tiny step, and say which one you are using.
### 4. Step 4

Note tracking gaps before blaming the product.
### 5. Step 5

Separate a new-user funnel from a returning-user funnel if they differ in the data.
### 6. Step 6

Recommend one investigation or one product change to test, not five.

## Output

Deliver a **funnel analysis**.

- Purpose of this funnel analysis, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a funnel analysis by 30 September 2026. A funnel shows a huge drop between two events that can fire in either order.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A funnel shows a huge drop between two events that can fire in either order.

The steps and their definitions: orders_daily; customers. Both unassigned as of 14 September 2026
Counts they provided: 45 in the last period. No prior period attached, so no trend
How users are identified: customers, last reviewed 14 September 2026. No owner named since
Known tracking gaps: orders_daily is missing a source
```

### Example outcome

**Funnel analysis**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Calls the funnel unordered, pauses the product blame, and asks for a sequenced definition.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The steps and their definitions | orders_daily; customers. Both unassigned as of 14 September 2026 | Needs confirmation |
| Counts they provided | 45 in the last period. No prior period attached, so no trend | Carried into the draft |
| How users are identified | customers, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Known tracking gaps | orders_daily is missing a source | Needs confirmation |

**How this draft was built**

**1. Write the step definitions. If two steps can fire out of order, say the funnel is messy**

**2. Compute conversion only from counts they gave. Show the arithmetic**

**3. Find the largest loss of people, not the largest percentage on a tiny step, and say which one you are using**

**4. Note tracking gaps before blaming the product**

**5. Separate a new-user funnel from a returning-user funnel if they differ in the data**

**Deliberately not done**
- Blaming the product when tracking is broken.
- A funnel with undefined steps.
- Invented counts.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Blaming the product when tracking is broken
- A funnel with undefined steps
- Invented counts

## Related skills

- `cohort-analysis`
- `event-tracking-spec`
