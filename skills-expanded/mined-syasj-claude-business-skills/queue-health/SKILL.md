---
name: queue-health
description: "Review a queue's age, arrival, and handling so the team fixes flow instead of only urging people to work faster. Use when the user mentions queue health, backlog aging, ticket backlog, work in process, or asks for a queue health review. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'queue-health' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Queue Health

Review a queue's age, arrival, and handling so the team fixes flow instead of only urging people to work faster.

## When to use this skill

Use this skill when the user:

- queue health
- backlog aging
- ticket backlog
- work in process

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Arrivals and completions
- Age of the oldest items
- Who is blocked
- Special handling rules

## Workflow


### 1. Step 1

Show arrivals versus completions. A pep talk will not fix a queue that arrives faster than it leaves.
### 2. Step 2

Age the oldest items. The tail matters more than the average if they have the data.
### 3. Step 3

Find blocked work and name the blocker.
### 4. Step 4

Check whether special handling is jumping the queue and starving older work.
### 5. Step 5

Recommend a WIP limit, a policy change, or a demand cut before adding people, if the math shows a flow problem.
### 6. Step 6

Set the review cadence.

## Output

Deliver a **queue health review**.

- Purpose of this queue health review, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a queue health review by 30 September 2026. Leaders want the team to stay late, but arrivals have exceeded completions for six weeks.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

Leaders want the team to stay late, but arrivals have exceeded completions for six weeks.

Arrivals and completions: two deals cited from memory. Neither has a written loss reason
Age of the oldest items: SOP 118 receiving, recorded 14 September 2026. No supporting file attached
Who is blocked: Diane Cho, operations manager
Special handling rules: their one-page rule dated 2 Mar 2026. No exception log since
```

### Example outcome

**Queue health review**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the imbalance and recommends a demand or policy change before overtime becomes the system.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Arrivals and completions | two deals cited from memory. Neither has a written loss reason | Needs confirmation |
| Age of the oldest items | SOP 118 receiving, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Who is blocked | Diane Cho, operations manager | Carried into the draft |
| Special handling rules | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |

**How this draft was built**

**1. Show arrivals versus completions. A pep talk will not fix a queue that arrives faster than it leaves**

**2. Age the oldest items. The tail matters more than the average if they have the data**

**3. Find blocked work and name the blocker**

**4. Check whether special handling is jumping the queue and starving older work**

**5. Recommend a WIP limit, a policy change, or a demand cut before adding people, if the math shows a flow problem**

**Deliberately not done**
- Blaming individuals for an arrival-rate problem.
- Managing only the average.
- Ignoring blocked work.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Blaming individuals for an arrival-rate problem
- Managing only the average
- Ignoring blocked work

## Related skills

- `capacity-plan`
- `ticket-quality-review`
