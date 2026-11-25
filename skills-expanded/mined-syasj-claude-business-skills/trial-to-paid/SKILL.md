---
name: trial-to-paid
description: "Report trial-to-paid from the cohort dates in the export. Use when the user mentions trial conversion, trial to paid, free trial results, cohort conversion, or asks for a conversion note. SaaS skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: saas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'trial-to-paid' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Trial To Paid

Report trial-to-paid from the cohort dates in the export.

## When to use this skill

Use this skill when the user:

- trial conversion
- trial to paid
- free trial results
- cohort conversion

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent churn, revenue, retention, or a security certification. If the export is missing, say so.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The trial start dates
- Paid counts
- The trial length
- Cohorts still inside the trial

## Workflow


### 1. Step 1

Exclude cohorts that have not finished the trial.
### 2. Step 2

Use their paid definition.
### 3. Step 3

Do not count a trial that is still running as a failure.
### 4. Step 4

Show the finished cohort only.
### 5. Step 5

Do not invent a channel split they did not export.
### 6. Step 6

Name the date the next cohort closes.

## Output

Deliver a **conversion note**.

- Purpose of this conversion note, in two sentences.
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

August trials: 100 started, 18 paid, trial length 14 days, all finished. September trials started 1 to 14 September and are still inside 14 days. A slide blends them.

### Example data

```text
trial length: 14 days
August: 100 started, 18 paid, cohort closed
September 1-14: 80 started, still inside the trial
paid definition: a paid workspace, not a card added and removed
channel split: not exported
```

### Example outcome

**Conversion**
August, closed: 18 of 100.
September 1-14: still open. Do not count them as lost or as converted.
Do not blend the months.
No channel split. None was exported.
Next cohort closes 28 September for the 14 September starts.

## Anti-patterns

- An open cohort counted as lost
- A channel story with no export
- A blended rate that hides the definition

## Related skills

- `activation-gap`
- `saas-weekly-metrics`
