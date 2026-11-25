---
name: readme-for-a-process
description: "Write a README for a repeated personal or team process so someone else can run it. Use when the user mentions process README, how I do this, document my workflow, checklist README, or asks for a process README. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'readme-for-a-process' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Process README

Write a README for a repeated personal or team process so someone else can run it.

## When to use this skill

Use this skill when the user:

- process README
- how I do this
- document my workflow
- checklist README

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Productivity systems serve the person's actual constraints. Do not recommend surveillance of colleagues or hidden monitoring.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The trigger
- The steps
- The tools
- The failure mode

## Workflow


### 1. Step 1

Open with when to use the process.
### 2. Step 2

Number the steps and the expected result.
### 3. Step 3

Name the failure mode and the fix.
### 4. Step 4

Keep secrets out of the README.
### 5. Step 5

Say who to ask.
### 6. Step 6

Cut steps that are superstition. If they cannot say why a step exists, mark it optional.

## Output

Deliver a **process README**.

- Purpose of this process README, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a process README by 30 September 2026. A README includes a personal access token so others can run a report.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A README includes a personal access token so others can run a report.

The trigger: Friday review block, recorded 14 September 2026. No supporting file attached
The steps: Friday review block; Inbox triage batch. Both unassigned as of 14 September 2026
The tools: the one named in the ask. Version and owner not recorded
The failure mode: Friday review block, first seen 14 September 2026. No root cause recorded yet
```

### Example outcome

**Process readme**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the token, names the secret store, and keeps the real steps.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The trigger | Friday review block, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The steps | Friday review block; Inbox triage batch. Both unassigned as of 14 September 2026 | Carried into the draft |
| The tools | the one named in the ask. Version and owner not recorded | Carried into the draft |
| The failure mode | Friday review block, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |

**How this draft was built**

**1. Open with when to use the process**

**2. Number the steps and the expected result**

**3. Name the failure mode and the fix**

**4. Keep secrets out of the README**

**5. Say who to ask**

**Deliberately not done**
- Secrets in the README.
- Steps with no trigger.
- Superstition presented as required.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Secrets in the README
- Steps with no trigger
- Superstition presented as required

## Related skills

- `sop-writer`
- `documentation-as-code`
