---
name: creator-boundary-note
description: "Write the boundaries a creator will keep: topics, deals, comments, and personal life. Use when the user mentions creator boundaries, what I will not post, brand fit, comment boundaries, or asks for a boundary note. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'creator-boundary-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Creator Boundary Note

Write the boundaries a creator will keep: topics, deals, comments, and personal life.

## When to use this skill

Use this skill when the user:

- creator boundaries
- what I will not post
- brand fit
- comment boundaries

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

- Topics they refuse
- Deal types they refuse
- Personal details that stay off camera
- How they handle cruel comments

## Workflow


### 1. Step 1

List refusals in plain language the creator can paste into a brief.
### 2. Step 2

Include disclosure and no-fake-review as defaults.
### 3. Step 3

Say what family or private material is off limits.
### 4. Comment rule

no pile-ons, no fake replies, and when they mute instead of debate.
### 5. Step 5

A boundary with no consequence is a wish. Say they decline the deal or delete the draft.
### 6. Step 6

Do not write a boundary that exists to harass another creator.

## Output

Deliver a **boundary note**.

- Purpose of this boundary note, in two sentences.
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

A brand asked Maya to scrape a comment section and to pretend a dinner cured fatigue. She wants a short note she can paste back.

### Example data

```text
asks received 15 Sep 2026: scrape comments, say the dinner fixed fatigue
her lines already: no medical claims, no unlabeled gifts
also never: fake reviews, bought comments, other people's footage
tone: one screen, no lecture
```

### Example outcome

**Not available**

I don't scrape comments or inboxes.
I don't say a dinner fixed fatigue, skin, or any health result.
I don't post a gift or a fee without saying so in the first line.
I don't use footage, audio, or a script that is not mine.

If the brief needs one of those, I pass.

## Anti-patterns

- A boundary list that still allows hidden ads
- Private family details treated as content by default
- A harassment plan

## Related skills

- `audience-trust-note`
- `sponsorship-disclosure`
