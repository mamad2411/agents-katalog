---
name: opportunity-assessment
description: "Assess whether an opportunity is worth a discovery sprint, using evidence rather than enthusiasm. Use when the user mentions opportunity assessment, is this worth building, product opportunity, discovery go or no-go, or asks for a opportunity assessment. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'opportunity-assessment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Opportunity Assessment

Assess whether an opportunity is worth a discovery sprint, using evidence rather than enthusiasm.

## When to use this skill

Use this skill when the user:

- opportunity assessment
- is this worth building
- product opportunity
- discovery go or no-go

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

- The proposed opportunity
- Evidence in hand
- Strategic bets it must serve
- Cost of a sprint

## Workflow


### 1. Strategic fit

Does it serve a stated bet. If there is no strategy, say the assessment is local only.
### 2. Evidence grade

Strong, weak, or absent, based only on supplied evidence.
### 3. Alternatives

Include doing nothing and fixing adoption of what already exists.
### 4. Cost of learning

A small sprint with a question, not a quarter of build by default.
### 5. Kill criteria

What result would stop the work.
### 6. Recommendation

Sprint, park, or kill, with the missing fact named.

## Output

Deliver a **opportunity assessment**.

- Purpose of this opportunity assessment, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs an opportunity assessment by 30 September 2026. A large customer requested a feature that fits none of the current bets.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A large customer requested a feature that fits none of the current bets.

The proposed opportunity: Activation checklist, recorded 14 September 2026. No supporting file attached
Evidence in hand: one PDF, 2 pages, dated 14 September 2026
Strategic bets it must serve: 35 in the last period. No prior period attached, so no trend
Cost of a sprint: CAD 27 direct. Overhead not in this line
```

### Example outcome

**Opportunity assessment**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Parks the feature, names the strategy conflict, and defines the evidence that would reopen it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The proposed opportunity | Activation checklist, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Evidence in hand | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Strategic bets it must serve | 35 in the last period. No prior period attached, so no trend | Carried into the draft |
| Cost of a sprint | CAD 27 direct. Overhead not in this line | Needs confirmation |

**How this draft was built**

**1. Strategic fit**  
Does it serve a stated bet. If there is no strategy, say the assessment is local only.

**2. Evidence grade**  
Strong, weak, or absent, based only on supplied evidence.

**3. Alternatives**  
Include doing nothing and fixing adoption of what already exists.

**4. Cost of learning**  
A small sprint with a question, not a quarter of build by default.

**5. Kill criteria**  
What result would stop the work.

**Deliberately not done**
- A yes because a customer shouted.
- Skipping the do-nothing option.
- A quarter-long build disguised as discovery.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A yes because a customer shouted.
- Skipping the do-nothing option.
- A quarter-long build disguised as discovery.

## Related skills

- `product-brief`
- `portfolio-prioritization`
