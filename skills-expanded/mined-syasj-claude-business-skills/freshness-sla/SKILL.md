---
name: freshness-sla
description: "Set a freshness promise the job can meet, from the finish times the user has. Use when the user mentions freshness SLA, data SLA, when is the table ready, late data, or asks for a freshness note. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'freshness-sla' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Freshness SLA

Set a freshness promise the job can meet, from the finish times the user has.

## When to use this skill

Use this skill when the user:

- freshness SLA
- data SLA
- when is the table ready
- late data

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent numbers. If a source file is missing, say so. Distinguish observation from inference. Do not re-identify private data to make a point.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The last ten finish times if they have them
- The time the consumer needs
- The job owner
- What happens if it is late

## Workflow


### 1. Step 1

Use their finish times. If they have fewer than five, say the promise is thin.
### 2. Step 2

Set the promise after the slow runs, not at the average.
### 3. Step 3

Name the consumer clock.
### 4. Step 4

Say who is called when it misses.
### 5. Step 5

Do not promise a time the job has already missed twice.
### 6. Step 6

Write the exception path.

## Output

Deliver a **freshness note**.

- Purpose of this freshness note, in two sentences.
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

Jonah wants the dashboard to say data is ready at 06:00. Noah listed the last ten weekday finish times. Eight are after 09:00. Two failed.

### Example data

```text
job: fct_active_accounts
finish times: 09:12, 09:20, 09:41, failed, 09:18, 09:33, 09:15, failed, 09:28, 09:22
consumer need: 06:00 America/Edmonton
owner: Noah Berger
if late: dashboard should show the prior day, Jonah agrees
```

### Example outcome

**Freshness note**
Do not promise 06:00. Eight finished runs landed between 09:12 and 09:41. Two failed.

Promise that matches the file: ready by 10:00, or show the prior day.
Call if it misses 10:00: Noah first, Jonah if the prior day is also missing.
The average is not the promise. The slow run is.
Next: Jonah changes the dashboard label. Noah does not sign 06:00.

## Anti-patterns

- A 6 a.m. promise on a 9 a.m. job
- No owner for a miss
- An average used as a guarantee

## Related skills

- `data-contract`
- `pipeline-incident`
