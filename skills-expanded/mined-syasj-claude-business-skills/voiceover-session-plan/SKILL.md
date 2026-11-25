---
name: voiceover-session-plan
description: "Plan a voice-over recording session with the script, the room, and the takes to keep. Use when the user mentions voice over session, recording plan, narration session, record the VO, or asks for a session plan. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'voiceover-session-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Voice-Over Session Plan

Plan a voice-over recording session with the script, the room, and the takes to keep.

## When to use this skill

Use this skill when the user:

- voice over session
- recording plan
- narration session
- record the VO

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

- The locked script
- The room they have
- The deadline
- File naming

## Workflow


### 1. Step 1

Lock the script before the session. A rewrite in the booth is a new session.
### 2. Note the room problems they already know

echo, street noise, and how they will reduce them without a gadget lecture.
### 3. Plan a slate

project, line, take.
### 4. Step 4

Record a safety take of any line with a name or a number.
### 5. Step 5

Do not record someone else's voice from a clip to 'blend it in'.
### 6. Step 6

End with which takes are keepers, named in the file, not left as 'the good one'.

## Output

Deliver a **session plan**.

- Purpose of this session plan, in two sentences.
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

Maya is recording Sunday at 9 a.m. in her kitchen. The fridge is loud. She wants three takes and a file name she can find later.

### Example data

```text
when: Sun 21 Sep 2026, 9:00 a.m.
room: kitchen
problem: fridge hum
takes: 3, then stop
save: her drive, folder Price Check, not a public link
mic: phone, the same one as last week
```

### Example outcome

**Session**
9:00 fridge off or move to the hall. Last week the hum sat under the whole read.
9:10 level check, one sentence.
9:15 three takes of the 45-second read. Stop. Do not do a twelfth take looking for a commercial voice.
9:30 label the keeper: 2026-09-21-price-check-take. The other two stay in the folder, not in the edit, unless the keeper has a misspoken total.
No public link. The file stays on her drive.

## Anti-patterns

- An unlocked script
- An unlabeled session
- A plan to mix in another person's recorded voice

## Related skills

- `voiceover-edit-notes`
- `voiceover-brief`
