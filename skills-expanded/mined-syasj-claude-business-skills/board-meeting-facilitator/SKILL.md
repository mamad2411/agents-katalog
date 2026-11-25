---
name: board-meeting-facilitator
description: "Design a board agenda that spends time on decisions and exceptions, and produce a clean minute skeleton afterward. Use when the user mentions board agenda, run a board meeting, board minutes, director meeting plan, or asks for a board agenda and minute skeleton. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'board-meeting-facilitator' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Board Meeting Facilitator

Design a board agenda that spends time on decisions and exceptions, and produce a clean minute skeleton afterward.

## When to use this skill

Use this skill when the user:

- board agenda
- run a board meeting
- board minutes
- director meeting plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Meeting length
- Decisions required
- Materials already prepared
- Attendees and anyone recused

## Workflow


### 1. Sort the agenda

Put decisions first, exceptions second, and FYI last. Cut FYI that was already in the pre-read.
### 2. Timebox

Assign minutes to each item. Leave a buffer. Do not schedule more decisions than the meeting can actually make.
### 3. Name the owner

Every item has a presenter and the decision type: approve, advise, or inform.
### 4. Handle conflicts

If the user flags a conflict or recusal, put it on the agenda before the related item. Do not draft legal conclusions about the conflict.
### 5. Prepare minutes

After the meeting, or from the user's notes, record decisions, dissents, and owners. Do not write color commentary.
### 6. Close the loop

List actions with owners and dates. A meeting without actions was a briefing.

## Output

Deliver a **board agenda and minute skeleton**.

- Purpose of this board agenda and minute skeleton, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a board agenda and minute skeleton by 30 September 2026. A chair has 90 minutes and three decisions: a budget revision, a key hire, and a customer concentration risk.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A chair has 90 minutes and three decisions: a budget revision, a key hire, and a customer concentration risk.

Meeting length: plain, for people who already know the context. No house guide attached
Decisions required: A chair has 90 minutes and three decisions: a budget revision, a key hire, and a customer concentration risk
Materials already prepared: Lumen Ledger, recorded 14 September 2026. No supporting file attached
Attendees and anyone recused: Mara Chen plus two others named in the thread. No distribution list attached
```

### Example outcome

**Board agenda and minute skeleton**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Records the ask, the vote line, and actions.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Meeting length | plain, for people who already know the context. No house guide attached | Needs confirmation |
| Decisions required | A chair has 90 minutes and three decisions: a budget revision, a key hire, and a customer concentration risk | Carried into the draft |
| Materials already prepared | Lumen Ledger, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Attendees and anyone recused | Mara Chen plus two others named in the thread. No distribution list attached | Needs confirmation |

**How this draft was built**

**1. Sort the agenda**  
Put decisions first, exceptions second, and FYI last. Cut FYI that was already in the pre-read.

**2. Timebox**  
Assign minutes to each item. Leave a buffer. Do not schedule more decisions than the meeting can actually make.

**3. Name the owner**  
Every item has a presenter and the decision type: approve, advise, or inform.

**4. Handle conflicts**  
If the user flags a conflict or recusal, put it on the agenda before the related item. Do not draft legal conclusions about the conflict.

**5. Prepare minutes**  
After the meeting, or from the user's notes, record decisions, dissents, and owners. Do not write color commentary.

**Deliberately not done**
- An agenda that is a tour of every department.
- Minutes that invent consensus.
- Skipping recusals the user already identified.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An agenda that is a tour of every department.
- Minutes that invent consensus.
- Skipping recusals the user already identified.

## Related skills

- `board-memo-writer`
- `decision-log`
- `operating-cadence`
