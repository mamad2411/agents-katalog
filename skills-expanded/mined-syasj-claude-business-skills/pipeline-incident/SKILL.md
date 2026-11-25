---
name: pipeline-incident
description: "Write a pipeline failure from the log lines the user has, with the hold and the rerun owner. Use when the user mentions pipeline failed, data job down, ETL incident, broken load, or asks for a pipeline note. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pipeline-incident' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Pipeline Incident

Write a pipeline failure from the log lines the user has, with the hold and the rerun owner.

## When to use this skill

Use this skill when the user:

- pipeline failed
- data job down
- ETL incident
- broken load

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

- The job name
- The error line they copied
- What is stale
- Who reruns it

## Workflow


### 1. Step 1

Quote the error they pasted. Do not invent a stack.
### 2. Step 2

Say which table is stale and as of when.
### 3. State the hold

who should not use the table.
### 4. Step 4

Name the rerun owner.
### 5. Step 5

Separate a late file from a bad transform if the log shows which.
### 6. Step 6

Do not include credentials from the log.

## Output

Deliver a **pipeline note**.

- Purpose of this pipeline note, in two sentences.
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

orders_daily failed this morning. Noah pasted one error line. The sales dashboard refreshed anyway and still shows yesterday's subtitle as today.

### Example data

```text
job: orders_daily
error line pasted: 15 Sep 2026 05:12 ERROR missing file s3://harbor/orders/2026-09-14.csv
table: analytics.orders_daily
last good load: 14 Sep 2026 05:40, covering 13 Sep
dashboard: refreshed 15 Sep 06:05, subtitle says 15 Sep
rerun owner: Noah Berger
credentials in the paste: none
```

### Example outcome

**Pipeline note**
orders_daily is stale. Last good load covers 13 September, loaded 14 September 05:40.
Error on file: missing 2026-09-14.csv at 05:12. No other cause is in the paste.
Hold: do not use the dashboard figure labeled 15 September. The refresh did not bring new orders.
Rerun: Noah, after the file is actually there. Do not rerun against a missing path and call it fixed.
Next: Jonah changes the subtitle to the last good day before the 09:00 sales meeting.

## Anti-patterns

- A guessed root cause
- A silent rerun
- Credentials copied into the note

## Related skills

- `data-contract`
- `incident-postmortem`
