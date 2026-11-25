---
name: voiceover-rights-note
description: "Write the usage terms for a voice recording the speaker is willing to grant. Use when the user mentions voice over contract points, usage rights, can they use my voice, VO license, or asks for a rights note. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'voiceover-rights-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Voice-Over Rights Note

Write the usage terms for a voice recording the speaker is willing to grant.

## When to use this skill

Use this skill when the user:

- voice over contract points
- usage rights
- can they use my voice
- VO license

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

- Where the audio will appear
- How long
- Whether ads are included
- Whether AI training or a voice clone is in scope

## Workflow


### 1. Step 1

State the media, the territory if they named one, and the term.
### 2. Step 2

Ads and cutdowns are separate from one organic video unless the speaker included them.
### 3. Step 3

A voice clone or model training is off unless the speaker gives a clear yes. Default is no.
### 4. Step 4

Credit is stated if they asked for it.
### 5. Step 5

This note is not a finished contract. Counsel should review if money or a long term is involved.
### 6. Step 6

Do not help a buyer assume they own the speaker's voice forever.

## Output

Deliver a **rights note**.

- Purpose of this rights note, in two sentences.
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

A local grocer heard the receipt episode and asked to use Maya's voice in their radio ad. She has not agreed. She needs a note that says what they do not have.

### Example data

```text
recording: 21 Sep 2026, her voice, receipt episode
they asked: radio ad, all October, no fee discussed
what she granted so far: play on her own channel
clone: they asked if they could "match her voice" with a tool
```

### Example outcome

**Rights note**
The 21 September read may play on Maya's channel, in that episode.

Not granted: radio, ads, October, any other month, any edit that adds a store offer.
Not granted: a matched or cloned voice. She does not license that.

If they want the read in an ad, that is a new yes, a fee she sets, a date it ends, and her own voice only.
Until that yes is written, the answer is no.

## Anti-patterns

- A forever buyout slipped into a one-video job
- Voice cloning without a clear yes
- A note presented as a lawyer's contract

## Related skills

- `brand-deal-brief`
- `voiceover-brief`
