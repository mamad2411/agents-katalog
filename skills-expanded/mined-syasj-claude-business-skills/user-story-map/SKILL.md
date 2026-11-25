---
name: user-story-map
description: "Map the user's journey into slices of value so a release is a story, not a pile of tickets. Use when the user mentions story map, user story map, slice a release, journey to tickets, or asks for a story map. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'user-story-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# User Story Map

Map the user's journey into slices of value so a release is a story, not a pile of tickets.

## When to use this skill

Use this skill when the user:

- story map
- user story map
- slice a release
- journey to tickets

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The user and the job
- The backbone steps they take
- Candidate stories
- The first release goal

## Workflow


### 1. Backbone

The steps the user takes, in order. Internal tasks do not lead the map.
### 2. Stories under steps

Place each story under the step it serves. Orphan stories are a finding.
### 3. Slice

Draw a first release that completes a thin journey. A release that finishes only the left half of the journey is not releasable.
### 4. Later slices

What waits, and why.
### 5. Risks

The step with the least evidence.
### 6. Language

Stories a customer would recognize. No internal code names as the only label.

## Output

Deliver a **story map**.

- Purpose of this story map, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a story map by 30 September 2026. A team has 80 tickets and wants a release that builds the admin console before the user can finish the core job.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team has 80 tickets and wants a release that builds the admin console before the user can finish the core job.

The user and the job: Activation checklist, recorded 14 September 2026. No supporting file attached
The backbone steps they take: Activation checklist; Trial day-3 email. Both unassigned as of 14 September 2026
Candidate stories: 30 September 2026
The first release goal: A team has 80 tickets and wants a release that builds the admin console before the user can finish the core job. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Story map**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A map whose first slice completes the core job thinly, and parks the admin console.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The user and the job | Activation checklist, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The backbone steps they take | Activation checklist; Trial day-3 email. Both unassigned as of 14 September 2026 | Carried into the draft |
| Candidate stories | 30 September 2026 | Carried into the draft |
| The first release goal | A team has 80 tickets and wants a release that builds the admin console before the user can finish the core job. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Backbone**  
The steps the user takes, in order. Internal tasks do not lead the map.

**2. Stories under steps**  
Place each story under the step it serves. Orphan stories are a finding.

**3. Slice**  
Draw a first release that completes a thin journey. A release that finishes only the left half of the journey is not releasable.

**4. Later slices**  
What waits, and why.

**5. Risks**  
The step with the least evidence.

**Deliberately not done**
- A backlog dump called a map.
- A first release that cannot be used end to end.
- Stories with no user step.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A backlog dump called a map.
- A first release that cannot be used end to end.
- Stories with no user step.

## Related skills

- `prd-writer`
- `definition-of-done`
