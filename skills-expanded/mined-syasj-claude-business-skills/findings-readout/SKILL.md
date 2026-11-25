---
name: findings-readout
description: "Read out findings with evidence, implications, and a recommendation the sponsor can reject. Use when the user mentions findings readout, client readout, recommendation readout, consulting readout, or asks for a findings readout. Consulting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: consulting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'findings-readout' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Findings Readout

Read out findings with evidence, implications, and a recommendation the sponsor can reject.

## When to use this skill

Use this skill when the user:

- findings readout
- client readout
- recommendation readout
- consulting readout

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Client work stays confidential to the engagement. Do not fabricate findings to please a sponsor. Separate evidence from recommendation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The findings
- The evidence
- The recommendation
- The audience

## Workflow


### 1. Step 1

Lead with the answer.
### 2. Step 2

Attach evidence to each finding. No evidence, no finding.
### 3. Step 3

Separate implication from fact.
### 4. Step 4

Give the sponsor a real alternative.
### 5. Step 5

Note limits.
### 6. Step 6

Do not soften a finding to please the sponsor, and do not exaggerate to justify fees.

## Output

Deliver a **findings readout**.

- Purpose of this findings readout, in two sentences.
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

Elena Voss, engagement manager at Clearlane Advisors in Calgary, needs a findings readout by 30 September 2026. A readout drops a critical finding because the sponsor disliked it in the dry run.

### Example data

```text
From: Elena Voss, engagement manager
Organization: Clearlane Advisors, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A readout drops a critical finding because the sponsor disliked it in the dry run.

The findings: Scope item 4, recorded 14 September 2026. No supporting file attached
The evidence: one PDF, 2 pages, dated 14 September 2026
The recommendation: Scope item 4, recorded 14 September 2026. No supporting file attached
The audience: people who already buy from Clearlane Advisors
```

### Example outcome

**Findings readout**
To: Elena Voss, engagement manager, Clearlane Advisors
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps the finding, labels it clearly, and offers the sponsor a decision.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The findings | Scope item 4, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The recommendation | Scope item 4, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The audience | people who already buy from Clearlane Advisors | Needs confirmation |

**How this draft was built**

**1. Lead with the answer**

**2. Attach evidence to each finding. No evidence, no finding**

**3. Separate implication from fact**

**4. Give the sponsor a real alternative**

**5. Note limits**

**Deliberately not done**
- Findings with no evidence.
- A readout written to please.
- No alternative.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Findings with no evidence
- A readout written to please
- No alternative

## Related skills

- `executive-one-pager`
- `executive-insight`
