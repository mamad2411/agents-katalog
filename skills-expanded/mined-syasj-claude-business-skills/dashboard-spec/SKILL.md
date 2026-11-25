---
name: dashboard-spec
description: "Specify a dashboard that answers a few decisions, with an owner and a refresh the team can trust. Use when the user mentions dashboard spec, design a dashboard, KPI dashboard, executive dashboard, or asks for a dashboard specification. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'dashboard-spec' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Dashboard Spec

Specify a dashboard that answers a few decisions, with an owner and a refresh the team can trust.

## When to use this skill

Use this skill when the user:

- dashboard spec
- design a dashboard
- KPI dashboard
- executive dashboard

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

- The decisions the dashboard must support
- The metrics and their definitions
- Who will use it and how often
- Known data delays

## Workflow


### 1. Step 1

Limit the dashboard to the decisions named. A gallery of charts is a finding.
### 2. Step 2

Every chart needs a question, a defined metric, and a source.
### 3. Step 3

State the refresh lag. A daily decision on a monthly feed is a mismatch.
### 4. Step 4

Specify filters that change a decision, not every possible slice.
### 5. Step 5

Name the owner who fixes a broken number.
### 6. Step 6

Include an empty-state note for when data is late, so nobody reads a blank chart as zero.

## Output

Deliver a **dashboard specification**.

- Purpose of this dashboard specification, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a dashboard specification by 30 September 2026. A leader wants 30 tiles on one page and cannot name the Monday decision.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A leader wants 30 tiles on one page and cannot name the Monday decision.

The decisions the dashboard must support: A leader wants 30 tiles on one page and cannot name the Monday decision
The metrics and their definitions: plan 180, actual 95
Who will use it and how often: Noah Berger, data lead
Known data delays: customers. Stated in the ask, not documented anywhere else
```

### Example outcome

**Dashboard specification**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A spec of a few decision tiles, each with a source, a lag, and an owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decisions the dashboard must support | A leader wants 30 tiles on one page and cannot name the Monday decision | Needs confirmation |
| The metrics and their definitions | plan 180, actual 95 | Carried into the draft |
| Who will use it and how often | Noah Berger, data lead | Carried into the draft |
| Known data delays | customers. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Limit the dashboard to the decisions named. A gallery of charts is a finding**

**2. Every chart needs a question, a defined metric, and a source**

**3. State the refresh lag. A daily decision on a monthly feed is a mismatch**

**4. Specify filters that change a decision, not every possible slice**

**5. Name the owner who fixes a broken number**

**Deliberately not done**
- A chart with no question.
- Hidden refresh lag.
- No owner for a broken tile.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A chart with no question
- Hidden refresh lag
- No owner for a broken tile

## Related skills

- `metric-definition`
- `management-reporting-pack`
