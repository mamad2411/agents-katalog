---
name: image-prompt-spec
description: "Specify an image prompt from the scene the user can describe, without copying a living artist's name as a style lock. Use when the user mentions image prompt, picture prompt, generate an image, visual prompt, or asks for a image prompt. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'image-prompt-spec' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Image Prompt Spec

Specify an image prompt from the scene the user can describe, without copying a living artist's name as a style lock.

## When to use this skill

Use this skill when the user:

- image prompt
- picture prompt
- generate an image
- visual prompt

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

- The subject
- The use of the image
- Text that must appear, if any
- References they have rights to

## Workflow


### 1. Step 1

Describe the subject, the action, and the frame in plain words.
### 2. Say the image's job

thumbnail, story frame, or internal mock.
### 3. Step 3

Do not name a living artist as the style to copy. Describe light, lens, and palette instead.
### 4. Step 4

Do not ask for a real private person's face. A public figure impersonation is out.
### 5. Step 5

Text in the image must be short and spelled.
### 6. Step 6

Note what the user still has to check before publishing, including trademarks.

## Output

Deliver a **image prompt**.

- Purpose of this image prompt, in two sentences.
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

Maya needs a thumbnail image for the faceless channel. She wants the counter and the receipts. She does not want a famous cook's face or a store logo.

### Example data

```text
use: thumbnail, her channel
must show: paper receipts on a wood counter, top-down, no face
must not show: a real person's face, a store logo, a copied lower-third
text in image: $52
style references: none she has rights to
```

### Example outcome

**Image spec**
Top-down wood counter. Four paper receipts. Black text "$52" on one corner. No face. No logo. No hands unless they are unspecified and not a real person.

Do not name another creator, a film, or a brand as the style.
If the tool adds a logo or a face, reject the image and say what it added.
Text check: the only number is $52, matching her food total.

## Anti-patterns

- A living artist's name as the style
- A real person's face without a clear rights note
- A trademark treated as a prop

## Related skills

- `youtube-title-thumbnail`
- `prompt-boundary-check`
