---
name: instagram-collab-brief
description: "Brief an Instagram collaboration so both creators know the work, the credit, and what is not allowed. Use when the user mentions Instagram collab, creator collaboration, collab post, joint Reel, or asks for a collab brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'instagram-collab-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Instagram Collab Brief

Brief an Instagram collaboration so both creators know the work, the credit, and what is not allowed.

## When to use this skill

Use this skill when the user:

- Instagram collab
- creator collaboration
- collab post
- joint Reel

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

- Both creators' roles
- The asset
- Credit and usage
- What each person refuses

## Workflow


### 1. Step 1

State who films, who edits, and who posts.
### 2. Step 2

Write the credit in the caption and on screen if they asked for that.
### 3. Step 3

Usage is limited to what both people approved.
### 4. Step 4

Do not plan a collab that uses a third person's likeness or content without permission.
### 5. Step 5

Disclosure applies if either side is paid.
### 6. Agree the kill term

either person can stop the post if the cut misrepresents them.

## Output

Deliver a **collab brief**.

- Purpose of this collab brief, in two sentences.
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

A Calgary baker wants to appear in Maya's dinner Reel for 10 seconds, handing over bread. They have not agreed who posts, who approves, or whether the baker's flour brand is a paid mention.

### Example data

```text
guest: Jon Ellis, Ellis Bread, Calgary
shot: hands over one loaf, 10 seconds
flour brand: Jon was given flour, he has not said it is paid
who posts: not agreed
approval: both want to see the cut
date: film Thu 25 Sep, 7:30 p.m.
```

### Example outcome

**Collab brief**
Shot: Jon hands Maya one loaf. 10 seconds. Then he is out of frame.

Credit: his name and Ellis Bread on screen for that shot, and in the caption.
Who posts: Maya's account only, unless Jon says he will post too. He has not.
Paid flour: not in this Reel. Jon has not said the flour is a paid placement. Do not mention the flour brand.
Approval: both see the cut before 27 September. Either can pull their face.
If the flour becomes a paid mention, this brief stops and a disclosure brief starts.

## Anti-patterns

- One creator using the other's audience beyond the agreement
- A paid collab with no disclosure
- A third person's content used as filler

## Related skills

- `brand-deal-brief`
- `voiceover-rights-note`
