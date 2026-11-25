---
name: farm-record-review
description: "Review farm records for completeness before a buyer, auditor, or lender asks. Use when the user mentions farm records, spray records review, livestock records, traceability farm, or asks for a record review. Agriculture operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: agriculture
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'farm-record-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Farm Record Review

Review farm records for completeness before a buyer, auditor, or lender asks.

## When to use this skill

Use this skill when the user:

- farm records
- spray records review
- livestock records
- traceability farm

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Farm plans are operational, not agronomic prescriptions for hazardous materials. Do not provide instructions for synthesizing pesticides, toxins, or pathogens. A local agronomist or veterinarian should confirm field decisions.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The records they keep
- The asker's list
- Gaps they know
- The period

## Workflow


### 1. Step 1

Compare records to the list they were given.
### 2. Step 2

Flag missing dates, lots, or animal IDs.
### 3. Step 3

Do not backfill a record with invented applications or treatments.
### 4. Step 4

Note withdrawal or treatment questions for their agronomist or veterinarian.
### 5. Step 5

Separate a paperwork gap from a food-safety conclusion.
### 6. Step 6

Recommend a simple habit so the next period is complete.

## Output

Deliver a **record review**.

- Purpose of this record review, in two sentences.
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

Ruth McKay, operator at Two Hills Farm in Olds, needs a record review by 30 September 2026. A buyer asks for treatment records and the draft invents dates to look complete.

### Example data

```text
From: Ruth McKay, operator
Organization: Two Hills Farm, Olds
Date: 14 September 2026
Needed by: 30 September 2026

A buyer asks for treatment records and the draft invents dates to look complete.

The records they keep: one file, dated 14 September 2026. No earlier version attached for comparison
The asker's list: North quarter, 140 acres; Input invoice 442; Harvest window
Gaps they know: North quarter, 140 acres is missing a source
The period: month ending 14 September 2026
```

### Example outcome

**Record review**
To: Ruth McKay, operator, Two Hills Farm
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Lists the gap and refuses the invented dates.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The records they keep | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| The asker's list | North quarter, 140 acres; Input invoice 442; Harvest window | Carried into the draft |
| Gaps they know | North quarter, 140 acres is missing a source | Carried into the draft |
| The period | month ending 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Compare records to the list they were given**

**2. Flag missing dates, lots, or animal IDs**

**3. Do not backfill a record with invented applications or treatments**

**4. Note withdrawal or treatment questions for their agronomist or veterinarian**

**5. Separate a paperwork gap from a food-safety conclusion**

**Deliberately not done**
- Backfilled invented treatments.
- A food-safety clearance.
- Missing lots ignored.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Ruth McKay by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Backfilled invented treatments
- A food-safety clearance
- Missing lots ignored

## Related skills

- `traceability-lot`
- `audit-prep-pbc`
