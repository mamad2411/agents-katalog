---
name: faceless-source-check
description: "Check whether a faceless episode's script and visuals are cleared to publish. Use when the user mentions can I use this clip, source check, copyright check for a video, is this compile allowed, or asks for a source check. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'faceless-source-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Faceless Source Check

Check whether a faceless episode's script and visuals are cleared to publish.

## When to use this skill

Use this skill when the user:

- can I use this clip
- source check
- copyright check for a video
- is this compile allowed

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

- The script origin
- Each visual's origin
- Music origin
- What the operator owns

## Workflow


### 1. Step 1

List every asset.
### 2. Step 2

Owned, licensed, or public-domain with a citation can stay. Unknown is a cut.
### 3. Step 3

A 'fair use' hunch is not a clearance. Say counsel must answer that, and do not bless a compile of other creators.
### 4. Step 4

Music and voice need the same test.
### 5. Step 5

Do not suggest trimming a watermark or mirroring a video to dodge a match.
### 6. Step 6

The output is a pass, a cut list, or a stop.

## Output

Deliver a **source check**.

- Purpose of this source check, in two sentences.
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

Before she publishes, Maya's folder has her receipts, a photo of a store flyer she did not shoot, and a price she typed from memory.

### Example data

```text
receipts: hers, 10 to 14 Sep
flyer photo: torn from a store window, she did not get permission
typed price: "butter was $6.99", no receipt line
narration: her voice, recorded 20 Sep
music: none
```

### Example outcome

**Source check**

| Item | Use |
| --- | --- |
| Her receipts | yes |
| Her voice, 20 Sep | yes |
| Flyer photo | no — not hers to publish |
| Butter at $6.99 | no — memory, no line on a receipt |

Episode can publish only after the flyer and the butter line are out.
Do not replace them with a price from a website.

## Anti-patterns

- Watermark removal
- Mirroring to dodge a match
- A homemade fair-use blessing

## Related skills

- `faceless-episode-brief`
- `open-source-license-review`
