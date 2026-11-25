---
name: youtube-retention-pass
description: "Review a YouTube edit plan for the moments viewers would leave, using the creator's own cut or notes. Use when the user mentions YouTube retention, edit for retention, why do people leave, retention pass, or asks for a retention notes. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'youtube-retention-pass' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# YouTube Retention Pass

Review a YouTube edit plan for the moments viewers would leave, using the creator's own cut or notes.

## When to use this skill

Use this skill when the user:

- YouTube retention
- edit for retention
- why do people leave
- retention pass

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

- The outline or a description of the cut
- The promise in the title
- Known slow sections
- What the creator measured if anything

## Workflow


### 1. Step 1

Compare the opening to the title. A mismatch is the first cut.
### 2. Step 2

Mark sections that repeat or delay the promised payoff.
### 3. Step 3

Suggest a cut, a visual, or a shorter setup. Do not add fake stakes.
### 4. Step 4

If they have an analytics export, use only that. Do not invent a drop-off second.
### 5. Step 5

Keep one clear payoff. A retention trick that lies is a finding, not a technique.
### 6. Step 6

Do not tell them to steal a pacing trick by copying another video shot for shot.

## Output

Deliver a **retention notes**.

- Purpose of this retention notes, in two sentences.
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

Maya watched her last video with a notebook. She wrote that people left during a 70-second pantry tour and stayed when the pan was on screen. She does not have YouTube analytics access yet. She wants to know what to cut on the next cutdown.

### Example data

```text
video: chili, published 28 Aug 2026, 9:10 long
her notes: drop at the pantry tour, 1:10 to 2:20; stay when the pot is on screen, 2:20 to 4:00
analytics export: none
next cut: Thursday chicken video, keep under 8:00
```

### Example outcome

**Retention pass**
Use her notebook. Do not invent a retention curve.

Cut: the pantry tour pattern. On the chicken video, do not spend 70 seconds showing the cupboard.
Keep: the pan-on-screen block. Start the clock there.
Open question: the 28 Aug drop size. No export, so do not write a percentage.
Next: Maya times the chicken cut so the cupboard is one sentence, not a tour.

## Anti-patterns

- Invented retention graphs
- A lie used as a hook
- A copied edit of someone else's video

## Related skills

- `youtube-title-thumbnail`
- `tiktok-hook-pack`
