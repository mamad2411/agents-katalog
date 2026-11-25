---
name: influencer-rate-card
description: "Draft a rate card from the creator's real deliverables and the prices they are willing to charge. Use when the user mentions rate card, influencer pricing, how much should I charge, media kit rates, or asks for a rate card draft. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'influencer-rate-card' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Influencer Rate Card

Draft a rate card from the creator's real deliverables and the prices they are willing to charge.

## When to use this skill

Use this skill when the user:

- rate card
- influencer pricing
- how much should I charge
- media kit rates

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

- Deliverables they will actually make
- Prices they authorize
- Usage limits they want
- What they will not sell

## Workflow


### 1. List deliverables as concrete outputs

one Reel, one story set, usage window.
### 2. Step 2

Use only prices the creator authorized. If they have no price, mark it unset. Do not invent a market rate.
### 3. State usage

organic post only, or paid amplification, and for how long.
### 4. Put exclusions on the card

no competitor slam, no fake review, no usage beyond the window.
### 5. Step 5

Separate a package from a custom quote so a brand cannot assume the cheap bundle includes ads.
### 6. Step 6

Label the card as the creator's asking terms, not a contract.

## Output

Deliver a **rate card draft**.

- Purpose of this rate card draft, in two sentences.
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

Maya wants a one-page rate card before a kitchen-tool brand asks. She will sell one Reel, three stories, and 30 days of organic use. She has not set a price. A template told her to print a 12 percent engagement rate. Her export does not show that.

### Example data

```text
deliverables she will make: 1 Reel, 3 stories, posted in one week
usage: organic on her accounts only, 30 days, no ads
exclusivity: no competing cookware brand for 14 days
prices she authorized: none yet
will not sell: fake review, before-after health claim, whitelisting
export 12 Sep 2026: Instagram 8,400 followers. Engagement rate not in the export.
```

### Example outcome

**Rate card — Weeknight Table**
Asking terms, not a contract. Prices blank until Maya writes them.

| Deliverable | What they get | Price |
| --- | --- | --- |
| Reel | 1 dinner video, her kitchen, her words | unset |
| Stories | 3 frames, same week as the Reel | unset |
| Usage | Organic only, 30 days, her accounts | included |
| Paid ads / whitelisting | Not offered | — |

Exclusions: no competitor slam, no result she has not cooked, no use after day 30.
Removed: 'engagement rate 12 percent'. It was not in the export.
Next: Maya writes the two prices before the card goes to a brand.

## Anti-patterns

- A borrowed rate from a bigger creator
- Usage rights left blank
- A fake average engagement rate

## Related skills

- `brand-deal-brief`
- `sponsorship-disclosure`
