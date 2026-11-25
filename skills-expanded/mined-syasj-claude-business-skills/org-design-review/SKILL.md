---
name: org-design-review
description: "Review a proposed org change against the work that must happen, not against a fashionable span-of-control number. Use when the user mentions org design, restructure, span of control, team structure, or asks for a org design review. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'org-design-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Org Design Review

Review a proposed org change against the work that must happen, not against a fashionable span-of-control number.

## When to use this skill

Use this skill when the user:

- org design
- restructure
- span of control
- team structure

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The work the organization must do
- The proposed structure
- Known single points of failure
- What problem the redesign is meant to solve

## Workflow


### 1. Start with the problem

Slow decisions, unclear ownership, or a new strategy. A redraw with no problem will create a new one.
### 2. Map work to owners

Every critical outcome needs one owner. Shared ownership of a customer outcome is a finding.
### 3. Spans and layers

Comment on spans using their reality, not a magic number from a article. Too many layers shows up as slow decisions they can name.
### 4. Transitions

Who reports to whom on day one, and what is temporary. Do not leave people in limbo.
### 5. Cost

Management load and role changes, qualitatively, unless they gave numbers.
### 6. People impact

Be honest about role loss if the user said it exists. Do not help conceal a layoff from people who must be told through the proper process. Do not draft deceptive scripts.

## Output

Deliver a **org design review**.

- Purpose of this org design review, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs an org design review by 30 September 2026. A CEO wants squads because a conference recommended them, but product decisions are already stuck between two leaders.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A CEO wants squads because a conference recommended them, but product decisions are already stuck between two leaders.

The work the organization must do: Jordan Hale; Sam Okonkwo. Both unassigned as of 14 September 2026
The proposed structure: Jordan Hale, recorded 14 September 2026. No supporting file attached
Known single points of failure: A CEO wants squads because a conference recommended them, but product decisions are already stuck between two leaders. Stated once, in the ask. Not written down anywhere else
What problem the redesign is meant to solve: A CEO wants squads because a conference recommended them, but product decisions are already stuck between two leaders. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Org design review**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the stuck decision, assigns one owner, and treats squads as optional rather than as the goal.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The work the organization must do | Jordan Hale; Sam Okonkwo. Both unassigned as of 14 September 2026 | Needs confirmation |
| The proposed structure | Jordan Hale, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Known single points of failure | A CEO wants squads because a conference recommended them, but product decisions are already stuck between two leaders. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| What problem the redesign is meant to solve | A CEO wants squads because a conference recommended them, but product decisions are already stuck between two leaders. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Start with the problem**  
Slow decisions, unclear ownership, or a new strategy. A redraw with no problem will create a new one.

**2. Map work to owners**  
Every critical outcome needs one owner. Shared ownership of a customer outcome is a finding.

**3. Spans and layers**  
Comment on spans using their reality, not a magic number from a article. Too many layers shows up as slow decisions they can name.

**4. Transitions**  
Who reports to whom on day one, and what is temporary. Do not leave people in limbo.

**5. Cost**  
Management load and role changes, qualitatively, unless they gave numbers.

**Deliberately not done**
- A structure copied from a famous company.
- No owner for the core outcome.
- A deceptive script about a layoff.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A structure copied from a famous company.
- No owner for the core outcome.
- A deceptive script about a layoff.

## Related skills

- `workforce-plan`
- `change-leadership`
- `succession-plan`
