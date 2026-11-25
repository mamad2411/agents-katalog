---
name: manager-one-on-one
description: "Set up a one-on-one that surfaces blockers and growth, not a status meeting in disguise. Use when the user mentions one on one, 1:1 agenda, manager conversation, skip-level questions, or asks for a one-on-one guide. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'manager-one-on-one' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Manager One-on-One

Set up a one-on-one that surfaces blockers and growth, not a status meeting in disguise.

## When to use this skill

Use this skill when the user:

- one on one
- 1:1 agenda
- manager conversation
- skip-level questions

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

- How often they meet
- What the employee wants from the meeting
- Current goals
- Known sensitive topics

## Workflow


### 1. Purpose

The employee's agenda first. Status belongs in the team channel unless it blocks them.
### 2. A small standing structure

Wins, blockers, feedback both ways, and one growth question. Cut the rest.
### 3. Feedback

Specific and recent. No saved-up surprise list.
### 4. Notes

Shared notes the employee can see, unless a topic is confidential for a stated reason.
### 5. Skip-levels

If asked, write questions that check the system, not questions that recruit complaints about a named peer.
### 6. Follow-through

Every meeting ends with at most two manager actions.

## Output

Deliver a **one-on-one guide**.

- Purpose of this one-on-one guide, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs an one-on-one guide by 30 September 2026. A new manager is using the weekly 1:1 to collect project status the team already tracks in a board.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A new manager is using the weekly 1:1 to collect project status the team already tracks in a board.

How often they meet: Sam Okonkwo, last reviewed 14 September 2026. No owner named since
What the employee wants from the meeting: Open coordinator role, last reviewed 14 September 2026. No owner named since
Current goals: A new manager is using the weekly 1:1 to collect project status the team already tracks in a board. Stated once, in the ask. Not written down anywhere else
Known sensitive topics: email and billing address only. They stated no health or payment data
```

### Example outcome

**One-on-one guide**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Moves status out, puts the employee's agenda first, and caps manager actions at two.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| How often they meet | Sam Okonkwo, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| What the employee wants from the meeting | Open coordinator role, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Current goals | A new manager is using the weekly 1:1 to collect project status the team already tracks in a board. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Known sensitive topics | email and billing address only. They stated no health or payment data | Needs confirmation |

**How this draft was built**

**1. Purpose**  
The employee's agenda first. Status belongs in the team channel unless it blocks them.

**2. A small standing structure**  
Wins, blockers, feedback both ways, and one growth question. Cut the rest.

**3. Feedback**  
Specific and recent. No saved-up surprise list.

**4. Notes**  
Shared notes the employee can see, unless a topic is confidential for a stated reason.

**5. Skip-levels**  
If asked, write questions that check the system, not questions that recruit complaints about a named peer.

**Deliberately not done**
- A 1:1 that is only a status update.
- Secret notes used against someone later without process.
- Fishing for gossip in a skip-level.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A 1:1 that is only a status update.
- Secret notes used against someone later without process.
- Fishing for gossip in a skip-level.

## Related skills

- `performance-review`
- `stay-interview`
- `coaching-session`
