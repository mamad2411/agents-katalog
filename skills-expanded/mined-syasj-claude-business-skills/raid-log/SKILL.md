---
name: raid-log
description: "Maintain a RAID log that separates risks, assumptions, issues, and dependencies, each with an owner. Use when the user mentions RAID log, risk issue dependency, project RAID, assumptions log, or asks for a RAID log. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'raid-log' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# RAID Log

Maintain a RAID log that separates risks, assumptions, issues, and dependencies, each with an owner.

## When to use this skill

Use this skill when the user:

- RAID log
- risk issue dependency
- project RAID
- assumptions log

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

- Current worries
- Owners
- Dates
- Which items are already issues

## Workflow


### 1. Classify each item

risk, assumption, issue, or dependency. An issue is already happening.
### 2. Step 2

Give each item one owner and a next date.
### 3. Step 3

Write the impact in delivery terms.
### 4. Step 4

Close items that are no longer true rather than letting the log rot.
### 5. Step 5

Escalate dependencies the team cannot move.
### 6. Step 6

Do not hide an issue inside a risk to keep a status green.

## Output

Deliver a **RAID log**.

- Purpose of this RAID log, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a RAID log by 30 September 2026. A dependency has already missed its date and is still labeled a risk.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A dependency has already missed its date and is still labeled a risk.

Current worries: RAID item 12 and one other, both unconfirmed as of 14 September 2026
Owners: Owen Blake, delivery lead
Dates: 30 September 2026
Which items are already issues: Change request 118. Stated in the ask, not documented anywhere else
```

### Example outcome

**Raid log**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Reclassifies it as an issue, names the owner, and shows the delivery impact.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Current worries | RAID item 12 and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |
| Owners | Owen Blake, delivery lead | Carried into the draft |
| Dates | 30 September 2026 | Carried into the draft |
| Which items are already issues | Change request 118. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Classify each item**  
risk, assumption, issue, or dependency. An issue is already happening.

**2. Give each item one owner and a next date**

**3. Write the impact in delivery terms**

**4. Close items that are no longer true rather than letting the log rot**

**5. Escalate dependencies the team cannot move**

**Deliberately not done**
- A log with no owners.
- An issue disguised as a risk.
- A log nobody closes.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A log with no owners
- An issue disguised as a risk
- A log nobody closes

## Related skills

- `risk-register`
- `status-report`

## Optional local tool

A stdlib script is bundled at `scripts/raid_lint.py`. It checks a CSV of `type,item,owner,date,status` for missing owners and dates. It does not update a project system. Example: `python3 scripts/raid_lint.py raid.csv --json`.
