---
name: skill-finder
description: "Recommend the smallest set of skills in this library for a task, and say what not to load. Use when the user mentions which skill, skill finder, what skill should I use, help me pick a workflow, or asks for a skill recommendation. Skill library skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: library
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'skill-finder' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Skill Finder

Recommend the smallest set of skills in this library for a task, and say what not to load.

## When to use this skill

Use this skill when the user:

- which skill
- skill finder
- what skill should I use
- help me pick a workflow

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Library skills help you choose, write, and trust agent skills. They do not grant extra permissions or weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The task
- The domain
- Whether a regulated professional must review
- Skills already loaded

## Workflow


### 1. Step 1

Restate the task in one sentence.
### 2. Step 2

Pick the one skill whose output matches the task. Add a second only if the task truly crosses domains.
### 3. Step 3

Prefer a specialist skill over a general strategy skill when the output is a defined artifact.
### 4. Step 4

Say which nearby skill is the wrong one and why.
### 5. Step 5

If the task asks for deception, evasion, or harm, do not route to a skill. Refuse and offer a legitimate alternative.
### 6. Step 6

Remind the user that descriptions load for installed skills, so they should install a domain rather than the whole library.

## Output

Deliver a **skill recommendation**.

- Purpose of this skill recommendation, in two sentences.
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

Yasir Jilani, author at Practice Skills in Airdrie, needs a skill recommendation by 30 September 2026. A user asks for a cash view and also wants a full corporate strategy loaded.

### Example data

```text
From: Yasir Jilani, author
Organization: Practice Skills, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A user asks for a cash view and also wants a full corporate strategy loaded.

The task: A user asks for a cash view and also wants a full corporate strategy loaded. Stated once, in the ask. Not written down anywhere else
The domain: plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached
Whether a regulated professional must review: plugins/finance/cash-flow-forecast. Partly documented: the what is written down, the who is not
Skills already loaded: 50 in the last period. No prior period attached, so no trend
```

### Example outcome

**Skill recommendation**
To: Yasir Jilani, author, Practice Skills
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A recommendation of cash-flow-forecast only, with strategy skills named as unnecessary for this task.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The task | A user asks for a cash view and also wants a full corporate strategy loaded. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The domain | plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Whether a regulated professional must review | plugins/finance/cash-flow-forecast. Partly documented: the what is written down, the who is not | Carried into the draft |
| Skills already loaded | 50 in the last period. No prior period attached, so no trend | Needs confirmation |

**How this draft was built**

**1. Restate the task in one sentence**

**2. Pick the one skill whose output matches the task. Add a second only if the task truly crosses domains**

**3. Prefer a specialist skill over a general strategy skill when the output is a defined artifact**

**4. Say which nearby skill is the wrong one and why**

**5. If the task asks for deception, evasion, or harm, do not route to a skill. Refuse and offer a legitimate alternative**

**Deliberately not done**
- Loading five skills for a simple memo.
- Routing a harmful request into a skill.
- Recommending a skill you cannot name.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Yasir Jilani by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Loading five skills for a simple memo
- Routing a harmful request into a skill
- Recommending a skill you cannot name

## Related skills

- `skill-authoring`
- `skill-library-trust-review`
