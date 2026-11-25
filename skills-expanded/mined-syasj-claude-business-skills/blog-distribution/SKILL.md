---
name: blog-distribution
description: "Say where a finished post goes, based on channels the writer actually has. Use when the user mentions distribute this post, blog promotion, where to share a post, republish, or asks for a distribution note. Blog and editorial skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: blog
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'blog-distribution' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Blog Distribution

Say where a finished post goes, based on channels the writer actually has.

## When to use this skill

Use this skill when the user:

- distribute this post
- blog promotion
- where to share a post
- republish

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not copy another publication's article. Do not invent sources, quotes, or results. Label an update when a post is refreshed.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The live URL
- Channels they control
- A partner who has agreed
- Places they must not paste the whole post

## Workflow


### 1. Step 1

List channels they control.
### 2. Step 2

Put the link, not a full copy, on channels that are not theirs.
### 3. Step 3

A partner share needs a yes already in the file.
### 4. Step 4

Do not buy reposts.
### 5. Step 5

Match the disclosure if the post is paid.
### 6. Step 6

Set one day, not a spam burst.

## Output

Deliver a **distribution note**.

- Purpose of this distribution note, in two sentences.
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

The grocery post is live. A plan says email Maya's list, paste the full text into a neighbourhood Facebook group she does not run, and tag a grocer who has not replied.

### Example data

```text
url: weeknighttable.example/week-of-14-sep
channels she controls: her email list, 420 people, her Instagram
partner yes: none
group: neighbourhood Facebook group, she is not a moderator
grocer: no reply to her 12 Sep note
paid: no
```

### Example outcome

**Distribution**
Email the list once, with the link.
Instagram: the link and the $52 line she can support. Not the full post pasted as a new article.
Do not paste the full text into the Facebook group.
Do not tag the grocer. There is no yes.
One day, 21 September. Not a burst across groups she does not run.

## Anti-patterns

- Pasting the full post onto someone else's site
- A partner named without a yes
- Bought shares

## Related skills

- `blog-assignment`
- `newsletter-editor`
