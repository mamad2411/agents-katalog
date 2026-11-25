---
name: faceless-channel-concept
description: "Define a faceless channel that can be made from material the operator has the right to use. Use when the user mentions faceless channel, faceless YouTube, channel without showing my face, anonymous channel idea, or asks for a channel concept. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'faceless-channel-concept' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Faceless Channel Concept

Define a faceless channel that can be made from material the operator has the right to use.

## When to use this skill

Use this skill when the user:

- faceless channel
- faceless YouTube
- channel without showing my face
- anonymous channel idea

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

- The viewer job
- Source material they own or can license
- Time to produce
- Topics they must not fake

## Workflow


### 1. Step 1

The absence of a face is a production choice, not a license to copy.
### 2. Step 2

Name the viewer job and the episode shape.
### 3. List sources they own

their own footage, licensed clips, public-domain material they can identify, or original graphics.
### 4. Step 4

If the concept depends on downloading other creators' videos, stop and redesign.
### 5. Step 5

Write a promise the channel can keep without pretending a person is on camera who is not.
### 6. Step 6

Do not promise automated income.

## Output

Deliver a **channel concept**.

- Purpose of this channel concept, in two sentences.
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

Maya wants a second channel with no face, about grocery prices in Calgary. She can film her receipts and her kitchen counter. She cannot use supermarket ads or another creator's voice.

### Example data

```text
viewer: Calgary shopper comparing a week of dinners
assets she has rights to: her receipts, her counter, her voice if she wants it off-camera
assets she does not have: store ads, news charts, a cloned voice
cadence: one video a week, Sunday
name draft: Price Check Kitchen
```

### Example outcome

**Concept — Price Check Kitchen**
No face. Her counter, her receipts, her narration.

**Episode**
One week of dinners. The receipts on the counter. The total. What she would swap next week. No store logo she does not have the right to show.

**Voice**
Her own, off camera. No cloned voice. No other creator's read.

**Cadence**
Sunday. One video. She already shops Saturday.

**Not the concept**
Reuploaded ads. A chart from a news site. A voice that is not hers.

## Anti-patterns

- A channel built by reuploading others
- A fake on-camera persona of a real person
- An income promise

## Related skills

- `faceless-source-check`
- `faceless-episode-brief`
