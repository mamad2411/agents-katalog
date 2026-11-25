---
name: crew-duty-limit
description: "Check a duty figure against the limit the user provides. Do not advise exceeding it. Use when the user mentions crew duty, duty limit, pairing hours, crew legality check, or asks for a duty check. Airline operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: airline
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'crew-duty-limit' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Crew Duty Check

Check a duty figure against the limit the user provides. Do not advise exceeding it.

## When to use this skill

Use this skill when the user:

- crew duty
- duty limit
- pairing hours
- crew legality check

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not advise exceeding a duty limit, skipping a maintenance release, or concealing a safety issue. Passenger messages must match the facts supplied.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The hours they calculated
- The limit they stated
- The pairing
- Who releases the crew

## Workflow


### 1. Step 1

Compare their hours to their limit.
### 2. Step 2

If they are over, say stop.
### 3. Step 3

Do not suggest a workaround.
### 4. Step 4

If the hours are incomplete, say the check cannot pass.
### 5. Step 5

Name who releases the crew.
### 6. Step 6

This is not a regulatory opinion beyond the limit they stated.

## Output

Deliver a **duty check**.

- Purpose of this duty check, in two sentences.
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

A pairing is calculated at 14 hours. The limit Luis was given for this duty is 13. Someone asked how to make the pairing legal.

### Example data

```text
pairing: KA412 turn plus KA188
hours calculated: 14
limit stated: 13
hours complete: yes, his sheet
release owner: crew scheduling, not the station agent
ask: how to make it legal
```

### Example outcome

**Duty check**
Stop. 14 is over the 13 they stated.
No workaround is in this check. Do not split, waive, or reword the hours to pass.
Release sits with crew scheduling. The station does not release this pairing.
This is not a regulatory opinion beyond the limit in the file.

## Anti-patterns

- A workaround over the limit
- A pass with incomplete hours
- A homemade legal opinion

## Related skills

- `irrops-brief`
- `station-open-check`
