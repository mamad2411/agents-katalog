---
name: fleet-safety-review
description: "Review a fleet safety pattern from incidents they logged, and pick one control. Use when the user mentions fleet safety, driver incident review, vehicle incident pattern, transport safety, or asks for a fleet safety review. Transport and logistics operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: transport
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'fleet-safety-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Fleet Safety Review

Review a fleet safety pattern from incidents they logged, and pick one control.

## When to use this skill

Use this skill when the user:

- fleet safety
- driver incident review
- vehicle incident pattern
- transport safety

## When not to use this skill

- Hiding incidents

## Professional boundary

Transport plans follow hours, load, and safety rules the user states. Do not advise concealment of cargo or evasion of inspections.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The incidents
- The pattern they see
- Current controls
- The owner

## Workflow


### 1. Step 1

Use their incident log. Do not invent rates.
### 2. Step 2

Describe the pattern in conditions, not in insults.
### 3. Recommend one control

rest, maintenance, or route design, based on the pattern.
### 4. Step 4

Do not recommend hiding incidents from an insurer or regulator.
### 5. Step 5

Name the owner.
### 6. Step 6

Recheck after the next period.

## Output

Deliver a **fleet safety review**.

- Purpose of this fleet safety review, in two sentences.
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

Luis Ortega, dispatch lead at Kite Freight in Calgary, needs a fleet safety review by 30 September 2026. A review suggests not reporting a minor crash so the score stays clean.

### Example data

```text
From: Luis Ortega, dispatch lead
Organization: Kite Freight, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A review suggests not reporting a minor crash so the score stays clean.

The incidents: Calgary-Edmonton lane, first seen 14 September 2026. No root cause recorded yet
The pattern they see: Calgary-Edmonton lane, recorded 14 September 2026. No supporting file attached
Current controls: their one-page rule dated 2 Mar 2026. No exception log since
The owner: Luis Ortega, dispatch lead
```

### Example outcome

**Fleet safety review**
To: Luis Ortega, dispatch lead, Kite Freight
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the non-report and assigns a control for the actual pattern.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The incidents | Calgary-Edmonton lane, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| The pattern they see | Calgary-Edmonton lane, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Current controls | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| The owner | Luis Ortega, dispatch lead | Needs confirmation |

**How this draft was built**

**1. Use their incident log. Do not invent rates**

**2. Describe the pattern in conditions, not in insults**

**3. Recommend one control**  
rest, maintenance, or route design, based on the pattern.

**4. Do not recommend hiding incidents from an insurer or regulator**

**5. Name the owner**

**Deliberately not done**
- Hidden incidents.
- An invented rate.
- A blame poster with no control.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Luis Ortega by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Hidden incidents
- An invented rate
- A blame poster with no control

## Related skills

- `safety-toolbox-talk`
- `incident-postmortem`
