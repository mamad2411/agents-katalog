---
name: clinical-documentation-quality
description: "Review documentation quality for completeness and clarity against their template, not for a diagnosis. Use when the user mentions documentation quality, chart quality, note review, clinical documentation, or asks for a documentation quality review. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'clinical-documentation-quality' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Clinical Documentation Quality

Review documentation quality for completeness and clarity against their template, not for a diagnosis.

## When to use this skill

Use this skill when the user:

- documentation quality
- chart quality
- note review
- clinical documentation

## When not to use this skill

- Upcoding
- Invented clinical facts

## Professional boundary

This is not medical advice, diagnosis, or a treatment protocol. Do not recommend drugs, doses, or clinical interventions. Limit the work to practice operations, documentation quality, and communication drafts for a licensed clinician to approve.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Their template
- The note or a description of gaps
- Who signs
- The handoff risk

## Workflow


### 1. Step 1

Compare the note to their required elements. Missing elements are findings.
### 2. Step 2

Flag ambiguity that would confuse the next clinician, without supplying a diagnosis.
### 3. Step 3

Do not rewrite a note to add clinical facts that were not observed.
### 4. Step 4

Separate a billing-motivated addendum request from a clarity fix. Refuse invented history.
### 5. Step 5

Name who must correct the note under their policy.
### 6. Step 6

This review is not a coding maximization exercise and not medical advice.

## Output

Deliver a **documentation quality review**.

- Purpose of this documentation quality review, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a documentation quality review by 30 September 2026. A manager asks to add a symptom the clinician did not record so a claim pays more.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

A manager asks to add a symptom the clinician did not record so a claim pays more.

Their template: their existing list, 6 lines. Two lines have no owner
The note or a description of gaps: Tuesday clinic is missing a source
Who signs: Dr. Helen Cho, clinic director
The handoff risk: Tuesday clinic is open. No score in the file
```

### Example outcome

**Documentation quality review**
To: Dr. Helen Cho, clinic director, Cedar Clinic
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Are truly missing.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Their template | their existing list, 6 lines. Two lines have no owner | Needs confirmation |
| The note or a description of gaps | Tuesday clinic is missing a source | Carried into the draft |
| Who signs | Dr. Helen Cho, clinic director | Carried into the draft |
| The handoff risk | Tuesday clinic is open. No score in the file | Needs confirmation |

**How this draft was built**

**1. Compare the note to their required elements. Missing elements are findings**

**2. Flag ambiguity that would confuse the next clinician, without supplying a diagnosis**

**3. Do not rewrite a note to add clinical facts that were not observed**

**4. Separate a billing-motivated addendum request from a clarity fix. Refuse invented history**

**5. Name who must correct the note under their policy**

**Deliberately not done**
- Invented history.
- A diagnosis added by the assistant.
- Coding pressure that changes the facts.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented history
- A diagnosis added by the assistant
- Coding pressure that changes the facts

## Related skills

- `medical-billing-review`
- `referral-workflow`
