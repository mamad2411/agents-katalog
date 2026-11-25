---
name: activation-gap
description: "Find where new workspaces stall, from the step counts the user exported. Use when the user mentions activation, time to value, onboarding drop, activation gap, or asks for a activation note. SaaS skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: saas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'activation-gap' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Activation Gap

Find where new workspaces stall, from the step counts the user exported.

## When to use this skill

Use this skill when the user:

- activation
- time to value
- onboarding drop
- activation gap

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent churn, revenue, retention, or a security certification. If the export is missing, say so.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The steps
- The counts
- The definition of activated
- The week

## Workflow


### 1. Step 1

Use their definition of activated.
### 2. Step 2

Show the count at each step.
### 3. Step 3

Name the largest drop.
### 4. Step 4

Do not invent a reason for the drop.
### 5. Step 5

Recommend one step to fix, not a redesign.
### 6. Step 6

Say if the export is one week only.

## Output

Deliver a **activation note**.

- Purpose of this activation note, in two sentences.
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

Fieldnote defines activated as inviting a teammate. In the week of 8 September, 200 trials started, 90 created a project, and 20 sent an invite.

### Example data

```text
week: 8-14 Sep 2026
trials: 200
created a project: 90
invited a teammate: 20
activated means: the invite
interviews: none
```

### Example outcome

**Activation note**
The gap is the invite. 90 created a project. 20 invited someone. Activated, by their definition, is 20 of 200.
No reason is in this note. Nobody was interviewed.
One week only. Not a redesign.
Next question, not a build: why the 70 who had a project did not invite. That question is open.

## Anti-patterns

- A reason with no interview
- A redesign from one week
- A definition they do not use

## Related skills

- `trial-to-paid`
- `onboarding-success-plan`
