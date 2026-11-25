---
name: succession-plan
description: "Name successors for a few critical roles based on evidence, and identify the gap without a secret ranking of everyone's worth. Use when the user mentions succession plan, bench strength, who could replace, critical role backup, or asks for a succession plan. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'succession-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Succession Plan

Name successors for a few critical roles based on evidence, and identify the gap without a secret ranking of everyone's worth.

## When to use this skill

Use this skill when the user:

- succession plan
- bench strength
- who could replace
- critical role backup

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The critical roles
- Possible successors the user names
- Evidence of readiness
- Roles with no backup

## Workflow


### 1. Limit the scope

A handful of critical roles, not a ranking of the whole company.
### 2. Ready now versus ready later

Use evidence of work already done. Potential without evidence is labeled as such.
### 3. Emergency cover

Who covers the role for two weeks. That is different from a permanent successor.
### 4. Gaps

A role with no cover is the finding. Do not invent a successor to make the chart look full.
### 5. Development

One experience the likely successor still needs. Not a personality makeover.
### 6. Sensitivity

The plan is confidential. Do not draft an email that tells people they are or are not successors unless the user has a communication plan reviewed by HR.

## Output

Deliver a **succession plan**.

- Purpose of this succession plan, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a succession plan by 30 September 2026. The head of implementation is a single point of failure, and nobody has led a rollout without them.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The head of implementation is a single point of failure, and nobody has led a rollout without them.

The critical roles: Chris Adeyemi plus two others named in the thread. No distribution list attached
Possible successors the user names: Sam Okonkwo, recorded 14 September 2026. No supporting file attached
Evidence of readiness: one PDF, 2 pages, dated 14 September 2026
Roles with no backup: Chris Adeyemi plus two others named in the thread. No distribution list attached
```

### Example outcome

**Succession plan**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the emergency cover gap honestly and defines the experience a successor still needs.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The critical roles | Chris Adeyemi plus two others named in the thread. No distribution list attached | Needs confirmation |
| Possible successors the user names | Sam Okonkwo, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Evidence of readiness | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Roles with no backup | Chris Adeyemi plus two others named in the thread. No distribution list attached | Needs confirmation |

**How this draft was built**

**1. Limit the scope**  
A handful of critical roles, not a ranking of the whole company.

**2. Ready now versus ready later**  
Use evidence of work already done. Potential without evidence is labeled as such.

**3. Emergency cover**  
Who covers the role for two weeks. That is different from a permanent successor.

**4. Gaps**  
A role with no cover is the finding. Do not invent a successor to make the chart look full.

**5. Development**  
One experience the likely successor still needs. Not a personality makeover.

**Deliberately not done**
- A stack rank of all employees.
- Naming a successor with no evidence to fill a box.
- A careless email announcing the plan.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A stack rank of all employees.
- Naming a successor with no evidence to fill a box.
- A careless email announcing the plan.

## Related skills

- `workforce-plan`
- `org-design-review`
- `learning-path`
