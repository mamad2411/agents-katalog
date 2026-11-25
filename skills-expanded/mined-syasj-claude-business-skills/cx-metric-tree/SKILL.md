---
name: cx-metric-tree
description: "Build a customer-experience metric tree that connects a relationship metric to operational inputs. Use when the user mentions CX metrics, customer metric tree, NPS driver tree, experience KPIs, or asks for a CX metric tree. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'cx-metric-tree' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# CX Metric Tree

Build a customer-experience metric tree that connects a relationship metric to operational inputs.

## When to use this skill

Use this skill when the user:

- CX metrics
- customer metric tree
- NPS driver tree
- experience KPIs

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not blame the customer. Do not invent policy exceptions. Do not ask a customer for passwords or full payment card numbers.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The relationship metric they use
- Operational inputs they can measure weekly
- Owners
- Known gaming risks

## Workflow


### 1. Step 1

Define the relationship metric they actually collect. Do not install a new score by fashion.
### 2. Add inputs a team can move

wait time, reopen rate, or time to value, if they have them.
### 3. Step 3

Pair speed with quality.
### 4. Step 4

Name the owner of each input.
### 5. Step 5

Note how the metric is gamed, such as survey begging. Recommend against it.
### 6. Step 6

Use their baseline or mark it unknown.

## Output

Deliver a **CX metric tree**.

- Purpose of this CX metric tree, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a CX metric tree by 30 September 2026. The company tracks NPS and wants the number up, with no operational input on the tree.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The company tracks NPS and wants the number up, with no operational input on the tree.

The relationship metric they use: plan 160, actual 90
Operational inputs they can measure weekly: Ticket 4418, recorded 14 September 2026. No supporting file attached
Owners: Rita Santos, support lead
Known gaming risks: Ticket 4412 is open. No score in the file
```

### Example outcome

**Cx metric tree**
Fieldnote · 14 September 2026 · Due 30 September 2026

**Decision**
Keeps their relationship metric and adds owned operational inputs, and bans survey begging.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Redline Parts | plan 160, actual 90 | Use | Both sides of the comparison are in the file |
| Lantern Inn | score 62 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Define the relationship metric they actually collect. Do not install a new score by fashion
2. Add inputs a team can move
3. Pair speed with quality
4. Name the owner of each input
5. Note how the metric is gamed, such as survey begging. Recommend against it

**Deliberately not done**
- A new vanity score with no inputs.
- Survey begging.
- No owner.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Rita Santos attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- A new vanity score with no inputs
- Survey begging
- No owner

## Related skills

- `north-star-metric`
- `ops-scorecard`
