---
name: tiktok-short-script
description: "Write a TikTok script the creator can perform in the time they have, in their own voice. Use when the user mentions TikTok script, short script, 15 second script, 30 second script, or asks for a short script. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tiktok-short-script' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# TikTok Short Script

Write a TikTok script the creator can perform in the time they have, in their own voice.

## When to use this skill

Use this skill when the user:

- TikTok script
- short script
- 15 second script
- 30 second script

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
- The seconds available
- Words they actually use
- The visual they can shoot

## Workflow


### 1. Step 1

Fit the script to the seconds. Read it aloud in the note and cut if it does not fit.
### 2. Step 2

Use the creator's vocabulary. Do not paste a meme voice that is not theirs.
### 3. Step 3

One point, one proof, one ending.
### 4. Step 4

On-screen text is a support, not a second script that contradicts the voice.
### 5. Step 5

Do not include copyrighted lyrics or a copied monologue.
### 6. Step 6

Mark any claim that needs proof before filming.

## Output

Deliver a **short script**.

- Purpose of this short script, in two sentences.
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

Maya wants the words for the 25-second chicken TikTok. She talks the way she talks in her kitchen, short sentences. She will not read a joke from another account.

### Example data

```text
seconds: 25
beats she listed: clock, pan, list, plate
facts: 5:40, $18.40, 36 minutes on 11 Sep
voice: short sentences, no slang she does not use
words she rejected: "you won't believe", "hack"
```

### Example outcome

**Script — 25 seconds**

0:00 Clock. It is 5:40.
0:04 Pan on. High. Before the chicken.
0:10 Chicken in. This took 36 minutes on 11 September.
0:16 List. $18.40. That's this shop, this day.
0:21 Plate. Eat by 6:20 in my kitchen. Yours may differ.

No 'hack'. No 'you won't believe'. No other account's joke.

## Anti-patterns

- A script longer than the slot
- Copyrighted lyrics
- A copied monologue

## Related skills

- `tiktok-hook-pack`
- `voiceover-read-script`
