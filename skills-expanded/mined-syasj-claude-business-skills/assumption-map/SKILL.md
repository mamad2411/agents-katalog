---
name: assumption-map
description: "List the assumptions that would kill the idea if they are wrong, in the founder's words. Use when the user mentions assumption map, what has to be true, leap of faith, riskiest assumption, or asks for a assumption map. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'assumption-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Assumption Map

List the assumptions that would kill the idea if they are wrong, in the founder's words.

## When to use this skill

Use this skill when the user:

- assumption map
- what has to be true
- leap of faith
- riskiest assumption

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
- Assumptions they stated
- Which one they can test this week
- Evidence already in hand

## Workflow


### 1. Step 1

Write assumptions as sentences that can be false.
### 2. Step 2

Mark the one that kills the idea.
### 3. Step 3

Match it to a test they can run this week.
### 4. Step 4

Evidence in hand is labeled evidence.
### 5. Step 5

Do not add a market assumption they did not state.
### 6. Step 6

Leave the test result blank.

## Output

Deliver a **assumption map**.

- Purpose of this assumption map, in two sentences.
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

Mara says the idea dies if shop owners will not pay $49 a month. She has four who pay. She has not asked the six names on the whiteboard. A friend assumed the market is huge.

### Example data

```text
idea: Saturday list for independent shops
killer, her words: owners will not pay $49 a month
evidence: 4 pay
not tested: the 6 names with no conversation
friend's line: the market is huge
test she can run this week: ask 5 of the 6, yes or no on $49
```

### Example outcome

**Assumptions**
Killer: owners will not pay $49 a month. Her sentence.
Evidence: four pay. That is evidence for those four, not for the six.
Test this week: ask five of the six for a yes or no on $49. Result: blank until she asks.
Not on this map: 'the market is huge'. She did not state it, and it is not the killer.

## Anti-patterns

- A test result filled in early
- A dozen assumptions and no killer
- A survey of friends called proof

## Related skills

- `idea-screen`
- `beachhead-market`
