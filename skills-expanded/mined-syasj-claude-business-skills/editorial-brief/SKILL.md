---
name: editorial-brief
description: "Brief a story or communication with the reader, the news, and the sources that exist. Use when the user mentions editorial brief, story brief, comms brief, article brief, or asks for a editorial brief. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'editorial-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Editorial Brief

Brief a story or communication with the reader, the news, and the sources that exist.

## When to use this skill

Use this skill when the user:

- editorial brief
- story brief
- comms brief
- article brief

## When not to use this skill

- Fabricated quotes
- Impersonation

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

- The reader
- The news or point
- Sources on hand
- What is off the record

## Workflow


### 1. Step 1

Write the point in one sentence.
### 2. Step 2

List sources they have. Do not plan a quote you will invent.
### 3. Step 3

Note what is off the record and must not be used.
### 4. State the fairness check

who else should be asked.
### 5. Step 5

Set length and deadline.
### 6. Step 6

Do not brief a piece whose method is deception or impersonation.

## Output

Deliver a **editorial brief**.

- Purpose of this editorial brief, in two sentences.
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

Jonah Ellis, assignment editor at Foothills Desk in Calgary, needs an editorial brief by 30 September 2026. A brief says to write a quote from a CEO who has not spoken.

### Example data

```text
From: Jonah Ellis, assignment editor
Organization: Foothills Desk, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A brief says to write a quote from a CEO who has not spoken.

The reader: Jonah Ellis plus two others named in the thread. No distribution list attached
The news or point: A brief says to write a quote from a CEO who has not spoken
Sources on hand: note from Jonah Ellis, 14 September 2026. No outside report
What is off the record: one file, dated 14 September 2026. No earlier version attached for comparison
```

### Example outcome

**Editorial brief**
To: Jonah Ellis, assignment editor, Foothills Desk
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Replaces the quote with a request for a real interview.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The reader | Jonah Ellis plus two others named in the thread. No distribution list attached | Needs confirmation |
| The news or point | A brief says to write a quote from a CEO who has not spoken | Carried into the draft |
| Sources on hand | note from Jonah Ellis, 14 September 2026. No outside report | Carried into the draft |
| What is off the record | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |

**How this draft was built**

**1. Write the point in one sentence**

**2. List sources they have. Do not plan a quote you will invent**

**3. Note what is off the record and must not be used**

**4. State the fairness check**  
who else should be asked.

**5. Set length and deadline**

**Deliberately not done**
- Planned fabricated quotes.
- Ignoring off-the-record.
- Impersonation.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Ellis by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Planned fabricated quotes
- Ignoring off-the-record
- Impersonation

## Related skills

- `writing-brief`
- `pr-pitch`
