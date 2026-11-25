---
name: station-open-check
description: "Check the station open items against the list the station uses. Use when the user mentions station opening, open checklist, first wave, station ready, or asks for a open check. Airline operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: airline
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'station-open-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Station Open Check

Check the station open items against the list the station uses.

## When to use this skill

Use this skill when the user:

- station opening
- open checklist
- first wave
- station ready

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

- Their open list
- Items done
- The first wave
- Who signs

## Workflow


### 1. Step 1

Walk their list.
### 2. Step 2

A fuel or security item left open blocks the first wave.
### 3. Step 3

Do not mark an item done because the time has arrived.
### 4. Step 4

Name the signer.
### 5. Step 5

Separate a commercial item from a safety item.
### 6. Step 6

Do not skip a check to make the first departure.

## Output

Deliver a **open check**.

- Purpose of this open check, in two sentences.
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

The first wave is KA188 at 06:10. Fuel paperwork is still open. A draft says open the station because the clock says 05:40.

### Example data

```text
first wave: KA188 at 06:10
open: fuel paperwork
done: security walk, gate screens
signer required: Luis Ortega
draft: open anyway, it is 05:40
```

### Example outcome

**Open check**
Hold KA188. Fuel paperwork is open. The clock does not close it.
Done: security walk, gate screens.
Signer: Luis. He does not sign the fuel line blank.
A commercial wish to leave on time is not a reason to skip the check.

## Anti-patterns

- A safety item marked done by the clock
- A first wave released against an open check
- No signer

## Related skills

- `crew-duty-limit`
- `irrops-brief`
