---
name: inclusive-hiring
description: "Review a hiring process for avoidable bias in the funnel, using the user's data and without quotas theater. Use when the user mentions inclusive hiring, bias in hiring, diverse slate, hiring process fairness, or asks for a inclusive hiring review. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'inclusive-hiring' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Inclusive Hiring Review

Review a hiring process for avoidable bias in the funnel, using the user's data and without quotas theater.

## When to use this skill

Use this skill when the user:

- inclusive hiring
- bias in hiring
- diverse slate
- hiring process fairness

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

- The stages of their process
- Drop-off data if they have it
- The job criteria
- Constraints they will not fake

## Workflow


### 1. Look at the process before the ads

Criteria, referrals-only sourcing, and unstructured interviews are the usual leaks.
### 2. Use their numbers

If they have no funnel data, the first recommendation is to count, not to claim a representation result.
### 3. Criteria check

Requirements that are not tied to the work are candidates for removal. Say why.
### 4. Slates

A diverse slate is a sourcing practice, not a hiring quota and not a reason to tokenise a person. Refuse tactics that treat people as props.
### 5. Interview consistency

Structured questions are the practical fix. See the structured interview skill rather than repeating a sermon.
### 6. Do not invent demographics

Never guess a person's identity to fill a chart.

## Output

Deliver a **inclusive hiring review**.

- Purpose of this inclusive hiring review, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs an inclusive hiring review by 30 September 2026. A company hires only from employee referrals and wants a more inclusive process without changing the referral habit.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A company hires only from employee referrals and wants a more inclusive process without changing the referral habit.

The stages of their process: email to Chris Adeyemi. No written steps after 1 Sep 2026
Drop-off data if they have it: Jordan Hale. Stated in the ask, not documented anywhere else
The job criteria: their existing list, 6 lines. Two lines have no owner
Constraints they will not fake: no extra headcount, and no result that is not in this file
```

### Example outcome

**Inclusive hiring review**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names referrals-only sourcing as the constraint and recommends a structured process plus real counting, with no invented demographics.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The stages of their process | email to Chris Adeyemi. No written steps after 1 Sep 2026 | Needs confirmation |
| Drop-off data if they have it | Jordan Hale. Stated in the ask, not documented anywhere else | Carried into the draft |
| The job criteria | their existing list, 6 lines. Two lines have no owner | Carried into the draft |
| Constraints they will not fake | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Look at the process before the ads**  
Criteria, referrals-only sourcing, and unstructured interviews are the usual leaks.

**2. Use their numbers**  
If they have no funnel data, the first recommendation is to count, not to claim a representation result.

**3. Criteria check**  
Requirements that are not tied to the work are candidates for removal. Say why.

**4. Slates**  
A diverse slate is a sourcing practice, not a hiring quota and not a reason to tokenise a person. Refuse tactics that treat people as props.

**5. Interview consistency**  
Structured questions are the practical fix. See the structured interview skill rather than repeating a sermon.

**Deliberately not done**
- Invented demographic statistics.
- Tokenising candidates.
- A quota dressed up as a process tip.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented demographic statistics.
- Tokenising candidates.
- A quota dressed up as a process tip.

## Related skills

- `structured-interview`
- `job-description-writer`
- `hiring-scorecard`
