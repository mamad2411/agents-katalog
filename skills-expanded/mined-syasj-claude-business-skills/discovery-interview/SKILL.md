---
name: discovery-interview
description: "Plan a discovery interview that learns the user's current behavior without pitching the solution. Use when the user mentions discovery interview, customer interview, user interview guide, problem interview, or asks for a interview guide. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'discovery-interview' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Discovery Interview

Plan a discovery interview that learns the user's current behavior without pitching the solution.

## When to use this skill

Use this skill when the user:

- discovery interview
- customer interview
- user interview guide
- problem interview

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision the interview must inform
- Who to talk to
- Hypotheses
- What you must not pitch

## Workflow


### 1. Decision

What you will do differently after five interviews. If nothing would change, do not run the interviews.
### 2. Participants

The people who have the problem, not only fans. Note how they will be recruited without deception.
### 3. Guide

Questions about recent behavior, not hypothetical love of your idea.
### 4. No pitching

The solution mention, if any, comes after the story. Do not lead the witness.
### 5. Notes

Capture quotes and concrete incidents. Interpretations go in a separate column.
### 6. Synthesis rule

What pattern across interviews would support or kill the hypothesis.

## Output

Deliver a **interview guide**.

- Purpose of this interview guide, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs an interview guide by 30 September 2026. A founder wants interview questions that ask customers to rate a feature idea from one to ten.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A founder wants interview questions that ask customers to rate a feature idea from one to ten.

The decision the interview must inform: A founder wants interview questions that ask customers to rate a feature idea from one to ten
Who to talk to: Jonah Park, product manager
Hypotheses: Usage limit warning, recorded 14 September 2026. No supporting file attached
What you must not pitch: Usage limit warning, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Interview guide**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Replaces the rating with questions about the last time the problem occurred.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision the interview must inform | A founder wants interview questions that ask customers to rate a feature idea from one to ten | Needs confirmation |
| Who to talk to | Jonah Park, product manager | Carried into the draft |
| Hypotheses | Usage limit warning, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| What you must not pitch | Usage limit warning, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Decision**  
What you will do differently after five interviews. If nothing would change, do not run the interviews.

**2. Participants**  
The people who have the problem, not only fans. Note how they will be recruited without deception.

**3. Guide**  
Questions about recent behavior, not hypothetical love of your idea.

**4. No pitching**  
The solution mention, if any, comes after the story. Do not lead the witness.

**5. Notes**  
Capture quotes and concrete incidents. Interpretations go in a separate column.

**Deliberately not done**
- Asking 'would you use this' as the main question.
- Pitching in the first five minutes.
- Treating one enthusiastic interview as proof.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Asking 'would you use this' as the main question.
- Pitching in the first five minutes.
- Treating one enthusiastic interview as proof.

## Related skills

- `jobs-to-be-done`
- `feedback-synthesis`
