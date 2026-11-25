---
name: deep-work-plan
description: "Plan focus time around real constraints, with a definition of done for the block. Use when the user mentions deep work, focus plan, time block, distraction plan, or asks for a focus plan. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'deep-work-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Deep Work Plan

Plan focus time around real constraints, with a definition of done for the block.

## When to use this skill

Use this skill when the user:

- deep work
- focus plan
- time block
- distraction plan

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

- The outcome of the block
- Available time
- Known interruptions
- The environment

## Workflow


### 1. Step 1

Define done for the block so it is not just 'work on the project'.
### 2. Step 2

Place the block where interruptions are actually lowest.
### 3. Step 3

Remove one distraction they control.
### 4. Step 4

Leave a buffer. A plan with no margin will be abandoned.
### 5. Step 5

Say what will be deferred so the block is not stolen by mail.
### 6. Step 6

Do not recommend monitoring other people to protect your focus.

## Output

Deliver a **focus plan**.

- Purpose of this focus plan, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a focus plan by 30 September 2026. A focus plan depends on coworkers never messaging, with no defer rule.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A focus plan depends on coworkers never messaging, with no defer rule.

The outcome of the block: A focus plan depends on coworkers never messaging, with no defer rule. Stated once, in the ask. Not written down anywhere else
Available time: five working days, due 30 September 2026
Known interruptions: Inbox triage batch. Stated in the ask, not documented anywhere else
The environment: the one named in the ask. Version and owner not recorded
```

### Example outcome

**Focus plan**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A plan with a done statement, a defer rule for mail, and no monitoring of others.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcome of the block | A focus plan depends on coworkers never messaging, with no defer rule. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Available time | five working days, due 30 September 2026 | Carried into the draft |
| Known interruptions | Inbox triage batch. Stated in the ask, not documented anywhere else | Carried into the draft |
| The environment | the one named in the ask. Version and owner not recorded | Needs confirmation |

**How this draft was built**

**1. Define done for the block so it is not just 'work on the project'**

**2. Place the block where interruptions are actually lowest**

**3. Remove one distraction they control**

**4. Leave a buffer. A plan with no margin will be abandoned**

**5. Say what will be deferred so the block is not stolen by mail**

**Deliberately not done**
- A block with no definition of done.
- Surveillance of colleagues.
- No buffer.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A block with no definition of done
- Surveillance of colleagues
- No buffer

## Related skills

- `weekly-review`
- `manager-one-on-one`
