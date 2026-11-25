---
name: graphic-brief
description: "Write a visual design brief so a designer or image-generation tool has a complete spec before starting. Use when the user mentions graphic brief, design brief, visual brief, brief for a designer, or asks for a design brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'graphic-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Graphic Design Brief

Write a visual design brief so a designer or image-generation tool has a complete spec before starting.

## When to use this skill

Use this skill when the user:

- graphic brief
- design brief
- visual brief
- brief for a designer
- image brief
- illustration brief

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

- What the graphic is for (thumbnail, social post, report cover, ad)
- The message it must carry
- The audience
- Brand colors or reference images they can share
- Size and format requirements

## Workflow


### 1. State the graphic's job in one sentence

what must the viewer understand or do.
### 2. Step 2

Describe the subject, the hierarchy (what the eye hits first, second, third), and the mood.
### 3. Step 3

List the required text on the image, exactly as it should appear. Do not paraphrase; the brief is a spec.
### 4. Name any brand constraints

color hex codes, fonts, or logos that must appear.
### 5. Step 5

State the size, format, and where the image will be used, because a 1080x1080 Instagram post and a 16:9 YouTube thumbnail need different layouts.
### 6. What must not appear

a competitor's logo, a specific color associated with a rival, or a person's face if they have not consented.

## Output

Deliver a **design brief**.

- Purpose of this design brief, in two sentences.
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

Maya Brooks, creator at Weeknight Table in Calgary, needs a design brief by 30 September 2026. A creator needs a YouTube thumbnail for a video about saving $10,000 in a year.

### Example data

```text
From: Maya Brooks, creator
Organization: Weeknight Table, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A creator needs a YouTube thumbnail for a video about saving $10,000 in a year.

What the graphic is for (thumbnail, social post, report cover, ad): one file, dated 14 September 2026. No earlier version attached for comparison
The message it must carry: Tuesday dinner Reel, recorded 14 September 2026. No supporting file attached
The audience: people who already buy from Weeknight Table
Brand colors or reference images they can share: Tuesday dinner Reel and one other, both unconfirmed as of 14 September 2026
Size and format requirements: plain, for people who already know the context. No house guide attached
```

### Example outcome

**Design brief**
To: Maya Brooks, creator, Weeknight Table
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A brief: 1280x720px, text reads '$10,000 SAVED', bold white with black stroke, foreground is a piggy bank graphic on a bright green background, no face required, export as PNG, visual hierarchy: text first, graphic second.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What the graphic is for (thumbnail, social post, report cover, ad) | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| The message it must carry | Tuesday dinner Reel, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The audience | people who already buy from Weeknight Table | Carried into the draft |
| Brand colors or reference images they can share | Tuesday dinner Reel and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |
| Size and format requirements | plain, for people who already know the context. No house guide attached | Carried into the draft |

**How this draft was built**

**1. State the graphic's job in one sentence**  
what must the viewer understand or do.

**2. Describe the subject, the hierarchy (what the eye hits first, second, third), and the mood**

**3. List the required text on the image, exactly as it should appear. Do not paraphrase; the brief is a spec**

**4. Name any brand constraints**  
color hex codes, fonts, or logos that must appear.

**5. State the size, format, and where the image will be used, because a 1080x1080 Instagram post and a 16:9 YouTube thumbnail need different layouts**

**Deliberately not done**
- A brief that says 'make it look good' with no reference point.
- Colors described as 'something blue'.
- Missing size and output format.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Maya Brooks by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A brief that says 'make it look good' with no reference point
- Colors described as 'something blue'
- Missing size and output format

## Related skills

- `image-prompt-spec`
- `youtube-title-thumbnail`
- `presentation-structure`
