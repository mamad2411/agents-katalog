---
name: data-contract
description: "Write the columns, grain, freshness, and owner a producer and a consumer can both use. Use when the user mentions data contract, schema agreement, producer consumer contract, table contract, or asks for a data contract. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'data-contract' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Data Contract

Write the columns, grain, freshness, and owner a producer and a consumer can both use.

## When to use this skill

Use this skill when the user:

- data contract
- schema agreement
- producer consumer contract
- table contract

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

- The table or file
- The grain
- The columns that must not be null
- The freshness the consumer needs

## Workflow


### 1. Step 1

Name the grain in one sentence.
### 2. Step 2

List required columns and which may be null.
### 3. Step 3

Write the freshness as a clock time the producer can hit.
### 4. Step 4

Name both owners.
### 5. Step 5

Say what breaks the contract.
### 6. Step 6

Do not add columns nobody produces.

## Output

Deliver a **data contract**.

- Purpose of this data contract, in two sentences.
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

Product wants active_accounts on the dashboard by 06:00. Noah's job finished at 09:30 on eight of the last ten weekdays. They need a contract both sides can sign.

### Example data

```text
table: analytics.active_accounts
grain: one row per workspace per day
required columns: workspace_id, day, active_flag
nullable: none of those three
producer: Noah Berger
consumer: Jonah Park
job finish, last 10 weekdays: 09:12 to 09:41, two runs failed
consumer ask: 06:00 local
```

### Example outcome

**Contract — analytics.active_accounts**
Grain: one row per workspace per day.
Required: workspace_id, day, active_flag. None null.
Freshness in this contract: ready by 10:00 America/Edmonton, or the dashboard shows the prior day.
Not in this contract: 06:00. The job does not finish then.
Breaks the contract: a null workspace_id, a day with two rows, or a finish after 10:00.
Owners: Noah produces. Jonah accepts the 10:00 clock or funds a faster job.
Next: both initial this by 30 September 2026. Until then the dashboard must not say 'live at 6'.

## Anti-patterns

- A contract with no grain
- Freshness the producer never agreed
- Hidden personal columns

## Related skills

- `freshness-sla`
- `metric-definition`
