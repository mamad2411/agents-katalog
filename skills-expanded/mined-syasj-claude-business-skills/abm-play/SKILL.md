---
name: abm-play
description: "Design an account-based play for a short list of named accounts, with a reason for each account. Use when the user mentions ABM, account based marketing, target account campaign, named accounts, or asks for a account-based play. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'abm-play' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Account-Based Play

Design an account-based play for a short list of named accounts, with a reason for each account.

## When to use this skill

Use this skill when the user:

- ABM
- account based marketing
- target account campaign
- named accounts

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

- The named accounts and why they fit
- The buyer role
- The offer
- Sales ownership

## Workflow


### 1. Short list

A handful of accounts with a fit reason. A thousand-account 'ABM' list is just a list.
### 2. Reason

Why this account, why now, from evidence the user has. Do not invent intent scores.
### 3. Offer

Something useful to that buyer's job, not a generic newsletter.
### 4. Sales pact

A named seller owns the follow-up. Marketing does not spray and disappear.
### 5. Personalization limits

Use public, relevant facts. No creepy personal details.
### 6. Readout

What will be reviewed after the plays run. Meetings accepted is a clearer signal than impressions.

## Output

Deliver a **account-based play**.

- Purpose of this account-based play, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs an account-based play by 30 September 2026. Marketing built a 2,000-account ABM list from a bought spreadsheet and wants custom gifts for all of them.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Marketing built a 2,000-account ABM list from a bought spreadsheet and wants custom gifts for all of them.

The named accounts and why they fit: Marketing built a 2,000-account ABM list from a bought spreadsheet and wants custom gifts for all of them
The buyer role: Kite Freight
The offer: CAD 180, dates not set, cap not set
Sales ownership: Lena Ortiz, marketing lead
```

### Example outcome

**Account-based play**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Cuts to a short evidenced list, assigns sellers, and bans creepy personalization.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The named accounts and why they fit | Marketing built a 2,000-account ABM list from a bought spreadsheet and wants custom gifts for all of them | Needs confirmation |
| The buyer role | Kite Freight | Carried into the draft |
| The offer | CAD 180, dates not set, cap not set | Carried into the draft |
| Sales ownership | Lena Ortiz, marketing lead | Needs confirmation |

**How this draft was built**

**1. Short list**  
A handful of accounts with a fit reason. A thousand-account 'ABM' list is just a list.

**2. Reason**  
Why this account, why now, from evidence the user has. Do not invent intent scores.

**3. Offer**  
Something useful to that buyer's job, not a generic newsletter.

**4. Sales pact**  
A named seller owns the follow-up. Marketing does not spray and disappear.

**5. Personalization limits**  
Use public, relevant facts. No creepy personal details.

**Deliberately not done**
- Fake personalization.
- A huge list with no seller owner.
- Invented intent data.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Fake personalization.
- A huge list with no seller owner.
- Invented intent data.

## Related skills

- `account-plan`
- `campaign-brief`
