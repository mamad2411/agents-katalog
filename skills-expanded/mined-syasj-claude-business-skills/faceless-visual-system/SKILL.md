---
name: faceless-visual-system
description: "Define a repeatable visual system for a faceless channel so episodes look related without stealing a brand. Use when the user mentions faceless style, visual system, thumbnail system faceless, motion template, or asks for a visual system. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'faceless-visual-system' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Faceless Visual System

Define a repeatable visual system for a faceless channel so episodes look related without stealing a brand.

## When to use this skill

Use this skill when the user:

- faceless style
- visual system
- thumbnail system faceless
- motion template

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

- The mood they want
- Colors and type they can use
- Tools they already have
- Brands they must not imitate

## Workflow


### 1. Step 1

Choose a small set of type, color, and layout rules.
### 2. Step 2

Make a title-card pattern the operator can rebuild.
### 3. Step 3

Do not copy a known channel's thumbnail layout, logo, or lower third and call it inspiration.
### 4. Step 4

Stock or generated images need a note on what the operator may use.
### 5. Step 5

On-screen text must be readable and must not invent a claim.
### 6. Step 6

Write the file naming rule so editors do not mix uncleared clips into the system.

## Output

Deliver a **visual system**.

- Purpose of this visual system, in two sentences.
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

Maya's faceless channel has used three fonts and a different color each week. She wants a system she can repeat. She does not want a copied 'finance bro' caption look.

### Example data

```text
frame: counter, top-down
type she already owns: one sans she licensed in June
colors from her kitchen: paper bag brown, white receipt, black text
never on screen: another channel's lower third, a fake chart, a face she did not film
caption size: readable on a phone
```

### Example outcome

**Visual system**
Top-down counter. White receipt. Black type. Brown only as the bag in the shot, not as a graphic theme she has to draw.

Type: the sans she licensed in June. One size for totals, one for labels.
Lower third: her words, left, no copied bar.
Never: a chart she did not calculate, a face, another channel's caption skin.
If a week needs a number, it comes from a receipt in that episode.

## Anti-patterns

- A cloned channel look
- Uncleared clips in the template folder
- Unreadable text used as a style

## Related skills

- `faceless-channel-concept`
- `design-system-token`
