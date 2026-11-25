---
name: product-analytics-spec
description: "Specify the events and properties a product change needs so the team can tell whether it worked. Use when the user mentions tracking plan, event spec, analytics specification, what should we instrument, or asks for a analytics spec. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'product-analytics-spec' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Product Analytics Spec

Specify the events and properties a product change needs so the team can tell whether it worked.

## When to use this skill

Use this skill when the user:

- tracking plan
- event spec
- analytics specification
- what should we instrument

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

- The decision the data must support
- The user actions that matter
- Existing events
- Privacy limits they already follow

## Workflow


### 1. Decision first

Write the question, then the events. Do not add events with no question.
### 2. Event definitions

Name, trigger, and properties. A vague 'button clicked' with no context is a finding.
### 3. Identity

How a user is recognized, using their existing approach. Do not invent a tracking identity that violates their privacy rules.
### 4. Privacy

Collect the minimum. Do not specify secrets, full card numbers, or health details as event properties.
### 5. QA

How an engineer will know the event fired correctly before release.
### 6. Naming

Match their existing convention. Do not rename the warehouse for one feature.

## Output

Deliver a **analytics spec**.

- Purpose of this analytics spec, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs an analytics spec by 30 September 2026. A spec adds a property for a user's full home address to measure a button click.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A spec adds a property for a user's full home address to measure a button click.

The decision the data must support: A spec adds a property for a user's full home address to measure a button click
The user actions that matter: Activation checklist; Trial day-3 email. Both unassigned as of 14 September 2026
Existing events: Trial day-3 email, last reviewed 14 September 2026. No owner named since
Privacy limits they already follow: email and billing address. They said no health data
```

### Example outcome

**Analytics spec**
Fieldnote · 14 September 2026 · Due 30 September 2026

**Decision**
Removes the address, defines the click in context, and names the decision it serves.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Harbor & Co | plan 150, actual 105 | Use | Both sides of the comparison are in the file |
| Lumen Ledger | score 78 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Decision first
2. Event definitions
3. Identity
4. Privacy
5. QA: How an engineer will know the event fired correctly before release

**Deliberately not done**
- Events with no decision behind them.
- Tracking secrets or card numbers.
- A spec that ignores the current naming convention.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Jonah Park attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- Events with no decision behind them.
- Tracking secrets or card numbers.
- A spec that ignores the current naming convention.

## Related skills

- `event-tracking-spec`
- `privacy-by-design`
