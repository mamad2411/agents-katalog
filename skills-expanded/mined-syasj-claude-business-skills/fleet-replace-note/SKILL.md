---
name: fleet-replace-note
description: "Compare fleet units the user listed on age, cost, and downtime, without a forced replacement. Use when the user mentions fleet replacement, which vans to replace, unit replacement, fleet plan, or asks for a replacement note. Automotive skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: automotive
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'fleet-replace-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Fleet Replacement Note

Compare fleet units the user listed on age, cost, and downtime, without a forced replacement.

## When to use this skill

Use this skill when the user:

- fleet replacement
- which vans to replace
- unit replacement
- fleet plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not a repair procedure for safety-critical systems and not a recall determination. Do not invent defect rates or tell anyone to disable a safety feature.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The units
- Age or kilometres they have
- Downtime
- The budget they named

## Workflow


### 1. Step 1

Rank only on the figures they gave.
### 2. Step 2

A unit with no downtime stays unranked on that column.
### 3. Step 3

Do not invent a residual value.
### 4. Step 4

Stay inside the budget count they named.
### 5. Step 5

Separate a safety hold from a cost preference.
### 6. Step 6

Name who approves the order.

## Output

Deliver a **replacement note**.

- Purpose of this replacement note, in two sentences.
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

Harbor Goods can replace two vans this year. Three are old. Van 4 is on a safety hold for brakes. No residual values are in the file.

### Example data

```text
budget count: 2
van 2: 11 years, downtime 6 days this quarter
van 4: 9 years, safety hold, brakes, downtime 14 days
van 7: 12 years, downtime not recorded
residual values: none in the file
approver: Diane Cho
```

### Example outcome

**Replacement note**
First: van 4. It is on a safety hold. Budget optics do not delay that.
Second: van 2, because downtime is in the file: 6 days.
Van 7: unranked on downtime. The cell is empty. It is the one that stays if only two can be ordered.
No residual is in this note. None was supplied.
Approver: Diane. This is not a purchase order.

## Anti-patterns

- An invented residual
- A safety hold delayed for budget optics
- A full fleet replacement they cannot fund

## Related skills

- `dealer-morning-review`
- `parts-backorder-note`
