---
name: voiceover-read-script
description: "Write a voice-over script that can be read aloud, with breaths, and without copied prose. Use when the user mentions voice over script, narration script, read this aloud, VO script, or asks for a read script. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'voiceover-read-script' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Voice-Over Read Script

Write a voice-over script that can be read aloud, with breaths, and without copied prose.

## When to use this skill

Use this skill when the user:

- voice over script
- narration script
- read this aloud
- VO script

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
- The seconds or words available
- Facts that need a source
- Terms to say exactly

## Workflow


### 1. Write for the ear

short sentences, no stacked clauses.
### 2. Step 2

Mark a pause where the picture must catch up, if they described a picture.
### 3. Step 3

Facts that are not the user's get a source or come out.
### 4. Step 4

Do not transcribe a book, a lyric, or another video.
### 5. Step 5

Read the timing in the note. If it overruns, cut.
### 6. Step 6

Spell odd names as the user spelled them.

## Output

Deliver a **read script**.

- Purpose of this read script, in two sentences.
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

Maya needs the 45-second read for the receipt episode. She speaks in short sentences. The $52 total and the pharmacy exclusion have to be in the read.

### Example data

```text
seconds: 45
must include: $52 food, pharmacy excluded, this week only
must exclude: butter price, "out of control"
pace: short sentences
name: she does not say her name
```

### Example outcome

**Read — about 45 seconds**

Four stops this week. I put the receipts on the counter.

One stop was the pharmacy. That line is not food. It stays out of the total.

Food came to $52. That is these receipts, these dates. Not a city price. Not next week.

I'm not adding a price I can't point to on the paper.

**Check**
No butter line. No 'out of control'. No name.

## Anti-patterns

- A script copied from a book or video
- A wall of text with no pauses
- Unsourced claims in the narration

## Related skills

- `voiceover-brief`
- `faceless-episode-brief`
