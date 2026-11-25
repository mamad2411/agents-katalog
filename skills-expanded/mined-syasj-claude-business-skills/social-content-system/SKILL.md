---
name: social-content-system
description: "Set a social posting system that a real person can sustain, with review and no engagement bait. Use when the user mentions social media plan, posting system, LinkedIn plan, content cadence, or asks for a social system. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'social-content-system' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Social Content System

Set a social posting system that a real person can sustain, with review and no engagement bait.

## When to use this skill

Use this skill when the user:

- social media plan
- posting system
- LinkedIn plan
- content cadence

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

- Channels the company will actually maintain
- Themes tied to buyer questions
- Reviewer
- Topics that are off limits

## Workflow


### 1. Channel choice

Keep a channel only if someone owns replies. An unowned channel is a reputation risk.
### 2. Themes

Three themes from real buyer questions. Not a meme strategy by default.
### 3. Cadence

A cadence the owner can review. Fewer posts, higher truth.
### 4. Review

Who checks claims before posting. Executives are not exempt from review.
### 5. Replies

How comments are handled, including criticism. No fake accounts and no bought engagement.
### 6. Stop list

No impersonation, no fake reviews, no scraped personal details.

## Output

Deliver a **social system**.

- Purpose of this social system, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a social system by 30 September 2026. A founder wants two posts a day and has no reviewer for technical claims.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A founder wants two posts a day and has no reviewer for technical claims.

Channels the company will actually maintain: plain, for people who already know the context. No house guide attached
Themes tied to buyer questions: A founder wants two posts a day and has no reviewer for technical claims
Reviewer: Lena Ortiz. No second reviewer named
Topics that are off limits: Email to lapsed buyers and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Social system**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A system with a lower cadence, a named reviewer, and an explicit ban on fake engagement.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Channels the company will actually maintain | plain, for people who already know the context. No house guide attached | Needs confirmation |
| Themes tied to buyer questions | A founder wants two posts a day and has no reviewer for technical claims | Carried into the draft |
| Reviewer | Lena Ortiz. No second reviewer named | Carried into the draft |
| Topics that are off limits | Email to lapsed buyers and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Channel choice**  
Keep a channel only if someone owns replies. An unowned channel is a reputation risk.

**2. Themes**  
Three themes from real buyer questions. Not a meme strategy by default.

**3. Cadence**  
A cadence the owner can review. Fewer posts, higher truth.

**4. Review**  
Who checks claims before posting. Executives are not exempt from review.

**5. Replies**  
How comments are handled, including criticism. No fake accounts and no bought engagement.

**Deliberately not done**
- Bought engagement.
- Fake accounts.
- A cadence nobody can review.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Bought engagement.
- Fake accounts.
- A cadence nobody can review.

## Related skills

- `content-calendar`
- `brand-voice-guide`
