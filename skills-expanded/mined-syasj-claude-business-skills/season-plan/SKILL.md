---
name: season-plan
description: "Plan a season from fields, labor, and cash the farm can actually commit. Use when the user mentions season plan, crop plan, planting plan, farm season, or asks for a season plan. Agriculture operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: agriculture
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'season-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Season Plan

Plan a season from fields, labor, and cash the farm can actually commit.

## When to use this skill

Use this skill when the user:

- season plan
- crop plan
- planting plan
- farm season

## When not to use this skill

- Pesticide or toxin synthesis
- Pathogen production

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

- Fields or enterprises
- Labor
- Cash constraints
- Rotation or withdrawal limits they already follow

## Workflow


### 1. Step 1

List enterprises they will run.
### 2. Step 2

Match labor and equipment to the calendar they supplied.
### 3. Step 3

Note cash needs at the expensive weeks.
### 4. Step 4

Respect withdrawal or rotation limits they stated. Do not provide instructions to synthesize pesticides or bypass a label.
### 5. Step 5

Identify the week that breaks if labor is short.
### 6. Step 6

This is an operating plan, not agronomic or veterinary advice.

## Output

Deliver a **season plan**.

- Purpose of this season plan, in two sentences.
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

Ruth McKay, operator at Two Hills Farm in Olds, needs a season plan by 30 September 2026. A plan adds a crop the only operator cannot harvest in the same week as the existing one.

### Example data

```text
From: Ruth McKay, operator
Organization: Two Hills Farm, Olds
Date: 14 September 2026
Needed by: 30 September 2026

A plan adds a crop the only operator cannot harvest in the same week as the existing one.

Fields or enterprises: North quarter, 140 acres, last reviewed 14 September 2026. No owner named since
Labor: Input invoice 442 and one other, both unconfirmed as of 14 September 2026
Cash constraints: no extra headcount, and no result that is not in this file
Rotation or withdrawal limits they already follow: Input invoice 442, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Season plan**
To: Ruth McKay, operator, Two Hills Farm
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows the labor clash and asks which enterprise to cut.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Fields or enterprises | North quarter, 140 acres, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Labor | Input invoice 442 and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Cash constraints | no extra headcount, and no result that is not in this file | Carried into the draft |
| Rotation or withdrawal limits they already follow | Input invoice 442, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. List enterprises they will run**

**2. Match labor and equipment to the calendar they supplied**

**3. Note cash needs at the expensive weeks**

**4. Respect withdrawal or rotation limits they stated. Do not provide instructions to synthesize pesticides or bypass a label**

**5. Identify the week that breaks if labor is short**

**Deliberately not done**
- Pesticide synthesis.
- A plan that ignores a stated label limit.
- No labor check.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Ruth McKay by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Pesticide synthesis
- A plan that ignores a stated label limit
- No labor check

## Related skills

- `cash-flow-forecast`
- `workforce-plan`
