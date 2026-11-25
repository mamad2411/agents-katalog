---
name: content-batch-plan
description: "Plan a batch filming day so the creator leaves with usable pieces, not a camera roll of half ideas. Use when the user mentions batch content, filming day, content batch, record a week of posts, or asks for a batch plan. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'content-batch-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Content Batch Plan

Plan a batch filming day so the creator leaves with usable pieces, not a camera roll of half ideas.

## When to use this skill

Use this skill when the user:

- batch content
- filming day
- content batch
- record a week of posts

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

- The pieces to film
- Location and wardrobe limits
- The shot list
- Energy and time

## Workflow


### 1. Step 1

Choose a few finished ideas, not a brainstorm on set.
### 2. Step 2

Group by setup so they are not rebuilding the frame every take.
### 3. Step 3

Each card has the line, the shot, and the thumbnail or cover.
### 4. Step 4

Plan water, breaks, and a hard stop.
### 5. Step 5

Label files before they leave the session.
### 6. Step 6

Do not add a last-minute impersonation or a copied sketch to 'use the light'.

## Output

Deliver a **batch plan**.

- Purpose of this batch plan, in two sentences.
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

Maya has Tuesday 7 to 9 p.m. She wrote six videos on the card. Setup for one dinner takes 20 minutes in her kitchen. She needs a batch she can actually finish and label.

### Example data

```text
block: Tue 23 Sep, 7:00 to 9:00 p.m.
setup: 20 minutes per dinner, her last three sessions
dinners prepped: chicken ingredients out; eggs not bought
card: 6 videos
labels she must write the same night: title and whether it is paid
```

### Example outcome

**Batch — Tuesday**
Two videos, not six.

7:00 setup chicken
7:20 film chicken Reel and the 25-second cut
8:10 label both: unpaid, title from her note, receipt fact checked
8:30 stop. Eggs are not in the house. Do not start a third setup.

Six videos would need three hours of setup before a single plate. The block is two hours.

## Anti-patterns

- Filming without a line
- Unlabeled files
- A copied sketch added on the day

## Related skills

- `content-creator-week`
- `youtube-video-outline`
