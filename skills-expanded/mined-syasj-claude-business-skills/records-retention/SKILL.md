---
name: records-retention
description: "Draft a retention schedule from the record types they know they keep, with owners and legal questions marked. Use when the user mentions records retention, retention schedule, how long do we keep this, record series, or asks for a retention schedule draft. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'records-retention' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Records Retention Schedule

Draft a retention schedule from the record types they know they keep, with owners and legal questions marked.

## When to use this skill

Use this skill when the user:

- records retention
- retention schedule
- how long do we keep this
- record series

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Record types
- Where they live
- Business need they stated
- Legal holds they know about

## Workflow


### 1. Step 1

List record types they actually keep, not a generic encyclopedia.
### 2. Step 2

Record the business reason to keep each one.
### 3. Step 3

Mark the legal period as a question for counsel unless they supplied it. Do not invent a statutory period.
### 4. Step 4

Note systems so people can find and delete on purpose.
### 5. Step 5

Holds override deletion. Say that, and do not help delete held records.
### 6. Step 6

Name an owner for the schedule.

## Output

Deliver a **retention schedule draft**.

- Purpose of this retention schedule draft, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a retention schedule draft by 30 September 2026. A team wants a seven-year rule on everything because it sounds safe.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A team wants a seven-year rule on everything because it sounds safe.

Record types: one file, dated 14 September 2026. No earlier version attached for comparison
Where they live: Vendor Redline Parts, recorded 14 September 2026. No supporting file attached
Business need they stated: Vendor Redline Parts. Partly documented: the what is written down, the who is not
Legal holds they know about: Issue log item 18 and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Retention schedule draft**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the blanket rule, separates business need from legal questions, and protects holds.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Record types | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| Where they live | Vendor Redline Parts, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Business need they stated | Vendor Redline Parts. Partly documented: the what is written down, the who is not | Carried into the draft |
| Legal holds they know about | Issue log item 18 and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. List record types they actually keep, not a generic encyclopedia**

**2. Record the business reason to keep each one**

**3. Mark the legal period as a question for counsel unless they supplied it. Do not invent a statutory period**

**4. Note systems so people can find and delete on purpose**

**5. Holds override deletion. Say that, and do not help delete held records**

**Deliberately not done**
- Invented statutory periods.
- Deleting records under a known hold.
- A schedule of records they do not have.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented statutory periods
- Deleting records under a known hold
- A schedule of records they do not have

## Related skills

- `legal-hold-notice`
- `policy-writer`
