---
name: youtube-title-thumbnail
description: "Write title and thumbnail options that match the video the creator actually made. Use when the user mentions YouTube title, thumbnail text, title ideas, packaging a video, or asks for a title and thumbnail brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'youtube-title-thumbnail' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# YouTube Title and Thumbnail

Write title and thumbnail options that match the video the creator actually made.

## When to use this skill

Use this skill when the user:

- YouTube title
- thumbnail text
- title ideas
- packaging a video

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

- What the video actually delivers
- The audience
- Words they must not use
- The frame they can film or design

## Workflow


### 1. Step 1

State the payoff the video really contains.
### 2. Step 2

Write a few titles that a stranger could understand. No empty curiosity with no payoff.
### 3. Step 3

Thumbnail text is three or four words that match the title, not a second mystery.
### 4. Ban claims the video does not prove

income, cures, 'they hated me'.
### 5. Step 5

Note the image the creator can legally use. Do not tell them to grab a celebrity face or another channel's thumbnail.
### 6. Step 6

Pick one pair and say what would make it dishonest.

## Output

Deliver a **title and thumbnail brief**.

- Purpose of this title and thumbnail brief, in two sentences.
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

Maya needs three title options and one thumbnail line for the chicken video. She wants them to sound like a video she saw with 2 million views. She may not copy that title. Her own result is 36 minutes and $18.40.

### Example data

```text
result she can show: 36 minutes, $18.40, 11 Sep and 10 Sep notes
viewer: home at 5:40
must not copy: "I tried the viral chicken hack"
thumbnail space: 4 words or fewer
deadline: title locked 17 Sep 2026
```

### Example outcome

**Titles she can use**
1. Home at 5:40. Chicken at 6:20.
2. The $18 chicken I actually timed.
3. 36 minutes, one pan, no second shop.

**Do not use**
Any title built by rewriting a viral video.

**Thumbnail line**
5:40 to 6:20

**Why this one**
It is the time in her note. It does not claim a view count or a hack.

## Anti-patterns

- Clickbait the video does not pay off
- Another creator's thumbnail
- A medical or money claim with no proof

## Related skills

- `youtube-video-outline`
- `marketing-claims-review`
