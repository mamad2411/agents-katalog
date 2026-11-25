---
name: permit-checklist-local
description: "List the permits the owner already knows they need, and the ones they have not checked. Use when the user mentions local permit, business license checklist, do I need a permit, sidewalk permit, or asks for a permit checklist. Small business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: small-business
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'permit-checklist-local' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Local Permit Checklist

List the permits the owner already knows they need, and the ones they have not checked.

## When to use this skill

Use this skill when the user:

- local permit
- business license checklist
- do I need a permit
- sidewalk permit

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not legal, tax, or employment advice. Do not invent license rules, tax rates, or a local bylaw.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The activity
- Permits they already hold
- The fee sheet if they have one
- What they have not asked the town

## Workflow


### 1. Step 1

List permits they hold.
### 2. Step 2

List the activity.
### 3. Step 3

If they have a fee sheet, use that fee.
### 4. Step 4

Do not invent a bylaw.
### 5. Step 5

Mark unchecked items as unchecked.
### 6. Step 6

Tell them to ask the town before they build the plan on a guess.

## Output

Deliver a **permit checklist**.

- Purpose of this permit checklist, in two sentences.
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

Diane has a business licence on the wall and a 2026 fee sheet that lists a sidewalk display at $75. She wants a sign and has not asked the town. A blog said signs under a certain size are free. She has no bylaw text.

### Example data

```text
holds: business licence, number on the wall copy
fee sheet: sidewalk display $75, effective 1 Jan 2026
activity she wants: a new sign, plus the sidewalk display
bylaw text: not in the folder
blog line: small signs are free
```

### Example outcome

**Checklist**
| Item | Status |
| --- | --- |
| Business licence | she holds one, wall copy |
| Sidewalk display | fee sheet says $75. Not the same as approved. |
| Sign | unchecked. Ask the town. |

The blog line about free signs is not a bylaw. It comes off the list.
This checklist is not an approval.

## Anti-patterns

- An invented bylaw
- A fee from memory
- A checklist that says they are approved

## Related skills

- `blog-refresh`
- `local-service-offer`
