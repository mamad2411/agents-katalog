---
name: corporate-narrative
description: "Write the company story employees and customers can repeat without sliding into hype. Use when the user mentions company narrative, our story, why we exist, elevator pitch for the company, or asks for a corporate narrative. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'corporate-narrative' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Corporate Narrative

Write the company story employees and customers can repeat without sliding into hype.

## When to use this skill

Use this skill when the user:

- company narrative
- our story
- why we exist
- elevator pitch for the company
- narrative memo

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Who the company serves
- The problem in the customer's language
- Proof points the user can stand behind
- What the company refuses to claim

## Workflow


### 1. Start with the customer

The first lines describe the customer's tension, not the founding myth.
### 2. State the change

What is different because the company exists. One change, not a list of values.
### 3. Add proof

Two proof points the user supplied. If proof is thin, write a humbler story rather than borrowing fake logos.
### 4. Write three lengths

A sentence, a paragraph, and a half page. They must agree with each other.
### 5. Remove hype

Delete 'revolutionary,' 'unique,' and unearned category claims. Specific beats grand.
### 6. Note the audience

Offer a variant for employees if the user needs one, focused on how daily work connects to the change.

## Output

Deliver a **corporate narrative**.

- Purpose of this corporate narrative, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a corporate narrative by 30 September 2026. A team has five conflicting About pages and wants one narrative before a launch.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A team has five conflicting About pages and wants one narrative before a launch.

Who the company serves: Mara Chen, founder
The problem in the customer's language: A team has five conflicting About pages and wants one narrative before a launch. Stated once, in the ask. Not written down anywhere else
Proof points the user can stand behind: one customer email, 14 September 2026, no attachment beyond that
What the company refuses to claim: the draft sentence is broader than the note
```

### Example outcome

**Corporate narrative**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Share one customer change and only the proof the user provided.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Who the company serves | Mara Chen, founder | Needs confirmation |
| The problem in the customer's language | A team has five conflicting About pages and wants one narrative before a launch. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Proof points the user can stand behind | one customer email, 14 September 2026, no attachment beyond that | Carried into the draft |
| What the company refuses to claim | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Start with the customer**  
The first lines describe the customer's tension, not the founding myth.

**2. State the change**  
What is different because the company exists. One change, not a list of values.

**3. Add proof**  
Two proof points the user supplied. If proof is thin, write a humbler story rather than borrowing fake logos.

**4. Write three lengths**  
A sentence, a paragraph, and a half page. They must agree with each other.

**5. Remove hype**  
Delete 'revolutionary,' 'unique,' and unearned category claims. Specific beats grand.

**Deliberately not done**
- A founding story that never mentions the customer.
- Claims of market leadership without evidence.
- A different story for every channel.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A founding story that never mentions the customer.
- Claims of market leadership without evidence.
- A different story for every channel.

## Related skills

- `positioning-statement`
- `messaging-house`
- `brand-voice-guide`
