---
name: learning-path
description: "Build a learning path for a role from the work, with practice tasks rather than a course catalog. Use when the user mentions learning path, upskilling plan, training plan for a role, skill development plan, or asks for a learning path. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'learning-path' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Learning Path

Build a learning path for a role from the work, with practice tasks rather than a course catalog.

## When to use this skill

Use this skill when the user:

- learning path
- upskilling plan
- training plan for a role
- skill development plan

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

- The skill gap in work terms
- Time available per week
- Real tasks they can practice on
- How proficiency will be judged

## Workflow


### 1. Define proficiency

What the person will be able to do, observed on the job. Course completion is not proficiency.
### 2. Sequence

Foundations, guided practice, then independent work. Skip modules that do not serve the gap.
### 3. Use real work

Prefer a sanitized piece of their actual work over a generic exercise.
### 4. Time box

Fit the path to the weekly time they have. A 40-hour plan for someone with two hours is not a plan.
### 5. Coach

Who reviews the practice. A path with no reviewer is content, not development.
### 6. Stop rule

If the gap is actually a job-design problem, say so instead of training someone to survive a broken role.

## Output

Deliver a **learning path**.

- Purpose of this learning path, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a learning path by 30 September 2026. An analyst is told to 'learn finance' in a month while closing the books full time.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An analyst is told to 'learn finance' in a month while closing the books full time.

The skill gap in work terms: Jordan Hale is missing a source
Time available per week: five working days, due 30 September 2026
Real tasks they can practice on: An analyst is told to 'learn finance' in a month while closing the books full time. Stated once, in the ask. Not written down anywhere else
How proficiency will be judged: Sam Okonkwo, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Learning path**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
The time budget does not fit a broad finance education.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The skill gap in work terms | Jordan Hale is missing a source | Needs confirmation |
| Time available per week | five working days, due 30 September 2026 | Carried into the draft |
| Real tasks they can practice on | An analyst is told to 'learn finance' in a month while closing the books full time. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| How proficiency will be judged | Sam Okonkwo, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Define proficiency**  
What the person will be able to do, observed on the job. Course completion is not proficiency.

**2. Sequence**  
Foundations, guided practice, then independent work. Skip modules that do not serve the gap.

**3. Use real work**  
Prefer a sanitized piece of their actual work over a generic exercise.

**4. Time box**  
Fit the path to the weekly time they have. A 40-hour plan for someone with two hours is not a plan.

**5. Coach**  
Who reviews the practice. A path with no reviewer is content, not development.

**Deliberately not done**
- A course catalog dump.
- Completion certificates as the goal.
- Ignoring an impossible workload.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A course catalog dump.
- Completion certificates as the goal.
- Ignoring an impossible workload.

## Related skills

- `onboarding-plan`
- `training-needs-analysis`
- `performance-review`
