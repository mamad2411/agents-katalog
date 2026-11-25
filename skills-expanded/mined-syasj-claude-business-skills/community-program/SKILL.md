---
name: community-program
description: "Design a community program with a member job-to-be-done, moderation, and no vanity member count. Use when the user mentions community program, user group, community strategy, forum plan, or asks for a community program brief. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'community-program' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Community Program

Design a community program with a member job-to-be-done, moderation, and no vanity member count.

## When to use this skill

Use this skill when the user:

- community program
- user group
- community strategy
- forum plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent testimonials, reviews, metrics, or claims the user cannot support. Do not draft spam, cloaking, fake scarcity, or impersonation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Why members would participate
- Who will moderate
- The offer to members
- Topics that are out of bounds

## Workflow


### 1. Member job

What a member can do in the community that they cannot do alone. If the answer is 'hear from us', it is a newsletter, not a community.
### 2. Moderation

A named moderator and a simple code of conduct. No program without moderation.
### 3. Programming

A small rhythm of useful sessions. Do not promise daily activity you cannot host.
### 4. Measures

Quality of participation, not a vanity member total.
### 5. Safety

How harassment and spam are handled. No doxxing, no scraping members.
### 6. Honesty

Do not promise customers influence you will not give them.

## Output

Deliver a **community program brief**.

- Purpose of this community program brief, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a community program brief by 30 September 2026. Leadership wants a community so marketing can email the members every day.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Leadership wants a community so marketing can email the members every day.

Why members would participate: Leadership wants a community so marketing can email the members every day
Who will moderate: Lena Ortiz, marketing lead
The offer to members: CAD 120, dates not set, cap not set
Topics that are out of bounds: Email to lapsed buyers and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Community program brief**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Either redesigns it around a member job or calls it a newsletter, with moderation required for a real community.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Why members would participate | Leadership wants a community so marketing can email the members every day | Needs confirmation |
| Who will moderate | Lena Ortiz, marketing lead | Carried into the draft |
| The offer to members | CAD 120, dates not set, cap not set | Carried into the draft |
| Topics that are out of bounds | Email to lapsed buyers and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Member job**  
What a member can do in the community that they cannot do alone. If the answer is 'hear from us', it is a newsletter, not a community.

**2. Moderation**  
A named moderator and a simple code of conduct. No program without moderation.

**3. Programming**  
A small rhythm of useful sessions. Do not promise daily activity you cannot host.

**4. Measures**  
Quality of participation, not a vanity member total.

**5. Safety**  
How harassment and spam are handled. No doxxing, no scraping members.

**Deliberately not done**
- A community that is only a broadcast channel.
- No moderator.
- Scraping member data for ads.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A community that is only a broadcast channel.
- No moderator.
- Scraping member data for ads.

## Related skills

- `newsletter-editor`
- `brand-voice-guide`
