---
name: gas-nomination
description: "Check a nomination against the confirmed volume and the cycle time the user states. Use when the user mentions gas nomination, nom cycle, pipeline nomination, confirm the nom, or asks for a nomination check. Oil and gas operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: oil-gas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'gas-nomination' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Gas Nomination

Check a nomination against the confirmed volume and the cycle time the user states.

## When to use this skill

Use this skill when the user:

- gas nomination
- nom cycle
- pipeline nomination
- confirm the nom

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational drafts only. Do not bypass isolation, lockout, permits, or reporting duties. Do not write instructions to conceal a release or to operate outside the site's limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The cycle deadline
- The volume they will nominate
- The confirmed production
- Who submits

## Workflow


### 1. Step 1

Compare the nom to the confirmed volume.
### 2. Step 2

A wish volume is labeled a wish.
### 3. Step 3

Record the cycle deadline in their time zone.
### 4. Step 4

Do not submit a nom after the deadline and call it on time.
### 5. Step 5

Name the submitter.
### 6. Step 6

Flag a gap over their threshold.

## Output

Deliver a **nomination check**.

- Purpose of this nomination check, in two sentences.
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

The cycle closes at 11:00 America/Edmonton. Confirmed production for the pad is 3.6 mmcf. A draft nomination still says 4.2. It is 10:40.

### Example data

```text
cycle deadline: 11:00 America/Edmonton, 16 Sep 2026
now: 10:40
confirmed: 3.6 mmcf
draft nom: 4.2 mmcf
submitter: Devon Hale
threshold: 0.3
```

### Example outcome

**Nomination check**
Do not submit 4.2. Confirmed is 3.6. The gap is 0.6, over his threshold.
4.2 is a wish from yesterday's nom. It is not confirmed production.
There is time before 11:00 to submit 3.6. A nom after 11:00 is late. Do not call it on time.
Submitter: Devon.

## Anti-patterns

- A late nom called on time
- A wish volume submitted as confirmed
- No submitter

## Related skills

- `production-variance`
- `gas-balance`
