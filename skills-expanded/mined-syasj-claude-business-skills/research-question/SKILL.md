---
name: research-question
description: "Sharpen a research question so it is answerable with the methods and access the user has. Use when the user mentions research question, sharpen my question, study question, is this researchable, or asks for a research question. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'research-question' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Research Question

Sharpen a research question so it is answerable with the methods and access the user has.

## When to use this skill

Use this skill when the user:

- research question
- sharpen my question
- study question
- is this researchable

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The draft question
- The decision or knowledge gap
- Available access
- Time and skill limits

## Workflow


### 1. Step 1

Separate a topic from a question.
### 2. Step 2

Name the population, phenomenon, and comparison or change, as applicable.
### 3. Step 3

Check that the user can reach the evidence. A question they cannot observe needs a redesign.
### 4. Step 4

State what the question will not answer.
### 5. Step 5

Flag ethics review if people are involved. Do not invent an approval.
### 6. Step 6

Recommend the smallest study that would answer it.

## Output

Deliver a **research question**.

- Purpose of this research question, in two sentences.
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

Dr. Nia Okonkwo, research lead at Riverbend College in Lethbridge, needs a research question by 30 September 2026. The question is 'is remote work good' with no population or outcome.

### Example data

```text
From: Dr. Nia Okonkwo, research lead
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

The question is 'is remote work good' with no population or outcome.

The draft question: The question is 'is remote work good' with no population or outcome
The decision or knowledge gap: The question is 'is remote work good' with no population or outcome
Available access: Search log 12 Sep. Stated in the ask, not documented anywhere else
Time and skill limits: five working days, due 30 September 2026
```

### Example outcome

**Research question**
To: Dr. Nia Okonkwo, research lead, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A narrower question with a population, an outcome, and an explicit non-answer.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The draft question | The question is 'is remote work good' with no population or outcome | Needs confirmation |
| The decision or knowledge gap | The question is 'is remote work good' with no population or outcome | Carried into the draft |
| Available access | Search log 12 Sep. Stated in the ask, not documented anywhere else | Carried into the draft |
| Time and skill limits | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Separate a topic from a question**

**2. Name the population, phenomenon, and comparison or change, as applicable**

**3. Check that the user can reach the evidence. A question they cannot observe needs a redesign**

**4. State what the question will not answer**

**5. Flag ethics review if people are involved. Do not invent an approval**

**Deliberately not done**
- A topic pretending to be a question.
- A design they cannot access.
- Skipping ethics when people are involved.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Nia Okonkwo by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A topic pretending to be a question
- A design they cannot access
- Skipping ethics when people are involved

## Related skills

- `literature-review-plan`
- `ethics-review-prep`
