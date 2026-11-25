---
name: kill-the-idea
description: "Write the criteria that would stop the idea, before more money is spent. Use when the user mentions kill criteria, when do we stop, walk away, stop the idea, or asks for a kill note. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'kill-the-idea' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Kill Criteria

Write the criteria that would stop the idea, before more money is spent.

## When to use this skill

Use this skill when the user:

- kill criteria
- when do we stop
- walk away
- stop the idea

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
- The spend so far
- The test
- The result that means stop

## Workflow


### 1. Step 1

Write the stop line before the test if they can.
### 2. Step 2

Use a result they can observe.
### 3. Step 3

Include the spend they will not pass.
### 4. Step 4

Do not move the line after a weak result.
### 5. Step 5

Say who decides.
### 6. Step 6

A kill note is allowed to say stop.

## Output

Deliver a **kill note**.

- Purpose of this kill note, in two sentences.
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

Before the week started, Mara said she would stop the permit-app idea if five owners would not pay. She asked five. All five said no. A note from her friend says ask five more.

### Example data

```text
idea: permit app
line she set: stop if 5 owners will not pay
result: 5 asked, 5 no, 18 Sep 2026
spend so far: one evening
friend: ask 5 more
who decides: Mara Chen
```

### Example outcome

**Kill note**
Stop. The line was five noes. She has five noes.
Do not add five more. The line does not move after the miss.
Spend so far: one evening. Do not add the free week.
Who decides: Mara. The friend does not get a vote that rewrites the line.

## Anti-patterns

- A line moved after a miss
- A vanity metric as the only test
- No person who can stop it

## Related skills

- `idea-screen`
- `runway-choice`
