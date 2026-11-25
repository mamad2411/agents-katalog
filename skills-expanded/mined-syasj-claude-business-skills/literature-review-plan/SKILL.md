---
name: literature-review-plan
description: "Plan a literature review around a question, with sources the user can actually obtain and no fabricated papers. Use when the user mentions literature review, review plan, evidence review, what should I read, or asks for a review plan. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'literature-review-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Literature Review Plan

Plan a literature review around a question, with sources the user can actually obtain and no fabricated papers.

## When to use this skill

Use this skill when the user:

- literature review
- review plan
- evidence review
- what should I read

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
- Inclusion rules
- Databases or shelves they can access
- Time

## Workflow


### 1. Step 1

Write the question so a paper can be in or out.
### 2. Step 2

Define inclusion and exclusion.
### 3. Step 3

Plan a search from sources they can open. Do not pretend you searched a database you did not search.
### 4. Step 4

Keep a log of queries they run.
### 5. Step 5

A paper you cannot identify precisely is not cited. Say it is missing.
### 6. Step 6

Synthesize by theme after screening, not before.

## Output

Deliver a **review plan**.

- Purpose of this review plan, in two sentences.
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

Dr. Nia Okonkwo, research lead at Riverbend College in Lethbridge, needs a review plan by 30 September 2026. A draft cites three articles with confident titles the user cannot find.

### Example data

```text
From: Dr. Nia Okonkwo, research lead
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A draft cites three articles with confident titles the user cannot find.

The question: A draft cites three articles with confident titles the user cannot find
Inclusion rules: their one-page rule dated 2 Mar 2026. No exception log since
Databases or shelves they can access: Interview set A. Partly documented: the what is written down, the who is not
Time: five working days, due 30 September 2026
```

### Example outcome

**Review plan**
To: Dr. Nia Okonkwo, research lead, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes unverified citations and sets an inclusion rule before more reading.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question | A draft cites three articles with confident titles the user cannot find | Needs confirmation |
| Inclusion rules | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Databases or shelves they can access | Interview set A. Partly documented: the what is written down, the who is not | Carried into the draft |
| Time | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Write the question so a paper can be in or out**

**2. Define inclusion and exclusion**

**3. Plan a search from sources they can open. Do not pretend you searched a database you did not search**

**4. Keep a log of queries they run**

**5. A paper you cannot identify precisely is not cited. Say it is missing**

**Deliberately not done**
- Fabricated citations.
- A review with no inclusion rule.
- Claiming a search you did not run.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Nia Okonkwo by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Fabricated citations
- A review with no inclusion rule
- Claiming a search you did not run

## Related skills

- `citation-hygiene`
- `evidence-table`
