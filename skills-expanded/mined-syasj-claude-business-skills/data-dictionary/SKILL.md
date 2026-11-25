---
name: data-dictionary
description: "Write a data dictionary entry that tells an analyst what a field means, what it does not mean, and who owns it. Use when the user mentions data dictionary, document this field, column definition, semantic layer entry, or asks for a data dictionary entry. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'data-dictionary' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Data Dictionary

Write a data dictionary entry that tells an analyst what a field means, what it does not mean, and who owns it.

## When to use this skill

Use this skill when the user:

- data dictionary
- document this field
- column definition
- semantic layer entry

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

- The field and table
- The business meaning
- Known null or sentinel values
- The owner

## Workflow


### 1. Step 1

Name the grain of the table before defining the field.
### 2. Step 2

Write the business meaning in plain language, plus a false friend it is often confused with.
### 3. Step 3

Document nulls, sentinels, and units. Do not guess a unit.
### 4. Step 4

State the source system if they know it.
### 5. Step 5

Name an owner. An unowned field will rot.
### 6. Step 6

Add an example value only if they supplied one. Do not invent customer data.

## Output

Deliver a **data dictionary entry**.

- Purpose of this data dictionary entry, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a data dictionary entry by 30 September 2026. A field called status has values 1, 2, and 9, and nobody agrees what 9 means.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A field called status has values 1, 2, and 9, and nobody agrees what 9 means.

The field and table: orders_daily, recorded 14 September 2026. No supporting file attached
The business meaning: orders_daily, recorded 14 September 2026. No supporting file attached
Known null or sentinel values: customers. Stated in the ask, not documented anywhere else
The owner: Noah Berger, data lead
```

### Example outcome

**Data dictionary entry**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Records the known values, marks 9 as unresolved, and names the owner who must decide.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The field and table | orders_daily, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The business meaning | orders_daily, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Known null or sentinel values | customers. Stated in the ask, not documented anywhere else | Carried into the draft |
| The owner | Noah Berger, data lead | Needs confirmation |

**How this draft was built**

**1. Name the grain of the table before defining the field**

**2. Write the business meaning in plain language, plus a false friend it is often confused with**

**3. Document nulls, sentinels, and units. Do not guess a unit**

**4. State the source system if they know it**

**5. Name an owner. An unowned field will rot**

**Deliberately not done**
- A dictionary that copies the column name as the definition.
- Invented example customers.
- No owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A dictionary that copies the column name as the definition
- Invented example customers
- No owner

## Related skills

- `metric-definition`
- `event-tracking-spec`
