---
name: regulatory-change-log
description: "Log a regulatory change the user has identified, with impact questions and an owner, without giving a legal opinion. Use when the user mentions regulatory change, new rule log, compliance change, regulation tracker, or asks for a regulatory change log. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'regulatory-change-log' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Regulatory Change Log

Log a regulatory change the user has identified, with impact questions and an owner, without giving a legal opinion.

## When to use this skill

Use this skill when the user:

- regulatory change
- new rule log
- compliance change
- regulation tracker

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The source they provided
- The date they believe applies
- Products or processes affected
- The owner

## Workflow


### 1. Step 1

Record the source they gave. Do not invent a citation.
### 2. Step 2

Summarize the change in their words and mark uncertainties.
### 3. List impact questions for counsel or compliance

does it apply, by when, and to which process.
### 4. Step 4

Assign an owner to get those answers.
### 5. Step 5

Do not tell the business to ignore a rule, and do not declare them compliant.
### 6. Step 6

Review the log on a cadence so a noted change does not sit unread.

## Output

Deliver a **regulatory change log**.

- Purpose of this regulatory change log, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a regulatory change log by 30 September 2026. A blog post says a rule changed, and the team wants to mark the company compliant today.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A blog post says a rule changed, and the team wants to mark the company compliant today.

The source they provided: note from Priya Shah, 14 September 2026. No outside report
The date they believe applies: 30 September 2026
Products or processes affected: email to Priya Shah. No written steps after 1 Sep 2026
The owner: Priya Shah, controller
```

### Example outcome

**Regulatory change log**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Sources the blog as unverified, assigns counsel questions, and makes no compliance claim.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The source they provided | note from Priya Shah, 14 September 2026. No outside report | Needs confirmation |
| The date they believe applies | 30 September 2026 | Carried into the draft |
| Products or processes affected | email to Priya Shah. No written steps after 1 Sep 2026 | Carried into the draft |
| The owner | Priya Shah, controller | Needs confirmation |

**How this draft was built**

**1. Record the source they gave. Do not invent a citation**

**2. Summarize the change in their words and mark uncertainties**

**3. List impact questions for counsel or compliance**  
does it apply, by when, and to which process.

**4. Assign an owner to get those answers**

**5. Do not tell the business to ignore a rule, and do not declare them compliant**

**Deliberately not done**
- An invented citation.
- A compliance declaration.
- An instruction to ignore a rule.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented citation
- A compliance declaration
- An instruction to ignore a rule

## Related skills

- `compliance-calendar`
- `outside-counsel-brief`
