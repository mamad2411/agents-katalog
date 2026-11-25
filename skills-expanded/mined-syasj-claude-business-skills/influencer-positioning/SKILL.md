---
name: influencer-positioning
description: "Position an influencer around one audience job and one proof point the creator can actually show. Use when the user mentions influencer positioning, personal brand, what should I be known for, creator niche, or asks for a positioning note. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'influencer-positioning' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Influencer Positioning

Position an influencer around one audience job and one proof point the creator can actually show.

## When to use this skill

Use this skill when the user:

- influencer positioning
- personal brand
- what should I be known for
- creator niche

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

- The audience and the job they hire the creator for
- Proof the creator already has
- Topics they will not cover
- Platforms they actually post on

## Workflow


### 1. Step 1

Name one audience and the job they want done, in the creator's words.
### 2. Step 2

Pick one proof point the creator can show this month. A vibe is not proof.
### 3. Step 3

Write a one-sentence position and a paragraph that agree with each other.
### 4. Step 4

List three topics that fit and three that do not.
### 5. Step 5

Say which platform is home and which are echoes.
### 6. Step 6

Do not invent follower counts, income, or a niche award.

## Output

Deliver a **positioning note**.

- Purpose of this positioning note, in two sentences.
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

Maya Brooks posts weeknight dinners for people in Calgary. A brand kit template told her to call the account 'everything wellness'. She has no nutrition credential and no wellness result she can show. She needs a position she can defend.

### Example data

```text
creator: Maya Brooks, Weeknight Table, Calgary
audience: people who need dinner on the table in 30 minutes after work
proof she can show: 18 dinner posts since May 2026, grocery list under $25, filmed in her own kitchen
platforms: Instagram home, TikTok echo, no YouTube yet
will not cover: medical claims, weight loss, supplements
follower export: 8,400 Instagram, 2,100 TikTok, pulled 12 September 2026
```

### Example outcome

**Position**
Weeknight dinners for Calgary cooks who have 30 minutes and one grocery bag.

**Proof this month**
The 18 dinner posts and the under-$25 list. Not a wellness result.

**Say**
I show the Tuesday dinner, the list, and the time on the clock.

**Do not say**
Everything wellness. Any health outcome. Any follower count that is not in the 12 September export.

**Topics that fit**
Sheet-pan dinners, one-pot dinners, a $25 list.

**Topics that do not fit**
Supplements, fasting, 'what I eat in a day' as health advice.

**Home**
Instagram. TikTok gets the same dinner, cut shorter. No second niche.

## Anti-patterns

- A niche so broad it is 'lifestyle'
- Invented follower counts
- Copying another creator's tagline

## Related skills

- `influencer-media-kit`
- `content-creator-week`
