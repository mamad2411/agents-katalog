---
name: presentation-structure
description: "Structure a presentation so the argument is clear and the audience knows what to do. Use when the user mentions presentation structure, slide deck outline, how to structure my deck, presentation outline, or asks for a presentation outline. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'presentation-structure' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Presentation Structure

Structure a presentation so the argument is clear and the audience knows what to do.

## When to use this skill

Use this skill when the user:

- presentation structure
- slide deck outline
- how to structure my deck
- presentation outline
- PowerPoint structure

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

- The audience and their prior knowledge
- The one thing they must leave knowing or doing
- The available time
- Any must-include sections

## Workflow


### 1. Step 1

State the one decision or action the audience must take. A presentation with two asks usually gets neither.
### 2. Build the structure backward from that decision

what do they need to believe to take that action?
### 3. Step 3

Sequence sections to remove the biggest objection first, not to tell the story in chronological order.
### 4. Step 4

Name the sections by their claim, not their topic. 'Costs are under control' beats 'Financials'.
### 5. Step 5

Limit to the time they have. Twelve minutes of material does not fit in eight.
### 6. Step 6

Leave room for questions and do not plan a conclusion after time is up.

## Output

Deliver a **presentation outline**.

- Purpose of this presentation outline, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a presentation outline by 30 September 2026. A 10-minute all-hands presentation has 22 slides and three asks.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A 10-minute all-hands presentation has 22 slides and three asks.

The audience and their prior knowledge: people who already buy from Northline Studio
The one thing they must leave knowing or doing: two deals cited from memory. Neither has a written loss reason
The available time: five working days, due 30 September 2026
Any must-include sections: Inbox triage batch. Partly documented: the what is written down, the who is not
```

### Example outcome

**Presentation outline**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A restructured outline with 8 slides, one clear ask, and two minutes for questions.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The audience and their prior knowledge | people who already buy from Northline Studio | Needs confirmation |
| The one thing they must leave knowing or doing | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| The available time | five working days, due 30 September 2026 | Carried into the draft |
| Any must-include sections | Inbox triage batch. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. State the one decision or action the audience must take. A presentation with two asks usually gets neither**

**2. Build the structure backward from that decision**  
what do they need to believe to take that action?

**3. Sequence sections to remove the biggest objection first, not to tell the story in chronological order**

**4. Name the sections by their claim, not their topic. 'Costs are under control' beats 'Financials'**

**5. Limit to the time they have. Twelve minutes of material does not fit in eight**

**Deliberately not done**
- A structure that covers everything because it might come up.
- More slides than time allows.
- Section titles that are topics not arguments.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A structure that covers everything because it might come up
- More slides than time allows
- Section titles that are topics not arguments

## Related skills

- `executive-one-pager`
- `writing-brief`
