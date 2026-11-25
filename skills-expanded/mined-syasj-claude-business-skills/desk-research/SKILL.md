---
name: desk-research
description: "Brief desk research so secondary sources are scoped, credited, and not mistaken for primary proof. Use when the user mentions desk research, secondary research, landscape scan, background research, or asks for a desk research brief. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'desk-research' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Desk Research Brief

Brief desk research so secondary sources are scoped, credited, and not mistaken for primary proof.

## When to use this skill

Use this skill when the user:

- desk research
- secondary research
- landscape scan
- background research

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision
- Sources they can use
- Time
- What would count as good enough

## Workflow


### 1. Step 1

Define the decision and the facts that would change it.
### 2. Step 2

List source types they will accept.
### 3. Step 3

Credit every fact with the source they found. Unknown stays unknown.
### 4. Step 4

Separate a vendor's marketing from independent reporting.
### 5. Step 5

Stop when the decision is informed or the time box ends.
### 6. Step 6

Do not present desk research as a customer study.

## Output

Deliver a **desk research brief**.

- Purpose of this desk research brief, in two sentences.
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

Dr. Nia Okonkwo, research lead at Riverbend College in Lethbridge, needs a desk research brief by 30 September 2026. A landscape scan quotes a vendor's homepage as market share.

### Example data

```text
From: Dr. Nia Okonkwo, research lead
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A landscape scan quotes a vendor's homepage as market share.

The decision: A landscape scan quotes a vendor's homepage as market share
Sources they can use: note from Dr. Nia Okonkwo, 14 September 2026. No outside report
Time: five working days, due 30 September 2026
What would count as good enough: 25 in the last period. No prior period attached, so no trend
```

### Example outcome

**Desk research brief**
To: Dr. Nia Okonkwo, research lead, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Labels the homepage as a claim, not as market share, and lists the missing independent source.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision | A landscape scan quotes a vendor's homepage as market share | Needs confirmation |
| Sources they can use | note from Dr. Nia Okonkwo, 14 September 2026. No outside report | Carried into the draft |
| Time | five working days, due 30 September 2026 | Carried into the draft |
| What would count as good enough | 25 in the last period. No prior period attached, so no trend | Needs confirmation |

**How this draft was built**

**1. Define the decision and the facts that would change it**

**2. List source types they will accept**

**3. Credit every fact with the source they found. Unknown stays unknown**

**4. Separate a vendor's marketing from independent reporting**

**5. Stop when the decision is informed or the time box ends**

**Deliberately not done**
- Vendor copy treated as independent proof.
- Unsourced facts.
- Desk research sold as interviews.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Nia Okonkwo by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Vendor copy treated as independent proof
- Unsourced facts
- Desk research sold as interviews

## Related skills

- `market-entry-assessment`
- `citation-hygiene`
