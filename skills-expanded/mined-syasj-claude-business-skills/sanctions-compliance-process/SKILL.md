---
name: sanctions-compliance-process
description: "Describe how a legitimate screening process should handle a possible match, for compliance staff. Not evasion advice. Use when the user mentions sanctions screening, possible match, screening operations, name match review, or asks for a screening operations note. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sanctions-compliance-process' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sanctions Screening Operations

Describe how a legitimate screening process should handle a possible match, for compliance staff. Not evasion advice.

## When to use this skill

Use this skill when the user:

- sanctions screening
- possible match
- screening operations
- name match review

## When not to use this skill

- Sanctions evasion
- Altering records to defeat screening

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The match information they are allowed to share
- Their escalation policy
- The business process paused
- The compliance owner

## Workflow


### 1. Step 1

Treat a possible match as unresolved until their compliance owner clears it.
### 2. Step 2

Do not advise altering a name, address, or ownership record to avoid a match.
### 3. Step 3

List the documents their policy already uses to distinguish a false positive.
### 4. Step 4

Pause the prohibited transaction if their policy says to pause.
### 5. Step 5

Record the decision and the reviewer.
### 6. Step 6

This skill does not determine whether a person is sanctioned and does not help anyone evade screening.

## Output

Deliver a **screening operations note**.

- Purpose of this screening operations note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a screening operations note by 30 September 2026. Sales wants to tweak a customer name so the screening tool stops flagging it.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Sales wants to tweak a customer name so the screening tool stops flagging it.

The match information they are allowed to share: plain, for people who already know the context. No house guide attached
Their escalation policy: their one-page rule dated 2 Mar 2026. No exception log
The business process paused: email to Priya Shah. No written steps after 1 Sep 2026
The compliance owner: Priya Shah, controller
```

### Example outcome

**Screening operations note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A refusal of the tweak, a pause recommendation, and a handoff to the compliance owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The match information they are allowed to share | plain, for people who already know the context. No house guide attached | Needs confirmation |
| Their escalation policy | their one-page rule dated 2 Mar 2026. No exception log | Carried into the draft |
| The business process paused | email to Priya Shah. No written steps after 1 Sep 2026 | Carried into the draft |
| The compliance owner | Priya Shah, controller | Needs confirmation |

**How this draft was built**

**1. Treat a possible match as unresolved until their compliance owner clears it**

**2. Do not advise altering a name, address, or ownership record to avoid a match**

**3. List the documents their policy already uses to distinguish a false positive**

**4. Pause the prohibited transaction if their policy says to pause**

**5. Record the decision and the reviewer**

**Deliberately not done**
- Advice to alter records to dodge a match.
- A homemade legal clearance.
- Skipping the compliance owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Advice to alter records to dodge a match
- A homemade legal clearance
- Skipping the compliance owner

## Related skills

- `third-party-risk`
- `ethics-hotline-triage`
