---
name: discovery-call
description: "Plan and review a discovery call that uncovers the buyer's problem, timing, and authority without pitching over them. Use when the user mentions discovery call, first sales call, qualify a lead, what should I ask the buyer, or asks for a discovery call plan or review. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'discovery-call' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Discovery Call

Plan and review a discovery call that uncovers the buyer's problem, timing, and authority without pitching over them.

## When to use this skill

Use this skill when the user:

- discovery call
- first sales call
- qualify a lead
- what should I ask the buyer

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What you already know about the account
- The meeting length
- The offer you might eventually discuss
- Any claim you must not make

## Workflow


### 1. Open on their world

Start with why they took the meeting, in their words, before any product tour.
### 2. Problem evidence

Ask what the problem costs in time, money, or risk, and what they have already tried.
### 3. Timing

Find the event that makes this urgent now. No event means a nurture, not a forecast commit.
### 4. People

Who feels the pain, who signs, and who can block. Do not invent a champion.
### 5. Next step

End with a specific next step the buyer accepts. A vague 'I'll send something' is a miss.
### 6. Notes

Record facts separately from your interpretation. Do not log personal data you do not need.

## Output

Deliver a **discovery call plan or review**.

- Purpose of this discovery call plan or review, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a discovery call plan or review by 30 September 2026. A salesperson has 30 minutes with an operations lead and usually spends 25 of them on slides.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A salesperson has 30 minutes with an operations lead and usually spends 25 of them on slides.

What you already know about the account: 25 in the last period. No prior period attached, so no trend
The meeting length: plain, for people who already know the context. No house guide attached
The offer you might eventually discuss: CAD 120, dates not set, cap not set
Any claim you must not make: the draft sentence is broader than the note
```

### Example outcome

**Discovery call plan or review**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Separates facts from guesses.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What you already know about the account | 25 in the last period. No prior period attached, so no trend | Needs confirmation |
| The meeting length | plain, for people who already know the context. No house guide attached | Carried into the draft |
| The offer you might eventually discuss | CAD 120, dates not set, cap not set | Carried into the draft |
| Any claim you must not make | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Open on their world**  
Start with why they took the meeting, in their words, before any product tour.

**2. Problem evidence**  
Ask what the problem costs in time, money, or risk, and what they have already tried.

**3. Timing**  
Find the event that makes this urgent now. No event means a nurture, not a forecast commit.

**4. People**  
Who feels the pain, who signs, and who can block. Do not invent a champion.

**5. Next step**  
End with a specific next step the buyer accepts. A vague 'I'll send something' is a miss.

**Deliberately not done**
- A twenty-minute monologue about the product.
- Scoring a buyer as qualified because they were polite.
- Inventing a budget they never stated.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A twenty-minute monologue about the product.
- Scoring a buyer as qualified because they were polite.
- Inventing a budget they never stated.

## Related skills

- `qualification-meddic`
- `demo-storyboard`
