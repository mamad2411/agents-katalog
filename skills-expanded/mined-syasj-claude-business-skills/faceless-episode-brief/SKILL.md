---
name: faceless-episode-brief
description: "Brief one faceless episode with the narration point, the visuals, and the sources. Use when the user mentions faceless video brief, compilation episode, faceless script brief, episode without a host, or asks for a episode brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'faceless-episode-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Faceless Episode Brief

Brief one faceless episode with the narration point, the visuals, and the sources.

## When to use this skill

Use this skill when the user:

- faceless video brief
- compilation episode
- faceless script brief
- episode without a host

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

- The point of the episode
- Visuals they can use
- Narration facts and sources
- Length

## Workflow


### 1. Step 1

Write the point before the visuals.
### 2. Every visual needs a source note

owned, licensed, or original. Unknown is not usable.
### 3. Step 3

Narration must not read a book, article, or another video word for word.
### 4. Step 4

Do not invent a study or a quote to fill a gap.
### 5. Step 5

Plan on-screen citations for factual claims.
### 6. Step 6

If a visual is a stranger's face, ask whether they have permission. If not, cut it.

## Output

Deliver a **episode brief**.

- Purpose of this episode brief, in two sentences.
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

Sunday's episode is the week of 14 September. Maya has four receipts. She needs the shot list and the sentence the episode is allowed to say.

### Example data

```text
receipts: Co-op 10 Sep $18.40, Co-op 13 Sep $22.10, pharmacy 12 Sep $6.00 not food, market 14 Sep $11.50
food total she calculated: $52.00
claim she wanted: "Calgary groceries are out of control"
shots: counter only, no store interior
```

### Example outcome

**Episode brief — week of 14 September**
Sentence the episode may say: these four stops cost $52 for food. The pharmacy line is not food and stays out.

**Shots**
1. Four receipts, pharmacy folded under.
2. Food lines only, her finger on the totals.
3. Her sum: $52.00.
4. One swap she will try next week. She has not named it. Leave a blank, do not invent the swap.

**Do not say**
Calgary groceries are out of control. One week of her receipts is not that claim.
No store interior. No one else's chart.

## Anti-patterns

- A word-for-word read of someone else's work
- Visuals with no source
- A stranger's face used as decoration

## Related skills

- `faceless-channel-concept`
- `voiceover-read-script`
