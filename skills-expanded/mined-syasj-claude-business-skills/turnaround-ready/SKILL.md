---
name: turnaround-ready
description: "Check a turnaround checklist against the items the site says must be done before isolation. Use when the user mentions turnaround readiness, shutdown ready, outage checklist, TA ready, or asks for a readiness note. Oil and gas operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: oil-gas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'turnaround-ready' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Turnaround Readiness

Check a turnaround checklist against the items the site says must be done before isolation.

## When to use this skill

Use this skill when the user:

- turnaround readiness
- shutdown ready
- outage checklist
- TA ready

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational drafts only. Do not bypass isolation, lockout, permits, or reporting duties. Do not write instructions to conceal a release or to operate outside the site's limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Their checklist
- Items still open
- The start date
- The isolation owner

## Workflow


### 1. Step 1

List open items.
### 2. Step 2

A start date does not close an item.
### 3. Step 3

Isolation and lockout stay with the named owner.
### 4. Step 4

Do not tell anyone to skip a hold point.
### 5. Step 5

Separate materials from permits.
### 6. Step 6

Recommend a slip if a safety item is open.

## Output

Deliver a **readiness note**.

- Purpose of this readiness note, in two sentences.
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

The plant turnaround is on the board for Monday 22 September. Two items are open: a permit signature and the blind list. The isolation owner is Devon.

### Example data

```text
start on the board: Mon 22 Sep 2026
open: permit signature, blind list
closed: materials on site, scaffold tagged
isolation owner: Devon Hale
percent a slide showed: 90 percent
```

### Example outcome

**Readiness**
Monday does not start. Two items are open, and one of them is the blind list.

| Item | Status |
| --- | --- |
| Permit signature | open |
| Blind list | open |
| Materials | closed |
| Scaffold tag | closed |

The 90 percent slide does not close a safety item. Isolation stays with Devon. Nobody skips the blind list to hold the date.

## Anti-patterns

- A start with an open isolation item
- A skipped hold
- A percent complete with open safety items

## Related skills

- `isolation-work-plan`
- `hse-observation`
