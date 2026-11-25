---
name: embargo-check
description: "Check whether an embargo still applies and who agreed to it. Use when the user mentions embargo, can we publish, press embargo, release time, or asks for a embargo note. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'embargo-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Embargo Check

Check whether an embargo still applies and who agreed to it.

## When to use this skill

Use this skill when the user:

- embargo
- can we publish
- press embargo
- release time

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate quotes, sources, or images. Label opinion. Do not draft impersonation or defamation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The document
- The embargo time
- Who agreed
- The clock now

## Workflow


### 1. Step 1

Record the embargo time in the zone they stated.
### 2. Step 2

Say whether this desk agreed.
### 3. Step 3

If they did not agree, do not invent an obligation, and do not help break a confidence they do hold.
### 4. Step 4

If the time has passed, say so.
### 5. Step 5

Do not publish early to beat a competitor if they agreed.
### 6. Step 6

Name the owner of the decision.

## Output

Deliver a **embargo note**.

- Purpose of this embargo note, in two sentences.
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

A utility release is embargoed until 10:00 ET Tuesday. The desk agreed in writing on Monday. It is 07:30 in Calgary on Tuesday. An editor wants to post now.

### Example data

```text
embargo: 10:00 ET, Tuesday 16 Sep 2026
desk agreed: yes, email 15 Sep 18:04
now: 07:30 America/Edmonton, Tuesday 16 Sep
ET offset they stated: ET is 2 hours ahead of MT
decision owner: Jonah Ellis
```

### Example outcome

**Embargo note**
Do not post.

07:30 MT is 09:30 ET. The embargo they agreed to lifts at 10:00 ET, which is 08:00 MT.
The desk agreed. Early is not available.
Owner: Jonah. Post at or after 08:00 MT if the story is ready, not before.

## Anti-patterns

- Publishing early after agreeing
- A guessed embargo
- No time zone

## Related skills

- `news-assignment`
- `pr-pitch`
