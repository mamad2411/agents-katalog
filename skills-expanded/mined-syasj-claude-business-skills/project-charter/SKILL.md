---
name: project-charter
description: "Write a project charter that names the outcome, the sponsor, the constraint, and what is out of scope. Use when the user mentions project charter, initiate a project, project brief, charter draft, or asks for a project charter. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'project-charter' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Project Charter

Write a project charter that names the outcome, the sponsor, the constraint, and what is out of scope.

## When to use this skill

Use this skill when the user:

- project charter
- initiate a project
- project brief
- charter draft

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Delivery plans are commitments only when owners and dates are real. Do not fabricate status to make a report look healthy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The outcome
- The sponsor
- The constraint
- Known non-goals

## Workflow


### 1. Step 1

Write the outcome as a change in the world, not as 'deliver the project'.
### 2. Step 2

Name one sponsor who can resolve priority.
### 3. State the binding constraint

date, cost, or scope. All three cannot be sacred.
### 4. Step 4

List non-goals.
### 5. Step 5

Record assumptions that would cancel the work if false.
### 6. Step 6

Define done at the charter level so later status has something to point at.

## Output

Deliver a **project charter**.

- Purpose of this project charter, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a project charter by 30 September 2026. A sponsor wants a fixed date, fixed scope, and fixed cost with no contingency.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A sponsor wants a fixed date, fixed scope, and fixed cost with no contingency.

The outcome: A sponsor wants a fixed date, fixed scope, and fixed cost with no contingency. Stated once, in the ask. Not written down anywhere else
The sponsor: Milestone 3 handover, recorded 14 September 2026. No supporting file attached
The constraint: no extra headcount, and no result that is not in this file
Known non-goals: A sponsor wants a fixed date, fixed scope, and fixed cost with no contingency. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Project charter**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Forces a binding constraint and writes the non-goals.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcome | A sponsor wants a fixed date, fixed scope, and fixed cost with no contingency. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The sponsor | Milestone 3 handover, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The constraint | no extra headcount, and no result that is not in this file | Carried into the draft |
| Known non-goals | A sponsor wants a fixed date, fixed scope, and fixed cost with no contingency. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Write the outcome as a change in the world, not as 'deliver the project'**

**2. Name one sponsor who can resolve priority**

**3. State the binding constraint**  
date, cost, or scope. All three cannot be sacred.

**4. List non-goals**

**5. Record assumptions that would cancel the work if false**

**Deliberately not done**
- A charter with no sponsor.
- All of scope, date, and cost marked fixed.
- No non-goals.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A charter with no sponsor
- All of scope, date, and cost marked fixed
- No non-goals

## Related skills

- `milestone-plan`
- `raid-log`
