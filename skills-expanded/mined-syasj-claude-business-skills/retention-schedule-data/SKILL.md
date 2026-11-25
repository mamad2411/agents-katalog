---
name: retention-schedule-data
description: "Draft a retention note from the policy the user already has, not from a guessed law. Use when the user mentions data retention, how long do we keep rows, retention schedule, delete old data, or asks for a retention note. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'retention-schedule-data' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Data Retention Schedule

Draft a retention note from the policy the user already has, not from a guessed law.

## When to use this skill

Use this skill when the user:

- data retention
- how long do we keep rows
- retention schedule
- delete old data

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

- The datasets
- The policy or contract clause they have
- What they use the rows for
- Who approves a delete

## Workflow


### 1. Step 1

List each dataset and the clause they cited.
### 2. Step 2

If they have no clause, say the period is unset.
### 3. Step 3

Do not invent a statute.
### 4. Step 4

Separate a backup from the live table.
### 5. Step 5

Name who may approve a delete.
### 6. Step 6

Flag personal columns they pointed out.

## Output

Deliver a **retention note**.

- Purpose of this retention note, in two sentences.
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

A draft schedule says delete support tickets after 90 days because a blog recommended it. Fieldnote's customer contract in the folder does not mention ticket retention.

### Example data

```text
dataset: support.tickets
columns called out: email, home address on 6 of 14 sample rows
clause in the folder: customer contract 2026, no retention sentence
blog rule in the draft: 90 days
delete approver in their policy: privacy lead, role vacant
backups: nightly, kept 35 days, per Noah's note
```

### Example outcome

**Retention note**
support.tickets: period unset. The contract in the folder has no clause. The 90-day blog line is removed.
Backups: 35 days, from Noah's note. A live-table delete would not clear those until they age out.
Personal columns in the sample: email, home address. That is a flag, not a delete order.
Approver: privacy lead. The role is vacant, so nobody can approve a delete from this note.
Next: counsel or the contract owner writes the period. This note does not invent one.

## Anti-patterns

- A seven-year rule copied from memory
- Deleting without an owner
- Ignoring backups

## Related skills

- `records-retention`
- `ai-data-note`
