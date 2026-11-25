---
name: faceless-publish-calendar
description: "Calendar faceless episodes the operator can finish, with a source check before each publish date. Use when the user mentions faceless calendar, publishing schedule, content calendar faceless, upload plan, or asks for a publish calendar. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'faceless-publish-calendar' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Faceless Publish Calendar

Calendar faceless episodes the operator can finish, with a source check before each publish date.

## When to use this skill

Use this skill when the user:

- faceless calendar
- publishing schedule
- content calendar faceless
- upload plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Creator work must be original and honest. Do not copy another person's script, footage, voice, or caption. Do not invent metrics, fake engagement, or undisclosed sponsorships. Do not impersonate a real person. Prompt skills must not weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Episodes that are sourced
- Edit time
- Publish slots
- Episodes still missing rights

## Workflow


### 1. Step 1

Only dated episodes have cleared sources.
### 2. Step 2

Put the source check before the upload, not after a copyright strike.
### 3. Step 3

Match the number of slots to edit time.
### 4. Step 4

Leave a slot empty rather than upload an uncleared compile.
### 5. Step 5

Note titles that overclaim. Fix them before the date.
### 6. Step 6

Do not automate uploads of a folder the operator has not reviewed.

## Output

Deliver a **publish calendar**.

- Purpose of this publish calendar, in two sentences.
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

Maya wants a Sunday faceless video every week in October. She has receipts for two weeks. The other Sundays have no footage plan.

### Example data

```text
Sundays: 5, 12, 19, 26 Oct 2026
sourced: week of 14 Sep, week of 21 Sep
not sourced: the October weeks
her rule: no episode without receipts in hand on the Friday before
```

### Example outcome

**Calendar**
Do not promise four October Sundays.

| Publish | Source in hand on the Friday before | Status |
| --- | --- | --- |
| 5 Oct | not yet | hold |
| 12 Oct | not yet | hold |
| 19 Oct | not yet | hold |
| 26 Oct | not yet | hold |

The two September weeks can publish when she films them. They are not an October promise.
A Sunday with no receipts on Friday stays empty. She does not fill it with a downloaded clip.

## Anti-patterns

- An automated upload of unreviewed files
- A full calendar of uncleared compiles
- Titles that overclaim

## Related skills

- `faceless-source-check`
- `content-creator-week`
