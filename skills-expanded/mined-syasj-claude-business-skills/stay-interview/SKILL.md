---
name: stay-interview
description: "Prepare a stay conversation that asks what would keep a person, without turning it into surveillance or a promise. Use when the user mentions stay interview, retention conversation, why might they leave, keep this person, or asks for a stay interview guide. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'stay-interview' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Stay Interview

Prepare a stay conversation that asks what would keep a person, without turning it into surveillance or a promise.

## When to use this skill

Use this skill when the user:

- stay interview
- retention conversation
- why might they leave
- keep this person

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

- The person's role
- What the manager can actually change
- Known flight risks the user may share
- Promises already made

## Workflow


### 1. Purpose

Learn what helps this person do their best work and what might push them out. It is voluntary.
### 2. Questions

A few open questions about the work, the manager, and growth. No trick questions. No asking friends' opinions.
### 3. Authority

The manager notes what they can change and what they cannot. Do not script a promise of promotion or pay they cannot keep.
### 4. Listen for themes

Workload, recognition, growth, or manager behavior. Do not diagnose personal lives.
### 5. Follow-up

One action the manager will take, and one they will explicitly not pretend to take.
### 6. Privacy

The notes are for the manager and HR if the user says that is the process. Not for a rumor file.

## Output

Deliver a **stay interview guide**.

- Purpose of this stay interview guide, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a stay interview guide by 30 September 2026. A manager heard a star performer is interviewing and wants a script that promises a new title.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A manager heard a star performer is interviewing and wants a script that promises a new title.

The person's role: Jordan Hale, recorded 14 September 2026. No supporting file attached
What the manager can actually change: requested 14 September 2026. Not yet approved
Known flight risks the user may share: Jordan Hale is open. No score in the file
Promises already made: none written down beyond the ask
```

### Example outcome

**Stay interview guide**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Asks useful questions and forbids a title promise the manager has not had approved.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The person's role | Jordan Hale, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| What the manager can actually change | requested 14 September 2026. Not yet approved | Carried into the draft |
| Known flight risks the user may share | Jordan Hale is open. No score in the file | Carried into the draft |
| Promises already made | none written down beyond the ask | Needs confirmation |

**How this draft was built**

**1. Purpose**  
Learn what helps this person do their best work and what might push them out. It is voluntary.

**2. Questions**  
A few open questions about the work, the manager, and growth. No trick questions. No asking friends' opinions.

**3. Authority**  
The manager notes what they can change and what they cannot. Do not script a promise of promotion or pay they cannot keep.

**4. Listen for themes**  
Workload, recognition, growth, or manager behavior. Do not diagnose personal lives.

**5. Follow-up**  
One action the manager will take, and one they will explicitly not pretend to take.

**Deliberately not done**
- A stay interview that is really an interrogation.
- Fake promotion promises.
- Collecting personal family details.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A stay interview that is really an interrogation.
- Fake promotion promises.
- Collecting personal family details.

## Related skills

- `engagement-survey-readout`
- `compensation-band`
- `manager-one-on-one`
