---
name: youtube-description-pack
description: "Write a YouTube description, chapters, and links from the video that was actually recorded. Use when the user mentions YouTube description, chapter timestamps, video description, YouTube SEO description, or asks for a description pack. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'youtube-description-pack' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# YouTube Description Pack

Write a YouTube description, chapters, and links from the video that was actually recorded.

## When to use this skill

Use this skill when the user:

- YouTube description
- chapter timestamps
- video description
- YouTube SEO description

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

- The real chapters and times if known
- Links the creator may share
- Affiliate or sponsor facts
- Keywords that match the video

## Workflow


### 1. Step 1

First lines say what the viewer gets. Do not stuff keywords the video does not cover.
### 2. Step 2

Chapters match the edit. If times are unknown, leave a placeholder instead of inventing them.
### 3. Step 3

Disclose paid links and sponsors in the description, not only in a spoken aside the viewer can miss.
### 4. Step 4

Link only pages the creator supplied.
### 5. Step 5

Do not add a false transcript of someone else's video.
### 6. Step 6

Keep the description useful on a phone.

## Output

Deliver a **description pack**.

- Purpose of this description pack, in two sentences.
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

Maya needs the description for the chicken video. She has three chapter times, one grocery link she really uses, and a paid-pan disclosure that does not belong on this video. This video is not sponsored.

### Example data

```text
title: Home at 5:40. Chicken at 6:20.
chapters: 0:00 clock, 1:00 pan, 5:30 list
link she can include: her own list note, not an affiliate
sponsored: no
tags she brainstormed: viral hack, weight loss dinner, must try
publish: 19 Sep 2026
```

### Example outcome

**Description**
Home at 5:40, eating at 6:20. Times are from my 11 September note. The list totalled $18.40 on 10 September. Your shop will differ.

0:00 Clock starts
1:00 Pan hot first
5:30 The list

List note: link to her own note only.
Disclosure: none. This video was not paid.

**Cut**
viral hack, weight loss dinner, must try. She has no source for those.

## Anti-patterns

- Invented timestamps
- Keyword stuffing
- A sponsor hidden from the description

## Related skills

- `sponsorship-disclosure`
- `youtube-video-outline`
