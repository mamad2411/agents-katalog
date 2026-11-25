---
name: brand-deal-brief
description: "Brief a brand deal so the creative, the disclosure, and the usage are agreed before anyone films. Use when the user mentions brand deal, sponsorship brief, influencer collaboration, paid partnership brief, or asks for a deal brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'brand-deal-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Brand Deal Brief

Brief a brand deal so the creative, the disclosure, and the usage are agreed before anyone films.

## When to use this skill

Use this skill when the user:

- brand deal
- sponsorship brief
- influencer collaboration
- paid partnership brief

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

- The brand and the product they actually use or will test
- The deliverable
- The claim the brand wants
- The disclosure rule they must follow

## Workflow


### 1. Step 1

Write the audience outcome, not the brand's slogan.
### 2. Step 2

Limit claims to what the creator has tested or the brand can substantiate.
### 3. Step 3

Put the disclosure in the brief, not as a maybe.
### 4. Step 4

Define usage, exclusivity, and the kill date.
### 5. Step 5

Name who approves the cut.
### 6. Step 6

Refuse a brief that asks the creator to hide the payment or invent a result.

## Output

Deliver a **deal brief**.

- Purpose of this deal brief, in two sentences.
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

A skillet brand wants Maya to say the pan cleared her skin concern in three days and to leave the paid label off. She has cooked with the pan twice. She has not tested a skin claim. She needs a brief she can send back before she films.

### Example data

```text
brand: Hearth Pan, 26 cm skillet
product status: Maya cooked eggs and a chicken thigh in it, 8 and 10 September 2026
deliverable they asked for: 1 Reel
claim they asked for: cleared a skin concern in three days
disclosure they asked for: none
usage they asked for: organic plus ads, no end date
approval: brand review by 22 September 2026
```

### Example outcome

**Deal brief — Hearth Pan**
Audience outcome: show one Tuesday dinner in this pan. Not a skin result.

**Claim that can be filmed**
Eggs did not stick on 8 September. Chicken thigh on 10 September. That is the test. No skin claim.

**Disclosure**
Paid partnership, said in the first line and in the on-screen label. Not optional.

**Usage**
Organic on Maya's accounts for 30 days. Ads are out until a separate yes. No forever license.

**Approval**
Brand may check facts by 22 September. They do not get a hidden-ad cut.

**Do not film**
The three-day skin line. Any 'before and after'.

## Anti-patterns

- A hidden ad
- An untested medical or income claim
- Usage that lasts forever by default

## Related skills

- `sponsorship-disclosure`
- `marketing-claims-review`
