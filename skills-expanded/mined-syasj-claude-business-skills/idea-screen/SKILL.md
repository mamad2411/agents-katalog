---
name: idea-screen
description: "Screen a business idea against the customer, the proof, and the reason to stop. Use when the user mentions business idea, is this a business, idea screen, should we build this, or asks for a screen. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'idea-screen' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Idea Screen

Screen a business idea against the customer, the proof, and the reason to stop.

## When to use this skill

Use this skill when the user:

- business idea
- is this a business
- idea screen
- should we build this

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Startup advice is a set of choices, not a promise of funding or growth. Do not invent traction, customers, or investor interest.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The idea
- The customer
- Proof they have
- The cost of a week of work

## Workflow


### 1. Step 1

Name the customer.
### 2. Step 2

State the proof in hand.
### 3. Step 3

If the proof is zero, say so.
### 4. Step 4

Name one reason to stop.
### 5. Step 5

Do not score it with a fake matrix.
### 6. Step 6

Recommend a next test or a stop.

## Output

Deliver a **screen**.

- Purpose of this screen, in two sentences.
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

Mara's friend wants a permit app for every town. No owner has asked for it. A week of build would consume the only free week she has before the Harbor pilot.

### Example data

```text
idea: permit app for every town
customer named: none
proof: none
week cost: her only free week before the Harbor pilot, 16 Sep
friend's enthusiasm: high
```

### Example outcome

**Screen**
Stop, or talk to five owners first. Do not build this week.
Customer: none named. Proof: none.
The week is already claimed by the Harbor pilot. That is the cost.
No score. A market size would not fix the empty customer.
Reason to stop: no owner has asked, and the week is not free.

## Anti-patterns

- A weighted score with no data
- A market size as proof
- A build decision from excitement

## Related skills

- `assumption-map`
- `kill-the-idea`
