---
name: video-storyboard
description: "Write a shot-by-shot visual storyboard for a video, naming what is on screen, the motion, and the audio for each shot. Use when the user mentions storyboard, video storyboard, shot list, scene by scene video, or asks for a video storyboard. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'video-storyboard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Video Storyboard

Write a shot-by-shot visual storyboard for a video, naming what is on screen, the motion, and the audio for each shot.

## When to use this skill

Use this skill when the user:

- storyboard
- video storyboard
- shot list
- scene by scene video
- visual script
- shot breakdown

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

- The video topic and goal
- The intended length
- The narration or script if they have it
- The style and on-screen text they want

## Workflow


### 1. Step 1

Break the video into scenes and each scene into shots. One shot = one camera moment.
### 2. For each shot

describe what the viewer sees (on-screen elements, text overlays, B-roll), the motion (pan, zoom, static, transition), and the audio (VO line, music cue, silence).
### 3. Step 3

Sync each shot to the narration or talking point it covers. A storyboard not tied to the VO cannot be edited.
### 4. Step 4

Flag shots that require footage the creator does not have, and suggest an alternative (B-roll, screen recording, graphic).
### 5. Step 5

Note the estimated duration per shot so the total stays in range.
### 6. Step 6

Do not claim a shot is achievable if it requires licensed footage, a real person's likeness, or a location the creator has not mentioned.

## Output

Deliver a **video storyboard**.

- Purpose of this video storyboard, in two sentences.
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

Maya Brooks, creator at Weeknight Table in Calgary, wants a 60-second explainer on compound interest. She has a rough script and needs it broken into shots she can actually film or build.

### Example data

```text
From: Maya Brooks, creator
Channel: Weeknight Table, Calgary
Target length: 60 seconds · Format: 16:9, YouTube

Rough script points:
  - savings accounts earn almost nothing
  - interest earns interest: that is compounding
  - $1,000 at 5% grows to about $1,629 over 10 years
  - time matters more than the starting amount
  - subscribe

Assets on hand: screen recording setup, Canva, own spreadsheet
Assets NOT on hand: stock footage licence, animation software
```

### Example outcome

**Video storyboard — "How compound interest works" (60s, 16:9)**
To: Maya Brooks, creator, Weeknight Table · Date: 14 September 2026

| # | Dur | On screen | Motion | Audio / VO |
| --- | ---: | --- | --- | --- |
| 1 | 3s | Title: **"Your $1,000 becomes $4,000 — without doing anything"**, dark background, coin graphics | Coins fade up from the lower edge | No VO. Music in. |
| 2 | 10s | Split frame: left, a piggy bank sitting still; right, empty | Left half fades in, then right, to set up the contrast | "Most people leave money in a savings account earning almost nothing. There's a way to make your money earn money." |
| 3 | 14s | Screen recording of your own spreadsheet. Year 1: $1,000 · Year 2: $1,050 · Year 3: $1,102.50. Formula bar visible. Overlay: **"5% annual interest"** | Rows animate in one at a time, on the VO beat | "Invest $1,000 at 5%. After year one you have $1,050. Year two, you earn interest on the $1,050 — not just the original thousand. That's compounding." |
| 4 | 12s | Bar chart, 10 years, $1,000 rising to about $1,629. Axes labelled. | Bars grow left to right | "Over 10 years that $1,000 grows to over $1,600, without you adding a dollar. Start earlier and the effect multiplies." |
| 5 | 12s | Three cards: $1K/10yr → ~$1,629 · $5K/10yr → ~$8,144 · $1K/30yr → ~$4,322. Footer: *"Illustrative. Rates vary."* | Cards slide in from the right | "Five thousand for ten years becomes over eight thousand. One thousand for thirty years becomes over four. The variable that matters most isn't the amount — it's time." |
| 6 | 9s | **"Subscribe for more money basics"** + channel logo | Logo fades in, subscribe button pulses | "Hit subscribe for more plain-English money explainers every week." Music out. |

**Total: 60 seconds.**

**What you need to build, and how — given your asset list**

| Shot | Source | Note |
| --- | --- | --- |
| 1 | Canva | You have no stock licence, so build the coin graphic rather than pulling footage. |
| 2 | Canva | Simple two-up illustration. No footage needed. |
| 3 | Your own screen recording | Use your own spreadsheet. Do not screen-record someone else's video. |
| 4 | Canva or Flourish | Both do animated bar charts without animation software. |
| 5 | Canva | Three-card template. |
| 6 | Your existing end card | Reuse. |

Every shot is achievable with the tools you listed. Nothing here needs the stock licence or animation software you said you do not have.

**Deliberately not done**
- No shot depends on licensed footage or another creator's video.
- No real person's likeness appears.
- The timings add to 60 seconds, not to 75 with the expectation of cutting later.

**Open items**
- The dollar figures are illustrative. Add the on-screen disclaimer in shot 5 and a sources note in the pinned comment.
- Confirm the 5% rate is the one you want to use before the VO is recorded; it appears in three shots.

Next: Maya Brooks by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A storyboard for someone else's footage
- A shot list with no audio note
- Timings that add up to more than the target length

## Related skills

- `youtube-video-outline`
- `instagram-story-sequence`
- `video-prompt-spec`
