---
name: tiktok-comment-reply
description: "Draft replies to TikTok comments that are useful, bounded, and free of fake engagement. Use when the user mentions reply to comments, TikTok replies, comment section, creator replies, or asks for a reply set. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tiktok-comment-reply' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# TikTok Comment Reply

Draft replies to TikTok comments that are useful, bounded, and free of fake engagement.

## When to use this skill

Use this skill when the user:

- reply to comments
- TikTok replies
- comment section
- creator replies

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

- The comments they pasted
- The video's actual point
- What they will not promise
- Tone

## Workflow


### 1. Step 1

Reply to real questions first.
### 2. Step 2

Correct a wrong assumption about the video without insulting the commenter.
### 3. Step 3

Do not draft fake comments from sock accounts.
### 4. Step 4

Do not ask people to comment a keyword to juice the video if the creator does not mean to answer.
### 5. Step 5

A sponsorship question gets the disclosure, not a dodge.
### 6. Step 6

Skip abuse. Do not draft a pile-on.

## Output

Deliver a **reply set**.

- Purpose of this reply set, in two sentences.
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

A commenter asked Maya if the chicken dinner is high-protein and safe for a medical diet. Another asked which store had the $18.40 total. She wants replies that don't bluff.

### Example data

```text
comment 1: "is this high protein / ok for my diet"
comment 2: "which store"
facts she has: Co-op receipt 10 Sep, $18.40; she is not a dietitian
tone: short, no argument
```

### Example outcome

**Replies**

Comment 1: I can't say. I'm not a dietitian, and I didn't calculate it.
Comment 2: Co-op, 10 September. The $18.40 is that receipt, not every store.

Do not reply with a protein number. She does not have one.

## Anti-patterns

- Fake accounts
- A bait keyword with no real answer
- A pile-on reply

## Related skills

- `audience-trust-note`
- `instagram-caption`
