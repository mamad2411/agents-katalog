---
name: pip-design
description: "Design a fair, time-boxed improvement plan with observable standards, not a paper trail dressed up as coaching. Use when the user mentions PIP, performance improvement plan, underperformance plan, improvement plan, or asks for a performance improvement plan draft. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pip-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Performance Improvement Plan

Design a fair, time-boxed improvement plan with observable standards, not a paper trail dressed up as coaching.

## When to use this skill

Use this skill when the user:

- PIP
- performance improvement plan
- underperformance plan
- improvement plan

## When not to use this skill

- A plan designed to force someone out
- Discriminatory targeting

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

- The gap, in observable terms
- Support already offered
- The standard for the role
- Duration and reviewer

## Workflow


### 1. Describe the gap

What work is below the standard, with examples. 'Bad attitude' is not a standard.
### 2. Confirm the standard was known

If it was not, the first step may be a clear expectation, not a PIP. Say so.
### 3. Set a short list of observable targets

What done looks like, how it will be measured, and the review dates.
### 4. Support

Training, examples, or workload changes the manager will actually provide.
### 5. Consequences

Use only consequences the user says the company process allows. Do not invent a firing script or a legal conclusion.
### 6. Dignity

The plan is private, specific, and free of humiliation. Refuse plans whose real aim is to force a resignation through impossible tasks.

## Output

Deliver a **performance improvement plan draft**.

- Purpose of this performance improvement plan draft, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a performance improvement plan draft by 30 September 2026. A manager wants a PIP because a teammate 'is not a culture fit' and cannot name a missed deliverable.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants a PIP because a teammate 'is not a culture fit' and cannot name a missed deliverable.

The gap, in observable terms: Jordan Hale is missing a source
Support already offered: CAD 79, dates not set, cap not set
The standard for the role: their one-page rule dated 2 Mar 2026. No exception log since
Duration and reviewer: Chris Adeyemi. No second reviewer named
```

### Example outcome

**Performance improvement plan draft**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Stops the PIP until an observable gap exists, and refuses a plan built to force a resignation.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The gap, in observable terms | Jordan Hale is missing a source | Needs confirmation |
| Support already offered | CAD 79, dates not set, cap not set | Carried into the draft |
| The standard for the role | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Duration and reviewer | Chris Adeyemi. No second reviewer named | Needs confirmation |

**How this draft was built**

**1. Describe the gap**  
What work is below the standard, with examples. 'Bad attitude' is not a standard.

**2. Confirm the standard was known**  
If it was not, the first step may be a clear expectation, not a PIP. Say so.

**3. Set a short list of observable targets**  
What done looks like, how it will be measured, and the review dates.

**4. Support**  
Training, examples, or workload changes the manager will actually provide.

**5. Consequences**  
Use only consequences the user says the company process allows. Do not invent a firing script or a legal conclusion.

**Deliberately not done**
- Vague attitude goals.
- Impossible tasks designed to push someone out.
- Invented legal conclusions about termination.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Vague attitude goals.
- Impossible tasks designed to push someone out.
- Invented legal conclusions about termination.

## Related skills

- `performance-review`
- `employee-relations-intake`
- `manager-one-on-one`
