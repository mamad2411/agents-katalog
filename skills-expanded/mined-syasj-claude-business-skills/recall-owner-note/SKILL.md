---
name: recall-owner-note
description: "Draft the customer note for a recall using the notice the dealer has, not a homemade defect claim. Use when the user mentions recall letter, recall customer note, campaign notice, owner notification, or asks for a owner note. Automotive skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: automotive
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'recall-owner-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Recall Owner Note

Draft the customer note for a recall using the notice the dealer has, not a homemade defect claim.

## When to use this skill

Use this skill when the user:

- recall letter
- recall customer note
- campaign notice
- owner notification

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not a repair procedure for safety-critical systems and not a recall determination. Do not invent defect rates or tell anyone to disable a safety feature.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The notice
- The VINs they have
- The remedy the notice states
- What they must not add

## Workflow


### 1. Step 1

Use the notice wording for the defect and the remedy.
### 2. Step 2

List only VINs they matched.
### 3. Step 3

Do not add a failure rate.
### 4. Step 4

Do not tell the owner to keep driving if the notice says park.
### 5. Step 5

Say how to book.
### 6. Step 6

This note does not decide that a recall exists.

## Output

Deliver a **owner note**.

- Purpose of this owner note, in two sentences.
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

Notice 26-118 says park the vehicle and wait for the remedy. Bright Axle matched two VINs. A draft tells those owners they can keep driving until the part arrives.

### Example data

```text
notice: 26-118
remedy in the notice: park, wait for the part, dealer will call
VINs matched: 2, both in her sold file
failure rate: not in the notice
booking: Carla's desk, 403-555-0199
draft line: you can drive until the part arrives
```

### Example outcome

**Owner note**
Notice 26-118 says park the vehicle. This note repeats that. It does not say they can keep driving.

We matched two VINs in our file. This note goes to those two owners only.
The notice does not give a failure rate. None is added.
To book: call Carla's desk, 403-555-0199.
This note does not decide that a recall exists. It follows the notice they have.

## Anti-patterns

- A homemade defect claim
- A VIN that did not match
- Advice that contradicts the notice

## Related skills

- `dealer-morning-review`
- `warranty-file-review`
