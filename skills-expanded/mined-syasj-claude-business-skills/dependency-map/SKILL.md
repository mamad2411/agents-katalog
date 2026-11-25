---
name: dependency-map
description: "Map delivery dependencies so external waits have owners and dates, not just arrows. Use when the user mentions dependency map, cross-team dependencies, who are we waiting on, dependency review, or asks for a dependency map. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'dependency-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Dependency Map

Map delivery dependencies so external waits have owners and dates, not just arrows.

## When to use this skill

Use this skill when the user:

- dependency map
- cross-team dependencies
- who are we waiting on
- dependency review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Delivery plans are commitments only when owners and dates are real. Do not fabricate status to make a report look healthy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The work packages
- External teams or vendors
- Dates they have given
- The consequence of a slip

## Workflow


### 1. Step 1

List dependencies that can slip the outcome. Internal niceties stay off the map.
### 2. Step 2

Each dependency needs a giver, a receiver, a date, and evidence of done.
### 3. Step 3

Mark dates that were not confirmed.
### 4. Step 4

Show the consequence of the top slip.
### 5. Step 5

Escalate unowned dependencies. An arrow is not an owner.
### 6. Step 6

Review the map at the operating cadence, not only when it is already late.

## Output

Deliver a **dependency map**.

- Purpose of this dependency map, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a dependency map by 30 September 2026. A Gantt chart shows a vendor delivery with no named vendor owner.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A Gantt chart shows a vendor delivery with no named vendor owner.

The work packages: Milestone 3 handover; RAID item 12. Both unassigned as of 14 September 2026
External teams or vendors: two people on shift, one off
Dates they have given: 30 September 2026
The consequence of a slip: Milestone 3 handover, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Dependency map**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks the date unconfirmed and assigns an internal owner to chase it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The work packages | Milestone 3 handover; RAID item 12. Both unassigned as of 14 September 2026 | Needs confirmation |
| External teams or vendors | two people on shift, one off | Carried into the draft |
| Dates they have given | 30 September 2026 | Carried into the draft |
| The consequence of a slip | Milestone 3 handover, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. List dependencies that can slip the outcome. Internal niceties stay off the map**

**2. Each dependency needs a giver, a receiver, a date, and evidence of done**

**3. Mark dates that were not confirmed**

**4. Show the consequence of the top slip**

**5. Escalate unowned dependencies. An arrow is not an owner**

**Deliberately not done**
- Unowned arrows.
- Unconfirmed dates drawn as promises.
- A map that includes every minor task.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Unowned arrows
- Unconfirmed dates drawn as promises
- A map that includes every minor task

## Related skills

- `milestone-plan`
- `raid-log`
