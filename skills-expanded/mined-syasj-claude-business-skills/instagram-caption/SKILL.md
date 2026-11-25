---
name: instagram-caption
description: "Write an Instagram caption that delivers the post's point and discloses any paid relationship. Use when the user mentions Instagram caption, write the caption, Reel caption, post copy, or asks for a caption. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'instagram-caption' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Instagram Caption

Write an Instagram caption that delivers the post's point and discloses any paid relationship.

## When to use this skill

Use this skill when the user:

- Instagram caption
- write the caption
- Reel caption
- post copy

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

- What the image or Reel actually shows
- The one point
- Sponsor or affiliate facts
- Length they want

## Workflow


### 1. Step 1

First line carries the point. Do not waste it on 'link in bio' unless that is the point.
### 2. Step 2

Match the caption to the picture. Do not describe a result the image does not show.
### 3. Step 3

Disclose payment, gifts, or affiliate links in the caption body.
### 4. Step 4

Hashtags are a few relevant labels, not a block of unrelated tags.
### 5. Step 5

Invite a real reply only if the creator will read it.
### 6. Step 6

Do not invent a quote from a customer.

## Output

Deliver a **caption**.

- Purpose of this caption, in two sentences.
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

Maya needs the caption for the unpaid chicken Reel. She writes short. She does not want hashtags she cannot explain. A friend told her to add #weightlossdinner.

### Example data

```text
paid: no
fact: 36 minutes, $18.40, Co-op, 10 and 11 Sep
voice: two short paragraphs
hashtags she was told to add: #weightlossdinner #viral
hashtags she actually uses: #yycfood #weeknightdinner
```

### Example outcome

**Caption**

Home at 5:40. Chicken at 6:20. I timed it on 11 September: 36 minutes.

List was $18.40 at Co-op on 10 September. Your total will not match mine.

#yycfood #weeknightdinner

**Left out**
#weightlossdinner and #viral. She has no fact for either. No disclosure line. Nothing was paid.

## Anti-patterns

- A caption that lies about the image
- Hidden affiliate links
- A fake customer quote

## Related skills

- `sponsorship-disclosure`
- `instagram-reel-brief`
