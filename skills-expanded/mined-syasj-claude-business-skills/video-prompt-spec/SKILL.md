---
name: video-prompt-spec
description: "Specify a video-generation prompt for a shot the user can describe, with motion and limits. Use when the user mentions video prompt, text to video, animate this, shot prompt, or asks for a video prompt. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'video-prompt-spec' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Video Prompt Spec

Specify a video-generation prompt for a shot the user can describe, with motion and limits.

## When to use this skill

Use this skill when the user:

- video prompt
- text to video
- animate this
- shot prompt

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

- The shot
- The motion
- The length
- What must not appear

## Workflow


### 1. Step 1

One shot per prompt. A whole episode is a storyboard, not one prompt.
### 2. Step 2

Describe the start frame and the motion.
### 3. Say what must stay consistent

object, color, or on-screen words.
### 4. Step 4

Ban copyrighted characters, a real person's likeness, and another creator's footage as the reference unless the user has rights and says so.
### 5. Step 5

Length matches the tool they named. If they named none, keep the shot short and say the tool is unknown.
### 6. Step 6

The result is a draft to review, not a cleared publish.

## Output

Deliver a **video prompt**.

- Purpose of this video prompt, in two sentences.
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

Maya wants a 4-second opener of receipts landing on a counter. She does not want her face generated, and she does not want a store interior the tool might invent.

### Example data

```text
length: 4 seconds
shot: receipts drop onto a wood counter, top-down
no: face, store interior, logos, cloned voice
on-screen text: none in the generated shot
use: opener only, her channel
```

### Example outcome

**Video spec**
4 seconds. Top-down. Blank wood counter. Four blank receipts land. No text. No face. No aisle. No logo.

Reject the clip if a face, a readable brand, or a store aisle appears.
No voice in this clip. Her real read stays a separate file.
This spec does not ask a tool to copy a living person.

## Anti-patterns

- A copyrighted character
- A real person's likeness
- One prompt for a whole stolen scene

## Related skills

- `image-prompt-spec`
- `faceless-visual-system`
