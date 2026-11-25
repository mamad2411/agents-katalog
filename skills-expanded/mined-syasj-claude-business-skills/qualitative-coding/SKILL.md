---
name: qualitative-coding
description: "Plan qualitative coding so themes come from the data they have, with a second-coder check when it matters. Use when the user mentions qualitative coding, codebook, thematic analysis, code these interviews, or asks for a coding plan. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'qualitative-coding' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Qualitative Coding Plan

Plan qualitative coding so themes come from the data they have, with a second-coder check when it matters.

## When to use this skill

Use this skill when the user:

- qualitative coding
- codebook
- thematic analysis
- code these interviews

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

- The question
- The transcripts or notes they have
- Whether a second coder exists
- The decision

## Workflow


### 1. Step 1

Start from the question, not from a favorite theme.
### 2. Step 2

Define codes with inclusion and exclusion examples from their text only.
### 3. Step 3

Do not invent quotations.
### 4. Step 4

If reliability matters for the decision, plan a second coder on a sample.
### 5. Step 5

Separate codes from themes. A theme needs more than one code name.
### 6. Step 6

Note what the sample cannot support.

## Output

Deliver a **coding plan**.

- Purpose of this coding plan, in two sentences.
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

Dr. Nia Okonkwo, research lead at Riverbend College in Lethbridge, needs a coding plan by 30 September 2026. A report lists themes and the user has not provided the supporting lines.

### Example data

```text
From: Dr. Nia Okonkwo, research lead
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A report lists themes and the user has not provided the supporting lines.

The question: A report lists themes and the user has not provided the supporting lines
The transcripts or notes they have: one file, dated 14 September 2026. No earlier version attached for comparison
Whether a second coder exists: Interview set A. Partly documented: the what is written down, the who is not
The decision: A report lists themes and the user has not provided the supporting lines
```

### Example outcome

**Coding plan**
To: Dr. Nia Okonkwo, research lead, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the report until each theme has a supplied excerpt.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question | A report lists themes and the user has not provided the supporting lines | Needs confirmation |
| The transcripts or notes they have | one file, dated 14 September 2026. No earlier version attached for comparison | Carried into the draft |
| Whether a second coder exists | Interview set A. Partly documented: the what is written down, the who is not | Carried into the draft |
| The decision | A report lists themes and the user has not provided the supporting lines | Needs confirmation |

**How this draft was built**

**1. Start from the question, not from a favorite theme**

**2. Define codes with inclusion and exclusion examples from their text only**

**3. Do not invent quotations**

**4. If reliability matters for the decision, plan a second coder on a sample**

**5. Separate codes from themes. A theme needs more than one code name**

**Deliberately not done**
- Invented quotations.
- Themes decided before reading.
- A codebook with no examples.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Nia Okonkwo by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented quotations
- Themes decided before reading
- A codebook with no examples

## Related skills

- `interview-guide-research`
- `research-memo`
