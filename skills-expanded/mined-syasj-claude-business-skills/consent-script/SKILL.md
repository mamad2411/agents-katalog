---
name: consent-script
description: "Draft the words a participant hears before they agree, from the study facts the user has. Use when the user mentions consent script, participant consent, verbal consent, information sheet, or asks for a consent script. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'consent-script' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Consent Script

Draft the words a participant hears before they agree, from the study facts the user has.

## When to use this skill

Use this skill when the user:

- consent script
- participant consent
- verbal consent
- information sheet

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What the person will be asked to do
- What is recorded
- How they can stop
- What the user cannot promise

## Workflow


### 1. Step 1

Say the task and the time.
### 2. Step 2

Say what is recorded.
### 3. Step 3

Say they can stop.
### 4. Step 4

Do not promise confidentiality the design cannot keep.
### 5. Step 5

Do not hide a risk they named.
### 6. Step 6

This is a draft for the ethics owner, not an approval.

## Output

Deliver a **consent script**.

- Purpose of this consent script, in two sentences.
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

Nia will record 30-minute interviews. Two researchers will hear the audio. A draft script says nobody will know who spoke.

### Example data

```text
task: one interview, 30 minutes, about hiring
recorded: audio
who hears it: Nia and one co-researcher
stop: they can stop at any time, recording deleted if they ask before publication
cannot promise: that a quote will be unrecognizable to their own staff
ethics owner: the college board, not this script
```

### Example outcome

**Words they hear**
This is a 30-minute interview about hiring. I will record audio.
Nia Okonkwo and one co-researcher will hear it. I cannot promise your staff would not recognize a detailed story.
You can stop at any time. If you ask before publication, the recording is deleted.
This script is not the ethics approval. The board still has to accept the study.

**Removed**
"Nobody will know who spoke." The recording and the small staff make that false.

## Anti-patterns

- A promise of anonymity the recording breaks
- Hidden recording
- A script that is also the ethics approval

## Related skills

- `ethics-review-prep`
- `interview-guide-research`
