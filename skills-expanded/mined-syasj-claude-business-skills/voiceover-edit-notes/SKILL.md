---
name: voiceover-edit-notes
description: "Write edit notes for a voice-over so the editor knows which breaths, mistakes, and levels to fix. Use when the user mentions voice over edit, audio notes, clean up the VO, narration edit, or asks for a edit notes. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'voiceover-edit-notes' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Voice-Over Edit Notes

Write edit notes for a voice-over so the editor knows which breaths, mistakes, and levels to fix.

## When to use this skill

Use this skill when the user:

- voice over edit
- audio notes
- clean up the VO
- narration edit

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

- The keeper takes
- Mistakes they heard
- Picture limits
- Music they are allowed to use

## Workflow


### 1. Step 1

Refer to takes by the file names they gave.
### 2. Step 2

Note specific lines to replace. Do not say 'make it better'.
### 3. Breaths and room tone

say what the listener should not notice, without asking the editor to fabricate words the speaker did not say.
### 4. Step 4

Music must be cleared. Do not suggest a popular song as a bed.
### 5. Levels

voice in front, music under, if music exists.
### 6. Step 6

Do not ask the editor to paste in another person's phrase to fix a flub.

## Output

Deliver a **edit notes**.

- Purpose of this edit notes, in two sentences.
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

Maya's editor friend is cutting the episode. He wants to move the $52 line next to a sigh so it sounds worse. She wants the total said once, plainly.

### Example data

```text
keeper take: take 2
bad line in take 2: she said "fifty-two" then corrected to "$52"
sigh: exists at 0:18, he wants it under the total
music: none
claim that must stay intact: this week, these receipts, not a city trend
```

### Example outcome

**Edit notes**
Use take 2. Cut the first 'fifty-two' and keep '$52'.
Do not park the sigh under the total. The total is a figure, not a sting.
Say the limit in her words: this week, these receipts. Do not cut that sentence out to make the $52 sound bigger.
No music. No flyer shot. No butter line.
Export name: 2026-09-21-price-check.

## Anti-patterns

- Fabricated words the speaker did not say
- An uncleared song bed
- Notes with no file names

## Related skills

- `voiceover-session-plan`
- `faceless-source-check`
