---
name: news-budget
description: "Rank stories the desk can staff today from the sources they have, not from the stories they wish they had. Use when the user mentions news budget, story list, what leads, rundown, or asks for a budget note. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'news-budget' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# News Budget

Rank stories the desk can staff today from the sources they have, not from the stories they wish they had.

## When to use this skill

Use this skill when the user:

- news budget
- story list
- what leads
- rundown

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

- The candidates
- The sources for each
- The staff on shift
- The slot count

## Workflow


### 1. Step 1

Cut stories with no source.
### 2. Step 2

Match the rest to the people on shift.
### 3. Step 3

Put the best-sourced story first, not the loudest topic.
### 4. Step 4

Say what slips.
### 5. Step 5

Do not staff a story with a person who is not on the shift.
### 6. Step 6

Leave a slot empty rather than fill it with an unsourced item.

## Output

Deliver a **budget note**.

- Purpose of this budget note, in two sentences.
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

Five items are on the board. Two have documents. Three reporters are on shift, and one is already out on a fire briefing. Four slots are open on the site.

### Example data

```text
candidates: plant turnaround (statement in hand), fare change (airline PDF in hand), school board rumor (no source), shop-fire follow (reporter out), council land vote (agenda PDF, no vote yet)
staff: 3 reporters, 1 already on the fire
slots: 4
```

### Example outcome

**Budget**
Staff two. Leave the other slots empty.

| Story | Source | Who |
| --- | --- | --- |
| Turnaround dates | statement | Jonah |
| Fare change | airline PDF | second reporter |

Not today: the school rumor, the land vote that has not happened, a second fire story. The reporter is already out and has not filed.
A full rundown is not the goal. An empty slot is better than an unsourced item.

## Anti-patterns

- A lead with no source
- A full rundown nobody can report
- A wish list called a budget

## Related skills

- `news-assignment`
- `editorial-calendar-newsroom`
