---
name: data-lineage
description: "Trace a metric to the source tables the user can name, and stop where the trail stops. Use when the user mentions data lineage, where does this number come from, metric source, column lineage, or asks for a lineage note. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'data-lineage' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Data Lineage

Trace a metric to the source tables the user can name, and stop where the trail stops.

## When to use this skill

Use this skill when the user:

- data lineage
- where does this number come from
- metric source
- column lineage

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

- The metric
- The tables they know
- The transform they can point to
- The gap

## Workflow


### 1. Step 1

Start at the metric definition they use.
### 2. Step 2

Walk only to tables they named.
### 3. Step 3

Mark the first hop you cannot show.
### 4. Step 4

Do not draw a source you inferred from a column name.
### 5. Step 5

Note if two jobs write the same column.
### 6. Step 6

Give the owner one place to look next.

## Output

Deliver a **lineage note**.

- Purpose of this lineage note, in two sentences.
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

Jonah asked where active_accounts comes from. Noah can point at a dbt model name and then the trail stops. The slide says 'the warehouse'.

### Example data

```text
metric: active_accounts, defined as workspaces with a login on that day
known hop: model fct_active_accounts, owner Noah
source tables named: none
second writer: unknown
slide text: "comes from the warehouse"
```

### Example outcome

**Lineage note**
active_accounts is the count of workspaces with a login that day, per Jonah's definition.
Known hop: fct_active_accounts, owner Noah Berger.
Next hop: not in the file. Do not draw a source table from the column name.
The slide line 'the warehouse' is not a source.
Open: the table under the model, and whether any other job writes active_flag.
Next: Noah names that table before this metric is used in a board pack.

## Anti-patterns

- A full map drawn from guesses
- Ignoring a second writer
- A lineage slide with no table names

## Related skills

- `metric-definition`
- `data-dictionary`
