---
name: lessons-learned
description: "Capture lessons that change a template or a checklist, not lessons that only blame a completed project. Use when the user mentions lessons learned, after action review, project lessons, retrospective of a project, or asks for a lessons note. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'lessons-learned' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Lessons Learned

Capture lessons that change a template or a checklist, not lessons that only blame a completed project.

## When to use this skill

Use this skill when the user:

- lessons learned
- after action review
- project lessons
- retrospective of a project

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Delivery plans are commitments only when owners and dates are real. Do not fabricate status to make a report look healthy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What surprised the team
- Decisions that aged badly
- Evidence
- The template or checklist to change

## Workflow


### 1. Step 1

Describe the surprise as a fact.
### 2. Step 2

Ask what the plan assumed that turned out false.
### 3. Step 3

Write the lesson as a change to a checklist, estimate, or template.
### 4. Step 4

Assign someone to make that change. A lesson with no template change will be repeated.
### 5. Step 5

Keep personalities out.
### 6. Step 6

Limit the note to a few lessons the next project will actually use.

## Output

Deliver a **lessons note**.

- Purpose of this lessons note, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a lessons note by 30 September 2026. A project learned that vendor review takes a month, and the next template still assumes a week.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A project learned that vendor review takes a month, and the next template still assumes a week.

What surprised the team: two people on shift, one off
Decisions that aged badly: A project learned that vendor review takes a month, and the next template still assumes a week
Evidence: one PDF, 2 pages, dated 14 September 2026
The template or checklist to change: Milestone 3 handover; RAID item 12; Change request 118
```

### Example outcome

**Lessons note**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Changes the template's vendor-review duration, with an owner for the edit.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What surprised the team | two people on shift, one off | Needs confirmation |
| Decisions that aged badly | A project learned that vendor review takes a month, and the next template still assumes a week | Carried into the draft |
| Evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The template or checklist to change | Milestone 3 handover; RAID item 12; Change request 118 | Needs confirmation |

**How this draft was built**

**1. Describe the surprise as a fact**

**2. Ask what the plan assumed that turned out false**

**3. Write the lesson as a change to a checklist, estimate, or template**

**4. Assign someone to make that change. A lesson with no template change will be repeated**

**5. Keep personalities out**

**Deliberately not done**
- A blame narrative.
- Lessons with no template change.
- A novel nobody will read.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A blame narrative
- Lessons with no template change
- A novel nobody will read

## Related skills

- `retrospective`
- `project-closeout`
