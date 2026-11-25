---
name: onboarding-plan
description: "Plan a new hire's first weeks so they can do useful work without drinking from a firehose of links. Use when the user mentions onboarding plan, first week plan, new hire ramp, orientation plan, or asks for a onboarding plan. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'onboarding-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Onboarding Plan

Plan a new hire's first weeks so they can do useful work without drinking from a firehose of links.

## When to use this skill

Use this skill when the user:

- onboarding plan
- first week plan
- new hire ramp
- orientation plan

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

- Role outcomes
- Start date
- Tools and access they truly need
- The buddy or manager

## Workflow


### 1. Week-one outcome

One useful piece of work, not a tour of every tool.
### 2. Access list

Only the systems required for that work. Do not request or store passwords in the plan.
### 3. People

Manager, buddy, and the three colleagues they will need. A 20-person meet-and-greet is optional, not the plan.
### 4. Context pack

The strategy page, the team scorecard, and the glossary they actually use.
### 5. Checkpoints

End of week one and end of week four, with questions the manager will ask.
### 6. Feedback path

How the hire raises confusion early. Onboarding is a management duty, not only an HR calendar.

## Output

Deliver a **onboarding plan**.

- Purpose of this onboarding plan, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs an onboarding plan by 30 September 2026. A new analyst starts Monday and the current plan is a folder of 40 documents.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A new analyst starts Monday and the current plan is a folder of 40 documents.

Role outcomes: A new analyst starts Monday and the current plan is a folder of 40 documents. Stated once, in the ask. Not written down anywhere else
Start date: 30 September 2026
Tools and access they truly need: the one named in the ask. Version and owner not recorded
The buddy or manager: Jordan Hale, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Onboarding plan**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A four-week plan with one week-one deliverable, a short access list, and two manager checkpoints.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Role outcomes | A new analyst starts Monday and the current plan is a folder of 40 documents. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Start date | 30 September 2026 | Carried into the draft |
| Tools and access they truly need | the one named in the ask. Version and owner not recorded | Carried into the draft |
| The buddy or manager | Jordan Hale, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Week-one outcome**  
One useful piece of work, not a tour of every tool.

**2. Access list**  
Only the systems required for that work. Do not request or store passwords in the plan.

**3. People**  
Manager, buddy, and the three colleagues they will need. A 20-person meet-and-greet is optional, not the plan.

**4. Context pack**  
The strategy page, the team scorecard, and the glossary they actually use.

**5. Checkpoints**  
End of week one and end of week four, with questions the manager will ask.

**Deliberately not done**
- A link dump.
- No manager checkpoint.
- Passwords written into the plan.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A link dump.
- No manager checkpoint.
- Passwords written into the plan.

## Related skills

- `thirty-sixty-ninety`
- `job-description-writer`
- `learning-path`
