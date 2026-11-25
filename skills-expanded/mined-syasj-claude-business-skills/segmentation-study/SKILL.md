---
name: segmentation-study
description: "Segment users or customers from supplied data into groups that change an action, not into decorative clusters. Use when the user mentions segmentation, customer segments, cluster analysis, how should we segment, or asks for a segmentation note. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'segmentation-study' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Segmentation Study

Segment users or customers from supplied data into groups that change an action, not into decorative clusters.

## When to use this skill

Use this skill when the user:

- segmentation
- customer segments
- cluster analysis
- how should we segment

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

- The action the segment must change
- Available fields
- Sample limits
- Segments they already use

## Workflow


### 1. Start from the action

message, offer, or service model. Segments that do not change an action are cut.
### 2. Step 2

Use fields they have. Do not require a model they cannot run.
### 3. Step 3

Keep the number of segments small enough to operate.
### 4. Step 4

Describe each segment with a rule a teammate can apply, not only a cluster id.
### 5. Step 5

Note sample size. A segment of a handful of rows is a list, not a strategy.
### 6. Step 6

Recommend one test, not an immediate company-wide rewrite of the motion.

## Output

Deliver a **segmentation note**.

- Purpose of this segmentation note, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a segmentation note by 30 September 2026. A model produced eight clusters and the team cannot say what they would do differently for any of them.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A model produced eight clusters and the team cannot say what they would do differently for any of them.

The action the segment must change: requested 14 September 2026. Not yet approved
Available fields: customers. Stated in the ask, not documented anywhere else
Sample limits: active_accounts, recorded 14 September 2026. No supporting file attached
Segments they already use: orders_daily, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Segmentation note**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Collapses to a few actionable rules and parks the rest as unusable.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The action the segment must change | requested 14 September 2026. Not yet approved | Needs confirmation |
| Available fields | customers. Stated in the ask, not documented anywhere else | Carried into the draft |
| Sample limits | active_accounts, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Segments they already use | orders_daily, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Start from the action**  
message, offer, or service model. Segments that do not change an action are cut.

**2. Use fields they have. Do not require a model they cannot run**

**3. Keep the number of segments small enough to operate**

**4. Describe each segment with a rule a teammate can apply, not only a cluster id**

**5. Note sample size. A segment of a handful of rows is a list, not a strategy**

**Deliberately not done**
- Clusters with no action.
- A segment too small to mean anything.
- Invented demographic attributes.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Clusters with no action
- A segment too small to mean anything
- Invented demographic attributes

## Related skills

- `cohort-analysis`
