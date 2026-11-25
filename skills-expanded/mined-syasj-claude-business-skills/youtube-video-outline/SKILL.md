---
name: youtube-video-outline
description: "Outline one YouTube video with a cold open, chapters, and a point that is the creator's own. Use when the user mentions YouTube script outline, video outline, YouTube structure, plan this video, or asks for a video outline. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'youtube-video-outline' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# YouTube Video Outline

Outline one YouTube video with a cold open, chapters, and a point that is the creator's own.

## When to use this skill

Use this skill when the user:

- YouTube script outline
- video outline
- YouTube structure
- plan this video

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

- The viewer question
- The creator's own experience or sources
- Target length
- What must not be claimed

## Workflow


### 1. Step 1

Write the viewer question in the first two sentences.
### 2. Step 2

Outline chapters that answer it. Cut a chapter that only exists to stretch the video.
### 3. Step 3

Mark which lines are the creator's experience and which need a source.
### 4. Step 4

Do not paste another creator's script, a book chapter, or lyrics.
### 5. Plan the screen

what is shown, not only what is said.
### 6. Step 6

End with one next step, not three asks.

## Output

Deliver a **video outline**.

- Purpose of this video outline, in two sentences.
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

Maya is filming an 8-minute video on Thursday. The question is how to get a chicken dinner done when she got home at 5:40. She has her own grocery receipt and last Thursday's timing notes. She does not have another channel's script.

### Example data

```text
viewer: got home at 5:40, wants to eat by 6:20
promise: one chicken dinner, three steps, list on screen
length: 8 minutes
sources she has: Co-op receipt 10 Sep 2026, $18.40; her timing note from 11 Sep, 36 minutes
must not use: any other creator's outline or transcript
filming: Thursday 18 Sep 2026, 7 p.m.
```

### Example outcome

**Outline — Chicken when you get home at 5:40**

0:00 Hook: the receipt is $18.40 and the clock starts at 5:40.
0:20 Promise: eat by 6:20. Three steps. No second shop.
1:00 Step 1, from her 11 Sep note: pan hot before the chicken is unwrapped. 4 minutes.
3:00 Step 2: the tray from that note, 18 minutes, not a new time she has not tried.
5:30 Step 3: the list on screen, items from the 10 Sep receipt only.
7:20 What she would change: the onion was late last time. Say that. Do not invent a fix she has not cooked.
7:50 Close: the 36-minute result from her note. Not a promise that every kitchen matches it.

Sources on screen: her receipt, her note. No other channel.

## Anti-patterns

- A script copied from another channel
- An outline with no viewer question
- Unsourced statistics presented as the creator's knowledge

## Related skills

- `youtube-title-thumbnail`
- `voiceover-read-script`
