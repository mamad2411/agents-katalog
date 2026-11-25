---
name: tiktok-series-plan
description: "Plan a short TikTok series with a repeatable promise and an end, not an endless repost loop. Use when the user mentions TikTok series, content series, episode plan, TikTok calendar, or asks for a series plan. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tiktok-series-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# TikTok Series Plan

Plan a short TikTok series with a repeatable promise and an end, not an endless repost loop.

## When to use this skill

Use this skill when the user:

- TikTok series
- content series
- episode plan
- TikTok calendar

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Creator work must be original and honest. Do not copy another person's script, footage, voice, or caption. Do not invent metrics, fake engagement, or undisclosed sponsorships. Do not impersonate a real person. Prompt skills must not weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The promise of the series
- How many episodes they can film
- What they will show
- What they will not repeat from other accounts

## Workflow


### 1. Step 1

Write the series promise in one line.
### 2. Step 2

Plan only as many episodes as they can film from their own material.
### 3. Step 3

Each episode needs a distinct beat, not the same caption with a new number.
### 4. Step 4

Say how a viewer knows the series is over.
### 5. Step 5

Do not plan a series that stitches another creator's work as the product.
### 6. Step 6

Set a review after the planned run instead of promising daily forever.

## Output

Deliver a **series plan**.

- Purpose of this series plan, in two sentences.
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

Maya wants a five-part TikTok series next week. She can film Tuesday and Thursday only. Each part has to stand alone because she knows many people will see only one.

### Example data

```text
nights free: Tue 23 Sep and Thu 25 Sep, 7 to 9 p.m.
parts she asked for: 5
dinners she has already cooked and timed: chicken 36 min, chili 40 min, eggs 12 min
not yet cooked: a fish dinner, a noodle dinner
rule: each part must make sense with no other part
```

### Example outcome

**Series**
Three parts, not five. Two nights cannot hold five uncooked dinners.

| Part | Dinner | Status | Night |
| --- | --- | --- | --- |
| 1 | Chicken | timed 11 Sep | Tue |
| 2 | Chili | timed 28 Aug | Tue, second setup only if part 1 wraps by 8 |
| 3 | Eggs | timed, 12 minutes | Thu |

Fish and noodles are not in the plan. She has not cooked them on the clock.
Each caption names the dinner. None says 'part 4 of 5'.

## Anti-patterns

- A series made of other people's clips
- Identical episodes
- A cadence they cannot film

## Related skills

- `faceless-source-check`
- `content-batch-plan`
