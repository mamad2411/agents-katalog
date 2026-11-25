---
name: executive-insight
description: "Turn an analysis into a one-page insight a leader can use, with the number, the comparison, and the limit. Use when the user mentions insight memo, executive readout, so what from the data, analytics summary, or asks for a insight memo. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'executive-insight' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Executive Insight Memo

Turn an analysis into a one-page insight a leader can use, with the number, the comparison, and the limit.

## When to use this skill

Use this skill when the user:

- insight memo
- executive readout
- so what from the data
- analytics summary

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

- The finding
- The comparison
- The decision it informs
- Caveats

## Workflow


### 1. Step 1

Lead with the finding and the comparison in one or two sentences.
### 2. Step 2

Show only numbers they provided. Round only if you say so.
### 3. Step 3

State what the finding does not prove.
### 4. Step 4

Recommend one decision or one question.
### 5. Step 5

Put method in a short note, not in the opening.
### 6. Step 6

Do not add a market explanation you were not given.

## Output

Deliver a **insight memo**.

- Purpose of this insight memo, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs an insight memo by 30 September 2026. An analyst has a retention drop and wants the memo to say a competitor caused it.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

An analyst has a retention drop and wants the memo to say a competitor caused it.

The finding: orders_daily, recorded 14 September 2026. No supporting file attached
The comparison: orders_daily, recorded 14 September 2026. No supporting file attached
The decision it informs: An analyst has a retention drop and wants the memo to say a competitor caused it
Caveats: orders_daily is open. customers was raised verbally and never logged
```

### Example outcome

**Insight memo**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Reports the drop, refuses the competitor cause without evidence, and names the next question.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The finding | orders_daily, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The comparison | orders_daily, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The decision it informs | An analyst has a retention drop and wants the memo to say a competitor caused it | Carried into the draft |
| Caveats | orders_daily is open. customers was raised verbally and never logged | Needs confirmation |

**How this draft was built**

**1. Lead with the finding and the comparison in one or two sentences**

**2. Show only numbers they provided. Round only if you say so**

**3. State what the finding does not prove**

**4. Recommend one decision or one question**

**5. Put method in a short note, not in the opening**

**Deliberately not done**
- A chart dump with no sentence.
- Causal language the design does not support.
- Invented context.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A chart dump with no sentence
- Causal language the design does not support
- Invented context

## Related skills

- `analysis-plan`
- `decision-memo-from-data`
