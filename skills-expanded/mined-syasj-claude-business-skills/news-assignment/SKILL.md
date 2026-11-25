---
name: news-assignment
description: "Assign a story with the question, the sources already in hand, and what is not known. Use when the user mentions news assignment, story brief, assign a reporter, news budget item, or asks for a assignment. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'news-assignment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# News Assignment

Assign a story with the question, the sources already in hand, and what is not known.

## When to use this skill

Use this skill when the user:

- news assignment
- story brief
- assign a reporter
- news budget item

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate quotes, sources, or images. Label opinion. Do not draft impersonation or defamation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The question
- Sources in hand
- The deadline
- What must not be implied

## Workflow


### 1. Step 1

Write the question, not the conclusion.
### 2. Step 2

List sources they have.
### 3. Step 3

Mark what is unknown.
### 4. Step 4

Set a deadline that matches the sources.
### 5. Step 5

Say what the story will not claim if a source is missing.
### 6. Step 6

Do not assign a version that needs a quote they do not have.

## Output

Deliver a **assignment**.

- Purpose of this assignment, in two sentences.
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

The desk wants a Friday story that Prairie Line 'cut safety' at a plant. The only document is a company statement that a turnaround starts Monday 22 September and lasts ten days.

### Example data

```text
question the desk wrote: did the plant cut safety staff
document: company statement, 15 Sep 2026, turnaround starts 22 Sep, ten days, no staffing figures
other sources: none
deadline asked: Friday 19 Sep 17:00
must not imply: a safety verdict
reporter: Jonah Ellis
```

### Example outcome

**Assignment**
Question: what dates did the company state for the turnaround, and what did the statement not say?
Source: the 15 September statement only.
Not assigned: a safety-staff verdict. There is no figure and no worker on the record.
Deadline: 19 September only for a story that stays inside the statement.
If a second source arrives, this assignment is rewritten. It is not expanded in the draft.

## Anti-patterns

- A conclusion assigned as the story
- A deadline with no source
- An implied wrongdoing

## Related skills

- `source-log-news`
- `editorial-brief`
