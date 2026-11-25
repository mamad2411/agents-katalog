---
name: tiktok-hook-pack
description: "Write TikTok hooks that the creator can say on camera and that the video will actually pay off. Use when the user mentions TikTok hooks, opening line, hook ideas, stop the scroll, or asks for a hook pack. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tiktok-hook-pack' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# TikTok Hook Pack

Write TikTok hooks that the creator can say on camera and that the video will actually pay off.

## When to use this skill

Use this skill when the user:

- TikTok hooks
- opening line
- hook ideas
- stop the scroll

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

- The video's real point
- The audience
- Lines they are willing to say
- Claims that are off limits

## Workflow


### 1. Step 1

Write the payoff in one sentence before any hook.
### 2. Step 2

Draft a few spoken hooks a real person would say.
### 3. Step 3

Each hook must be true of this video.
### 4. Step 4

Cut hooks that depend on a fake emergency, a fake income, or a copied sound gag the creator cannot clear.
### 5. Step 5

Note the on-screen text so it matches the spoken line.
### 6. Step 6

Pick one hook and the first visual.

## Output

Deliver a **hook pack**.

- Purpose of this hook pack, in two sentences.
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

Maya is cutting the chicken dinner into a 25-second TikTok. She wants three opening lines. She does not want to lip-sync a sound whose joke she does not control. Her first second on camera is the receipt and the clock.

### Example data

```text
length: 25 seconds
first image she can film: receipt and phone clock at 5:40
fact: $18.40, eat by 6:20, her 11 Sep timing
trend audio she mentioned: a sound she cannot explain
post date: 19 Sep 2026
```

### Example outcome

**Hooks she can say**
1. It is 5:40. Dinner is $18.40. Eat at 6:20.
2. Don't open the cupboard. Start the pan.
3. I timed this on 11 September. 36 minutes.

**Do not open with**
A sound she cannot explain. Another cook's line. A view-count promise.

On-screen text for hook 1: 5:40 / $18.40

## Anti-patterns

- A hook the video does not pay off
- A copied viral script
- Fake urgency

## Related skills

- `tiktok-short-script`
- `youtube-title-thumbnail`
