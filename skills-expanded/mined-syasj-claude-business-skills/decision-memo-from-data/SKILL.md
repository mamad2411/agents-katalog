---
name: decision-memo-from-data
description: "Write a decision memo that uses data the user supplied and labels every non-data judgment. Use when the user mentions decision memo, recommend from this data, data-backed decision, what should we do with these numbers, or asks for a decision memo. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'decision-memo-from-data' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Decision Memo From Data

Write a decision memo that uses data the user supplied and labels every non-data judgment.

## When to use this skill

Use this skill when the user:

- decision memo
- recommend from this data
- data-backed decision
- what should we do with these numbers

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent numbers. If a source file is missing, say so. Distinguish observation from inference. Do not re-identify private data to make a point.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision
- The data
- The options
- The constraints

## Workflow


### 1. Step 1

State the decision in one sentence.
### 2. Step 2

List the data facts that bear on it, with comparisons.
### 3. Step 3

List judgments separately from facts.
### 4. Step 4

Compare options against the constraint they named, not against an invented benchmark.
### 5. Step 5

Recommend one option and the fact that would change it.
### 6. Step 6

Say what the data cannot see.

## Output

Deliver a **decision memo**.

- Purpose of this decision memo, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a decision memo by 30 September 2026. Leadership must cut one of two channels, and the data shows correlation, not incrementality.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Leadership must cut one of two channels, and the data shows correlation, not incrementality.

The decision: Leadership must cut one of two channels, and the data shows correlation, not incrementality
The data: orders_daily, recorded 14 September 2026. No supporting file attached
The options: keep orders_daily, or stop. No third option written
The constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Decision memo**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Recommends a reversible cut or a test, and refuses a causal claim the data cannot support.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision | Leadership must cut one of two channels, and the data shows correlation, not incrementality | Needs confirmation |
| The data | orders_daily, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The options | keep orders_daily, or stop. No third option written | Carried into the draft |
| The constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. State the decision in one sentence**

**2. List the data facts that bear on it, with comparisons**

**3. List judgments separately from facts**

**4. Compare options against the constraint they named, not against an invented benchmark**

**5. Recommend one option and the fact that would change it**

**Deliberately not done**
- A recommendation that ignores the constraint.
- Benchmarks from memory.
- Facts and judgments mixed.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A recommendation that ignores the constraint
- Benchmarks from memory
- Facts and judgments mixed

## Related skills

- `executive-insight`
- `marketing-attribution`
