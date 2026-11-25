---
name: operating-cadence
description: "Design the weekly, monthly, and quarterly meetings that keep a strategy alive without drowning the team. Use when the user mentions operating cadence, meeting rhythm, weekly business review, how should leadership meet, or asks for a operating cadence. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'operating-cadence' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Operating Cadence

Design the weekly, monthly, and quarterly meetings that keep a strategy alive without drowning the team.

## When to use this skill

Use this skill when the user:

- operating cadence
- meeting rhythm
- weekly business review
- how should leadership meet

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

- Team size and roles
- Decisions that currently stall
- Existing meetings the user wants to keep or kill
- Time zone or capacity constraints

## Workflow


### 1. Start from decisions

List the decisions that are late or relitigated. Meetings exist to make those decisions, not to share updates that could be written.
### 2. Design three loops

A weekly operating review, a monthly performance look, and a quarterly strategy check. Do not add a fourth loop unless the user has a specific failure it solves.
### 3. Define inputs

Each meeting gets a one-page pre-read and a named owner. No pre-read, no meeting.
### 4. Kill overlaps

Recommend which current meetings to cancel or merge. A new cadence on top of the old one is how calendars die.
### 5. Set the tone

Issues are raised with a proposed move. Status theater is out of scope.
### 6. Pilot it

Recommend a six-week pilot and what would prove the cadence is worth keeping.

## Output

Deliver a **operating cadence**.

- Purpose of this operating cadence, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs an operating cadence by 30 September 2026. A 40-person company has eleven recurring leadership meetings and still misses hiring and cash decisions.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A 40-person company has eleven recurring leadership meetings and still misses hiring and cash decisions.

Team size and roles: two people on shift, one off
Decisions that currently stall: A 40-person company has eleven recurring leadership meetings and still misses hiring and cash decisions
Existing meetings the user wants to keep or kill: Lantern Inn, last reviewed 14 September 2026. No owner named since
Time zone or capacity constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Operating cadence**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A three-loop cadence, the meetings to cancel, the pre-read owner for each loop, and a six-week pilot test.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Team size and roles | two people on shift, one off | Needs confirmation |
| Decisions that currently stall | A 40-person company has eleven recurring leadership meetings and still misses hiring and cash decisions | Carried into the draft |
| Existing meetings the user wants to keep or kill | Lantern Inn, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Time zone or capacity constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Start from decisions**  
List the decisions that are late or relitigated. Meetings exist to make those decisions, not to share updates that could be written.

**2. Design three loops**  
A weekly operating review, a monthly performance look, and a quarterly strategy check. Do not add a fourth loop unless the user has a specific failure it solves.

**3. Define inputs**  
Each meeting gets a one-page pre-read and a named owner. No pre-read, no meeting.

**4. Kill overlaps**  
Recommend which current meetings to cancel or merge. A new cadence on top of the old one is how calendars die.

**5. Set the tone**  
Issues are raised with a proposed move. Status theater is out of scope.

**Deliberately not done**
- Adding standups to every team by default.
- A cadence with no cancelled meetings.
- Dashboards that take longer to prepare than the meeting itself.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Adding standups to every team by default.
- A cadence with no cancelled meetings.
- Dashboards that take longer to prepare than the meeting itself.

## Related skills

- `meeting-operating-system`
- `okrs-and-scorecard`
- `weekly-review`
