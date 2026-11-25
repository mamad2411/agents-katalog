---
name: tiktok-analytics-note
description: "Read a TikTok analytics paste the creator provides and recommend one honest test. Use when the user mentions TikTok analytics, TikTok insights, why did this flop, TikTok readout, or asks for a analytics note. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tiktok-analytics-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# TikTok Analytics Note

Read a TikTok analytics paste the creator provides and recommend one honest test.

## When to use this skill

Use this skill when the user:

- TikTok analytics
- TikTok insights
- why did this flop
- TikTok readout

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

- The figures they pasted
- The videos those figures belong to
- What was different about the outlier
- The next decision

## Workflow


### 1. Step 1

Use only the numbers they pasted.
### 2. Compare like with like

same length and same promise, if they have that.
### 3. Step 3

Do not declare the algorithm 'punished' them. Say what the export can and cannot show.
### 4. Recommend one test

hook, length, or topic.
### 5. Step 5

Ignore vanity totals that do not change the next video.
### 6. Step 6

Do not recommend fake comments, pods, or bought views.

## Output

Deliver a **analytics note**.

- Purpose of this analytics note, in two sentences.
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

Maya's chicken TikTok has more views than her other posts this week. She wants the note to say the hook 'went viral'. She exported the last 7 days only.

### Example data

```text
export: 14 Sep to 20 Sep 2026, 7 days
chicken post: 6,200 views, 210 likes, 4 comments
other posts that week: 800, 640, 700 views
average watch time: not in the export
follower change: +18
```

### Example outcome

**Analytics note**
The chicken post is larger than the other three in this 7-day file: 6,200 views against 800, 640, and 700.

Do not write 'went viral'. This export has no watch-time curve and no traffic source.
Follower change in the file: +18. That is the whole claim.
Next: if she wants to know whether the first second held people, she needs that chart. It is not here.

## Anti-patterns

- Bought views or comment pods
- An algorithm myth presented as fact
- A test of five changes at once

## Related skills

- `tiktok-hook-pack`
- `youtube-analytics-note`
