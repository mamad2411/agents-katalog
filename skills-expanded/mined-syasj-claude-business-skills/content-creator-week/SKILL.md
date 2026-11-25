---
name: content-creator-week
description: "Plan a creator's week from the slots they can actually film, edit, and reply. Use when the user mentions content calendar creator, creator week, posting schedule, how do I batch content, or asks for a weekly creator plan. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'content-creator-week' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Creator Operating Week

Plan a creator's week from the slots they can actually film, edit, and reply.

## When to use this skill

Use this skill when the user:

- content calendar creator
- creator week
- posting schedule
- how do I batch content

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

- Available hours
- Platforms they will touch
- Pieces already filmed
- Replies they owe

## Workflow


### 1. Step 1

Start from hours, not from a guru's daily quota.
### 2. Step 2

Put filming, editing, and replies on the week as separate work.
### 3. Step 3

One hero piece can feed smaller cuts only if the creator will actually cut them.
### 4. Step 4

Leave a buffer. A full grid with no edit time will slip.
### 5. Step 5

Do not schedule a post that depends on footage they do not have rights to.
### 6. Step 6

Name the one metric they will look at, from an export, not a feeling.

## Output

Deliver a **weekly creator plan**.

- Purpose of this weekly creator plan, in two sentences.
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

Maya is planning 22 to 28 September. She can film two nights. She already has three timed dinners. She does not want a seventh post made of reposted memes.

### Example data

```text
week: 22 to 28 Sep 2026
film nights: Tue 23, Thu 25
dinners ready: chicken, chili, eggs
posts she wants: 7
meme folder: 12 images she did not make
```

### Example outcome

**Week**

| Day | Post | Source |
| --- | --- | --- |
| Tue | Chicken Reel | timed 11 Sep |
| Wed | List still, from the receipt | 10 Sep receipt |
| Thu | Eggs, 12 minutes | her timing note |
| Sat | Chili, cut down | 28 Aug video |
| Sun | Off | — |

Five posts, not seven. The meme folder is not a post. She did not make those images.
Tue and Thu are the only film nights. Wednesday and Saturday use material she already has.

## Anti-patterns

- A daily quota they cannot staff
- Repurposing footage they do not own
- A week with no edit time

## Related skills

- `content-batch-plan`
- `content-repurpose-map`
