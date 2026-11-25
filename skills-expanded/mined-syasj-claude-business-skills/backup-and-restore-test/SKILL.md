---
name: backup-and-restore-test
description: "Plan a restore test that proves a backup can be recovered, not merely that a backup job ran. Use when the user mentions backup test, restore drill, can we recover, backup review, or asks for a restore test plan. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'backup-and-restore-test' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Backup and Restore Test

Plan a restore test that proves a backup can be recovered, not merely that a backup job ran.

## When to use this skill

Use this skill when the user:

- backup test
- restore drill
- can we recover
- backup review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Defensive use only. Do not write exploits, payloads, bypasses, malware, or intrusion steps. Describe controls, ownership, detection, and safe verification.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What must be recoverable
- The backup they believe exists
- The recovery time they need
- Who may run the test

## Workflow


### 1. Step 1

Define the asset and the acceptable loss of data and time, in their words.
### 2. Step 2

A successful backup job is not evidence of a restorable backup. Plan an actual restore into a safe environment.
### 3. Step 3

The test environment must not overwrite production. Say that explicitly.
### 4. Step 4

Record what was restored, how long it took, and what failed.
### 5. Step 5

Name the owner who fixes a failed restore.
### 6. Step 6

Do not ask for backup credentials to be pasted into the plan.

## Output

Deliver a **restore test plan**.

- Purpose of this restore test plan, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a restore test plan by 30 September 2026. The team says backups are fine because the nightly job is green, and nobody has restored one.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The team says backups are fine because the nightly job is green, and nobody has restored one.

What must be recoverable: Phishing report 4412, last reviewed 14 September 2026. No owner named since
The backup they believe exists: Access review Q3, recorded 14 September 2026. No supporting file attached
The recovery time they need: five working days, due 30 September 2026
Who may run the test: Aisha Rahman, engineering lead
```

### Example outcome

**Restore test plan**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A restore test into a non-production target, with a recorded time and a ban on production overwrite.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What must be recoverable | Phishing report 4412, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| The backup they believe exists | Access review Q3, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The recovery time they need | five working days, due 30 September 2026 | Carried into the draft |
| Who may run the test | Aisha Rahman, engineering lead | Needs confirmation |

**How this draft was built**

**1. Define the asset and the acceptable loss of data and time, in their words**

**2. A successful backup job is not evidence of a restorable backup. Plan an actual restore into a safe environment**

**3. The test environment must not overwrite production. Say that explicitly**

**4. Record what was restored, how long it took, and what failed**

**5. Name the owner who fixes a failed restore**

**Deliberately not done**
- Equating a green backup job with recoverability.
- A test that can overwrite production.
- Credentials in the plan.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Equating a green backup job with recoverability
- A test that can overwrite production
- Credentials in the plan

## Related skills

- `business-continuity`
- `disaster-recovery-brief`
