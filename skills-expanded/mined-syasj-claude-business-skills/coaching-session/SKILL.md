---
name: coaching-session
description: "Plan a coaching conversation that builds a skill on real work, not a motivational speech. Use when the user mentions coaching session, coach a manager, feedback coaching, skill coaching, or asks for a coaching session plan. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'coaching-session' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Coaching Session

Plan a coaching conversation that builds a skill on real work, not a motivational speech.

## When to use this skill

Use this skill when the user:

- coaching session
- coach a manager
- feedback coaching
- skill coaching

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The skill to build
- A recent work example
- What good looks like
- The coachee's goal

## Workflow


### 1. Pick one skill

Coaching on five traits in one sitting teaches nothing.
### 2. Use a real moment

A meeting, a draft, or a decision from the last two weeks.
### 3. Show the gap

The difference between what happened and what good looks like, specifically.
### 4. Practice

The session includes a redo, not only advice.
### 5. Ask before telling

Start with the coachee's view. A lecture is not coaching.
### 6. Next rep

Where they will try the skill again, and when you will review it.

## Output

Deliver a **coaching session plan**.

- Purpose of this coaching session plan, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a coaching session plan by 30 September 2026. A team lead's written updates confuse stakeholders, and the director wants a coaching plan.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A team lead's written updates confuse stakeholders, and the director wants a coaching plan.

The skill to build: Jordan Hale, recorded 14 September 2026. No supporting file attached
A recent work example: Jordan Hale; Sam Okonkwo. Both unassigned as of 14 September 2026
What good looks like: Open coordinator role, last reviewed 14 September 2026. No owner named since
The coachee's goal: A team lead's written updates confuse stakeholders, and the director wants a coaching plan. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Coaching session plan**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A session built on one recent update, with a redo in the meeting and a next rep on the following weekly note.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The skill to build | Jordan Hale, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| A recent work example | Jordan Hale; Sam Okonkwo. Both unassigned as of 14 September 2026 | Carried into the draft |
| What good looks like | Open coordinator role, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The coachee's goal | A team lead's written updates confuse stakeholders, and the director wants a coaching plan. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Pick one skill**  
Coaching on five traits in one sitting teaches nothing.

**2. Use a real moment**  
A meeting, a draft, or a decision from the last two weeks.

**3. Show the gap**  
The difference between what happened and what good looks like, specifically.

**4. Practice**  
The session includes a redo, not only advice.

**5. Ask before telling**  
Start with the coachee's view. A lecture is not coaching.

**Deliberately not done**
- A pep talk with no example.
- Five development areas in thirty minutes.
- Coaching that is really a PIP in disguise. Use the PIP skill if standards are missed repeatedly.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A pep talk with no example.
- Five development areas in thirty minutes.
- Coaching that is really a PIP in disguise. Use the PIP skill if standards are missed repeatedly.

## Related skills

- `manager-one-on-one`
- `performance-review`
- `learning-path`
