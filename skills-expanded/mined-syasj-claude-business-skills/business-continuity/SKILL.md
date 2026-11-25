---
name: business-continuity
description: "Draft a continuity plan for a named disruption, with a manual path and a named leader. Use when the user mentions business continuity, BCP, what if this system is down, continuity plan, or asks for a continuity plan. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'business-continuity' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Business Continuity Plan

Draft a continuity plan for a named disruption, with a manual path and a named leader.

## When to use this skill

Use this skill when the user:

- business continuity
- BCP
- what if this system is down
- continuity plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The disruption they want to survive
- The critical process
- Manual workaround if any
- The leader

## Workflow


### 1. Step 1

Name the disruption and the process that must continue. A plan for 'anything' is not a plan.
### 2. Step 2

Define the acceptable pause in their words.
### 3. Step 3

Write the workaround with the people and tools it actually needs.
### 4. Step 4

Name the leader and the alternate.
### 5. Step 5

List who must be told.
### 6. Step 6

Test the workaround on a date. An untested workaround is a rumor.

## Output

Deliver a **continuity plan**.

- Purpose of this continuity plan, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a continuity plan by 30 September 2026. The team has a continuity binder and nobody knows who declares the workaround in effect.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

The team has a continuity binder and nobody knows who declares the workaround in effect.

The disruption they want to survive: Tuesday shift, recorded 14 September 2026. No supporting file attached
The critical process: email to Diane Cho. No written steps after 1 Sep 2026
Manual workaround if any: Tuesday shift; SOP 118 receiving. Both unassigned as of 14 September 2026
The leader: Tuesday shift, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Continuity plan**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A plan for one disruption, with a leader, a manual path, and a test date.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The disruption they want to survive | Tuesday shift, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The critical process | email to Diane Cho. No written steps after 1 Sep 2026 | Carried into the draft |
| Manual workaround if any | Tuesday shift; SOP 118 receiving. Both unassigned as of 14 September 2026 | Carried into the draft |
| The leader | Tuesday shift, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Name the disruption and the process that must continue. A plan for 'anything' is not a plan**

**2. Define the acceptable pause in their words**

**3. Write the workaround with the people and tools it actually needs**

**4. Name the leader and the alternate**

**5. List who must be told**

**Deliberately not done**
- A plan with no leader.
- An untested workaround presented as ready.
- A plan so broad it cannot be used.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A plan with no leader
- An untested workaround presented as ready
- A plan so broad it cannot be used

## Related skills

- `backup-and-restore-test`
- `disaster-recovery-brief`
