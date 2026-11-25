---
name: content-repurpose-map
description: "Map one original piece into smaller posts without stripping the context or hiding the source. Use when the user mentions repurpose content, turn a video into posts, content atomization, cross-post plan, or asks for a repurpose map. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'content-repurpose-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Content Repurpose Map

Map one original piece into smaller posts without stripping the context or hiding the source.

## When to use this skill

Use this skill when the user:

- repurpose content
- turn a video into posts
- content atomization
- cross-post plan

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

- The original piece they own
- The platforms
- What must stay attached, such as a disclosure
- Time to edit

## Workflow


### 1. Step 1

Start from a piece they own. If they do not own it, stop.
### 2. Step 2

Each cut must still make sense alone.
### 3. Step 3

Carry disclosures and credits into every cut.
### 4. Step 4

Do not tell them to reupload another creator's file with a new caption.
### 5. Step 5

Match the cut to the platform's shape. A 20-minute chapter is not a TikTok without a new point.
### 6. Step 6

Name the cuts they will not make because the context would be misleading.

## Output

Deliver a **repurpose map**.

- Purpose of this repurpose map, in two sentences.
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

Maya wants five posts from Thursday's chicken video, which she filmed. She also dropped a news clip into the folder that she did not shoot. She wants to know what she may cut.

### Example data

```text
owned: chicken video, filmed 18 Sep 2026, 8:02, her kitchen
not owned: 14-second news clip, downloaded, watermark still on it
cuts she hopes for: Reel, TikTok, 3 stories, a still, a list post
faces of other people: none in her video
```

### Example outcome

**Repurpose map**
Source: her 18 September video only.

| Cut | From her file | Out |
| --- | --- | --- |
| Reel | 0:20 to 1:10, pan | yes |
| TikTok | first 25 seconds | yes |
| 3 stories | clock, list, plate | yes |
| Still | receipt frame | yes |
| News clip | not her footage | no |

The news clip does not get a 'reaction' edit. It leaves the folder.

## Anti-patterns

- Reuploading someone else's file
- A cut that drops the sponsorship disclosure
- A misleading out-of-context clip

## Related skills

- `faceless-source-check`
- `content-creator-week`
