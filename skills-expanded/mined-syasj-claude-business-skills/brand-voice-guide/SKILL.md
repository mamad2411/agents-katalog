---
name: brand-voice-guide
description: "Write a short voice guide with examples of on-voice and off-voice lines for real situations. Use when the user mentions brand voice, tone of voice, writing style guide, how we sound, or asks for a brand voice guide. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'brand-voice-guide' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Brand Voice Guide

Write a short voice guide with examples of on-voice and off-voice lines for real situations.

## When to use this skill

Use this skill when the user:

- brand voice
- tone of voice
- writing style guide
- how we sound

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

- Audiences
- Words they already like or hate
- Situations: sales, support, incident, social
- Claims that are off limits

## Workflow


### 1. Principles

Three principles, each with a meaning. 'Be human' alone is not a principle.
### 2. Examples

For each situation, an on-voice line and an off-voice line. Examples do the teaching.
### 3. Vocabulary

Words to prefer and words to avoid, including hype and internal jargon.
### 4. Hard moments

How the voice handles an outage or a mistake. Calm and specific, not cute.
### 5. Claims

The voice guide points to substantiation. Wit does not excuse a false claim.
### 6. Length

Short enough that writers will use it. A 40-page guide will be ignored.

## Output

Deliver a **brand voice guide**.

- Purpose of this brand voice guide, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a brand voice guide by 30 September 2026. The current guide says 'be bold' and writers are producing unsupported superlatives.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The current guide says 'be bold' and writers are producing unsupported superlatives.

Audiences: people who already buy from Fieldnote
Words they already like or hate: Email to lapsed buyers and one other, both unconfirmed as of 14 September 2026
Situations: sales, support, incident, social: sales: in the file; support: not in the file; incident: open; social: in the file
Claims that are off limits: the draft sentence is broader than the note
```

### Example outcome

**Brand voice guide**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Replaces 'be bold' with examples, and bans superlatives that lack proof.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Audiences | people who already buy from Fieldnote | Needs confirmation |
| Words they already like or hate | Email to lapsed buyers and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Situations: sales, support, incident, social | sales: in the file; support: not in the file; incident: open; social: in the file | Carried into the draft |
| Claims that are off limits | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Principles**  
Three principles, each with a meaning. 'Be human' alone is not a principle.

**2. Examples**  
For each situation, an on-voice line and an off-voice line. Examples do the teaching.

**3. Vocabulary**  
Words to prefer and words to avoid, including hype and internal jargon.

**4. Hard moments**  
How the voice handles an outage or a mistake. Calm and specific, not cute.

**5. Claims**  
The voice guide points to substantiation. Wit does not excuse a false claim.

**Deliberately not done**
- Adjectives with no examples.
- A cute voice for an incident.
- Banning plain language in the name of brand.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Adjectives with no examples.
- A cute voice for an incident.
- Banning plain language in the name of brand.

## Related skills

- `messaging-house`
- `marketing-claims-review`
