---
name: instagram-story-sequence
description: "Plan an Instagram story sequence with a beginning, a proof frame, and a single sticker ask. Use when the user mentions Instagram stories, story sequence, stories plan, story frames, or asks for a story sequence. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'instagram-story-sequence' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Instagram Story Sequence

Plan an Instagram story sequence with a beginning, a proof frame, and a single sticker ask.

## When to use this skill

Use this skill when the user:

- Instagram stories
- story sequence
- stories plan
- story frames

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

- The point of the sequence
- Frames they can shoot today
- The ask
- Disclosure if the sequence is paid

## Workflow


### 1. Step 1

Limit the sequence to frames they can shoot.
### 2. Step 2

Frame one states the point. A later frame proves it.
### 3. Step 3

One sticker or reply ask. A poll, a question, and a link is a finding.
### 4. Step 4

Paid sequences say so on an early frame, not only on the last.
### 5. Step 5

Do not plan a story that screenshots a private message without a clear yes from the sender.
### 6. Step 6

End on the ask or the payoff, not on a leftover trend frame.

## Output

Deliver a **story sequence**.

- Purpose of this story sequence, in two sentences.
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

Maya is posting three stories after the Reel. A viewer who only sees frame 1 still needs the time and the price. Nothing is gifted.

### Example data

```text
frames: 3
frame 1 must carry: 5:40 and $18.40
frame 2: the list
frame 3: the plate and the question she will answer
sticker: poll, "under 40 minutes?" 
gift or fee: none
```

### Example outcome

**Stories**

1. Clock and receipt. Text: 5:40 / $18.40. No poll yet.
2. List, three lines from the receipt. Text: this shop, this day.
3. Plate. Poll: under 40 minutes? Her note said 36. The poll is a question, not a promise that the viewer matches it.

No disclosure sticker. Not paid.
Do not put the price only on frame 3.

## Anti-patterns

- A private screenshot without consent
- Disclosure only on the last frame
- Three competing stickers

## Related skills

- `instagram-caption`
- `creator-boundary-note`
