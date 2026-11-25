---
name: instagram-reel-brief
description: "Brief one Instagram Reel with the shot list, the line, and the cover frame. Use when the user mentions Instagram Reel, Reel brief, plan a Reel, Reel script, or asks for a Reel brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'instagram-reel-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Instagram Reel Brief

Brief one Instagram Reel with the shot list, the line, and the cover frame.

## When to use this skill

Use this skill when the user:

- Instagram Reel
- Reel brief
- plan a Reel
- Reel script

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

- The point
- The location and props they have
- Length
- Music they are allowed to use

## Workflow


### 1. Step 1

Write the spoken line and the shot list together.
### 2. Step 2

Cover frame must be understandable with the sound off.
### 3. Step 3

Use only music or audio the creator can confirm they may use. Do not tell them to rip a track.
### 4. Step 4

One Reel, one point.
### 5. Step 5

Note the caption job so it does not repeat a false claim.
### 6. Step 6

Do not storyboard a recreation of another creator's Reel.

## Output

Deliver a **Reel brief**.

- Purpose of this Reel brief, in two sentences.
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

Maya is filming the chicken Reel on Thursday. It is not paid. She needs the shot list so she does not wander into a pantry tour.

### Example data

```text
length: 35 to 45 seconds
fact: 5:40 start, 36 minutes on 11 Sep, $18.40 receipt
paid: no
shots she can get: clock, pan, chicken, list, plate
shot she tends to add: cupboard tour
post: 19 Sep 2026
```

### Example outcome

**Reel brief**
One dinner. Not a tour.

| Order | Shot | Seconds | Fact on screen |
| --- | --- | --- | --- |
| 1 | Phone clock | 3 | 5:40 |
| 2 | Pan, empty, heat on | 4 | none |
| 3 | Chicken in | 8 | 36 min, her note |
| 4 | Receipt | 5 | $18.40 |
| 5 | Plate | 6 | eat by 6:20 |

Cut if she films it: the cupboard.
Disclosure: none. Not paid.
Caption points at the list, not at a health result.

## Anti-patterns

- A copied Reel
- Unlicensed music presented as free
- A cover that depends on sound

## Related skills

- `tiktok-short-script`
- `instagram-caption`
