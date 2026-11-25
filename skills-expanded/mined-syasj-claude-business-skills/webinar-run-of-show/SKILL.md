---
name: webinar-run-of-show
description: "Plan a webinar that teaches one job and makes one honest ask. Use when the user mentions webinar plan, run of show, online event, workshop agenda, or asks for a webinar run of show. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'webinar-run-of-show' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Webinar Run of Show

Plan a webinar that teaches one job and makes one honest ask.

## When to use this skill

Use this skill when the user:

- webinar plan
- run of show
- online event
- workshop agenda

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

- The audience
- The one teaching goal
- Speakers
- The ask

## Workflow


### 1. Promise

The title matches the content. No bait title.
### 2. Run of show

Timed blocks, including questions. A 40-minute monologue is a finding.
### 3. Proof

Slides use only approved numbers. Mark missing numbers as gaps.
### 4. Ask

One next step at the end. Do not pretend the session is free of an ask if it is not.
### 5. Roles

Host, speaker, and the person watching questions. A demo backup if live product is involved.
### 6. Follow-up

The email after the session restates the teaching point, not only the pitch.

## Output

Deliver a **webinar run of show**.

- Purpose of this webinar run of show, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a webinar run of show by 30 September 2026. A webinar titled as a practical workshop is planned as a 45-minute product pitch.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A webinar titled as a practical workshop is planned as a 45-minute product pitch.

The audience: people who already buy from Fieldnote
The one teaching goal: A webinar titled as a practical workshop is planned as a 45-minute product pitch. Stated once, in the ask. Not written down anywhere else
Speakers: Fall service page. Partly documented: the what is written down, the who is not
The ask: A webinar titled as a practical workshop is planned as a 45-minute product pitch. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Webinar run of show**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Either retitles the session or replaces half the pitch with the promised practice.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The audience | people who already buy from Fieldnote | Needs confirmation |
| The one teaching goal | A webinar titled as a practical workshop is planned as a 45-minute product pitch. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Speakers | Fall service page. Partly documented: the what is written down, the who is not | Carried into the draft |
| The ask | A webinar titled as a practical workshop is planned as a 45-minute product pitch. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Promise**  
The title matches the content. No bait title.

**2. Run of show**  
Timed blocks, including questions. A 40-minute monologue is a finding.

**3. Proof**  
Slides use only approved numbers. Mark missing numbers as gaps.

**4. Ask**  
One next step at the end. Do not pretend the session is free of an ask if it is not.

**5. Roles**  
Host, speaker, and the person watching questions. A demo backup if live product is involved.

**Deliberately not done**
- A bait-and-switch title.
- Unapproved metrics on slides.
- No time for questions in a session that promised them.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A bait-and-switch title.
- Unapproved metrics on slides.
- No time for questions in a session that promised them.

## Related skills

- `campaign-brief`
- `workshop-facilitation`
