---
name: structured-interview
description: "Design an interview that asks every candidate the same job-related questions and scores them the same way. Use when the user mentions interview guide, structured interview, interview questions, onsite plan, or asks for a structured interview kit. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'structured-interview' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Structured Interview

Design an interview that asks every candidate the same job-related questions and scores them the same way.

## When to use this skill

Use this skill when the user:

- interview guide
- structured interview
- interview questions
- onsite plan

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

- The outcomes in the job description
- Interview length
- Interviewers and their lanes
- Legal constraints the user already stated

## Workflow


### 1. Map questions to outcomes

Every question earns its place by predicting one outcome. Cut clever questions that do not.
### 2. Write the look-fors

What a strong, mixed, and weak answer contains, so interviewers are not improvising taste.
### 3. Assign lanes

Each interviewer owns different questions. Overlap is a waste of the candidate's time.
### 4. Ban the irrelevant

No questions about family, health, age, or other personal status. If the user asks for those, refuse and explain why.
### 5. Score independently

Interviewers score before the debrief. The debrief discusses evidence, not charisma.
### 6. Candidate experience

Tell the candidate what will be covered and how long it takes. No trick assignments.

## Output

Deliver a **structured interview kit**.

- Purpose of this structured interview kit, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a structured interview kit by 30 September 2026. Two interviewers want to 'just chat' with finalists for a role that has a written outcomes list.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Two interviewers want to 'just chat' with finalists for a role that has a written outcomes list.

The outcomes in the job description: Two interviewers want to 'just chat' with finalists for a role that has a written outcomes list. Stated once, in the ask. Not written down anywhere else
Interview length: plain, for people who already know the context. No house guide attached
Interviewers and their lanes: Sam Okonkwo. Stated in the ask, not documented anywhere else
Legal constraints the user already stated: no extra headcount, and no result that is not in this file
```

### Example outcome

**Structured interview kit**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A kit with shared questions, look-fors, independent scoring, and no personal-status questions.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcomes in the job description | Two interviewers want to 'just chat' with finalists for a role that has a written outcomes list. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Interview length | plain, for people who already know the context. No house guide attached | Carried into the draft |
| Interviewers and their lanes | Sam Okonkwo. Stated in the ask, not documented anywhere else | Carried into the draft |
| Legal constraints the user already stated | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Map questions to outcomes**  
Every question earns its place by predicting one outcome. Cut clever questions that do not.

**2. Write the look-fors**  
What a strong, mixed, and weak answer contains, so interviewers are not improvising taste.

**3. Assign lanes**  
Each interviewer owns different questions. Overlap is a waste of the candidate's time.

**4. Ban the irrelevant**  
No questions about family, health, age, or other personal status. If the user asks for those, refuse and explain why.

**5. Score independently**  
Interviewers score before the debrief. The debrief discusses evidence, not charisma.

**Deliberately not done**
- Unstructured 'tell me about yourself' as the whole process.
- Different questions for different candidates to fish for a favorite.
- Personal-status questions.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Unstructured 'tell me about yourself' as the whole process.
- Different questions for different candidates to fish for a favorite.
- Personal-status questions.

## Related skills

- `hiring-scorecard`
- `job-description-writer`
- `inclusive-hiring`
