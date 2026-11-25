---
name: source-log-news
description: "Log who said what, when, and whether it was on the record. Use when the user mentions source log, who said this, on the record, news sources, or asks for a source log. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'source-log-news' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Source Log

Log who said what, when, and whether it was on the record.

## When to use this skill

Use this skill when the user:

- source log
- who said this
- on the record
- news sources

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

- The notes
- Whether each person was on the record
- Documents
- What was not confirmed

## Workflow


### 1. Step 1

One row per source.
### 2. Step 2

Mark on the record, background, or not for use, as the reporter noted.
### 3. Step 3

A quote with no name and no note does not go in the story.
### 4. Step 4

Separate a document from a recollection.
### 5. Step 5

Do not upgrade background to on the record.
### 6. Step 6

Record who did not call back.

## Output

Deliver a **source log**.

- Purpose of this source log, in two sentences.
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

Jonah's notebook has a company statement and a sentence from a person who said they would not be named and would not be quoted.

### Example data

```text
source 1: Prairie Line statement, 15 Sep 2026, on the record as a document, turnaround 22 Sep, ten days
source 2: person at the gate, 15 Sep 16:40, said "do not quote me and do not name me"
callback: spokesperson, left message 15 Sep 17:10, no reply
document not in hand: any staffing list
```

### Example outcome

**Source log**
| Source | Status | Use |
| --- | --- | --- |
| 15 Sep statement | document | dates only |
| Gate conversation 16:40 | not for use | out |
| Spokesperson | no reply | do not write 'declined' |

The unnamed sentence does not go in the story.
No staffing list, so no staffing claim.

## Anti-patterns

- A quote with no source
- Background used as a named quote
- A document they do not have

## Related skills

- `news-assignment`
- `citation-hygiene`
