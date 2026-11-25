---
name: audit-response
description: "Draft a response to an audit request that is complete, tied to evidence, and not misleading. Use when the user mentions audit response, auditor question, management response, finding response, or asks for a audit response. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'audit-response' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Audit Response

Draft a response to an audit request that is complete, tied to evidence, and not misleading.

## When to use this skill

Use this skill when the user:

- audit response
- auditor question
- management response
- finding response

## When not to use this skill

- Misleading an auditor
- Altering evidence

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

- The request or finding
- The evidence
- The process owner
- The due date

## Workflow


### 1. Step 1

Restate the request so you answer the question asked.
### 2. Step 2

Point to evidence. Do not describe a control that the evidence does not show.
### 3. Step 3

If the finding is fair, say what will change, with an owner and a date.
### 4. Step 4

If the finding is wrong, explain with evidence, not with adjectives.
### 5. Step 5

Do not coach anyone to alter evidence.
### 6. Step 6

Mark drafts for the process owner to approve before they go to the auditor.

## Output

Deliver a **audit response**.

- Purpose of this audit response, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an audit response by 30 September 2026. A draft response describes a monthly review that exists only in the policy, not in practice.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A draft response describes a monthly review that exists only in the policy, not in practice.

The request or finding: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The evidence: one PDF, 2 pages, dated 14 September 2026
The process owner: Priya Shah, controller
The due date: 30 September 2026
```

### Example outcome

**Audit response**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Tells the truth about the gap and commits to an owned fix instead of a fictional review.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The request or finding | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The process owner | Priya Shah, controller | Carried into the draft |
| The due date | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Restate the request so you answer the question asked**

**2. Point to evidence. Do not describe a control that the evidence does not show**

**3. If the finding is fair, say what will change, with an owner and a date**

**4. If the finding is wrong, explain with evidence, not with adjectives**

**5. Do not coach anyone to alter evidence**

**Deliberately not done**
- Misleading the auditor.
- Altering evidence.
- A promise with no owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Misleading the auditor
- Altering evidence
- A promise with no owner

## Related skills

- `sox-walkthrough`
- `audit-prep-pbc`
