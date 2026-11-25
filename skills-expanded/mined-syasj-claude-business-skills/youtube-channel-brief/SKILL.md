---
name: youtube-channel-brief
description: "Brief a YouTube channel around one viewer job, a repeatable episode shape, and a publishing promise the creator can keep. Use when the user mentions YouTube channel strategy, start a YouTube channel, channel brief, what should my channel be about, or asks for a channel brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'youtube-channel-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# YouTube Channel Brief

Brief a YouTube channel around one viewer job, a repeatable episode shape, and a publishing promise the creator can keep.

## When to use this skill

Use this skill when the user:

- YouTube channel strategy
- start a YouTube channel
- channel brief
- what should my channel be about

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

- The viewer and the job
- Episode length they can sustain
- How often they can publish
- Topics they refuse

## Workflow


### 1. Step 1

Name the viewer who would subscribe, not 'everyone who likes videos'.
### 2. Define one episode shape

problem, demonstration, result, next step.
### 3. Step 3

Set a cadence the creator can keep for eight weeks. A daily promise they cannot meet is a finding.
### 4. Pick the home shelf

tutorials, reviews, or a series. Do not copy a famous channel's format and claim it.
### 5. Step 5

Write the channel promise in one sentence.
### 6. Step 6

Do not invent watch hours, RPM, or a viral prediction.

## Output

Deliver a **channel brief**.

- Purpose of this channel brief, in two sentences.
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

Maya wants a YouTube channel and wrote '40 videos in September' on a planning card. She can film on Tuesday and Thursday evenings. She has not published a YouTube video yet.

### Example data

```text
viewer: Calgary home cook who decides dinner at 5 p.m.
job: leave with a dinner and a list
time she has: Tuesday and Thursday, 7 p.m. to 9 p.m.
length she can edit: 8 to 10 minutes
topics she refuses: weight loss, supplements
September plan in her notes: 40 videos
```

### Example outcome

**Channel brief — Weeknight Table**
Promise: one dinner, one list, under 10 minutes.

**Episode shape**
The clock starts. The list is on screen. She cooks. She plates. She says what she would change next time.

**Cadence she can keep**
Two videos a week for eight weeks. 16 videos, not 40.

**Shelf**
Tutorials. Not a copied 'day in the life' channel.

**Removed**
The 40-video September promise. Watch-hour and RPM guesses. None were in the file.

## Anti-patterns

- A daily cadence with no time
- A copied channel identity
- An RPM promise

## Related skills

- `youtube-video-outline`
- `content-batch-plan`
