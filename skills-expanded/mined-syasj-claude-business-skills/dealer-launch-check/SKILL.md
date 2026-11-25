---
name: dealer-launch-check
description: "Check whether a local launch day has the cars, the staff, and the offer the dealer can honor. Use when the user mentions dealer launch, model launch day, sales event ready, launch checklist, or asks for a launch check. Automotive skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: automotive
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'dealer-launch-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Dealer Launch Check

Check whether a local launch day has the cars, the staff, and the offer the dealer can honor.

## When to use this skill

Use this skill when the user:

- dealer launch
- model launch day
- sales event ready
- launch checklist

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not a repair procedure for safety-critical systems and not a recall determination. Do not invent defect rates or tell anyone to disable a safety feature.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Cars on the ground
- Staff roster
- The offer
- The date

## Workflow


### 1. Step 1

Count cars they can demo.
### 2. Step 2

Match staff to the date.
### 3. Step 3

The offer must be one they can honor on the day.
### 4. Step 4

Do not advertise a payment they did not calculate.
### 5. Step 5

Hold the event claim if the cars are in transit.
### 6. Step 6

Name the owner.

## Output

Deliver a **launch check**.

- Purpose of this launch check, in two sentences.
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

Saturday's ad says six cars to test-drive and a $299 payment. Two cars are on the ground. The payment was not calculated. Four staff are rostered.

### Example data

```text
date: Sat 20 Sep 2026
ad: 6 test-drive cars, $299 a month
on the ground: 2
in transit: 4, no arrival date
staff rostered: 4
payment worksheet: none
owner: Carla Singh
```

### Example outcome

**Launch check**
Cut the ad to two test-drive cars. The other four are not on the ground.
Remove $299. Nobody calculated it.
Staff: four are rostered. That part can stand.
Owner: Carla. She does not run the six-car line on Saturday.

## Anti-patterns

- An ad for cars that are not on the ground
- A payment invented for the ad
- Staff who are not rostered

## Related skills

- `dealer-morning-review`
- `local-service-offer`
