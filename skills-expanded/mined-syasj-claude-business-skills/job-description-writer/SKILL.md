---
name: job-description-writer
description: "Write a job description from outcomes and constraints, not a wishlist of tools and years. Use when the user mentions job description, write a JD, role profile, hiring post, or asks for a job description. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'job-description-writer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Job Description Writer

Write a job description from outcomes and constraints, not a wishlist of tools and years.

## When to use this skill

Use this skill when the user:

- job description
- write a JD
- role profile
- hiring post

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

- Why the role exists now
- Outcomes for the first year
- Team and manager
- Location, level, and whether pay can be disclosed

## Workflow


### 1. Purpose

One sentence a candidate can repeat, tied to the team's current need.
### 2. Outcomes

Three to five first-year results. Tools support outcomes. They are not the job.
### 3. Must-haves

Cap at five. A requirement the manager cannot defend as a predictor moves to nice-to-have.
### 4. Context

Level, location, travel, and reporting line. Do not invent a salary. If pay is undisclosed, say so.
### 5. Inclusive language

Remove jargon and requirements that narrow the pool without improving the work, and say what you removed.
### 6. Process

How to apply and what the process involves, only if the user knows it. Do not invent a hiring promise.

## Output

Deliver a **job description**.

- Purpose of this job description, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a job description by 30 September 2026. A manager wants a senior analyst posting and sends a list of software products.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants a senior analyst posting and sends a list of software products.

Why the role exists now: A manager wants a senior analyst posting and sends a list of software products
Outcomes for the first year: A manager wants a senior analyst posting and sends a list of software products. Stated once, in the ask. Not written down anywhere else
Team and manager: two people on shift, one off
Location, level, and whether pay can be disclosed: two deals cited from memory. Neither has a written loss reason
```

### Example outcome

**Job description**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A posting with first-year outcomes, five must-haves, and pay left undisclosed rather than invented.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Why the role exists now | A manager wants a senior analyst posting and sends a list of software products | Needs confirmation |
| Outcomes for the first year | A manager wants a senior analyst posting and sends a list of software products. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Team and manager | two people on shift, one off | Carried into the draft |
| Location, level, and whether pay can be disclosed | two deals cited from memory. Neither has a written loss reason | Needs confirmation |

**How this draft was built**

**1. Purpose**  
One sentence a candidate can repeat, tied to the team's current need.

**2. Outcomes**  
Three to five first-year results. Tools support outcomes. They are not the job.

**3. Must-haves**  
Cap at five. A requirement the manager cannot defend as a predictor moves to nice-to-have.

**4. Context**  
Level, location, travel, and reporting line. Do not invent a salary. If pay is undisclosed, say so.

**5. Inclusive language**  
Remove jargon and requirements that narrow the pool without improving the work, and say what you removed.

**Deliberately not done**
- A tool dump.
- Ten must-haves copied from a senior role onto a junior one.
- An invented salary range.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A tool dump.
- Ten must-haves copied from a senior role onto a junior one.
- An invented salary range.

## Related skills

- `structured-interview`
- `hiring-scorecard`
- `compensation-band`
