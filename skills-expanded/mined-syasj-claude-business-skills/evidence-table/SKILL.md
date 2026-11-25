---
name: evidence-table
description: "Build an evidence table from sources the user supplied, with columns that match the question. Use when the user mentions evidence table, extraction table, study table, literature matrix, or asks for a evidence table. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'evidence-table' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Evidence Table

Build an evidence table from sources the user supplied, with columns that match the question.

## When to use this skill

Use this skill when the user:

- evidence table
- extraction table
- study table
- literature matrix

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The question
- The sources they have
- The fields to extract
- Inclusion status

## Workflow


### 1. Columns follow the question

population, method, finding, limit.
### 2. Step 2

Extract only what the source they provided actually says.
### 3. Step 3

Mark a field unknown rather than filling it from memory.
### 4. Step 4

Keep excluded sources in a short log with the reason.
### 5. Step 5

Do not add a source you cannot identify.
### 6. Step 6

Note if the table is too thin for a conclusion.

## Output

Deliver a **evidence table**.

- Purpose of this evidence table, in two sentences.
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

Dr. Nia Okonkwo, research lead at Riverbend College in Lethbridge, needs an evidence table by 30 September 2026. A table has effect sizes the user never found in the papers.

### Example data

```text
From: Dr. Nia Okonkwo, research lead
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A table has effect sizes the user never found in the papers.

The question: A table has effect sizes the user never found in the papers
The sources they have: note from Dr. Nia Okonkwo, 14 September 2026. No outside report
The fields to extract: Interview set A, recorded 14 September 2026. No supporting file attached
Inclusion status: Interview set A. Stated in the ask, not documented anywhere else
```

### Example outcome

**Evidence table**
To: Dr. Nia Okonkwo, research lead, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A table with those cells marked unknown and a warning against a numeric conclusion.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question | A table has effect sizes the user never found in the papers | Needs confirmation |
| The sources they have | note from Dr. Nia Okonkwo, 14 September 2026. No outside report | Carried into the draft |
| The fields to extract | Interview set A, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Inclusion status | Interview set A. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Columns follow the question**  
population, method, finding, limit.

**2. Extract only what the source they provided actually says**

**3. Mark a field unknown rather than filling it from memory**

**4. Keep excluded sources in a short log with the reason**

**5. Do not add a source you cannot identify**

**Deliberately not done**
- Cells filled from memory.
- Ghost sources.
- A conclusion the table does not support.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Nia Okonkwo by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Cells filled from memory
- Ghost sources
- A conclusion the table does not support

## Related skills

- `literature-review-plan`
- `citation-hygiene`
