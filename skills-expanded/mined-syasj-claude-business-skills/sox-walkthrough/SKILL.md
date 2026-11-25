---
name: sox-walkthrough
description: "Prepare a walkthrough of a financial control so the performer can show what they actually do. Use when the user mentions SOX walkthrough, control walkthrough prep, audit walkthrough, ICFR prep, or asks for a SOX walkthrough prep. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sox-walkthrough' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SOX Walkthrough Prep

Prepare a walkthrough of a financial control so the performer can show what they actually do.

## When to use this skill

Use this skill when the user:

- SOX walkthrough
- control walkthrough prep
- audit walkthrough
- ICFR prep

## When not to use this skill

- Misleading an auditor

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

- The control description
- The performer
- The evidence
- The period

## Workflow


### 1. Step 1

Restate the risk and the control in plain language.
### 2. Step 2

Ask the performer to walk a real transaction, not a theoretical one.
### 3. Step 3

Match the walk to the control description. Differences are findings, not things to hide.
### 4. Step 4

Identify missing evidence before the auditor does, and say so to management.
### 5. Step 5

Do not coach anyone to misrepresent the control.
### 6. Step 6

Note samples you did not test. A prep is not a test of operating effectiveness.

## Output

Deliver a **SOX walkthrough prep**.

- Purpose of this SOX walkthrough prep, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a SOX walkthrough prep by 30 September 2026. A manager wants the performer to describe a review that does not happen.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants the performer to describe a review that does not happen.

The control description: their one-page rule dated 2 Mar 2026. No exception log since
The performer: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The evidence: one PDF, 2 pages, dated 14 September 2026
The period: month ending 14 September 2026
```

### Example outcome

**Sox walkthrough prep**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the false story and writes the gap for management.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The control description | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |
| The performer | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The period | month ending 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Restate the risk and the control in plain language**

**2. Ask the performer to walk a real transaction, not a theoretical one**

**3. Match the walk to the control description. Differences are findings, not things to hide**

**4. Identify missing evidence before the auditor does, and say so to management**

**5. Do not coach anyone to misrepresent the control**

**Deliberately not done**
- Coaching a false story.
- Hiding a gap.
- Claiming effectiveness from a prep chat.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Coaching a false story
- Hiding a gap
- Claiming effectiveness from a prep chat

## Related skills

- `control-design`
- `audit-response`
