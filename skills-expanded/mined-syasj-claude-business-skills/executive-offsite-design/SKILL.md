---
name: executive-offsite-design
description: "Design an offsite that leaves with decisions, not a pile of flip charts. Use when the user mentions executive offsite, leadership offsite, strategy day, offsite agenda, or asks for a offsite design and pre-work. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'executive-offsite-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Executive Offsite Design

Design an offsite that leaves with decisions, not a pile of flip charts.

## When to use this skill

Use this skill when the user:

- executive offsite
- leadership offsite
- strategy day
- offsite agenda

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

- The decisions the offsite must produce
- Attendees
- Length of the offsite
- Sensitive topics the user wants handled carefully

## Workflow


### 1. Pick two outcomes

An offsite that tries to settle culture, budget, product, and hiring will settle none of them.
### 2. Send pre-work

A short memo per outcome, read before the day. The offsite is for disagreement and decision, not live briefing.
### 3. Design the room

Small working sessions before a plenary decision. Give skeptics a scheduled voice so they do not ambush the end.
### 4. Facilitate the choice

Each session ends with a recommended choice, the alternative, and what would reopen it.
### 5. Protect breaks

Decisions get worse when the agenda is a forced march. Say so if the user has overpacked the day.
### 6. Leave with owners

The last block assigns owners and dates. No owner means the topic was a discussion, and the notes should say that.

## Output

Deliver a **offsite design and pre-work**.

- Purpose of this offsite design and pre-work, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs an offsite design and pre-work by 30 September 2026. A CEO has one day with the exec team and wants to leave with a focus decision and a hiring principle.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A CEO has one day with the exec team and wants to leave with a focus decision and a hiring principle.

The decisions the offsite must produce: A CEO has one day with the exec team and wants to leave with a focus decision and a hiring principle
Attendees: Mara Chen plus two others named in the thread. No distribution list attached
Length of the offsite: plain, for people who already know the context. No house guide attached
Sensitive topics the user wants handled carefully: email and billing address only. They stated no health or payment data
```

### Example outcome

**Offsite design and pre-work**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
An agenda with two outcomes, pre-reads, a decision block for each, and a closing owner assignment.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decisions the offsite must produce | A CEO has one day with the exec team and wants to leave with a focus decision and a hiring principle | Needs confirmation |
| Attendees | Mara Chen plus two others named in the thread. No distribution list attached | Carried into the draft |
| Length of the offsite | plain, for people who already know the context. No house guide attached | Carried into the draft |
| Sensitive topics the user wants handled carefully | email and billing address only. They stated no health or payment data | Needs confirmation |

**How this draft was built**

**1. Pick two outcomes**  
An offsite that tries to settle culture, budget, product, and hiring will settle none of them.

**2. Send pre-work**  
A short memo per outcome, read before the day. The offsite is for disagreement and decision, not live briefing.

**3. Design the room**  
Small working sessions before a plenary decision. Give skeptics a scheduled voice so they do not ambush the end.

**4. Facilitate the choice**  
Each session ends with a recommended choice, the alternative, and what would reopen it.

**5. Protect breaks**  
Decisions get worse when the agenda is a forced march. Say so if the user has overpacked the day.

**Deliberately not done**
- An offsite with no pre-read and twelve topics.
- Trust falls instead of the decision the team came to make.
- Notes that imply agreement when the room did not agree.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An offsite with no pre-read and twelve topics.
- Trust falls instead of the decision the team came to make.
- Notes that imply agreement when the room did not agree.

## Related skills

- `board-meeting-facilitator`
- `strategic-plan-builder`
- `decision-log`
