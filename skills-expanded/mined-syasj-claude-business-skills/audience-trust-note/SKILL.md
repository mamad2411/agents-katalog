---
name: audience-trust-note
description: "Review a creator's recent posts for trust gaps: undisclosed deals, recycled claims, and metrics they cannot show. Use when the user mentions audience trust, creator credibility, why is engagement down, trust review, or asks for a trust note. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'audience-trust-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Audience Trust Note

Review a creator's recent posts for trust gaps: undisclosed deals, recycled claims, and metrics they cannot show.

## When to use this skill

Use this skill when the user:

- audience trust
- creator credibility
- why is engagement down
- trust review

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

- Recent posts they described
- Deals in that period
- Claims they made
- Metrics they can export

## Workflow


### 1. Step 1

List claims that need proof the creator does not have.
### 2. Step 2

Match paid posts to disclosures. A miss is a finding.
### 3. Step 3

Use only metrics they exported. Do not invent a drop or a spike.
### 4. Step 4

Separate a content problem from a trust problem.
### 5. Recommend one repair

a correction, a disclosure, or a narrower claim.
### 6. Step 6

Do not advise buying engagement to hide a dip.

## Output

Deliver a **trust note**.

- Purpose of this trust note, in two sentences.
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

Maya wants a caption about how authentic her page is. In the last 30 days she posted three gifted items and did not say they were gifts. She has no analytics export for the dip she thinks she sees.

### Example data

```text
window: 15 August to 14 September 2026
gift posts with no disclosure: linen towel 22 Aug, knife 2 Sep, oil 9 Sep
fee posts: none in the window
claims: "my most honest month" in a draft caption
metrics export: not attached
ask: publish the authenticity caption tomorrow
```

### Example outcome

**Trust note**
Do not post the authenticity caption tomorrow.

| Post | Gap | Repair |
| --- | --- | --- |
| Towel, 22 Aug | Gift, no label | Add a gift note or take it down |
| Knife, 2 Sep | Gift, no label | Same |
| Oil, 9 Sep | Gift, no label | Same |

The dip is not a finding. No export was attached.
Repair: fix the three labels first. Then write about the work, not about being authentic.

## Anti-patterns

- Bought engagement
- A trust lecture with no specific post
- Invented analytics

## Related skills

- `sponsorship-disclosure`
- `creator-boundary-note`
