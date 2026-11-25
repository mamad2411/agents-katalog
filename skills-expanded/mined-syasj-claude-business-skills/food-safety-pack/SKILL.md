---
name: food-safety-pack
description: "Assemble a food-safety document pack from the practices they already run, for their auditor or buyer. Use when the user mentions food safety pack, farm audit pack, GAP pack, buyer food safety, or asks for a food-safety pack. Agriculture operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: agriculture
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'food-safety-pack' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Food Safety Pack

Assemble a food-safety document pack from the practices they already run, for their auditor or buyer.

## When to use this skill

Use this skill when the user:

- food safety pack
- farm audit pack
- GAP pack
- buyer food safety

## When not to use this skill

- Pathogen production
- Toxin instructions

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

- Practices they documented
- The buyer's checklist
- Known gaps
- The owner

## Workflow


### 1. Step 1

Map their documents to the checklist.
### 2. Step 2

Missing items stay missing.
### 3. Step 3

Do not write a procedure for a practice they do not perform and present it as current.
### 4. Step 4

Escalate hazards they named to the person responsible. Do not provide pathogen growth or toxin instructions.
### 5. Step 5

Name the owner of each gap.
### 6. Step 6

This pack is not a certification.

## Output

Deliver a **food-safety pack**.

- Purpose of this food-safety pack, in two sentences.
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

Ruth McKay, operator at Two Hills Farm in Olds, needs a food-safety pack by 30 September 2026. A pack includes a handwashing SOP the farm does not use, to satisfy a checklist.

### Example data

```text
From: Ruth McKay, operator
Organization: Two Hills Farm, Olds
Date: 14 September 2026
Needed by: 30 September 2026

A pack includes a handwashing SOP the farm does not use, to satisfy a checklist.

Practices they documented: one PDF, 2 pages, dated 14 September 2026
The buyer's checklist: North quarter, 140 acres; Input invoice 442; Harvest window
Known gaps: North quarter, 140 acres is missing a source
The owner: Ruth McKay, operator
```

### Example outcome

**Food-safety pack**
To: Ruth McKay, operator, Two Hills Farm
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks the SOP as not in place and assigns an owner if they choose to adopt it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Practices they documented | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |
| The buyer's checklist | North quarter, 140 acres; Input invoice 442; Harvest window | Carried into the draft |
| Known gaps | North quarter, 140 acres is missing a source | Carried into the draft |
| The owner | Ruth McKay, operator | Needs confirmation |

**How this draft was built**

**1. Map their documents to the checklist**

**2. Missing items stay missing**

**3. Do not write a procedure for a practice they do not perform and present it as current**

**4. Escalate hazards they named to the person responsible. Do not provide pathogen growth or toxin instructions**

**5. Name the owner of each gap**

**Deliberately not done**
- A fake current procedure.
- Pathogen or toxin instructions.
- A certification claim.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Ruth McKay by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A fake current procedure
- Pathogen or toxin instructions
- A certification claim

## Related skills

- `audit-prep-pbc`
- `sop-writer`
