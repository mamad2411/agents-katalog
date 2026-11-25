---
name: conflict-mediation
description: "Prepare a fair conversation between coworkers in conflict, without taking a side or diagnosing character. Use when the user mentions team conflict, mediate a disagreement, coworker conflict, working relationship breakdown, or asks for a mediation prep. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'conflict-mediation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Conflict Mediation Prep

Prepare a fair conversation between coworkers in conflict, without taking a side or diagnosing character.

## When to use this skill

Use this skill when the user:

- team conflict
- mediate a disagreement
- coworker conflict
- working relationship breakdown

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

- The work that is suffering
- Each person's stated concern, if known
- What the manager has already tried
- Safety issues, if any

## Workflow


### 1. Safety first

If the user describes threats, harassment, or violence, stop mediation tips and point them to their reporting and safety process. Do not investigate as a hobby.
### 2. Frame the work

The conversation is about a working agreement, not about who is the better person.
### 3. Each voice

Structure time so both people state the impact on the work. No surprise audience.
### 4. Interests

What each person needs in order to deliver. Positions are 'I refuse to work with them'. Interests are more useful.
### 5. Agreement

A written working agreement with behaviors and a review date. No forced apology script.
### 6. Escalation

If the conflict includes possible misconduct, route it to employee relations instead of a cozy mediation.

## Output

Deliver a **mediation prep**.

- Purpose of this mediation prep, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a mediation prep by 30 September 2026. Two leads are blocking each other's releases, and one has started insulting the other in public channels.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Two leads are blocking each other's releases, and one has started insulting the other in public channels.

The work that is suffering: Jordan Hale; Sam Okonkwo. Both unassigned as of 14 September 2026
Each person's stated concern, if known: Jordan Hale, last reviewed 14 September 2026. No owner named since
What the manager has already tried: Open coordinator role, last reviewed 14 September 2026. No owner named since
Safety issues, if any: Open coordinator role. Partly documented: the what is written down, the who is not
```

### Example outcome

**Mediation prep**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Addresses the work blockage, moves insults out of public channels, and routes possible misconduct to employee relations.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The work that is suffering | Jordan Hale; Sam Okonkwo. Both unassigned as of 14 September 2026 | Needs confirmation |
| Each person's stated concern, if known | Jordan Hale, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| What the manager has already tried | Open coordinator role, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Safety issues, if any | Open coordinator role. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Safety first**  
If the user describes threats, harassment, or violence, stop mediation tips and point them to their reporting and safety process. Do not investigate as a hobby.

**2. Frame the work**  
The conversation is about a working agreement, not about who is the better person.

**3. Each voice**  
Structure time so both people state the impact on the work. No surprise audience.

**4. Interests**  
What each person needs in order to deliver. Positions are 'I refuse to work with them'. Interests are more useful.

**5. Agreement**  
A written working agreement with behaviors and a review date. No forced apology script.

**Deliberately not done**
- Taking a side in the prep notes.
- Mediating a harassment allegation informally.
- A forced apology.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Taking a side in the prep notes.
- Mediating a harassment allegation informally.
- A forced apology.

## Related skills

- `employee-relations-intake`
- `manager-one-on-one`
- `stakeholder-map`
