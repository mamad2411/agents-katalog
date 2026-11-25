---
name: complaint-root-cause
description: "Analyze a cluster of complaints to the cause the company can fix, without dismissing the customer. Use when the user mentions complaint analysis, root cause of complaints, repeated complaints, why are tickets rising, or asks for a complaint analysis. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'complaint-root-cause' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Complaint Root Cause

Analyze a cluster of complaints to the cause the company can fix, without dismissing the customer.

## When to use this skill

Use this skill when the user:

- complaint analysis
- root cause of complaints
- repeated complaints
- why are tickets rising

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not blame the customer. Do not invent policy exceptions. Do not ask a customer for passwords or full payment card numbers.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The complaint cluster
- Volumes
- What agents already do
- Recent changes

## Workflow


### 1. Step 1

Define the cluster with their labels and volumes.
### 2. Step 2

Read for the failed job, not for the customer's tone.
### 3. Step 3

Separate a product defect, a policy surprise, and an expectation set by marketing.
### 4. Step 4

Check a recent change that matches the timing.
### 5. Recommend one fix

policy, product, or message.
### 6. Step 6

Do not blame the customer in the write-up.

## Output

Deliver a **complaint analysis**.

- Purpose of this complaint analysis, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a complaint analysis by 30 September 2026. Complaints rose after a pricing page started hiding a fee.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Complaints rose after a pricing page started hiding a fee.

The complaint cluster: Ticket 4412, first seen 14 September 2026. No root cause recorded yet
Volumes: 40 in the last period. No prior period attached, so no trend
What agents already do: Ticket 4420, last reviewed 14 September 2026. No owner named since
Recent changes: requested 14 September 2026. Not yet approved
```

### Example outcome

**Complaint analysis**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the hidden fee as the hypothesis to fix and does not blame the customers for writing in.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The complaint cluster | Ticket 4412, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| Volumes | 40 in the last period. No prior period attached, so no trend | Carried into the draft |
| What agents already do | Ticket 4420, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Recent changes | requested 14 September 2026. Not yet approved | Needs confirmation |

**How this draft was built**

**1. Define the cluster with their labels and volumes**

**2. Read for the failed job, not for the customer's tone**

**3. Separate a product defect, a policy surprise, and an expectation set by marketing**

**4. Check a recent change that matches the timing**

**5. Recommend one fix**  
policy, product, or message.

**Deliberately not done**
- Blaming tone.
- A fix that does not match the cause.
- Ignoring a recent change.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Blaming tone
- A fix that does not match the cause
- Ignoring a recent change

## Related skills

- `voice-of-customer`
- `marketing-claims-review`
