---
name: writing-brief
description: "Brief a piece of writing so the drafter knows the reader, the point, and the length. Use when the user mentions writing brief, help me outline, draft structure, what should this say, or asks for a writing brief. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'writing-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Writing Brief

Brief a piece of writing so the drafter knows the reader, the point, and the length.

## When to use this skill

Use this skill when the user:

- writing brief
- help me outline
- draft structure
- what should this say

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

- The reader
- The point
- The length
- The action you want

## Workflow


### 1. Step 1

Name the reader and what they already know.
### 2. Step 2

Write the point in one sentence.
### 3. Step 3

Choose a structure that serves the point.
### 4. Step 4

Set a length.
### 5. Step 5

List facts that must be included and claims that must not.
### 6. Step 6

Do not start drafting until the point is stable, unless the user asked for a rough exploration.

## Output

Deliver a **writing brief**.

- Purpose of this writing brief, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a writing brief by 30 September 2026. A brief says 'write something inspiring about the quarter' with no reader or ask.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A brief says 'write something inspiring about the quarter' with no reader or ask.

The reader: Mara Chen plus two others named in the thread. No distribution list attached
The point: A brief says 'write something inspiring about the quarter' with no reader or ask. Stated once, in the ask. Not written down anywhere else
The length: plain, for people who already know the context. No house guide attached
The action you want: Friday review block; Inbox triage batch. Both unassigned as of 14 September 2026
```

### Example outcome

**Writing brief**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the reader, one point, and the action, or stops until those exist.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The reader | Mara Chen plus two others named in the thread. No distribution list attached | Needs confirmation |
| The point | A brief says 'write something inspiring about the quarter' with no reader or ask. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| The length | plain, for people who already know the context. No house guide attached | Carried into the draft |
| The action you want | Friday review block; Inbox triage batch. Both unassigned as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Name the reader and what they already know**

**2. Write the point in one sentence**

**3. Choose a structure that serves the point**

**4. Set a length**

**5. List facts that must be included and claims that must not**

**Deliberately not done**
- A draft with no point.
- Unsupported claims required by the brief.
- No reader.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A draft with no point
- Unsupported claims required by the brief
- No reader

## Related skills

- `executive-one-pager`
- `creative-brief`
