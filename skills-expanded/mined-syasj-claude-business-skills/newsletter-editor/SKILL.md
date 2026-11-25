---
name: newsletter-editor
description: "Edit a newsletter so each issue has one idea, true links, and a reason to exist. Use when the user mentions edit a newsletter, newsletter review, email newsletter, company newsletter, or asks for a newsletter edit. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'newsletter-editor' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Newsletter Editor

Edit a newsletter so each issue has one idea, true links, and a reason to exist.

## When to use this skill

Use this skill when the user:

- edit a newsletter
- newsletter review
- email newsletter
- company newsletter

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

- The draft
- The reader
- The one idea
- Links and claims

## Workflow


### 1. Reason

Why this issue exists this week. If there is no reason, recommend skipping the send.
### 2. One idea

Cut items that do not serve it. A link dump is a finding.
### 3. Claims and links

Check that each link matches the description and each claim has a source. Do not invent a quote.
### 4. Subject line

It matches the content. No bait.
### 5. Skim

A reader on a phone can see the point in the first lines.
### 6. Ask

At most one ask, clearly marked.

## Output

Deliver a **newsletter edit**.

- Purpose of this newsletter edit, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a newsletter edit by 30 September 2026. A draft newsletter has seven unrelated links and a subject line promising a major announcement that is not in the body.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A draft newsletter has seven unrelated links and a subject line promising a major announcement that is not in the body.

The draft: one file, dated 14 September 2026. No earlier version attached for comparison
The reader: Lena Ortiz plus two others named in the thread. No distribution list attached
The one idea: A draft newsletter has seven unrelated links and a subject line promising a major announcement that is not in the body. Stated once, in the ask. Not written down anywhere else
Links and claims: the draft sentence is broader than the note
```

### Example outcome

**Newsletter edit**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Either adds the real announcement or rewrites the subject, and cuts the issue to one idea.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The draft | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| The reader | Lena Ortiz plus two others named in the thread. No distribution list attached | Carried into the draft |
| The one idea | A draft newsletter has seven unrelated links and a subject line promising a major announcement that is not in the body. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Links and claims | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Reason**  
Why this issue exists this week. If there is no reason, recommend skipping the send.

**2. One idea**  
Cut items that do not serve it. A link dump is a finding.

**3. Claims and links**  
Check that each link matches the description and each claim has a source. Do not invent a quote.

**4. Subject line**  
It matches the content. No bait.

**5. Skim**  
A reader on a phone can see the point in the first lines.

**Deliberately not done**
- A subject line that misleads.
- Broken or misdescribed links left as an exercise.
- A weekly send with nothing to say.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A subject line that misleads.
- Broken or misdescribed links left as an exercise.
- A weekly send with nothing to say.

## Related skills

- `email-lifecycle`
- `brand-voice-guide`
