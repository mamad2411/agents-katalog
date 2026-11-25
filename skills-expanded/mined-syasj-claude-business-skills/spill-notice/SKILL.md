---
name: spill-notice
description: "Draft the internal notice for a release the user has already described, with the facts they have. Use when the user mentions spill notice, release notification draft, incident notice, what do we report internally, or asks for a notice draft. Oil and gas operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: oil-gas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'spill-notice' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Spill Notice

Draft the internal notice for a release the user has already described, with the facts they have.

## When to use this skill

Use this skill when the user:

- spill notice
- release notification draft
- incident notice
- what do we report internally

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational drafts only. Do not bypass isolation, lockout, permits, or reporting duties. Do not write instructions to conceal a release or to operate outside the site's limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What they saw
- When
- Where
- Who has already been told

## Workflow


### 1. Step 1

Use their description. Do not add a volume they did not measure.
### 2. Step 2

Record the time and place.
### 3. Step 3

List who has been told.
### 4. Step 4

Do not write language that hides the release.
### 5. Step 5

Do not give cleanup chemistry or a way to avoid a report.
### 6. Step 6

Say which facts are still unknown.

## Output

Deliver a **notice draft**.

- Purpose of this notice draft, in two sentences.
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

A night operator saw a sheen at the pad flare knock-out at 02:10. Nobody measured the area. A draft says it was minor and does not need a log.

### Example data

```text
what was seen: sheen, flare knock-out, pad 14-22
when: 16 Sep 2026 02:10
measured volume: none
already told: night lead, by radio at 02:15
draft line: minor, no need to log
```

### Example outcome

**Notice**
Sheen seen at the flare knock-out, pad 14-22, 02:10 on 16 September. Volume: unknown. Do not write a litre figure.
Already told: night lead, radio, 02:15.
The line 'no need to log' comes out. This notice is the log.
Unknown: area, cause, whether it left the pad. Leave them unknown.
This draft does not tell anyone how to clean it up or how to avoid a report.

## Anti-patterns

- A hidden release
- An invented volume
- Cleanup instructions that bypass the site procedure

## Related skills

- `hse-observation`
- `outage-communication`
