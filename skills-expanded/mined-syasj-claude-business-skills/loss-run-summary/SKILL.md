---
name: loss-run-summary
description: "Summarize a loss run the user provided, without forecasting a premium or hiding a large loss. Use when the user mentions loss run, claims history summary, loss summary, insurance history, or asks for a loss-run summary. Insurance operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: insurance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'loss-run-summary' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Loss Run Summary

Summarize a loss run the user provided, without forecasting a premium or hiding a large loss.

## When to use this skill

Use this skill when the user:

- loss run
- claims history summary
- loss summary
- insurance history

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not coverage advice and not a claim determination. Do not tell anyone they are covered. Organize facts for a licensed professional.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The loss run
- The years it covers
- Large losses
- What the reader needs

## Workflow


### 1. Step 1

State the period and the source.
### 2. Step 2

Summarize counts and amounts from the run.
### 3. Step 3

Call out large or open items.
### 4. Step 4

Do not drop a loss to improve the picture.
### 5. Step 5

Do not predict an insurer's price.
### 6. Step 6

Note gaps in the years if the run is incomplete.

## Output

Deliver a **loss-run summary**.

- Purpose of this loss-run summary, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a loss-run summary by 30 September 2026. A summary averages away one severe open claim.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A summary averages away one severe open claim.

The loss run: Claim file 8841, recorded 14 September 2026. No supporting file attached
The years it covers: Claim file 8841, recorded 14 September 2026. No supporting file attached
Large losses: Claim file 8841. Stated in the ask, not documented anywhere else
What the reader needs: Priya Shah plus two others named in the thread. No distribution list attached
```

### Example outcome

**Loss-run summary**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows the severe claim separately and makes no price prediction.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The loss run | Claim file 8841, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The years it covers | Claim file 8841, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Large losses | Claim file 8841. Stated in the ask, not documented anywhere else | Carried into the draft |
| What the reader needs | Priya Shah plus two others named in the thread. No distribution list attached | Needs confirmation |

**How this draft was built**

**1. State the period and the source**

**2. Summarize counts and amounts from the run**

**3. Call out large or open items**

**4. Do not drop a loss to improve the picture**

**5. Do not predict an insurer's price**

**Deliberately not done**
- A dropped loss.
- A premium prediction.
- An incomplete run treated as complete.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A dropped loss
- A premium prediction
- An incomplete run treated as complete

## Related skills

- `claim-file-checklist`
- `management-reporting-pack`
