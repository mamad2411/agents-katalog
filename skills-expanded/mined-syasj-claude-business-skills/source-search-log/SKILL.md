---
name: source-search-log
description: "Log the searches and the dates so a review can see what was looked for. Use when the user mentions search log, literature search, what did we search, database log, or asks for a search log. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'source-search-log' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Search Log

Log the searches and the dates so a review can see what was looked for.

## When to use this skill

Use this skill when the user:

- search log
- literature search
- what did we search
- database log

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

- The databases
- The query strings
- The dates
- What was not searched

## Workflow


### 1. Step 1

Record each database, query, and date.
### 2. Step 2

Record zero results as zero.
### 3. Step 3

Do not add databases they did not open.
### 4. Step 4

Note filters.
### 5. Step 5

Say who ran it.
### 6. Step 6

A log is not a review.

## Output

Deliver a **search log**.

- Purpose of this search log, in two sentences.
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

A methods draft says Nia searched PubMed, Scopus, and Web of Science on 2 September. Her notebook shows PubMed and Scopus only. Scopus returned zero hits. Web of Science is not in the notebook.

### Example data

```text
who: Dr. Nia Okonkwo
date in the draft: 2 Sep 2026
PubMed: query "small shop hiring interview", 42 hits, notebook page 3
Scopus: same query, 0 hits, notebook page 3
Web of Science: not in the notebook
filters: English, 2018-2026, written on page 3
```

### Example outcome

**Search log**
| Database | Date | Query | Hits |
| --- | --- | --- | --- |
| PubMed | 2 Sep 2026 | small shop hiring interview | 42 |
| Scopus | 2 Sep 2026 | small shop hiring interview | 0 |

Filters: English, 2018-2026.
Web of Science comes out of the methods draft. It was not opened.
Zero stays in the log. A log is not a review.

## Anti-patterns

- A database listed that was not opened
- A dropped zero
- No date

## Related skills

- `literature-review-plan`
- `citation-hygiene`
