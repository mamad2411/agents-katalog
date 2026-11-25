---
name: status-report
description: "Write a status report that leads with the decision needed and the variance from plan. Use when the user mentions status report, project status, weekly status, steerco update, or asks for a status report. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'status-report' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Status Report

Write a status report that leads with the decision needed and the variance from plan.

## When to use this skill

Use this skill when the user:

- status report
- project status
- weekly status
- steerco update

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

- Plan versus actual
- Decisions needed
- Risks that changed
- The audience

## Workflow


### 1. Step 1

Lead with the period, the overall status, and the decision needed.
### 2. Step 2

Define the status rule they use. If they have none, propose one and label it a proposal.
### 3. Step 3

Report variance in milestone, scope, or cost using their facts.
### 4. Step 4

Separate a new risk from an issue.
### 5. Step 5

Ask for the decision in a sentence the sponsor can answer.
### 6. Step 6

Do not turn a late milestone green because the team worked hard.

## Output

Deliver a **status report**.

- Purpose of this status report, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a status report by 30 September 2026. A report lists many completed tasks while the customer milestone slipped two weeks.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A report lists many completed tasks while the customer milestone slipped two weeks.

Plan versus actual: Change request 118. Stated in the ask, not documented anywhere else
Decisions needed: A report lists many completed tasks while the customer milestone slipped two weeks
Risks that changed: Milestone 3 handover is open. No score in the file
The audience: people who already buy from Harbor Goods
```

### Example outcome

**Status report**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks the slip, leads with the needed decision, and refuses effort as a substitute for status.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Plan versus actual | Change request 118. Stated in the ask, not documented anywhere else | Needs confirmation |
| Decisions needed | A report lists many completed tasks while the customer milestone slipped two weeks | Carried into the draft |
| Risks that changed | Milestone 3 handover is open. No score in the file | Carried into the draft |
| The audience | people who already buy from Harbor Goods | Needs confirmation |

**How this draft was built**

**1. Lead with the period, the overall status, and the decision needed**

**2. Define the status rule they use. If they have none, propose one and label it a proposal**

**3. Report variance in milestone, scope, or cost using their facts**

**4. Separate a new risk from an issue**

**5. Ask for the decision in a sentence the sponsor can answer**

**Deliberately not done**
- A green status on a missed milestone.
- Activity with no variance.
- A buried ask.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A green status on a missed milestone
- Activity with no variance
- A buried ask

## Related skills

- `stakeholder-update`
- `raid-log`
