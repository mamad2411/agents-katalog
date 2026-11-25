---
name: voiceover-brief
description: "Brief a voice-over so the reader knows the listener, the tone, and the words that must not change. Use when the user mentions voice over brief, VO brief, narration brief, hire a voice, or asks for a voice-over brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'voiceover-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Voice-Over Brief

Brief a voice-over so the reader knows the listener, the tone, and the words that must not change.

## When to use this skill

Use this skill when the user:

- voice over brief
- VO brief
- narration brief
- hire a voice

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

- The listener
- The length
- Words that are legally or factually fixed
- Pronunciations

## Workflow


### 1. Step 1

State who is listening and what they should do or understand.
### 2. Step 2

Give the runtime. A 400-word script is not a 30-second ad.
### 3. Step 3

Mark lines that must be read as written.
### 4. Step 4

Give pronunciations for names the user supplied. Do not guess a person's name pronunciation and present it as fact.
### 5. Step 5

Tone is a few plain words plus one example line, not 'be epic'.
### 6. Step 6

Do not ask the reader to imitate a living person's voice.

## Output

Deliver a **voice-over brief**.

- Purpose of this voice-over brief, in two sentences.
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

Maya is hiring no one. She is reading a 45-second narration for the faceless episode. She needs the brief so the read stays inside her receipts.

### Example data

```text
reader: Maya, her own voice
length: 45 seconds
facts allowed: $52 food total, four stops, pharmacy excluded
facts not allowed: citywide price claims, butter $6.99
music: none
use: her channel only, this episode
```

### Example outcome

**Voice-over brief**
Reader: Maya. No other voice. No clone.

Length: 45 seconds. One take she can say without rushing.

May say: four stops, food total $52, pharmacy line excluded, her kitchen, this week.
May not say: a city price trend, the butter price, a store name as an ad.

Rights: her channel, this episode. Not a license for a brand to reuse the read.
If she later wants a paid reuse, that is a new note.

## Anti-patterns

- A request to clone a celebrity or a private person
- An impossible runtime
- A tone note with no example line

## Related skills

- `voiceover-read-script`
- `voiceover-rights-note`
