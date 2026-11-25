---
name: disaster-recovery-brief
description: "Brief a disaster recovery choice for one system, including the recovery point they are actually buying. Use when the user mentions disaster recovery, RPO RTO, DR brief, recovery objective, or asks for a disaster recovery brief. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'disaster-recovery-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Disaster Recovery Brief

Brief a disaster recovery choice for one system, including the recovery point they are actually buying.

## When to use this skill

Use this skill when the user:

- disaster recovery
- RPO RTO
- DR brief
- recovery objective

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

- The system
- The recovery point and time they need
- What they have tested
- Dependencies

## Workflow


### 1. Step 1

Define the business process the system serves.
### 2. Step 2

Record the recovery point and time they want, labeled as a want until a test proves it.
### 3. Step 3

List dependencies. A restored app with no identity provider is not recovered.
### 4. Step 4

Note the last test and its result. No test, no claim of readiness.
### 5. Step 5

Identify the gap between the want and the evidenced capability.
### 6. Step 6

Hand the investment decision to finance with the gap visible. Do not invent a vendor price.

## Output

Deliver a **disaster recovery brief**.

- Purpose of this disaster recovery brief, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a disaster recovery brief by 30 September 2026. A team claims a four-hour recovery and has never failed over the identity provider.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A team claims a four-hour recovery and has never failed over the identity provider.

The system: the one named in the ask. Version and owner not recorded
The recovery point and time they need: five working days, due 30 September 2026
What they have tested: A team claims a four-hour recovery and has never failed over the identity provider
Dependencies: SOP 118 receiving and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Disaster recovery brief**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Downgrades the claim to untested and names the identity dependency.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The system | the one named in the ask. Version and owner not recorded | Needs confirmation |
| The recovery point and time they need | five working days, due 30 September 2026 | Carried into the draft |
| What they have tested | A team claims a four-hour recovery and has never failed over the identity provider | Carried into the draft |
| Dependencies | SOP 118 receiving and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Define the business process the system serves**

**2. Record the recovery point and time they want, labeled as a want until a test proves it**

**3. List dependencies. A restored app with no identity provider is not recovered**

**4. Note the last test and its result. No test, no claim of readiness**

**5. Identify the gap between the want and the evidenced capability**

**Deliberately not done**
- Claiming a recovery time that was never tested.
- Ignoring a dependency.
- An invented price.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Claiming a recovery time that was never tested
- Ignoring a dependency
- An invented price

## Related skills

- `business-continuity`
- `backup-and-restore-test`
